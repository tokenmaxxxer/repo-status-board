# Conformance-review record (issue #23)

loop_state: reported

## What was done

Checked the merged implementation (PR #24, `issue-23/implementation`,
commit `4ea2e48` on `main`) against issue #23's 6 acceptance criteria and
`docs/specs/flows-schema.md` §2.2, decomposed into 19 independently
verifiable sub-requirements (R1a-R7c) per the approved phase-1 proposal.
Verdicts below were derived from direct code/spec inspection and a fresh
local test run, not from `docs/issue-23/reports/implementation.md`'s
self-report.

## Upstream basis

Rests on `docs/issue-23/proposals/conformance-review.md` (this role's
approved phase-1 proposal, requirement list R1-R7) and
`docs/issue-23/reports/conformance-review/survey.md` (current-state
survey), both approved via issue #23 comment
`APPROVE issue-23/conformance-review` (jjongkwann, listed in
`docs/specs/approvers.md`; single-account mode, PR #25 author ==
approver). Subject artifact: PR #24, merged `4ea2e48`. No `src/`/`test/`
change is made by this record.

Method: `review-traceability`'s `finding-record` verdict set (Present /
Surface / Absent / Incorrect / Unverifiable) per sub-requirement, each
with an evidence pointer and rationale. Verification method is either
code inspection or an existing automated test (named per row); no new
tests were written by this role. Test suite re-run this session:
`python3 -c "import sys; sys.path.insert(0,'src'); import pytest;
sys.exit(pytest.main(['test/','-q']))"` → **41 passed**, 0 failed,
matching the implementation record's claimed count.
`review-severity`'s `severity-classification` is not invoked — every row
below is Present or Unverifiable-within-scope; no Surface/Absent/
Incorrect finding survived to require severity weighting.

## R1 — spec-copy sync (AC1)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R1a: §2.2 `plan` row covers type, step-line format, `‖` split, code-fence-ignored, header-variant match, `null` vs `[]` distinction, plan-only-issue note | Present | `docs/specs/flows-schema.md:96` | The upstream contract is mirrored in English while issue #23's body states the same facts in Korean — a byte-identical string match is impossible across that language boundary, so "verbatim" is read (as the proposal's own parenthetical frames it) as: every sub-fact enumerated in the issue body appears in the row. All seven do: the union type, the `- [ ] step <N> <role>[ ‖ <role2> ...]` format, the `‖`-splits-into-`roles` rule, code-fence-ignored parsing, the `## 실행 계획 (...)` header-variant match, the `null`≠`[]` "never interchangeable" clause, and the plan-only-issue-gets-an-entry-immediately note |
| R1b: §7 worked example includes a `plan` key consistent with R1a | Present | `docs/specs/flows-schema.md:296-298` | `flows[0].plan` = `[{"step": 1, "roles": ["implementation"], "done": false}]`, shape matches the R1a type exactly |
| R1c: header "as of" date reflects the re-sync | Present | `docs/specs/flows-schema.md:5` reads "as of 2026-08-03"; survey.md records the pre-PR#24 copy read "as of 2026-07-31" | Date was bumped by the same commit (`4ea2e48`, authored 2026-08-03) that added the `plan` row/example, consistent with a genuine re-sync rather than a stale carry-over |

## R2 — plan rendering for issues with a plan (AC2)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R2a: steps render in `step`-ascending order, not payload order | Present | `src/rsb/web/dashboard.js:255` (`flow.plan.slice().sort((a, b) => a.step - b.step)`); `test/rsb_tests/test_model.py:160-172` (`test_dashboard_js_plan_steps_sorted_by_step_number_ascending`, drives the real `dashboard.js` via `node -e`, fixture lists steps 2,1,3 → asserts output `[1,2,3]`) | Automated test exercises the shipped function directly, not a reimplementation |
| R2b: each step's role(s) shown, parallel roles (same step) grouped together | Present | `src/rsb/web/dashboard.js:284-293` (`renderPlanSection`, `step.roles.map(...).join(" ‖ ")`) | Code inspection only — `renderPlanSection` is not in `module.exports` (`dashboard.js:428`: only `ageBucket, ageBucketStatus, selectSummary, isPageEmpty, buildPlanSteps` are exported), so no Node-subprocess test drives this string-building function directly; the underlying data grouping it consumes (`buildPlanSteps`'s per-step `roles` array) is test-covered (R2a, R4b rows) |
| R2c: each step's `done` state shown as a distinct visual state | Present | `src/rsb/web/dashboard.js:294` (`doneBadge`: `status-success`/`"done"` vs `status-neutral`/`"pending"`) | Code inspection only, same export-surface gap as R2b — no browser/DOM was driven this session (matches the same limitation `docs/issue-4/reports/conformance-review.md` recorded) |

