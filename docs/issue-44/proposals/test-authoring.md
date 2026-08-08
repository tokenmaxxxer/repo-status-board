# ADR: DOM-layer test harness for `dashboard.js` (issue #44 phase 1)

files:
- test/rsb_tests/test_model.py (existing `_run_dashboard_js` convention)
- src/rsb/web/dashboard.js (subject under test, read-only this phase)
- src/rsb/web/index.html (element ids the harness's DOM must replicate)
- docs/handbooks/rsb.md (documentation target, phase 2)

## What was asked

Issue #44: `dashboard.js`'s DOM-wiring/side-effect layer has zero test
coverage — only pure functions get `node -e` coverage via
`test_model.py`'s `_run_dashboard_js`. Three real wiring defects shipped
through this gap (repo-filter `<select>` never populated — issue #29;
row-toggle relying on `<tr>` bubbling with no `sourceTable`, so
`aria-expanded`/`aria-controls` were permanently wrong — issue #29;
mobile overflow — issue #38 P1-1), plus one independent Absent-coverage
verdict on `load()`'s `fetch("api/board.json")` path (issue #27
conformance-review). Requirements: (1) introduce a DOM-layer harness that
loads `dashboard.js` against a real DOM, dispatches events, and asserts
on resulting state; (2) minimum coverage reproducing the repo-filter
population gap, the row-toggle `aria-expanded`/empty-cell-no-open
behavior, and the `load()` fetch-path gap; (3) document usage so future
verification sessions stop building one-off throwaway scripts
(`.tmp-verify/pptr/verify.js`, `tmp-verify-issue-36.js`,
`tmp-selfcheck-issue-36.js`, `.smoke-tmp/`); (4) decide the fate of
`_run_dashboard_js`. Out of scope per the issue body: visual/screenshot
regression, a CI test gate, and any `src/**` change (this role's write
scope is `test/**` only — a required export would be a hand-off, not
something made here). This phase (phase 1) delivers research + survey +
this proposal only; no test code, no `src/**` touch, no
`docs/issue-44/reports/test-authoring.md` record until an approval lands.

## Survey pointer

Full detail: `docs/issue-44/reports/test-authoring/survey.md`. Key
findings this decision leans on:

- §1: `dashboard.js`'s `module.exports` guard exports exactly 10
  pure/DOM-free helpers (`f353910` added `detailRowHtml`,
  `collapsibleDetailHtml` after this bullet was first written); every
  DOM-wiring function (`attachRowToggleHandlers`, `updateRepoFilterOptions`,
  `renderData`, `load`, the browser-only auto-init block) is unexported
  and untested today.
- §2: the auto-init block's `typeof window !== "undefined"` guard
  (`dashboard.js:658-665`) is already a usable test seam — if a
  `window`/`document` pair exists before `require("dashboard.js")` runs,
  requiring the module itself wires both top-level listeners and calls
  `load()` once, with no new export needed.
- §3: the existing `_run_dashboard_js` stub
  (`global.document = { getElementById: () => null }`) is not a DOM
  implementation and structurally cannot reach any DOM-wiring code —
  this is why the gap exists, not an oversight in test-writing.
- §5/§7: the repo has zero JS dependencies today; a `package.json` (and
  its `node_modules/`) placed at `test/package.json` stays inside this
  role's `test/**` write scope, since Node resolves `node_modules` by
  walking up from the requiring script's directory.
- §6: a `.gitignore` line for `node_modules/` is needed and sits outside
  `test/**` — flagged as a small companion hand-off, not made this phase.

## Adopted methodology

**Harness: jsdom**, driven from small per-test Node subprocesses,
entered through the existing `python -m pytest test/` command (no new
documented entry point):

- New file `test/package.json` declares `jsdom` as the sole dependency
  (`test/node_modules/` installed alongside, `.gitignore`d per the
  hand-off note above).
- New test file `test/rsb_tests/test_dashboard_dom.py`, sibling to
  `test_model.py`, holding a new helper (parallel to, not replacing,
  `_run_dashboard_js`) that: builds a minimal HTML string matching
  `index.html`'s seven element ids (`refresh-button`, `header-meta`,
  `summary-strip`, `partial-banner`, `main-content`, `detail-panel-slot`,
  `repo-filter`), constructs `new JSDOM(html, { url: "http://localhost/" })`,
  installs `global.window`/`global.document`, stubs `global.fetch` as a
  spy, deletes `dashboard.js` from `require.cache`, then `require()`s it
  fresh — same "subprocess + JSON on stdout, parsed and asserted from
  Python" contract `_run_dashboard_js` already uses, with a real DOM
  underneath instead of a null-stub.
