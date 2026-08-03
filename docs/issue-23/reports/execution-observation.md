# Execution-observation record (issue #23)

code_under_review: PR #24 (`issue-23/implementation` → `main`, merged @
`4ea2e48b4184fbd11a5981c977993cdd25a17715`) — `src/rsb/model.py`,
`src/rsb/web/dashboard.js`, `docs/specs/flows-schema.md`,
`test/rsb_tests/fixtures.py`, `test/rsb_tests/test_model.py`.
loop_state: reported

Approved via issue #23 comment `APPROVE issue-23/execution-observation`
(jjongkwann, exact bare string,
https://github.com/tokenmaxxxer/repo-status-board/issues/23#issuecomment-5161191623,
2026-08-03T00:46:36Z), against
`docs/issue-23/proposals/execution-observation.md` (this role's own
approved phase-1 proposal). Executes that proposal's §0-§2 method: static
diff/code-path tracing in place of live re-execution, three-level verdict,
per-acceptance-criterion table, blameless-shaped findings.

## What was done

Read PR #24 (`issue-23/implementation`, merged @ `4ea2e48`) in full —
its 3 commits' diffs (`99c050f`, `a858b80`, `d71cb85`), its cross-review
comment, and its own phase-1/phase-2 records/survey/scout-brief/proposal
— and rendered the three-level verdict this role's contract requires
(outcome/trajectory/step), per the method committed to in this role's own
approved phase-1 proposal (`docs/issue-23/proposals/execution-observation.md`):
static diff/code-path tracing in place of live re-execution, since this
session's role directive prohibits re-running the observed role's code.
Traced `model.py`'s `plan` extraction and `dashboard.js`'s
`buildPlanSteps()`/`planCellLabel()`/`renderPlanSection()`/
`isFlowInProgress()` by hand against every case named in that proposal;
checked all 6 of issue #23's acceptance criteria against specific
file:line evidence; and checked the approval-comment and PR-lifecycle
trail against contract v3's approval-gate and issue-closure rules, which
surfaced the two governance findings (T1, T2) below. No code was written
or changed by this role.

## Independence statement

This role did not author, propose, or edit any part of PR #24
(`issue-23/implementation`) — not its code, its tests, its spec-doc sync,
or its own record (`docs/issue-23/reports/implementation.md`) — in this
session or any prior one. Nothing under PR #24's `src/`, `test/`, or
`docs/issue-23/{proposals,reports}/implementation*` paths was touched by
this role. Everything below is read-only observation of artifacts already
on `main` (commits `99c050f`, `a858b80`, `d71cb85`, merge `4ea2e48`) and
this role's own prior phase-1 commit (`6562fd5`); no command that would
re-run the observed role's code (`pytest`, `node`, `rsb serve`) was
executed this session, per this role's re-execution prohibition.

## Three-level verdict

### 1. Outcome — did PR #24 land what issue #23 asked

