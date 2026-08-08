# issue-61 current-state survey

Read this session: `src/rsb/web/dashboard.js` (전체), `docs/specs/screen-spec.md`
§1.3/§1.6, `docs/specs/design-system.md` §5, `test/rsb_tests/test_dashboard_dom.py`
(전체), `test/rsb_tests/test_model.py`(하네스 부분), `docs/issue-36/reports/conformance-review.md`
(F1/F2/Appendix A4 전문), `docs/issue-38/reports/conformance-review.md`(R2f),
issue #61 본문(`gh issue view 61`), issue #62 본문(`gh issue view 62`).
`grep`으로 `src/rsb/fetch.py`, `src/rsb/web/dashboard.css`도 확인(overlap 판단용).

## 1.요구사항 1 — `window.matchMedia` 무가드 호출 (F1)

현재 `dashboard.js:508`(`applySelectionLayout` 내부, 함수 전체는
`:473-514`):

```js
  const contentHtml = renderDetailPanel(data, selectedIssue.issue, selectedIssue.repo);
  if (!selectedRow || window.matchMedia(WIDE_LAYOUT_QUERY).matches) {
    DETAIL_SLOT.innerHTML = contentHtml;
  } else {
    DETAIL_SLOT.innerHTML = "";
    selectedRow.insertAdjacentHTML("afterend", detailRowHtml(selectedRow.children.length, contentHtml));
  }
```

`WIDE_LAYOUT_QUERY = "(min-width: 1200px)"` (`:16`). 가드(`typeof
window.matchMedia === "function"` 체크, try/catch, optional chaining)
없이 즉시 호출한다. **줄 번호 드리프트 주의**: 이슈 본문·issue-36
conformance-review(Appendix A4)는 이 호출을 `dashboard.js:520`으로
인용하는데, 그건 그 리뷰가 대상으로 삼은 커밋 시점 기준이다. `main`
현재 head 기준 실제 위치는 `:508`이며, 이 survey/proposal은 전부 현재
head 기준 줄 번호로 인용한다.

`applySelectionLayout`은 `renderData`(`:563-632`) 내부 `:629`에서
호출되고, `attachRowToggleHandlers`는 그 다음 줄 `:630`에서 호출된다 —
이슈가 말하는 "`attachRowToggleHandlers` 앞에 호출"이 정확히 이 순서다.

`renderData`는 `.row-toggle` 클릭 핸들러(`attachRowToggleHandlers`,
`:537-561`) 안에서도 다시 호출된다(`:545`) — 즉 두 번째·세 번째 클릭마다
`applySelectionLayout`이 재실행되고, 매번 무가드 `matchMedia` 호출을
다시 거친다.

### 실측: jsdom은 `window.matchMedia`를 아예 구현하지 않는다

`test/node_modules/jsdom`(`package.json` `"version": "30.0.1"`)로 직접
확인:

```
typeof window.matchMedia: undefined
'matchMedia' in window: false
THREW: TypeError window.matchMedia is not a function
```

("not implemented" 경고를 던지는 스텁이 아니라, 속성 자체가 없다 —
`in` 연산자로도 `false`.)

### 실측: DOM 이벤트 리스너 내부에서 발생한 예외는 `.click()` 호출자에게
전파되지 않는다

`button.click()` → 리스너 내부에서 `renderData` 호출 → `renderData`가
`MAIN.innerHTML`을 새 버튼들로 재작성(`:607-628`, 여기서 새 버튼의
`aria-expanded`는 이미 최신값으로 찍힌다) → `applySelectionLayout`
호출 → `:508`에서 `TypeError` throw. jsdom(과 브라우저)의 이벤트 디스패치
계약상 리스너 내부 예외는 `reportException` 경로로 처리되고
`dispatchEvent`/`.click()` 호출자에게 재throw되지 않는다 — 그래서
`_run_dom_js`의 node 서브프로세스는 `returncode 0`으로 끝나고, pytest
쪽에서 보이는 건 "assertion 실패"이지 "노드 스크립트 크래시"가 아니다
(아래 §3 실측 출력 참고). 대신 `attachRowToggleHandlers`(`:630`)가
실행되지 못한 채로 남아, 새로 그려진 버튼들이 리스너를 못 받는다 —
issue-36 conformance-review Appendix A4가 문서화한 것과 같은 메커니즘
(§5 참고).

### 스파이크: 가드 추가 시 실제로 green이 되는지 직접 확인(로컬, 적용 후
되돌림)

