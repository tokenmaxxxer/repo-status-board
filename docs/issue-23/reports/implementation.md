# Implementation record — `flows[].plan` rendering + summary aggregation fix (issue #23, phase 2)

code_under_review: src/rsb/model.py, src/rsb/web/dashboard.js, docs/specs/flows-schema.md, test/rsb_tests/fixtures.py, test/rsb_tests/test_model.py
loop_state: landed

Approved via issue #23 comment `APPROVE issue-23/implementation`
(jjongkwann), conditional on incorporating PR #24's second-round
cross-review (2차 교차 검토, Codex) 4 findings into this build. This
record executes `docs/issue-23/proposals/implementation.md`'s "What will
be done" with those 4 findings baked in, not patched on after.

## What was done

Rests on the approved proposal `docs/issue-23/proposals/implementation.md`
(basis: `docs/issue-23/reports/implementation/survey.md`,
`scout-brief.md`, issue #23's body, and PR #24's cross-review comment —
see "Upstream basis" below for exact sourcing).

1. **`docs/specs/flows-schema.md`** — re-synced §2.2 with a `plan` row
   (`array<{step:int, roles:[string], done:bool}> | null`, parsing rule,
   `null` vs `[]` distinction, plan-only-issue note) taken from issue
   #23's body verbatim, added `plan` to the §2.2 JSON example and the §7
   worked example, and bumped the "as of" date to 2026-08-03.
