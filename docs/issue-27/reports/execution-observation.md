# Execution-observation record (issue #27)

code_under_review: PR #28 (`issue-27/implementation` → `main`, merged @
`3ebecaebcc3be9aa6a42c6622254e422b0069ecd`) — `.github/workflows/deploy-board.yml`,
`.github/boards.ci.toml`, `src/rsb/web/dashboard.js`, `docs/handbooks/rsb.md`.
loop_state: reported

Approved via issue #27 comment `APPROVE issue-27/execution-observation`
(jjongkwann, exact bare string,
https://github.com/tokenmaxxxer/repo-status-board/issues/27#issuecomment-5165736988,
2026-08-03T11:28:46Z), against
`docs/issue-27/proposals/execution-observation.md` (this role's own
approved phase-1 proposal). Executes that proposal's §0-§2 method: static
diff/config tracing plus live-artifact inspection (this repo's PR #28
merged and its GitHub Actions workflow/Pages deployment have since
executed for real, so criteria the phase-1 survey marked
live-runner-only are now empirically checkable from the deployed
artifacts themselves — no code was re-run to get this evidence, only
already-produced Actions run history and the already-served `board.json`
were read).

## What was done

Read PR #28 (`issue-27/implementation`, merged @ `3ebecae`) in full —
both commits' diffs, its 3 PR comments, and its own phase-1/phase-2
records/survey/scout-brief/proposal (already read once in this role's
prior phase-1 session, re-cited here) — then, because PR #28 has since
merged and its workflow has executed live (unlike this role's own
phase-1 survey, which observed it still open/unmerged), inspected the
actual produced artifacts: the GitHub Actions run history for
`deploy-board.yml` and the live-served `board.json`/Pages page. Rendered
the three-level verdict this role's contract requires
(outcome/trajectory/step) against that evidence, mapped all 6 of issue
#27's acceptance criteria to specific evidence or an explicit
not-yet-verifiable/claimed-not-reproduced marking, and surfaced two
process/documentation findings (F1, F2) below. No code was written or
changed by this role.

**Rationale (why now, why this method):** issue #27's own `## 실행 계획`
names this role's step-2 verification as required alongside
`conformance-review` before the issue's work is considered done, and
this role's own phase-1 proposal committed to rendering exactly this
three-level verdict once `APPROVE issue-27/execution-observation`
landed (cited above). The method substitutes live-artifact inspection
for the live-runner gaps the phase-1 survey flagged, instead of
re-executing PR #28's code, because this session's role directive
prohibits re-running the observed role's code regardless of whether a
live environment now exists to run it in.

## Independence statement

This role did not author, propose, or edit any part of PR #28
(`issue-27/implementation`) — not its workflow YAML, its config, its
one-line `dashboard.js` fix, its handbook section, or its own record
(`docs/issue-27/reports/implementation.md`) — in this session or any
prior one. Nothing under PR #28's `src/`, `test/`, or
`docs/issue-27/{proposals,reports}/implementation*` paths was touched by
this role. This session ran no command that re-executes the observed
role's code (no `pytest`, no manual `workflow_dispatch` trigger, no
Pages-source change) — the GitHub Actions run history and `board.json`
cited below are artifacts the implementation's own merged workflow
already produced on its normal schedule, read here, not re-run.

## Three-level verdict

### 1. Outcome — did PR #28 land what issue #27 asked

