files:
- src/rsb/model.py
- src/rsb/render.py
- src/rsb/web/dashboard.js
- src/rsb/web/dashboard.css
- test/rsb_tests/fixtures.py
- test/rsb_tests/test_model.py
- test/rsb_tests/test_render.py
- test/rsb_tests/test_webserver.py
- docs/issue-34/decisions/owner-name-wire-format.md

## Request

이슈·PR 번호에서 GitHub 으로 바로 이동할 수 있게 한다. 선행 조건: `flows
--json` 페이로드 최상위 `repo` (owner/name, flows-schema.md §1)가 `rsb`
정규화 단계에서 버려지고 있어 링크를 만들 수 없다 — owner/name 을
모델에서 화면까지 관통시키는 것이 실제 작업이고, 링크 마크업은 그
위에 얹는다. 대상: Decision queue/Flows/Sessions/Accounting 네 표의
이슈 번호(모두) + Decision queue 의 PR 번호 + Flows 의 PRs 열. 접근성
(`<a href>`, 키보드 충돌 없음), owner/name 부재 시 텍스트로만 표시(깨진
링크 금지)가 수용 기준에 포함.

## Constraints

- `schema_version` 변경 불필요 — 공급자는 이미 `repo` 필드를 주고
  있다(모든 테스트 픽스처에 이미 존재, survey §1). 소비자 쪽만 고친다.
- 필터·조인 키는 짧은 이름(`repo_name`, config `name`)에 계속 묶여
  있어야 한다 — issue #29 의 `filterByRepo`/`repoList`/레포 필터
  `<select>` 가 전부 이 짧은 이름으로 동작한다(survey §4). owner/name 은
  이를 대체하지 않고 병행 유지한다.
