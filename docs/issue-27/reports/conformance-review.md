# Conformance-review record (issue #27)

loop_state: reported

## What was done

Checked the merged implementation (PR #28, `issue-27/implementation`,
merge commit `3ebecae` on `main`) against issue #27's 6 acceptance
criteria, decomposed into 19 independently verifiable sub-requirements
(R1a-R6b) per the approved phase-1 proposal. Verdicts below come from
direct code inspection against `main`, PR #28's true isolated diff, live
HTTP requests against the deployed Pages site and its `board.json`, `gh
run list` history for `deploy-board.yml`, a read-only source check of
`on-the-record`'s `spawn.py`/`gates/flows.py`, and an independently
re-run test suite — not from `docs/issue-27/reports/implementation.md`'s
self-report.

Housekeeping note: this session's local `main` ref started stale
(pointing at a pre-issue-27 commit); it was fast-forwarded to
`origin/main` (`git merge-base --is-ancestor` confirmed a pure
fast-forward, no local-only commits lost) before any evidence was
gathered, so all "current main" facts below reflect `origin/main`, not a
stale snapshot. Separately, an initial attempt to isolate PR #28's own
diff via `git diff c02eee3^..3ebecae` produced a misleading large diff
(it happened to span unrelated later commits, since `c02eee3` sits on a
different branch than `3ebecae`'s real parent); this was caught and
corrected using `git diff 3ebecae^..3ebecae` before any R1c/R1d/R3a
verdict was written.

## Upstream basis

Rests on `docs/issue-27/proposals/conformance-review.md` (this role's
approved phase-1 proposal, requirement list R1-R6 / 19 sub-facts) and
`docs/issue-27/reports/conformance-review/survey.md` (current-state
survey), both approved via issue #27 comment `APPROVE
issue-27/conformance-review` (jjongkwann, 2026-08-03T11:28:44Z, listed in
`docs/specs/approvers.md`; single-account mode, PR #32 author ==
approver). Subject artifact: PR #28, merged as `3ebecae` on `main`. No
`src/`/`test/` change is made by this record.

Method: `review-traceability`'s `finding-record` verdict set
(Present/Surface/Absent/Incorrect/Unverifiable) per sub-requirement, each
with an evidence pointer and rationale. Verification method is code
inspection, live HTTP requests against the deployed site
(`https://tokenmaxxxer.github.io/repo-status-board/`), `gh run
list`/`gh api` against `deploy-board.yml`'s actual run history, a
read-only fetch of `on-the-record`'s source (`raw.githubusercontent.com`,
no local checkout needed), or an independently re-run test suite (named
per row). Test suite re-run this session, against a disposable `git
worktree` of `main` (this role's own branch never carries `src/`/
`.github/` changes): `pytest test/ -q` → **55 passed**, 0 failed (higher
than `implementation.md`'s "41 passed" baseline because `main` has since
gained unrelated issue-29/34/36 tests; PR #28's own diff adds no test).

Live-only sub-facts (R1e, R2d, R3c, R5c) were flagged
Unverifiable-within-this-repo by the phase-1 survey, under the
assumption of no live access at review time. That assumption no longer
fully holds — the Pages site is now live and reachable — so R1e/R2d/R3c
carry real live evidence below, recorded as `Surface`: confirmed at the
data/mechanism level, but this sandbox still has no browser/DOM engine
(`node -e "require('jsdom')"` → module not found), so the final rendered
DOM was never directly observed. R5c remains `Unverifiable`: every
recorded workflow run to date succeeded, so no natural failure exists to
observe, and deliberately triggering one is out of this role's scope (no
repo-admin access; would mean deliberately breaking shared live
infrastructure).

`review-severity`'s `severity-classification` was considered for the 5
non-Present rows below but is not invoked: its band criteria (Chromium's
arbitrary-code-execution/cross-origin scale, or Microsoft's
attacker-authentication-state/persistence bug bar) are calibrated for
security vulnerabilities, and none of these 5 findings are
security-vulnerability-shaped — they are live-observation-depth and
test-coverage gaps in an otherwise-`Present` mechanism. Forcing a
Critical/High/Medium/Low band onto them would not be a genuine
risk-weighting judgment.

## R1 — merged 3-repo board renders at the Pages URL (AC1)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R1a: static-deploy mechanism (relative fetch, `_site/api/board.json` placement) resolves under a Pages project subpath | Present | Live-fetched `dashboard.js:566` (`https://tokenmaxxxer.github.io/repo-status-board/dashboard.js`): `fetch("api/board.json")`; live `GET https://tokenmaxxxer.github.io/repo-status-board/api/board.json` → HTTP 200; `.github/workflows/deploy-board.yml` (main) "Assemble Pages site" step: `cp board.json _site/api/board.json` | Relative fetch path plus the workflow's artifact placement resolve correctly under the project subpath — confirmed live, not just by construction |
| R1b: `boards.ci.toml` wires all 3 board repos into one merged `board.json`, not a subset | Present | `.github/boards.ci.toml` (main): 3 `[[repo]]` blocks (on-the-record, repo-status-board, tokenmaxxxer-core); live `board.json.generated_at_by_repo`: `{"on-the-record":"2026-08-03T11:31:25Z","repo-status-board":"2026-08-03T11:31:09Z","tokenmaxxxer-core":"2026-08-03T11:31:12Z"}`, `errors: []` | All 3 configured repos actually appear with fresh per-repo timestamps and zero errors in the live payload — a genuinely merged board, not a subset |
| R1c: Flows/Decision queue/Hygiene render functions reused unmodified by this diff | Present | `git diff 3ebecae^..3ebecae -- src/rsb/web/dashboard.js`: exactly one hunk, `load()`'s fetch line | PR #28's true isolated diff touches nothing in `renderHygiene`/`flowRows`/`decisionRows`/`renderTable` |
| R1d: plan rendering (issue #23's feature) unbroken by this diff | Present | Same isolated diff as R1c | The one changed line (fetch path, inside `load()`) is structurally unrelated to `buildPlanSteps()`/`renderPlanSection()` |
| R1e: opening the live Pages URL and visually confirming Flows/Decision queue/Hygiene/plan all render correctly | Surface | Live `board.json` (as of `generated_at` 2026-08-03T11:31:25Z): `flows: 57` entries, `decisions: 6`, `closure_sweep: 0`, `sessions: 0`, `ledger: 0`, `errors: []`; render functions confirmed unchanged (R1c/R1d) and structurally functional; no browser/DOM engine available in this sandbox | Every mechanism-level fact needed for a correct render is confirmed live (valid data shape, correct fetch resolution, unmodified render code), but the actual rendered DOM was never observed — short of the literal "visually confirm" method specified, hence `Surface` rather than `Present` |

## R2 — `board.json` refreshes on each cron tick (AC2)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R2a: the `schedule` trigger's cron expression is syntactically a 30-minute-interval trigger | Present | `.github/workflows/deploy-board.yml` (main): `schedule: - cron: "*/30 * * * *"` | Standard 5-field cron, `*/30` in the minutes field |
| R2b: each triggered run regenerates `board.json` with a fresh timestamp | Present | `src/rsb/cli.py:54,58,60`: `_now_iso()` defined; `_run_once()` calls `generated_at = _now_iso()` at its own top; unchanged by PR #28 | Each invocation computes a fresh timestamp, not a cached one |
| R2c: the as-of timestamp is surfaced in the dashboard's rendered UI | Present | `src/rsb/web/dashboard.js:501`: `` HEADER_META.textContent = `as of ${data.generated_at} — ...` ``; live `board.json.generated_at`: `"2026-08-03T11:31:25Z"` (populated) | As-of timestamp is both wired in the UI and actually present in the live payload |
| R2d: two real consecutive scheduled runs on the live workflow actually producing two different published `generated_at` values | Surface | `gh run list --workflow=deploy-board.yml`: 6 runs total; exactly 1 with `event: schedule` (id 30807318129, 2026-08-03T10:53:08Z, `success`); the other 5 are `workflow_dispatch`. Live `generated_at` (11:31:25Z) reflects the most recent `workflow_dispatch` run, not a second schedule tick | One genuine cron-triggered run is confirmed to fire and succeed with a real, fresh timestamp — real evidence the mechanism works — but the literal claim ("two consecutive scheduled runs, two different timestamps") needs a second schedule tick that has not yet occurred in the recorded history |

## R3 — empty `sessions`/`ledger` render cleanly (AC3)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R3a: this diff adds no new empty-state handling code | Present | Same isolated diff as R1c/R1d | Diff touches nothing in `sessionRows`/`renderAccounting`/`renderTable`'s `emptyMessage` branch or the page-level all-empty guard |
| R3b: the `runs/`-absent-on-a-fresh-runner path degrades to empty `sessions[]`/`ledger[]` without error | Present | `on-the-record` `main` (read-only, `raw.githubusercontent.com`) `spawn.py:1291-1295` (`_roster_load()`: `except (OSError, ValueError): return {}`); `gates/flows.py:141-144` (`_ledger_read()`: `if not p.is_file(): return []`) | Both the session-roster and ledger readers degrade to an empty collection, not an exception, when `runs/` (or its files) are absent — confirmed by direct source read of the actual upstream code |
| R3c: the live Pages output actually looks clean (no error banner, no broken layout) for a real all-empty case | Surface | Live `board.json` (2026-08-03T11:31:25Z): `sessions: 0`, `ledger: 0`, `errors: []`; `dashboard.js:173-176` (`renderTable`'s `emptyMessage` branch renders `<div class="region-empty">...</div>`); `:496` (`renderFullError` only fires on non-empty `data.errors`) | A real (not simulated) all-empty production case is live right now, and the code path it hits is confirmed to be the clean empty-state branch rather than the error branch — but, same boundary as R1e, no browser/DOM engine was available to directly observe the rendered page |

## R4 — local `rsb serve` has zero regression; full test suite passes (AC4)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R4a: `src/rsb/webserver.py` (local-serve's live handler) is untouched by this diff | Present | PR #28's file list (`gh pr view 28 --json files`): `src/rsb/webserver.py` not present | Confirmed absent from the changed-files list |
| R4b: the changed fetch path resolves identically under local `rsb serve` | Present | `src/rsb/webserver.py:41` (`self.path == "/api/board.json"`); local `rsb serve` serves the dashboard's `index.html` at `/` (page root) | A relative `fetch("api/board.json")` from a page at exactly `/` resolves to `/api/board.json` — identical to the pre-fix absolute path in this specific serving context |
| R4c: the existing test suite passes with PR #28's diff applied, independently re-run | Present | Independent `pytest test/ -q` against a fresh `git worktree` of `main` (`3ebecae` + later commits): **55 passed**, 0 failed | Re-run independently in this session, not accepted from `implementation.md`'s claim as-is |
| R4d: whether the one-line client-side change has direct test coverage | Absent | `test/rsb_tests/test_model.py:145-239` (`_run_dashboard_js`-based tests cover `buildPlanSteps`/`selectSummary`/`isPageEmpty` only); no test in `test/` asserts on the `fetch(...)` call or `load()` | No test exists that would fail if the fetch path regressed — a real coverage gap, distinct from R4c's "suite still passes" fact |

## R5 — a failed workflow run leaves the prior deployment untouched (AC5)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R5a: the job graph gates `deploy` on `build`'s success via `needs:`, with no `if:` weakening it | Present | `.github/workflows/deploy-board.yml` (main): `deploy: needs: build`; no `if:` key anywhere in the file | `deploy` is gated purely by `needs:`'s default success-required semantics, matching the mechanism (not PR #28's own looser prose) |
| R5b: no step in `build` suppresses failure between the generation step and the artifact-upload steps | Present | Same file, `build` job's full step list (checkout ×3, setup-python, install, generate `board.json`, assemble `_site`, configure-pages, upload-pages-artifact) | No `continue-on-error:` or `\|\| true` on any step; a nonzero `rsb` exit in "Generate board.json" stops the job before the upload steps run |
| R5c: triggering a deliberately-broken-config run against the live workflow and confirming the live Pages URL still serves the prior `board.json` | Unverifiable | `gh run list --workflow=deploy-board.yml`: all 6 recorded runs, `conclusion: success` | No failed run has occurred naturally to observe the fail-safety outcome; deliberately manufacturing one is out of this role's scope (no repo-admin access; would mean deliberately breaking shared live infrastructure) |

## R6 — PR-body closing-keyword prohibition (issue #27's 6th item)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R6a: PR #28's body text contains no closing-keyword pattern immediately followed by `#27` | Present | `gh pr view 28 --json body`, regex-checked for `close(s\|d)?`/`fix(es\|ed)?`/`resolve(s\|d)?` within 20 characters before `#27`: no match (body ends "...References #27.") | "References" is not a closing keyword; no match found anywhere in the body |
| R6b: this role's own PR body independently satisfies the same constraint | Present | `gh pr view 32 --json body`, same regex check: no match | This role's own PR (PR #32, carrying this phase-2 record) satisfies the constraint it holds PR #28 to |

## Open findings

Five sub-requirements are not `Present`: R1e, R2d, R3c (`Surface`), R4d
(`Absent`), R5c (`Unverifiable`). No `Incorrect` verdict was assigned to
any sub-requirement.

**Open-finding resolution path / next-steps:**

- **R1e / R3c** (`Surface`): no action available to this role — moving
  either to `Present` needs a browser/DOM-capable environment (not part
  of this sandbox's current toolset; `node`'s `jsdom` is not installed
  and this role does not install new tooling just to check its own
  review). A verification-depth ceiling, not a defect in the built
  artifact.
- **R2d** (`Surface`): no action needed — the live cron will keep firing
  on its own 30-minute schedule; a later look at `gh run list` (by this
  role or a future one) would likely find the second scheduled tick
  needed to fully confirm this claim. Not a defect.
- **R4d** (`Absent`): a genuine, actionable gap. A follow-up could add a
  JS-level assertion on the fetch URL, mirroring the existing
  `_run_dashboard_js` pattern already used for `buildPlanSteps` etc. —
  but `load()` itself is not in `module.exports`, so covering it would
  need either exporting a testable seam or an integration-style test.
  Handed off as a follow-up-issue candidate; not fixed by this role.
- **R5c** (`Unverifiable`): no action available to this role (needs
  deliberately breaking a live shared deployment plus repo-admin access
  to Pages settings, both out of scope per the approved proposal).
- This record is this role's terminal phase-2 deliverable for issue #27
  per contract v3 s19; next step is the human PR-merge decision on
  PR #32 (acceptance) or a requested revision on the same branch
  (feedback) — no further iteration is planned by this role absent
  either.

## Scope notes

- Per contract, this record reports verdicts only; no `src/`/`test/`
  change is made or proposed by this role. R4d's follow-up (if the human
  reviewer wants it picked up) is a task for a future `implementation`
  role on a new issue, not this record.
- Re-litigating `boards.ci.toml`'s design choices, on-the-record's
  broader internals beyond the R3b citation, and the flows-fully-remote
  optimization were out of scope, matching the approved phase-1
  proposal's own scope boundary.
