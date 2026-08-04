# Execution-observation record (issue #27)

code_under_review: PR #28 (`issue-27/implementation` → `main`, merged @
`3ebecaebcc3be9aa6a42c6622254e422b0069ecd`, 2026-08-03T07:01:53Z) —
`.github/workflows/deploy-board.yml`, `.github/boards.ci.toml`,
`src/rsb/web/dashboard.js`, `docs/handbooks/rsb.md`.
loop_state: reported

loop_state transitions (this session, 2026-08-04):
`observing` (07:05Z, evidence collection opened) →
`measuring` (07:15Z, live deployment measured — §B below) →
`reported` (07:20Z, three-level verdict written and committed).

## Approval basis

Phase 2 opened on the issue-level comment `APPROVE
issue-27/execution-observation` — author `jjongkwann`, 2026-08-03T11:28:46Z,
https://github.com/tokenmaxxxer/repo-status-board/issues/27#issuecomment-5165736988,
body read this session via `gh issue view 27 --json comments`: the entire
body is that bare string, no surrounding prose. `docs/specs/approvers.md`
on `origin/main` (read this session, `git show origin/main:docs/specs/approvers.md`)
lists `JiwonJung94` and `jjongkwann` — single-account mode per contract v3
s19, gate satisfied. This role's own phase-1 PR #31 (survey, scout brief,
proposal) merged 2026-08-03T12:31:10Z (`gh pr view 31 --json mergedAt`);
this record is the phase-2 artifact that approval unblocked.

## Provenance of this document (read this before the verdicts)

An earlier version of this record was written on this same branch in a
session that was halted mid-flight (commit
`8a77359fcf7f4dd51a077e7dc24b55edd1809099`, 2026-08-03T11:40:30Z). It is
**already on the board**: PR #31's squash merge `a604a5c8b384e884c2fe78d906818f75b34b801e`
(2026-08-03T12:31:10Z) carried it into `main` — `git show --stat a604a5c`
lists `docs/issue-27/reports/execution-observation.md` (332 lines)
alongside the three phase-1 files, even though PR #31's body announced
phase-1 content only. So the verdicts being revised below are published
verdicts, not a private draft, which is why the revision is stated
explicitly rather than silently overwritten.

This session (2026-08-04, ~07:05–07:20Z) re-collected every piece of
evidence first-hand rather than inheriting that version's conclusions,
because this role may not state a verdict about an artifact it did not
read in the session that states it. Two substantive changes resulted:

- the merged version's finding **F1** (the "issue #29 must land first"
  sequencing precondition was not honored) is **withdrawn** — it rested
  on a misread of PR #30's state, and this session's evidence refutes it
  (see "Trajectory", F1 below);
- a new measured finding **F3** (nominal 30-minute cron delivers at a
  measured ~125-minute mean interval) exists only because this session
  had ~22.6 hours of live run history to measure, where the earlier one
  had ~4.5 hours.

## What was done

Read, this session: issue #27 in full (`gh issue view 27`, body + all 3
comments with URLs); PR #28's body, its 3 review comments, its 2 commits
(`f51fc76050110119fc40e8c7d70bad6409cfb3ff`,
`c02eee3fe6103764a9fd6bcd5543bc41d503241e`) and its merge commit
`3ebecae` with per-file diffs (`git show 3ebecae -- <path>`, `--stat`);
the merge commit's parent chain (`gh api repos/.../commits/3ebecae`); the
implementation role's own record and the handbook text as merged
(`git show origin/main:<path>`); `docs/specs/approvers.md`. Then measured
the live deployment — the artifacts the merged workflow has already
produced on its own schedule — via the GitHub Actions API (run list, job
and step timings, deployment list, workflow registry state) and two
read-only fetches of the served Pages URLs. Rendered the three-level
verdict (outcome / trajectory / step) below against that evidence, mapped
all 6 of issue #27's acceptance criteria to specific evidence or an
explicit not-verifiable marking, and carried forward two findings.

Method note: this role's directive prohibits re-executing the observed
role's code, so nothing below comes from running `pytest`, dispatching
the workflow, or altering the Pages source. The Actions runs and the
served `board.json` cited here are outputs the implementation's own
merged workflow produced on its own cron; this session read them, it did
not cause them.

