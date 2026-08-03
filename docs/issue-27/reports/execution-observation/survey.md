# Current-state survey — execution-observation (issue #27)

Scope statement: this is the execution-observation role, current session,
observing issue #27 ("대시보드 순수 원격 배포 — GitHub Actions cron +
Pages, 보드 3개"), specifically PR #28 ("issue-27 phase 1+2: Actions cron
+ Pages deployment", branch `issue-27/implementation` → `main`, **still
open, unmerged**). Read this session to arrive at this scope: `gh issue
view 27 --json title,body,comments`, `gh pr view 28 --json
title,body,url,commits,files,reviews`, `gh pr view 28 --json comments`,
`gh pr list --state all`, `git log --oneline -20 --all --graph`, `git
fetch origin issue-27/implementation` + `git diff --stat main
origin/issue-27/implementation`, `git log main..origin/issue-27/implementation
--oneline`, and full `git show`/diff of every changed file on that
branch.

## What exists already

- Issue #27: **OPEN**. Body specifies 5 numbered requirements (workflow
  cron+dispatch, dashboard static-fetch fix, Pages publish, `runs/`-absence
  verification, fail-safe-on-failure) and 6 acceptance-criteria checkboxes
  (merged 3-repo Pages render; `board.json` refresh per cron tick; empty
  sessions/ledger render cleanly; local `rsb serve` no regression;
  failed-workflow-leaves-prior-deploy confirmed; PR body carries no
  closing-keyword+`#27` pattern, per issue #23 T2 precedent). Its own
  "## 실행 계획" names step 1 (implementation) and step 2
  (`execution-observation ‖ conformance-review`, parallel). One
  issue-level comment exists: `APPROVE issue-27/implementation`
  (jjongkwann, 2026-08-03T05:05:38Z). **No `APPROVE
  issue-27/execution-observation` comment exists on the issue — approval
  for issue-27/implementation ≠ approval for this role.**
- PR #28: `issue-27/implementation` → `main`, **OPEN** (created
  2026-08-03T05:01:14Z, not merged, `reviews: []` — no formal GitHub
  review submitted). Two commits:
  - `f51fc76050110119fc40e8c7d70bad6409cfb3ff` (2026-08-03T05:00:56Z UTC /
    14:00:56+09:00) — phase 1 (survey + scout brief + proposal only;
    `git diff --stat` confirms only `docs/issue-27/` paths touched by this
    branch's phase-1 portion).
  - `c02eee3fe6103764a9fd6bcd5543bc41d503241e` (2026-08-03T05:11:24Z UTC /
    14:11:24+09:00) — phase 2 implementation. `git diff --stat main
    origin/issue-27/implementation` (full branch vs. main): 8 files, +764/-1
    — `.github/boards.ci.toml` (new), `.github/workflows/deploy-board.yml`
    (new), `docs/handbooks/rsb.md` (+22), `docs/issue-27/proposals/
    implementation.md` (new), `docs/issue-27/reports/implementation.md`
    (new), `docs/issue-27/reports/implementation/scout-brief.md` (new),
    `docs/issue-27/reports/implementation/survey.md` (new),
    `src/rsb/web/dashboard.js` (1 line changed).
  - Commit-timestamp ordering: phase-1 commit (05:00:56) → PR opened
    (05:01:14) → issue-level approval comment (05:05:38) → PR feedback
    comment #1 (05:05:39) → phase-2 commit (05:11:24) → PR comment #2
    (05:45:57, **after** the phase-2 commit — see below).
  - PR #28 comment #1 (jjongkwann, 2026-08-03T05:05:39Z): approval-adjacent
    feedback — document GitHub's 60-day scheduled-workflow auto-disable
    and its reactivation method in `docs/handbooks/rsb.md`.
  - PR #28 comment #2 (jjongkwann, 2026-08-03T05:45:57Z): "로컬 프리뷰(정적
    배포 경로 재현) 중 발견 — 이 PR의 결함은 아니지만 배포 결과에 직결" —
    `fetch.py`'s hardcoded 15s timeout + serial collection truncates
    on-the-record's fetch (measured 26.7s) every time; deploying as-is
    would publish a half-broken board. States the fix is split into issue
    #29 and must land **before** PR #28's first live workflow run. Posted
    34 minutes after the phase-2 commit — the implementation record
    (frozen at the phase-2 commit) could not have addressed this and does
    not claim to.