| # | Acceptance criterion (issue #23 body) | Evidence | Verdict |
|---|---|---|---|
| 1 | 스펙 사본 §2.2 `plan` 행 + worked example, 원본과 일치 | `docs/specs/flows-schema.md:96` (table row, verbatim type/parsing-rule/null-vs-[] text matches issue #23 body word-for-word), `:82-85` (§2.2 JSON example adds `plan`), `:296-298` (§7 worked example adds `plan`) — all from commit `a858b80` | **Met** |
| 2 | plan 있는 이슈: 스텝 순서·역할·done 상태가 화면에 보임 | `dashboard.js:253-255` `buildPlanSteps()` sorts `flow.plan.slice().sort((a,b) => a.step - b.step)` (ascending, not payload order); `:278-291` `renderPlanSection()` renders each step's number, joined roles, and a done/pending badge; wired into `renderDetailPanel()` at `:317,323` | **Met** |
| 3 | plan-only 이슈(보드 레코드 없음)가 생성 직후 flows에 나타남 | Not independently verifiable from this repo — see "What could not be verified" below | **Not applicable to this repo's write surface** |
| 4 | 스텝별 역할에 loop_state/verdict, 대기 PR이 조인되어 표시 | `dashboard.js:257-266`: `roleStatus` looked up from `flow.roles` by name (loop_state/verdict), `pendingPrs` from `decisions.filter(d => d.issue===issue && d.repo===repo && d.role===roleName)` (all matches, not `.find()`); `model.py:14` confirms `Decision.repo` is populated at normalize time (`repo=repo_name`, `model.py:140`), so the JS-side `.repo` field the join depends on genuinely exists in the merged payload, not just in the test fixtures | **Met** |
| 5 | 요약 칩이 진행 중 flow만 셈 (delivered/closed 제외, 기준 문서화) | `dashboard.js:45` `isFlowInProgress(f) = f.stage_derived === false \|\| ["proposal","approved","implementing"].includes(f.stage)`, used at `:60` in `selectSummary()`; doc comment at `:27-41` states the over-count risk explicitly (policy, not exact count) | **Met** |
| 6 | `plan: null` vs `[]` 렌더링 구분(또는 동일 취급 결정)이 기록됨 | `dashboard.js:156-160` `planCellLabel()`: `—` for null/undefined, distinct `0 steps` for empty; `:253-254,278-282` `buildPlanSteps()`/`renderPlanSection()`: `null` vs `{steps: []}` is a different **return value**, not just a different rendered string (survives past the render layer); `model.py:190-197` normalization keeps `None` and `[]` distinct at the data layer too | **Met** |

5 of 6 criteria are met with direct code citations; criterion 3 sits
outside this repo's testable reach (see below) rather than being unmet.
**Outcome verdict: substantially met.**

### 2. Trajectory — was PR #24's own phase-1→phase-2 path sound

Phase 1 discipline: commit `99c050f` (2026-08-02T16:17:13Z) touched only
3 files under `docs/issue-23/` (`git show --stat 99c050f` — 337
insertions, 0 deletions, no `src/`/`test/`) — survey, scout-brief, and
proposal, no code. Sound.

Cross-review-before-approval ordering: PR-level comment "2차 교차 검토
(Codex) 결과 반영" (jjongkwann,
https://github.com/tokenmaxxxer/repo-status-board/pull/24#issuecomment-5159290973,
2026-08-02T16:38:27Z, 4 numbered findings) landed **before** the
issue-level approval comment (16:40:03Z) and well before the phase-2
commit (16:58:41Z) — the implementation role had the corrective feedback
in hand before writing phase-2 code, and did not write phase-2 code before
either comment existed. Sound.

Approval-gate ordering: phase-2 commit `a858b80` (16:58:41Z) came after
the approval comment (16:40:03Z), not before — contract v3's
approve-then-execute ordering was respected in time. **However**, the
approval comment itself does not satisfy contract v3's single-account-mode
gate — see Finding T1 below, the one substantive trajectory defect found
in this pass.

Scope discipline in the diff itself: no file outside the frozen write set
(`docs/specs/flows-schema.md`, `src/rsb/model.py`,
`src/rsb/web/dashboard.js`, `test/rsb_tests/fixtures.py`,
`test/rsb_tests/test_model.py`) was touched by `a858b80` or `d71cb85`
(confirmed via `gh pr view 24 --json files`); `dashboard.css` — named as a
conditional write-set member in the proposal — has an empty diff, and the
record's claim that existing tokens sufficed is consistent with the
`planCellLabel()`/`renderPlanSection()` code only using pre-existing
`.badge`/`.status-*`/`.text-secondary`/`.mono` classes (`dashboard.js:159-160,289`).
The frozen, already-approved proposal document
(`docs/issue-23/proposals/implementation.md`) was never edited after
approval — the finding-#1 rationale correction went into a `model.py`
comment (`:163-189`) instead, which is the correct place per this
project's convention of not rewriting historical proposal docs. Sound.

**Trajectory verdict: sound overall, with one confirmed governance
defect (T1) in how phase 2 was authorized.**

### 3. Step — which specific artifact, if any, is deficient

Hand-traced (per approved proposal §1) against the specific cases named
there:

- **`plan` key absent** (pre-`plan` legacy payload): `model.py:190-197`
  — ternary condition is `fl.get("plan") is not None`; for an absent key,
  `dict.get(key)` (no default arg) returns `None` implicitly, condition
  is `False`, so the `else` branch (`None`) is selected — Python does not
  evaluate the `for st in fl["plan"]` comprehension in the untaken branch,
  so no `KeyError` risk despite the direct `fl["plan"]` indexing in the
  taken-only branch. Traced correct.
