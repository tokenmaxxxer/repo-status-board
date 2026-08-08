# Phase 2 record — issue #78 test-authoring

## What was done

Added three tests to `test/rsb_tests/test_dashboard_dom.py` (no existing
test modified or removed), implementing REQ-72-1..3 from
`docs/issue-72/reports/requirements-engineering.md`:

- `test_req_72_1_all_four_dashboard_tables_have_table_scroll_parent` —
  DOM check that all four rendered `.data-table` elements
  (decisions/flows/sessions/ledger) have a `.table-scroll` parent.
- `test_req_72_2_table_scroll_rule_declares_overflow_x_auto` — CSSOM
  lookup (`document.styleSheets[0].cssRules`, filtered by
  `selectorText === ".table-scroll"`) asserting `overflow-x: auto` on
  that rule specifically.
- `test_req_72_3_main_content_and_detail_panel_slot_rule_declares_min_width_zero`
  — CSSOM lookup on `selectorText === "#main-content, #detail-panel-slot"`
  asserting `min-width: 0`.

Both CSS tests load `_dashboard_html_with_css()` (real shipped
`dashboard.css` inlined) and resolve the declaration against its own
parsed rule block, never a whole-file substring search — the technique
REQ-72-2/3's Given/When/Then names explicitly.

Also ran `npm install --prefix test` (jsdom was not yet installed in this
checkout), which is what let the new tests execute rather than skip.

## Why

Per the approved proposal (`docs/issue-78/proposals/test-authoring.md`):
REQ-72-1's partition is table count, covered by exercising all four
tables in one payload — the boundary the requirement text itself sets.
REQ-72-2/3's partition is "declaration present on the correct selector
vs. present-but-on-the-wrong-selector vs. absent"; CSSOM rule lookup is
the only technique among those surveyed that distinguishes all three
(`getComputedStyle` was considered and rejected as asserting a strictly
stronger, cascade-resolved claim than the requirement text makes).

## Upstream / basis

- `docs/issue-72/reports/requirements-engineering.md` (REQ-72-1..3)
- `docs/issue-78/proposals/test-authoring.md` (approved)
- `docs/issue-78/reports/test-authoring/survey.md`

## Suite architecture note

These are unit-level tests at the bottom of the test pyramid: each
exercises `dashboard.js` in isolation against a stubbed `fetch` and an
in-process jsdom DOM, with no server, network, or `src/rsb/web` HTTP
layer involved. The three tests live in the existing
`test_dashboard_dom.py` module rather than a new file, reusing its
jsdom-subprocess-per-test convention (`_run_dom_js`) — consistent with
the module's existing isolation strategy across its issue-#44/#56/#62
test groups.

## Fixture strategy

Fresh-fixture per test: each test spawns its own `node -e` subprocess
via `_run_dom_js`, giving it a fresh `require` cache and a fresh jsdom
DOM — no state or fixture is shared across tests. No new fixtures were
added; the three tests reuse `_run_dom_js`, `_dashboard_html_with_css`,
and `_board_payload` as surveyed in phase 1, with the CSS tests passing
`html=_dashboard_html_with_css()` the same way the existing 24px-min-box
tests do.

## Smell list

No test smells (Meszaros) found in the three added tests: each is a
single-assertion-concern test (Eager Test avoided — `test_req_72_1`
asserts one fact pair, count and wrapping, not the whole render tree),
no Mystery Guest (all payload data is inline in `_REQ72_PAYLOAD`), and no
Interacting Tests (fresh-fixture-per-test rules out Test Run War /
shared-state smells, per the fixture strategy above).

## Test-design technique and traceability

Equivalence Partitioning / Boundary-Value Analysis at the REQ level:
`test_req_72_1_all_four_dashboard_tables_have_table_scroll_parent`
(traces REQ-72-1) partitions on table count — boundary: all four
dashboard tables, per the requirement's own text.
`test_req_72_2_table_scroll_rule_declares_overflow_x_auto` (traces
REQ-72-2) and `test_req_72_3_main_content_and_detail_panel_slot_rule_declares_min_width_zero`
(traces REQ-72-3) partition on declaration-on-correct-selector /
on-wrong-selector / absent, with the CSSOM technique chosen because it
is the only one of those surveyed that distinguishes all three classes.

Traceability, verified via `grep -r "REQ-72-" test/`:

- REQ-72-1 → `test_req_72_1_all_four_dashboard_tables_have_table_scroll_parent`
- REQ-72-2 → `test_req_72_2_table_scroll_rule_declares_overflow_x_auto`
- REQ-72-3 → `test_req_72_3_main_content_and_detail_panel_slot_rule_declares_min_width_zero`

## Verification run

- `python3 -m pytest test/rsb_tests/test_dashboard_dom.py -q` — 15 passed
  (3 new, none skipped).
- `python3 -m pytest test/ -q` — 80 passed, full suite.
- `git diff --stat` on the phase-2 commit is additive-only under `test/`.
- Before-landing warrant-hunter dispatch (stance: rule-cancellation),
  120s cap: NO FINDING — recorded in
  `docs/reports/2026-08-09-hunt-test-authoring.md`.

## What did not work

- Initial `_REQ72_PAYLOAD` used wrong field names for `sessions`
  (`elapsed_hours` instead of `elapsed_min`) and `ledger`
  (`cost`/string `outcomes` instead of `cost_usd_total`/dict `outcomes`),
  which made `renderData` throw and `MAIN.innerHTML` render an
  error-state instead of the four tables — `test_req_72_1` initially saw
  `tableCount: 0`. Fixed by matching the field names `sessionRows`/
  `renderAccounting` actually read.
- The `min-width: 0` assertion initially failed because jsdom's CSSOM
  normalizes the value to `"0px"`, not `"0"` — widened the assertion to
  accept either.

## Open findings

None.

## kind / loop_state

kind: report
loop_state: landed
