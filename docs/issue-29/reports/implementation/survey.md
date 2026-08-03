# Current-state survey — issue #29

Scope: the write set issue #29 touches — parallel fetch + timeout
(`fetch.py`), a client-side repo filter, table column ordering, the
partial-failure banner, and accessible row-detail disclosure (all three
in `src/rsb/web/`), plus the accepted specs (`docs/specs/screen-spec.md`,
`docs/specs/design-system.md`) that some of this either contradicts or
already (unimplemented-ly) calls for.

## 1. Parallel fetch + timeout (`src/rsb/fetch.py`, `cli.py`, `webserver.py`, `config.py`)

`DEFAULT_TIMEOUT_SECONDS = 15` (fetch.py:12), consumed only by
`run_flows_json(repo_config, timeout=DEFAULT_TIMEOUT_SECONDS)`
(fetch.py:15), passed straight into `subprocess.run(..., timeout=timeout)`
(fetch.py:24-29); `TimeoutExpired` becomes `RuntimeError(f"... timed out
after {timeout}s")` (fetch.py:30-31). `fetch_and_normalize_one(repo_config,
run_json_fn=run_flows_json)` (fetch.py:43) calls `run_json_fn(repo_config)`
with **no timeout argument threaded through** — today the only way to vary
it is to monkeypatch `run_json_fn` itself in tests.

`fetch_board(repo_configs, run_json_fn=run_flows_json)` (fetch.py:67-70) is
the sequential point: a plain list comprehension, one repo at a time — this
is what becomes the `ThreadPoolExecutor` call. `fetch_and_normalize_one`
already never raises (catches `RuntimeError`/`JSONDecodeError`/
`PayloadError` internally, always returns a 3-tuple) — it's already safe to
hand straight to an executor with no extra try/except wrapper.

**Ordering hazard for parallelization**: `merge_repos()` (model.py:279-304)
explicitly re-sorts `decisions` (by `age_hours` desc), `flows`/`sessions`
(by `(repo, issue)`), and `ledger` (by `(repo, issue)`) — so those four are
already order-independent of `per_repo_results`' input order. But
`model.errors`, `model.unattributed`, `model.closure_sweep`,
`model.unapproved_open_prs`, and `model.generated_at_by_repo` are **not**
re-sorted — they're appended/set in `per_repo_results` iteration order.
Today that's `repo_configs` order (deterministic); switching to
`ThreadPoolExecutor.submit()`+`as_completed()` would make these four
nondeterministic run-to-run (fetch-completion order). `.map()` preserves
input order regardless of completion order — a decision point for the
proposal.

No config or CLI timeout knob exists anywhere: `RepoConfig` (config.py:20)
has no timeout field, `load_config` (config.py:35) doesn't read one, and
`cli.py`'s full flag list (`--config`, `--repo`, `--watch`/`--once`,
`--no-color`, `--json`, `serve`'s `--host`/`--port`/`--log`) has nothing
timeout-related. `docs/issue-1/proposals/cli-design.md` §4 already fixed
the 15s default as "configurable later if needed — not v1", and its §8
open-questions list literally flags "whether per-repo `flows --json` calls
should run concurrently... not needed for v1... worth revisiting if it
becomes a bottleneck" — issue #29 is that revisit.

`docs/specs/flows-schema.md` has no timeout-related content at all (grepped
full file) — the 15s value has always been `rsb`'s own operational choice,
not part of the upstream wire contract, so raising it is not a spec
resync.

`webserver.py`'s `_serve_board_json` (webserver.py:46-48) calls
`fetch_board_fn(repo_configs)` fresh on every `/api/board.json` request, no
caching. `ThreadingHTTPServer` (webserver.py:6, 64) already parallelizes
*across concurrent HTTP requests*, but each individual request's fetch
across repos is still the same sequential `fetch_board` call — the
parallelization fix in `fetch.py` benefits `serve` mode for free with no
`webserver.py` changes needed, since it just calls the same `fetch_board_fn`
it's always called.

## 2. Repo `<select>` filter (`web/index.html`, `web/dashboard.js`, `webserver.py`)

No `<select>` exists in `index.html` today. Body structure: `.page` >
`.page-header` (title + `#refresh-button`) > `#partial-banner` >
`#summary-strip` > `#page-body` > (`#main-content`, `#detail-panel-slot`
siblings).

`dashboard.js` has no filter state. The only comparable module-level UI
state is `selectedIssue` (dashboard.js:300), used for the detail panel — a
`selectedRepo` var would follow the same pattern. `renderData(data)`
(dashboard.js:339-401) is the single entry point that both computes
`selectSummary(data)` (dashboard.js:49-73, called at :349) and renders all
five sections (:376-398) from the same unfiltered `data`; none of
`selectSummary`/`decisionRows`/`flowRows`/`sessionRows`/`renderAccounting`/
`renderHygiene`/`renderErrors`/`isPageEmpty` take a repo-scope argument
today. The fetched payload (`data`) is local to `load()`'s try block
(dashboard.js:403-416), not module-scoped — a filter-only re-render (no
refetch) needs it hoisted.

