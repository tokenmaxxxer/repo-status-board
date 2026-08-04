files:
- src/rsb/web/dashboard.js
- src/rsb/web/dashboard.css
- test/rsb_tests/test_model.py
- docs/specs/design-system.md
- docs/specs/screen-spec.md

## Request

Decision queue/Flows/Sessions/Accounting 네 표의 이슈 번호와 Decision
queue/Flows 의 PR 번호를 issue #34 의 ↗ 아이콘 대신 `#<n>` 텍스트의 파란
`<a href>` 로 바꾼다. 이슈 셀은 지금 그 번호 자체가 상세 패널을 여는
`<button class="row-toggle">` 의 라벨이므로, 번호가 링크가 되는 순간
disclosure 트리거를 같은 셀 안 다른 자리로 옮겨야 한다 — 기존
`aria-expanded`/`aria-controls`/키보드 조작 시맨틱은 유지하고, 행 전체
클릭으로 되돌리지 않는다. owner/name 이 없는 레코드는 링크 없이 `#<n>`
텍스트만 표시(issue #34 와 동일 정책 확장). `design-system.md`/
`screen-spec.md` 를 실제 구현에 맞게 갱신한다.

## Constraints

- 새 디자인 토큰 추가 금지 — `color-action-primary-background`
  (`--color-blue-500`) 재사용(design-system.md:61 이 이미 "links" 를
  용도로 명시).
- `render.py`(CLI 텍스트 렌더러)는 범위 밖 — issue #23/#29/#34 와 동일
  로직(survey §6).
- GitHub API 추가 호출 없음, 새 런타임 의존성 없음, 빌드 스텝 없는 순수
  JS 유지(기존 관례, survey §6).
- 필터·조인 키(`repo` 짧은 이름)에 영향 없음 — 이 변경은 렌더링 계층만
  건드리고 `filterByRepo`/`repoList`(issue #29)에는 손대지 않는다.
- PR 본문에 closing 키워드 금지(백틱 인용 포함, issue #23 T2).
- 상세 패널을 실제로 여는 유일한 컨테이너는 `#detail-panel-slot`
  하나뿐이다(survey §2) — 테이블마다 다른 컨테이너를 만들지 않는다.

## Rationale

**트리거 위치 — 셀 안 선두 버튼 vs. 새 전용 열.** Alternative
considered and rejected: Carbon Design System 이 채택한 것처럼 4개 표
전부에 전용 "expand" 열을 새로 추가하는 방법(scout-brief 가 실제
찾아낸, 업계에 존재하는 대안). Rejected because 이 변경의 실제 필요는
"번호와 트리거가 같은 텍스트를 공유할 수 없다"는 것 하나뿐이고, 전용
열 추가는 4개 표의 헤더·열 목록·`screen-spec.md` §1.3-§1.7 전부를
구조적으로 바꾸는 훨씬 큰 변경이다. scout-brief 의 segment-fit 판단대로
이 보드는 내부용 소형 대시보드이지 Carbon 급 그리드 시스템이 필요한
제품이 아니다. Instead, 기존 Issue `<td>` 안에서 토글 버튼을 아이콘
전용으로 줄이고 링크 앞에 선두 배치한다 — scout-brief 의 4개 각도가
모두 수렴한 "분리된 형제 컨트롤 + 선두 위치"(W3C APG 포럼 논의: 스크린
리더 사용자가 토글 직후 아래 화살표로 새로 드러난 내용을 바로 읽을 수
있어야 한다는 이유)를 그대로 따른다.

**aria-controls/aria-expanded 배선 — 기존 버그를 그대로 재현 vs. 이
편집 안에서 고치기.** Alternative considered and rejected: 기존
`rowToggleId`/`sourceTable` 미배선을 그대로 둔 채 버튼 마크업만 옮기는
것. Rejected because 이 두 함수(`issueToggleCell`, 관련 클릭 핸들러)를
어차피 다시 쓰는 이 작업에서 그대로 재현하면, 새로 추가하는 `▸`/`▾`
글리프의 펼침 상태 자체가 절대 반영되지 않는 채로 배포된다(survey
§2 — `selectedIssue.sourceTable` 이 지금 항상 `undefined` 라 `isRowExpanded`
가 항상 `false`). 글리프 상태가 실제로 동작하려면 이 배선을 고치는
수밖에 없다 — "기존 시맨틱 유지"는 버튼이 실제로 펼침 상태를 반영하는
것을 뜻하지, 항상 `false` 를 렌더링하는 깨진 상태를 그대로 옮기는 것을
뜻하지 않는다고 판단한다. `aria-controls` 도 존재하지 않는
`detail-row-*` id 대신 실제 유일한 컨테이너 `#detail-panel-slot` 을
가리키도록 고친다(같은 이유). 좁은 화면 전용 인라인 확장 행
(`insertDetailRow`, screen-spec.md §1.6 이 문서화했지만 구현되지 않은
기능, survey §2)을 새로 구현하는 것은 이번 이슈가 요구하지 않은 훨씬
큰 별도 작업이라 범위 밖으로 남긴다 — 지금 유일하게 존재하는 컨테이너
하나를 정확히 가리키게 고치는 것과, 존재하지 않는 두 번째 렌더링
경로를 새로 만드는 것은 다른 크기의 작업이다.

## What will be done

**`dashboard.js`:**
- `externalLinkHtml` 를 `numberLinkHtml(ownerName, kind, number)` 로
  교체(순수 함수, 기존 `buildGithubUrl` 재사용): `buildGithubUrl` 이
  `null` 이면 `escapeHtml('#' + number)` 평문 반환(AC4 — 깨진 링크
  없음); 아니면 `<a class="number-link" href="${url}" target="_blank"
  rel="noopener noreferrer">#${number}</a>`(새 탭 유지, issue #34 관례
  그대로 — 별도 `aria-label` 없이 링크 텍스트 `#<n>` 자체를 접근성
  이름으로 사용, 열 헤더가 이슈/PR 을 구분해줌).
- 새 순수 함수 `rowToggleButtonHtml(sourceTable, issue, repo, expanded)`:
  `<button type="button" class="row-toggle" aria-expanded="${expanded}"
  aria-controls="detail-panel-slot" aria-label="Toggle details for issue
  ${issue}" data-issue="${issue}" data-repo="${escapeHtml(repo)}"
  data-table="${sourceTable}"><span aria-hidden="true">${expanded ? "▾" :
  "▸"}</span></button>` 반환.
- `issueToggleCell(sourceTable, issue, repo, ownerName)`: `isRowExpanded`
  로 펼침 여부를 구해 `rowToggleButtonHtml` 호출 결과와
  `numberLinkHtml(ownerName, "issues", issue)` 를
  `<span class="issue-cell">...</span>` 로 감싸 반환(줄바꿈 방지 컨테이너,
  AC2). 버튼이 링크보다 먼저 온다(선두 배치).
- `rowToggleId` 함수 제거(더 이상 어떤 호출자도 없음 — `aria-controls`
  가 고정 문자열 `"detail-panel-slot"` 이 됨).
- `prCellHtml(ownerName, prNumbers)`: `externalLinkHtml` 호출을
  `numberLinkHtml` 호출로 교체, `<span class="mono">${prNumber}...</span>`
  래핑을 `<span class="mono">${numberLinkHtml(...)}</span>` 로 단순화
  (PR 셀엔 disclosure 컨트롤이 없어 셀 구조 자체는 변하지 않는다).
- `attachRowClickHandlers(data)` → `attachRowToggleHandlers(data)` 로
  교체: `MAIN.querySelectorAll(".row-toggle")` 에 대해서만
  클릭 리스너를 붙인다(더 이상 `tr[data-issue]` 전체가 아님 — AC3 이
  요구하는 "행 전체 클릭 없음"을 직접 보장). 핸들러는 버튼의
  `data-issue`/`data-repo`/`data-table` 을 읽어, 이미 펼쳐진 바로 그
  버튼이면 `selectedIssue = null`(접기), 아니면 `{ issue, repo,
  sourceTable }` 로 설정(펼치기/다른 행으로 전환) 후 `renderData(data)`
  재호출. `renderData()` 안의 호출부도 `attachRowToggleHandlers(data)`
  로 교체.
- `dashboard.js:15,187` 의 존재하지 않는 `insertDetailRow()` 를 가리키는
  주석 2곳을 실제 동작(유일한 컨테이너는 `#detail-panel-slot`)에 맞게
  정정.
- `module.exports`: `externalLinkHtml` 를 `numberLinkHtml` 로 교체.

**`dashboard.css`:**
- `.external-link` 규칙(및 `:hover`/`:focus`/`:focus-visible`) 삭제.
- `.number-link` 추가: `color: var(--color-action-primary-background);
  text-decoration: none;`, `:hover`/`:focus` 시 `text-decoration:
  underline;`, `:focus-visible` 은 `.row-toggle` 과 동일한
  `outline: 2px solid var(--color-blue-500); outline-offset: 2px;`.
- `.issue-cell` 추가: `display: inline-flex; align-items: center; gap:
  var(--space-1); white-space: nowrap;`(AC2 의 직접적 원인 수정 —
  survey §4).
- `.row-toggle` 은 유지하되 주석을 아이콘 전용 버튼으로 정정(글리프만
  담는다는 사실 반영). 색상/포커스 규칙은 기존 그대로 재사용.

**테스트 (`test/rsb_tests/test_model.py`):**
- `numberLinkHtml('a/b', 'issues', 42)` → 정확한 `<a class="number-link"
  href="https://github.com/a/b/issues/42" ...>#42</a>` 문자열 검증.
- `numberLinkHtml(null, 'issues', 42)` → `"#42"` 평문(HTML 이스케이프,
  `<a>` 없음) 검증 — AC4.
- 기존 33개+`buildPlanSteps`/`filterByRepo` 계열 테스트는 무변경으로
  통과해야 한다(회귀 없음 확인용, 새 함수만 추가하고 기존 export 는
  이름만 바뀜).

**문서 (doctrine ladder):**
- `docs/specs/screen-spec.md` §1.3: Issue 셀 서술을
  "선두 아이콘 전용 `row-toggle` 버튼(▸/▾, `aria-expanded`,
  `aria-controls="detail-panel-slot"`) + 뒤따르는 `#<n>` 링크
  (`color-action-primary-*`, owner/name 없으면 평문)" 로 갱신, PR
  컬럼에도 동일 링크 규칙 한 줄 추가. §1.4/§1.5/§1.7 은 기존 관례대로
  "§1.3 과 동일 패턴" 참조로 갱신.
- `docs/specs/design-system.md` §6 component inventory: `DataTable` 행
  또는 새 행에 `.number-link`(`color-action-primary-*`)/아이콘 전용
  `.row-toggle` 갱신 사실 반영.

**수동 검증 (phase 2):** `rsb serve` 로컬 구동 후 네 표 모두 `#<n>` 파란
링크가 정확한 GitHub URL 로 새 탭에서 열리는지, Flows 표에서 Issue
셀이 줄바꿈 없이 한 줄인지, `row-toggle` 버튼을 Tab 으로 포커스해
Enter/Space 로 펼치고/접을 수 있는지(같은 버튼 두 번째 활성화 시
접힘), owner/name 없는 레코드가 `#<n>` 평문으로만 보이는지 확인.

## Out of scope

- 좁은 화면(< `breakpoint-lg`) 인라인 확장 행(`insertDetailRow`) 신규
  구현 — `screen-spec.md` §1.6/`design-system.md` §5 가 문서화했지만
  구현되지 않은 기존 gap(survey §2)이며, 이슈 본문이 요구하는 것은
  "기존 시맨틱 유지"이지 이 두 번째 렌더링 경로를 새로 만드는 것이
  아니다.
- `WIDE_LAYOUT_QUERY`(`dashboard.js:16`, 정의되었으나 `matchMedia` 등
  어디서도 쓰이지 않는 죽은 상수) 정리 — 이번에 다시 쓰는 함수들과
  무관한 별개의 기존 gap.
- `render.py`(CLI) 링크 — issue #23/#29/#34 와 동일 로직으로 대상 아님.
- GitHub API 추가 호출로 제목·상태 등을 끌어오는 것 — 번호로 URL
  조립만.
- 이슈/PR 링크의 새 탭 여부를 같은 탭으로 바꾸는 것 — issue #34 가 이미
  결정한 관례를 유지, 재논의하지 않는다.

## How you'll know it worked

- `python -m pytest test/` 전부 통과(기존 53개 + 신규 `numberLinkHtml`
  테스트 2개, 회귀 없음).
- `node --check src/rsb/web/dashboard.js` 문법 검사 통과.
- `node -e` 로 `numberLinkHtml`/`buildGithubUrl` 을 owner/name 있음/없음
  두 경우 직접 호출해 출력 문자열 확인.
- 브라우저 수동 검증(위 "수동 검증" 항목)으로 7개 수용 기준(파란
  `#<n>` 링크, GitHub 이동, Flows 한 줄 표시, 키보드만으로 열고 닫기,
  owner/name 없음 시 평문, 기존 테스트 통과, 스펙-구현 일치)을 하나씩
  확인.
- PR 본문에 closing 키워드(백틱 인용 포함) 없는지 제출 직전 재확인.
