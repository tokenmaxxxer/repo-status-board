files:
- src/rsb/web/dashboard.js
- src/rsb/web/dashboard.css
- test/rsb_tests/test_dashboard_dom.py
- docs/specs/screen-spec.md
- docs/specs/design-system.md

## Request

이슈 #38(PR #43)의 step 2 관찰(`docs/issue-38/reports/execution-observation.md`
F1·F3)이 남긴 두 공백을 처리한다: (1) 세 번째 오류 표면 `renderErrors`
(`dashboard.js:355-365`, 호출부 `:632`)가 AC5 규칙(요약+접힌 상세, 내부
경로 비노출)을 적용받지 못한 채 항상-표시 상태로 남아 있는 문제, (2)
`.number-link`(8×17px)를 WCAG 2.5.8 인라인 예외로 범위 밖 처리한 issue-38
승인 결정(`docs/issue-38/proposals/implementation.md:310-312`)이 조건으로
건 phase-2 실측 확인이 실제로는 수행·보고되지 않은 문제. PR #43 이 랜딩한
나머지 8개 AC 구현은 무변경.

## Constraints

- PR #43 이 이미 충족한 8개 AC(AC1/2/3/4-사이즈된세컨트롤/6/7/8/9)의
  구현은 무변경 — survey §3 이 명시한 write set 밖 함수/CSS 규칙은
  손대지 않는다.
- 새 디자인 토큰·새 런타임 의존성 금지(issue-38 관례 그대로) — 기존
  CSS 커스텀 프로퍼티(`--color-status-error-*`, `--space-*` 등)만
  재사용한다.
- 새 테스트 하네스 도입 금지 — `test/rsb_tests/test_model.py`의
  `node -e` pure-function 관례와 `test/rsb_tests/test_dashboard_dom.py`의
  jsdom DOM 관례만 확장한다(survey §4).
- 이 phase-1 세션은 브라우저 자동화가 없는 샌드박스에서 실행됐다(survey
  §2 — `google-chrome`/`chromium` 바이너리 없음, `python3 -c "import
  playwright"` → `ModuleNotFoundError`, issue-38 phase 2가 겪은 것과 같은
  차단). `.number-link`의 "실측"은 이번에도 실제 픽셀 렌더링이 아니라
  CSS 박스 모델·DOM 구조를 WCAG 2.5.8 인라인 예외 텍스트에 대조하는
  판정으로 대체되며(scout-brief), 이는 대체이지 은폐가 아니라고 phase-2
  기록에 명시한다.

## Rationale

**Requirement 1 — "제거" 안을 채택하고 "배너처럼 접어서 유지" 안은
alternative considered and rejected 이다.** survey §1 이 `renderData`의
두 조건식(전체-실패 조기 반환, 부분-배너 조건)을 직접 대조해 증명한
대로, `renderErrors`가 비어 있지 않은 출력을 내는 모든 도달 가능
상태에서 부분 배너도 정확히 같은 `{repo}: {message}` 데이터를 이미 접힌
`<details>`로 렌더링한 뒤다 — 겹치지 않는 경우가 하나도 없다.
`renderErrors`도 배너처럼 `collapsibleDetailHtml`로 감싸 유지하는 대안을
검토했으나, 그 경우 화면에 같은 실패 목록이 두 개의 독립된 접힌 섹션으로
중복 표시되어 scout-brief 가 인용한 single-source-of-truth 원칙(같은
실패는 한 곳에서만 보여준다)에 반하고, `screen-spec.md` §1.9
(`ErrorListItem`)가 issue #4 때 작성된 뒤 issue #29/#38 어느 쪽의
접힌-상세 도입 때도 갱신되지 않은 채 방치됐다는 사실(survey §1, `git
log -S`로 확인)도 이 표면이 애초에 banner와 별도 존재해야 할 근거로
유지된 적이 없었음을 뒷받침하기 때문에, 이 유지 대안은 rejected —
대신 `renderErrors` 제거 + 호출부 삭제 + `screen-spec.md` §1.9 삭제
(§2.5 가 이미 그 자리를 규정) 쪽을 택한다.

**Requirement 2 — WCAG 2.5.8 인라인 예외는 성립하지 않는다고 판정하고
최소 크기를 적용하는 안을 택하며, "issue #38 본문의 8×17px 실측치를
그대로 F3 충족 근거로 간주" 하는 대안은 alternative considered and
rejected 이다.** 1차 출처(W3C `Understanding SC 2.5.8`, 직접 WebFetch
인용, scout-brief)의 예외 문구는 "타깃이 문장 안에 있거나 비-타깃
텍스트의 line-height 로 크기가 제약되는 경우"로 좁다. `.number-link`가
실제로 등장하는 두 문맥(`dashboard.js:243`의 `.issue-cell` — 옆에 있는
것은 텍스트가 아니라 `.row-toggle` 버튼뿐; `dashboard.js:254`의 `.mono`
— 셀 안의 유일한 내용물) 어느 쪽에도 링크를 둘러싼 산문 텍스트가 없다 —
이는 보조 출처들(TestParty, AllAccessible)이 명시적으로 예외 미적용
사례로 드는 "표 셀/리스트 항목의 단독 링크"와 정확히 같은 모양이다.
"8×17px 실측치가 이미 있으니 그것으로 충분" 하다는 대안은, 그 수치가
*문제의 크기*를 잰 것이지 issue-38 이 승인 조건으로 건 *예외 성립 여부
판정*이 아니며(survey §2), F3가 바로 이 판정 자체가 한 번도 수행되지
않았다고 지적한 지점이라는 이유로 rejected 된다. 판정 결과가 "예외
불성립"이므로 issue #56 요구사항 2의 괄호 조건("성립하지 않으면 최소
크기 적용 포함")에 따라 최소 크기 CSS를 적용하며, 이 저장소에 이미
존재하는 `.row-toggle`의 `min-width: 24px; min-height: 24px; display:
inline-flex; align-items: center; justify-content: center` 패턴을
재사용한다 — 패딩으로 히트박스만 넓히는 방식도 검토했으나, 새 기법을
하나 더 들여오는 대신 이미 검증된 동일 저장소 관례를 따르는 쪽을
scout-brief가 지지하므로 이 패딩 안 역시 rejected 되고 rather than
inventing a new technique, the existing `.row-toggle` box-model pattern
is reused instead. `.issue-cell`의 flex 정렬과 `.mono` 셀 안에서의
줄바꿈/정렬 영향은 phase 2 구현 시 `inline-flex` 적용 후 실제 렌더
확인으로 결정한다(브라우저가 있다면 `rsb serve`, 없다면 jsdom + 계산된
CSS 값 대조로 대체하고 그 대체를 기록에 명시).

