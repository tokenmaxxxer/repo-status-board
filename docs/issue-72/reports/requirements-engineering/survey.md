# Current-state survey — issue #72

## Upstream basis

- `docs/issue-44/reports/conformance-review.md` R5a (line 93): scores AC2's
  fourth item (mobile-overflow) **Absent** and names the three-way spec
  contradiction — AC2 counts 4 items, 요구사항 2 lists 3 bullets, 범위 밖
  excludes visual regression.
- `docs/issue-44/reports/execution-observation.md` O7 (lines 136-146):
  independently confirms the exclusion is *dispositioned, not silent* (a
  reason is recorded), but AC2's literal text stays unmet on that item.
- Both records route the contradiction to "the issue author" / "a product
  decision" without resolving it — that is the exact gap issue #72 opens.

## What the contradiction is actually about

`gh issue view 44` 원문 확인:
- 요구사항 2 (최소 커버리지) lists exactly 3 bullets: repo-filter 배선,
  row-toggle `aria-expanded`, `load()` fetch 경로.
- AC2 checkbox text says "배경의 결함 3건 + Absent 1건에 각각 대응하는
  테스트가 있고" — 4 items, where 결함 3건 = 배경 목록의 세 항목(레포
  필터, row-toggle, **모바일 오버플로**) and Absent 1건 = the issue #27
  fetch-path gap. Repo-filter/row-toggle/fetch-path map cleanly onto the 3
  bullets; **mobile-overflow is the fourth AC2 item with no matching
  bullet**.
- 범위 밖 bullet 1 explicitly excludes "시각 회귀 테스트(스크린샷 비교)".

## Is mobile-overflow inherently a visual-regression check?

Traced the actual defect and its fix in the repo, not just the issue text:

- Issue #38 (문서 title "디자인 게이트 P1/P2 보완") P1-1 names the root
  cause precisely: `#main-content { min-width: 0 }` missing (grid/flex
  items default to `min-width: auto`, so their content's intrinsic width
  pushes the whole page into horizontal scroll instead of scrolling only
  the table).
- The landed fix is present in `src/rsb/web/dashboard.css`:
  - `:412-413` — `#main-content, #detail-panel-slot { min-width: 0; }`,
    comment at `:407` cites "P1-1" by name.
  - `:181` — `.data-table { min-width: 640px; }` (explicit table floor).
  - `:219` — `.table-scroll { overflow-x: auto; width: 100%; }`.
- The wrapper that makes the scroll-container structural (not just CSS)
  is emitted in `src/rsb/web/dashboard.js:205`:
  `` `<div class="table-scroll"><table class="data-table">...` ``,
  with a same-file comment at `:201-203` naming exactly this
  fix mechanism.
- `test/rsb_tests/test_dashboard_dom.py` and `test_model.py`: grepped for
  `table-scroll`, `scrollWidth`, `overflow` — **zero matches**. No test
  anywhere asserts this structure exists.

This means the mobile-overflow *fix* is a discrete, named DOM-structure +
stylesheet-rule pair, not merely "whatever pixels render at 390px." A test
can assert the structure/rule exist without measuring rendered layout at
all.

## Why jsdom can't do the literal thing AC2 implies

jsdom has no CSS layout engine — `getBoundingClientRect`, `offsetWidth`,
`scrollWidth` on jsdom elements are always 0 regardless of markup or
stylesheet content (this is documented jsdom behavior, confirmed by
`reports/test-authoring.md:251-259` and R5a's own check). Any assertion
built on those APIs would pass or fail independent of the real defect —
not a valid regression test. That rules out a jsdom-only literal
reproduction of "390px → 621px."

## Options on the table

1. **(a) Non-visual reformulation**: assert the structural/CSS-rule
   fingerprint of the fix — `.table-scroll` wrapper present in the
   rendered table HTML, `min-width: 0` present on `#main-content` /
   `#detail-panel-slot` rules, `overflow-x: auto` present on
   `.table-scroll`. This is a DOM-string/stylesheet-text assertion, not a
   screenshot or computed layout — stays inside 범위 밖's exclusion (no
   screenshot comparison, no layout engine). It reproduces "would this
   fail pre-fix?": deleting `min-width: 0` or the `table-scroll` wrapper
   is exactly the regression this defect was.
2. **(b) Explicit removal**: strike AC2's fourth item, rescope
   mobile-overflow coverage to a future browser-automation-based
   visual-regression issue (would itself have to overturn 범위 밖 bullet
   1), and record why: real intrinsic-width regressions the current fix
   didn't anticipate (e.g. a future wide element added inside
   `#main-content`) would not be caught by (a)'s structural fingerprint.

## Constraint (a) does not remove

Even under (a), a *different* mobile-overflow regression — a new element
added inside `#main-content` whose intrinsic width the P1-1 min-width:0
override doesn't shrink — would not be caught, because jsdom cannot
compute what actually overflows. (a) protects the *known, named* fix
mechanism, not the general property "the page never overflows at 390px."
That residual gap is real and should be named in the requirement, not
hidden.
