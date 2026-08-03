# Current-state survey — issue #27

Scope of the survey: the write set phase 2 is expected to touch — a new
GitHub Actions workflow, a new CI-only rsb config, the dashboard's board
fetch path, and the rsb handbook doc. This phase-1 survey is
research-only; no `.github/`, `src/`, or `test/` file is created or
modified this turn.

## 1. `rsb` CLI JSON output path (`src/rsb/cli.py`)

`--json` (line 33) is a top-level flag, orthogonal to the `serve`
subcommand. `_run_once()` (lines 58-66) is what actually runs on `--json`:
it calls `fetch_board(repo_configs)`, then
`print(json.dumps(render_json_model(model, generated_at), indent=2))`
(line 62) — plain `print()` to **stdout**, no TTY dependency, so
`rsb --json > board.json` in a CI step captures exactly the same payload
a human would see via `rsb serve`'s `/api/board.json` route.

Exit codes, read directly from `_run_once()` and `main()`:
- `main()` lines 76-82: `ConfigError` (bad `--config` path, unknown
  `--repo` name) → prints to stderr, returns **2**.
- `_run_once()` line 65-66: `all_failed = len(repo_configs) > 0 and
  len(model.errors) == len(repo_configs)` → returns **1** only when
  *every* configured repo failed to fetch/parse/normalize.
- Otherwise (including partial per-repo failures, which land in
  `model.errors` and render as an `errors[]` array in the JSON, not as a
  nonzero exit) → returns **0**.

This means a CI step can gate purely on `rsb`'s own exit code (`0` →
proceed to publish, nonzero → stop) without inspecting the JSON body,
which is exactly the mechanism requirement 5 (fail-safe: never overwrite
a good deployment with a broken one) needs.

`--watch` is explicitly rejected together with `--json`
(`parser.error("--watch is incompatible with --json")`, line 74) — not
relevant to a cron-triggered one-shot workflow anyway, but confirms
`--json` is a single-render code path with no lingering process.

## 2. Config loading (`src/rsb/config.py`)

`load_config()` (lines 35-63) reads TOML `[[repo]]` blocks into
`RepoConfig(name, path, command)` (frozen dataclass, lines 19-23).
`command` defaults to `["python", "spawn.py"]` (line 60) when the TOML
entry omits it, but is fully overridable per repo as a list — this is
the mechanism a CI config can use to point every board entry at a single
shared `spawn.py` checkout regardless of each board's own `path`.
`resolve_config_path()` (lines 26-32) prefers an explicit `--config`
path, so a workflow step can pass a repo-committed CI-only TOML file
without touching `$RSB_CONFIG` or `~/.config/rsb/boards.toml` (the local
dev defaults, left untouched).

## 3. Subprocess boundary (`src/rsb/fetch.py`)

`run_flows_json()` (lines 15-40) builds
`[*repo_config.command, "flows", "--json", "-C", repo_config.path]` and
runs it via `subprocess.run(..., timeout=15)` (default
`DEFAULT_TIMEOUT_SECONDS = 15`, line 12). Any failure mode — nonzero
exit (lines 35-38), `TimeoutExpired` (lines 30-31), or the executable
not existing at all (`OSError`, lines 32-33) — is converted to a
`RuntimeError`, which `fetch_and_normalize_one()` (lines 43-64) always
catches and turns into a per-repo `(name, None, error_message)` tuple —
**never** propagates to the caller. `merge_repos()` (in `model.py`,
called from `fetch_board()`, lines 67-70) aggregates these into
`model.errors`. This is why "all repos failed" is the only case that
maps to a nonzero CLI exit (survey §1) — a single misconfigured board
entry degrades to a per-repo error row, not a hard failure, which is
worth flagging as an operational nuance for phase 2: a CI run where 2 of
3 boards succeed still exits 0 and would still publish (partial data,
not a full failure) unless the workflow adds its own stricter check.
Not something to fix in this repo — flagged for the proposal's
constraints/rationale section to decide explicitly rather than leave
implicit.

## 4. Local-serve mode (`src/rsb/webserver.py`) — must stay unchanged