## R3 — plan-only issue appears in flows (AC3)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R3a: a flow entry with no matching decision/session/ledger data is not filtered/dropped by `rsb`'s render path | Present | `src/rsb/web/dashboard.js:165-178` (`flowRows` maps `data.flows` unconditionally, no filter predicate); `:314` (`renderDetailPanel`'s guard `if (!detail.decision && !detail.flow && detail.sessions.length === 0 && !detail.ledger)` requires flow to also be falsy to hide the panel); `src/rsb/model.py:279-303` (`merge_repos`/`normalize_payload` extend/build lists with no cross-referencing filter against decisions/sessions/ledger) | Two independent non-filtering points confirmed: the Flows table row (`flowRows`) never filters on cross-referenced data at all, and the detail-panel guard only hides when `detail.flow` is itself falsy — a plan-only flow entry present in `data.flows` makes `detail.flow` truthy, so the guard does not fire regardless of decision/session/ledger absence |
| R3b: the entry appears "as soon as the issue is created" (provider-side timing) | Unverifiable | No local fixture or live `on-the-record`/`spawn.py` checkout in this repo/environment | Per `flows-schema.md` §2.2's own text, this is `on-the-record`'s (`flows --json` producer's) behavior, not `rsb`'s — `rsb` only consumes and renders `data.flows` as received. This repo has no means to drive a real plan-only-issue-creation event end to end. Recorded as Unverifiable-within-this-repo per the proposal's stated method, not silently omitted or scored as a pass |

## R4 — step-role join (AC4)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R4a: each step-role joined against `flows[].roles` to surface `loop_state`/`verdict` | Present | `src/rsb/web/dashboard.js:261` (`buildPlanSteps`: `(flow.roles \|\| []).find((r) => r.role === roleName)`); `:286-287` (`renderPlanSection` reads `r.roleStatus.loop_state`/`.verdict` into a badge) | Code inspection; `PLAN_STEPS_PAYLOAD` fixture (`fixtures.py:141-185`) has matching `roles` entries for both plan roles, but no test asserts on `roleStatus` specifically — existing tests target the PR-join (R4b) and sort order (R2a) facts only |
| R4b: joined against `decision_queue`, showing *all* matching PRs for the same `(issue, repo, role)`, not just the first | Present | `src/rsb/web/dashboard.js:265-267` (`decisions.filter((d) => d.issue === issue && d.repo === repo && d.role === roleName)`); `test/rsb_tests/test_model.py:175-193` (`test_dashboard_js_plan_steps_join_shows_all_pending_prs_not_just_first`, two PRs #501/#502 against the same role → asserts both returned) | Automated test on the shipped function |
| R4c: a role with neither a `flows[].roles` entry nor a pending PR still renders (role name alone), not an error | Present | `src/rsb/web/dashboard.js:261,265-266` (`roleStatus` defaults to `null` via `\|\| null`; `pendingPrs` defaults to `[]`, the natural empty-array result of `.filter()` finding no match — no throw path); `:286-292` (`renderPlanSection`: `statusBadge`/`prBadges` both render as empty strings when their inputs are `null`/`[]`, leaving `<span class="mono">${role}</span>` alone) | Code inspection; no dedicated test isolates this exact zero-match case, but the code path is the unconditional default branch of R4a/R4b's already-tested logic — no separate conditional exists that could error instead |

## R5 — summary-chip in-progress count (AC5)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R5a: count numerically excludes `delivered`/`closed`-stage flows | Present | `src/rsb/web/dashboard.js:45-47` (`isFlowInProgress`); `test/rsb_tests/test_model.py:220-246` (`test_dashboard_js_select_summary_counts_in_progress_and_raw_unmapped_flows`: 5-flow fixture with one each of proposal/approved/delivered/closed/unmapped → asserts "3 flows in progress", i.e. delivered+closed correctly excluded) | Automated test on the shipped function. Note: a `stage_derived: false` flow is *always* counted in-progress regardless of its raw `loop_state`'s true semantic stage (an intentional, documented over-count risk, see R5b) — this is a distinct policy question from R5a's literal claim (which is about the five-enum `stage` field) and does not make R5a Incorrect |
| R5b: `stage_derived: false` handling choice documented in a durable location | Present | `src/rsb/web/dashboard.js:28-44` (17-line comment directly above `isFlowInProgress` stating the policy, its rationale, the rejected alternative, and a cross-reference to `docs/issue-23/proposals/implementation.md`) | Comment is in the shipped source file itself — durable and co-located with the logic it documents, satisfying AC5's "기준 문서화" (criterion: documented) clause beyond just correct runtime behavior |

## R6 — `plan: null` vs `[]` distinction recorded (AC6)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R6a: `null` and `[]` render as visibly distinct states | Present | `src/rsb/web/dashboard.js:156-163` (`planCellLabel`: `null`/`undefined` → "—" secondary text; `.length === 0` → "0 steps" secondary text — different label text, not the same placeholder); `:278-283` (`renderPlanSection`: `null` → `""` (no plan section at all); `{steps: []}` → explicit "0 steps" line); `test/rsb_tests/test_model.py:196-217` (`test_dashboard_js_empty_plan_is_distinct_from_null_plan`, asserts `buildPlanSteps` returns `{"steps": []}` vs `None`) | Both the table-cell and detail-panel rendering paths use visibly different text/structure for the two cases, and the underlying data shape is test-covered up to `buildPlanSteps`; the final string differences (`planCellLabel`/`renderPlanSection` outputs) are confirmed by code inspection only, since neither function is in `module.exports` |
| R6b: the distinct-treatment decision recorded in a durable location, separate from the rendering fact | Present | `src/rsb/web/dashboard.js:148-155` (comment above `planCellLabel`); `:246-251` (comment above `buildPlanSteps` return-shape doc); `src/rsb/model.py:166-168` (comment above the `plan=` extraction) | Three separate source-level comments document the decision, independent of the rendering code itself |

## R7 — implementation conforms to schema §2.2's `plan` contract

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R7a: `PlanStep`/`Flow.plan` shapes match §2.2's `array<{step:int, roles:[string], done:bool}> \| null` | Present | `src/rsb/model.py:32-36` (`PlanStep(step, roles, done)`); `:46` (`Flow.plan: object`) | `PlanStep`'s three fields match the element shape exactly; `Flow.plan` is typed loosely (`object`, matching this dataclass's existing convention for other union-typed fields like `stage`) but holds either `None` or a `list[PlanStep]` at runtime, matching the union |
| R7b: `normalize_payload()` preserves `null` vs `[]` as distinct values | Present | `src/rsb/model.py:190-197` (`plan=(... if fl.get("plan") is not None else None)`); `test/rsb_tests/test_model.py:112-119` (`test_normalize_plan_explicit_null_is_none`, `test_normalize_plan_empty_list_stays_distinct_from_null`) | Automated test confirms both branches independently |
| R7c: missing-`plan`-key case (schema §2.2 silent) handled by an explicit, stated repo-local policy, not an unstated fallthrough | Present | `src/rsb/model.py:163-189` (27-line comment stating the policy: absent key ≡ explicit `null` ≡ `None`, never `[]`, with rationale for rejecting a `.get("plan", [])` alternative); `test/rsb_tests/test_model.py:100-109` (`test_normalize_plan_missing_key_is_treated_as_none`, uses `WORKED_EXAMPLE` whose flow predates the `plan` field entirely) | Both the policy statement and its regression test target the exact silent-in-spec case; recorded here as a stated *extension* of §2.2, not scored as either a schema pass or violation, per the proposal's framing |

## Open findings

None. All 19 sub-requirements (R1a-R7c) verdict Present, except R3b
(Unverifiable-within-this-repo — provider-side timing claim, no local
means to observe, not scored as a failure). No Surface/Absent/Incorrect
row exists, so `review-severity`'s `severity-classification` is not
invoked (its own trigger condition is non-Present findings, none of
which survived here).

**Open-finding resolution path / next-steps:**

- No Surface/Absent/Incorrect finding exists, so there is no `src/`/
  `test/` follow-up issue to file — nothing to hand off.
- R3b (Unverifiable-within-this-repo): no resolution action, by design —
  the provider-side "appears as soon as the issue is created" timing
  claim is `on-the-record`'s (`flows --json` producer's) behavior, not
  `rsb`'s, and this repo has no fixture or live upstream checkout to
  drive it. Left as a standing scope boundary for any future review with
  access to a live `on-the-record`/`spawn.py` environment, not a task
  for this repo to pick up.
- This record is this role's terminal phase-2 deliverable for issue #23
  per contract v3 s19; next step is the human PR-merge decision on
  PR #25 (acceptance) or a requested revision on the same branch
  (feedback) — no further iteration is planned by this role absent
  either.

## Scope notes

- `src/rsb/render.py` (CLI text renderer) plan output, new JS test
  harness/framework, and accessibility were out of scope for this
  review, per the approved proposal (matching the approved
  implementation proposal's own out-of-scope calls) — not evaluated
  above.
- PR #24's own second-round cross-review (4 findings) was not
  re-litigated as a separate pass; its fixes are the subject of R2a,
  R4b, R5b, R6a-b, R7c above and were independently re-derived from the
  current code/spec, not carried over from `implementation.md`'s
  self-report.
- Per contract, this record reports verdicts only; no `src/`/`test/`
  change is made by this role. There is nothing to hand off to a
  follow-up issue — no non-Present finding exists.