`applySelectionLayout`의 해당 두 줄을 로컬에서만 다음과 같이 바꿔
(`git diff`, 실행 후 `git checkout --`로 되돌림 — 이 survey 작성 시점
기준 커밋 트리에는 반영되지 않음):

```diff
   const contentHtml = renderDetailPanel(data, selectedIssue.issue, selectedIssue.repo);
-  if (!selectedRow || window.matchMedia(WIDE_LAYOUT_QUERY).matches) {
+  const isWideLayout = typeof window.matchMedia === "function"
+    ? window.matchMedia(WIDE_LAYOUT_QUERY).matches
+    : true;
+  if (!selectedRow || isWideLayout) {
     DETAIL_SLOT.innerHTML = contentHtml;
```

이 변경만으로 `test_dashboard_dom.py`가 9/9 green, 전체 스위트가
66/66 green(§3 참고)이 된다. `matchMedia`가 없을 때 `isWideLayout`을
`true`(와이드 레이아웃)로 폴백한 것이 핵심 — `false`로 폴백하면 narrow
분기(`tr.detail-row` 삽입)를 타서 `#detail-panel-slot`이 비고, 기존
테스트들이 `document.getElementById("detail-panel-slot").innerHTML...`을
직접 단언하므로 여전히 실패한다(narrow 분기로 폴백하는 건 그 자체로는
크래시하지 않지만 기존 테스트 기대치와 어긋난다는 뜻 — 이 트레이드오프는
proposal Rationale에서 다룬다).

## 2. 요구사항 2 — `<1200px` 분기의 `aria-controls` 오지시 (F2 / R2f)

`rowToggleButtonHtml`(`dashboard.js:230-239`, 버튼 마크업 자체는 `:238`):

```js
function rowToggleButtonHtml(sourceTable, issue, repo, expanded) {
  return `<button type="button" class="row-toggle" aria-expanded="${expanded}" aria-controls="detail-panel-slot" aria-label="Toggle details for issue ${issue}" data-issue="${issue}" data-repo="${escapeHtml(repo)}" data-table="${sourceTable}"><span aria-hidden="true">${expanded ? "▾" : "▸"}</span></button>`;
}
```

`aria-controls="detail-panel-slot"`는 모든 토글 버튼에 하드코딩된
리터럴이다 — 소스 테이블/레이아웃과 무관하게 항상 이 값이다.

그런데 `applySelectionLayout`(§1)의 narrow 분기(`:511-512`)는
`DETAIL_SLOT.innerHTML = ""`로 그 요소를 비우고, 실제 패널 콘텐츠는
`selectedRow.insertAdjacentHTML("afterend", detailRowHtml(...))`로
선택된 행 바로 뒤에 삽입되는 `<tr class="detail-row">`
(`detailRowHtml`, `:452-453`)로 간다:

```js
function detailRowHtml(colspan, contentHtml) {
  return `<tr class="detail-row"><td colspan="${colspan}">${contentHtml}</td></tr>`;
}
```

이 `<tr>`에는 `id`가 없다 — 즉 narrow 레이아웃에서 열린 패널을 가리킬
수 있는 IDREF 자체가 DOM에 존재하지 않는다. 버튼의 `aria-controls`는
여전히 `"detail-panel-slot"`을 가리키는데, 그 요소는 이 시점에 빈
컨테이너다 — "실제로 열린 콘텐츠"와 IDREF가 가리키는 대상이 서로 다른
거짓 관계(issue-36 F2가 지적한 정확히 그 지점, issue-38 R2f가 재확인).

### spec §1.3 대조

`docs/specs/screen-spec.md` §1.3(`:59-64`)은 다음과 같이 서술한다:

> Issue 셀은 선행 아이콘 전용 `<button class="row-toggle">`(▸/▾ 글리프,
> `aria-expanded`, `aria-controls="detail-panel-slot"`, ...)을
> 렌더한다.

이 문장은 `aria-controls="detail-panel-slot"`을 무조건 참인 사실처럼
서술하며, `<1200px` 분기가 콘텐츠를 다른 곳(`tr.detail-row`)으로
옮긴다는 사실을 전혀 언급하지 않는다. §1.6(Detail panel, `:104-111`)은
레이아웃 스위치 자체(`breakpoint-lg` 기준 side panel ↔ expandable row)는
서술하지만, 그 스위치가 §1.3의 `aria-controls` 값을 무효화한다는
연결은 어느 섹션에도 없다 — issue-36 conformance-review가 이미 같은
결론("`screen-spec.md`도 분기를 서술하지 않는다")에 도달했다(F2 evidence
문단). 요구사항 2가 요구하는 "screen-spec.md §1.3이 양 분기를
서술하게 갱신"은 아직 전혀 반영되지 않은 상태다.

