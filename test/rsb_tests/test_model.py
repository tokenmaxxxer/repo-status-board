import pytest

from rsb.model import PayloadError, merge_repos, normalize_payload

from .fixtures import EMPTY_PAYLOAD, RAW_STAGE_PAYLOAD, WITH_LAST_ACTIVITY_PAYLOAD, WORKED_EXAMPLE


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


def test_merge_repos_collects_errors_without_dropping_other_repos():
    a = normalize_payload("repo-a", WORKED_EXAMPLE)
    model = merge_repos([("repo-a", a, None), ("repo-b", None, "flows --json failed: boom")])
    assert len(model.decisions) == 1
    assert len(model.errors) == 1
    assert model.errors[0].repo == "repo-b"
    assert "boom" in model.errors[0].message
