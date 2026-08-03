files:
- src/rsb/fetch.py
- src/rsb/cli.py
- src/rsb/web/index.html
- src/rsb/web/dashboard.js
- src/rsb/web/dashboard.css
- docs/specs/design-system.md
- docs/specs/screen-spec.md
- test/rsb_tests/test_fetch.py
- test/rsb_tests/test_cli.py

## Request

멀티 레포를 실사용 가능하게 만드는 5개 요구사항 묶음(issue #29): (1)
`fetch.py`의 직렬 수집을 병렬화하고 15초 타임아웃을 실측(26.7초, 3레포
기준) 여유를 두고 상향 + CLI로 조정 가능하게, (2) 상단 네이티브
`<select>` 레포 필터로 표/요약 칩을 클라이언트에서 재계산, (3) `Repo`
열을 모든(대시보드) 표의 첫 열로 통일 + 표별 가로 스크롤만 허용(모바일
카드 UI 없음), (4) 실패 배너를 `N of M repos failed` + 접힌 `<details>`
로 단순화, (5) 클릭 가능한 `<tr>` 대신 Issue 셀의 실제 `<button>`으로
행 상세를 열고 좁은 화면에서는 선택 행 바로 아래에 펼친다(issue #23
execution-observation이 지적한 클릭 전용 문제의 처방). 트리거는 issue
#27 프리뷰를 로컬에서 돌리다 발견된 실측 결함 — 3레포 중 가장 느린
레포(26.7초)가 15초 캡에서 잘려 보드의 2/3만 뜨는 상태.

## Constraints

- `flows --json`의 데이터 계약(`docs/specs/flows-schema.md`)은 무변경 —
  이 이슈는 `rsb` 쪽 수집/렌더링 동작만 바꾼다. 타임아웃값은 애초에
  스펙 문서 어디에도 없는 `rsb` 자체 운영 선택(survey §1 확인)이라
  스펙 재동기화 대상이 아니다.
- 기존 pytest 33개 전부 통과해야 함(회귀 없음) — 단, `test_cli.py`가
  `cli.fetch_board`를 단일 인자 람다로 monkeypatch하는 기존 패턴은 새
  `timeout` 키워드 인자 추가로 인해 그 람다들 자체를 갱신해야 한다(이는
  회귀가 아니라 시그니처 변경에 따른 예정된 테스트 갱신 — survey §6에서
  미리 확인한 리플).
- 이 레포에는 JS 테스트 하네스가 없다(issue #23 phase-1이 범위 밖으로
  확정, survey §6). 새로 들이지 않는다 — DOM을 만지는 로직(select
  wiring, 버튼 핸들러, 행-인접 패널 삽입)은 수동 검증에 남고, 순수
  함수만 기존 `module.exports` 가드를 통해 `node -e` 테스트 커버리지를
  받는다.
- PR 본문에 closing 키워드 금지, 백틱 인용도 파싱됨(issue #23 T2 —
  이슈 본문 자체의 경고).
- 새 런타임 의존성 없음 — 표준 라이브러리 `concurrent.futures.
  ThreadPoolExecutor`/`functools`만 사용, 프런트엔드도 기존처럼 빌드
  스텝 없는 순수 JS 유지.
- `docs/specs/design-system.md` §7 / `screen-spec.md` §5가 "still
  deferred"로 명시한 인증/접근 모델, auto-refresh는 이 이슈가 재론하지
  않는다.

## Rationale

**병렬화 결과 취합 — `ThreadPoolExecutor.map()` vs.
`submit()`+`as_completed()`.** 채택안: `.map()`.

Alternative considered and rejected: `submit()` + `as_completed()`
(완료 순서대로 결과 취합). Rejected because — `merge_repos()`
(model.py:279-304)는 `decisions`/`flows`/`sessions`/`ledger`만
명시적으로 재정렬하고, `errors`/`unattributed`/`closure_sweep`/
`unapproved_open_prs`/`generated_at_by_repo`는 입력 순서 그대로
누적한다(survey §1). 오늘의 순차 코드는 이 네 필드의 순서가 항상
`repo_configs` 순서로 결정적인데, `as_completed()`로 바꾸면 이 순서가
매 실행마다 "어느 레포가 먼저 끝났는가"에 좌우되어 비결정적이 된다.
`.map()`은 입력 순서를 그대로 보존하면서 병렬 실행하므로, 추가 코드
없이 오늘과 같은 결정성을 그대로 유지한다.

**타임아웃 조정 방식 — 전역 CLI 플래그 vs. `RepoConfig`에 레포별
필드 추가.** 채택안: 전역 `--timeout SECONDS` CLI 플래그(기본값 =
새 `DEFAULT_TIMEOUT_SECONDS`).

Alternative considered and rejected: `[[repo]]` TOML 항목에 레포별
`timeout` 필드 추가(`roles`/`prs`처럼 optional 필드로). Rejected
because — 이슈 본문의 실측 표를 보면 느린 레포(on-the-record, 26.7초)는
그 레포 고유의 고정 특성이 아니라 현재 flow/이슈 개수가 많아서 생긴
결과다(시간이 지나면 다른 레포가 느려질 수도 있다). 레포별 고정값을
config에 박아두면 보드가 자랄 때마다 수동 재조정이 필요해지고,
`RepoConfig` 데이터클래스 필드 추가 + `config.py` 파싱/검증 +
`test_config.py` 커버리지까지 스키마 표면이 늘어난다. 전역 플래그
하나로 "지금 느린 레포가 어디든" 여유를 준 뒤 필요할 때만
`--timeout`으로 조정하는 편이 이슈가 요구하는 "실측 여유 포함 상향 +
필요시 조정 가능"을 더 적은 표면으로 만족시킨다.

**기본 타임아웃 값 — 60초 vs. 실측치(26.7초)에 근접한 타이트한
마진(예: 30초).** 채택안: 60초(≈2.25배 마진).

Alternative considered and rejected: 30초(실측 최대치의 ~1.1배).
Rejected because — 이슈 본문의 표는 "2026-08-03 기준, 보드 3개 기준"이라
명시된 스냅샷이지 상한이 아니다. `flows --json` 소요 시간은 이슈/PR이
쌓일수록 늘어날 개연성이 높고, 타이트한 마진은 며칠 안에 다시 잘릴 위험이
크다. 60초는 근시일 성장을 흡수하면서도, 그래도 부족하면 `--timeout`
플래그가 코드 변경 없는 탈출구로 남는다.

**행 상세 펼침(요구사항 5) — 좁은 화면에서 클릭한 표의 행만 펼칠지, 같은
이슈 번호가 걸리는 모든 표의 행을 동시에 펼칠지.** 채택안: 클릭한
표(`sourceTable`)의 행만.

Alternative considered and rejected: 동일 `(issue, repo)`가 나타나는
모든 표(decisions/flows/sessions/ledger)의 행을 동시에 펼침. Rejected
because — 스카우트 결과(WAI-ARIA APG disclosure 패턴, scout-brief.md)의
전제는 버튼 하나가 자신에게 인접한 패널 하나를 제어한다는 1:1 대응이다.
버튼 하나를 눌렀는데 화면 멀리 떨어진 다른 표의 행까지 동시에 펼쳐지면
이 대응이 깨지고, 사용자가 예상 못 한 위치에서 레이아웃이 뛴다. 클릭한
행 하나만 펼치는 편이 접근성 패턴과 사용자 기대 모두에 맞는다.

**실패 배너 단순화(요구사항 4) — `PartialFailureBanner`만 vs.
전체 실패 시의 `ErrorState`(풀페이지)도 함께 접을지.** 채택안:
`PartialFailureBanner`만.

Alternative considered and rejected: `renderFullError()`가 그리는
풀페이지 에러 상태의 메시지 목록도 같은 `<details>` 패턴으로 접음.
Rejected because — `design-system.md` §6 컴포넌트 인벤토리가
`PartialFailureBanner`와 `ErrorState`를 별개 컴포넌트로 구분하고,
이슈 본문의 "실패 배너"라는 표현은 전자를 가리킨다. 풀페이지 상태는
화면에 다른 콘텐츠가 없어 상세 에러 목록이 화면을 어지럽히는 문제(배너가
있는 부분 실패 상태와 달리) 자체가 없어 같은 처방을 적용할 이유가 약하다.

**표 반응형 처리(요구사항 3) — 순수 가로 스크롤 vs. Repo 열
sticky-column 추가.** 채택안: 순수 `overflow-x: auto` 스크롤, sticky
없음.

Alternative considered and rejected: `position: sticky; left: 0`으로
Repo 열 고정(scout-brief.md가 소개한 CSS-Tricks 패턴). Rejected because
— 이슈의 수용 기준은 "표별 가로 스크롤만 허용"이지 열 고정을 요구하지
않는다. sticky 열은 스크롤 중 다른 셀이 비쳐 보이지 않도록 배경색을
명시적으로 지정해야 하는 실제 구현 비용이 있다(스카우트 소스가 직접
지적) — 요구되지 않은 기능에 그 비용을 들일 이유가 없다.

**Repo 열 통일 범위 — 대시보드(HTML)만 vs. `render.py`(CLI 텍스트
렌더러)까지.** 채택안: 대시보드만.

Alternative considered and rejected: `render.py`의 `_table()` 호출들도
같이 Repo-first로 재정렬. Rejected because — 요구사항 3의 문구("모바일",
"가로 스크롤")는 웹 대시보드에서만 의미가 있는 개념이고 터미널
렌더러에는 대응 개념이 없다. issue #23이 `plan` 렌더링을 "터치포인트에
CLI 출력이 없다"는 이유로 `render.py`를 범위 밖으로 뒀던 것과 동일한
논리 — issue #29도 마찬가지로 대시보드 전용 요구로 읽는다.

## What will be done

1. **`src/rsb/fetch.py`** — `DEFAULT_TIMEOUT_SECONDS`를 15 → 60으로
   상향. `fetch_board(repo_configs, run_json_fn=None,
   timeout=DEFAULT_TIMEOUT_SECONDS)`로 시그니처 변경: `run_json_fn`이
   `None`이면 내부에서 `lambda rc: run_flows_json(rc, timeout=timeout)`을
   구성해 사용(기존 실제-서브프로세스 경로는 그대로, 새 `timeout` 인자만
   반영); 명시적으로 넘겨진 `run_json_fn`(테스트의 fake들)은 그대로
   단일 인자로 호출되어 기존 테스트에 영향 없음. 수집 루프를
   `concurrent.futures.ThreadPoolExecutor(max_workers=len(repo_configs)
   or 1)` + `.map()`으로 교체(Rationale 참조) — `fetch_and_normalize_one`은
   이미 예외를 삼키고 항상 3-tuple을 반환하므로 executor에 그대로 넘겨도
   안전(추가 try/except 불필요).
2. **`src/rsb/cli.py`** — 최상위 `--timeout SECONDS` 플래그 추가
   (기본값 `DEFAULT_TIMEOUT_SECONDS`, `rsb.fetch`에서 import). `_run_once`
   가 `timeout` 인자를 받아 `fetch_board(repo_configs, timeout=timeout)`
   호출(모듈 전역 `fetch_board` 이름을 함수 본문에서 참조 — 기존
   `test_cli.py`의 `monkeypatch.setattr(cli, "fetch_board", ...)` 패턴이
   계속 동작하도록 `_run_once`의 기본 인자로 함수 객체를 바인딩하지
   않는다). `serve` 서브커맨드는 `functools.partial(fetch_board,
   timeout=args.timeout)`을 구성해 `run_server(...)`에 넘긴다(호출 시점에
   전역 `fetch_board` 이름을 참조하므로 monkeypatch와 호환) —
   `webserver.py`는 무변경(survey §1 확인대로 그대로 유효).
3. **`test/rsb_tests/test_cli.py`** — 기존 `monkeypatch.setattr(cli,
   "fetch_board", lambda repo_configs: ...)` 형태의 람다들을 `lambda
   repo_configs, **kwargs: ...`로 갱신(새 `timeout` 키워드를 흡수하되
   기존 단언은 그대로). `--timeout` 파싱 테스트(기본값, 커스텀 값이
   `fetch_board` 호출까지 전달되는지) 추가.
4. **`test/rsb_tests/test_fetch.py`** — 병렬 실행을 증명하는 테스트
   추가: 각 fake `run_json_fn`에 `time.sleep`을 넣고 전체 wall-clock이
   `N * sleep`보다 유의미하게 짧음을 단언. `fetch_board`의 결과 순서가
   `repo_configs` 순서와 일치함을 단언하는 테스트(`.map()`의 순서 보존
   확인, Rationale 참조). `DEFAULT_TIMEOUT_SECONDS == 60` 값 자체와,
   `fetch_board(repo_configs, timeout=N)`이 실제 경로(`run_json_fn=None`)
   에서 `run_flows_json`에 `timeout=N`으로 전달됨을 확인하는 테스트.
5. **`src/rsb/web/index.html`** — `.page-header` 안에 `<select
   id="repo-filter"><option value="">All repos</option></select>`
   추가(기본 선택 "All repos").
6. **`src/rsb/web/dashboard.js`**:
   - fetch된 원본 payload를 모듈 스코프 변수로 승격(현재
     `load()`의 지역 변수), `<select>`의 `change` 리스너가 refetch 없이
     재렌더할 수 있게 함.
   - 순수 함수 `filterByRepo(data, repo)` 추가·`module.exports`에
     등록(node 테스트 커버리지 대상): `repo`가 falsy면 `data`를 그대로,
     아니면 `decisions`/`flows`/`sessions`/`ledger`/`unattributed`/
     `closure_sweep`/`unapproved_open_prs`/`errors`를 `.repo === repo`로
     필터링하고 `generated_at_by_repo`를 해당 키 하나로 좁힌 새 객체를
     반환.
   - `<select>`의 `change` 리스너: `selectedIssue`를 초기화(필터 전환 시
     상세 패널 닫힘 — 다른 레포로 전환했는데 이전 레포의 상세가 남아있는
     비일관 상태를 피함) 후 `renderData(filterByRepo(boardData,
     select.value))` 호출(디바운스 불필요 — `change`는 커밋당 1회만
     발생, scout-brief.md 근거). `load()` 성공 시 `<select>`의 옵션
     목록을 갱신하되 이전 선택값이 여전히 존재하면 유지, 사라졌으면
     "All repos"로 폴백.
   - `flowRows()`/`sessionRows()`/`renderAccounting()`(ledger)의 헤더
     배열과 셀 순서에서 `Repo`를 맨 앞으로 이동(`decisionRows()`가 이미
     따르는 패턴과 통일).
   - `renderTable()`이 반환하는 `<table>` 마크업을 `<div
     class="table-scroll">...</div>`로 감싸도록 변경 — decisions/flows/
     sessions/ledger 네 표 모두 한 지점 수정으로 적용됨.
   - 부분 실패 배너: `${failedRepos.length} of ${total} repos failed to
     load` 문구는 항상 보이는 줄로 유지하고, 레포별 `"{repo}:
     {message}"` 상세는 `<details><summary>Details</summary><ul>...
     </ul></details>`로 감싸 기본 접힘. `#partial-retry` 버튼과 그
     클릭 핸들러는 그대로 유지. `renderFullError()`는 무변경(Rationale
     참조).
   - Issue 셀을 `<button type="button" class="row-toggle"
     aria-expanded="…" aria-controls="detail-row-…" data-issue="…"
     data-repo="…" data-table="decisions|flows|sessions|ledger">${issue}
     </button>`로 교체(4개 표 전부, decisionRows/flowRows/sessionRows/
     ledger 행 빌더 각각).
   - `attachRowClickHandlers`를 `attachRowToggleHandlers`로 교체:
     `button.row-toggle`을 대상으로 클릭 리스너 연결, `selectedIssue`를
     `{issue, repo, sourceTable}`로 확장.
   - 렌더 분기: `matchMedia('(min-width: 1200px)').matches`(기존
     `breakpoint-lg` 값과 동일)면 오늘처럼 `DETAIL_SLOT`에 패널을 쓰고
     표에는 아무 것도 삽입하지 않음. 미만이면 `DETAIL_SLOT`을 비우고,
     `selectedIssue.sourceTable`에 해당하는 표의 선택된 행 바로 다음에
     `<tr class="detail-row"><td colspan="N">…renderDetailPanel(...)…
     </td></tr>`를 삽입(Rationale — 클릭한 표의 행만).
7. **`src/rsb/web/dashboard.css`**:
   - `.table-scroll { overflow-x: auto; }` 추가.
   - `tbody tr { cursor: pointer }`/hover 규칙 제거, `.row-toggle`(버튼
     리셋 스타일 + `:focus-visible` 아웃라인)과 `.detail-row td`(기존
     `.detail-panel`과 시각적으로 맞춤) 규칙 추가.
   - `.partial-banner details`/`summary` 스타일 추가(포인터 커서, 여백).
8. **`docs/specs/design-system.md`** — §5 근처 "Multi-device/mobile
   optimization is out of scope" 문구를 이번 변경(표별 가로 스크롤 지원)
   에 맞게 갱신. §6 컴포넌트 인벤토리에 필터 select(예: `RepoFilter`)
   항목 추가, `PartialFailureBanner` 항목에 `<details>` 사용 명시.
9. **`docs/specs/screen-spec.md`** — §1.3/§1.4/§1.5/§1.7의 "Row click
   opens DetailPanel" 문구를 "Issue-cell button click opens DetailPanel"
   로 갱신. §2.5 배너 Copy 문구를 `"{M} of {N} repos failed to load"`
   (항상 표시) + 접힌 상세로 재동기화. 표 가로 스크롤 + Repo-first 열
   결정을 §1.3–§1.5/§1.7 근처에 명문화.
10. 수동 검증(phase 2, JS 하네스 부재 — Constraints 참조): `rsb serve`
    로 로컬 서버를 띄우고 브라우저에서 (a) 3레포 fixture로 병렬 수집이
    26.7초 케이스를 자르지 않는지, (b) 레포 필터 전환 시 표/칩이
    재계산되는지, (c) 좁은 뷰포트에서 표만 가로 스크롤되고 페이지 본문은
    스크롤되지 않는지, (d) 실패 배너가 요약+접힌 상세로 뜨는지, (e)
    키보드(Tab + Enter/Space)만으로 행 상세를 열고 닫을 수 있는지 직접
    확인.

## Out of scope

- 검색, 탭, 페이지네이션, 캐시, 자동 새로고침(issue 본문이 명시한 범위
  밖).
- `render.py`(CLI 텍스트 렌더러)의 Repo 열 재정렬(Rationale 참조).
- Repo 열 `position: sticky` 고정(Rationale 참조).
- `/api/board.json`에 서버사이드 `?repo=` 쿼리 파라미터 추가 — 요구사항
  2는 클라이언트 재계산으로 명시되어 있고, 서버는 항상 전체 payload를
  주는 현재 동작을 유지한다.
- `renderFullError()`(풀페이지 `ErrorState`)의 메시지 목록 접기
  (Rationale 참조).
- 새 JS 테스트 하네스(jest 등) 도입 — 레포 전역 결정, issue #23이 이미
  범위 밖으로 확정(survey §6).
- `RepoConfig`에 레포별 타임아웃 필드 추가(Rationale 참조) —
  `src/rsb/config.py`, `test/rsb_tests/test_config.py` 무변경.
- 인증/접근 모델, hygiene/sessions/ledger 등 이 이슈와 무관한 스펙
  드리프트 재동기화 — `design-system.md`/`screen-spec.md`는 이 이슈가
  건드리는 항목(모바일/스크롤, 배너, 행-상세 트리거)만 갱신한다.

## How you'll know it worked

- `python3 -m pytest test/ -q` — 기존 33개 전부 통과(갱신된
  `test_cli.py` 람다 포함) + 새 병렬성/타임아웃/`--timeout` 플래그
  테스트 통과.
- 3레포 fixture(느린 레포 `time.sleep`로 시뮬레이션, 26.7초 상당)로
  `fetch_board`의 wall-clock이 직렬 합계(56.1초 상당)가 아니라 가장
  느린 레포 시간에 근접함을 테스트로 확인 — 수용 기준 1번.
- 레포 하나가 실패하도록 만든 fixture로 `fetch_board`가 나머지 레포
  데이터를 그대로 반환함을 기존 `fetch_and_normalize_one`/`fetch_board`
  부분 실패 테스트 패턴으로 확인 — 수용 기준 2번(병렬화 이후에도
  유지됨을 재확인).
- 브라우저 수동 검증(10번 항목)으로 수용 기준 3–6번(필터 재계산, Repo
  첫 열 + 표별 스크롤만, 배너 요약+접힘, 키보드로 행 상세 열기) 확인.
- `docs/specs/design-system.md`/`screen-spec.md`가 실제 구현과
  문구 단위로 일치(모바일/스크롤 문구, 배너 Copy, 버튼 트리거 문구).
- PR 본문에 closing 키워드 없음(직접 확인) — 수용 기준의 마지막 "주의"
  항목.
- 수용 기준 8개 항목 전부 커밋 diff/문서에서 추적 가능.
