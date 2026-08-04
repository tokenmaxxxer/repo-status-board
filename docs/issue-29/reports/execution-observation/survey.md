# Current-state survey — execution-observation (issue #29)

Scope statement: this is the execution-observation role, current session,
observing issue #29 ("멀티 레포 실사용 — 병렬 수집 + 타임아웃 상향, 레포
필터, 표/배너/상세 접근성 정리"), specifically the two merged PRs that
delivered its implementation step: PR #30 ("issue-29 phase 1: parallel
fetch + repo filter + accessible tables proposal", merged `b6302925`) and
PR #33 ("issue-29 fast-follow: wire up repo filter select + change
handler", merged `c94e12d9`). Read this session to arrive at this scope:
`gh issue view 29 --comments`, `gh issue view 29` (title/body/state),
`gh pr view 30 --json number,title,body,commits,mergeCommit,files,reviews,comments`,
`gh pr view 33` (same fields), `gh pr list --state all --search issue-29`,
`git log --oneline --all`, `git branch -a`, `git fetch origin` +
`git log origin/main`, `git show --stat b621082`, and full reads of
`docs/issue-29/reports/implementation.md`, `docs/issue-23/reports/
execution-observation.md` and its `proposals/execution-observation.md` +
`reports/execution-observation/survey.md` (this same role's most recent
prior pass, read for record-structure/rigor precedent, not as evidence
about issue-29).

## What exists already

- **Issue #29: OPEN.** Body specifies 5 requirement areas (parallel
  fetch + raised timeout; native `<select>` repo filter; `Repo` as first
  column on all tables with per-table horizontal scroll instead of a
  separate mobile UI; simplified `N of M repos failed` banner with
  per-repo detail collapsed; button-based row-detail replacing the
  clickable-`<tr>` pattern, with narrow-screen inline expansion) and 7
  acceptance-criteria checkboxes (the 7th is a process rule: no
  GitHub closing-keyword in the PR body, "issue #23 T2" citation).
  Its own `## 실행 계획` names step 1 (implementation) and step 2
  (`execution-observation ‖ conformance-review`, parallel — the same
  two-role step-2 shape issue #23 and #27 used).
- **3 issue-level comments, all by `jjongkwann`:**
  1. `APPROVE issue-29/implementation` — exact bare string, the
     single-account-mode approval token for the *implementation* role
     only (contract v3: approval for one role does not carry over to
     another).
  2. Defect report (posted after live-deployment verification at
     `https://tokenmaxxxer.github.io/repo-status-board/`, exact
     wording preserved in the issue): acceptance criterion 3 (repo
     filter) unmet — `filterByRepo()`/`repoList()` existed and were
     tested but had zero real call sites; states this "overlaps with
     the period when the session crashed twice" (세션이 두 차례
     비정상 종료된 구간과 겹침).
  3. Defect report ("main 코드 직접 확인" — direct main-code check):
     acceptance criterion 6 (keyboard row-detail) and requirement 5
     (narrow-screen inline expansion) unmet, with 5 numbered specifics
     citing `dashboard.js:458-465` (`attachRowClickHandlers()` still
     binds `tbody tr[data-issue]`), the `.row-toggle` button lacking
     its own handler, `aria-expanded` permanently `"false"`
     (`selectedIssue` lacks `sourceTable`, cited at `:461`),
     `aria-controls` pointing at a nonexistent `detail-row-*` id, and
     `insertDetailRail`/`WIDE_LAYOUT_QUERY` being dead
     (comment-only/unused). States items 1-4 are being fixed "within
     scope" by issue #36's proposal (PR #37); item 5 (inline expansion)
     is explicitly left out of #36's scope, "별도 처리 필요" (needs
     separate handling).
- **PR #30**: `issue-29/implementation` → `main`, **MERGED**
  (`mergeCommit b6302925088820d3cff97e402c67249fbfe926ca`). Two commits:
  - `cc3466a1` — phase 1 (survey + scout-brief + proposal only; `files`
    list confirms only the 3 `docs/issue-29/` files, no `src/`/`test/`).
  - `05d632f5` — phase 2 (14 files: backend `fetch.py`/`cli.py` + their
    tests, frontend `index.html`/`dashboard.js`/`dashboard.css`, both
    spec docs, its own `reports/implementation.md`).
  - One PR-level comment (2026-08-03T06:12:33Z, before the phase-2
    commit): feedback attached to the approval requiring
    `max_workers=min(len(repo_configs), 8)` instead of the approved
    proposal's uncapped `len(repo_configs) or 1` — this comment is
    *not* itself an approval token (the issue-level bare-string comment
    already was); it is a same-account PR-review-shaped feedback
    comment landing between approval and phase-2 commit. `reviews: []`
    — no formal GitHub PR review exists on this PR.
  - PR body states verbatim: "This PR references #29 for context only;
    it does not close it." — the AC7 process rule (no closing keyword)
    appears honored on its face; not yet independently re-checked
    against the literal PR body text for a parseable keyword this
    session (see Gaps below).