## 3. 실측: pytest 적색 2건 (수정 전, `git status` clean 상태에서)

`npm install --prefix test`(1회성 사전 준비, `docs/handbooks/rsb.md`
관례)로 `test/node_modules/jsdom`을 설치한 뒤:

```
$ python3 -m pytest test/rsb_tests/test_dashboard_dom.py -v -rs
collected 9 items

test_repo_filter_options_empty_when_no_repos PASSED
test_repo_filter_options_populated_for_single_repo PASSED
test_repo_filter_options_populated_for_multiple_repos_including_errored PASSED
test_row_toggle_click_opens_detail_and_flips_aria_expanded FAILED
test_row_toggle_click_on_non_button_cell_does_not_open_detail PASSED
test_row_toggle_click_only_affects_its_own_table PASSED
test_row_toggle_reactivating_open_button_closes_it FAILED
test_partial_failure_raw_message_absent_from_main_content_and_errors_section_gone PASSED
test_load_fetches_relative_board_json_path PASSED

FAILURES:
test_row_toggle_click_opens_detail_and_flips_aria_expanded
    assert result["detailHasContent"] is True
E   assert False is True

test_row_toggle_reactivating_open_button_closes_it
    assert result["expanded"] == "false"
E   AssertionError: assert 'true' == 'false'
E     - false
E     + true

2 failed, 7 passed in 3.79s
```

**개수 드리프트 주의**: 이슈 본문은 "65 중 63 통과"/"8/8 통과"로 인용하는데
(issue-36 conformance-review 시점 기준), 그 이후 issue #56 phase 2가
`test_partial_failure_raw_message_absent_from_main_content_and_errors_section_gone`
케이스를 추가해 이 파일은 현재 8건이 아니라 **9건**, 전체 스위트는 65건이
아니라 **66건**이다(아래). 실패 건수 자체(2건)는 이슈 본문과 일치한다.

전체 스위트(`pip install -e .`는 샌드박스 쓰기 제한으로 실패해
`PYTHONPATH` 삽입 방식으로 우회 — `docs/issue-44/reports/conformance-review.md:64-68`가
쓴 것과 같은 우회):

```
$ python3 -c "import sys; sys.path.insert(0,'src'); import pytest; sys.exit(pytest.main(['test/','-q']))"
66 passed  # 스파이크(§1) 적용 상태에서 측정 — 스파이크 되돌린 원래 상태는 64 passed, 2 failed
```

스파이크를 되돌린 원상태에서는 `test_dashboard_dom.py` 9건 중 2건
실패, 나머지 5개 파일(`test_cli`/`test_config`/`test_fetch`/`test_model`/`test_render`/`test_webserver`)은
전부 기존대로 통과 — 이슈가 규정하는 "main 스위트 적색 2건"과 정확히
일치한다.

## 4. 브라우저 API 무가드 사용 전수 감사

`grep -n "window\.\|document\.\|navigator\.\|localStorage\|sessionStorage\|IntersectionObserver\|ResizeObserver\|MutationObserver\|requestAnimationFrame\|WebSocket\|indexedDB\|history\.\|location\.\|fetch(" src/rsb/web/dashboard.js` — 저장소 전체에서 `src/rsb/web/dashboard.js`가
유일한 JS 파일이므로(`find . -iname "*.js" -not -path "*/node_modules/*"`
1건), 이 감사는 "dashboard.js의 다른 무가드 호출"(이슈 §20 클래스
질문)과 "코드베이스 전수"가 사실상 동일 범위다. `navigator.*`,
`localStorage`, `sessionStorage`, `IntersectionObserver`,
`ResizeObserver`, `MutationObserver`, `requestAnimationFrame`,
`WebSocket`, `indexedDB`, `history.*`, `location.*` — 전부 0건.