`make_handler()` (lines 35-59) serves static files from `WEB_DIR`
(`src/rsb/web/`, line 10) via `SimpleHTTPRequestHandler`, with one
override: `do_GET()` (lines 40-44) special-cases `self.path ==
"/api/board.json"` and calls `_serve_board_json()` (lines 46-54), which
invokes `fetch_board_fn` live and streams
`json.dumps(render_json_model(model, _now_iso()))` back as
`application/json`. This is the **local-only** mode the issue's
requirement 2 says must keep working with zero regression — it is a
live HTTP handler, not a static file, so it is structurally unaffected
by anything phase 2 does to `dashboard.js`'s fetch path (see §6) as long
as that fetch path still resolves to whatever origin the page is served
from.

## 5. JSON payload shape (`src/rsb/render.py`)

`render_json_model` (referenced from `cli.py` line 62 and `webserver.py`
line 49) is the single function both the CLI `--json` path and the
local-serve `/api/board.json` path call — confirming a CI step running
`rsb --json` and a browser hitting local `rsb serve` receive
byte-for-byte the same payload shape (`generated_at`,
`generated_at_by_repo`, `decisions`, `flows`, `sessions`, `ledger`,
`unattributed`, `closure_sweep`, `unapproved_open_prs`, `errors`). No
divergent code path to keep in sync — a static `board.json` produced by
`rsb --json` in CI is a drop-in replacement for what the live handler
would have returned at that instant.

## 6. Dashboard fetch path — the absolute-path bug (`src/rsb/web/dashboard.js`)

Confirmed by direct read, line 406:

```js
const res = await fetch("/api/board.json");
```

This is an **absolute** root-relative path. For local `rsb serve` the
page is served at the server root (`http://host:port/`), so
`/api/board.json` and `api/board.json` resolve identically — no
observable difference today. For a GitHub Pages *project* site
(`https://tokenmaxxxer.github.io/repo-status-board/`), the page itself
lives under a subpath, but an absolute `/api/board.json` resolves
against the *origin* (`https://tokenmaxxxer.github.io/api/board.json`),
which is outside the repo's Pages subpath and would 404. Changing line
406 to the relative form `fetch("api/board.json")` resolves against the
current document URL in both cases: `http://host:port/api/board.json`
under local serve (identical behavior, zero regression) and
`https://tokenmaxxxer.github.io/repo-status-board/api/board.json` under
Pages (correct). This one-line change is the entire mechanism for
requirement 2.

`src/rsb/web/index.html` already uses relative `href`/`src` for
`dashboard.css` and `dashboard.js` (no leading `/`) — confirmed by read,
only the JS fetch call carries the absolute-path bug. No other absolute
references were found in `dashboard.js` or `dashboard.css`.

## 7. `runs/`-absence behavior — requirement 4

