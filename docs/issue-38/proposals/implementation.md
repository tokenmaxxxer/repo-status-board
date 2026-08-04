files:
- src/rsb/web/dashboard.js
- src/rsb/web/dashboard.css
- src/rsb/web/index.html
- test/rsb_tests/test_model.py
- docs/specs/screen-spec.md
- docs/specs/design-system.md

## Request

디자인 게이트 P1/P2 재검토(issue #38)가 남긴 P1-1/P1-3/P1-4 및
P2-5/P2-6/P2-7, P3-8 을 처리한다 — P1-2(상세 펼침 배선)는 issue #36
(PR #37, merged) 이 이미 고쳤으므로 범위 밖(survey §0). 구체적으로:
390px 에서 페이지 본문 전체가 가로로 밀리는 오버플로를 표별
`.table-scroll` 스크롤로 되돌리고(P1-1), <1200px 화면에서 상세 패널이
선택 행 바로 아래 `<tr>` 로 나타나도록 실제 구현하고(P1-3, 지금은
주석과 죽은 CSS 만 존재), 로딩·부분/전체 오류·상세 열림에
`aria-live`/`aria-busy`/`role="alert"`/포커스 이동을 배선하고(P1-4),
모바일 인터랙티브 컨트롤을 최소 24×24px 로 키우고(P2-5), 부분/전체
오류를 요약+접힌 상세 구조로 재구성하고(P2-6), 표에 `caption`/
`th[scope=col]` 을 추가하고 선택 행을 시각적으로 구분하고(P2-7), 마지막
으로 Refresh/필터 상태·행 hover/selected·skeleton 높이·outcomes 배지·
neutral border 대비를 정리한다(P3-8). `screen-spec.md`/`design-system.md`
를 실제 구현에 맞게 갱신한다.

## Constraints

- 새 디자인 토큰 추가 금지(issue-34/issue-36 관례 그대로) — 기존
  `color-status-info-*`, `color-neutral-500`, `color-neutral-100` 등
  이미 정의된 토큰만 재사용한다. `--color-border-default` 는 값을
  `--color-neutral-300` → `--color-neutral-500` 로 바꾸지만(대비 개선,
  survey §7) 새 프리미티브를 추가하지 않는다.
- `render.py`(CLI 텍스트 렌더러)와 `webserver.py` 등 백엔드는 범위
  밖 — 이 이슈가 요구하는 것은 프런트엔드(`dashboard.js`/`.css`/
  `index.html`)의 렌더링·접근성 배선이지 서버 응답 스키마 변경이
  아니다(survey §9, issue #23/#29/#34/#36 과 동일 로직).
- 새 런타임 의존성·빌드 스텝 없는 순수 JS 유지, 새 JS 테스트 하네스
  도입 금지 — `test/rsb_tests/test_model.py` 의 기존 `node -e` 셸아웃
  관례만 확장한다(survey §9).
- 필터·조인 키(`repo` 짧은 이름), `owner_name_by_repo` 배선(issue #34/
  #36)에는 손대지 않는다 — 이 변경은 레이아웃·접근성·오류 표시 계층만
  건드린다.
- PR 본문에 closing 키워드 금지(백틱 인용 포함, issue #23 T2).
- P1-2(상세 펼침 자체의 토글 배선)는 issue #36 소관 — 이미 올바르게
  동작하는 `attachRowToggleHandlers`/`isRowExpanded`(survey §0)를
  재작성하지 않고, 오직 그 결과를 렌더링하는 위치(넓은 화면
  `#detail-panel-slot` vs 좁은 화면 인라인 `<tr>`)만 이번에 추가한다.

## Rationale

**모바일 오버플로 — 표 `min-width` + 스크롤 유지 vs. 무제한 축소.**
Alternative considered and rejected: `table.data-table` 에 명시적
`min-width` 를 주지 않고 폰트/열 폭이 뷰포트에 맞춰 무한히 줄어들게
두는 방법. Rejected because 이슈-29 가 이미 확립한 패턴(표별 독립
가로 스크롤, `design-system.md` §5)이 "표는 스크롤하고 페이지는
스크롤하지 않는다"는 원칙이지 "표가 읽을 수 없을 만큼 축소된다"가
아니다 — 열이 무한 축소되면 상태 보드의 핵심 기능(수치·상태 판독)이
깨진다. 대신 `table.data-table` 에 `min-width`(640px, 첫 시도 값 —
`design-system.md` §7 의 age-bucket 임계값처럼 재검토 대상으로 명시)
를 주고, 그 아래 폭에서는 `.table-scroll` 자체가 스크롤을 맡는다 —
issue 본문이 요구한 세 가지(`#main-content { min-width: 0 }`, 명시적
표 최소폭, `.table-scroll` 폭 제한)를 그대로 따른다.

**좁은 화면 상세 — 기존 `renderDetailPanel` 재사용 vs. 별도 좁은
화면 전용 렌더 함수.** Alternative considered and rejected: 좁은
화면용 마크업을 별도 함수로 새로 작성. Rejected because 두 렌더
경로가 나뉘면 향후 필드 추가(예: 새 decision/flow 속성)마다 두 곳을
동시에 고쳐야 하고 드리프트 위험이 생긴다(scout-brief performance
axis 3). 대신 `renderDetailPanel(data, issue, repo)` 하나를 두 자리
(넓은 화면 `DETAIL_SLOT`, 좁은 화면 `<tr>`) 에서 그대로 호출하는
단일 진실 공급원 구조를 쓴다 — scout-brief 의 네 각도가 모두 수렴한
"토글 직후 다음 형제로 삽입" 원칙과도 맞는다.

**Live region 배치 — 기존 상태 컨테이너에 직접 부착 vs. 별도
공용 announcer 엘리먼트.** Alternative considered and rejected:
`index.html` 에 화면에 보이지 않는 전용 announcer `<div
aria-live="polite">` 를 하나 새로 만들고, 상태가 바뀔 때마다 그
안의 텍스트를 미러링. Rejected because 이미 `#header-meta`/
`#partial-banner`/에러 상태 마크업이 정확히 알려야 할 텍스트를
담고 있다 — 그 컨테이너들에 직접 `aria-live`/`role` 을 붙이는 편이
텍스트를 두 곳에 유지할 필요가 없어 더 작고 드리프트가 없는 변경
이다. `#header-meta`/`#partial-banner` 는 페이지 로드 시점부터
`aria-live="polite"` 를 정적으로 갖는다(scout-brief must-be: "라이브
리전은 로드 시점부터 존재하는 편이 낫다").

**포커스 이동 범위 — row-toggle 열기/닫기에만 적용 vs. Refresh/필터
변경 시에도 적용.** Alternative considered and rejected: Refresh
버튼·repo-filter 변경으로 인한 재렌더링에도 포커스를 상세/에러
영역으로 옮기는 것. Rejected because 그 두 액션은 사용자가 이미
포커스를 두고 있는 컨트롤(Refresh 버튼/select)에서 스스로 트리거한
것이라, 매번 포커스를 다른 곳으로 옮기면 오히려 방해가 되고, 수용
기준 문구("로딩·오류·상세 열림") 도 그 세 가지만 명시한다 — 필터
변경은 포함되지 않는다.

**오류 메시지 내부 경로 처리 — 요약+접힌 상세 구조 vs. 정규식
기반 경로 제거.** Alternative considered and rejected: `message`
문자열에서 파일 경로처럼 보이는 패턴을 정규식으로 찾아 지우는 방법.
Rejected because `dashboard.js` 는 provider/backend 가 만드는 모든
오류 문자열의 형식을 알지 못한다 — 정규식은 새로운 경로 형식을
놓치거나 유용한 정보까지 지울 수 있다. 대신 `design-system.md` §6
이 이미 issue-29 승인안으로 명시한 "요약 한 줄 + `<details>` 접힌
상세" 구조를 전체 오류 상태에도 동일하게 적용한다 — "내부 경로를
노출하지 않는다"를 "기본 상태에서 노출하지 않는다(펼쳐야 보인다)"로
해석하며, 이는 백엔드 스키마를 모르는 프런트엔드 전용 변경 범위
안에서 낼 수 있는 정확한 결과다.

**Neutral border 대비 — 기존 `color-neutral-500` 재사용 vs. 새
프리미티브 추가.** Alternative considered and rejected:
`color-neutral-300`(1.47:1)과 3:1 사이의 새 중간값(예:
`color-neutral-400`)을 새로 정의. Rejected because issue-34/issue-36
이 이미 세운 "기존 토큰으로 충분하면 새 토큰을 만들지 않는다" 관례를
따른다 — `color-neutral-500` 은 이미 `design-system.md` §2.2 에
4.6:1 로 문서화되어 있고 이 페이지에서 이미 쓰이고 있어(text-secondary),
재사용이 토큰셋을 늘리지 않고 3:1 바닥을 여유 있게 통과한다.

**터치 영역 — `min-width`/`min-height` + flex 중앙 정렬 vs. 패딩
기반 확대.** Alternative considered and rejected: scout-brief 가 든
예시 그대로(아이콘 16px + 패딩 4px)의 패딩 기반 확대. Rejected because
`.row-toggle` 의 글리프는 고정 크기 아이콘이 아니라 상속된
`font-size-body`(14px)로 그려지므로, 패딩만으로는 폰트 크기가 바뀔
때마다 24px 를 보장하지 못한다. 대신 `min-width`/`min-height: 24px`
+ `display: inline-flex` 중앙 정렬을 써서 글리프 렌더 크기와 무관하게
타겟 크기를 보장한다 — 속성 하나가 늘지만 더 견고하다.

## What will be done

**`dashboard.js`:**

- P1-1: 코드 변경 없음(CSS 전용 수정, 아래 참조).
- P1-3 (좁은 화면 인라인 상세): 새 순수 함수
  `detailRowHtml(colspan, contentHtml)` →
  `` `<tr class="detail-row"><td colspan="${colspan}">${contentHtml}</td></tr>` ``.
  `renderData()` 끝의 `DETAIL_SLOT.innerHTML = selectedIssue ? renderDetailPanel(...) : "";`
  를 새 함수 `applySelectionLayout(data)` 호출로 교체:
  - 먼저 `MAIN.querySelectorAll(".selected-row")` 에서 기존 `selected-row`
    클래스를 제거(P2-7 시각 강조 초기화).
  - `selectedIssue` 가 없으면 `DETAIL_SLOT.innerHTML = ""` 후 반환.
  - 있으면 `MAIN.querySelectorAll(".row-toggle")` 를 순회해 `data-issue`/
    `data-repo`/`data-table` 이 `selectedIssue` 와 일치하는 버튼을 찾고
    `.closest("tr")` 로 그 행을 얻는다. 찾은 행에 `selected-row` 클래스를
    추가(P2-7).
  - `window.matchMedia(WIDE_LAYOUT_QUERY).matches` 로 넓은 화면 여부를
    판정. 넓은 화면(또는 행을 못 찾은 예외 상황)이면 기존처럼
    `DETAIL_SLOT.innerHTML = renderDetailPanel(...)`. 좁은 화면이면
    `DETAIL_SLOT.innerHTML = ""` 후 `row.insertAdjacentHTML("afterend",
    detailRowHtml(row.children.length, renderDetailPanel(...)))`.
  - `WIDE_LAYOUT_QUERY` 상수 및 주변 주석(`dashboard.js:11-19`)을 실제
    동작(이제 살아있는 media-query 체크)에 맞게 정정.
- P1-4 (포커스 이동): `attachRowToggleHandlers` 의 클릭 리스너에서
  `wasExpanded` 를 `renderData(data)` 호출 전에 저장해두고, 호출 후:
  - 닫는 동작(`wasExpanded === true`)이면 같은 `data-issue`/`data-repo`/
    `data-table` 을 가진(재생성된) 버튼을 다시 찾아 `.focus()`.
  - 여는 동작이면 `document.getElementById("detail-panel-heading")` 를
    찾아(있으면) `.focus()` — 상세 패널/“no longer has board activity”
    메시지 둘 다 이 id 를 갖도록 `renderDetailPanel` 을 아래처럼 수정.
- `renderDetailPanel`: 헤더를 `<h2 id="detail-panel-heading"
  tabindex="-1">Issue ${issue} — ${repo}</h2>` 로, 바깥 wrapper 를
  `<div class="detail-panel" role="region" aria-labelledby="detail-panel-heading">`
  로 바꾼다. "no longer has board activity" 분기의 div 에도 동일하게
  `id="detail-panel-heading" tabindex="-1"` 를 추가(포커스 대상이 항상
  존재하도록).
- P1-4 (busy/live 상태): `renderSkeleton()` 시작 부분에
  `MAIN.setAttribute("aria-busy", "true")`. `renderData()`/
  `renderFullError()` 각각 끝에서 `MAIN.setAttribute("aria-busy", "false")`.
  `index.html` 의 `#header-meta`/`#partial-banner` 는 정적으로
  `aria-live="polite"` 를 갖는다(아래 index.html 절 참조) — JS 변경
  없음, 텍스트를 그 안에 쓰는 기존 코드 경로가 그대로 announce 된다.
- P2-6 (오류 요약+접힌 상세): 새 순수 함수
  `collapsibleDetailHtml(summaryLabel, detailText)` →
  `` `<details><summary>${escapeHtml(summaryLabel)}</summary><p>${escapeHtml(detailText)}</p></details>` ``.
  `renderFullError(message)`: `<h1>Couldn't load board status</h1>` 를
  `<h2>Couldn't load board status</h2>` 로(중복 `<h1>` 수정, survey §5),
  `.error-state` div 에 `role="alert"` 추가, 원문 `message` 를 직접
  본문에 넣던 것을 `<p>The board data couldn't be loaded.</p>` +
  `collapsibleDetailHtml("Details", message)` 로 교체(요약 줄은
  일반화된 문구, 원문/내부 경로는 접힌 `<details>` 뒤로). 부분 실패
  배너(`renderData()` 의 `PARTIAL_BANNER.innerHTML` 블록)도 동일하게
  `` `${failedRepos.length} of ${total} repos failed to load` `` 한 줄만
  항상 보이고 `collapsibleDetailHtml("Details", detail)` 로 per-repo
  상세를 접는다 — `design-system.md` §6 이 이미 승인해 뒀지만 한 번도
  배선되지 않았던 issue-29 결정을 이 김에 완성한다(survey §5, 이미
  존재하는 `dashboard.css:252-258` 의 `.partial-banner
  summary`/`details[open] summary` CSS 를 그대로 재사용).
- P2-5 (Refresh 버튼 disabled 상태): `load()` 시작에서
  `REFRESH_BUTTON.disabled = true`, `try/catch` 를 `try/catch/finally`
  로 바꾸고 `finally` 에서 `REFRESH_BUTTON.disabled = false` — 로드 중
  중복 클릭을 막고 P3-8 이 요구하는 "일관된 disabled 상태"가 실제로
  발동할 경로를 만든다.
- P2-7 (표 caption/scope): `renderTable(headers, rows, emptyMessage,
  caption)` 에 네 번째 인자 추가 — `<th>` 를 `<th scope="col">` 로,
  `<caption class="visually-hidden">${escapeHtml(caption)}</caption>`
  를 `<thead>` 앞에 추가. 네 호출부(`renderData()` 의 Decision
  queue/Flows/Sessions, `renderAccounting()`)에 각각
  `"Decision queue"`/`"Flows"`/`"Sessions"`/`"Accounting ledger"` 전달.
- P3-8 (outcomes 배지): `renderAccounting()` 의
  `` `${k}:${v}` `` 텍스트 join 을
  `` `<span class="badge status-neutral mono">${escapeHtml(k)}:${v}</span>` ``
  로 바꿔 다른 상태 값들과 같은 배지 스타일을 쓴다.
- `module.exports`: `detailRowHtml`, `collapsibleDetailHtml` 추가(기존
  8개는 유지).

**`dashboard.css`:**

- P1-1: `#main-content, #detail-panel-slot { min-width: 0; }` 추가.
  `table.data-table` 에 `min-width: 640px;` 추가(첫 시도 값, 재검토
  대상으로 design-system.md §7 에 기록). `.table-scroll` 에
  `width: 100%;` 추가.
- P1-3: 변경 없음 — `.detail-row td`(`dashboard.css:203-208`)는 이미
  존재하는 스타일을 그대로 쓴다.
- P2-5: `.row-toggle` 에 `min-width: 24px; min-height: 24px; display:
  inline-flex; align-items: center; justify-content: center;` 추가.
  새 규칙 `#repo-filter { min-height: 24px; padding: var(--space-1)
  var(--space-2); border: 1px solid var(--color-border-default);
  border-radius: 4px; font: inherit; }` + `#repo-filter:focus-visible
  { outline: 2px solid var(--color-blue-500); outline-offset: 2px; }`.
  `.refresh-button` 에 `min-height: 24px;` 추가(대부분 이미 통과하지만
  명시적으로 보장).
- P2-6: `.error-state h1` 셀렉터를 `.error-state h2` 로 이름만 변경.
  새 규칙 `.error-state details summary { cursor: pointer; margin-top:
  var(--space-2); }`(기존 `.partial-banner summary` 규칙과 대칭).
- P2-7: 새 유틸리티 클래스 `.visually-hidden`(표준 sr-only 기법 —
  `position: absolute; width: 1px; height: 1px; overflow: hidden; clip:
  rect(0,0,0,0); white-space: nowrap; border: 0; padding: 0; margin:
  -1px;`) — 새 디자인 토큰이 아닌 위치 기법이라 Constraints 의 토큰
  금지와 무관. 새 규칙 `tr.selected-row { background:
  var(--color-status-info-background); }`(기존 status-info 토큰
  재사용). 새 규칙 `.detail-panel > h2 { font-size: var(--font-size-300);
  margin: 0; font-weight: 600; }`.
- P3-8: `.refresh-button:hover { background: var(--color-blue-700); }`,
  `.refresh-button:focus-visible { outline: 2px solid
  var(--color-blue-500); outline-offset: 2px; }`,
  `.refresh-button:disabled { opacity: 0.5; cursor: not-allowed; }`.
  새 규칙 `table.data-table tbody tr:hover { background:
  var(--color-neutral-100); }`. `.skeleton-row` 의 `height: 2em;` 을
  `height: calc(var(--space-table-cell-padding-y) * 2 + 1.4em);` 로
  교체(실제 데이터 행 높이 계산에 맞춤). 토큰 블록에서
  `--color-border-default: var(--color-neutral-300);` 를
  `--color-border-default: var(--color-neutral-500);` 로 변경(대비
  개선, survey §7 — 새 프리미티브 아님, 기존 `neutral-500` 재사용).

**`index.html`:**

- `#header-meta` 에 `aria-live="polite"` 추가.
- `#partial-banner` 에 `aria-live="polite"` 추가.
- `#main-content` 에 초기 `aria-busy="true"`(페이지 로드 시 아직 JS
  가 데이터를 받아오기 전이므로 로딩 중 상태로 시작).

**테스트 (`test/rsb_tests/test_model.py`):**

- `detailRowHtml(5, "<div>x</div>")` → 정확한
  `<tr class="detail-row"><td colspan="5"><div>x</div></td></tr>`
  문자열 검증.
- `collapsibleDetailHtml("Details", "a/b: boom")` → 정확한
  `<details><summary>Details</summary><p>a/b: boom</p></details>`
  문자열 검증(HTML 이스케이프 포함 케이스 하나 추가).
- 기존 55개 테스트(이번 세션에 `python3 -m pytest test/` 로 재확인)는
  무변경으로 통과해야 한다 — 기존 export 이름 유지, 새 export 2개만
  추가.

**문서 (doctrine ladder):**

- `docs/specs/screen-spec.md`: §1.3(및 §1.4/§1.5/§1.7 의 "§1.3 과 동일
  패턴" 참조)에 caption(시각적으로 숨김)/`scope="col"`/선택 행
  `status-info` 배경 강조 한 줄씩 추가. §1.6 에 좁은 화면 `<tr>`
  삽입이 이제 실제로 구현됨과, 상세 패널이 `role="region"
  aria-labelledby`/`<h2 id="detail-panel-heading" tabindex="-1">` 를
  가지며 열기/닫기 시 포커스가 이동함을 기록. §2.1/§2.4/§2.5/§2.6 에
  `aria-busy`(`#main-content`)/`aria-live="polite"`(`#header-meta`,
  `#partial-banner`)/`role="alert"`(전체 오류)/포커스 이동 사실을
  추가하고, §2.4/§2.5 의 카피 서술을 "요약 한 줄 + 접힌 `<details>`"
  구조로 갱신(전체 오류는 `<h2>`, 부분 배너는 issue-29 승인안 그대로
  마침내 배선됨을 명시).
- `docs/specs/design-system.md`: §2.2 에 `color-border-default`
  (`neutral-500`) 의 대비(4.6:1)를 명시적으로 추가. §5 breakpoint
  표의 "Multi-device/mobile optimization out of scope" 문단을 "이슈
  #38 로 오버플로 방지(`min-width` 체계)와 24×24px 터치 타겟 최소
  보장은 갖췄으나, 전면 반응형 재설계는 여전히 범위 밖"으로 좁혀
  갱신. §6 컴포넌트 표: `DataTable`(caption/scope/selected-row/
  min-width 추가), `RefreshButton`/`RepoFilter`(hover/focus-visible/
  disabled, 24×24 최소 크기), `DetailPanel`(heading/landmark/
  포커스 이동/좁은 화면 `<tr>` 삽입), `ErrorState`(`role="alert"`,
  `<h2>`, 접힌 상세), `PartialFailureBanner`(그 아래 "이번에 마침내
  배선됨, 더 이상 미배선 아님" 으로 기존 노트 갱신).

**수동 검증 (phase 2):** `rsb serve` 로컬 구동 후 — 390px 폭에서
페이지 본문이 가로로 밀리지 않고 각 표만 개별 스크롤되는지; 1024px
에서 행 토글 시 상세가 선택 행 바로 아래 나타나고 1200px 이상에서는
사이드 패널로 전환되는지; 스크린리더(VoiceOver 등)로 로딩→로드완료,
부분/전체 오류, 상세 열기/닫기 시 announce 되고 포커스가 이동하는지;
Tab 으로 `.row-toggle`/`#repo-filter`/`.refresh-button` 를 순회하며
포커스 링과 24×24 클릭 영역을 확인하는지; 부분/전체 오류에서 요약
줄만 보이고 "Details" 를 펼쳐야 원문이 보이는지; 표에 caption(스크린
리더 전용)과 `scope=col` 이 있는지, 선택 행이 시각적으로 구분되는지;
1440px 기본 화면에서 기존 밀도에 회귀가 없는지 확인한다.

## Out of scope

- P1-2(상세 펼침 토글 배선 자체) — issue #36(PR #37, merged) 소관,
  이미 올바르게 동작(survey §0).
- `render.py`(CLI), `webserver.py` 등 백엔드 변경 — 프런트엔드 렌더링/
  접근성 계층만 다룬다(Constraints).
- 오류 메시지 문자열 자체에서 내부 경로를 정규식 등으로 제거하는
  백엔드/프런트엔드 sanitization — 요약+접힌 상세 구조로 "기본
  노출 안 함"을 satisfy(Rationale).
- 전면 반응형/모바일 최적화(카드 레이아웃 등) — 이슈 본문이 요구하는
  것은 표별 스크롤 유지 + 오버플로 방지이지 별도 모바일 UI 가 아니다
  (design-system.md §5 관례 그대로).
- 새 JS 테스트 프레임워크/`package.json` 도입 — 기존 `node -e` 셸아웃
  관례만 확장(Constraints).
- `.number-link` 자체의 시각적 크기 확대 — WCAG 2.5.8 인라인 텍스트
  타겟 예외 적용 가능성이 높다고 판단(scout-brief), phase-2 실측으로
  확인만 하고 CSS 는 건드리지 않는다.
- `--color-border-default` 이외의 다른 토큰들의 대비 재검토 — 이번에
  이슈 본문이 명시적으로 지적한 border 대비 한 건만 다룬다.

## How you'll know it worked

- `python3 -m pytest test/`(이 환경은 `PYTHONPATH=src` 필요, 이번
  세션에 baseline 55 passed 확인) 전부 통과(기존 55개 + 신규
  `detailRowHtml`/`collapsibleDetailHtml` 테스트 2개, 회귀 없음).
- `node --check src/rsb/web/dashboard.js` 문법 검사 통과.
- `node -e` 로 `detailRowHtml`/`collapsibleDetailHtml` 를 owner/name
  케이스 없이 직접 호출해 출력 문자열 확인(HTML 이스케이프 포함).
- 브라우저 수동 검증(위 "수동 검증" 항목)으로 이슈 본문의 8개 수용
  기준을 하나씩 확인하고 phase-2 record 에 기재(사용자 지시: DOM
  배선 변경은 반드시 브라우저 실제 조작으로 확인).
- PR 본문에 closing 키워드(백틱 인용 포함) 없는지 제출 직전 재확인.