## Independence statement

This role did not author, propose, review, or edit any part of PR #28
(`issue-27/implementation`) — not `.github/workflows/deploy-board.yml`,
not `.github/boards.ci.toml`, not the one-line `src/rsb/web/dashboard.js`
change, not the `docs/handbooks/rsb.md` section, not the observed role's
own record `docs/issue-27/reports/implementation.md` — in this session or
any prior one. Nothing under the observed role's `src/`, `test/`, or
`docs/issue-27/{proposals,reports}/implementation*` paths was written to
by this role at any point; the only file this session writes is this
record. No command run this session re-executes the observed role's code:
no `pytest`, no `workflow_dispatch` trigger, no `rsb` invocation, no
change to the Pages configuration. Verdict language begins only after
this statement.

## §B — Live deployment measurement (실측, 2026-08-04)

All measurements below were taken between 07:05Z and 07:16Z on
2026-08-04; wall-clock reference `date -u` = `2026-08-04T07:15:39Z`.

**B1. Pages configuration** — `gh api repos/tokenmaxxxer/repo-status-board/pages`:
`"build_type": "workflow"`, `"html_url": "https://tokenmaxxxer.github.io/repo-status-board/"`,
`"public": true`, `"https_enforced": true`, `"source": {"branch": "main", "path": "/"}`.

**B2. Served payload** — read-only fetch of
`https://tokenmaxxxer.github.io/repo-status-board/api/board.json`:
- `"generated_at": "2026-08-04T05:38:47Z"`; `"errors": []`
- `"sessions": []`, `"ledger": []` — both present as empty arrays, not
  missing and not null; `"closure_sweep": []`
- top-level keys: `generated_at`, `generated_at_by_repo`,
  `owner_name_by_repo`, `decisions`, `flows`, `sessions`, `ledger`,
  `unattributed`, `closure_sweep`, `unapproved_open_prs`, `errors`
- `flows`: **73** entries — `on-the-record` 46, `repo-status-board` 14,
  `tokenmaxxxer-core` 13; **27** entries carry a non-empty `plan`
- `decisions`: 1 entry; `unapproved_open_prs`: 0; `unattributed`: 3
- `generated_at_by_repo`: `repo-status-board` 2026-08-04T05:38:36Z,
  `tokenmaxxxer-core` 2026-08-04T05:38:41Z, `on-the-record`
  2026-08-04T05:38:47Z — all three inside one 11-second window, and
  `owner_name_by_repo` resolves all three to `tokenmaxxxer/<repo>`
- staleness at read time: 07:15:39Z − 05:38:47Z = **1h 36m 52s**

**B3. Served shell** — read-only fetch of
`https://tokenmaxxxer.github.io/repo-status-board/`: `<title>rsb — status
board</title>`, heading "rsb status board", an "All repos" control, a
"Refresh" control, and the pre-JS placeholder "Loading…". (The fetch tool
available this session converts HTML to markdown, so `<script>`/`<link>`
tags were stripped from what it returned and could not be confirmed
tag-by-tag; see "What could not be verified".)

