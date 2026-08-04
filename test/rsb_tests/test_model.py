import json
import shutil
import subprocess
from pathlib import Path

import pytest

from rsb.model import PayloadError, merge_repos, normalize_payload

from .fixtures import (
    EMPTY_PAYLOAD,
    MISSING_OWNER_NAME_PAYLOAD,
    PLAN_EMPTY_PAYLOAD,
    PLAN_NULL_PAYLOAD,
    PLAN_STEPS_PAYLOAD,
    RAW_STAGE_PAYLOAD,
    WITH_LAST_ACTIVITY_PAYLOAD,
    WORKED_EXAMPLE,
)


def test_normalize_worked_example():
    normalized = normalize_payload("on-the-record", WORKED_EXAMPLE)
    assert normalized["generated_at"] == "2026-07-31T08:00:00Z"
    assert len(normalized["decisions"]) == 1
    assert normalized["decisions"][0].issue == 172
    assert normalized["decisions"][0].awaiting == "approve-full"
    assert len(normalized["flows"]) == 1
    assert normalized["flows"][0].stage_derived is True
    assert len(normalized["sessions"]) == 1
    assert normalized["sessions"][0].last_activity is None
    assert normalized["ledger"][0].cost_usd_total == 3.14
    assert normalized["unattributed"][0].sessions == 0
    assert len(normalized["closure_sweep"]) == 1
    assert len(normalized["unapproved_open_prs"]) == 1


def test_normalize_empty_sections():
    normalized = normalize_payload("empty-repo", EMPTY_PAYLOAD)
    assert normalized["decisions"] == []
    assert normalized["flows"] == []
    assert normalized["sessions"] == []
    assert normalized["ledger"] == []
    assert normalized["unattributed"] == []
    assert normalized["closure_sweep"] == []
    assert normalized["unapproved_open_prs"] == []


def test_normalize_raw_stage_and_null_last_activity():
    normalized = normalize_payload("raw-stage", RAW_STAGE_PAYLOAD)
    flow = normalized["flows"][0]
    assert flow.stage_derived is False
    assert flow.stage == "some-unmapped-loop-state"
    assert normalized["sessions"][0].last_activity is None
    assert normalized["sessions"][0].alive is False


def test_normalize_last_activity_populated():
    normalized = normalize_payload("last-activity", WITH_LAST_ACTIVITY_PAYLOAD)
    la = normalized["sessions"][0].last_activity
    assert la.kind == "tool_use"
    assert la.detail == "Write roles/data-modeling.json"


def test_normalize_rejects_unsupported_schema_version():
    payload = dict(EMPTY_PAYLOAD, schema_version=2)
    with pytest.raises(PayloadError, match="schema_version=2"):
        normalize_payload("empty-repo", payload)


def test_normalize_rejects_malformed_payload():
    payload = dict(EMPTY_PAYLOAD, decision_queue=[{"issue": 1}])
    with pytest.raises(PayloadError, match="malformed payload"):
        normalize_payload("empty-repo", payload)


def test_merge_repos_sorts_decisions_by_age_descending():
    a = normalize_payload("repo-a", WORKED_EXAMPLE)
    other_payload = dict(WORKED_EXAMPLE)
    other_payload["decision_queue"] = [
        {**WORKED_EXAMPLE["decision_queue"][0], "issue": 999, "pr": 999, "age_hours": 100.0}
    ]
    b = normalize_payload("repo-b", other_payload)

    model = merge_repos([("repo-a", a, None), ("repo-b", b, None)])
    assert [d.age_hours for d in model.decisions] == [100.0, 22.8]


def test_normalize_payload_returns_owner_name_from_repo_field():
    normalized = normalize_payload("on-the-record", WORKED_EXAMPLE)
    assert normalized["owner_name"] == "tokenmaxxxer/on-the-record"


def test_normalize_payload_owner_name_is_none_when_repo_field_absent():
    assert "repo" not in MISSING_OWNER_NAME_PAYLOAD
    normalized = normalize_payload("empty-repo", MISSING_OWNER_NAME_PAYLOAD)
    assert normalized["owner_name"] is None


