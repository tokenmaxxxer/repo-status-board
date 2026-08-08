---
status: proposed
files:
  - docs/issue-72/reports/requirements-engineering.md
---

## Intent

Reconcile the AC2 contradiction issue #44's conformance-review (R5a) and
execution-observation (O7) records both flagged and declined to resolve:
AC2 counts four coverage items, 요구사항 2 lists three bullets, and 범위
밖 excludes the visual-regression technique the fourth item
(mobile-overflow) would seem to need. Produce, in phase 2, a requirements
record that disposes of the fourth item one way or the other, with every
requirement statement carrying an ID and a verification method.

## Constraints established so far

- Upstream basis is fixed by the issue: R5a
  (`docs/issue-44/reports/conformance-review.md:93`) and O7
  (`docs/issue-44/reports/execution-observation.md:136-146`) must both be
  cited.
- No AC item may end up both required and excluded — the disposition must
  be explicit either way.
- If resolution genuinely needs a product decision, the record must name
  the exact decision and route it, not silently pick.
- write_scope for this role is [] until phase 2 approval — this proposal
  and its survey/scout-brief are the only writes this turn.

## What will be done (recommended direction, confirmed by survey)

The survey (`docs/issue-72/reports/requirements-engineering/survey.md`)
traced the actual mobile-overflow fix in the repo, not just the issue
text: it is a named, discrete DOM-structure + stylesheet-rule pair
(`#main-content, #detail-panel-slot { min-width: 0 }` at
`src/rsb/web/dashboard.css:412-413`, `.table-scroll { overflow-x: auto }`
at `:219`, and the `<div class="table-scroll">` wrapper emitted at
`src/rsb/web/dashboard.js:205`), currently asserted by no test. jsdom
cannot compute real layout (`offsetWidth`/`scrollWidth`/
`getBoundingClientRect` are always 0 there — confirmed both in-repo via
`reports/test-authoring.md:251-259` and externally, see scout-brief), so a
literal "390px → no overflow" test is not achievable in the existing
harness. But the field's accepted jsdom-tier substitute for a
layout-dependent defect is a structural/CSS-declaration assertion, not a
screenshot — which stays inside 범위 밖's screenshot/pixel-comparison
exclusion.

Phase 2 will therefore write `docs/issue-72/reports/requirements-engineering.md`
recommending **(a)**: reformulate AC2's fourth item as a non-visual,
DOM-string/stylesheet-text test —
assert the rendered table markup contains the `table-scroll` wrapper and
that `dashboard.css` declares `min-width: 0` on `#main-content`/
`#detail-panel-slot` and `overflow-x: auto` on `.table-scroll` — that
would fail if any of those three declarations were reverted (the actual
regression shape of this defect). 요구사항 2 gains a fourth bullet
matching AC2's count; 범위 밖's visual-regression exclusion is left
untouched since no screenshot or computed layout is involved. The record
will also name, explicitly, the residual gap this does not close: a
*different* future overflow (e.g. a new wide element added inside
`#main-content` that the existing min-width:0 override doesn't shrink)
would not be caught, because that requires real layout computation this
harness cannot do — and will state that catching it is out of scope
per 범위 밖 bullet 1 unless a future issue deliberately overturns that
exclusion.

Each requirement in the phase-2 record will carry an ID, an EARS-pattern
statement, a verification method, and a verification condition, and a
traceability matrix will link each ID back to R5a/O7 and forward to
`test/rsb_tests/test_dashboard_dom.py`.

## Out of scope

- Writing or editing the test itself (`test/**` is not this role's
  write_scope; a future test-authoring session implements it).
- Overturning 범위 밖's visual-regression exclusion — that would be a
  separate product decision, only named as a possible future path if the
  residual gap above is later judged unacceptable.
- Editing `docs/issue-44/**` records — they are read-only upstream basis.

## How you will know it worked

- `docs/issue-72/reports/requirements-engineering.md` cites both R5a and O7 by
  file path.
- Every requirement statement in that record has an ID and a verification
  method.
- AC2's fourth item is resolved one way, explicitly (not left both
  required and excluded).

## Adopted norm

Scout-brief's field consensus: when a defect's real assertion needs a CSS
layout engine jsdom does not have, the accepted jsdom-tier substitute is a
structural/CSS-declaration assertion (does the markup/stylesheet contain
the specific rule the fix depends on), never `offsetWidth`/`scrollWidth`
comparisons inside jsdom (always 0, tautological). Adopted here: option
(a), a `.table-scroll`/`min-width: 0`/`overflow-x: auto` declaration
assertion, as the phase-2 recommendation.

## Rejected alternative

Option (b) — striking AC2's fourth item outright and rescoping
mobile-overflow to a future visual-regression issue — was considered and
rejected as the primary recommendation because a non-visual, in-scope
formulation that actually reproduces the regression shape (deleting the
named min-width/overflow-x/wrapper fix) is achievable today, per the
survey. (b) is kept in the phase-2 record as the fallback path only if a
human approver judges the residual gap named above (a *different* future
overflow the structural check can't catch) unacceptable to leave open.

## Plugin-reflection

This proposal is itself the phase-1 deliverable gated by the
proposal-discipline-gate hook; no other repo plugin/hook surface is
touched by this change (no `package.json`, CI, or handbook edits — the
write set is a single `docs/issue-72/**` record).

## Verification plan

Phase 2's record is checked against issue #72's own `## Acceptance`
block: `grep -l "R5a\|O7" docs/issue-72/reports/requirements-engineering*`
must match; every requirement row must carry an ID and a verification
method; and a manual read must confirm no AC item is left both required
and excluded. The hunter dispatch (warrant directive) covers the proposal
and pre-landing transitions separately.