| file:line | API | 가드 여부 | 위험 |
|---|---|---|---|
| `dashboard.js:3-9` (모듈 스코프 7개 `const`) | `document.getElementById(...)` | **아니오** — `typeof document`체크도 try/catch도 없음. 파일 하단 `:658`의 `typeof window !== "undefined"` 가드는 auto-init *부작용*만 감싸고, 이 모듈-스코프 `const` 선언 자체는 그 가드보다 먼저, 무조건 실행된다 | `document`가 전혀 정의 안 된 순수 Node 환경에서 이 모듈을 `require()`하면 `ReferenceError: document is not defined`로 즉시 크래시 — `typeof window` 가드에 도달하기도 전. 현재 두 테스트 하네스(`test_model.py`의 `{getElementById: () => null}` 스텁, `test_dashboard_dom.py`의 실제 jsdom)는 둘 다 require 전에 `global.document`를 먼저 채워서 이 경로를 우회하고 있을 뿐, 이 파일 자체가 가드하는 게 아니다 |
| `dashboard.js:169` | `document.getElementById("retry-button").addEventListener(...)` | 아니오(자체 가드 없음) | `renderFullError()` 내부 — 이 함수가 실행되려면 이미 위 모듈-스코프 `document` 접근이 성공했어야 하므로 독립적인 추가 위험은 낮지만, 별도 방어선은 없다 |
| `dashboard.js:508` | `window.matchMedia(WIDE_LAYOUT_QUERY)` | **아니오 — 이슈의 핵심 결함(F1)** | jsdom(및 `matchMedia` 미구현 UA)에서 `TypeError: window.matchMedia is not a function`으로 `renderData`를 중간 중단(§1) |
| `dashboard.js:556` | `document.getElementById("detail-panel-heading")` | 아니오(자체 가드 없음) | `attachRowToggleHandlers`의 클릭 콜백 내부 — 위와 같은 클래스, 이미 DOM이 있는 컨텍스트에서만 도달 |
| `dashboard.js:595` | `document.getElementById("partial-retry").addEventListener(...)` | 아니오(자체 가드 없음) | 위와 같은 클래스 |
| `dashboard.js:638` | `fetch("api/board.json")` | **예** — `load()`의 `try { ... } catch (err) { renderFullError(...) } finally { ... }`(`:635-651`)가 이 호출을 감싼다 | `fetch`가 전역에 없는 환경이라도 `ReferenceError`가 try 블록 안에서 발생해 catch로 잡히고 `renderFullError`로 라우팅된다 — 이 호출부는 이미 안전 |
| `dashboard.js:659-663` (auto-init 블록: `REFRESH_BUTTON.addEventListener`, `REPO_FILTER.addEventListener`, `load()`) | 사실상 `window` 존재 여부에 의존하는 부작용 | **예** — `:658`의 `if (typeof window !== "undefined")`로 전체를 감쌈 | 이 파일에 이미 존재하는 유일한 "명시적 가드" 사례 — 이번 수정이 따라야 할 로컬 선례 |

**결론**: 이 파일에서 실질적으로 위험한 무가드 지점은 두 클래스다 —
(a) 모듈 스코프 `document.getElementById` 7건(요구 없이도 항상
실행되며, 현재는 두 테스트 하네스가 매번 `document`를 미리 채워주는
관례로 우회되고 있을 뿐 파일 자체의 방어는 없음), (b) `:508`의
`window.matchMedia` 1건(F1, 실제로 관측되는 크래시). `fetch`(:638)는
이미 try/catch로 안전하고, `:169/:556/:595`의 `document.getElementById`
3건은 (a)가 이미 성립한 컨텍스트에서만 도달하므로 독립적으로 새 위험을
추가하지 않는다. proposal에서 이번 이슈 범위에 (a)까지 포함할지,
(b)만 다룰지 트레이드오프를 판단한다.

## 5. issue #62 겹침 조사

`git branch -a`, `gh pr list --state all`에 `issue-62/*` 브랜치나 PR이
없다 — 아직 아무 코드도 나오지 않았다. 이슈 본문(`gh issue view 62`)만
근거로 예상 겹침을 판단:

- **`src/rsb/web/dashboard.css`**: R4e(`#partial-retry` 24px 최소
  크기), R4e2(두 `<summary>` 24px), R6d(선택 행 대비) — 전부 CSS 전용
  변경으로 보인다. 이번 이슈가 `dashboard.css`를 건드릴 계획은 없다
  (F1/F2 둘 다 JS+spec 변경). **파일 겹침 없음.**
- **`src/rsb/fetch.py`**: R5d(내부 경로 마스킹) — 이번 이슈가 손대지
  않는 파일. **겹침 없음.**