Requirement 4 asks whether `flows --json` errors when `runs/` doesn't
exist (the case on a fresh Actions runner checkout, which has no prior
orchestrator state). This repo's own code (`fetch.py`, §3 above) already
degrades any subprocess failure to a per-repo error row rather than
crashing — but the more direct question is whether `spawn.py` itself
raises on missing `runs/` before it even gets to emit JSON. Read
directly from a local on-the-record clone
(`/Users/jk/workspace/10_WORK/tokenmaxxxer/on-the-record`, read-only
reference, not part of this repo's write set):

- `spawn.py:35` — `ROOT = Path(__file__).resolve().parent`. `runs/` is
  always resolved relative to wherever `spawn.py` itself lives (the
  orchestrator checkout), independent of the `-C` target path. In the
  frozen CI design (proposal), the single on-the-record checkout that
  provides `spawn.py` is what determines where it looks for `runs/`,
  regardless of which board (`-C <path>`) it's being asked to report on.
- `spawn.py:1291-1295`, `_roster_load()`:
  ```python
  def _roster_load() -> dict:
      try:
          return json.loads(ROSTER.read_text())
      except (OSError, ValueError):
          return {}
  ```
  A missing `runs/active.json` raises `FileNotFoundError` (an `OSError`
  subclass) from `.read_text()`, which is caught and turned into `{}`.
  No exception propagates.
- `gates/flows.py:141-154`, `_ledger_read()`:
  ```python
  def _ledger_read() -> list[dict]:
      p = spawn.ROOT / "runs" / "ledger.jsonl"
      if not p.is_file():
          return []
      ...
  ```
  A missing `runs/ledger.jsonl` is guarded explicitly by `is_file()`,
  returning `[]` with no exception.
- Both feed directly into `flows_payload()`
  (`gates/flows.py:344-347,383-391`), which puts the empty results
  straight into the JSON payload as `"sessions": []` and `"ledger": []`
  — no error, no nonzero exit.

**Conclusion**: requirement 4 is already satisfied by existing
on-the-record code. This was verified by direct source reading (exact
file:line citations above), not by executing `spawn.py` against a real
empty-`runs/` runner. No feedback to on-the-record is needed and this
issue is not blocked on it. The gap between "verified by reading source"
and "verified by an actual empty-`runs/` CI run" is real but small —
noted in the proposal as a risk/observability item for phase 2's first
live workflow run, not as a phase-1 blocker.

One related operational note found while reading the same files:
`gates/flows.py:45-73` (`_pr_list_all` / `_issue_list_all`) shells out to
`gh pr/issue list ...` with `cwd=root`, letting `gh` auto-detect the
target repo from the checkout's git remote — meaning the `-C` target
passed to `spawn.py` must be an actual git checkout with a correctly
configured `origin` remote (which `actions/checkout` produces
automatically, so this is satisfied by design, not something phase 2
needs to add). These same functions silently return `[]` on any `gh`
failure (auth, network, rate limit) rather than raising — an operational
risk worth naming in the proposal (a silent-empty-data failure mode) but
not something to fix in this repo, since it is `spawn.py`'s own
behavior, out of scope for this issue's write set.

## 8. Dependency footprint

`pyproject.toml`: `requires-python = ">=3.10"`, single runtime dependency
`tomli` (only pulled in below Python 3.11 — `tomllib` from stdlib is used
at 3.11+, confirmed in `config.py` lines 7-10), single console entrypoint
`rsb = "rsb.cli:main"` via setuptools (`pyproject.toml` lines 10-11,
13-18). `spawn.py` itself has zero pip dependencies (pure stdlib:
`argparse, contextlib, re, fcntl, hashlib, json, os, stat, string,
subprocess, sys`, plus `pathlib`/`time` in `gates/flows.py`) — `fcntl` is
POSIX-only, which is fine on GitHub-hosted `ubuntu-latest` runners. No
`pip install` step is needed for `spawn.py`; only this repo's own `rsb`
package needs `pip install -e .` in the workflow.

## 9. No existing `.github/` directory

Confirmed: this repo has no `.github/` directory or workflow files of
any kind today. Phase 2's `.github/workflows/deploy-board.yml` and
`.github/boards.ci.toml` are wholly new paths, not edits to existing CI
config.

## Write-set summary (what phase 2 will actually touch)

- `.github/workflows/deploy-board.yml` — new: cron + `workflow_dispatch`
  triggered workflow, multi-repo checkout, `rsb --json` generation,
  Pages publish gated on generation success (requirements 1, 3, 5).
- `.github/boards.ci.toml` — new: CI-only rsb config (paths/commands,
  no secrets) pointing all three board entries at a single shared
  `spawn.py` checkout (issue's background note).
- `src/rsb/web/dashboard.js` — one-line fix, line 406:
  `fetch("/api/board.json")` → `fetch("api/board.json")` (requirement 2).
- `docs/handbooks/rsb.md` — add the one-time manual Pages-source setup
  step (repo-admin prerequisite, cannot be scripted from inside the
  workflow) and a short static-deploy section.
- No `src/rsb/cli.py`, `src/rsb/fetch.py`, `src/rsb/config.py`,
  `src/rsb/webserver.py`, `src/rsb/render.py`, or `src/rsb/model.py`
  changes — all already support the static-generation path unchanged
  (confirmed by reading each in full, §1-5 above). No on-the-record
  changes — requirement 4 already satisfied by existing code (§7).
