# Verification proposal — execution-observation (issue #23)

Status: phase-1 proposal. Scope: this role only, observing PR #24
(`issue-23/implementation` → `main`, merged, merge commit `4ea2e48`).
Grounded in `docs/issue-23/reports/execution-observation/survey.md`'s
gaps and `scout-brief.md`'s adopt/skip decisions. No code changes. This
document proposes a *method*, not a result: no verdict on whether PR #24
is sound appears anywhere below — that judgment is phase-2-only, gated on
approval, and goes into `docs/issue-23/reports/execution-observation.md`.

## 0. Which verdict levels will be checked, and against what evidence

Phase 2 will render all three levels required by this role's contract:

1. **Outcome** — did PR #24 land what issue #23 asked, checked against:
   the issue's 6 acceptance-criteria checkboxes, each mapped to a specific
   file:line in the merged diff (`git show a858b80 -- <path>`) or to the
   `docs/specs/flows-schema.md` text, not to the implementation record's
   summary of itself.
2. **Trajectory** — was the implementation role's own phase-1→phase-2
   path sound, checked against: `git show --stat` on all 3 of PR #24's
   commits (confirms phase 1 touched only `docs/issue-23/` and no
   `src/`/`test/`), the commit-timestamp ordering versus the issue's
   approval-comment timestamp and the PR's cross-review-comment timestamp
   (already pulled in the survey), and the content of
   `docs/issue-23/reports/implementation/survey.md`,
   `scout-brief.md`, and `docs/issue-23/proposals/implementation.md`
   (not yet read in full this session — phase 2 will read them before
   rendering a trajectory verdict, since the survey above only confirmed
   their existence and commit membership, not their content).
3. **Step** — which specific artifact, if any, is deficient, checked
   against: line-by-line diff tracing of `src/rsb/model.py`'s
   `normalize_payload()` plan-extraction branch and
   `src/rsb/web/dashboard.js`'s `isFlowInProgress()`, `planCellLabel()`,
   `buildPlanSteps()`, and `renderPlanSection()`, run by hand against the
   specific cases issue #23 and this task name: `plan: null`, `plan: []`,
   a populated multi-step plan, the summary-chip in-progress count, and
   the step→role→(loop_state/verdict, pending-PR) join.

## 1. Method (substituting for live execution — see scout-brief "Skip")

This session's role directive prohibits re-running the observed role's
code; `docs/issue-4/reports/execution-observation.md` (the prior pass of
this same role) used live `pytest`/HTTP execution, which is **not**
available to this pass for that reason, not a capability gap. Phase 2
will instead:

1. **Static diff tracing, not execution.** For each of the 3 rendering
   cases (`plan: null`, `plan: []`, populated plan) and the aggregation
   case, trace the actual merged code path by hand from the relevant
   `git show a858b80 -- <path>` diff hunk (the Python-side extraction
   branch in `normalize_payload()` and the JS-side `planCellLabel()`/
   `buildPlanSteps()`/`isFlowInProgress()` branches), following each case
   through every conditional it hits, and write the traced path out
   explicitly in the phase-2 record — not just cite the line number and
   assert an outcome.
2. **Test-file reading as corroboration, not proof.** `test/rsb_tests/
   test_model.py`'s new assertions (8 tests named in the implementation
   record) will be read to confirm they actually assert the traced
   behavior (e.g. that the "empty vs null" test asserts on the *return
   value* `{steps: []}` vs `None`, not just a rendered string) — but their
   claimed 41/41-pass result will be reported as *claimed, not
   independently reproduced*, per the re-execution prohibition, rather
   than presented as independently confirmed.
3. **Acceptance-criteria mapping.** Each of the issue's 6 checkboxes will
   get one row in phase 2: criterion text → the specific diff hunk or
   spec-doc line that addresses it → any criterion that has no clean
   1:1 code mapping (the "plan-only issue appears in `flows[]`
   immediately" criterion is largely an upstream/on-the-record data-
   contract fact, not new `dashboard.js`/`model.py` logic) called out
   explicitly as such, not silently marked done.
4. **Trajectory read.** `docs/issue-23/reports/implementation/survey.md`,
   `scout-brief.md`, and `docs/issue-23/proposals/implementation.md` will
   be read in full (not just confirmed to exist) before the trajectory
   verdict is written.
5. **Independence statement** will open the phase-2 record, before any
   verdict language, per this role's ordering requirement.

## 2. Record format

`docs/issue-23/reports/execution-observation.md` (phase-2 output) will
contain: the independence statement first; the three-level verdict
(outcome/trajectory/step), each verdict-bearing sentence with an adjacent
citation (commit SHA / file:line / PR comment URL); a
per-acceptance-criterion table; any deficiency finding in the four-part
blameless shape (impact, timeline, root cause, action item); and a
`loop_state` field updated at each transition.

## 3. Out of scope

- Any code fix for a discovered defect — hand-off only, per this role's
  prohibition on editing the observed role's `src/`/`test/`.
- Re-judging `conformance-review`'s parallel step-2 work — separate role,
  separate branch/PR, not this role's write surface.
- Independently verifying the upstream `on-the-record` repo's
  `flows-schema.md` source-of-truth text byte-for-byte (out of this
  checkout's reach) — the phase-2 record will state this limitation
  explicitly rather than assert a match it cannot check.
