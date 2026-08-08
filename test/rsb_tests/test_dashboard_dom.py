"""DOM-wiring tests for dashboard.js (issue #44).

`test_model.py`'s `_run_dashboard_js` stubs `document` as
`{ getElementById: () => null }` — harmless for the 8 pure functions it
covers, but structurally unable to reach any DOM-wiring code (survey.md
§3): every module-scope element const becomes `null`, and there is no
event system to dispatch against. This module installs a real jsdom DOM
as `global.window`/`global.document` *before* `require()`-ing
dashboard.js, so its require-time auto-init seam (dashboard.js:584-591,
guarded only by `typeof window !== "undefined"`; survey.md §2) actually
wires listeners and calls `load()` against real elements — no `src/**`
change needed.

Each test spawns its own `node -e` subprocess (same convention as
`_run_dashboard_js`), so every test gets a fresh require cache and a
fresh DOM for free; the `delete require.cache[...]` below is defensive
belt-and-suspenders, not load-bearing under this per-test-process
convention (scout-brief.md's fresh-module-per-test must-have).

Traces to issue #44's three minimum-coverage bullets:
- repo-filter `<select>` population (defect #1, issue #29)
- `.row-toggle` click wiring / `aria-expanded` / empty-cell-no-open (defect #2, issue #29)
- `load()` fetches the relative path `api/board.json` (Absent-coverage gap, issue #27 conformance-review)
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

DASHBOARD_JS = Path(__file__).resolve().parents[2] / "src" / "rsb" / "web" / "dashboard.js"
TEST_DIR = Path(__file__).resolve().parents[1]
JSDOM_MODULE = TEST_DIR / "node_modules" / "jsdom"

# Mirrors index.html's seven element ids (survey.md §2) — the DOM shape
# dashboard.js's module-scope consts read via document.getElementById at
# require time.
DASHBOARD_HTML = """<!doctype html><html><body>
<span id="header-meta"></span>
<select id="repo-filter"><option value="">All repos</option></select>
<button id="refresh-button"></button>
<div id="partial-banner"></div>
<div id="summary-strip"></div>
<main id="main-content"></main>
<div id="detail-panel-slot"></div>
</body></html>"""


def _run_dom_js(script, fetch_body='throw new Error("fetch not stubbed");'):
    """Load dashboard.js fresh against a real jsdom DOM, run `script`, return its JSON stdout.

    Same subprocess+JSON-on-stdout contract `_run_dashboard_js` uses
    (test_model.py), with a real DOM (jsdom) installed as
    global.window/document instead of the null-returning stub, so
    dashboard.js's require-time DOM-wiring seam actually fires.
    `script` runs after dashboard.js's auto-init `load()` call has had one
    macrotask tick to settle its fetch-stub-backed promise chain
    (fetch -> res.json -> renderData).
    """
    if shutil.which("node") is None:
        pytest.skip("node is not installed; skipping dashboard.js DOM test")
    if not JSDOM_MODULE.exists():
        pytest.skip("jsdom is not installed; run `npm install --prefix test` first")
    program = """
const { JSDOM } = require("jsdom");

async function main() {
  const dom = new JSDOM(%(html)s, { url: "http://localhost/" });
  global.window = dom.window;
  global.document = dom.window.document;
  global.__fetchCalls = [];
  global.fetch = async function (url) {
    global.__fetchCalls.push(url);
    %(fetch_body)s
  };
  delete require.cache[require.resolve(%(dashboard_path)s)];
  require(%(dashboard_path)s);
  await new Promise((resolve) => setTimeout(resolve, 0));
  %(script)s
}