Repo-list source already exists: the union of `data.generated_at_by_repo`
keys and `data.errors[].repo` is exactly what's already computed for
`repoCount` at dashboard.js:346 — reusable as-is for populating `<option>`s.

`--repo NAME` already exists as a **CLI** flag (cli.py:21,
`_select_repos` cli.py:44-50) — but that restricts which repos get
*fetched* server/config-side, a different mechanism from issue #29's
client-side runtime filter (recompute an already-fetched payload without
re-fetching). Worth naming both explicitly in the proposal so they aren't
conflated.

`webserver.py`'s `_serve_board_json` ignores query strings entirely
(webserver.py:41-54, always fetches all `repo_configs`) — issue #29's
requirement 2 is phrased as client-side recompute ("표와 요약 칩이 함께
재계산"), which needs no server change; a server-side `?repo=` param is one
alternative the proposal should explicitly reject rather than silently
skip.

## 3. Repo-first column + table-only horizontal scroll (`dashboard.js`, `dashboard.css`, `render.py`)

Column order per table (`dashboard.js`):
- **Decisions** — already compliant: headers `["Repo","Issue","PR","Phase","Role","Awaiting","Age"]` (:379) match `decisionRows()` (:135-143, repo cell first at :136).
- **Flows** — Repo is **last**: headers `["Issue","Stage","Plan","Roles","PRs","Repo"]` (:383); `flowRows()` cells same order, repo cell at :175.
- **Sessions** — Repo is **last**: headers `["Role","Issue","Elapsed","PID","Alive","Last activity","Repo"]` (:387); `sessionRows()` repo cell at :193.
- **Ledger/Accounting** — Repo is **last**: headers `["Issue","Sessions","Cost","Outcomes","Repo"]` (:210); repo cell at :207.
- **Hygiene**/**Errors** are `<ul>` lists (:217-224, :226-236), not tables — repo is embedded inline at the end of each `<li>` text; not a "column" to reorder, flagged for visual-consistency judgment call only.

All four tables share one renderer, `renderTable(headers, rows,
emptyMessage)` (dashboard.js:120-127) — the fix is per-function header/cell
reordering in each `*Rows()`/`renderAccounting()`, not in `renderTable`
itself; a wrapper added inside `renderTable` would apply to all four for
free (relevant for the scroll-wrapper decision below too).

`render.py` (the CLI **text** renderer, a separate surface from the HTML
dashboard) also puts `repo` last in every `_table()` call
(render.py:76-77, 89-90/97, 108-109/117-118, 131). Issue #29's requirement
3 wording ("모바일", "가로 스크롤") is dashboard/web-specific vocabulary — a
terminal has neither concept — so `render.py` reads as out of scope by the
same "requirement text implies dashboard-only" logic issue #23's proposal
used for `render.py` (its Write-set summary explicitly excluded
`render.py` because touch points named only dashboard files). Confirming
this reading is a Rationale item, not an assumption to leave silent.

**Mobile/scroll**: `dashboard.css` has zero `overflow-x`, no scroll
wrapper around `table.data-table`, and no card-layout CSS — confirmed by
full-file read; the only responsive rule at all is `@media
(max-width: 768px) { .summary-strip { gap: var(--space-2); } }`
(dashboard.css:244-246). `table.data-table` (dashboard.css:139-145) is
`width: 100%` with nothing bounding it — on a narrow viewport today the
table (or the whole page) overflows/squishes, which is the literal bug
requirement 3's "가로 스크롤 안 됨" acceptance criterion is written
against.

Two accepted-spec passages this directly contradicts:
- `docs/specs/design-system.md:147`: "Multi-device/mobile optimization is
  out of scope; the 768px floor exists only so the single screen degrades
  gracefully." Requirement 3 explicitly adds mobile-safe table behavior —
  this line needs updating, not just new code.
- `docs/specs/screen-spec.md`'s breakpoint table (§5, mirrored via
  design-system.md:143-144) documents chip-wrap and detail-panel-mode
  breakpoints but says nothing about table scroll — undesigned territory,
  not a contradiction, but a gap the proposal's spec update needs to fill.

## 4. Failure banner simplification (`dashboard.js`, `dashboard.css`, `screen-spec.md`)

Current partial-banner block in `renderData()` (~dashboard.js:355-368):
builds `${failedRepos.length} of ${total} repos failed to load —
${detail}` where `detail` is every failed repo's `"{repo}: {message}"`
comma-joined and **always inline**, plus a `#partial-retry` button wired to
`load`. Requirement 4 wants the count kept always-visible and the
per-repo detail moved into a collapsed `<details>`.

Separately, `renderFullError(message)` (dashboard.js:105-118, invoked at
:342 when `succeededRepoCount === 0 && errors.length > 0`) joins **all**
error messages with `"; "` for the full-page `ErrorState` — a different
component (`design-system.md` §6 lists `PartialFailureBanner` and
`ErrorState` as distinct entries). The issue text says "실패 배너"
(banner), which per the design-system's own naming is
`PartialFailureBanner` specifically — whether `ErrorState`'s full-page
message list is in scope too is a scope call the proposal needs to state
explicitly rather than leave ambiguous.

`docs/specs/screen-spec.md` §2.5 currently documents, word for word, the
**old** behavior this issue changes: `Copy: "{M} of {N} repos failed to
load — {repo}: {message}(, …)"` — this accepted spec text is exactly what
requirement 4 says to stop doing. It needs a resync in the same PR (same
pattern as issue #23's `flows-schema.md` resync), not just a code change
that silently drifts from an accepted doc.

`dashboard.css`'s `.partial-banner` rules (dashboard.css:179-195) have no
`<details>`/`<summary>` styling to build on or conflict with.

## 5. Accessible row disclosure (`dashboard.js`, `dashboard.css`, `index.html`, `screen-spec.md`)

`renderTable()` (dashboard.js:120-127) stamps every body `<tr>` with
`data-issue`/`data-repo` (:125) — the **whole row** is the click target
across all four `DataTable`s (decisions, flows, sessions, ledger all route
through `renderTable`). `attachRowClickHandlers(data)` (dashboard.js:
330-337), called at the end of `renderData()` (:400), wires
`click` on `tbody tr[data-issue]` → sets `selectedIssue` → re-renders. No
`<button>` exists in any Issue cell — they're plain `<td class="mono">`
(decisions :137, flows :170, sessions :186, ledger :203).
`dashboard.css:151-152` (`tbody tr { cursor: pointer }` + hover) is the row
click affordance that needs replacing with button-specific styling.

Detail-panel placement: `#main-content` and `#detail-panel-slot` are
**siblings** inside `#page-body` (index.html:20-23) — the panel is never
structurally inside/adjacent to the clicked row, it's a separate slot that
always renders after all table content regardless of viewport.
`renderData()` sets `DETAIL_SLOT.innerHTML` unconditionally (:399) — zero
JS branching on breakpoint. CSS (dashboard.css:230-242): `#page-body` is a
1-column grid by default; only `@media (min-width: 1200px) {
#page-body:has(#detail-panel-slot:not(:empty)) { grid-template-columns: 1fr
minmax(280px,340px) } }` switches to a side panel. Below 1200px the panel
falls to the very bottom of the page (after Accounting/Hygiene/Errors),
not below the selected row — the exact gap requirement 5 names.

Important: `docs/specs/screen-spec.md` §1.6 **already** says "Layout choice
resolved: side panel at/above `breakpoint-lg` (1200px), expandable row
below `breakpoint-lg`" — the accepted spec already calls for exactly the
narrow-screen behavior requirement 5 asks for; the code just never
implemented the "expandable row" half, it always uses the fixed bottom
slot. This is a shipped-code-vs-accepted-spec gap, not a new design
decision on *whether* to do this — only on *how* to implement it
structurally. Same shape as issue #23's plan-field spec-drift finding.

Structural complication: all four tables' Issue cells feed the *same*
`selectedIssue`/`DETAIL_SLOT`, and `renderDetailPanel()` already aggregates
decision + flow + session + ledger data for one `(issue, repo)` regardless
of which table was clicked — so a click in any of the four tables opens
the identical aggregated content today. For a below-row expandable
placement, the code needs to know **which table/row** triggered the
selection (to insert the expansion `<tr>` there), something `selectedIssue
= {issue, repo}` doesn't currently carry — a design point the proposal
must resolve (candidates: track which table triggered it and expand only
that row, vs. expand the matching row in every table that has one).

`screen-spec.md` §1.3/§1.4 currently say "Row click opens DetailPanel" —
needs rewording once the trigger is a button, not the row.

## 6. Testing patterns (`test/rsb_tests/`)

Run via `python -m pytest test/` (`docs/handbooks/rsb.md`). All 33 current
tests pass on `main`/this branch tip.

- **`test_fetch.py`**: `run_json_fn` is injected as a plain closure
  (`_fake_run_json`, test_fetch.py:9-15) — no real subprocess, no
  `subprocess.run` monkeypatching anywhere. `fetch_and_normalize_one`/
  `fetch_board` are called directly with the fake. Parallelization tests
  should follow this shape: assert all repos' fakes get invoked despite
  artificial delay (e.g., `time.sleep` inside the fake + wall-clock
  assertion `elapsed < N * sleep_time`) to prove concurrent execution, not
  serial.
- **`test_cli.py`**: monkeypatches `cli.fetch_board` wholesale with
  `lambda repo_configs: ...` (single positional arg) at the module-attribes
  level. Any new parameter threaded through `fetch_board`'s call sites
  (e.g. a timeout) needs every existing `test_cli.py` monkeypatch lambda
  checked for signature compatibility — a ripple to watch, not just a new
  test to add.
- **`test_config.py`**: `load_config`/`resolve_config_path`/`ConfigError`
  assertions against `tmp_path`-written TOML — only relevant if the
  proposal ends up adding a config field (survey leans toward a CLI-only
  flag instead, see §1 above — would keep this file untouched).
- **`test_render.py`**: substring/key assertions against
  `render_text()`/`render_json_model()` output, not snapshot-based. Stays
  untouched under the dashboard-only reading of requirement 3.
- **`test_webserver.py`**: spins a real `ThreadingHTTPServer` on
  `("127.0.0.1", 0)`, hits it via `urllib.request.urlopen`, same
  fake-injection style as `test_fetch.py`. Untouched if requirement 2 stays
  client-side-only (no `?repo=` query param added).
- **`fixtures.py`**: canonical fixture-dict style (`WORKED_EXAMPLE`,
  `EMPTY_PAYLOAD`, etc.); multi-repo composition for cross-repo assertions
  is already demonstrated in `test_model.py` (merging two differently-named
  normalized payloads) — reusable for any filter-related Python-side test
  without new fixtures.
- **No JS test harness** (`test_model.py`'s own comments confirm: no
  `package.json`, no Jest/`node --test` config — explicitly ruled
  out-of-scope by the accepted issue #23 proposal). Existing JS coverage
  works by `node -e`-requiring the real `dashboard.js` with `document`
  stubbed to `{ getElementById: () => null }`, calling only the pure
  functions exported through the `module.exports` guard (dashboard.js:
  `{ ageBucket, ageBucketStatus, selectSummary, isPageEmpty, buildPlanSteps
  }`). Any new pure helper this issue introduces (e.g., a repo-filter
  function operating on the merged payload) should be added to that export
  list to get equivalent coverage; DOM-wiring (the `<select>` `change`
  listener, the new button click handlers, the row-adjacent panel
  insertion) is not testable this way and stays manually verified — same
  precedent `attachRowClickHandlers` itself is under today (also
  untested).

## Write-set summary (what phase 2 will actually touch)

- `src/rsb/fetch.py` — `ThreadPoolExecutor`-based `fetch_board`, raised
  `DEFAULT_TIMEOUT_SECONDS`, timeout threaded from an optional CLI flag.
- `src/rsb/cli.py` — new CLI flag for the timeout override, threaded into
  `_run_once`/`serve`'s `fetch_board`/`run_server` calls.
- `src/rsb/web/index.html` — repo `<select>` in the header; Issue-cell
  buttons come from `dashboard.js`-generated markup, no other structural
  index.html change expected.
- `src/rsb/web/dashboard.js` — filter state + pure filter function
  (exported for node-test coverage), column reordering in
  `flowRows`/`sessionRows`/`renderAccounting`, partial-banner `<details>`
  markup, button-based row toggle replacing `attachRowClickHandlers`,
  narrow-screen expandable-row insertion logic.
- `src/rsb/web/dashboard.css` — scroll wrapper for `table.data-table` (or
  wrapped inside `renderTable`'s output), `<details>`/`<summary>` styling,
  button-based row-toggle affordance replacing the `tbody tr` hover/cursor
  rule.
- `docs/specs/design-system.md` — drop/replace the "mobile optimization
  out of scope" line (§5 area), add a `RepoFilterSelect` (or similar)
  component-inventory entry (§6), note the banner's `<details>` in
  `PartialFailureBanner`'s entry.
- `docs/specs/screen-spec.md` — §1.3/§1.4/§1.5/§1.7 "row click" wording →
  button wording; §2.5 banner copy resync; new subsection for per-table
  horizontal scroll + repo-first column.
- `test/rsb_tests/test_fetch.py` — concurrency + timeout coverage.
- `test/rsb_tests/test_cli.py` — new flag parsing/threading coverage,
  signature-compatibility check across existing `fetch_board` monkeypatch
  lambdas.
- No `src/rsb/config.py`, `src/rsb/model.py`, `src/rsb/webserver.py`,
  `src/rsb/render.py`, or `test/rsb_tests/{test_config,test_model,
  test_render,test_webserver}.py` changes are currently expected — each
  confirmed by full-file read against every requirement above; the
  proposal will restate this explicitly rather than leave it implicit.