- **`src/rsb/web/dashboard.js`**: R5d의 증거 체인이
  `src/rsb/fetch.py:35,40` → `dashboard.js:600`(옛 커밋 기준 줄 번호 —
  현재 head 기준으로는 부분-실패 배너의 `collapsibleDetailHtml("Details",
  detail)` 호출부, `:585-598` 부근, `collapsibleDetailHtml` 자체는
  `:462-464`)까지 이어진다고 명시한다. 이슈 #62의 마스킹 지점 결정("fetch.py
  생성부 vs 렌더부")이 렌더부 쪽으로 결정되면 `dashboard.js`의
  `collapsibleDetailHtml`/`renderData`의 배너 블록을 건드리게 된다 —
  이번 이슈가 고치는 `applySelectionLayout`(`:473-514`)·`rowToggleButtonHtml`(`:230-239`)·`detailRowHtml`(`:452-453`)과는
  **같은 파일, 다른 함수/다른 줄 범위**라 자동 머지 가능성이 높지만,
  같은 파일을 병렬로 건드리는 건 사실이므로 phase 2 시작 시 rebase
  충돌 가능성을 배제할 수 없다. 이 리스크를 proposal에 명시적으로
  기록한다(런처 지시 그대로).
- **`test/rsb_tests/`**: 양쪽 다 새 테스트 케이스를 이 디렉터리에
  추가한다(이슈-61은 `test_dashboard_dom.py`, 이슈-62는 터치 타깃/마스킹
  케이스 — 파일명 미정이지만 같은 디렉터리 관례를 따를 가능성이 큼).
  같은 파일(`test_dashboard_dom.py`)을 둘 다 건드릴 가능성이 있다 —
  줄 추가 위주라 충돌 가능성은 낮지만 마찬가지로 flag.
- **`docs/specs/design-system.md` §5**: 이슈-62 요구사항 3의 "design-system §5
  24px 목록 갱신"이 명시 대상. 이번 이슈-61은 `design-system.md`를 건드릴
  계획이 없다(§1.3만 다룸, 별개 문서인 `screen-spec.md`). **겹침 없음.**

## 6. issue #36 Appendix A4 (계측 프로브) 원문 발췌

`docs/issue-36/reports/conformance-review.md`의 F1(§1 evidence)과
Appendix A4(`:441-468` 부근)에서 확인한 내용, 요약 없이 그대로 인용:

> A4 — instrumented probe isolating F1's mechanism (at `main`)
>
> A throwaway jsdom driver, identical to the #44 harness except that
> `window.matchMedia` is supplied, run against
> `src/rsb/web/dashboard.js`; two synthetic activations of the same
> Decision-queue button. The probe file was deleted after the run and
> is not committed.
>
> ```
> narrow (matchMedia -> {matches:false}):
>   {"initial":"false","afterClick1":"true","slotAfter1":false,"detailRowAfter1":true,
>    "afterClick2":"false","slotAfter2":false,"detailRowAfter2":false}
>
> wide   (matchMedia -> {matches:true}):
>   {"initial":"false","afterClick1":"true","slotAfter1":true,"detailRowAfter1":false,
>    "afterClick2":"false","slotAfter2":false,"detailRowAfter2":false}
>
> native (jsdom's own window, no matchMedia):
>   {"probe":{"typeofMatchMedia":"undefined","windowError":"window.matchMedia is not a function"},
>    "initial":"false","afterClick1":"true","slotAfter1":false,"detailRowAfter1":false,
>    "afterClick2":"true","slotAfter2":false,"detailRowAfter2":false}
>   TypeError: window.matchMedia is not a function
>       at applySelectionLayout (src/rsb/web/dashboard.js:520:30)
>       at renderData (src/rsb/web/dashboard.js:642:3)
>       at HTMLButtonElement.<anonymous> (src/rsb/web/dashboard.js:557:7)
> ```

