import json

from rsb.model import merge_repos, normalize_payload
from rsb.render import render_json_model, render_text

from .fixtures import EMPTY_PAYLOAD, WORKED_EXAMPLE


def _model(payload, repo_name="on-the-record"):
    normalized = normalize_payload(repo_name, payload)
    return merge_repos([(repo_name, normalized, None)])


def test_render_text_contains_section_headers_and_data():
    model = _model(WORKED_EXAMPLE)
    text = render_text(model, "2026-07-31T08:00:00Z")
    for header in ["DECISION QUEUE", "FLOWS", "SESSIONS", "ACCOUNTING", "HYGIENE"]:
        assert header in text
    assert "172" in text
    assert "approve-full" in text
    assert "implementing" in text
    assert "closure-sweep" in text
    assert "unapproved-pr" in text
    assert "ERRORS" not in text


def test_render_text_empty_sections_render_as_none():
    model = _model(EMPTY_PAYLOAD, repo_name="empty-repo")
    text = render_text(model, "2026-07-31T08:00:00Z")
    assert text.count("(none)") == 5


def test_render_text_shows_errors_section_when_present():
    model = merge_repos([("broken-repo", None, "flows --json failed: boom")])
    text = render_text(model, "2026-07-31T08:00:00Z")
    assert "ERRORS" in text
    assert "boom" in text


def test_render_json_model_is_serializable_and_matches_data():
    model = _model(WORKED_EXAMPLE)
    payload = render_json_model(model, "2026-07-31T08:00:00Z")
    text = json.dumps(payload)
    parsed = json.loads(text)
    assert parsed["decisions"][0]["issue"] == 172
    assert parsed["flows"][0]["stage_derived"] is True
    assert parsed["errors"] == []
