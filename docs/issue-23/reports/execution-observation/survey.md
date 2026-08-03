# Current-state survey — execution-observation (issue #23)

Scope statement: this is the execution-observation role, current session,
observing issue #23 ("flows[].plan 실행 계획을 대시보드에 렌더링 + \"N flows
in progress\" 집계 결함 수정"), specifically PR #24 ("issue-23 phase 1+2:
flows[].plan rendering + summary aggregation fix"). Read this session to
arrive at this scope: `gh issue view 23 --json title,body,state,comments`,
`gh pr view 24 --json number,title,state,mergedAt,commits,reviews,comments,baseRefName,headRefName,mergeCommit`,
`git log --oneline -20 --all --graph`, `git show --stat` on all three of
PR #24's commits, and full `git show`/diff of every changed file in the
phase-2 commit.

## What exists already

- Issue #23: **CLOSED**. Body specifies the `flows[].plan` field contract
  (type, parsing rule, `null` vs `[]` distinction, plan-only-issue
  behavior — all "배경" facts sourced from on-the-record #189/#197) and 6
  acceptance-criteria checkboxes. Its own "## 실행 계획" block names step 1
  (implementation) and step 2 (`execution-observation ‖ conformance-review`,
  parallel). One issue-level comment exists:
  `APPROVE issue-23/implementation` (jjongkwann, 2026-08-02T16:40:03Z),
  conditional on PR #24's second-round cross-review findings landing in
  phase 2. **No `APPROVE issue-23/execution-observation` comment exists on
  the issue, and PR #24 carries no formal GitHub review (`reviews: []`) —
  approval for issue-23/implementation ≠ approval for this role.**
- PR #24: `issue-23/implementation` → `main`, **MERGED**
  (`mergedAt: 2026-08-03T00:31:16Z`, merge commit `4ea2e48b4184fbd11a5981c977993cdd25a17715`,
  now `HEAD` of `main` and of this branch). Three commits:
  - `99c050f4db3e550ea09ff19077a5b1d6250ba996` — phase 1 (survey + scout
    brief + proposal only; `git show --stat` confirms zero `src/`/`test/`
    touched, 3 files under `docs/issue-23/` only).
  - `a858b80a3a61bfac35e1be6d888c7256bf1eacad` — phase 2 implementation
    (6 files: `docs/issue-23/reports/implementation.md`,
    `docs/specs/flows-schema.md`, `src/rsb/model.py`,
    `src/rsb/web/dashboard.js`, `test/rsb_tests/fixtures.py`,
    `test/rsb_tests/test_model.py`), committed 2026-08-02T16:58:41Z —
    **after** the 16:40:03Z approval comment.
  - `d71cb8547b20e4f3a5ee1fe9e9e5cdca84445929` — same-day follow-up filling
    in the phase-2 record's self-check commit-SHA references.
  - One PR-level comment: "2차 교차 검토(Codex) 결과 반영" (jjongkwann,
    2026-08-02T16:38:27Z, i.e. **before** the issue-level approval
    comment and **before** the phase-2 commit) — 4 numbered findings.
- `docs/issue-23/reports/implementation.md` (the observed role's own
  phase-2 record, read in full this session): `loop_state: landed`,
  claims all 4 cross-review findings addressed, cites its own upstream
  basis, states 41/41 tests passed, and includes a self-check section
  re-verifying each finding against commit `a858b80`.
- This role's own tree (`docs/issue-23/reports/execution-observation/`,
  `docs/issue-23/proposals/execution-observation.md`): **does not exist
  yet** — this is this role's first phase-1 pass for issue #23.

## What was independently read and diffed this session (not taken on the
implementation record's word)

- `src/rsb/model.py` full diff (`git show a858b80 -- src/rsb/model.py`):
  `PlanStep` dataclass, `Flow.plan: object` field, and the
  `normalize_payload()` extraction line
  `plan=([PlanStep(...) for st in fl["plan"]] if fl.get("plan") is not None else None)`.
  Traced by hand against all three cases (`plan` key absent, `plan: null`,
  `plan: []`, `plan: [...]`) — the code's actual branching, not the
  record's prose description of it.
- `src/rsb/web/dashboard.js` full diff: `isFlowInProgress()`,
  `selectSummary()`'s new `flows` chip expression, `planCellLabel()`,
  `buildPlanSteps()`, `renderPlanSection()`, and the
  `renderDetailPanel()`/`renderData()`/`module.exports` wiring.
- `docs/specs/flows-schema.md` diff — compared its new `plan` row and
  worked-example addition word-for-word against issue #23's body text.
- `test/rsb_tests/fixtures.py` and `test/rsb_tests/test_model.py` diffs —
  read every new fixture and every new assertion, not just the test
  names.
- `src/rsb/model.py`'s pre-existing `Session.last_activity: object` field
  (grep), to check the record's claim that `plan: object` "mirrors"
  an existing convention rather than being made up.
- Prior, directly comparable in-repo precedent: `docs/issue-4/reports/execution-observation.md`
  and `docs/issue-4/proposals/execution-observation.md` (this exact role,
  earlier issue) — read in full to calibrate record structure/rigor and
  to check what verification method that pass actually used.

## Gaps / unknowns this proposal must resolve

1. **Method conflict.** Issue-4's execution-observation precedent
   re-ran `pytest` and drove a live `webserver.run_server()` instance with
   real HTTP requests. This session's role directive prohibits that
   outright ("never re-run the observed role's code... the only
   admissible evidence [is] diff, commits, its own record"). The proposal
   must state the substitute method plainly, not silently drop rigor.
2. **Sandbox execution ability is untested this session** — no attempt to
   run `node`/`pytest` has been made (correctly, per the prohibition
   above), so there is no environment-capability gap to report here, only
   a methodology decision.
3. **Approval path.** No `APPROVE issue-23/execution-observation` exists
   yet (single-account mode, per approvers.md: `JiwonJung94`,
   `jjongkwann`). Phase 2 cannot start in this session.
4. **Six acceptance criteria** in the issue body need explicit
   per-criterion evidence pointers in phase 2, not just a global "looks
   done" — including the one (plan-only issue appearing in `flows[]`
   immediately) that is largely an upstream/on-the-record contract rather
   than something `dashboard.js` implements new code for; the proposal
   must state how that criterion will be checked given this repo cannot
   independently drive the upstream provider.
5. **Trajectory-level evidence** (did phase 1 survey/scout before
   proposing, did phase 2 wait for real approval) is already visible from
   commit timestamps and `git show --stat` (see "What exists already"
   above) but needs to be checked against the *actual* survey/scout-brief/
   proposal file contents, not just their existence, before any trajectory
   verdict is written in phase 2.
