import json

from rsb.config import RepoConfig
from rsb.fetch import fetch_and_normalize_one, fetch_board

from .fixtures import EMPTY_PAYLOAD, WORKED_EXAMPLE


def _fake_run_json(payload_text_or_exc):
    def _run(repo_config):
        if isinstance(payload_text_or_exc, Exception):
            raise payload_text_or_exc
        return payload_text_or_exc

    return _run


def test_fetch_and_normalize_one_success():
    repo = RepoConfig(name="on-the-record", path="/x", command=["python", "spawn.py"])
    result = fetch_and_normalize_one(repo, _fake_run_json(json.dumps(WORKED_EXAMPLE)))
    repo_name, normalized, error = result
    assert repo_name == "on-the-record"
    assert error is None
    assert len(normalized["decisions"]) == 1


def test_fetch_and_normalize_one_subprocess_failure():
    repo = RepoConfig(name="broken", path="/x", command=["python", "spawn.py"])
    result = fetch_and_normalize_one(repo, _fake_run_json(RuntimeError("flows --json failed: exit 1")))
    _, normalized, error = result
    assert normalized is None
    assert "exit 1" in error


def test_fetch_and_normalize_one_unparseable_json():
    repo = RepoConfig(name="broken-json", path="/x", command=["python", "spawn.py"])
    result = fetch_and_normalize_one(repo, _fake_run_json("not json {"))
    _, normalized, error = result
    assert normalized is None
    assert "unparseable" in error


def test_fetch_and_normalize_one_schema_mismatch():
    payload = dict(EMPTY_PAYLOAD, schema_version=99)
    repo = RepoConfig(name="future-schema", path="/x", command=["python", "spawn.py"])
    result = fetch_and_normalize_one(repo, _fake_run_json(json.dumps(payload)))
    _, normalized, error = result
    assert normalized is None
    assert "schema_version=99" in error


def test_fetch_board_merges_multiple_repos_partial_failure():
    repos = [
        RepoConfig(name="on-the-record", path="/a", command=["python", "spawn.py"]),
        RepoConfig(name="empty-repo", path="/b", command=["python", "spawn.py"]),
    ]

    def run_json(repo_config):
        if repo_config.name == "on-the-record":
            return json.dumps(WORKED_EXAMPLE)
        return json.dumps(EMPTY_PAYLOAD)

    model = fetch_board(repos, run_json)
    assert len(model.decisions) == 1
    assert len(model.errors) == 0
