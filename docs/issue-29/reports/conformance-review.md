# Conformance-review record (issue #29)

loop_state: reported

## What was done

Checked the merged implementation (PR #30 `issue-29/implementation`
phase 2, PR #33 fast-follow, both merged to `main`, current tip
`b621082`) against issue #29's 8 acceptance-criteria checkboxes,
decomposed per the approved phase-1 proposal into R1a-R9b. Verdicts
below were derived from direct code/spec/PR-body inspection and a fresh
local test run this session, not from
`docs/issue-29/reports/implementation.md`'s self-report. Both defects
logged as issue #29 comments after PR #30 merged (repo-filter wiring;
row-toggle wiring/aria) are independently re-confirmed as fixed; the
third gap the phase-1 survey surfaced independently (AC5's missing
`<details>` collapse) and 요구사항 5 (narrow-screen inline expansion,
Defect B item 5) are independently re-confirmed as still unfixed.

**Requirement-count correction.** The approved proposal's own summary
states "23 independently-checkable sub-requirements"; the requirement
list it actually itemizes (R1a through R9b) totals **27**
(R1: 5, R2: 2, R3: 5, R4: 3, R5: 2, R6: 4, R7: 2, R8: 2, R9: 2). This
record scores all 27 items as actually listed in
`docs/issue-29/proposals/conformance-review.md` — the "23" in that
document's own summary/PR-#41-description text is an arithmetic
undercount, not a narrower requirement set. No requirement was dropped
or added; the discrepancy is noted here rather than silently carried
forward.

## Upstream basis

Rests on `docs/issue-29/proposals/conformance-review.md` (this role's
approved phase-1 proposal, requirement list R1-R9) and
`docs/issue-29/reports/conformance-review/survey.md` +
`docs/issue-29/reports/conformance-review/scout-brief.md` (current-state
survey and scout), all approved via issue #29 comment
`APPROVE issue-29/conformance-review` (jjongkwann, 2026-08-03T11:53:57Z,
listed in `docs/specs/approvers.md`; single-account mode, PR #41 author
== approver). Subject artifact: PR #30 (`b630292`) + PR #33 (`c94e12d`),
both merged to `main`; current `main` tip at review time `b621082`
(confirmed identical to `origin/main` this session — no drift since the
phase-1 survey). No `src/`/`test/` change is made by this record.

Method: `review-traceability`'s `finding-record` verdict set (Present /
Surface / Absent / Incorrect / Unverifiable) per sub-requirement, each
with an evidence pointer and rationale. Verification method is either
code inspection, an existing automated test (named per row), or PR-body
text inspection (R9); no new tests were written by this role, matching
the approved implementation proposal's explicit out-of-scope call on a
new JS test harness. Test suite re-run this session:
`python3 -c "import sys; sys.path.insert(0,'src'); import pytest;
sys.exit(pytest.main(['test/','-q']))"` → **55 passed**, 0 failed, at
`main`'s actual current tip (higher than either PR's self-reported count
of 49, reflecting tests added by the intervening issue-34/issue-36
merges, not a discrepancy — matches the phase-1 survey's own note).
`review-severity`'s `severity-classification` is applied to the four
non-Present findings below, using this repo's own precedent adaptation
(`docs/issue-4/reports/conformance-review.md`) of a deterministic
four-band lookup for this non-security context — **Blocking** (defeats
the requirement's purpose or misleads the operator), **Major** (spec
violation, user-visible, doesn't defeat the requirement's core purpose),
**Minor** (spec violation, cosmetic/non-blocking), **Note** (not itself a
proven spec violation — an observation worth flagging).