- **PR #33**: `issue-29/implementation` → `main`, **MERGED**
  (`mergeCommit c94e12d94a6c585b7d04cc664fc579c62f7383d4`). One commit
  `d462b6d0` (`dashboard.js` +23/-1, `docs/issue-29/reports/
  implementation.md` +112). Body states it executes "item 6 of the
  already-approved `docs/issue-29/proposals/implementation.md`... no
  new proposal/approval round per that record's own recommendation" —
  i.e. it does not carry its own `APPROVE issue-29/implementation`
  comment or PR review; it treats the original phase-1 approval plus
  its own record's self-recommendation as sufficient authorization.
  Body references "#29" bare (no closing keyword prefix).
- **`docs/issue-29/reports/implementation.md`** (the observed role's own
  record, read in full this session): two sections in one file —
  the PR #30 phase-2 build (commit reference `7370d27`, `loop_state:
  landed`) and an appended "Fast-follow — repo filter wiring" section
  (PR #33, `loop_state: landed`). The PR #30 section's own "What did
  not work" names 2 defects it fixed itself (header/cell column-order
  mismatch on Flows/Sessions tables; `filterByRepo` missing from
  `module.exports`) and its own "Open findings" section **self-discloses
  4 unwired proposal-item-6 pieces before either issue comment was
  posted**: (1) repo-filter `<select>` not wired — later became issue
  comment 2's defect, fixed by PR #33; (2) no wide/narrow render
  branching / `insertDetailRow()` missing — matches issue comment 3's
  item 5, explicitly left open by issue #36; (3) `attachRowClickHandlers`
  not replaced, `aria-expanded` permanently false — matches issue
  comment 3's items 1-3; (4) **partial-failure-banner `<details>`/
  `<summary>` collapse not implemented — this specific gap is not
  mentioned in either issue comment 2 or 3.** The record also states the
  frontend build unit (the code with these 2 fixed + 4 open-finding
  defects) "had already landed in the working tree from a prior session
  that crashed before committing" and that this phase-2 session "picked
  that tree up" rather than writing it from scratch.
- **This role's own tree** (`docs/issue-29/reports/
  execution-observation/`, `docs/issue-29/proposals/
  execution-observation.md`): **does not exist yet** — this is this
  role's first phase-1 pass for issue #29, and no prior session left any
  partial commit on this branch (`git log` on `issue-29/execution-
  observation` shows no commit past what's already on `main`).
- **Current `main` (post `git fetch origin`)**: `origin/main` is exactly
  1 commit ahead of this branch — `b6210821` ("issue-36 phase 1:
  link-as-text proposal + row-toggle relocation (#37)", a **squash
  merge** of PR #37's two feature-branch commits into one). `git show
  --stat` on it confirms the squashed message contains both a "phase 1"
  and a "phase 2" section, i.e. it is not docs-only despite its
  message's "phase 1" label — its phase-2 half is code. Its own commit
  message states: "Survey found the row-toggle button's aria-expanded/
  aria-controls wiring was already broken pre-issue-36 ... the proposal
  folds the fix into the same rewrite" — i.e. issue #36's PR appears to
  have fixed part of issue comment 3's defect (items 1-4) as a
  side-effect of its own unrelated feature (relocating the row-toggle
  icon), not via any issue-29 PR. **Issue #36 and PR #37 are a separate
  issue/role's work, outside this role's write surface** — noted here
  only because it changes what "current main" looks like relative to
  what PR #30/#33 themselves delivered.

## What was independently read this session (not taken on any record's
word)

- Full `gh issue view 29 --comments` text (all 3 comments, verbatim).
- Full `gh issue view 29` body/title/state/labels.
- `gh pr view 30`/`gh pr view 33` full JSON (`body`, `commits`,
  `mergeCommit`, `files`, `reviews`, `comments`).
- `docs/issue-29/reports/implementation.md` in full (330 + 112 lines
  across its two sections) — its "What was done", "What did not work",
  "Rationale for deviations", "Open findings", "Manual smoke check",
  "Self-check", and the appended "Fast-follow" section.
- `git log --oneline --all`, `git branch -a`, `git rev-list --left-
  right --count` (branch-vs-main divergence), `git fetch origin`,
  `git show --stat b621082` (issue-36's squash-merge commit, stat only
  — full diff not read, out of this role's scope).
- Precedent structure only (not evidence about issue-29):
  `docs/issue-23/reports/execution-observation.md`, its
  `proposals/execution-observation.md`, and
  `reports/execution-observation/survey.md`; `docs/issue-27/reports/
  implementation/scout-brief.md` (scout-brief format reference).
- `docs/specs/approvers.md`: `JiwonJung94`, `jjongkwann`.

## Gaps / unknowns this proposal must resolve

1. **Scope boundary for AC6/requirement 5.** Issue #29's own PRs (#30,
   #33) left the row-detail accessibility work (AC6, requirement 5)
   substantially unmet at the time they merged (per implementation.md's
   own "Open findings" #2/#3 and issue comment 3's citations). Part of
   that gap (items 1-3 of comment 3) appears to have since been closed
   by a **different issue's** PR (#37, issue #36) as an incidental
   side-effect. The proposal must state plainly how phase 2 will render
   an outcome verdict scoped to what PR #30/#33 *themselves* delivered,
   versus separately and clearly-attributed noting of current-`main`
   state — not credit PR #30/#33 for a fix landed by a different role's
   PR on a different issue.
2. **An apparently unreported third gap.** Implementation.md's own
   "Open findings" #4 (partial-failure-banner `<details>`/`<summary>`
   collapse never implemented) maps directly to issue #29's own 5th
   acceptance-criterion bullet (`N of M repos failed` summary + collapsed
   detail) — but neither issue comment 2 nor 3 mentions it. This proposal
   must state how phase 2 will independently verify current
   `dashboard.js`'s actual `PARTIAL_BANNER` rendering against that
   specific acceptance criterion, rather than silently relying on the
   two comments' coverage as if it were exhaustive.
3. **Backend criteria (requirement 1: parallel fetch + raised timeout;
   requirement 3: Repo-first columns) are not flagged as defective in
   any issue comment.** Implementation.md's own "Manual smoke check" and
   "Self-check" sections claim these work (capped `ThreadPoolExecutor`,
   `--timeout` flag, header/cell reordering fix) but this session has
   not yet independently traced the diffs for these — the proposal must
   state the tracing method given `pytest`/live-`rsb serve` re-execution
   is prohibited to this role, same constraint issue-23's precedent
   named.
4. **Crash-recovery trajectory.** Implementation.md discloses that the
   frontend build unit (containing both the 2 defects it fixed and the
   4 it left open) "had already landed in the working tree from a prior
   session that crashed before committing," and both issue comments
   independently note their discovered defects overlap with that same
   crash period. The proposal must name this explicitly as a trajectory
   question (did picking up uncommitted crashed-session code, rather
   than a clean phase-2 build, correlate with the defects found) rather
   than treat it as incidental color.
5. **PR #33's authorization path.** PR #33 carries no
   `APPROVE issue-29/implementation` comment or PR review of its own —
   it proceeds on the original phase-1 approval plus its own
   predecessor record's self-recommendation ("fast-follow... no new
   proposal/approval round"). The proposal must name whether/how phase 2
   checks this against contract v3's approval-gate requirement, as a
   distinct trajectory question from PR #30's own approval-ordering.
6. **AC7 (no closing keyword) self-check.** Both PR bodies read this
   session appear compliant on their face (PR #30: explicit "references
   #29 for context only"; PR #33: bare "#29" with no prefix keyword),
   but this session has not yet checked the literal raw PR body text
   character-by-character for a keyword GitHub actually parses (issue
   #23's T2 finding — and issue #27's AC list — flag that even a
   backtick-quoted keyword still parses). The proposal must state this
   will be re-checked verbatim in phase 2, not assumed from a first read.
7. **Approval path.** No `APPROVE issue-29/execution-observation` issue
   comment exists, and this branch carries no open PR yet (`gh pr list
   --head issue-29/execution-observation` → empty). Phase 2 cannot start
   in this session; this pass ends at the phase-1 proposal + PR-open
   step per contract v3 s19.