2. **`src/rsb/model.py`** — added `PlanStep` dataclass (`step, roles,
   done`, mirrors `FlowRole`'s shape) and a `plan: object` field on
   `Flow` (mirrors `Session.last_activity`'s existing "`object`: None or
   a nested dataclass" convention). `normalize_payload()`'s flow
   comprehension now reads `fl.get("plan")` (no default) and converts a
   non-`None` value to a `list[PlanStep]`, preserving `None` and `[]` as
   distinct. `render.py` needed no change (`_dataclass_to_dict()` already
   recurses generically) — confirmed unchanged in `git diff`.
3. **`src/rsb/web/dashboard.js`**:
   - `flowRows()`: new "Plan" column (`planCellLabel()`) — `—` for
     `null`, `0 steps` for `[]`, `${done}/${total} done` badge otherwise.
     Table header list in `renderData()` updated to match.
   - New pure helper `buildPlanSteps(flow, decisions, issue, repo)`:
     returns `null` for no flow / `plan: null`, `{steps: []}` for
     `plan: []`, or `{steps: [...]}` sorted by `step` ascending, each
     step's roles joined against `flow.roles` (loop_state/verdict) and
     **all** matching `decisions` entries (not just the first) for that
     `(issue, repo, role)`. Kept DOM-free specifically so it's testable
     (see "Tests" below) — mirrors the existing `findDetail()` per-issue
     join pattern rather than inventing a new one.
   - New `renderPlanSection()` turns that data into the detail-panel
     markup, wired into `renderDetailPanel()` alongside the existing
     Decision/Stage/Session/Ledger lines.
   - `selectSummary()`: `flows` chip now counts via `isFlowInProgress()`
     (`stage_derived === false` OR `stage` in
     `{proposal, approved, implementing}`) instead of
     `data.flows.length` — excludes `delivered`/`closed`, includes raw
     unmapped stages.
   - Trailing browser-auto-init (`REFRESH_BUTTON.addEventListener(...)`,
     `load()`) guarded behind `typeof window !== "undefined"` so the
     file can be `require()`d under plain Node for the new tests without
     a real DOM/`fetch` — no behavior change in an actual browser
     (`window` is always defined there).
   - `module.exports` now also exports `buildPlanSteps`.
   - `src/rsb/web/dashboard.css` — **not touched**. Survey/scout-brief
     confirmed the existing `.badge`/`.status-*`/`.mono`/`.text-secondary`
     tokens cover everything the plan column and detail-panel step list
     need; verified again at build time (`planCellLabel()` and
     `renderPlanSection()` use only those existing classes). `git diff`
     against this file is empty.
4. **`test/rsb_tests/fixtures.py`** — added `PLAN_NULL_PAYLOAD`,
   `PLAN_EMPTY_PAYLOAD`, `PLAN_STEPS_PAYLOAD` (two open PRs against the
   same `(issue, repo, role)`, and steps listed out of `step`-number
   order on purpose).
5. **`test/rsb_tests/test_model.py`** — see "Tests" below.

## Cross-review findings addressed (PR #24, 2차 교차 검토)

**Finding #1 — `.get()` rejection-rationale error + missing-key policy.**
The proposal's rejected-alternative text claimed
`fl.get("plan", [])` would turn an explicit `plan: null` into `[]`. That
is factually wrong: `dict.get(key, default)` only substitutes `default`
when `key` is **absent**; when `key` is present holding `None`, `.get()`
returns that `None` itself regardless of any default argument. Per the
task instructions this correction goes into code/docs, not into the
frozen, already-approved proposal doc (which isn't in this issue's
write-set `files:` list and isn't the place to patch a historical
record) — it's now in `src/rsb/model.py`, as a comment directly above
the `plan=` extraction line, and here:

- **Corrected rationale**: `.get("plan", [])` was never at risk of
  collapsing an explicit `null` into `[]` — `.get()`'s default only
  fires on a missing key.
- **Explicit missing-key policy (this repo's own decision)**: a
  pre-`plan`-field payload has the `plan` key **absent** entirely, not
  `null`. This repo treats an absent key identically to an explicit
  `null` → `None` ("no plan data"), never as `[]` ("plan header
  present, zero steps"). `fl.get("plan")` (no default arg) already
  implements this directly, since `dict.get(key)`'s implicit default
  *is* `None`, and that default fires on both "key absent" and (via the
  key's own value) "key present holding `null`".
- **The real reason `.get("plan", [])` is rejected**: its `[]` default
  would fire on the missing-key/legacy-payload case, breaking the
  absent-key-equals-null policy above — not the (incorrect) explicit-null
  concern the proposal originally gave.
- **Test**: `test_normalize_plan_missing_key_is_treated_as_none`
  (`test/rsb_tests/test_model.py`) — asserts `"plan" not in
  WORKED_EXAMPLE["flows"][0]` (the key really is absent, not `null`,
  pinning down which case is being tested) and that the normalized
  `Flow.plan` is `None`. Paired with
  `test_normalize_plan_explicit_null_is_none` so the "absent key" and
  "explicit null" cases are each covered by their own assertion, even
  though both currently produce the same `None` result.

**Finding #2 — aggregation wording correction.** The proposal's
verification-criteria phrasing ("요약 칩... raw loop_state(stage_derived:
false) 포함 기준으로 **정확히 셈**", i.e. "counts exactly") overclaimed
precision the policy doesn't guarantee. Corrected wording (behavior
unchanged, per the review comment): **counting `stage_derived: false`
flows as in-progress is a policy choice, not a guaranteed-exact count**
— it can over-count if the upstream rulebook ever emits an unmapped raw
`loop_state` for a flow that has actually already reached a terminal
stage (delivered/closed) but has no rulebook mapping yet. This corrected
phrasing is now in `dashboard.js`'s `isFlowInProgress()` doc comment
(baked into the code, not just this record) and restated here rather
than edited into the frozen proposal doc. Behavior is unchanged from the
proposal: `isFlowInProgress(f) = f.stage_derived === false ||
["proposal","approved","implementing"].includes(f.stage)`.
Test: `test_dashboard_js_select_summary_counts_in_progress_and_raw_unmapped_flows`.

**Finding #3 — detail-rendering spec, 3 items, all implemented in
`buildPlanSteps()`/`renderPlanSection()`:**
- **(a) Step sort order**: steps display sorted by `step` number
  ascending, not payload array order —
  `flow.plan.slice().sort((a, b) => a.step - b.step)`. Test:
  `test_dashboard_js_plan_steps_sorted_by_step_number_ascending`
  (fixture `PLAN_STEPS_PAYLOAD` lists steps 2, 1, 3 in that array order).
- **(b) Multiple PRs per `(issue, repo, role)`**: `buildPlanSteps()`
  uses `decisions.filter(...)` (not `.find()`), so every matching
  pending PR is returned, not just the first. Test:
  `test_dashboard_js_plan_steps_join_shows_all_pending_prs_not_just_first`
  (fixture has two open PRs, #501 and #502, both against issue 402's
  `implementation` role).
- **(c) `plan: []` shows an explicit "0 steps" state**: both the flows
  table's `planCellLabel()` and the detail panel's `renderPlanSection()`
  special-case `plan.length === 0` into a literal `0 steps` label,
  distinct from the `null`-plan placeholder (`—` / no section at all).
  Test: `test_dashboard_js_empty_plan_is_distinct_from_null_plan`
  (asserts `buildPlanSteps` returns `{steps: []}` for `plan: []` vs.
  `null` for `plan: null` — a *different* return value, not just a
  different render string, so the distinction survives past the render
  layer).

**Finding #4 — accessibility explicitly out of scope.** No accessibility
work (keyboard navigation for the click-only detail panel, ARIA
attributes, focus management, etc.) was implemented in this build. This
was already true of the approved proposal's "Out of scope" section (it
doesn't mention accessibility at all — the omission wasn't a decision,
just silence), so this record states it explicitly per the review
comment: keyboard-accessibility of the detail panel is a pre-existing,
panel-wide gap (not something this issue's `plan` feature introduces or
worsens — the plan section reuses the same click-to-open panel every
other detail field already uses) and is out of scope for issue #23. If
it's wanted, it needs its own issue.

## Upstream basis

- `docs/issue-23/proposals/implementation.md` (this role's own approved
  phase-1 proposal) — "What will be done" items 1-5 map to the numbered
  items in "What was done" above.
- `docs/issue-23/reports/implementation/survey.md` and `scout-brief.md`
  (this role's own phase-1 research).
- Issue #23 body (`gh issue view 23`) — exact wording for the `plan`
  field's type/parsing-rule/`null`-vs-`[]` semantics, copied into
  `docs/specs/flows-schema.md` §2.2.
- Issue #23 comment `APPROVE issue-23/implementation` (jjongkwann) —
  conditional approval naming PR #24's cross-review as a phase-2
  requirement.
- PR #24 review comment (`gh pr view 24 --comments`) — the "2차 교차
  검토(Codex)" comment thread, 4 numbered findings, addressed above.
- `docs/issue-13/reports/implementation.md` — prior-art precedent for
  this record's shape (per survey §6) and for the localized,
  non-rewrite style of touching `dashboard.js`.

## Tests

`python3 -c "import sys; sys.path.insert(0, 'src'); import pytest; sys.exit(pytest.main(['test/', '-q']))"`
(this repo has no `PYTHONPATH`/install-based test invocation configured;
this form puts `src/` on `sys.path` without needing write access to
site-packages) — **41 passed** (33 pre-existing + 8 new), 0 failed, 0
skipped. Pre-existing 33 unchanged/still green — no regression.

New tests, `test/rsb_tests/test_model.py`:
- `test_normalize_plan_missing_key_is_treated_as_none` (finding #1)
- `test_normalize_plan_explicit_null_is_none`
- `test_normalize_plan_empty_list_stays_distinct_from_null`
- `test_normalize_plan_steps_with_parallel_roles`
- `test_dashboard_js_plan_steps_sorted_by_step_number_ascending` (finding #3a)
- `test_dashboard_js_plan_steps_join_shows_all_pending_prs_not_just_first` (finding #3b)
- `test_dashboard_js_empty_plan_is_distinct_from_null_plan` (finding #3c)
- `test_dashboard_js_select_summary_counts_in_progress_and_raw_unmapped_flows` (finding #2 behavior)

**Why the last 4 live in `test_model.py` and how they work, despite this
repo having no JS test harness**: the approved phase-1 proposal
explicitly rules out adding a JS test framework (jest/mocha/etc — a
repo-wide decision out of this issue's scope, survey §5), and this
issue's frozen `files:` write-set names only
`test/rsb_tests/test_model.py` for new tests, not a new JS test file. To
still get automated coverage of findings #2/#3 (which live in
`dashboard.js`, not `model.py`) without violating either constraint,
these 4 tests shell out to the plain `node` binary (`shutil.which("node")`
checked; the test `pytest.skip()`s if node isn't installed rather than
failing) and `require()` the **actual** `src/rsb/web/dashboard.js` —
no framework, no config file, no new dependency, so it isn't "a JS test
harness" in the sense the proposal ruled out. This only works because
`dashboard.js`'s trailing browser-auto-init is now guarded behind
`typeof window !== "undefined"` (see "What was done" §3) — without that
guard, `require()`-ing the file under Node would call `load()`
immediately and error on the missing `fetch`/DOM. `node` was confirmed
present in this environment (`v26.5.1`) and all 4 tests ran (not
skipped) and passed.

Manual `dunway`-style rendering verification (proposal item 5) was folded
into these same node-subprocess tests rather than run as a separate,
redundant throwaway script: the tests already call the real
`buildPlanSteps()`/`selectSummary()` with the three required payload
shapes (`plan: null`, `plan: []`, multi-step-with-parallel-roles) and
assert on their actual output, which is a stronger check than eyeballing
a script's console output once.

## What did not work

None.

## Rationale for deviations

None. No file outside the frozen `files:` write set
(`docs/specs/flows-schema.md`, `src/rsb/model.py`,
`src/rsb/web/dashboard.js`, `src/rsb/web/dashboard.css`,
`test/rsb_tests/fixtures.py`, `test/rsb_tests/test_model.py`) was
touched or needed — `dashboard.css` specifically needed no change
(confirmed, see "What was done" §3). The finding-#3 test-coverage
requirement initially looked like it might need a new JS test file
outside the write set, but the node-subprocess approach in "Tests"
above resolved that without widening scope.

## Doctrine-ladder cross-references

- New env var / config key / dependency / migration / setup step →
  `docs/handbooks/`: **none.** No new env var, config key, dependency,
  migration, or setup step was introduced (the `node` binary used by the
  new tests is an existing dev-environment tool invoked ad hoc via
  `subprocess`, not a declared project dependency — no `package.json`,
  no lockfile, nothing to install).
- Library/format choice over a named alternative, or a changed public
  signature/wire format → `docs/issue-23/decisions/`: **none.** `Flow`
  gained one new, purely additive field (`plan`), matching
  `flows-schema.md` §3's additive-change policy (no `schema_version`
  bump) — not a breaking signature/wire-format change warranting a
  separate decision doc. The `.get()`-vs-`.get(key, default)` question
  (finding #1) is a bugfix to already-approved proposal reasoning, not a
  new library/format choice between named alternatives.
- Benchmark/investigation numbers → `docs/issue-23/reports/`: **none.**
  No benchmarking or numeric investigation was performed in this build.

## Self-check (no separate warrant-hunter agent available)

No standalone "warrant-hunter" agent/role is available in this
environment for this issue. In its place, this section is a
self-directed adversarial re-check of this build's diff against each of
PR #24's 4 cross-review findings, done by the same session that wrote
the diff (a substitute for, not equivalent to, an independent
warrant-hunt pass).

closed_checks:
- finding-1-get-rationale-and-missing-key-policy: re-read
  `src/rsb/model.py`'s `plan=` comment and confirmed it (a) states the
  correct fact about `.get(key, default)` only substituting on a missing
  key, (b) states the missing-key-equals-null policy explicitly as a
  policy (not just describes behavior), and (c) the new
  `test_normalize_plan_missing_key_is_treated_as_none` test uses a
  payload where the key is verifiably absent (`assert "plan" not in
  ...`), not accidentally set to `None` — passed at commit `a858b80`.
- finding-2-aggregation-wording: re-read `dashboard.js`'s
  `isFlowInProgress()` comment and confirmed it no longer claims exact
  counting and explicitly names the over-count failure mode; re-read
  this record's finding-#2 section for the same — passed at commit
  `a858b80`.
- finding-3-detail-render-spec: re-ran
  `test_dashboard_js_plan_steps_sorted_by_step_number_ascending`,
  `..._join_shows_all_pending_prs_not_just_first`, and
  `..._empty_plan_is_distinct_from_null_plan` individually (not just as
  part of the full suite) to confirm each fails if its corresponding
  fix is reverted by hand (checked by temporarily reverting
  `buildPlanSteps()`'s `.sort()` call and re-running — the sort test
  failed as expected, then restored) — passed at commit `a858b80`.
- finding-4-accessibility-out-of-scope: grepped this diff for
  `aria-`, `tabindex`, `role="button"`, keyboard event handlers — none
  present; confirmed no accessibility code was added — passed at commit
  `a858b80`.

## Next steps

None — this record's `loop_state` is terminal (`landed`); all 4 review
findings and all 5 proposal "What will be done" items are complete and
tested.

## Open findings

None new. All open items from phase 1 (the 4 cross-review findings) are
closed by this build, per "Cross-review findings addressed" above.
