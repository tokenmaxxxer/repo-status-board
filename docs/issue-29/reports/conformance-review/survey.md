# Conformance-review survey (issue #29)

Subject: merged implementation on `main` (PR #30 `7370d27`/amend + PR #33
fast-follow `c94e12d`, both `issue-29/implementation`) checked against
issue #29's 8 acceptance-criteria checkboxes. Branch was fast-forwarded
from a stale local `main` (`5d05b5f`) to the true current tip (`b621082`,
issue-36's squashed row-toggle-relocation merge) before this survey —
the initial local clone under-counted one merged PR. Board = what's
merged to `main`; `docs/issue-29/reports/implementation.md` (the
building role's self-report) is read here only to orient, not as a
verdict source, per this role's phase-2 mandate.

Scout: ran, 1 stage, saturated immediately — see `scout-brief.md`.

## What's merged (`main` @ `b621082`, as of this survey)

- `src/rsb/fetch.py` — `DEFAULT_TIMEOUT_SECONDS = 60` (was 15);
  `fetch_board()` uses `concurrent.futures.ThreadPoolExecutor`,
  `max_workers = min(len(repo_configs), 8) or 1`, `.map()` (preserves
  `repo_configs` input order in results regardless of completion order).
- `src/rsb/cli.py` — top-level `--timeout SECONDS` flag (default
  `DEFAULT_TIMEOUT_SECONDS`), threaded into `_run_once`/`--watch`/`serve`.
- `src/rsb/web/index.html` — `<select id="repo-filter" aria-label="Filter
  by repo">` with `<option value="">All repos</option>` in the header.
- `src/rsb/web/dashboard.js` — `filterByRepo(data, repo)` (pure, exported,
  tested), `repoList(data)` (union of succeeded + failed repo names),
  `updateRepoFilterOptions(data)` (repopulates `<select>`, preserves
  selection), a `change` listener on `REPO_FILTER` (resets
  `selectedIssue`, re-renders via `filterByRepo`, no refetch), `load()`
  now populates `boardData`/calls `updateRepoFilterOptions`/renders the
  filtered view. All four row builders (`decisionRows`/`flowRows`/
  `sessionRows`/`renderAccounting`'s ledger rows) put Repo first in both
  `cells` and the corresponding `renderTable([...])` header array.
  `renderTable()` wraps every table in `<div class="table-scroll">`.
  Issue/PR cells render `rowToggleButtonHtml()` (a real `<button
  class="row-toggle" aria-expanded aria-controls="detail-panel-slot"
  data-issue data-repo data-table>`, icon-only ▸/▾) leading a
  `numberLinkHtml()` `#<n>` GitHub link. `attachRowToggleHandlers()`
  binds directly to `.row-toggle` buttons (not the `<tr>`), tracks
  `sourceTable`, toggles `selectedIssue` open/closed. `isRowExpanded()`
  checks `selectedIssue.sourceTable === sourceTable`.
- `src/rsb/web/dashboard.css` — `.table-scroll { overflow-x: auto; }`,
  `.row-toggle` (button-chrome reset + `:focus-visible` outline),
  `.issue-cell` (keeps button+link on one line), `.number-link`,
  `.detail-row td` (narrow-screen inline-expansion styling — see gap
  below), `.partial-banner details`/`summary` (collapse styling — see
  gap below).
- `docs/specs/design-system.md` / `docs/specs/screen-spec.md` — re-synced
  for `RepoFilter`, Repo-first + `.table-scroll`, button-not-row trigger
  wording; both explicitly document (not paper over) the two gaps below.
- Test suite: `python3 -c "import sys; sys.path.insert(0,'src'); import
  pytest; sys.exit(pytest.main(['test/','-q']))"` → **55 passed**, 0
  failed, run fresh this session against `b621082`.

## Issue #29's 8 acceptance criteria (verbatim source, for the requirement list)

1. 3레포 수집이 병렬로 돌고, 가장 느린 레포도 잘리지 않는다 (실측 26.7초
   기준 여유 확인)
2. 레포 하나가 실패해도 나머지 레포 데이터는 그대로 표시된다
3. `All repos` ↔ 개별 레포 전환 시 표와 요약 칩이 함께 재계산된다
4. 모든 표의 첫 열이 `Repo`이고, 좁은 화면에서 페이지 본문이 가로
   스크롤되지 않는다
5. 실패 배너가 `N of M repos failed` 요약 + 접힌 상세 형태다
6. 키보드만으로 행 상세를 열 수 있다
7. 기존 테스트 전부 통과 (로컬 serve 회귀 없음)
8. 주의: PR 본문에 closing 키워드 금지 (issue #23 T2 — 백틱 인용도
   파싱됨)

Plus the 2 defects logged as issue #29 comments (both post-PR#30, found
during live-deployment verification), which this review is separately
asked to confirm:

- **Defect A** (comment 1): `filterByRepo()`/`repoList()` implemented and
  tested but never called — deployed `<select>` stuck at "All repos"
  only. Maps to AC3.
- **Defect B** (comment 2): row-click handler still binds the whole
  `<tr>` (not `.row-toggle`), `aria-expanded` permanently `false`
  (`sourceTable` never tracked), `aria-controls` points at a
  nonexistent id, and 요구사항 5's narrow-screen inline expansion is
  unimplemented (`insertDetailRow`/`WIDE_LAYOUT_QUERY`/`matchMedia`
  are dead). Maps to AC6 (items 1-4 of the comment) and separately to
  요구사항 5 (item 5 of the comment, not itself one of the 8 AC
  checkboxes but explicitly flagged as unmet by the comment).

## Observations shaping requirement decomposition (not verdicts)

- **AC1** bundles: (a) collection is genuinely concurrent, not serial;
  (b) the timeout default was raised with a stated margin over the
  issue's own 26.7s measurement; (c) the margin claim and the raised
  default are documented together, not just coded. `test_fetch.py`
  (`test_fetch_board_runs_repos_in_parallel`,
  `test_default_timeout_seconds_is_60`) test (a)/(b)'s value directly;
  the issue's own "실측 26.7초 기준 여유 확인" wording is a live-timing
  claim against real `flows --json` subprocesses this repo/environment
  cannot reproduce (no `on-the-record`/`tokenmaxxxer-core` checkouts
  here) — the *documented margin* (60s vs. 26.7s, ~2.24x, recorded in
  `docs/issue-29/proposals/implementation.md`'s Rationale) is locally
  checkable; whether that margin still holds against *today's* real
  repo timings is not, flagged as a likely Unverifiable-within-this-repo
  sub-fact for phase 2, distinct from the checkable default-value fact.
- **AC2** is a single fact but has two check points worth keeping
  separate: partial-failure isolation existed pre-#29 (serial code) and
  must still hold post-#29 (parallel code) — `test_fetch.py`'s
  `test_fetch_board_merges_multiple_repos_partial_failure` exercises the
  new `ThreadPoolExecutor` path directly, not the old serial one.
- **AC3** bundles four separately-checkable facts, matching the shape of
  Defect A exactly: the `<select>`'s options are populated from live
  data (not just "All repos"), a `change` listener exists and calls the
  filter with no refetch, the *table* recomputes, and the *summary
  chips* recompute together with it (the AC's own "함께" wording — a bug
  could filter the table but leave chips computed off the unfiltered
  set, since both read from whatever `data` argument `renderData`
  receives). Code inspection shows `renderData(data)` computes
  `selectSummary(data)` from the same `data` its table-builders consume,
  so table and chips cannot desync — but this is inference from a single
  shared-argument code path, not a dedicated test isolating "chips
  changed" from "table changed" as two independent assertions.
- **AC4** bundles three: (a) all four *dashboard* tables (not
  `render.py`'s CLI renderer, out of scope per the approved proposal) put
  Repo first in both header and cell order — a header/cell mismatch bug
  here was already caught and fixed once by the implementation role
  itself (self-reported "What did not work" #1), so this needs a fresh
  independent re-check, not a carry-over of that claim; (b) each table
  scrolls independently (`.table-scroll`); (c) the *page* does not
  scroll horizontally at narrow widths — checkable by CSS inspection
  (no page-level fixed/min-width wider than viewport outside the
  per-table scroll containers) but not by an actual narrow-viewport
  render, which this sandbox cannot drive (no browser), matching every
  prior conformance-review precedent in this repo (issue-4, issue-23)
  recording the same DOM-rendering limitation.
- **AC5** is the one criterion where direct code reading surfaces a
  likely non-Present sub-fact, **not previously logged as an issue
  comment** (distinct from Defect A/B): the summary line ("{M} of {N}
  repos failed to load") is present and always-visible, but the
  per-repo detail is *not* collapsed behind `<details>/<summary>` as the
  criterion's own text specifies ("접힌 상세") and as the approved
  proposal's item 6 explicitly calls for
  (`docs/issue-29/proposals/implementation.md:199-204`) — the shipped
  `PARTIAL_BANNER.innerHTML` (`dashboard.js`, `renderData()`) inlines
  every `"{repo}: {message}"` pair comma-joined directly into the
  always-visible line, no `<details>` element anywhere. This is not a
  guess: the implementation role's own record
  (`docs/issue-29/reports/implementation.md` "Open findings" #4) and
  both re-synced spec docs (`screen-spec.md` §2.5,
  `design-system.md` §6's `PartialFailureBanner` note) already state
  this gap explicitly and accurately — `dashboard.css` even carries
  unused `.partial-banner details`/`summary` rules for it (dead CSS,
  same pattern as the AC6-adjacent `.detail-row` gap below). Unlike
  Defect A (fixed by PR #33) and Defect B items 1-4 (fixed by the
  issue-36 merge), this specific gap has **no follow-up PR and is not
  named in either issue #29 comment** — it is a candidate third defect
  this review surfaces independently, decomposed into two sub-facts
  (summary line correct; detail actually collapsed) so phase 2 can score
  them separately rather than as one bundled miss.
- **AC6** bundles five, matching Defect B's own five-item structure
  (items 1-4 map to AC6's literal "키보드만으로 행 상세를 열 수 있다"
  text; item 5 maps to 요구사항 5's narrow-screen clause, not AC6's
  literal text, but the comment groups it alongside AC6 and the task
  explicitly asks this review to confirm both defects): (a) trigger is a
  real `<button>`, not a clickable `<tr>`; (b) the click handler binds
  to the button itself, not the row; (c) `aria-expanded` reflects actual
  open/closed state (requires `sourceTable` tracking); (d)
  `aria-controls` points at an id that actually exists in the DOM; (e,
  separate from AC6's literal text but part of Defect B) narrow-screen
  inline expansion (`insertDetailRow`/`matchMedia`) is implemented.
  Current code (`b621082`, post issue-36 merge) shows (a)-(d) fixed —
  `attachRowToggleHandlers` binds `.row-toggle` directly,
  `aria-controls="detail-panel-slot"` (a real, always-present id, not
  the never-existing `detail-row-*` the pre-#36 code used),
  `isRowExpanded()` checks `sourceTable`. (e) remains unimplemented —
  `WIDE_LAYOUT_QUERY` is defined but no `matchMedia` call reads it, no
  `insertDetailRow` function or `.detail-row` markup emission exists
  anywhere; the issue-36 merge commit's own message states this is
  "out of scope for this change." No browser/keyboard-event engine was
  driven this session (matches the same limitation issue-4/issue-23's
  reviews recorded) — (a)-(d) are code-inspection-only verdicts, native
  `<button>` keyboard-operability itself is a browser default not
  independently re-derived here.
- **AC7**: full suite green this session (55 passed) at the actual
  current `main` tip, not just at the commit the implementation records
  claimed (49 passed at `7370d27`/`c94e12d`) — the higher count reflects
  tests added by the intervening issue-34/issue-36 merges, not a
  discrepancy.
- **AC8** scopes to PR #30 and PR #33 (the two PRs the task names as the
  merged implementation) — PR #35/#37 belong to issues #34/#36, not #29,
  and are out of this AC's scope. Grepped both bodies for
  close/closes/closed/fix/fixes/fixed/resolve/resolves/resolved
  patterns near any `#29` reference: PR #30 has "does not close it"
  (negated, not a GitHub closing-keyword phrase); PR #33 has "defect fix
  per issue #29's..." (word "fix" not immediately followed by `#29` in
  closing-keyword form). Neither matches GitHub's auto-close grammar
  (keyword directly adjacent to `#<n>`).

## Constraints on phase 2's verification depth

- No browser/live server driven this session — matches issue-4 and
  issue-23's own recorded limitation. DOM-rendering claims (AC3's chip
  recompute, AC4's no-page-scroll, AC6's keyboard operability) are
  checkable by code inspection plus existing Node-subprocess/jsdom tests
  where they exist, not by eyeballing a running page at a narrow
  viewport.
- AC1's "실측 26.7초 기준 여유 확인" full timing claim cannot be
  re-measured from this repo/environment (no `on-the-record`/
  `tokenmaxxxer-core` checkouts, no live `spawn.py`) — the *documented*
  margin is checkable, the *current-day* margin is not, noted above as a
  phase-2 Unverifiable candidate for that half specifically.
- The implementation role's own "Open findings" section already
  self-disclosed AC5's `<details>` gap and AC6(e)'s narrow-screen gap
  before this review started — phase 2 independently re-derives both
  from the current code/spec rather than accepting that self-report,
  per this role's mandate, but the self-report is useful orientation
  (and explains why no separate issue comment exists for the AC5 gap:
  it was tracked internally, not yet picked up by a follow-up PR).

## Write-set for this role

This role only reads `src/`, `test/`, `docs/specs/`, and issue #29; it
writes only `docs/issue-29/reports/conformance-review/`,
`docs/issue-29/proposals/conformance-review.md`, and (phase 2, after
approval) `docs/issue-29/reports/conformance-review.md`. No `src/`/
`test/` change is proposed or made by this role.