def test_merge_repos_fills_owner_name_by_repo():
    a = normalize_payload("repo-a", WORKED_EXAMPLE)
    b = normalize_payload("repo-b", MISSING_OWNER_NAME_PAYLOAD)
    model = merge_repos([("repo-a", a, None), ("repo-b", b, None)])
    assert model.owner_name_by_repo == {
        "repo-a": "tokenmaxxxer/on-the-record",
        "repo-b": None,
    }


def test_merge_repos_collects_errors_without_dropping_other_repos():
    a = normalize_payload("repo-a", WORKED_EXAMPLE)
    model = merge_repos([("repo-a", a, None), ("repo-b", None, "flows --json failed: boom")])
    assert len(model.decisions) == 1
    assert len(model.errors) == 1
    assert model.errors[0].repo == "repo-b"
    assert "boom" in model.errors[0].message


# ---- `flows[].plan` normalization (issue #23) --------------------------


def test_normalize_plan_missing_key_is_treated_as_none():
    # Finding #1 (2차 교차 검토): explicit missing-key policy + regression
    # test. WORKED_EXAMPLE's flow predates the `plan` field entirely (the
    # key is absent, not set to `null`) -- this repo's documented policy
    # (see model.py's comment above the `plan=` extraction) is that an
    # absent key normalizes exactly like an explicit `null`: both become
    # `None`, never `[]`.
    normalized = normalize_payload("on-the-record", WORKED_EXAMPLE)
    assert "plan" not in WORKED_EXAMPLE["flows"][0]
    assert normalized["flows"][0].plan is None


def test_normalize_plan_explicit_null_is_none():
    normalized = normalize_payload("plan-null", PLAN_NULL_PAYLOAD)
    assert normalized["flows"][0].plan is None


def test_normalize_plan_empty_list_stays_distinct_from_null():
    normalized = normalize_payload("plan-empty", PLAN_EMPTY_PAYLOAD)
    assert normalized["flows"][0].plan == []


def test_normalize_plan_steps_with_parallel_roles():
    normalized = normalize_payload("plan-steps", PLAN_STEPS_PAYLOAD)
    plan = normalized["flows"][0].plan
    assert len(plan) == 3
    steps_by_number = {p.step: p for p in plan}
    assert steps_by_number[1].roles == ["implementation"]
    assert steps_by_number[1].done is True
    assert steps_by_number[3].roles == ["implementation", "review"]
    assert steps_by_number[3].done is False


# ---- dashboard.js plan/aggregation behavior (issue #23) -----------------
#
# This repo has no JS test harness (no package.json, no jest/mocha config
# — the approved phase-1 proposal explicitly rules out adding one, a
# repo-wide decision out of this issue's scope) and the frozen phase-1
# write set names only test/rsb_tests/test_model.py for new test
# coverage, not a new JS test file. These tests exercise the *actual*
# shipped dashboard.js (not a reimplementation) by shelling out to a
# plain `node` binary directly — no framework, no config file, no new
# dependency — which stays inside both constraints while still giving
# automated regression coverage for findings #2 and #3.

DASHBOARD_JS = Path(__file__).resolve().parents[2] / "src" / "rsb" / "web" / "dashboard.js"


