"""Runs `flows --json` per registered repo and normalizes the results.

The subprocess boundary (`run_flows_json`) is injectable so tests never
shell out to a real `spawn.py` (proposal §7).
"""

import concurrent.futures
import functools
import json
import os
import subprocess

from rsb.model import PayloadError, merge_repos, normalize_payload

DEFAULT_TIMEOUT_SECONDS = 60


def _redact_paths(text):
    """Collapse absolute-path-looking runs of text to their final path segment.

    Splits on single spaces and merges a leading `/`-starting word with
    every immediately-following word that still contains a `/` — so a
    path with an embedded space (e.g. a macOS `/Users/Jane Doe/repo` home
    directory) gets fully redacted rather than leaving its later segments
    exposed, which a whitespace-free-token-only regex would miss (warrant
    hunt, before-landing, issue #62). A following word with no `/` (prose)
    ends the run. Keeps error messages diagnosable (the failing filename
    stays visible) without exposing the internal filesystem layout the
    path implies (issue #62 R5d).
    """
    words = text.split(" ")
    out = []
    i = 0
    while i < len(words):
        word = words[i]
        if word.startswith("/") and "/" in word[1:]:
            end = i + 1
            while end < len(words) and "/" in words[end]:
                end += 1
            out.append(os.path.basename(" ".join(words[i:end])))
            i = end
        else:
            out.append(word)
            i += 1
    return " ".join(out)


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
        detail = e.strerror if e.strerror is not None else str(e)
        raise RuntimeError(
            f"failed to launch {os.path.basename(argv[0])!r}: {_redact_paths(detail)}"
        ) from e

    if result.returncode != 0:
        stderr_excerpt = (result.stderr or "").strip().splitlines()
        excerpt = stderr_excerpt[-1] if stderr_excerpt else f"exit code {result.returncode}"
        raise RuntimeError(f"flows --json failed: {_redact_paths(excerpt)}")

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


def fetch_board(repo_configs, run_json_fn=None, timeout=DEFAULT_TIMEOUT_SECONDS):
    """Fetch + normalize + merge all repos into one BoardModel.

    Repos are fetched concurrently (one subprocess call per repo), capped at
    8 worker threads regardless of repo count (rate-limit/resource review
    feedback). `.map()` is used rather than submit()+as_completed() so the
    result order matches `repo_configs` input order — merge_repos() and
    several BoardModel fields rely on that ordering rather than completion
    order.
    """
    if run_json_fn is None:
        run_json_fn = functools.partial(run_flows_json, timeout=timeout)

    max_workers = min(len(repo_configs), 8) or 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        per_repo_results = list(
            executor.map(
                functools.partial(fetch_and_normalize_one, run_json_fn=run_json_fn),
                repo_configs,
            )
        )
    return merge_repos(per_repo_results)
