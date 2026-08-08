files:
- src/rsb/web/dashboard.js
- test/rsb_tests/test_dashboard_dom.py
- docs/specs/screen-spec.md

## Request

#61(F1/F2, #36 검토 승계): `applySelectionLayout`(`dashboard.js:508`)의
무가드 `window.matchMedia` 호출이 `matchMedia`를 구현하지 않는 UA(jsdom
포함)에서 `renderData`를 중간 중단시켜 main의 `test_dashboard_dom.py`
2건이 적색이고, `<1200px` 분기에서 모든 `.row-toggle` 버튼의
`aria-controls="detail-panel-slot"`가 실제로는 빈 슬롯을 가리키는 거짓
IDREF 관계가 된다(narrow 분기는 콘텐츠를 `tr.detail-row`로 옮기는데
그 요소에 `id`가 없다). 수정 위치를 트레이드오프와 함께 결정하고
red-green으로 증명하며, aria-controls IDREF를 실제 패널 보유 요소로
정합시키고 `screen-spec.md` §1.3을 갱신하고, `dashboard.js`의 다른
무가드 브라우저 API 호출을 전수 감사해 이번 범위 포함 여부를 판단한다.

## Constraints

- issue #56이 제거한 `renderErrors` 표면 부활 금지.
- 새 런타임 의존성·새 디자인 토큰 금지.
- 시각 회귀 기법은 범위 밖(기존 관례, survey §1 스파이크도 DOM
  값 단언으로만 검증했다).