- **`plan: null`**: same ternary, `fl.get("plan")` returns the explicit
  `None` value itself (not a substituted default, since `.get(key, default)`'s
  default only ever fires on a missing key) → `None`. Traced correct,
  and the `model.py:163-189` comment states this exact mechanism.
- **`plan: []`**: `fl.get("plan")` returns `[]`, `[] is not None` is
  `True`, comprehension over an empty list yields `[]` → `Flow.plan == []`,
  distinct from `None`. Traced correct.
- **Populated multi-step plan with parallel roles**: each step dict's
  `step`/`roles`/`done` keys are read directly into `PlanStep(...)`
  (`model.py:192`) — no reordering or dedup at this layer; ordering is a
  JS-side (`buildPlanSteps`) concern, correctly separated.
- **`buildPlanSteps()` step-sort**: `flow.plan.slice().sort((a,b) => a.step - b.step)`
  (`dashboard.js:255`) — `.slice()` before `.sort()` avoids mutating the
  input array in place, which matters because the same `flow` object is
  also read by `flowRows()`/`planCellLabel()` for the table cell; sorting
  in place would have been a latent order-dependency bug between the two
  call sites. Not present — traced correct.
- **Multi-PR join** (`decisions.filter(...)`, `dashboard.js:262-265`):
  filters on `(issue, repo, role)`, returns every match. Traced correct;
  also independently corroborated by test `PLAN_STEPS_PAYLOAD` fixture
  carrying two PRs (#501, #502) against the same `(issue, repo, role)`
  (`fixtures.py`, `a858b80` diff) and the corresponding test asserting
  both come back (`test_model.py`, same commit).
- **Summary-chip aggregation** (`isFlowInProgress`, `dashboard.js:45`):
  hand-traced against the 5-flow case in
  `test_dashboard_js_select_summary_counts_in_progress_and_raw_unmapped_flows`'s
  fixture (proposal/approved/delivered/closed/unmapped) — `proposal` and
  `approved` match the stage-list branch, `unmapped` (`stage_derived:
  false`) matches the OR-branch regardless of its stage string, `delivered`
  and `closed` match neither branch → count of 3, matching the test's
  asserted `"3 flows in progress"`. Traced correct.

**No step-level code defect found** in the cases this proposal committed
to tracing. This is a stronger, hand-verified claim than the
implementation record's own self-check section, which re-read its own
diff rather than being traced by a role that did not write it.

Test-file reading (corroboration, not proof, per proposal §1.2): the 8
new test function names in `test/rsb_tests/test_model.py` (`a858b80`
diff) were counted directly (`test_normalize_plan_missing_key_is_treated_as_none`,
`test_normalize_plan_explicit_null_is_none`,
`test_normalize_plan_empty_list_stays_distinct_from_null`,
`test_normalize_plan_steps_with_parallel_roles`,
`test_dashboard_js_plan_steps_sorted_by_step_number_ascending`,
`test_dashboard_js_plan_steps_join_shows_all_pending_prs_not_just_first`,
`test_dashboard_js_empty_plan_is_distinct_from_null_plan`,
`test_dashboard_js_select_summary_counts_in_progress_and_raw_unmapped_flows`)
and each asserts on the specific behavior its name claims, not a weaker
proxy (e.g. the empty-vs-null test asserts on `buildPlanSteps()`'s
**return value** `{steps: []}` vs `None`, not on a rendered HTML string).
The record's "41 passed (33 pre-existing + 8 new)" and "`node` v26.5.1
present, all 4 ran (not skipped)" claims are **reported as claimed, not
independently reproduced** — this session ran no `pytest`/`node`
invocation, per the re-execution prohibition.

## Findings

**T1 (trajectory, governance/process — the approval comment that gated
PR #24's phase 2 does not satisfy contract v3's single-account-mode
string-equality gate).**

- **Impact**: PR #24's phase-2 code (the entire `src/`/`test/` diff this
  record evaluates) was authorized to proceed on an issue-comment whose
  body is not the exact string `APPROVE issue-23/implementation` — it is
  that string followed by `"\n\n조건부 승인 — PR #24 리뷰 코멘트(2차 교차
  검토 4건)를 phase 2에서 반영할 것."` Per this role's own governing
  contract text ("String equality only, never prose interpretation: any
  other comment ... is feedback, not approval"), this comment is, by the
  letter of that rule, feedback rather than a valid approval — meaning
  PR #24's phase 2 lacks a contract-conforming authorization event, even
  though the delivered code substantively satisfies the condition the
  comment states.
- **Timeline**: comment posted 2026-08-02T16:40:03Z
  (https://github.com/tokenmaxxxer/repo-status-board/issues/23#issuecomment-5159299982);
  phase-2 commit `a858b80` followed 18 minutes later (16:58:41Z), treating
  the comment as sufficient authorization to begin.
- **Root cause**: the comment interleaves the required bare-approval
  token with additional conditional prose in the same body, rather than
  posting the token alone (with the condition left in the separate,
  already-existing cross-review comment,
  https://github.com/tokenmaxxxer/repo-status-board/pull/24#issuecomment-5159290973,
  posted 2 minutes earlier). This is not a one-off slip: issue #20's
  `APPROVE issue-20/finance-unit-economics` comment (2026-08-01T10:30:31Z)
  shows the identical shape — bare token on line 1, approver feedback
  appended in the same comment body — and that role's own phase-2 record
  (`docs/issue-20/reports/finance-unit-economics.md`) also treated it as
  valid approval without flagging the format. Both observed cases where a
  condition needed to accompany an approval used this same non-conforming
  shape, suggesting the strict string-equality rule and this approver's
  actual practice for *conditional* approvals are in tension project-wide,
  not specific to PR #24. (This citation is offered as corroborating
  context only — this record renders no verdict on issue #20's own
  trajectory, which is outside this role's write surface for issue #23.)
- **Action item**: when a single-account-mode approval needs to carry a
  condition, post the bare `APPROVE issue-<n>/<role>` token as its own,
  standalone comment, and put any condition/feedback in a separate
  comment (the cross-review comment on PR #24 already demonstrates the
  right shape for the feedback half) — this keeps the approval gate
  mechanically string-checkable without relying on trailing-prose
  interpretation.

**T2 (trajectory, process — PR #24's body included a GitHub auto-close
keyword for issue #23 despite the issue's own declared plan having a
second, not-yet-done step).**

- **Impact**: issue #23 was auto-closed by GitHub the moment PR #24
  merged, even though issue #23's own body names a 2-step
  `## 실행 계획` (`step 1 implementation`, `step 2 execution-observation
  ‖ conformance-review`) and PR #24 only completes step 1. A human had to
  notice the premature closure and manually reopen the issue before the
  parallel step-2 roles (this one included) could be observed as still
  active against an open issue.
- **Timeline**: PR #24 body contains `"Closes #23."`
  (`gh pr view 24 --json body`); issue auto-closed at merge,
  2026-08-03T00:31:16Z (merge commit `4ea2e48`); reopened by jjongkwann's
  comment 14 minutes later
  (https://github.com/tokenmaxxxer/repo-status-board/issues/23#issuecomment-5161185557,
  00:45:18Z): "재오픈 — PR #24 본문의 'Closes #23' 키워드로 머지 시 자동
  종료됐으나, 실행 계획 step 2(execution-observation ‖
  conformance-review)가 진행 중."
- **Root cause**: PR #24's body carries a GitHub auto-close keyword
  referencing the parent multi-step issue, even though the PR itself only
  completes one of that issue's two declared plan steps — the keyword
  choice didn't account for the issue's own `## 실행 계획` block being
  the source of truth for when the issue is actually done.
- **Action item**: when an issue's body declares a multi-step
  `## 실행 계획`, a PR completing only one step should not carry a
  `Closes #<n>` / `Fixes #<n>` / `Resolves #<n>` keyword for the parent
  issue; the issue should close manually once every declared step reports
  complete.

Both findings are process/governance defects in how PR #24 was gated and
closed, not defects in the delivered `plan`-rendering/aggregation code
itself (see Step verdict above — no code defect found there). Per this
role's prohibition on editing the observed role's `src/`/`test/`/record,
neither is fixed here; both are handed off as findings on this record for
the human to judge.

## What could not be verified

- **Acceptance criterion 3** (plan-only issue appears in `flows[]`
  immediately on creation) depends on the upstream `on-the-record`
  provider's `spawn.py flows --json` actually emitting a `flows[]` entry
  for such an issue — this checkout has no local `on-the-record`
  instance to drive, and this repo's own code does not filter or drop
  such entries (`normalize_payload()` processes every object in
  `payload.get("flows", [])` unconditionally, `model.py:280`), so `rsb`
  is *compatible with* but cannot *independently confirm* this criterion.
  Flagged as an assumption on the implementation side, not verified here.
- **"41 passed (33 pre-existing + 8 new)" and the `node`-subprocess test
  run** are reported as claimed by `docs/issue-23/reports/implementation.md`,
  not independently reproduced — this session ran no `pytest` or `node`
  invocation, per the prohibition on re-running the observed role's code.
  The 8 new test names and their assertions were read and traced instead
  (see Step verdict).
- **Live rendering** (opening `dashboard.js` in an actual browser or
  driving `rsb serve`) was not attempted, for the same reason — this
  pass substitutes hand-traced code-path tracing per the approved
  proposal's stated method change from issue-4's precedent pass.
- Re-judging `conformance-review`'s parallel step-2 work on issue #23 is
  out of this role's write surface (separate role, separate branch/PR)
  and is not attempted here.

## Upstream basis

- `docs/issue-23/proposals/execution-observation.md` (this role's own
  approved phase-1 proposal) — method and record-format commitments this
  record executes.
- `docs/issue-23/reports/execution-observation/survey.md`,
  `scout-brief.md` (this role's own phase-1 research).
- PR #24 (`gh pr view 24 --json ...`), its 3 commits (`99c050f`,
  `a858b80`, `d71cb85`), its cross-review comment, and its diffs
  (`git show <sha> -- <path>`) — all read in full this session.
- `docs/issue-23/reports/implementation.md`,
  `docs/issue-23/reports/implementation/survey.md`, `scout-brief.md`,
  `docs/issue-23/proposals/implementation.md` — the observed role's own
  phase-1 and phase-2 artifacts, read in full this session (not merely
  confirmed to exist).
- Issue #23 (`gh issue view 23 --json ...`), all 4 of its comments, read
  in full this session.

## Open findings

T1 and T2 above are both open — process/governance findings handed off
on this record, not fixed by this role (per its prohibition on editing
the observed role's `src/`/`test/`/record) and not yet acted on by a
human. No step-level (code) defect is open; the Step verdict above found
none in the cases this role's approved proposal committed to tracing.

## Open-finding resolution path

This role cannot file issues (contract v3: issues are user-authored
only) and cannot edit PR #24 or `docs/issue-23/reports/implementation.md`
(independence requirement). Resolution of T1/T2 is therefore entirely in
the human approver's hands, via this record's own PR (#26):

- **Reviewing**: the approver reads T1/T2 on this record (PR #26) and
  judges whether each is a real defect worth acting on, a documented
  project-practice exception (e.g. that conditional single-account
  approvals in the bare-token-plus-prose shape are intentionally
  tolerated, given the issue #20 precedent cited in T1), or something in
  between.
- **If accepted as defects**: the approver — the only party who can file
  an issue under this contract — opens a new issue for whichever of T1
  (approval-comment format) / T2 (auto-close-keyword-vs-multi-step-plan)
  they want addressed, e.g. as a documentation/process fix to
  `docs/specs/approvers.md` or the role-handoff contract text itself, or
  as guidance for future `Closes #<n>` usage on multi-step issues. No
  code or doc under `src/`/`test/`/`docs/issue-23/` needs to change to
  act on either finding — both are about how future approval comments
  and PR bodies are written, not about the delivered `plan`-rendering
  feature.
- **If not accepted**: no further action; this record stands as the
  documented observation, and this role's phase 2 is complete
  (`loop_state: reported`) regardless of that decision.
- **Merge/close of PR #26** is itself the human decision this record
  waits on next, per contract v3 (PR merge = acceptance of the delivered
  observation work).

## Next steps

None from this role beyond this record and the resolution path above —
`loop_state: reported` is terminal for this role's own work on issue #23.