- Issue 셀은 issue #23/#29 가 이미 만든 disclosure `<button
  class="row-toggle">` 다(survey §4) — 같은 자리에 링크를 겹치면 클릭
  의미가 모호해진다는 것이 이슈 본문 자체의 경고이자, scout-brief 의
  must-be(분리된 형제 컨트롤)와 일치한다.
- `render.py`(CLI 텍스트 렌더러)는 범위 밖 — issue #23/#29 와 동일 로직
  (survey §3).
- GitHub API 추가 호출 없음 — 번호로 URL 을 조립할 뿐(이슈 본문 자체
  명시).
- PR 본문에 closing 키워드 금지, 백틱 인용도 파싱됨(issue #23 T2).
- 새 런타임 의존성 없음, 빌드 스텝 없는 순수 JS 유지(기존 관례).

## Rationale

**owner/name 을 어디에 둘지 — 레코드마다 내장 vs. 병행 lookup map.**
Alternative considered and rejected: 레코드(Decision/Flow/Session/
LedgerEntry 등 8개 dataclass) 각각에 `owner_name` 필드를 직접 추가하는
방법. Rejected because 레포당 하나뿐인 문자열을 레코드마다 중복시켜
JSON 페이로드를 불필요하게 부풀리고, 8개 dataclass 생성자 전부를
건드려야 한다. Instead of that, `merge_repos()` 가 이미 쓰고 있는
`generated_at_by_repo: dict[short_name, str]` 패턴(survey §2)을 그대로
재사용해 `owner_name_by_repo: dict[short_name, owner/name]` 하나만
추가한다 — AC1("각 레코드에서 owner/name 을 얻을 수 있다")은 레코드의
`repo`(짧은 이름)로 이 맵을 조회하는 것으로 충족되고, 짧은 이름을 대체할
필요도 없어 필터·조인 키 제약을 자동으로 만족한다.

**링크 위치 — 버튼 옆 별도 앵커 vs. 버튼에 링크를 씌우거나 행 전체를
링크화.** Alternative considered and rejected: 버튼을 `<a>` 로
감싸거나(인터랙티브 요소 중첩, 유효하지 않은 HTML) 행 전체를 GitHub 로
이동시키는 방법. Rejected because 기존 클릭 시맨틱을 다시 모호하게
만들기 때문 — issue #23 가 없앤 바로 그 문제의 재발이다. Rather than
that, scout-brief 의 3개 독립 검색 각도(Adrian Roselli 의 expando-table
패턴, GitLab 자체의 "행 식별자 옆에 아이콘/링크" 관례, W3C APG 버튼
패턴)가 모두 "분리된 형제 컨트롤" 로 수렴한 것을 따라, 기존
`row-toggle` 버튼 바로 뒤에 별도의 작은 `<a class="external-link">` 를
추가하는 쪽을 택한다.

## What will be done

**Python (와이어 관통):**
- `model.py`: `normalize_payload()`가 반환하는 dict 에
  `"owner_name": payload.get("repo")` 를 추가(§1 항목 나열에 한 줄
  추가, 8개 dataclass 는 무변경). `BoardModel` 에
  `owner_name_by_repo: dict = field(default_factory=dict)` 추가.
  `merge_repos()`가 `generated_at_by_repo` 를 채우는 바로 옆 줄에
  `model.owner_name_by_repo[repo_name] = normalized["owner_name"]` 추가
  (owner/name 이 없거나 문자열이 아니면 `None`/원값 그대로 저장 — 프런트
  헬퍼가 falsy 를 "링크 없음"으로 처리, 파이썬 쪽은 검증하지 않음).
- `render.py`: `render_json_model()` 출력 dict 에
  `"owner_name_by_repo": model.owner_name_by_repo` 한 줄 추가.
- `webserver.py`: 무변경 — 이미 `render_json_model()` 을 통해서만
  직렬화한다(survey §3).

**JS (링크 렌더링), `dashboard.js`:**
- 순수 헬퍼 2개 추가(기존 `buildPlanSteps`/`filterByRepo` 와 같은
  `module.exports` 관례로 `node -e` 커버리지 받음):
  `buildGithubUrl(ownerName, kind, number)` (`kind`: `"issues"` |
  `"pull"`; `ownerName` 이 falsy/비문자열이면 `null` 반환) 과
  `externalLinkHtml(ownerName, kind, number, label)` (URL 이 `null` 이면
  `""` 반환 — AC5; 아니면 `escapeHtml()` 로 이스케이프한 `href`/
  `aria-label` 을 가진 `<a class="external-link" target="_blank"
  rel="noopener noreferrer"><span aria-hidden="true">↗</span></a>` 반환).
- `issueToggleCell(sourceTable, issue, repo, ownerName)` 에 4번째 인자
  추가 — 기존 버튼 마크업 뒤에
  `externalLinkHtml(ownerName, "issues", issue, \`Open issue ${issue} on GitHub\`)`
  를 이어붙인다. 이 함수는 `decisionRows`/`flowRows`/`sessionRows`/
  `renderAccounting` 네 곳에서 이미 재사용되고 있어(survey §4), 이 한
  곳만 고치면 이슈 링크가 네 표 전부에 반영된다(AC2).
- PR 셀 전용 헬퍼 `prCellHtml(ownerName, prNumbers)` 추가 — 빈 배열/
  falsy 는 기존처럼 `"-"`, 아니면 각 PR 번호를 `<span class="mono">`
  + `externalLinkHtml(ownerName, "pull", pr, ...)` 로 매핑해 `", "` 로
  join. `decisionRows`의 PR `<td>`(`dashboard.js:219`)와 `flowRows`의
  PRs `<td>`(`dashboard.js:256`)를 이 헬퍼 호출로 교체(AC3).
- `renderData()` 에서 `data.owner_name_by_repo` 를 꺼내 위 네 row 빌더
  호출에 전달. `filterByRepo()` 는 무변경 — 이미 `{...data, ...}` 로
  나열하지 않은 키를 그대로 통과시킨다(survey §4).
- `dashboard.css`: `.external-link` 클래스 추가(마진은 `--space-1`,
  색은 `--color-text-secondary`/hover·focus 시
  `--color-action-primary-background`, `.row-toggle`과 동일한
  `:focus-visible` 아웃라인) — 기존 `design-system.md` 토큰만 사용,
  새 토큰 없음(survey §5).

**테스트:**
- `test_model.py`: `normalize_payload()` 반환값에 `owner_name` 키
  검증(정상/누락 두 경우) 추가; `merge_repos()` 가
  `owner_name_by_repo` 를 올바르게 채우는 테스트 추가.
- `test_render.py`: `render_json_model()` 출력에 `owner_name_by_repo`
  키가 있는지 검증 추가.
- `test_webserver.py`: `/api/board.json` 응답에 `owner_name_by_repo`
  가 실려 오는지 스팟체크 추가(필요 시).
- `fixtures.py`: AC5(owner/name 부재) 커버용으로 `repo` 키가 없거나
  `None` 인 페이로드 변형을 기존 픽스처에서 파생(dict 복사 + 키
  제거/치환)해 추가.

**문서 (doctrine ladder):**
- `docs/issue-34/decisions/owner-name-wire-format.md` — `board.json` 에
  `owner_name_by_repo` 필드가 새로 추가된다는 와이어 포맷 변경을
  기록(phase 2, implementation.md 레코드와 함께 커밋).

**수동 검증:** `rsb serve` 로컬 구동 후 브라우저에서 네 표 모두 이슈
링크가 정확한 `https://github.com/<owner>/<name>/issues/<n>` 로,
Decision queue/Flows 의 PR 번호가 `.../pull/<n>` 로 이동하는지, 키보드
탭 순서가 `row-toggle` 과 충돌 없이 두 컨트롤을 모두 통과하는지, 상세
패널 열기/닫기가 회귀 없는지 확인.

## Out of scope

- `render.py`(CLI) 링크 — issue #23·#29 와 동일 로직으로 대상 아님(이슈
  본문 명시).
- GitHub API 추가 호출로 제목·상태 등을 끌어오는 것 — 번호로 URL 조립만
  (이슈 본문 명시).
- 상세 패널(`renderDetailPanel`/`renderPlanSection`) 내부에 별도 링크
  추가 — 수용 기준이 요구하는 4개 표 + PR 셀에만 한정, 상세 패널은
  이미 해당 표의 링크를 통해 도달 가능하므로 중복 추가하지 않는다.
- owner/name 이 유효한 `owner/name` 형식인지 서버 쪽에서 검증하는 것 —
  기존 코드베이스가 `stage`/`role` 등 다른 문자열 필드도 형식 검증 없이
  그대로 통과시키는 것과 동일한 관례를 따른다; 프런트 헬퍼의 falsy 체크
  만으로 AC5 를 충족한다.

## How you'll know it worked

- `python -m pytest test/` 전부 통과(기존 33개 + 신규 테스트, 회귀
  없음 — AC "기존 테스트 전부 통과").
- 신규 순수 함수(`buildGithubUrl`, `externalLinkHtml`, 갱신된
  `issueToggleCell`)를 `node -e`로 개별 호출해 owner/name 있음/없음
  두 경우의 출력 문자열을 직접 확인.
- 브라우저 수동 검증(위 "수동 검증" 항목)으로 6개 수용 기준(owner/name
  획득 가능, 이슈 링크, PR 링크, 상세 패널 회귀 없음, owner/name 부재
  시 깨진 링크 없음, 기존 테스트 통과)을 하나씩 확인.
- PR 본문에 `Closes #34` 류 closing 키워드가 없는지(백틱 인용 포함)
  제출 직전 재확인.