| # | Acceptance criterion (issue #27 body) | Evidence | Verdict |
|---|---|---|---|
| 1 | Pages URL에서 3개 레포 병합 보드가 보인다 (Flows/Decision queue/Hygiene, plan 포함) | Live fetch this session of `https://tokenmaxxxer.github.io/repo-status-board/api/board.json` (generated_at `2026-08-03T10:53:36Z`): `on-the-record` 29 flow items, `repo-status-board` 8, `tokenmaxxxer-core` 17, `errors: []`. The static HTML shell (`index.html`) loads `dashboard.js`, which is the file whose one-line relative-fetch fix this PR made — the data contract it consumes is confirmed populated. The rendered DOM itself could not be visually confirmed (`WebFetch` on `https://tokenmaxxxer.github.io/repo-status-board/` returns the pre-JS "Loading…" shell, since it does not execute client-side JS) | **Met** (data contract verified live; DOM render not independently visualizable this session, see "What could not be verified") |
| 2 | cron 주기마다 board.json이 갱신된다 | `gh api repos/tokenmaxxxer/repo-status-board/actions/workflows/326003799/runs`: run id `30807318129`, `event: "schedule"`, `created_at 2026-08-03T10:53:08Z`, `conclusion: success` — an autonomous (non-manual) cron tick, whose completion window matches the `board.json` `generated_at: 2026-08-03T10:53:36Z` fetched above | **Met** (one autonomous tick observed and matched to the served payload's timestamp; repeated 30-min periodicity beyond this one sample not exhaustively paginated this session — see note below) |
| 3 | sessions/ledger 빈 상태가 깔끔히 렌더된다 | Same live `board.json`: `sessions: []`, `ledger: []`, both present (not missing/null) and empty, `closure_sweep: []` also empty, no error entries | **Met** |
| 4 | 로컬 `rsb serve` 동작 회귀 없음 (기존 테스트 전부 통과) | `docs/issue-27/reports/implementation.md` (read via `git show 3ebecae:docs/issue-27/reports/implementation.md`) claims "python -m pytest test/, 41 tests, green, no regression" | **Reported as claimed, not independently reproduced** — this role's re-execution prohibition bars running `pytest` itself |
| 5 | 워크플로 실패 시 직전 배포 유지가 확인된다 | `.github/workflows/deploy-board.yml` (`git show 3ebecae -- .github/workflows/deploy-board.yml`): `deploy` job carries `needs: build`, so a failed `build` job structurally cannot trigger `deploy-pages`. Of the 6 most-recent runs read via the Actions API this session (ids `30809822009` in-progress, `30807318129`, `30807016131`, `30793939259`, `30792209643`, `30792167074`), every completed run has `conclusion: success` — **no failed run exists in the observed history**, so the fail-safety property has not been exercised by an actual failure | **Not yet empirically verifiable** — structurally supported by the diffed job-dependency, but untested by any real failure to date |
| 6 | PR 본문에 closing 키워드 금지 | PR #28 body (`gh pr view 28 --json body`, read in full): opens "Phase 1 (research/survey/proposal) + phase 2 (implementation) for #27." and closes "References #27." — no `Closes`/`Fixes`/`Resolves #27` pattern anywhere in the body; issue #27 is confirmed still **OPEN** (`gh issue view 27 --json state`) | **Met** |

**Outcome verdict: substantially met.** 4 of 6 criteria met with direct
live/diff evidence; 1 (test-suite regression) is claimed-not-reproduced
per this role's own re-execution prohibition; 1 (failure fail-safety) is
structurally sound but has no failure event yet to empirically confirm.

**Deployment-readiness caveat (not a step defect in PR #28's own diff):**
PR #28 comment
(https://github.com/tokenmaxxxer/repo-status-board/pull/28#issuecomment-5162757441,
2026-08-03T05:45:57Z) flagged that `fetch.py`'s hardcoded 15s
per-repo timeout, combined with a locally-measured 26.7s fetch time for
`on-the-record`, would truncate that repo's data once deployed live,
and stated the fix (issue #29, still **OPEN**/unmerged — confirmed this
session via `gh issue view 29` and `gh pr list`) "must land before PR
#28's first live run." Empirically, this did **not** happen: the live
`board.json` fetched this session shows `on-the-record` fully present
(29 items) with an empty `errors` array, as of the `2026-08-03T10:53:36Z`
generation — several live runs (including the immediate post-merge runs
at `07:02:12Z`/`07:02:58Z` and the `07:31:02Z`/`10:48:30Z`/`10:53:08Z`
runs) have completed successfully without the predicted truncation. This
does not retroactively invalidate the commenter's caution — the 15s
timeout in `fetch.py` is unchanged, live code, and remains a latent risk
under slower network conditions — but the specific sequencing risk has
not materialized in any run observed this session.

### 2. Trajectory — was PR #28's own phase-1→phase-2 path sound

Phase 1 discipline: commit `f51fc76050110119fc40e8c7d70bad6409cfb3ff`
(2026-08-03T05:00:56Z) touched only `docs/issue-27/` paths (survey,
scout-brief, proposal — confirmed via this role's own phase-1 survey's
`git diff --stat`), no source/workflow code. Sound.

Approval-gate ordering: issue-level comment `APPROVE
issue-27/implementation` (jjongkwann,
https://github.com/tokenmaxxxer/repo-status-board/issues/27#issuecomment-5162505662,
2026-08-03T05:05:38Z) is an exact bare-string match against
`docs/specs/approvers.md`'s listed accounts (`JiwonJung94`, `jjongkwann`,
read this session) — a clean single-account-mode gate, unlike issue-23's
PR #24 precedent (which mixed the token with trailing prose). Phase-2
commit `c02eee3fe6103764a9fd6bcd5543bc41d503241e` (05:11:24Z) followed
the approval comment in time. Sound.

Feedback incorporation: PR comment #1
(https://github.com/tokenmaxxxer/repo-status-board/pull/28#issuecomment-5162505771,
05:05:39Z, one minute after the approval comment) asked for a
60-day-scheduled-workflow-inactivity note in the handbook. The phase-2
commit (05:11:24Z, six minutes later) added exactly that note —
confirmed by this role's own phase-1 survey's diff read of
`docs/handbooks/rsb.md` and re-confirmed against `main` this session
(`git show main:docs/handbooks/rsb.md`, "GitHub auto-disables a
`schedule`-triggered workflow after 60 days..." paragraph present).
Sound — feedback given before the phase-2 commit was folded into that
same commit, not bolted on after.

**Finding F1 (trajectory) — a stated sequencing precondition had no
enforcement mechanism and was not honored in practice:**

- **Impact**: PR comment #2 (cited above, 05:45:57Z) stated issue #29
  "must land before PR #28's first live run," but PR #28 merged at
  `07:01:53Z` and its workflow began running immediately after
  (`07:02:12Z` dispatch) and continued on its 30-minute cron. Issue #29
  and its PR #30 remain **OPEN**, unmerged, as of this session
  (`gh issue view 29`, `gh pr list`). The precondition was bypassed by
  the actual sequence of events. No harm has manifested yet (see outcome
  caveat above — the live board has not been observed truncated), but
  that is incidental to runner network conditions, not to any gate that
  enforced the stated order.
- **Timeline**: comment posted 05:45:57Z; PR #28 merged 07:01:53Z
  (`mergeCommit 3ebecaebcc3be9aa6a42c6622254e422b0069ecd`); first
  post-merge workflow runs at `07:02:12Z` and `07:02:58Z`; issue #29 /
  PR #30 still open at observation time this session.
- **Root cause**: the "must land first" constraint was stated only in
  PR-comment prose, never encoded as a mechanical gate (e.g. a disabled
  `schedule` trigger, a config flag, or branch protection tying
  `deploy-board.yml`'s activation to issue #29's merge state) — nothing
  in `.github/workflows/deploy-board.yml` (read in full this session)
  conditions the cron on any external issue status.
- **Action item**: if this sequencing constraint is still considered
  load-bearing given issue #29's continued open state, it needs an
  actual gate (e.g., hold `schedule:` disabled or gate `fetch.py`'s
  timeout via `boards.ci.toml` until issue #29 merges) rather than a
  comment-only precondition. Handed off as a finding on this record —
  this role does not edit `.github/workflows/deploy-board.yml` or
  `src/rsb/fetch.py` itself, per its independence requirement.

**Trajectory verdict: sound overall on this PR's own phase-1→phase-2
discipline and approval gate, with one confirmed process gap (F1) in how
a human-stated cross-issue sequencing precondition was (not) enforced.**

### 3. Step — which specific artifact, if any, is deficient

Hand-traced against the approved proposal's §0.3/§1 commitments, all via
`git show 3ebecae -- <path>` (the merge commit) read in full this
session:

- `.github/workflows/deploy-board.yml`: `schedule: '*/30 * * * *'` +
  `workflow_dispatch` triggers, `concurrency: {group: pages,
  cancel-in-progress: false}`, `build` job (3x `actions/checkout` — root,
  `on-the-record`→`_boards/on-the-record`, `tokenmaxxxer-core`→
  `_boards/tokenmaxxxer-core`; `rsb --config .github/boards.ci.toml
  --json > board.json`; `_site/` assembly; `configure-pages`;
  `upload-pages-artifact`), `deploy` job (`needs: build`,
  `deploy-pages@v4`) — matches the proposal's design and the
  implementation record's own description line for line. Traced correct.
- `.github/boards.ci.toml`: 3 `[[repo]]` blocks, all pointing `command`
  at the single shared `_boards/on-the-record/spawn.py` checkout — matches.
- `src/rsb/web/dashboard.js`: exactly one line changed (line 540 on
  `main` today, `fetch("/api/board.json")` → `fetch("api/board.json")`)
  — confirmed live-functional (outcome criterion 1 above). A fresh grep
  this session of `dashboard.js` (`fetch\(|href=|\.src=`) and
  `index.html` (`src=|href=`) for any other absolute-path reference this
  role's own proposal committed to checking found none — the only
  `fetch(` call is the one already fixed, `index.html`'s `<link
  href="dashboard.css">` and `<script src="dashboard.js">` are already
  relative, and the one dynamic `href` in `dashboard.js` (the external
  issue/PR link) is a data-driven URL, not a static asset path. No
  additional step defect in this file.

**Finding F2 (step, documentation) — a pre-merge doc-wording request was
not incorporated before merge:**

- **Impact**: `docs/handbooks/rsb.md`'s static-deploy section (read on
  `main` this session) documents only the UI path for enabling Pages
  ("a repo admin must set Settings → Pages → Build and deployment →
  Source: GitHub Actions") and states the default `GITHUB_TOKEN` "cannot
  flip this setting itself" — with no mention that an owner-scoped `gh`
  API call can do this non-interactively, which is exactly what actually
  happened in practice.
- **Timeline**: PR comment #3
  (https://github.com/tokenmaxxxer/repo-status-board/pull/28#issuecomment-5163037047,
  06:25:41Z) reports the commenter ran `gh api -X POST
  repos/tokenmaxxxer/repo-status-board/pages -f build_type=workflow` to
  enable Pages, and asks the handbook be supplemented to say "a repo
  admin, via UI or the above API call" — posted after the phase-2
  commit (`c02eee3`, 05:11:24Z) but 36 minutes **before** PR #28 merged
  (07:01:53Z). No third commit exists on the PR to incorporate it; `git
  show main:docs/handbooks/rsb.md` confirms the merged text still carries
  only the UI-only wording today.
- **Root cause**: the request landed in the window between the phase-2
  commit and merge, and the merge proceeded on the pre-existing
  `APPROVE issue-27/implementation` approval without a check for PR
  comments accumulated after that commit.
- **Action item**: a small follow-up (one line in
  `docs/handbooks/rsb.md`'s static-deploy section noting the `gh api -X
  POST repos/<owner>/<repo>/pages -f build_type=workflow` alternative)
  would close this; this role does not make that edit itself, per its
  independence requirement — handed off as a finding.

**Step verdict: no defect in the workflow/config/JS artifacts actually
diffed by PR #28; one documentation-completeness gap (F2) in
`docs/handbooks/rsb.md` relative to feedback given before merge.**

## What could not be verified

- The dashboard's actual rendered DOM (tables, plan rendering, repo
  filter, summary chips) at the live Pages URL — `WebFetch` returns the
  pre-JS "Loading…" shell since it does not execute client-side
  JavaScript; this role has no browser-automation tool available this
  session. Substituted with direct inspection of the `board.json` data
  contract the dashboard consumes (populated, error-free, per outcome
  criterion 1) and the already-diffed `dashboard.js` fetch-path fix.
- Full 30-minute cron periodicity beyond the single "schedule"-event run
  matched above — pagination of the full Actions run history beyond the
  6 most-recent runs was blocked by this session's command-approval
  gate (a `gh api` call with query-string filtering required interactive
  approval unavailable in this headless session); one autonomous tick
  was directly confirmed instead of an exhaustive series.
- The claimed "41 passed" `pytest` run and the YAML/TOML
  syntax-validation claims in `docs/issue-27/reports/implementation.md`
  — reported as claimed, not independently reproduced, per this role's
  re-execution prohibition.
- The workflow's actual behavior on a genuine failure (criterion 5) —
  no failed run exists in the observed history to exercise it; only the
  job-dependency structure was traced.
- `conformance-review`'s parallel step-2 work on issue #27 (PR #32,
  confirmed open this session via `gh pr list`) — separate role,
  separate branch, out of this role's write surface and not evaluated
  here.
- Issue #29 / PR #30's own soundness — out of this role's assigned scope
  (issue #27 only); cited above only as a fact (open/unmerged), not
  evaluated.

## Upstream basis

- `docs/issue-27/proposals/execution-observation.md`,
  `docs/issue-27/reports/execution-observation/survey.md`,
  `scout-brief.md` — this role's own phase-1 research and method
  commitments, executed above.
- PR #28 (`gh pr view 28 --json body,commits,files,comments,reviews,
  mergedAt,mergeCommit`), its 2 commits (`f51fc76`, `c02eee3`), its 3
  comments, and `git show 3ebecae -- <path>` for every changed file —
  all read in full this session.
- `docs/issue-27/reports/implementation.md`,
  `docs/issue-27/reports/implementation/survey.md`, `scout-brief.md`,
  `docs/issue-27/proposals/implementation.md` — the observed role's own
  phase-1/phase-2 artifacts, read in full in this role's prior phase-1
  session and re-cited here.
- Issue #27 (`gh issue view 27 --json title,body,comments,state`), all 3
  of its comments, read in full this session.
- Live artifacts produced by the merged workflow, read (not re-run) this
  session: `gh api repos/tokenmaxxxer/repo-status-board/actions/
  workflows` and `.../runs` (6 most-recent runs), and
  `https://tokenmaxxxer.github.io/repo-status-board/api/board.json`
  (generated_at `2026-08-03T10:53:36Z`).
- `docs/specs/approvers.md` (`JiwonJung94`, `jjongkwann`), confirming the
  approval-comment gate this record cites.
- Issue #29 (`gh issue view 29`) and `gh pr list --search "issue-27"` —
  cited as facts (open/unmerged states), not evaluated for their own
  content, per this role's scope boundary.

## Open findings

- **F1** (trajectory, process) — the "issue #29 before PR #28's first
  live run" sequencing precondition had no mechanical enforcement and
  was not honored in the actual event order; no observed harm to date.
  Open.
- **F2** (step, documentation) — `docs/handbooks/rsb.md` does not
  reflect the `gh api` Pages-activation alternative a pre-merge PR
  comment asked to be added. Open.

Neither finding blocks the outcome verdict above (substantially met);
both are handed off on this record for a human to judge and act on, per
this role's prohibition on editing PR #28 or its record directly.

## Open-finding resolution path

This role cannot file issues (contract v3: issues are user-authored
only) and cannot edit PR #28, `.github/workflows/deploy-board.yml`,
`src/rsb/fetch.py`, or `docs/issue-27/reports/implementation.md`
(independence requirement). Resolution of F1/F2 is therefore entirely in
the human approver's hands, via this record's own PR:

- **Reviewing**: the approver reads F1/F2 here and judges whether each
  is a real defect worth acting on, an accepted risk (e.g. that issue
  #29's fix landing later, given the observed lack of truncation so far,
  is tolerable), or something in between.
- **If accepted as defects**: the approver — the only party who can file
  an issue under this contract — opens a new issue for whichever of F1
  (sequencing-gate enforcement) / F2 (handbook API-method wording) they
  want addressed, e.g. as a small fast-follow PR against `main` (the
  issue-29 fast-follow precedent on this same repo already demonstrates
  this shape) or folded into issue #29's own scope.
- **If not accepted**: no further action; this record stands as the
  documented observation, and this role's phase 2 is complete
  (`loop_state: reported`) regardless of that decision.
- **Merge/close of this record's PR** is itself the human decision this
  record waits on next, per contract v3 (PR merge = acceptance of the
  delivered observation work).

## Next steps

None from this role beyond this record and the resolution path above —
`loop_state: reported` is terminal for this role's own work on issue
#27. Resolution of F1/F2, if accepted, is the human approver's action
(e.g. via a fast-follow PR, as already used for issue #29's own
repo-filter fast-follow on this repo) or a new user-authored issue, per
contract v3's issue-authorship rule.