- `docs/issue-27/reports/implementation.md` (the observed role's own
  phase-2 record, read in full this session, via `git show
  origin/issue-27/implementation:docs/issue-27/reports/implementation.md`):
  `code_under_review: f51fc76...`, `loop_state: landed`, states the
  60-day-doc feedback was folded in (not patched on after), lists 4
  numbered "What was done" items mapped 1:1 to the proposal's "What will
  be done", cites a 41/41 test-suite pass, a self-directed "Hunt" section
  with 5 `closed_checks`, and "Open findings: None." Does **not** mention
  PR comment #2 (correctly — it postdates this commit).
- This role's own tree (`docs/issue-27/reports/execution-observation/`,
  `docs/issue-27/proposals/execution-observation.md`): **does not exist
  yet** — this is this role's first phase-1 pass for issue #27.
- Parallel step-2 role `conformance-review`: no `issue-27/conformance-review`
  branch exists yet (`git branch -a` / `git ls-remote` show only
  `issue-27/implementation`, `issue-29/implementation`, `main` for this
  repo) — nothing to cross-reference from that role this session.
- Issue #29 ("parallel fetch + repo filter + accessible tables
  proposal", the fix PR comment #2 points to): **OPEN**, its own PR #30
  (`issue-29/implementation`) also **OPEN**, phase-1-only so far (commit
  `cc3466a`, one commit). Not merged — so PR #28's own not-yet-merged
  state means the "#29 must land before #28's first live run" sequencing
  constraint is not currently violated by anything already on `main`.

## What was independently read and diffed this session (not taken on the
implementation record's word)

- `.github/workflows/deploy-board.yml` (full file, via `git show`):
  triggers (`schedule: */30 * * * *` + `workflow_dispatch`), `permissions`,
  `concurrency: {group: pages, cancel-in-progress: false}`, `build` job
  (3x `actions/checkout` — root + `on-the-record`→`_boards/on-the-record`
  + `tokenmaxxxer-core`→`_boards/tokenmaxxxer-core`, Python 3.11 setup,
  `pip install -e .`, `rsb --config .github/boards.ci.toml --json >
  board.json`, `_site/` assembly, `configure-pages`,
  `upload-pages-artifact`), `deploy` job (`needs: build`,
  `github-pages` environment, `deploy-pages@v4`) — matches the
  implementation record's "What was done" §1 description line for line.
- `.github/boards.ci.toml` (full file): 3 `[[repo]]` blocks, all pointing
  `command` at the single shared `_boards/on-the-record/spawn.py` — matches
  the proposal's frozen TOML block verbatim.
- `src/rsb/web/dashboard.js` diff: exactly one line changed, line 406,
  `fetch("/api/board.json")` → `fetch("api/board.json")` — matches the
  claimed fix, no other lines touched in this file.
- `docs/handbooks/rsb.md` diff: new "## Static deploy (GitHub Pages)"
  section (+22 lines) — describes the workflow, the one-time
  Settings→Pages→Source manual prerequisite, and a 60-day
  auto-disable/reactivation paragraph — confirms PR comment #1's feedback
  was actually folded in, not just claimed.
