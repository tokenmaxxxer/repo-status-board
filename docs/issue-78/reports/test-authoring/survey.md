# Current-state survey — issue #78

## Upstream requirements record

`docs/issue-72/reports/requirements-engineering.md` specifies REQ-72-1..3
with EARS `ubiquitous` pattern and `verification_method: Test`, plus a
selector-scoping constraint carried from an after-proposal hunt finding:
REQ-72-2/3's checks must resolve the declaration against its specific
rule block, never a whole-file substring search. The traceability matrix
already names the intended downstream file:
`test/rsb_tests/test_dashboard_dom.py`, status `drafting` (spec exists,
test does not).

## Fix mechanism traced in `src/`

- `src/rsb/web/dashboard.js:205` — `renderTable()` returns
  `<div class="table-scroll"><table class="data-table">...`. All four
  dashboard tables (decisions/flows/sessions/ledger) route through this
  one function (comment at :201-203 confirms).
- `src/rsb/web/dashboard.css:219` — `.table-scroll { overflow-x: auto;
  width: 100%; }`.
- `src/rsb/web/dashboard.css:412-414` — `#main-content, #detail-panel-slot
  { min-width: 0; }` (comment at :406-411 names this the P1-1 grid-item
  fix).

All three match the requirements doc's cited line numbers exactly — no
drift since issue #72 landed.

## Existing test infrastructure (`test/rsb_tests/test_dashboard_dom.py`)

Already contains the DOM-wiring suite from issue #44 (not this issue's
scope — additive only). Reusable machinery:

- `_run_dom_js(script, fetch_body, html)` — spawns a fresh `node -e`
  subprocess per test with jsdom installed as `global.window`/`document`
  before `require()`-ing `dashboard.js`, so its require-time auto-init DOM
  wiring fires. Returns parsed JSON printed by `script`.
- `_dashboard_html_with_css()` — same DASHBOARD_HTML but with the real,
  shipped `dashboard.css` inlined as `<style>`, used by the existing
  24px-min-box tests (`getComputedStyle` against real CSS, not a stub).
- `_board_payload(**overrides)` — full board.json shape with sane empty
  defaults.
- `pytest.skip` guards for missing `node` / `test/node_modules/jsdom`
  (checked: `test/node_modules/jsdom` exists, `npm install --prefix test`
  already run in this checkout).

No existing test in this file inspects CSS *rules* (as opposed to
resolved `getComputedStyle` on a live element) or `renderTable`'s raw
markup directly — REQ-72-1..3 are new assertion shapes for this file, not
covered by anything already there.

## Design decision: how to satisfy the selector-scoping constraint

Two candidate techniques for REQ-72-2/3, both discussed in the
requirements doc's Given/When/Then:

1. **CSSOM rule lookup** (`document.styleSheets[0].cssRules`, filtered by
   `rule.selectorText === "..."`, then `rule.style.getPropertyValue(...)`)
   — inspects the parsed stylesheet's actual rule structure. A
   declaration on an unrelated selector never matches, by construction
   (this is exactly what the after-proposal hunt finding demanded: reject
   the same declaration on the wrong selector).
2. **`getComputedStyle` on a live element** matching the selector (already
   the pattern `_dashboard_html_with_css()` + the 24px tests use) — also
   selector-correct by construction (cascade resolves per-element), but
   conflates "declared on this selector" with "wins the cascade for this
   element," which is a *stronger*, less precise claim than REQ-72-2/3
   actually make (they assert the declaration exists on the named rule
   block, not that it's the winning computed value — though for these two
   single-purpose rules the two happen to coincide today).

Technique 1 is the closer literal match to the Given/When/Then ("the
`#main-content, #detail-panel-slot` block specifically is inspected");
technique 2 is what the file already has a helper for. Recommendation
(below): technique 1, via CSSOM, run inside the same `node -e` + jsdom
subprocess convention already in the file — no new test infra, no new
dependency (jsdom's `CSSStyleSheet`/`CSSStyleRule` are already present
since jsdom is already a devDependency).

## No design decision open for REQ-72-1

`renderTable`'s markup is a plain string template; a DOM query for
`table.data-table` and its parent `.table-scroll` on each of the four
rendered dashboard tables (via the existing `_run_dom_js` +
`_board_payload` machinery, supplying at least one row per table) is a
direct, unambiguous translation of the Given/When/Then — no alternative
technique to weigh.

## Scout: skipped

Skip condition 2 (scout-directive) applies — the spec leaves no
product-facing or exemplar-comparable design decision open. See "Design
decision: how to satisfy the selector-scoping constraint" above for the
one implementation choice that was open, resolved here rather than via
external scouting.

## Scoping note

`write_scope: ['test/**']` for this role. This survey and the phase-1
proposal are the only writes before approval; no `test/**` edits happen
in phase 1.