main().catch((err) => { console.error(err.stack || String(err)); process.exit(1); });
""" % {
        "html": json.dumps(DASHBOARD_HTML),
        "fetch_body": fetch_body,
        "dashboard_path": json.dumps(str(DASHBOARD_JS)),
        "script": script,
    }
    result = subprocess.run(
        ["node", "-e", program], cwd=str(TEST_DIR), capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, f"node script failed:\n{result.stderr}"
    return json.loads(result.stdout)


def _fetch_ok(payload):
    return "return { ok: true, status: 200, json: async () => (%s) };" % json.dumps(payload)


def _board_payload(**overrides):
    payload = {
        "generated_at": "2026-08-03T00:00:00Z",
        "generated_at_by_repo": {},
        "owner_name_by_repo": {},
        "decisions": [],
        "flows": [],
        "sessions": [],
        "ledger": [],
        "unattributed": [],
        "closure_sweep": [],
        "unapproved_open_prs": [],
        "errors": [],
    }
    payload.update(overrides)
    return payload


# ---- repo-filter `<select>` population ----------------------------------
# Traces to defect #1 (issue #29): filterByRepo()/repoList() were
# implemented and exported but never called, so the deployed select never
# got any options. EP axis: repo count (zero / one / multiple, including a
# repo that only appears via `errors` — repoList's succeeded+errored
# union).


def test_repo_filter_options_empty_when_no_repos():
    payload = _board_payload()
    result = _run_dom_js(
        'console.log(JSON.stringify({ options: Array.from(document.getElementById("repo-filter").options).map((o) => o.value) }));',
        fetch_body=_fetch_ok(payload),
    )
    assert result["options"] == [""]


def test_repo_filter_options_populated_for_single_repo():
    payload = _board_payload(generated_at_by_repo={"repo-a": "2026-08-03T00:00:00Z"})
    result = _run_dom_js(
        'console.log(JSON.stringify({ options: Array.from(document.getElementById("repo-filter").options).map((o) => o.value) }));',
        fetch_body=_fetch_ok(payload),
    )
    assert result["options"] == ["", "repo-a"]


def test_repo_filter_options_populated_for_multiple_repos_including_errored():
    payload = _board_payload(
        generated_at_by_repo={"repo-b": "2026-08-03T00:00:00Z"},
        errors=[{"repo": "repo-a", "message": "boom"}],
    )
    result = _run_dom_js(
        'console.log(JSON.stringify({ options: Array.from(document.getElementById("repo-filter").options).map((o) => o.value) }));',
        fetch_body=_fetch_ok(payload),
    )
    assert result["options"] == ["", "repo-a", "repo-b"]


# ---- `.row-toggle` click wiring ------------------------------------------
# Traces to defect #2 (issue #29): the toggle relied on <tr> bubbling with
# no sourceTable on selectedIssue, so aria-expanded/aria-controls were
# permanently wrong. Same issue+repo (7, "repo-a") appears in both
# `decisions` and `flows` to exercise the sourceTable fix directly. EP
# axes: click target (button vs. non-button cell), table identity
# (decisions vs. flows). BVA: re-activating an already-open button.

_ROWS_PAYLOAD = _board_payload(
    generated_at_by_repo={"repo-a": "2026-08-03T00:00:00Z"},
    decisions=[
        {"issue": 7, "repo": "repo-a", "pr": 101, "phase": "review", "role": "implementation", "awaiting": "approve-full", "age_hours": 5.0},
    ],
    flows=[
        {"issue": 7, "repo": "repo-a", "stage": "implementing", "stage_derived": True, "plan": None, "roles": [], "prs": []},
    ],
)


def test_row_toggle_click_opens_detail_and_flips_aria_expanded():
    result = _run_dom_js(
        """
        const decBtn = document.querySelector('.row-toggle[data-table="decisions"][data-issue="7"]');
        const before = decBtn.getAttribute("aria-expanded");
        decBtn.click();
        const after = document.querySelector('.row-toggle[data-table="decisions"][data-issue="7"]');
        console.log(JSON.stringify({
          before,
          afterExpanded: after.getAttribute("aria-expanded"),
          detailHasContent: document.getElementById("detail-panel-slot").innerHTML.trim().length > 0,
        }));
        """,
        fetch_body=_fetch_ok(_ROWS_PAYLOAD),
    )
    assert result["before"] == "false"
    assert result["afterExpanded"] == "true"
    assert result["detailHasContent"] is True


def test_row_toggle_click_on_non_button_cell_does_not_open_detail():
    result = _run_dom_js(
        """
        const firstCell = document.querySelector("main table tbody tr td");
        firstCell.click();
        const decBtn = document.querySelector('.row-toggle[data-table="decisions"][data-issue="7"]');
        console.log(JSON.stringify({
          expanded: decBtn.getAttribute("aria-expanded"),
          detailHasContent: document.getElementById("detail-panel-slot").innerHTML.trim().length > 0,
        }));
        """,
        fetch_body=_fetch_ok(_ROWS_PAYLOAD),
    )
    assert result["expanded"] == "false"
    assert result["detailHasContent"] is False


def test_row_toggle_click_only_affects_its_own_table():
    result = _run_dom_js(
        """
        document.querySelector('.row-toggle[data-table="decisions"][data-issue="7"]').click();
        const decBtn = document.querySelector('.row-toggle[data-table="decisions"][data-issue="7"]');
        const flowBtn = document.querySelector('.row-toggle[data-table="flows"][data-issue="7"]');
        console.log(JSON.stringify({
          decExpanded: decBtn.getAttribute("aria-expanded"),
          flowExpanded: flowBtn.getAttribute("aria-expanded"),
        }));
        """,
        fetch_body=_fetch_ok(_ROWS_PAYLOAD),
    )
    assert result["decExpanded"] == "true"
    assert result["flowExpanded"] == "false"


def test_row_toggle_reactivating_open_button_closes_it():
    result = _run_dom_js(
        """
        const selector = '.row-toggle[data-table="decisions"][data-issue="7"]';
        document.querySelector(selector).click();
        document.querySelector(selector).click();
        console.log(JSON.stringify({
          expanded: document.querySelector(selector).getAttribute("aria-expanded"),
          detailHasContent: document.getElementById("detail-panel-slot").innerHTML.trim().length > 0,
        }));
        """,
        fetch_body=_fetch_ok(_ROWS_PAYLOAD),
    )
    assert result["expanded"] == "false"
    assert result["detailHasContent"] is False


# ---- partial-failure error surface (issue #56 F1) -------------------------
# Traces to issue #38 execution-observation F1's root cause (
# docs/issue-38/reports/execution-observation.md): the prior partial-failure
# assertion was scoped to the banner element alone, so it missed that a
# second, always-visible surface (`renderErrors`, since removed) rendered
# the same raw per-repo message elsewhere in #main-content. The assertion
# below is document-scoped to #main-content itself (not to any one child
# element within it) so a regression anywhere inside it would be caught.


def test_partial_failure_raw_message_absent_from_main_content_and_errors_section_gone():
    payload = _board_payload(
        generated_at_by_repo={"repo-a": "2026-08-03T00:00:00Z"},
        errors=[{"repo": "repo-b", "message": "internal-path-should-not-leak: /srv/provider/internal.py refused"}],
    )
    result = _run_dom_js(
        """
        const mainContent = document.getElementById("main-content");
        console.log(JSON.stringify({
          mainContentHasRawMessage: mainContent.textContent.includes("internal-path-should-not-leak"),
          errorsHeadingExists: Array.from(document.querySelectorAll("h2")).some((h) => h.textContent === "Errors"),
          errorListExists: document.querySelector(".error-list") !== null,
          bannerHasCollapsedMessage: document.getElementById("partial-banner").innerHTML.includes("internal-path-should-not-leak"),
        }));
        """,
        fetch_body=_fetch_ok(payload),
    )
    assert result["mainContentHasRawMessage"] is False
    assert result["errorsHeadingExists"] is False
    assert result["errorListExists"] is False
    assert result["bannerHasCollapsedMessage"] is True


# ---- `load()` fetch path ---------------------------------------------------
# Traces to the Absent-coverage gap (issue #27 conformance-review): no
# test called load() under any path, so a regression to an absolute or
# otherwise-wrong fetch URL would have gone undetected.


def test_load_fetches_relative_board_json_path():
    result = _run_dom_js(
        "console.log(JSON.stringify({ fetchCalls: global.__fetchCalls }));",
        fetch_body=_fetch_ok(_board_payload()),
    )
    assert result["fetchCalls"] == ["api/board.json"]