**B4. Run history** — `gh run list --workflow=deploy-board.yml --limit 20`
returned the workflow's complete history to date: **17 runs**, first
`30792167074` at 2026-08-03T07:02:12Z (19 seconds after PR #28 merged),
latest `30881307783` at 2026-08-04T05:38:15Z — a 22h 36m observation
window. Event split: 10 `schedule`, 7 `workflow_dispatch`. Conclusion on
all 17: `success`. **Zero failed runs exist.** Workflow registry state:
`gh api repos/.../actions/workflows` → id `326003799`, `.github/workflows/deploy-board.yml`,
state `active`.

**B5. Cadence of autonomous (`schedule`) ticks** — created_at of the 10
schedule runs, and the interval to the next:

| # | run created_at (UTC) | interval to next |
|---|---|---|
| 1 | 2026-08-03T10:53:08Z | 2h 39m 37s |
| 2 | 2026-08-03T13:32:45Z | 2h 41m 03s |
| 3 | 2026-08-03T16:13:48Z | 2h 00m 20s |
| 4 | 2026-08-03T18:14:08Z | 1h 53m 02s |
| 5 | 2026-08-03T20:07:10Z | 1h 28m 57s |
| 6 | 2026-08-03T21:36:07Z | 1h 15m 18s |
| 7 | 2026-08-03T22:51:25Z | 1h 07m 42s |
| 8 | 2026-08-03T23:59:07Z | 2h 35m 30s |
| 9 | 2026-08-04T02:34:37Z | 3h 03m 38s |
| 10 | 2026-08-04T05:38:15Z | — (latest) |

Span run 1 → run 10: 18h 45m 07s over 9 intervals → **mean 125.0 min**;
min 1h 07m 42s, max 3h 03m 38s. The configured expression is
`cron: "*/30 * * * *"` (`git show origin/main:.github/workflows/deploy-board.yml`,
lines 3–5), which over that span nominally schedules ~37 ticks; **10 were
delivered (≈27%)**, and no observed interval came within 37 minutes of
the nominal 30.

**B6. Latest run, job and step level** — `gh api repos/.../actions/runs/30881307783/jobs`:
`build` 05:38:18Z→05:38:51Z `success`; `deploy` 05:38:55Z→05:39:04Z
`success`. Step `Generate board.json` ran 05:38:25Z→05:38:47Z = **22s
wall-clock for all 3 repos**, and its completion timestamp is exactly the
`generated_at` of the payload served at B2 — the live page is serving
that run's output, not a stale artifact.

**B7. Deployment records** — `gh api repos/.../deployments`: latest
`5738546994`, environment `github-pages`, sha `b2f6b637c372ceec3ba4654b363f0af1ddc0d800`,
created 2026-08-04T05:38:52Z; predecessors 2026-08-04T02:35:29Z and
2026-08-03T23:59:46Z — one deployment per successful run, matching B4/B5.

## Three-level verdict

### 1. Outcome — did PR #28 land what issue #27 asked

| # | Acceptance criterion (issue #27 body) | Evidence | Verdict |
|---|---|---|---|
| 1 | Pages URL에서 3개 레포 병합 보드가 보인다 (Flows/Decision queue/Hygiene, plan 렌더링 포함) | B2: live `board.json` at the Pages URL carries all 3 repos, each with its own `generated_at_by_repo` stamp (46/14/13 = 73 flow items), 27 items with non-empty `plan`, `errors: []`; the Decision-queue/Hygiene feeds are present with `decisions` = 1 entry and `unapproved_open_prs` = 0 (a genuinely empty queue, not a missing key); B3: the served shell is the dashboard page | **Met** (merged 3-repo payload live-verified at the data contract; the JS-rendered DOM itself not visualizable this session — B3) |
| 2 | cron 주기마다 board.json이 갱신된다 (as-of 타임스탬프로 확인) | B5: 10 autonomous `schedule` runs over 18h 45m, each followed by a deployment (B7); B6: the served payload's `generated_at` equals the latest run's generate-step completion to the second. Refresh-per-tick works. But the *period* is not the configured one — mean 125.0 min against a nominal 30 min, ≈27% of ticks delivered (B5) | **Met in mechanism, missed in period** — see finding F3 |
| 3 | sessions/ledger 빈 상태가 깔끔히 렌더된다 | B2: `sessions: []`, `ledger: []`, `closure_sweep: []` — all present as empty arrays (the shape the existing empty-state path expects), no error entries, no nulls | **Met** at the data level; the rendered empty-state DOM shares limitation B3 |
| 4 | 로컬 `rsb serve` 동작 회귀 없음 (기존 테스트 전부 통과) | `docs/issue-27/reports/implementation.md` (read this session via `git show origin/main:docs/issue-27/reports/implementation.md`) and PR #28's body both claim "python -m pytest test/, 41 tests" green. This role's re-execution prohibition bars running the suite to confirm | **Claimed, not independently reproduced** (structurally: `git show 3ebecae -- src/rsb/web/dashboard.js` shows a single-line change, `fetch("/api/board.json")` → `fetch("api/board.json")`, which resolves identically under a server that serves the shell at `/`) |
| 5 | 워크플로 실패 시 직전 배포 유지가 확인된다 | `git show 3ebecae -- .github/workflows/deploy-board.yml`: the `deploy` job carries `needs: build`, so a failed `build` cannot reach `deploy-pages`; B7 confirms deployments appear only alongside successful runs. B4: **all 17 runs to date concluded `success` — no failure event exists to exercise the path** | **Structurally sound, still empirically unexercised** — 22.6h of live history contains zero failures |
| 6 | PR 본문에 closing 키워드 금지 | PR #28 body read in full this session (`gh pr view 28 --json body`): opens "Phase 1 ... for #27." and closes "References #27." — no `Closes`/`Fixes`/`Resolves` form anywhere; issue #27 confirmed `OPEN` this session (`gh issue view 27`) | **Met** |

**Outcome verdict: met, with one measured expectation gap.** 4 of 6
criteria are met on direct live evidence (B2/B3/B5/B6/B7 and the PR body
read); criterion 4 is claimed-not-reproduced by this role's own
re-execution prohibition, not by any doubt raised in the artifacts;
criterion 5 is structurally satisfied by the `needs: build` gate in
`3ebecae`'s workflow diff but cannot be called empirically verified while
zero failures exist to test it; criterion 2's refresh mechanism works but
its delivered period is ~4× the configured one (F3).

**The pre-merge truncation risk did not materialize, and the reason is
now traceable.** PR #28 comment #2
(https://github.com/tokenmaxxxer/repo-status-board/pull/28#issuecomment-5162757441,
2026-08-03T05:45:57Z) warned that `fetch.py`'s hardcoded 15s per-repo
timeout plus serial collection would truncate `on-the-record` (locally
measured 26.7s) once deployed. Live: B2 shows `on-the-record` fully
present with 46 items and `errors: []`, and B6 shows all three repos
collected in 22s wall-clock. The mechanism is the fix that landed with
issue #29 — `git show origin/main:src/rsb/fetch.py` shows
`DEFAULT_TIMEOUT_SECONDS = 60` (line 14) and a
`concurrent.futures.ThreadPoolExecutor(max_workers=min(len(repo_configs), 8))`
fan-out (lines 82–83), introduced by commit
`b6302925088820d3cff97e402c67249fbfe926ca` (#30). That commit is the
**sole parent** of PR #28's merge commit `3ebecae`
(`gh api repos/tokenmaxxxer/repo-status-board/commits/3ebecae` →
`parents: ["b6302925088820d3cff97e402c67249fbfe926ca"]`), so every live
run — starting with the first at 07:02:12Z — has run the 60s parallel
collector, never the 15s serial one.

### 2. Trajectory — was PR #28's phase-1 → phase-2 path sound

**Phase separation.** Commit `f51fc76` (2026-08-03T05:00:56Z) touched only
`docs/issue-27/` research paths; the workflow, config, and `dashboard.js`
changes appear only in `c02eee3` (05:11:24Z) — confirmed this session from
`gh pr view 28 --json commits` and the merge commit's `--stat`
(`3ebecae`: 8 files, of which `.github/*`, `src/rsb/web/dashboard.js`, and
`docs/handbooks/rsb.md` are phase-2 surfaces). Sound: no execution work
preceded approval.

**Approval gate.** `APPROVE issue-27/implementation` (jjongkwann,
2026-08-03T05:05:38Z,
https://github.com/tokenmaxxxer/repo-status-board/issues/27#issuecomment-5162505662)
is an exact bare-string issue comment from an account listed in
`docs/specs/approvers.md`, and it precedes the phase-2 commit `c02eee3`
(05:11:24Z) by 6 minutes. Sound.

**Feedback incorporation.** PR comment #1
(https://github.com/tokenmaxxxer/repo-status-board/pull/28#issuecomment-5162505771,
05:05:39Z) asked for a 60-day scheduled-workflow auto-disable note in the
handbook; `git show origin/main:docs/handbooks/rsb.md` (read this session)
carries that paragraph at lines 81–85, and it arrived inside the same
phase-2 commit rather than as an afterthought. Sound. Live corroboration:
B4 shows the workflow's registry state is still `active`, so the 60-day
clock the note describes has not yet bitten.

**F1 (carried by the version already merged to `main` via `a604a5c`) —
WITHDRAWN.** That version asserted
the "issue #29 must land before PR #28's first live run" precondition of
PR comment #2 had been bypassed, on the basis that PR #30 was still open.
This session's evidence refutes that: PR #30 merged at 2026-08-03T07:01:47Z
(`gh pr list --json number,state,mergedAt`), **6 seconds before** PR #28
merged at 07:01:53Z, and its merge commit `b630292` — which carries the
`fetch.py` 60s-timeout and ThreadPoolExecutor change — is the sole parent
of `3ebecae` (cited in §1 above). The stated precondition was therefore
honored in fact, and the first live run at 07:02:12Z already contained the
fix. The withdrawn finding is recorded here rather than deleted so the
correction is auditable; no action item attaches to it.

**Trajectory verdict: sound.** Phase separation, approval ordering, and
in-commit feedback incorporation all check out against `f51fc76` /
`c02eee3` / `3ebecae` and the three PR comment URLs cited above, and the
one cross-issue sequencing constraint a human stated in comment #2 was met
by the actual merge order (`b630292` → `3ebecae`). The margin was 6
seconds and rested on merge ordering rather than any mechanical gate — a
thin margin is not a defect, and this record raises no finding on it.

### 3. Step — which specific artifact, if any, is deficient

Traced against the approved proposal's commitments, all from the merge
commit's own diff (`git show 3ebecae -- <path>`), read this session:

- `.github/workflows/deploy-board.yml` (+72): `schedule: "*/30 * * * *"` +
  `workflow_dispatch`; `permissions: {contents: read, pages: write,
  id-token: write}`; `concurrency: {group: pages, cancel-in-progress:
  false}`; `build` job with three `actions/checkout@v4` steps (root,
  `on-the-record` → `_boards/on-the-record`, `tokenmaxxxer-core` →
  `_boards/tokenmaxxxer-core`), Python setup, rsb install, board
  generation, `_site` assembly, `configure-pages`,
  `upload-pages-artifact`; `deploy` job with `needs: build` and
  `deploy-pages@v4`. B6's step list matches this structure step-for-step
  on the live runner. No defect.
- `.github/boards.ci.toml` (+14): three `[[repo]]` blocks all pointing at
  the single shared `_boards/on-the-record/spawn.py` checkout — matches
  the proposal and is corroborated by B2's three-repo payload. No defect.
- `src/rsb/web/dashboard.js` (1 line): `-  const res = await
  fetch("/api/board.json");` / `+  const res = await
  fetch("api/board.json");` at the `load()` function. Live-confirmed
  functional by B2 (the served page's fetch target resolves under the
  project subpath). No defect.
- `docs/handbooks/rsb.md` (+22): static-deploy section present with the
  fail-safety rationale (lines 65–85 on `origin/main`) — see F2 for its
  one gap.

**F2 (step, documentation) — a pre-merge doc request was never
incorporated. Confirmed, still open.**

- **Impact**: `docs/handbooks/rsb.md` on `origin/main` (read this session)
  documents Pages activation only as "a repo admin must set **Settings →
  Pages ...**" (line 76) and carries no mention of the non-interactive
  API alternative. A future operator following the handbook believes the
  UI is the only path, when in practice this deployment was activated by
  an API call.
- **Timeline**: PR comment #3
  (https://github.com/tokenmaxxxer/repo-status-board/pull/28#issuecomment-5163037047,
  2026-08-03T06:25:41Z) reported running `gh api -X POST
  repos/tokenmaxxxer/repo-status-board/pages -f build_type=workflow` and
  asked that the handbook be amended to "레포 관리자가 UI 또는 위 API
  호출로 1회 설정". It landed 74 minutes after the phase-2 commit
  (`c02eee3`, 05:11:24Z) and 36 minutes before merge (07:01:53Z). No third
  commit exists on PR #28 (`gh pr view 28 --json commits` returns exactly
  `f51fc76`, `c02eee3`), and `git grep` over `origin/main`'s handbook for
  `gh api` / `build_type` returns nothing. B1 independently confirms the
  end state the comment described: `"build_type": "workflow"`.
- **Root cause**: the request arrived in the window between the phase-2
  commit and the merge, and the merge proceeded on the pre-existing issue
  comment approval with no re-read of PR comments accumulated after that
  commit. The gap is in the merge-time check, not in any code.
- **Action item**: one line in the handbook's static-deploy section noting
  the `gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow`
  alternative, while keeping the "workflow cannot do this itself"
  statement that remains true. This role does not make that edit
  (independence); it is handed to the approver on this record.

**Step verdict: no defect in the workflow, config, or JS artifacts PR #28
diffed** — each traced above against `3ebecae`'s own diff and corroborated
by the live run structure in B6 — **with one documentation-completeness
gap (F2) in `docs/handbooks/rsb.md`.**

## F3 (outcome, live measurement) — the delivered cron period is ~4× the configured one

- **Impact**: issue #27's acceptance criterion 2 expects board refresh at
  the cron period, and `deploy-board.yml` configures `*/30 * * * *`. The
  live board's measured mean refresh interval is **125.0 minutes** (B5),
  and at the moment of this observation the served payload was **1h 37m
  old** (B2) — over three times the freshness the configuration implies.
  Anyone reading the board's as-of timestamp sees the true value, so this
  misleads no one silently; but an operator who plans around "at most 30
  minutes stale" is planning against a number this deployment does not
  deliver.
- **Timeline**: measured across the workflow's entire schedule history to
  date — 10 autonomous ticks between 2026-08-03T10:53:08Z and
  2026-08-04T05:38:15Z (B5), i.e. ~27% of the ~37 ticks the expression
  nominally schedules over that span. Not a degradation over time: the
  shortest interval observed (1h 07m 42s) and the longest (3h 03m 38s)
  are interleaved.
- **Root cause**: not a defect in PR #28's diff — the expression is valid
  and the runs that do fire complete in ~50s end-to-end (B6). GitHub
  delivers `schedule` events on a best-effort basis and drops ticks under
  platform load, most visibly on high-frequency crons in public repos.
  The configured value was chosen as the proposal's default and never
  measured against delivered behavior, because no live runner existed
  before merge (PR #28's own test plan says so explicitly).
- **Action item**: for the human to judge — either accept the measured
  ~2h cadence and correct the expectation where it is written (issue
  #27's AC 2 wording, and a handbook line stating the observed delivery
  rate), or, if sub-hour freshness is genuinely required, drive refresh
  from something other than a bare high-frequency `schedule` trigger
  (e.g. `repository_dispatch` from the boards' own activity, or a
  coarser cron whose nominal value matches reality). This role does not
  edit `.github/workflows/deploy-board.yml` or the issue text.

## What could not be verified

- **The rendered DOM at the live Pages URL** (tables, plan rendering,
  repo filter behaviour, summary chips, empty-state styling). The fetch
  tool available this session does not execute client-side JavaScript and
  converts HTML to markdown, so B3 could only observe the pre-JS shell —
  it returned the title, headings, the "All repos" and "Refresh"
  controls, and "Loading…", with `<script>`/`<link>` tags stripped by the
  markdown conversion. No browser-automation tool was available in this
  headless session. Substituted with B2's data-contract inspection.
  Criteria 1 and 3 are therefore verified at the data level, not the
  pixel level; `conformance-review` (PR #32, separate role) is the
  parallel step-2 check on issue #27.
- **The `41 passed` pytest run and the YAML/TOML syntax-validation
  claims** in `docs/issue-27/reports/implementation.md` — reported as
  claimed, not reproduced, per this role's re-execution prohibition.
- **Fail-safety under a real failure** (criterion 5) — B4 shows zero
  failed runs across all 17 to date, so only the `needs: build`
  dependency in `3ebecae`'s workflow diff could be traced. Deliberately
  breaking a run to test it would be re-execution of the observed role's
  code and is prohibited here.
- **Whether the ~27% schedule delivery rate (F3) persists**, or is
  specific to this 18h 45m window — one window is what exists to measure.
- **Issue #29 / PR #30 / PR #33's own soundness** — outside this role's
  assigned issue. Their merge times and `fetch.py` content are cited above
  strictly as facts bearing on PR #28's live behaviour, not evaluated.
- **`conformance-review`'s parallel work on issue #27** (PR #32, merged
  2026-08-03T12:31:16Z) — separate role, separate record, not read for
  verdict purposes here.

## Upstream basis (everything cited above, read this session)

- Issue #27 body + all 3 comments, with URLs and authors
  (`gh issue view 27 --json comments`); `gh issue view 29` for issue
  #29's state (`OPEN`) and its measured-timing background table.
- PR #28: body, 3 comments (URLs cited inline), commits `f51fc76` /
  `c02eee3`, merge commit `3ebecae` with `--stat` and per-file diffs, and
  its parent chain via `gh api repos/.../commits/3ebecae`.
- `origin/main` blobs: `.github/workflows/deploy-board.yml`,
  `docs/handbooks/rsb.md`, `docs/specs/approvers.md`,
  `docs/issue-27/reports/implementation.md`, `src/rsb/fetch.py` (the last
  read only to identify the mechanism that prevented the predicted
  truncation, and cited as current state, not as evidence of what the
  observed role did).
- `gh pr list --state all --json number,state,mergedAt,headRefName` for
  the merge ordering of #28 / #30 / #31 / #32 / #33.
- Live artifacts produced by the merged workflow, read (never triggered)
  this session: `gh run list --workflow=deploy-board.yml`,
  `gh api repos/.../actions/runs/30881307783/jobs`,
  `gh api repos/.../actions/workflows`, `gh api repos/.../deployments`,
  `gh api repos/.../pages`, and read-only fetches of
  `https://tokenmaxxxer.github.io/repo-status-board/` and
  `.../api/board.json`.
- This role's own phase-1 artifacts, merged via PR #31:
  `docs/issue-27/proposals/execution-observation.md`,
  `docs/issue-27/reports/execution-observation/survey.md`,
  `.../scout-brief.md` — the method commitments executed above.

## Open findings

- **F1** — *withdrawn* (trajectory). The merged version's claim that the
  issue-#29-first precondition was bypassed is refuted by
  `b630292` → `3ebecae` parentage and PR #30's 07:01:47Z merge. No action.
- **F2** — **open** (step, documentation). `docs/handbooks/rsb.md` omits
  the `gh api ... -f build_type=workflow` Pages-activation path that a
  pre-merge PR comment asked for and that was actually used. One-line
  fix; the approver's call.
- **F3** — **open** (outcome, measured). Configured 30-minute cron
  delivers at a measured 125-minute mean; served payload was 1h 37m stale
  at observation. Not a diff defect; an expectation-versus-platform gap
  that either the expectation or the trigger design should absorb.

Neither open finding changes the outcome verdict above (met, with the
criterion-2 period gap named as F3). Both are handed to the human on this
record.

## Open-finding resolution path

This role cannot file issues (contract v3 — issues are user-authored
only) and cannot edit PR #28's surfaces or the observed role's record
(independence). Resolution of F2/F3 sits with the human approver, via
this record's own PR:

- **Reviewing**: the approver judges F2 and F3 here — each is either a
  real defect worth acting on or an accepted condition.
- **If accepted as defects**: the approver, the only party who may author
  an issue under this contract, opens one for whichever of F2 (handbook
  wording) / F3 (cron expectation or trigger design) they want addressed;
  both are small enough for a fast-follow PR against `main`, the shape
  already used on this repo for issue #29's own fast-follow (PR #33,
  merged 2026-08-03T07:30:51Z).
- **If not accepted**: no further action; this record stands as the
  documented observation and this role's phase 2 is complete
  (`loop_state: reported`) either way.
- **Merge or close of this record's PR** is the next human decision this
  record waits on, per contract v3 (merge = acceptance of the delivered
  observation).

## Next steps

None from this role. `loop_state: reported` is terminal for
execution-observation on issue #27; F2/F3 resolution, if accepted, is the
approver's action.