- `docs/issue-27/proposals/implementation.md`, `docs/issue-27/reports/
  implementation/survey.md`, `docs/issue-27/reports/implementation/
  scout-brief.md` (all read in full via `git show`): proposal's "What
  will be done" §1-4 map 1:1 to the phase-2 record's "What was done" §1-4
  and to the actual diffed files above; survey traces `rsb`'s exit-code
  semantics (§1), config loading (§2), the subprocess error-swallowing
  boundary (§3), local-serve independence (§4), the shared
  `render_json_model` payload path (§5), the absolute-path bug at
  `dashboard.js:406` (§6, matches the diff above exactly), `runs/`-absence
  behavior traced by file:line in a separate on-the-record checkout (§7,
  outside this repo's write set, correctly not modified), dependency
  footprint (§8), and confirms zero pre-existing `.github/` (§9). Scout
  brief: single targeted WebSearch sweep (3 angles, 1 round, sourced)
  against GitHub's own Actions→Pages docs, adopts the two-job
  build/deploy split as the fail-safe mechanism for requirement 5.
- `src/rsb/fetch.py` on this branch (current `main`, unrelated to PR #28's
  write set): confirmed `DEFAULT_TIMEOUT_SECONDS = 15` still present at
  line 12 — grounds PR comment #2's claim in this repo's actual code, not
  just the comment's prose.
- PR #28's body, both comments, and `reviews: []` (`gh pr view 28 --json
  body,comments,reviews`) — read in full, not summarized secondhand.
- Issue #27's body and its one comment (`gh issue view 27 --json
  body,comments`) — read in full.
- Prior, directly comparable in-repo precedent:
  `docs/issue-23/reports/execution-observation/survey.md`,
  `scout-brief.md`, `docs/issue-23/proposals/execution-observation.md`
  (this exact role, prior issue) — read in full to calibrate record
  structure/rigor and to reuse the already-settled re-execution-prohibition
  method rather than re-deriving it.

## Gaps / unknowns this proposal must resolve

1. **PR #28 is unmerged.** Unlike issue-23's precedent (already merged
   when execution-observation started), several of issue #27's 6
   acceptance criteria are inherently live-runner-only — the Pages URL
   render, the cron-tick `generated_at` advance, and the
   deliberately-broken-config fail-safety demonstration all require an
   actual GitHub Actions run against an actually-enabled Pages
   environment, neither of which has happened. The proposal must state
   explicitly how phase 2 will mark these "not yet verifiable from
   artifacts" rather than asserting a false pass or fail on them.
2. **PR comment #2's sequencing risk.** The `fetch.py` 15s-timeout /
   26.7s-actual-fetch truncation issue is explicitly stated by the human
   commenter as *not* PR #28's own defect and is split to issue #29 with
   an explicit "must land first" ordering constraint. It postdates the
   phase-2 commit, so it cannot be a trajectory or step deficiency of the
   implementation role's actual work — but it is directly relevant
   deployment-readiness context. The proposal must decide, and phase 2
   must state explicitly, how this factors into the outcome-level
   verdict (a merge-readiness caveat, not a step deficiency in PR #28's
   diff) rather than silently omitting it or silently folding it into a
   "step" finding it doesn't belong to.
3. **Approval path.** No `APPROVE issue-27/execution-observation` exists
   yet (single-account mode, per `docs/specs/approvers.md`: `JiwonJung94`,
   `jjongkwann`). Phase 2 cannot start in this session.
4. **Six acceptance criteria** need explicit per-criterion evidence
   pointers in phase 2 (diff/config citation where checkable now; "live-
   runner-only, not yet checkable" where not), not a global "looks done."
5. **Re-execution prohibition** (this session's role directive) still
   applies — same substitute method as issue-23/issue-4: static diff
   tracing, not live execution. The claimed 41/41 test-suite pass and the
   YAML/TOML syntax-validation claims in `docs/issue-27/reports/
   implementation.md` must be reported in phase 2 as *claimed, not
   independently reproduced* — this session must not re-run `pytest` or
   the workflow itself.
6. **Trajectory-level evidence** (scout-before-propose, approval-before-
   phase-2-commit) is already visible from commit/comment timestamps above,
   but phase 2 must state it against the actual file contents already read
   this session (done, per "What was independently read" above), not
   merely their existence.
