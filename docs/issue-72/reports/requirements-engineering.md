# Requirements engineering — issue #72

## Upstream basis

- R5a — `docs/issue-44/reports/conformance-review.md:93`: scores AC2's
  fourth item (mobile-overflow) **Absent** and names the contradiction —
  AC2 counts four coverage items, 요구사항 2 lists three bullets, 범위 밖
  excludes the visual-regression technique the fourth item would need.
- O7 — `docs/issue-44/reports/execution-observation.md:136-146`:
  independently confirms the exclusion is dispositioned, not silent (a
  reason is recorded in `docs/issue-44/reports/test-authoring.md:251-259`),
  but AC2's literal text stays unmet on that item.
- Both records route the contradiction to a product decision without
  resolving it. Basis for phase 1's survey and this record: proposal at
  `docs/issue-72/proposals/requirements-engineering.md`, survey at
  `docs/issue-72/reports/requirements-engineering/survey.md`.

## Disposition

Option **(a)** — non-visual reformulation — adopted. AC2's fourth item is
resolved as **required**, restated as a structural/CSS-declaration
assertion that stays inside 범위 밖's visual-regression exclusion (no
screenshot, no computed layout). No AC item is left both required and
excluded: mobile-overflow is required, and the technique it now requires
(DOM-string / stylesheet-text assertion) is not the technique 범위 밖
excludes (screenshot/pixel comparison).

Rejected alternative — option (b), striking the item — is kept as the
fallback path only if a human approver later judges the residual gap
below unacceptable (see Ambiguity/residual gap).

## Requirements

### REQ-72-1
statement: The rendered table markup shall contain a `<div class="table-scroll">` wrapper around each `<table class="data-table">`.
ears_pattern: ubiquitous
verification_method: Test
Given the table-rendering function's return value (`src/rsb/web/dashboard.js:205`), When the markup is searched for `<div class="table-scroll">`, Then it is present for all four dashboard tables and the check fails if the wrapper is removed or renamed.

### REQ-72-2
statement: dashboard.css's `#main-content, #detail-panel-slot` rule block shall declare `min-width: 0`.
ears_pattern: ubiquitous
verification_method: Test
Given `dashboard.css` (`:412-413`) parsed into rule blocks, When the `#main-content, #detail-panel-slot` block specifically is inspected (not a whole-file substring search), Then `min-width: 0` is declared inside that block, and the check fails if removed, moved to an unrelated/ineffective selector, or the value changes.

### REQ-72-3
statement: dashboard.css's `.table-scroll` rule block shall declare `overflow-x: auto`.
ears_pattern: ubiquitous
verification_method: Test
Given `dashboard.css` (`:219`) parsed into rule blocks, When the `.table-scroll` block specifically is inspected (not a whole-file substring search), Then `overflow-x: auto` is declared inside that block, and the check fails if removed or moved to an unrelated selector.

Selector-scoping constraint (carried from the after-proposal hunt finding,
folded into the proposal before landing): REQ-72-2 and REQ-72-3's
verification methods must resolve each declaration against its specific
selector block, not a plain substring search over the stylesheet text. A
substring match would still pass if the same declaration text existed on
an unrelated, ineffective selector while the real regression (a grid
item's default `min-width: auto` pulling the page into overflow) was
reintroduced.

요구사항 2 gains a fourth bullet (mapping to REQ-72-1..3 collectively, one
AC2 coverage item): "모바일 뷰 테이블의 가로 스크롤 격리 — `table-scroll`
래퍼와 `#main-content`/`.table-scroll`의 관련 CSS 선언이 존재함을 검증한다."
범위 밖의 시각 회귀(스크린샷 비교) 항목은 변경하지 않는다 — REQ-72-1..3
어느 것도 스크린샷이나 computed layout을 사용하지 않는다.

## Traceability matrix

| ID | Description | Source | Downstream link | Status |
|----|----|----|----|----|
| REQ-72-1 | `table-scroll` wrapper present in rendered table markup | `docs/issue-44/reports/conformance-review.md:93` | `test/rsb_tests/test_dashboard_dom.py` | drafting |
| REQ-72-2 | `min-width: 0` declared on `#main-content, #detail-panel-slot` | `docs/issue-44/reports/execution-observation.md:136-146` | `test/rsb_tests/test_dashboard_dom.py` | drafting |
| REQ-72-3 | `overflow-x: auto` declared on `.table-scroll` | `src/rsb/web/dashboard.css:219` | `test/rsb_tests/test_dashboard_dom.py` | drafting |

Status vocabulary used: `drafting` — the requirement is specified and
traced but its downstream test does not exist yet; authoring the test is
out of this role's `write_scope` ([] per role directive) and belongs to a
future test-authoring session.

## Ambiguity list (resolved)

- **Statement**: "does mobile-overflow require a visual/pixel check, or
  can a structural assertion satisfy AC2's fourth item?"
  - Candidate readings: (1) AC2 literally requires measuring rendered
    width, which only a layout engine (browser automation) can do; (2)
    AC2 requires a test that would catch the actual defect that shipped,
    which the fix's own structural fingerprint (`table-scroll` wrapper +
    two CSS declarations) can do without layout computation.
  - Resolution: reading (2), adopted per scout-brief's field consensus
    (jsdom-tier substitute for layout-dependent defects is a
    structural/CSS-declaration assertion, not `offsetWidth`/`scrollWidth`
    which are always 0 in jsdom). REQ-72-1..3 implement reading (2).

## Residual gap (named explicitly, not hidden)

REQ-72-1..3 protect the *known, named* fix mechanism (the P1-1 min-width
override, the `overflow-x: auto` rule, and the `table-scroll` wrapper). A
*different* future mobile-overflow regression — e.g. a new wide element
added inside `#main-content` whose intrinsic width the existing
`min-width: 0` override does not shrink — would not be caught, because
that requires real layout computation jsdom cannot perform. This gap is
accepted as out of scope per 범위 밖 bullet 1 (시각 회귀 테스트 제외)
unless a future issue deliberately overturns that exclusion in favor of
browser-automation-based visual regression testing. That would be a
separate product decision, not decided here.

## Done

Reconciled the AC2 four-vs-three-vs-exclusion contradiction (R5a, O7) by
adopting option (a): reformulated the mobile-overflow item as three
non-visual, EARS-pattern requirements (REQ-72-1..3) with IDs, verification
methods scoped to specific CSS selectors (per the after-proposal hunt
finding), and Given/When/Then verification conditions; added a
traceability matrix linking each to R5a/O7 and to the (not-yet-authored)
downstream test file; and named the residual layout-computation gap the
structural approach cannot close, routing it to a future product decision
rather than hiding it.

## Why

Both upstream records (R5a, O7) identified the contradiction but
explicitly declined to resolve it, routing it to "the issue author" — this
record is that resolution, requested via issue #72.

## Upstream/basis

be02a70 (this branch, phase-1 proposal + survey + scout-brief), citing
`docs/issue-44/reports/conformance-review.md` (R5a) and
`docs/issue-44/reports/execution-observation.md` (O7).

## Kind and loop_state

kind: structured requirements doc
loop_state: landed

## Open findings

None outstanding. The one open item from phase 1 (selector-scoping
verification-method precision) was folded into REQ-72-2/REQ-72-3 above
before landing.
