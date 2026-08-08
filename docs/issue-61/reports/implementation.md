---
code_under_review: pending
loop_state: started
---

# issue-61 phase 2 — implementation record

Approved proposal: `docs/issue-61/proposals/implementation.md` (PR #66).
Approval: issue-level comment `APPROVE issue-61/implementation` by
`jjongkwann` (approvers.md-listed, single-account mode — PR #66's author
and the approving comment are the same account).

## What was done

(in progress — this section is updated as phase-2 build proceeds)

## Scope

Per the approved proposal's "What will be done" (items 1-6):

1. `dashboard.js:508` — replace unguarded `window.matchMedia(...)` with
   inline feature-detection + return-value validation, `isWideLayout`
   local variable.
2. `dashboard.js:452-454` — `detailRowHtml` gets a stable `id="detail-row"`.
3. `applySelectionLayout` narrow branch — selected button's
   `aria-controls` overwritten to `"detail-row"`.
4. `test_dashboard_dom.py` — new narrow-layout case asserting
   `aria-controls` IDREF resolution.
5. `screen-spec.md` §1.3/§1.6 — describe both layout branches.
6. Requirement 3 (§20 audit) verdict: module-scope `document.getElementById`
   (7 occurrences) stays out of scope — recorded here, no code change.

## Why / upstream basis

Issue #61 (F1/F2, carrying forward #36 conformance-review F1/F2 and #38
R2f). Root cause and fix direction are both settled upstream: #36's
conformance-review Appendix A4 instrumented probe confirmed the crash
mechanism and that both layout branches render correctly once
`matchMedia` is supplied; this issue's own phase-1 survey (`docs/issue-61
/reports/implementation/survey.md` §1) spiked the exact fix and measured
9/9, 66/66 green before this proposal was written.

## What did not work

None yet.

## Open findings

None yet.

## Next steps

Dispatch phase-2 build (code + test + doc changes per Scope, red-green
verification, then commit).

## Open finding resolution path

N/A — no open findings yet; this section will be populated if any surface
during the build.

## Closed checks

(to be filled at completion)