- Same graceful-degradation convention as `_run_dashboard_js`
  (`pytest.skip()` if `node` isn't on `PATH`): the new helper also skips
  if `test/node_modules/jsdom` isn't resolvable, so an environment that
  hasn't run the one-time `npm install --prefix test` doesn't hard-fail
  the suite.
- `_run_dashboard_js`/`test_model.py` are **kept as-is, not migrated**.
  Its 8 tests target pure functions that never read the DOM-element
  consts, so routing them through jsdom would add setup cost for zero
  coverage benefit. This narrows, rather than reverses, issue-23's "no
  JS harness" ruling: that ruling stays correct for pure-function
  testing and is superseded only for the DOM-wiring class of test issue
  #44 identifies as uncovered.
- The DOM-seam gap is resolved **without any `src/**` change** — see
  Survey pointer §2. Tests drive behavior by dispatching real DOM events
  against elements the fresh `require()` wired up (via the existing
  `typeof window !== "undefined"` guard), and assert on resulting DOM
  state, never by calling a newly-exported function.

## Rationale

**Why jsdom, not headless-browser automation (Playwright/Selenium).**
Scout-brief (`docs/issue-44/reports/test-authoring/scout-brief.md`) found
all four researched angles converging on the same shape: jsdom is an
in-process, no-binary DOM implementation built for event-wiring
assertions with no layout/paint involved, while Playwright/Selenium-class
tools target real rendering and full user-flow E2E at the cost of a
browser-binary install and per-test browser-context startup latency real
enough to matter across dozens of small wiring tests. Issue #44
explicitly puts visual/screenshot regression out of scope — exactly the
use case that would justify paying a browser-automation tool's footprint
— so nothing here needs what Playwright is actually good at.

**New runtime dependency footprint — justification.** `jsdom` (npm),
scoped to `test/package.json`, is this repo's first JS dependency of any
kind. AC1 requires loading `dashboard.js` "against a real DOM
implementation, dispatch events, and assert on resulting state" — the
existing null-returning stub cannot be extended into that without
re-implementing a DOM (i.e., becoming jsdom in substance if not in
name). jsdom is the field-standard, lowest-footprint way to get a real
DOM in a Node process with no browser binary. Its cost is confined to
`test/node_modules/` (dev/test-only, never shipped, never touches
`src/**` or the deployed static bundle) and is gated by the same
skip-if-missing pattern already used for `node` itself.

**Entry point stays `python -m pytest test/`.** The one-time
`npm install --prefix test` prerequisite is analogous to `node` itself
already being an implicit, skip-gated prerequisite — documented (phase
2), not a second test entry point, reconciling with the handbook's
single documented command.

**Alternatives considered and rejected:**
- *Headless-browser automation for this scope* — rejected; its natural
  strength (real rendering/screenshots) is exactly what issue #44 marks
  out of scope, and its footprint/latency is the wrong trade for
  wiring-level unit assertions. Left on the table as the right tool if a
  future issue reintroduces visual regression testing.
- *Migrating `_run_dashboard_js`'s existing tests onto jsdom* — rejected;
  they never touch the DOM consts, so moving them gains nothing and adds
  jsdom startup cost to tests that currently need none of it.
- *Exporting DOM-wiring functions from `dashboard.js` to bypass the
  auto-init/require-time seam* — rejected for this phase; it would touch
  `src/**` (outside this role's write scope) and survey §2 shows it
  isn't necessary — the existing browser-guard already provides a
  working seam once a jsdom DOM exists before `require()`. Noted below
  as an optional (not blocking) future simplification.
- *Hand-rolling a minimal DOM stub with just enough surface
  (`addEventListener`, fake `querySelectorAll`/event dispatch) instead of
  adopting jsdom* — rejected; this is substantially the same scope of
  work jsdom already solved, tested, and maintained — hand-rolling it
  would mean maintaining an ad-hoc, under-tested DOM implementation
  ourselves, the opposite of "zero footprint" in effort even if the
  dependency *count* stayed at zero.

## Plugin reflection plan

Phase-2 test design will apply this rulebook's named testing-methodology
conventions explicitly, not just in spirit:

- **EP/BVA framing** — every phase-2 suite below states its Equivalence
  Partitioning axis up front (repo count for the filter suite; click
  target and cross-table identity for the toggle suite) plus one
  Boundary Value Analysis case (re-activating an already-open toggle).
- **Traceability line** — each suite carries a one-line "traces to"
  pointer back to the specific issue #44 requirement/defect it
  reproduces (see the numbered list below), so the mapping from test to
  historical incident is explicit rather than implied.
- **xUnit-style suite shape** — the new DOM suite is added as plain
  pytest test functions in a new module (`test_dashboard_dom.py`), same
  shape as `test_model.py`'s existing functions; no new test framework,
  no class-based fixtures beyond what pytest itself already provides,
  keeping the addition consistent with this repo's existing xUnit-style
  pytest suite rather than introducing a second test-organization
  convention.
- **ADR-proposal-shape** — this document itself follows the required
  section set (What was asked / Survey pointer / Adopted methodology /
  Rationale / Plugin reflection plan / Deliberately out of scope), with
  Alternatives/Consequences/Status folded in as the remaining ADR
  content the phase-1 task also asked for.

## Phase-2 test list (concrete, 1:1 with issue #44's minimum-coverage bullets)

1. **Repo-filter `<select>` population** — traces to defect #1 (issue
   #29's `filterByRepo`/`repoList` implemented but never called). EP
   axis: repo count — zero repos (empty `generated_at_by_repo` +
   `errors`), one repo, multiple repos. Stub `fetch` to resolve a board
   payload per partition, require fresh against the jsdom DOM, await
   `load()` settling, assert `#repo-filter`'s `<option>` values match
   `repoList(data)`'s union of succeeded + errored repos. This is the
   test that would have failed under the actual issue #29 shipped state.

2. **Row-toggle click wiring** — traces to defect #2 (toggle relying on
   `<tr>` bubbling; `selectedIssue` had no `sourceTable`, so
   `aria-expanded`/`aria-controls` were permanently wrong). EP axis:
   click target — (a) click directly on a `.row-toggle` button →
   `aria-expanded` flips to `"true"`, detail panel renders; (b) click on
   the row's other, non-button cell content (the "empty cell" case) →
   `aria-expanded` stays `"false"`, detail panel does not open — the
   direct regression test for "relies on `<tr>` bubbling", since the
   listener now binds to `.row-toggle` only. Second EP axis: two
   different tables showing the same issue number — only the toggled
   table's own button reports `aria-expanded="true"`, exercising the
   `sourceTable` fix directly. BVA case: activating the same,
   already-open button a second time flips `aria-expanded` back to
   `"false"` (closes).

3. **`load()` fetches the relative path `api/board.json`** — traces to
   the Absent-coverage gap (issue #27 conformance-review verdict).
   Install a `global.fetch` spy before require, trigger the auto-init
   `load()` call, assert the spy was invoked with exactly the string
   `"api/board.json"` — not an absolute URL, not a different path.

**Note on the mobile-overflow defect (background item #3, issue #38
P1-1):** intentionally **not** in this list. jsdom does not implement
layout — computed widths/`getBoundingClientRect` are not meaningful in
it — so a DOM-wiring harness structurally cannot detect a CSS-overflow
regression regardless of test count. Measuring rendered content width at
a viewport is exactly the "visual/screenshot regression" class of test
issue #44 marks out of scope; the issue's own minimum-coverage bullet
list (three items) already excludes it, even though the background names
three historical defects plus the Absent gap.

## Documentation plan

`docs/handbooks/rsb.md`'s "Tests" section currently documents only
`python -m pytest test/`. Phase 2 will add: the one-time `npm install
--prefix test` prerequisite, a one-line description of what the new DOM
harness covers and where (`test/rsb_tests/test_dashboard_dom.py`), and an
explicit statement that future verification/smoke-check sessions should
extend this harness rather than build a new one-off script — directly
addressing requirement 3's "replace the throwaway scripts". This edit is
**not** made in this phase-1 pass: `docs/handbooks/rsb.md` is outside
both `test/**` and `docs/issue-44/**`, so it is described here as the
plan and executed in phase 2, once approved.

## Deliberately out of scope

- Any `src/**` change (this role's write scope is `test/**` only) — the
  DOM-seam gap is resolved without one; see Rationale's rejected
  alternative on exporting DOM-wiring functions.
- Visual/screenshot regression testing, including the mobile-overflow
  defect (issue #38 P1-1) — see the note under "Phase-2 test list";
  jsdom cannot detect it, and it is explicitly out of issue #44's scope.
- Adding a CI test gate — issue #44 marks this a separate future
  decision.
- Migrating `_run_dashboard_js`'s existing pure-function tests onto
  jsdom — see Rationale; kept as-is, new suite added alongside.
- Writing any test code, `test/package.json`, the `.gitignore`
  hand-off, or the `docs/handbooks/rsb.md` update itself — all phase-2,
  gated on approval.
- This role's final record, `docs/issue-44/reports/test-authoring.md` —
  phase-2-only per the role-handoff contract; not created this phase.

## Consequences

- First JS runtime dependency this repo has ever had (`jsdom`, dev/test
  scope only) — confined to `test/node_modules/`, never reaches `src/**`
  or the deployed static bundle.
- A `.gitignore` line for `test/node_modules/` is needed and is flagged
  as a small hand-off (outside `test/**`) rather than made this phase.
- `_run_dashboard_js`/`test_model.py` unchanged — zero regression risk to
  the 8 existing pure-function tests; the new DOM suite is fully
  additive in a new file.
- `python -m pytest test/` remains the single documented entry point;
  the only new operational step is a one-time `npm install --prefix
  test`, itself skip-gated like the existing `node` prerequisite.
- Mobile-overflow (issue #38 P1-1) remains untested by this harness by
  design — a future, explicitly-scoped visual-regression effort (out of
  scope here) would be the right place for it.

## Status

Proposed, awaiting approval. Phase 2 (writing the actual test code,
`test/package.json`, the `.gitignore` hand-off, the `docs/handbooks/rsb.md`
update, and this role's final record at
`docs/issue-44/reports/test-authoring.md`) does not begin until an
approval lands on issue #44 per this repo's role-handoff contract.

## Sources

Web sources consulted during scouting (full annotated list in
`docs/issue-44/reports/test-authoring/scout-brief.md`):

Sources:
- [JSDOM – Browser-Like DOM for Node.js Apps](https://jsdom.org/)
- [Testing DOM code with jsdom in Node.js: a tutorial | JSGuides](https://jsguides.dev/tutorials/testing-javascript/testing-dom-jsdom/)
- [Frontend testing in Node with jsdom | oliverjam.com](https://oliverjam.es/articles/frontend-testing-node-jsdom)
- [jsdom vs Playwright | What are the differences? | StackShare](https://stackshare.io/stackups/jsdom-vs-playwright)
- [Using pytest and Playwright to test a JavaScript web application | Simon Willison's TILs](https://til.simonwillison.net/pytest/playwright-pytest)
- [Pytest Plugin Reference | Playwright Python](https://playwright.dev/python/docs/test-runners)
- [How to toggle aria-expanded and other WAI-ARIA values with JavaScript — David MacDonald](https://www.davidmacd.com/blog/toggle-aria-expanded-javascript.html)
- [Is there a way to reset the jsdom instance between each test in order to test a router? — vitest-dev/vitest Discussion #2383](https://github.com/vitest-dev/vitest/discussions/2383)
- [import-fresh — sindresorhus](https://github.com/sindresorhus/import-fresh)
- [decache — dwyl](https://github.com/dwyl/decache)

Internal: `docs/issue-44/reports/test-authoring/survey.md`,
`docs/issue-44/reports/test-authoring/scout-brief.md`.
