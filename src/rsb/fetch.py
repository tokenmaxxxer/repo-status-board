"""Runs `flows --json` per registered repo and normalizes the results.

The subprocess boundary (`run_flows_json`) is injectable so tests never
shell out to a real `spawn.py` (proposal §7).
"""

import json
import subprocess

from rsb.model import PayloadError, merge_repos, normalize_payload

DEFAULT_TIMEOUT_SECONDS = 15


def run_flows_json(repo_config, timeout=DEFAULT_TIMEOUT_SECONDS):
    """Invoke `<command> flows --json -C <path>` for one repo; return raw stdout text.

    Raises RuntimeError with a human-readable message on any failure
    (nonzero exit, timeout, executable not found) — callers turn that into
    a per-repo error row rather than propagating it.
    """
    argv = [*repo_config.command, "flows", "--json", "-C", repo_config.path]
    try:
        result = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"flows --json timed out after {timeout}s") from None
    except OSError as e:
        raise RuntimeError(f"failed to launch {argv[0]!r}: {e}") from e

    if result.returncode != 0:
        stderr_excerpt = (result.stderr or "").strip().splitlines()
        excerpt = stderr_excerpt[-1] if stderr_excerpt else f"exit code {result.returncode}"
        raise RuntimeError(f"flows --json failed: {excerpt}")

    return result.stdout


def fetch_and_normalize_one(repo_config, run_json_fn=run_flows_json):
    """Fetch + parse + normalize one repo. Never raises — returns the
    (repo_name, normalized_or_None, error_message_or_None) tuple that
    merge_repos() consumes.
    """
    repo_name = repo_config.name
    try:
        stdout = run_json_fn(repo_config)
    except RuntimeError as e:
        return (repo_name, None, str(e))

    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as e:
        return (repo_name, None, f"unparseable JSON from flows --json: {e}")

    try:
        normalized = normalize_payload(repo_name, payload)
    except PayloadError as e:
        return (repo_name, None, str(e))

    return (repo_name, normalized, None)


def fetch_board(repo_configs, run_json_fn=run_flows_json):
    """Fetch + normalize + merge all repos into one BoardModel."""
    per_repo_results = [fetch_and_normalize_one(rc, run_json_fn) for rc in repo_configs]
    return merge_repos(per_repo_results)
