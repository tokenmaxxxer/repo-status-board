# issue-44 current-state survey

## 1. what today's `module.exports` guard actually covers

`dashboard.js:593-595`:

```js
module.exports = { ageBucket, ageBucketStatus, selectSummary, isPageEmpty,
  buildPlanSteps, filterByRepo, buildGithubUrl, numberLinkHtml };
```

Exactly these 8 pure/DOM-free helpers get `node -e` coverage via
`test/rsb_tests/test_model.py`'s `_run_dashboard_js` (lines 170-179).
Everything DOM-wiring shaped — `attachRowToggleHandlers`
(`dashboard.js:479-491`), `updateRepoFilterOptions` (`465-472`),
`renderData` (`493-561`), `load` (`563-578`), and the browser-only
auto-init block (`584-591`) — is defined but never exported and never
exercised by any test today. This is the exact gap issue #44 names: three
real wiring defects (repo-filter never populated, row-toggle never wired
to its own click, aria-controls pointing nowhere) and one Absent-coverage
verdict (`load()`'s fetch path) all live inside this unexported region.

## 2. the DOM seam already exists — it just has never been driven

`dashboard.js:3-9` reads seven elements via `document.getElementById(...)`
into module-scope `const`s at **require time**:

```js
const REFRESH_BUTTON = document.getElementById("refresh-button");
const HEADER_META = document.getElementById("header-meta");
const SUMMARY_STRIP = document.getElementById("summary-strip");
const PARTIAL_BANNER = document.getElementById("partial-banner");
const MAIN = document.getElementById("main-content");
const DETAIL_SLOT = document.getElementById("detail-panel-slot");
const REPO_FILTER = document.getElementById("repo-filter");
```

`dashboard.js:584-591`'s auto-init block is guarded only by
`typeof window !== "undefined"`:

```js
if (typeof window !== "undefined") {
  REFRESH_BUTTON.addEventListener("click", load);
  REPO_FILTER.addEventListener("change", () => { ... });
  load();
}
```

This means the seam is **already there** without any `src/**` change:
if a `window`/`document` pair exists in the global scope *before*
`require("dashboard.js")` runs, and the DOM behind `document` has real
elements at the seven ids above, requiring the module will itself (a)
capture live element references, (b) attach both top-level listeners,
and (c) call `load()` once — for free, as a require-time side effect.
`index.html:14-25` confirms the exact element/tag shapes needed:
`<select id="repo-filter">` (with a permanent `<option value="">All
repos</option>` per markup, though `updateRepoFilterOptions` replaces
`innerHTML` wholesale), `<button id="refresh-button">`,
`<span id="header-meta">`, plain `<div>`s for `partial-banner`,
`summary-strip`, `main-content` (actually `<main>`), and
`detail-panel-slot`.

## 3. why the existing `_run_dashboard_js` stub structurally cannot reach any of this

`test_model.py:170-179`'s stub is `global.document = { getElementById: ()
=> null }` — every module-scope const above becomes `null`. That's
harmless for the 8 exported pure functions (none of them read those
consts), which is exactly why this convention has worked fine so far. It
is not survivable for anything DOM-wiring shaped: `attachRowToggleHandlers`
calls `MAIN.querySelectorAll(...)` — `null.querySelectorAll` throws.
`updateRepoFilterOptions` reads `REPO_FILTER.value` — same failure mode.
There is no event system in a plain object stub, so "dispatch a click and
assert on state" (issue #44's core requirement) has no way to happen
through this path at all. This is not a bug in the existing tests; it
confirms the harness gap is structural, not an oversight in test-writing.

## 4. the fetch-path Absent gap

`dashboard.js:566`: `const res = await fetch("api/board.json");` inside
`load()`. `load()` is only ever invoked from the auto-init block
(`590`) or from two click handlers that also only exist inside that
block (`renderFullError`'s retry button, `525`'s partial-retry button).
No test today calls `load()` under any path — confirms issue #27's
conformance-review Absent verdict is still accurate as of this survey.

## 5. repo-wide JS dependency footprint: genuinely zero today

```
$ find . -iname package.json -not -path '*/node_modules/*' -not -path '*/.muster-cache/*'
(no matches)
```

No `package.json`, no lockfile, no `node_modules/`, no bundler/test-runner
config anywhere in the repo. `pyproject.toml` declares zero test-related
dependencies beyond what pytest itself needs (pytest isn't even listed
there; `docs/handbooks/rsb.md:37-41` documents `python -m pytest test/`
as the sole entry point, implying pytest is a pre-existing dev-environment
assumption, not something this repo's own manifest tracks). `node`
(v26.5.1 in this environment) is already an implicit prerequisite for the
existing `_run_dashboard_js` tests, which `pytest.skip()` gracefully if
`shutil.which("node") is None` (`test_model.py:171-172`) — that
graceful-degradation convention is worth preserving for any new harness.

## 6. `.gitignore` has no JS-tooling entries yet

Current full contents:

```
.venv/
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
```

No `node_modules/` entry exists because nothing has ever installed one.
If a harness introduces an npm dependency anywhere under `test/`, a
`node_modules/`-ignoring entry becomes necessary — `.gitignore` sits at
repo root, outside this role's `test/**` write scope, so this is flagged
here as a small, low-risk companion change the phase-2 session (or a
one-line hand-off) will need, not something decided or made in this
phase-1 pass.

## 7. where npm tooling could live without leaving `test/**`

Node resolves `node_modules` by walking up from the requiring script's
directory. A `package.json` (and its `node_modules/`) placed at
`test/` (e.g. `test/package.json`) would be found by `require()` calls
from any script under `test/rsb_tests/` or a new `test/js/` directory,
without needing anything at repo root except the `.gitignore` entry
above. This keeps the dependency-manifest addition itself inside
`test/**`.

## 8. prior-art tone check

`docs/issue-29/proposals/implementation.md`,
`docs/issue-34/proposals/implementation.md`, and
`docs/issue-36/proposals/implementation.md` all use a
Request/Constraints/Rationale/What-will-be-done/Out-of-scope/
How-you'll-know-it-worked shape, not literal ADR headers. This phase-1
task explicitly asks for ADR shape (Context/Decision/Alternatives
considered/Consequences/Status) instead — an intentional, one-off
deviation from those prior docs' template, not a house-style change.

## 9. approvers (context only, not actionable this phase)

`docs/specs/approvers.md`: `JiwonJung94`, `jjongkwann`.

## gaps this survey leaves for scout to aim at

- Whether jsdom (or an equivalent) is actually the field-standard way to
  get a "real DOM implementation" for event-dispatch assertions in a
  Node process with no browser binary, versus reaching for
  Playwright/Selenium-class browser automation instead — and how each
  option's footprint/setup cost compares.
- Field precedent for the require-cache-busting "fresh module against a
  fresh DOM, per test" pattern this repo's require-time seam (§2 above)
  depends on.
- Field precedent for asserting `aria-expanded` toggle state at the DOM
  level (click dispatch → attribute assertion), to confirm the test
  design below matches how the ecosystem actually writes this class of
  test.
