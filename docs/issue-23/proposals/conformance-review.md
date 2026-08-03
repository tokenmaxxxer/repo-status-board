# Conformance-review proposal (issue #23)

Scope: check the merged implementation (PR #24, `issue-23/implementation`,
commit `4ea2e48` on `main`) against issue #23's 6 acceptance-criteria
checkboxes and `docs/specs/flows-schema.md` §2.2 (the `plan` field
contract), working from the artifact and the spec directly per this
role's phase-2 mandate — not from `docs/issue-23/reports/implementation.md`'s
self-report of what was done.

## Method

Phase 2 will produce `docs/issue-23/reports/conformance-review.md` as a
per-requirement verdict table using `review-traceability`'s
`finding-record` skill: one row per requirement below, verdict ∈
{Present, Surface, Absent, Incorrect, Unverifiable}, an evidence pointer
(file:line, test name, or "no local means to observe"), and a rationale.
`review-severity`'s `severity-classification` is applied only to findings
that are not Present, if any survive — per its own trigger condition,
this is not invoked as a blanket pass over every row. No sampling is
needed: the touched surface is small (~350-line diff across 6 files) and
every touched line is in scope for a full check, not a subset.

Each of the 6 acceptance criteria is decomposed below into its
independently-checkable sub-facts (per the survey's observation that
several ACs bundle more than one verifiable claim) — this decomposition
is the discrete requirement list itself; no verdicts are assigned here.

## Requirement list

**R1 — spec-copy sync (AC1).** `docs/specs/flows-schema.md`:
- R1a: §2.2 `plan` table row text matches issue #23's body verbatim
  (type `array<{step:int, roles:[string], done:bool}> | null`, step-line
  format, `‖` parallel-role split, code-fence-ignored parsing, `null` vs
  `[]` distinction, plan-only-issue note).
- R1b: §7 worked example includes a `plan` key consistent with R1a.
- R1c: header "as of" date reflects the re-sync.

**R2 — plan rendering for issues with a plan (AC2).**
- R2a: steps render in `step`-number ascending order (not payload array
  order).
- R2b: each step's role(s) are shown, parallel roles (same step) grouped
  together.
- R2c: each step's `done` state is shown as a distinct visual state.

**R3 — plan-only issue appears in flows (AC3).**
- R3a (locally verifiable): a flow entry with no matching `decision`/
  `session`/`ledger` data is not filtered/dropped by `rsb`'s render path
  (`findDetail`/`renderDetailPanel`'s early-return guard).
- R3b (provider-side, likely Unverifiable from this repo): the entry
  appears "as soon as the issue is created" — no local fixture or live
  upstream payload exists in this repo/environment to drive this
  end-to-end; phase 2 records this as Unverifiable-within-scope rather
  than silently omitting it or guessing a pass.

**R4 — step-role join (AC4).**
- R4a: each step-role is joined against `flows[].roles` to surface
  `loop_state`/`verdict`.
- R4b: each step-role is joined against `decision_queue` to surface
  pending-PR info, and *all* matching PRs are shown when more than one
  exists for the same `(issue, repo, role)` — not just the first.
- R4c: a role with neither a `flows[].roles` entry nor a pending PR
  (the plan-only case) still renders (role name alone), not an error.

**R5 — summary-chip in-progress count (AC5).**
- R5a: the count numerically excludes `delivered`/`closed`-stage flows.
- R5b: the `stage_derived: false` (raw/unmapped `loop_state`) handling
  choice is documented in at least one durable location (schema doc,
  code comment, or implementation record) — not just present in runtime
  behavior with no written trace.

**R6 — `plan: null` vs `[]` distinction recorded (AC6).**
- R6a: `null` and `[]` render as visibly distinct states (not the same
  placeholder).
- R6b: the decision to treat them as distinct (rather than merging them)
  is recorded in a durable location, separate from the rendering fact
  itself.

**R7 — implementation conforms to schema §2.2's `plan` contract**
(the task's second axis, distinct from R1's doc-copy check):
- R7a: `PlanStep`/`Flow.plan` shapes match §2.2's
  `array<{step:int, roles:[string], done:bool}> | null` type.
- R7b: `normalize_payload()` preserves `null` vs `[]` as distinct values
  per §2.2's "never interchangeable" clause.
- R7c: the missing-`plan`-key case (schema §2.2 is silent on it) is
  handled by an explicit, stated repo-local policy rather than an
  unstated/accidental fallthrough — recorded as an extension of the
  schema, not scored as a schema violation either way.

## Out of scope for this role

- Re-litigating PR #24's own second-round cross-review (4 findings
  already addressed per `implementation.md`) — phase 2 will independently
  re-check the artifact against R1-R7 above, not re-run that review, but
  will not re-open findings outside this issue's 6 ACs / §2.2 scope.
- Fixing anything found — per contract, conformance-review records
  findings; it does not patch `src/`/`test/`. Any non-Present verdict
  hands off to a follow-up issue, matching this repo's
  `docs/issue-4/reports/conformance-review.md` precedent.
- `src/rsb/render.py` (CLI text renderer) plan output — issue #23's
  acceptance criteria are dashboard-only; not part of R1-R7.
- New JS test harness / accessibility — both already explicitly
  out-of-scope calls made by the approved implementation proposal
  (`docs/issue-23/proposals/implementation.md`), not reopened here.

## Deliverable

`docs/issue-23/reports/conformance-review.md`: one row per R1a-R7c above
(19 sub-requirements), verdict (Present/Surface/Absent/Incorrect/
Unverifiable), evidence pointer, rationale; a findings section,
severity-classified, for any non-Present row.