## What will be done

1. `dashboard.js`: `renderErrors` 함수와 `dashboard.js:632`의 호출부를
   삭제한다. `renderData`의 나머지 렌더 순서(Decision queue → Flows →
   Sessions → Hygiene → Accounting)는 그대로 유지한다.
2. `dashboard.css`: `.number-link`(`:248-259`)에 `.row-toggle`과 같은
   `min-width: 24px; min-height: 24px; display: inline-flex;
   align-items: center; justify-content: center`를 추가한다. `.mono`
   컨텍스트와 `.issue-cell` 컨텍스트 양쪽에서 레이아웃이 깨지지 않는지
   확인하고, 필요하면 `.issue-cell`의 `gap`/정렬 규칙을 그에 맞게
   조정한다(새 토큰 추가 없이 기존 `--space-*` 값 범위 내에서).
3. `screen-spec.md`: §1.9 "Errors panel — `ErrorListItem`"을 삭제하고,
   §2.5 "Partial failure (banner)"에 이 표면이 partial-failure 오류의
   유일한 표시 지점이라는 한 줄을 추가한다. `design-system.md` §5
   프로즈(24×24px 보장 컨트롤 목록)와 §6 `DataTable` 행에
   `.number-link`를 24×24px 최소 크기 목록으로 편입한다.
4. `test/rsb_tests/test_dashboard_dom.py`에 partial-failure 시나리오
   테스트 1건을 추가한다: 성공 repo와 실패 repo가 섞인 payload로
   `renderData`를 구동한 뒤, `#main-content`의 렌더된 텍스트(요소 범위가
   아니라 문서 범위 — issue-38 execution-observation F1의 근본 원인이
   지적한 element-scoped assertion의 재발을 막기 위해)에 실패 repo의
   raw 메시지가 접히지 않은 채로는 등장하지 않는다는 것과, `renderErrors`
   가 만들던 `"Errors"` 제목의 `<section>`이 더 이상 존재하지 않는다는
   것을 함께 단언한다.
5. 이 record(`docs/issue-56/reports/implementation.md`)에 F3 판정
   근거(WCAG 1차 출처 인용, 두 DOM 문맥, 예외 불성립 결론)를 requirement
   2의 "실측 보고"로 남긴다.

## Out of scope

- PR #43 이 이미 충족한 8개 AC(AC1/AC2/AC3/AC4의 세 컨트롤/AC6/AC7/AC8/
  AC9)의 구현 변경.
- `execution-observation.md`의 F2(어서션 카운트 불일치)와 F4(PR #43
  제목이 "phase 1"으로 남은 문제) — 이슈 #56 요구사항에 포함되지 않은
  기록/메타데이터 항목.
- 실제 브라우저·스크린리더로의 렌더 확인 — 이 샌드박스에 그 수단이
  없다는 것은 이미 issue-38 phase 2 가 겪고 disclose 한 동일한 제약이며,
  이 phase-1 세션도 재확인했다(survey §2, Constraints).
- `render.py`(CLI 텍스트 렌더러)·`webserver.py` 등 백엔드 변경 — 이
  이슈는 프런트엔드 렌더링/접근성 범위다(issue-38 관례와 동일).

## How you'll know it worked

- `node --check src/rsb/web/dashboard.js` clean 상태를 유지한다.
- 기존 `test/rsb_tests/test_model.py`, `test/rsb_tests/test_dashboard_dom.py`
  전체가 무회귀로 통과한다(`renderErrors`를 참조하는 기존 테스트가 0건임을
  survey §1 이 이미 확인했으므로 제거로 인한 기존 테스트 파손은 예상되지
  않는다).
- 새로 추가되는 1건의 jsdom 테스트(What will be done §4)가 통과해,
  partial-failure 상태에서 "Errors" 섹션이 더 이상 렌더되지 않고
  `#main-content`의 비-접힌 텍스트에 raw 오류 메시지가 없다는 것을
  document-scope 로 단언한다.
- `screen-spec.md`/`design-system.md` 갱신 후 `grep -n "ErrorListItem"
  docs/specs/screen-spec.md`가 빈 결과를 반환하고(§1.9 삭제 확인),
  `grep -n "number-link" docs/specs/design-system.md`가 24×24px 문구를
  포함한 줄을 반환한다.
- phase-2 record 가 `.number-link`의 WCAG 2.5.8 판정 근거(1차 출처 인용,
  두 DOM 문맥, 예외 불성립 결론)를 requirement 2 의 "실측 보고"로 명시적으로
  담고 있다.