- 병렬 진행 중인 issue #62(터치 타깃·대비·마스킹)와 파일이 겹치면
  phase 2 시작 시 rebase로 조율한다 — survey §5가 확인한 대로
  `dashboard.js`를 같은 파일·다른 함수/줄 범위로 병행 수정할 가능성이
  있다(`applySelectionLayout`/`rowToggleButtonHtml`/`detailRowHtml`
  vs. #62가 다룰 배너·마스킹 블록).
- 새 테스트 하네스 도입 금지 — `test_dashboard_dom.py`의 기존 jsdom
  `_run_dom_js` 관례(스크립트 문자열 안에서 `window.matchMedia`를
  일시적으로 재정의하는 방식, issue-36 conformance-review Appendix A4의
  계측 프로브와 같은 기법)만 확장한다.

## Rationale

**요구사항 1(수정 위치) — 호출부 인라인 feature-detection 가드를
채택하고, "하네스 matchMedia 스텁 주입"은 alternative considered and
rejected다.** survey §1의 스파이크가 `typeof window.matchMedia ===
"function" ? window.matchMedia(q).matches : true`로 바꾸는 것만으로
`test_dashboard_dom.py` 9/9, 전체 스위트 66/66 green을 실측 증명했다 —
하네스 변경 없이 기존 테스트 파일 그대로 통과한다. 하네스 스텁 안
(Jest/Vitest 생태계의 흔한 해법, scout-brief §2)은 테스트만 통과시키고
실제 `dashboard.js`의 프로덕션 호출부는 여전히 무가드로 남긴다 —
`matchMedia`가 없는 실제 UA(구형 webview 등)나 이 렌더 로직이 장차
비-브라우저 컨텍스트에서 재사용될 경우 크래시가 그대로 재현되므로,
issue-36 conformance-review F1이 "reachable in a default scenario for
any user agent lacking `matchMedia`"로 프레이밍한 위험을 닫지 못한다.
인라인 가드는 이 위험과 테스트 적색을 동시에 닫으므로 두 안을
병행할 기술적 필요도 없다(스텁이 인라인 가드에 추가할 게 없다).
fallback 값은 `true`(와이드)를 택한다 — survey §1이 실측한 대로
`false`로 폴백하면 narrow 분기(`tr.detail-row` 삽입, `#detail-panel-slot`
공백)를 타서 기존 테스트들의 `#detail-panel-slot` 직접 단언과 충돌해
여전히 적색이 남는다.

**요구사항 3(전수 감사, §20) — audit 결과 매트릭스에서 모듈 스코프
`document.getElementById` 7건(`dashboard.js:3-9`)은 이번 이슈 범위 밖으로
제외하고, "이번에 같이 가드한다"는 alternative considered and
rejected다.** survey §4의 감사가 이 저장소 유일의 JS 파일 전체를
전수 스캔해 확인한 대로, 무가드 브라우저 API는 두 클래스뿐이다 — (a)
모듈 스코프 `document.getElementById` 7건, (b) `:508`의 `matchMedia`
1건(F1 본체). `fetch`(:638)는 이미 try/catch로 안전하고 `:169/:556/:595`의
`document.getElementById`는 (a)가 이미 성립한 컨텍스트에서만 도달해
독립 위험이 없다. (a)를 이번에 같이 가드하는 안은, 모듈 로드 시점에
무조건 실행되는 7개 `const` 선언 블록 전체를 지연 초기화나 함수로
재구조화해야 해서(파일 하단 `:658`의 `typeof window !== "undefined"`
가드는 auto-init *부작용*만 감싸지 이 `const` 선언 자체는 감싸지 못한다)
이번 이슈가 요구하는 두 국소 수정보다 훨씬 큰 리팩터이고, (a)로 인한
실패는 현재 관측된 red 테스트가 0건이다 — 두 테스트 하네스
(`test_model.py`의 스텁, `test_dashboard_dom.py`의 jsdom) 모두 `require()`
전에 이미 `global.document`를 채워 두는 관례로 이 경로를 우회하고
있고, 이슈의 Acceptance는 `test_dashboard_dom.py` green 전환과
aria-controls IDREF만 규정한다. "새 의존성·새 토큰 금지" 제약의 정신도
필요 이상의 구조 변경을 지지하지 않는다. 결론: (b)만 이번 범위, (a)는
별도 follow-up 후보로 이 proposal에 명시하고 코드 변경은 하지 않는다.

## What will be done

1. `dashboard.js:508`의 `applySelectionLayout`에서
   `window.matchMedia(WIDE_LAYOUT_QUERY).matches`를 `isWideLayout` 지역
   변수로 바꾸고 그 값을 분기 조건에 재사용한다(survey §1 스파이크의
   `typeof window.matchMedia === "function" ? ... : true` 골격을
   유지하되, 이 phase-1의 warrant hunt(survey.md 말미 "Warrant hunt
   (phase 1)" 섹션, stance 0)가 재현한 갭을 반영해 반환값도 검증한다 —
   `typeof`만 체크하면 `matchMedia`가 함수이지만 `.matches`가 없는
   값(`undefined`/`null`)을 반환하는 손상된 shim에서 여전히 같은 클래스의
   `TypeError`로 크래시한다(hunt가 `node -e`로 직접 재현): `const mql =
   typeof window.matchMedia === "function" ? window.matchMedia(WIDE_LAYOUT_QUERY)
   : null; const isWideLayout = mql && typeof mql.matches === "boolean" ?
   mql.matches : true;`. 새 함수·헬퍼 추출 없이 인라인 두 줄로 끝나
   scout-brief가 채택한 "호출부 인라인" 패턴과 "공유 헬퍼 reject" 판단을
   그대로 유지한다.
2. `dashboard.js:452-454`의 `detailRowHtml`이 만드는
   `<tr class="detail-row">`에 안정된 `id="detail-row"`를 부여한다(선택
   가능한 이슈는 `selectedIssue` 단일 값이라 언제나 최대 1개만 존재하고,
   `renderData`의 `MAIN.innerHTML` 전체 재작성이 매 렌더마다 이전
   `detail-row`를 먼저 지우므로 정적 단일 id로 충분 — `#detail-panel-slot`과
   같은 싱글턴 패턴).
3. 같은 함수의 narrow 분기(`:511-512`)에서 `detailRowHtml` 삽입 직후,
   `selectedRow.querySelector(".row-toggle")`로 선택된 버튼을 찾아
   `aria-controls`를 `"detail-row"`로 덮어쓴다. 와이드 분기·미선택
   상태에서는 `rowToggleButtonHtml`이 매 렌더마다 새로 찍는 기본값
   `"detail-panel-slot"`을 그대로 둔다(다른 버튼은 건드리지 않음 — 선택된
   버튼 하나만 덮어쓰므로 새 `matchMedia` 호출이나 새 순회를 추가하지
   않는다, step 1의 `isWideLayout` 재사용).
4. `test/rsb_tests/test_dashboard_dom.py`에 narrow 레이아웃 케이스 1건을
   추가한다: 클릭 스크립트 안에서 `window.matchMedia = () =>
   ({ matches: false });`로 일시 재정의한 뒤(issue-36 A4 프로브와 같은
   기법, 하네스 자체는 무변경) 토글 버튼을 클릭하고, `#detail-panel-slot`이
   비어 있는 것·`#detail-row`가 존재하고 패널 콘텐츠를 담는 것·버튼의
   `aria-controls` 값이 `"detail-row"`인 것·그 값으로
   `document.getElementById(...)`를 resolve하면 실제 `#detail-row`
   요소가 나오는 것(IDREF 해소 자체를 단언)을 함께 확인한다.
5. `screen-spec.md` §1.3(`:59-64`)의 `aria-controls="detail-panel-slot"`
   문장에 각주 형태로 `<1200px`(narrow) 분기에서는 같은 속성이
   `"detail-row"`를 가리키도록 §1.6의 레이아웃 스위치에 맞춰 동적으로
   바뀐다는 한 줄을 추가하고, §1.6(`:104-111`)에도 그 값 전환을 명시하는
   대칭 문장을 추가해 두 섹션이 서로를 참조하게 한다.
6. survey §4 audit 결과(모듈 스코프 `document.getElementById` 7건은
   범위 밖)를 phase-2 record의 요구사항 3 판정 근거로 남긴다(코드
   변경 없음).

## Out of scope

- `dashboard.js:3-9` 모듈 스코프 `document.getElementById` 7건의 가드화
  (Rationale 요구사항 3) — 별도 follow-up 후보로만 기록.
- `dashboard.js:169/556/595`의 `document.getElementById`, `:638`의
  `fetch`(이미 안전) — audit에서 독립 위험 없음으로 판정, 변경 없음.
- issue #62의 터치 타깃·대비·마스킹 작업(`dashboard.css`,
  `src/rsb/fetch.py`) — 파일 겹침 없음(survey §5), rebase 조율만 Constraints에 기록.
- 실제 브라우저·스크린리더 렌더 확인, 시각 회귀 — 이 샌드박스의 기존
  제약(issue-38/#56 phase 2가 이미 disclose).

## How you'll know it worked

- `python3 -m pytest test/rsb_tests/test_dashboard_dom.py -v`가 현재
  적색인 `test_row_toggle_click_opens_detail_and_flips_aria_expanded`,
  `test_row_toggle_reactivating_open_button_closes_it` 2건을 포함해
  전건(기존 9건 + 신규 1건 = 10건) green, 0 skipped로 전환한다 — 수정
  전 2건 실패를 phase-2 record에 red로, 수정 후 전건 통과를 green으로
  남겨 red-green을 증명한다.
- `python3 -c "import sys; sys.path.insert(0,'src'); import pytest;
  sys.exit(pytest.main(['test/','-q']))"`가 전체 스위트(현재 66건 +
  신규 1건 = 67건) green을 보고한다.
- 신규 narrow 케이스가 `aria-controls` 값으로 `document.getElementById`를
  호출해 실제 `#detail-row` 요소를 resolve하는 것을 직접 단언한다(F2
  요구의 "DOM 테스트로 IDREF 해소를 단언" 충족).
- `grep -n "detail-row" docs/specs/screen-spec.md`가 §1.3/§1.6 양쪽에서
  결과를 반환한다(양 분기 서술 갱신 확인).
- `node --check src/rsb/web/dashboard.js`가 clean 상태를 유지한다.