## R1 — parallel collection + timeout headroom (AC1)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R1a: `fetch_board()` fetches repos concurrently (`ThreadPoolExecutor`/`.map()`), not serially | Present | `src/rsb/fetch.py:82-89` (`ThreadPoolExecutor(max_workers=...)`, `executor.map(...)`) | Replaces the pre-#29 serial loop; `.map()` fans work across up to 8 threads |
| R1b: `DEFAULT_TIMEOUT_SECONDS` raised from 15s to a value with a documented margin over the issue's 26.7s measurement | Present | `src/rsb/fetch.py:14` (`DEFAULT_TIMEOUT_SECONDS = 60`); `test/rsb_tests/test_fetch.py:71-72` (`test_default_timeout_seconds_is_60`); `docs/issue-29/proposals/implementation.md:83-84` ("채택안: 60초(≈2.25배 마진)") | Value change is test-locked and the margin (60s vs. 26.7s measured, ≈2.25x) is recorded in the approved implementation proposal's Rationale, not just coded silently |
| R1c: an automated test demonstrates parallel wall-clock is meaningfully shorter than serial | Present | `test/rsb_tests/test_fetch.py:75-91` (`test_fetch_board_runs_repos_in_parallel`: 4 repos × 0.2s each; asserts `elapsed < sleep_seconds * len(repos) * 0.75`) | Test measures actual wall-clock through the real `fetch_board()`/`ThreadPoolExecutor` path, not a mock of concurrency |
| R1d: a CLI/config mechanism exists to adjust the timeout without a code change | Present | `src/rsb/cli.py:35-41` (`--timeout SECONDS` flag, default `DEFAULT_TIMEOUT_SECONDS`); `:94` (threaded into `serve`'s `fetch_fn`), `:103`/`:109` (threaded into `--watch`/`_run_once`) | Flag reaches every code path that calls `fetch_board` |
| R1e: the documented margin still holds against real, present-day `flows --json` timings | Unverifiable | No `on-the-record`/`tokenmaxxxer-core` checkout or live `spawn.py` exists in this repo/environment to re-measure | This is a live-timing claim against real subprocesses this sandbox cannot reproduce; the *documented* margin (R1b) is checkable, the *current-day* margin is not — distinct facts, scored separately per the approved proposal |

## R2 — one repo failing doesn't drop the others (AC2)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R2a: per-repo fetch/normalize failures are caught and turned into a `RepoError`, never raised past `fetch_and_normalize_one` | Present | `src/rsb/fetch.py:45-66` (`fetch_and_normalize_one`: `try`/`except RuntimeError`/`except JSONDecodeError`/`except PayloadError`, each returning `(repo_name, None, message)`, never a bare `raise`); `test/rsb_tests/test_fetch.py:30-53` (`test_fetch_and_normalize_one_subprocess_failure`, `..._unparseable_json`, `..._schema_mismatch`) | All three failure modes (subprocess error, bad JSON, schema mismatch) are exercised directly against this function and confirmed non-raising |
| R2b: this isolation is proven against the *new* `ThreadPoolExecutor` path specifically, not just inherited from the old serial code by assumption | Surface | `test/rsb_tests/test_fetch.py:55-68` (`test_fetch_board_merges_multiple_repos_partial_failure` — misnamed: both repos actually *succeed*, `assert len(model.errors) == 0`); `:94-109` (`test_fetch_board_result_order_matches_repo_configs_order` — all 5 repos *fail*, proving per-repo error attribution survives reversed completion order under `ThreadPoolExecutor`, but with no repo succeeding alongside them) | No test calls `fetch_board()` (the actual `ThreadPoolExecutor`/`.map()` path) with a literal mix of ≥1 succeeding and ≥1 failing repo in the same invocation. `test_merge_repos_collects_errors_without_dropping_other_repos` (`test/rsb_tests/test_model.py:110-116`) does test a mixed outcome, but calls `merge_repos()` directly on hand-built tuples, bypassing the concurrent path entirely. The behavior is very likely correct by composition (R2a's non-raising guarantee + the all-fail ordering test), but the exact AC2 scenario — one fails, the others still show — is not directly demonstrated through the new concurrent code path |

## R3 — `All repos` ↔ per-repo switch recomputes table + chips together (AC3, = Defect A)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R3a: the repo-filter `<select>`'s options are populated from live fetched data | Present | `src/rsb/web/dashboard.js:465-472` (`updateRepoFilterOptions`, built from `repoList(data)`); `:130-136` (`repoList`: union of `generated_at_by_repo` keys + `errors[].repo`); `:573` (`load()` calls `updateRepoFilterOptions(boardData)`) | `<select>` is no longer hardcoded — Defect A's original bug (options never populated) is fixed |
| R3b: a `change` listener is attached and calls the filter/render path with no refetch | Present | `src/rsb/web/dashboard.js:586-589` (`REPO_FILTER.addEventListener("change", ...)` calls `renderData(filterByRepo(boardData, REPO_FILTER.value))` — no `fetch()` call in the handler) | Confirms the second half of Defect A (listener existed nowhere pre-fix) |
| R3c: the *table* rows narrow to the selected repo | Present | `src/rsb/web/dashboard.js:108-124` (`filterByRepo` filters `decisions`/`flows`/`sessions`/`ledger`/etc. by `repo`); `test/rsb_tests/test_model.py:271-300` (`test_dashboard_js_filter_by_repo_narrows_every_section`, asserts every field narrows) | Directly tested on the shipped function across all filtered fields |
| R3d: the *summary chips* recompute for the selected repo, not just the table | Present | `src/rsb/web/dashboard.js:509` (`selectSummary(data)`) and `:539-556` (row builders) both consume the same `data` argument inside `renderData(data)`; `:574`/`:588` both call `renderData(filterByRepo(boardData, REPO_FILTER.value))` | Structural guarantee by code reading — `renderData` never receives unfiltered data alongside filtered rows, so table and chips cannot desync. No dedicated test isolates "chips changed" as a separate assertion from "table changed" (verification method here is inspection, not test) |
| R3e: switching back to "All repos" restores the full unfiltered view | Present | `src/rsb/web/dashboard.js:109` (`filterByRepo`: `if (!repo) return data;`); `test/rsb_tests/test_model.py:293` (`unfiltered = dashboard.filterByRepo(data, "")`) | Empty-string repo value (the "All repos" `<option value="">`) is the explicit unfiltered branch, test-covered |

## R4 — Repo-first columns + per-table-only scroll (AC4)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R4a: all four dashboard tables render `Repo` as the first header and first cell in every row | Present | `src/rsb/web/dashboard.js:264` (`decisionRows`), `:298` (`flowRows`), `:313` (`sessionRows`), `:331` (`renderAccounting`'s ledger rows) — all emit `<td>${escapeHtml(<row>.repo)}</td>` as the first cell; headers at `:539` `["Repo", "Issue", "PR", ...]`, `:543` `["Repo", "Issue", "Stage", ...]`, `:547` `["Repo", "Role", "Issue", ...]`, `:338` `["Repo", "Issue", "Sessions", ...]` | Header/cell order independently re-checked and matched for all four tables — the implementation role's own record notes a header/cell mismatch was caught and fixed once already; this is a fresh confirmation, not a carry-over |
| R4b: each table is wrapped in its own horizontally-scrolling container, independent of the others | Present | `src/rsb/web/dashboard.js:187` (`renderTable` wraps every table in `<div class="table-scroll">`); `src/rsb/web/dashboard.css:154` (`.table-scroll { overflow-x: auto; }`) | Single shared function (`renderTable`) used by all four tables, so the scroll behavior is structurally uniform, not duplicated per-table code that could drift |
| R4c: no page-level horizontal scroll is structurally possible at narrow widths | Present | `src/rsb/web/dashboard.css:78-82` (`.page { max-width: var(--grid-max-width); }`, no `min-width`); `:88-93`/`:112-117` (`.page-header`/`.summary-strip` both `flex-wrap: wrap`); `:139-154` (`table.data-table { width: 100%; }` lives inside `.table-scroll`'s own `overflow-x: auto`) | Code/CSS inspection only — no narrow-viewport render was driven this session (no browser in this sandbox), matching the same limitation `docs/issue-4/reports/conformance-review.md` and `docs/issue-23/reports/conformance-review.md` both recorded. No element outside a `.table-scroll` container carries a fixed/min width wider than the viewport |

## R5 — failure banner: summary + collapsed detail (AC5)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R5a: an always-visible `"{M} of {N} repos failed to load"` summary line renders on partial failure | Present | `src/rsb/web/dashboard.js:515-524` (`renderData`: `${failedRepos.length} of ${total} repos failed to load`, rendered unconditionally into `PARTIAL_BANNER.innerHTML` whenever `failedRepos.length > 0` and at least one repo succeeded) | Summary line renders correctly and is always visible (not itself behind any disclosure) |
| R5b: the per-repo `"{repo}: {message}"` detail is actually collapsed behind `<details>/<summary>` | Absent | `src/rsb/web/dashboard.js:518-524` (`const detail = failedRepos.map((e) => \`${e.repo}: ${e.message}\`).join(", "); PARTIAL_BANNER.innerHTML = \`... — ${detail} ...\`` — `detail` is interpolated directly into the always-visible line, no `<details>` element anywhere in the template); `src/rsb/web/dashboard.css:252-258` (`.partial-banner summary`, `.partial-banner details[open] summary` rules exist but are never emitted by any JS — dead CSS) | AC5's own text ("접힌 상세") and the approved implementation proposal's item 6 both specify a collapsed disclosure; the shipped banner inlines every failing repo's message into one always-visible line instead. Confirmed independently from the current code, not from the implementation role's own self-disclosure of this gap — matches that self-report, but re-derived here per this role's phase-2 mandate. Not logged as an issue #29 comment (unlike Defect A/B); no follow-up PR exists for it |

## R6 — keyboard-only row-detail opening (AC6, = Defect B items 1-4)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R6a: the disclosure trigger is a real `<button>`, not a clickable `<tr>` | Present | `src/rsb/web/dashboard.js:237` (`rowToggleButtonHtml`: `<button type="button" class="row-toggle" ...>`); `:182` (`renderTable`'s `<tr>${r.cells.join("")}</tr>` carries no `onclick`/`data-*` of its own, per the comment at `:178-181` explaining the old whole-row binding was removed) | No `attachRowClickHandlers`-style whole-row handler exists anywhere in the file (grepped, zero matches) — Defect B item 1 is fixed |
| R6b: the click handler binds to the button itself (`.row-toggle`), not the row | Present | `src/rsb/web/dashboard.js:479-490` (`attachRowToggleHandlers`: `MAIN.querySelectorAll(".row-toggle").forEach((button) => button.addEventListener("click", ...))`) | Listener is attached directly to each toggle button, not the containing row — Defect B item 2 is fixed |
| R6c: `aria-expanded` reflects the actual open/closed state (tracking which table's row is selected) | Present | `src/rsb/web/dashboard.js:199-206` (`isRowExpanded(sourceTable, issue, repo)` checks `selectedIssue.sourceTable === sourceTable`); `:484-487` (`sourceTable` captured from `button.dataset.table` and stored on `selectedIssue` at click time); `:241-242` (`issueToggleCell` computes `expanded` via `isRowExpanded` before rendering the button) | `sourceTable` tracking (absent pre-fix, permanently `false`) now exists — Defect B item 3 is fixed |
| R6d: `aria-controls` references an id that actually exists in the rendered DOM | Present | `src/rsb/web/dashboard.js:237` (`aria-controls="detail-panel-slot"`); `src/rsb/web/index.html:26` (`<div id="detail-panel-slot"></div>`, present unconditionally in the page shell) | Fixed id, always present — replaces the pre-fix `detail-row-*` id that never existed anywhere in the DOM. Defect B item 4 is fixed. (Native `<button>` keyboard-operability itself is a browser default, not independently re-derived here — no browser/keyboard-event engine was driven this session, matching issue-4/issue-23's own recorded limitation; R6a-d verify the DOM structure/wiring that keyboard operability depends on) |

## R7 — narrow-screen inline expansion (요구사항 5, = Defect B item 5)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R7a: a `matchMedia`-driven branch exists selecting side-panel vs. inline-row rendering at `breakpoint-lg` (1200px) | Absent | `src/rsb/web/dashboard.js:19` (`WIDE_LAYOUT_QUERY = "(min-width: 1200px)"` defined) but no `matchMedia(...)` call anywhere in the file (grepped, zero matches) | The constant exists but is never read — dead code, not a partial implementation |
| R7b: the narrow-screen path inserts the detail as a row immediately below the triggering row in the same table | Absent | No `insertDetailRow` function definition or call anywhere in `dashboard.js` (grepped; the name appears only inside the file's own comment at `:14-18` explaining it does not exist); no `.detail-row` markup is ever emitted by any JS function — `src/rsb/web/dashboard.css:202-208`'s `.detail-row td` rule is unused dead CSS | On narrow screens, `DETAIL_SLOT` still renders (via the same `renderDetailPanel` used for the wide side-panel), placed after `MAIN` in DOM order rather than inline below the specific triggering row — detail is reachable by scrolling, not lost outright, but does not match 요구사항 5's inline-row placement |

## R8 — existing tests pass, no local-serve regression (AC7)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R8a: full pytest suite passes at the current `main` tip | Present | `python3 -c "import sys; sys.path.insert(0,'src'); import pytest; sys.exit(pytest.main(['test/','-q']))"` → **55 passed**, 0 failed, run fresh this session against `b621082` | Fresh run this session, not a carried-over count from either PR's self-report (which claimed 49 at their own commit) |
| R8b: `webserver.py`/`serve`-path tests specifically are included in that green run | Present | Same run's `test_webserver.py` subset: 4 passed (confirmed via `pytest test/ -q -k "web or serve"` → `4 passed, 51 deselected`) | AC's explicit "로컬 serve 회귀 없음" clause is covered, not just the suite total |

## R9 — PR body has no closing keyword (AC8, PR #30 and PR #33 only)

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R9a: PR #30's body contains no GitHub closing-keyword phrase immediately adjacent to `#29` | Present | PR #30 body (`gh pr view 30`): "This PR references #29 for context only; it does not close it." | "close" is followed by "it", not `#29` — negated and not adjacent, so it does not match GitHub's auto-close grammar (keyword immediately adjacent to `#<n>`) |
| R9b: same check for PR #33's body | Present | PR #33 body (`gh pr view 33`): "Follow-up defect fix per issue #29's live-deployment comment..."; footer line "#29" (bare) | "fix" is separated from `#29` by "per issue" — not adjacent closing-keyword form; the standalone "#29" footer line carries no keyword at all. Neither matches GitHub's auto-close grammar |

## Open findings

Four non-Present findings survive (R2b, R5b, R7a, R7b); all hand off to
a follow-up issue for a future implementation role to pick up, per this
repo's established pattern (`docs/issue-4/reports/conformance-review.md`,
`docs/issue-23/reports/conformance-review.md`) — this role does not
patch `src/`/`test/` itself.

- **R5b — partial-failure detail not collapsed** — severity: **Major**.
  `src/rsb/web/dashboard.js:518-524`. Directly contradicts AC5's own
  text and the approved implementation proposal's explicit design
  decision (item 6); user-visible whenever ≥1 but not all repos fail
  (every failing repo's message is dumped into one always-visible line
  instead of behind a disclosure). Does not block core function — the
  summary count is correct and data for succeeding repos still renders
  — but is a real, spec-contradicting UX regression as repo count grows.
- **R7a/R7b — narrow-screen inline expansion unimplemented** — severity:
  **Major**. `src/rsb/web/dashboard.js:19` (dead constant), no
  `matchMedia`/`insertDetailRow` anywhere. User-visible on any viewport
  narrower than 1200px (a majority of mobile/tablet widths): detail
  panel renders after all tables rather than inline below the triggering
  row, matching neither 요구사항 5's text nor the two-column side-panel
  behavior R6's evidence confirms works correctly at ≥1200px. Not
  blocking — the panel is still reachable by scrolling — but it is an
  explicitly named, still-unmet requirement (Defect B item 5), and the
  issue-36 merge that fixed Defect B items 1-4 explicitly scoped this
  item out rather than fixing it.
- **R2b — mixed-outcome partial-failure scenario untested on the new
  concurrent path** — severity: **Note** (not itself a proven spec
  violation). `test/rsb_tests/test_fetch.py:55-68,94-109`. The shipped
  behavior is very likely correct by composition of two already-tested
  facts (R2a's non-raising guarantee; the all-repos-fail ordering test),
  but no test drives `fetch_board()`'s actual `ThreadPoolExecutor` path
  with a literal mix of succeeding and failing repos in one call —
  flagged as a coverage gap worth closing before this path is next
  touched, not as a known-broken behavior.

**Open-finding resolution path / next steps:**

- R5b, R7a/R7b: file a follow-up GitHub issue covering both the
  `<details>` collapse (R5b) and the narrow-screen inline-row expansion
  (R7a/R7b, = 요구사항 5 / Defect B item 5) for a future implementation
  role. Both are pre-existing, explicitly scoped-out gaps (issue-36's
  merge commit states R7 is "out of scope for this change"; R5b has no
  follow-up PR and was not named in either issue #29 comment), not new
  regressions introduced by this review.
- R2b: no code change implied — recorded so a future touch to
  `fetch_board`/`fetch_and_normalize_one` has a named gap to close with
  a mixed-outcome test, rather than assuming existing coverage already
  proves it.
- R1e: no resolution action, by design — a live-timing claim against
  real `on-the-record`/`tokenmaxxxer-core` `flows --json` subprocesses
  this repo/environment has no means to reproduce. Left as a standing
  scope boundary for any future review with access to a live upstream
  checkout, not a task for this repo to pick up.
- This record is this role's terminal phase-2 deliverable for issue #29
  per contract v3 s19; next step is the human PR-merge decision on PR
  #41 (acceptance) or a requested revision on the same branch (feedback)
  — no further iteration is planned by this role absent either.

## Scope notes

- `src/rsb/render.py` (CLI text renderer)'s column order was out of
  scope, per the approved proposal — issue #29's Rationale section
  explicitly scopes the Repo-first requirement to the dashboard only.
- New JS test harness / browser automation was out of scope, per the
  approved implementation proposal's own out-of-scope call, not reopened
  here — R1e, R4c, R6's keyboard-operability inference, and R7 are
  constrained accordingly (code-inspection-only or
  Unverifiable-within-this-repo).
- The implementation role's own "Open findings" section had already
  self-disclosed R5b and R7's gaps before this review started; both
  verdicts above were independently re-derived from the current
  code/spec per this role's phase-2 mandate, not accepted from that
  self-report — they happen to agree with it.
- Per contract, this record reports verdicts only; no `src/`/`test/`
  change is made by this role.
