import concurrent.futures
import json
import subprocess
import time

from rsb.config import RepoConfig
from rsb.fetch import DEFAULT_TIMEOUT_SECONDS, fetch_and_normalize_one, fetch_board

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


def test_default_timeout_seconds_is_60():
    assert DEFAULT_TIMEOUT_SECONDS == 60


def test_fetch_board_runs_repos_in_parallel():
    repos = [
        RepoConfig(name=f"repo-{i}", path="/x", command=["python", "spawn.py"])
        for i in range(4)
    ]
    sleep_seconds = 0.2

    def run_json(repo_config):
        time.sleep(sleep_seconds)
        return json.dumps(EMPTY_PAYLOAD)

    start = time.monotonic()
    fetch_board(repos, run_json)
    elapsed = time.monotonic() - start

    # Sequential would take ~4 * sleep_seconds; parallel should be well under.
    assert elapsed < sleep_seconds * len(repos) * 0.75


def test_fetch_board_result_order_matches_repo_configs_order():
    repos = [
        RepoConfig(name=f"repo-{i}", path="/x", command=["python", "spawn.py"])
        for i in range(5)
    ]

    def run_json(repo_config):
        idx = int(repo_config.name.split("-")[1])
        # Reverse the completion order relative to input order: the first
        # repo sleeps longest, the last sleeps least.
        time.sleep(0.05 * (len(repos) - idx))
        raise RuntimeError(f"boom-{idx}")

    model = fetch_board(repos, run_json)

    assert [e.repo for e in model.errors] == [rc.name for rc in repos]


def test_fetch_board_caps_max_workers_at_8(monkeypatch):
    captured = {}

    class FakeExecutor:
        def __init__(self, max_workers=None):
            captured["max_workers"] = max_workers

        def __enter__(self):
            return self

        def __exit__(self, *exc_info):
            return False

        def map(self, fn, iterable):
            return [fn(x) for x in iterable]

    monkeypatch.setattr(concurrent.futures, "ThreadPoolExecutor", FakeExecutor)

    repos = [
        RepoConfig(name=f"repo-{i}", path="/x", command=["python", "spawn.py"])
        for i in range(12)
    ]

    def run_json(repo_config):
        return json.dumps(EMPTY_PAYLOAD)

    fetch_board(repos, run_json)

    assert captured["max_workers"] == 8


def test_fetch_board_real_path_threads_timeout_through(monkeypatch):
    captured = {}

    class FakeCompleted:
        returncode = 0
        stdout = json.dumps(EMPTY_PAYLOAD)
        stderr = ""

    def fake_run(argv, **kwargs):
        captured.update(kwargs)
        return FakeCompleted()

    monkeypatch.setattr(subprocess, "run", fake_run)

    repos = [RepoConfig(name="on-the-record", path="/x", command=["python", "spawn.py"])]
    fetch_board(repos, timeout=42)

    assert captured["timeout"] == 42