이 프로브의 결론("matchMedia가 있으면 두 레이아웃 분기 모두 open/close가
정상 동작하고, 없으면 첫 활성화 후 컨트롤이 죽는다")은 이번 survey §1의
자체 스파이크 결과와 정확히 일치한다 — 제품 로직 자체는 건전하고, 문제는
`matchMedia` 노출면의 무가드 호출과 테스트 하네스의 공백이라는 issue-36
conformance-review의 판단을 그대로 재확인한다.

## 7. 이 survey가 proposal에 남기는 결정 사항

- **요구사항 1의 가드 위치**: §1의 스파이크로 "src 가드 하나만으로
  green이 된다"는 사실은 이미 증명됐다 — 하네스 스텁을 추가로 도입할
  기술적 필요는 없다. 그래도 트레이드오프(src 가드 vs 하네스 스텁 vs
  병행)는 이슈가 명시적으로 요구하는 결정이므로 scout-brief에서 근거를
  붙여 proposal Rationale에서 확정한다.
- **요구사항 2의 구현 형태**: `detailRowHtml`이 생성하는 `<tr>`에 안정된
  `id`를 부여하고, `applySelectionLayout`이 narrow 분기를 탈 때 선택된
  버튼의 `aria-controls`만 그 id로 덮어쓰는 안(다른 미선택 버튼들은
  기존 `"detail-panel-slot"` 유지)이 유력한 후보 — 이건 §4의 audit로
  새 matchMedia 호출을 추가하지 않고도(레이아웃 판정은 §1에서 이미
  구한 `isWideLayout` 재사용) `applySelectionLayout` 내부에서만 완결된다.
  proposal의 "What will be done"에서 구체화한다.
- **요구사항 3(전수 감사)의 범위 판단**: §4의 표에서 (a) 모듈 스코프
  `document.getElementById` 7건을 이번 이슈에서 같이 고칠지, 별도
  hand-off로 미룰지는 이슈의 "범위 포함 여부를 제안에서 판단" 요구에
  따라 proposal이 결정한다.

## Warrant hunt (phase 1)

Verdict: FINDING — the proposed `typeof window.matchMedia === "function" ? window.matchMedia(WIDE_LAYOUT_QUERY).matches : true` guard only checks that `matchMedia` is *callable*, not that its return value has a usable `.matches`; any UA/shim where `window.matchMedia` exists as a function but returns `undefined`/`null` (a real, common shape — e.g. `window.matchMedia = window.matchMedia || function () {};`, or a bare `jest.fn()`/similar mock with no return value configured) still throws mid-`renderData`, reproducing the exact "unguarded matchMedia call interrupts renderData" failure mode issue #61 is fixing, just for a different, unguarded subset of environments.
Kind: design-error
Stance: 0 — assume the gate just touched is bypassable — find the bypass (after-proposal, issue-61)
Seed: docs/issue-61/proposals/implementation.md "What will be done" step 1 (planned dashboard.js:508 replacement); docs/issue-61/reports/implementation/survey.md §1
cap_seconds: 60
tier: default
diff_stat_lines: 0 (phase 1, proposal-only — no code diff exists yet; reasoned against src/rsb/web/dashboard.js:473-514 as currently committed)
started_at: 2026-08-08T00:00:00Z (approx, not logged precisely)
ended_at: 2026-08-08T00:02:30Z (approx)

### Reproduce
Node script evaluating the proposed guard expression verbatim against three `window` shapes (no jsdom needed — this is a pure-JS property-access hazard, independent of DOM):

```js
const WIDE_LAYOUT_QUERY = "(min-width: 1200px)";
function proposedGuard(window) {
  return typeof window.matchMedia === "function"
    ? window.matchMedia(WIDE_LAYOUT_QUERY).matches
    : true;
}
proposedGuard({ matchMedia: function () {} });       // returns undefined, no .matches
proposedGuard({ matchMedia: function () { return null; } });
```
Run: `node -e '<script above>'`

### Observed
```
B (matchMedia returns undefined) THREW: TypeError Cannot read properties of undefined (reading 'matches')
C (matchMedia returns null) THREW: TypeError Cannot read properties of null (reading 'matches')
```
(Confirmed jsdom 30, the project's own DOM test harness, actually leaves `window.matchMedia` fully `undefined` — `typeof` is `"undefined"`, not a broken function — so the `typeof === "function"` fallback correctly covers *that* case, case A in the script above returns `true` with no throw. The gap is specifically UAs/shims where `matchMedia` is present-but-broken, which `typeof` cannot distinguish from present-and-correct.)

### Expected
The guard should validate the actual value it depends on (`.matches` being a boolean) before branching on it, e.g. `typeof window.matchMedia === "function" && window.matchMedia(WIDE_LAYOUT_QUERY) && typeof window.matchMedia(WIDE_LAYOUT_QUERY).matches === "boolean" ? ... : true`, or wrap the call in try/catch — otherwise `applySelectionLayout()` (and therefore `renderData()`) still crashes mid-render for exactly the class of environments (matchMedia present but non-conformant) that issue #61's fix is meant to make renderData resilient against.