def _run_dashboard_js(script):
    if shutil.which("node") is None:
        pytest.skip("node is not installed; skipping dashboard.js behavior test")
    program = (
        "global.document = { getElementById: () => null };\n"
        "const dashboard = require(%s);\n%s" % (json.dumps(str(DASHBOARD_JS)), script)
    )
    result = subprocess.run(["node", "-e", program], capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, f"node script failed:\n{result.stderr}"
    return json.loads(result.stdout)


def test_dashboard_js_plan_steps_sorted_by_step_number_ascending():
    # Finding #3a: steps display in `step`-number ascending order, not
    # array order.
    flow = PLAN_STEPS_PAYLOAD["flows"][0]
    result = _run_dashboard_js(
        """
        const flow = %s;
        const planData = dashboard.buildPlanSteps(flow, [], flow.issue, %s);
        console.log(JSON.stringify(planData.steps.map((s) => s.step)));
        """
        % (json.dumps(flow), json.dumps(PLAN_STEPS_PAYLOAD["repo"]))
    )
    assert result == [1, 2, 3]


def test_dashboard_js_plan_steps_join_shows_all_pending_prs_not_just_first():
    # Finding #3b: when multiple PRs are open for the same
    # (issue, repo, role), all of them are shown, not just the first.
    flow = PLAN_STEPS_PAYLOAD["flows"][0]
    decisions = PLAN_STEPS_PAYLOAD["decision_queue"]
    repo = PLAN_STEPS_PAYLOAD["repo"]
    decisions_with_repo = [dict(d, repo=repo) for d in decisions]
    result = _run_dashboard_js(
        """
        const flow = %s;
        const decisions = %s;
        const planData = dashboard.buildPlanSteps(flow, decisions, flow.issue, %s);
        const step1 = planData.steps.find((s) => s.step === 1);
        const implRole = step1.roles.find((r) => r.role === "implementation");
        console.log(JSON.stringify(implRole.pendingPrs.map((d) => d.pr).sort()));
        """
        % (json.dumps(flow), json.dumps(decisions_with_repo), json.dumps(repo))
    )
    assert result == [501, 502]


def test_dashboard_js_empty_plan_is_distinct_from_null_plan():
    # Finding #3c: `plan: []` must render as an explicit "0 steps" state,
    # not an empty/blank section indistinguishable from `plan: null`.
    flow_empty = dict(PLAN_EMPTY_PAYLOAD["flows"][0], repo=PLAN_EMPTY_PAYLOAD["repo"])
    flow_null = dict(PLAN_NULL_PAYLOAD["flows"][0], repo=PLAN_NULL_PAYLOAD["repo"])
    result = _run_dashboard_js(
        """
        const empty = dashboard.buildPlanSteps(%s, [], %s, %s);
        const nul = dashboard.buildPlanSteps(%s, [], %s, %s);
        console.log(JSON.stringify({ empty, nul }));
        """
        % (
            json.dumps(flow_empty),
            json.dumps(flow_empty["issue"]),
            json.dumps(flow_empty["repo"]),
            json.dumps(flow_null),
            json.dumps(flow_null["issue"]),
            json.dumps(flow_null["repo"]),
        )
    )
    assert result["empty"] == {"steps": []}
    assert result["nul"] is None


def test_dashboard_js_select_summary_counts_in_progress_and_raw_unmapped_flows():
    # Finding #2 (behavior, corrected wording documented in the record and
    # in dashboard.js's isFlowInProgress comment): "in progress" counts
    # proposal/approved/implementing plus any stage_derived:false (raw,
    # unmapped loop_state) flow, and excludes delivered/closed.
    data = {
        "decisions": [],
        "sessions": [],
        "closure_sweep": [],
        "unapproved_open_prs": [],
        "errors": [],
        "flows": [
            {"stage": "proposal", "stage_derived": True},
            {"stage": "approved", "stage_derived": True},
            {"stage": "delivered", "stage_derived": True},
            {"stage": "closed", "stage_derived": True},
            {"stage": "some-unmapped-state", "stage_derived": False},
        ],
    }
    result = _run_dashboard_js(
        """
        const data = %s;
        console.log(JSON.stringify(dashboard.selectSummary(data).flows.label));
        """
        % json.dumps(data)
    )
    assert result == "3 flows in progress"


def test_dashboard_js_filter_by_repo_narrows_every_section():
    # issue #29 requirement 2 — filterByRepo is a pure, DOM-free helper
    # (module.exports guard, same convention as buildPlanSteps) that
    # narrows an already-fetched payload to one repo with no refetch.
    # Exercise every field it touches across two repos so a regression in
    # any one of them (a forgotten .filter() on a new section, a typo in
    # a repo key) is caught.
    data = {
        "decisions": [{"issue": 1, "repo": "repo-a"}, {"issue": 2, "repo": "repo-b"}],
        "flows": [{"issue": 1, "repo": "repo-a"}, {"issue": 3, "repo": "repo-b"}],
        "sessions": [{"issue": 1, "repo": "repo-a"}, {"issue": 4, "repo": "repo-b"}],
        "ledger": [{"issue": 1, "repo": "repo-a"}, {"issue": 5, "repo": "repo-b"}],
        "unattributed": [{"repo": "repo-a"}, {"repo": "repo-b"}],
        "closure_sweep": [{"repo": "repo-a"}, {"repo": "repo-b"}],
        "unapproved_open_prs": [{"repo": "repo-a"}, {"repo": "repo-b"}],
        "errors": [{"repo": "repo-a", "message": "boom"}, {"repo": "repo-b", "message": "bang"}],
        "generated_at_by_repo": {"repo-a": "2026-08-01T00:00:00Z", "repo-b": "2026-08-02T00:00:00Z"},
    }
    result = _run_dashboard_js(
        """
        const data = %s;
        const filtered = dashboard.filterByRepo(data, "repo-a");
        const unfiltered = dashboard.filterByRepo(data, "");
        console.log(JSON.stringify({ filtered, unfiltered }));
        """
        % json.dumps(data)
    )
    filtered = result["filtered"]
    assert [d["issue"] for d in filtered["decisions"]] == [1]
    assert [f["issue"] for f in filtered["flows"]] == [1]
    assert [s["issue"] for s in filtered["sessions"]] == [1]
    assert [le["issue"] for le in filtered["ledger"]] == [1]
    assert len(filtered["unattributed"]) == 1
    assert len(filtered["closure_sweep"]) == 1
    assert len(filtered["unapproved_open_prs"]) == 1
    assert [e["repo"] for e in filtered["errors"]] == ["repo-a"]
    assert filtered["generated_at_by_repo"] == {"repo-a": "2026-08-01T00:00:00Z"}
    # Falsy repo (e.g. the "All repos" option's value "") returns the data
    # unchanged.
    assert result["unfiltered"] == data


def test_dashboard_js_number_link_html_renders_blue_link_when_owner_name_present():
    # issue #36 requirement 1/2 — the number itself is the `<a>` text,
    # `class="number-link"` (dashboard.css maps this to
    # `color-action-primary-background`, blue at rest).
    result = _run_dashboard_js(
        """
        console.log(JSON.stringify(dashboard.numberLinkHtml("a/b", "issues", 42)));
        """
    )
    assert result == (
        '<a class="number-link" href="https://github.com/a/b/issues/42" '
        'target="_blank" rel="noopener noreferrer">#42</a>'
    )


def test_dashboard_js_number_link_html_falls_back_to_plain_text_without_owner_name():
    # issue #36 requirement 5 (AC4) — no owner/name on record means plain
    # `#<n>` text, never a broken link.
    result = _run_dashboard_js(
        """
        console.log(JSON.stringify(dashboard.numberLinkHtml(null, "issues", 42)));
        """
    )
    assert result == "#42"


def test_dashboard_js_detail_row_html_wraps_content_in_a_tr_with_colspan():
    # issue #38 P1-3 — narrow-screen inline detail row, inserted as a
    # sibling <tr> immediately after the toggled row.
    result = _run_dashboard_js(
        """
        console.log(JSON.stringify(dashboard.detailRowHtml(5, "<div>x</div>")));
        """
    )
    assert result == '<tr class="detail-row"><td colspan="5"><div>x</div></td></tr>'


def test_dashboard_js_collapsible_detail_html_escapes_summary_and_detail():
    # issue #38 P2-6 — summary line + collapsed <details> so internal
    # paths/messages aren't exposed by default; both arguments are escaped.
    result = _run_dashboard_js(
        """
        console.log(JSON.stringify(dashboard.collapsibleDetailHtml("Details", "a/b: boom")));
        """
    )
    assert result == "<details><summary>Details</summary><p>a/b: boom</p></details>"

    escaped = _run_dashboard_js(
        """
        console.log(JSON.stringify(dashboard.collapsibleDetailHtml("<Details>", "<script>alert(1)</script>")));
        """
    )
    assert escaped == (
        "<details><summary>&lt;Details&gt;</summary>"
        "<p>&lt;script&gt;alert(1)&lt;/script&gt;</p></details>"
    )
