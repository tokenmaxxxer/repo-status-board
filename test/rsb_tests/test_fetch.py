import concurrent.futures
import json
import subprocess
import time

import pytest

from rsb.config import RepoConfig
from rsb.fetch import DEFAULT_TIMEOUT_SECONDS, fetch_and_normalize_one, fetch_board, run_flows_json

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


# ---- internal-path masking (issue #62 R5d) ---------------------------------
# Traces to docs/issue-38/reports/conformance-review.md R5d: fetch.py's two
# message-construction sites embedded the launcher's/subprocess's raw
# internal filesystem paths verbatim; the dashboard collapsed the message
# behind a closed <details> but never redacted it, so the path was still
# present in both the rendered HTML and api/board.json. These call
# run_flows_json directly (no existing test does) with a monkeypatched
# subprocess.run, asserting a fixture absolute path is absent from the
# resulting message while the diagnosable portion (strerror / stderr
# excerpt text) survives.


def test_run_flows_json_oserror_masks_internal_path(monkeypatch):
    fixture_path = "/Users/ci-runner/.secret-checkout/spawn.py"

    def fake_run(argv, **kwargs):
        raise FileNotFoundError(2, "No such file or directory", fixture_path)

    monkeypatch.setattr(subprocess, "run", fake_run)

    repo = RepoConfig(name="broken-exe", path="/x", command=[fixture_path])

    with pytest.raises(RuntimeError) as exc_info:
        run_flows_json(repo)

    message = str(exc_info.value)
    assert fixture_path not in message
    assert "No such file or directory" in message


def test_run_flows_json_nonzero_exit_masks_internal_path(monkeypatch):
    fixture_path = "/Users/ci-runner/.secret-checkout/repo"

    class FakeCompleted:
        returncode = 1
        stdout = ""
        stderr = "Traceback (most recent call last):\nFileNotFoundError: %s/flows.json not found\n" % fixture_path

    def fake_run(argv, **kwargs):
        return FakeCompleted()

    monkeypatch.setattr(subprocess, "run", fake_run)

    repo = RepoConfig(name="broken-flows", path="/x", command=["python", "spawn.py"])

    with pytest.raises(RuntimeError) as exc_info:
        run_flows_json(repo)

    message = str(exc_info.value)
    assert fixture_path not in message
    assert "not found" in message


def test_run_flows_json_nonzero_exit_masks_internal_path_with_spaces(monkeypatch):
    # before-landing warrant hunt (docs/reports/2026-08-08-hunt-issue-62-implementation.md):
    # a whitespace-free-token-only regex leaves a directory name containing
    # a space (e.g. a macOS "Jane Doe" home dir) only partially redacted.
    fixture_path = "/Users/Jane Doe/.secret-checkout/repo"

    class FakeCompleted:
        returncode = 1
        stdout = ""
        stderr = "Traceback (most recent call last):\nFileNotFoundError: %s/flows.json not found\n" % fixture_path

    def fake_run(argv, **kwargs):
        return FakeCompleted()

    monkeypatch.setattr(subprocess, "run", fake_run)

    repo = RepoConfig(name="broken-flows-spaced", path="/x", command=["python", "spawn.py"])

    with pytest.raises(RuntimeError) as exc_info:
        run_flows_json(repo)

    message = str(exc_info.value)
    assert fixture_path not in message
    assert ".secret-checkout" not in message
    assert "not found" in message


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
