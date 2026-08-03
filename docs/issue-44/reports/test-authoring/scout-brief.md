# issue-44 scout brief

Mode: parallel sweep, 4 angles in one turn (jsdom for build-step-free
vanilla-JS testing invoked from a non-JS test runner; pytest-playwright /
browser automation as the DOM-dispatch alternative and how it's wired to
pytest-style suites; DOM-level testing precedent for `aria-expanded`
disclosure-button toggling; require-cache-busting "fresh module against a
fresh DOM per test" pattern). 1 stage total, ~20s wall-clock — all four
angles converged cleanly enough that a deepening round wouldn't move the
recommendation below.

## Must-haves a DOM test harness choice has to clear

- Must load the *actual shipped* `dashboard.js` (not a reimplementation)
  against something implementing real DOM APIs — `querySelector`,
  `addEventListener`, `dispatchEvent` — not a hand-stubbed object;
  jsdom is a real (simulated) DOM implementation for exactly this,
  runs in-process in Node, no browser binary.
- Toggle-state assertions read `aria-expanded` off the button element
  after a dispatched click — this is the field-standard shape (click →
  read the attribute), not a novel test design.
- Fresh module state per test: module-scope `const`s captured at
  `require()` time (survey §2) mean each test needs its own DOM installed
  as `global.window`/`global.document` *before* a `require.cache`-busted
  re-require — `delete require.cache[require.resolve(...)]` (or
  `import-fresh`/`decache`) plus a fresh DOM instance, one pair per test.

## Performance axes the real options compete on

1. **Setup cost / dependency footprint** — jsdom: one npm package,
   installs and requires in milliseconds, no binary download. Playwright:
   installs one or more browser binaries (Chromium/Firefox/WebKit,
   tens-to-hundreds of MB) plus its own driver process per test run.
2. **Speed** — jsdom tests run in-process in the same Node invocation, no
   browser process launch; Playwright's per-test browser-context startup
   is measured in seconds vs jsdom's milliseconds, a real cost across
   dozens of small wiring tests.
3. **What it's actually FOR** — Playwright/browser automation targets
   full user-facing E2E flows and real rendering/layout (screenshot
   regression is its natural fit); jsdom targets exactly this repo's need
   — DOM-wiring/event-listener unit assertions with no layout or paint.

## Adopt / skip

- **Adopt**: jsdom, driven from small per-test Node subprocesses (same
  "subprocess + JSON on stdout" shape `_run_dashboard_js` already uses),
  with the require-cache-bust + fresh-DOM-per-test pattern above.
- **Skip**: Playwright/Selenium-class real-browser automation for this
  issue's wiring-level scope — its footprint and per-test latency are
  the wrong trade for unit-style DOM assertions, and its natural
  strength (real rendering/screenshots) is exactly what issue #44 marks
  out of scope.

## Gap line

Already met: click→attribute-assertion is a well-worn pattern, no new
design needed there; this repo's existing subprocess-JSON test shape
transfers directly, only the DOM implementation underneath changes.
Missing: any DOM implementation at all today (current stub returns
`null`, structurally cannot reach wiring code — survey §3), and any npm
dependency/manifest anywhere in the repo (survey §5) — jsdom would be the
first.

## Sources

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
