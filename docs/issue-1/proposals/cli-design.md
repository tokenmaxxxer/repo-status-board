# issue-1 implementation proposal — status board CLI v1

Author: implementation role, issue #1. Phase 1 (design) deliverable — no
code in this branch until phase-2 approval per the role-handoff contract.
See `docs/issue-1/reports/implementation/current-state.md` for the survey
this proposal builds on, and `docs/specs/flows-schema.md` for the frozen
data contract.

## 1. Goals / non-goals

Goals (from issue #1):
- Single command (`rsb`) that renders one screen covering: decision queue
  (top), per-issue flow stages, running sessions, per-issue accounting,
  hygiene warnings.
- Multiple board repos registered via a config file.
- Data comes only from `flows --json`; no direct parsing of `spawn.py`
  internals.
- Clear error on `schema_version` mismatch.
- Default: single render and exit. `--watch`: periodic re-render.

Non-goals (v1): HTML renderer (explicit follow-up issue), write/mutate
operations of any kind, alerting/exit-code semantics beyond hard failures,
historical/trend views.

## 2. CLI surface

```
rsb [--config PATH] [--repo NAME ...] [--watch [INTERVAL]] [--once] [--no-color] [--json]
```

- `rsb` with no args: read config (default `~/.config/rsb/boards.toml`, or
  `$RSB_CONFIG`), run one `flows --json` pass across all registered repos,
  render one screen, exit 0.
- `--config PATH`: override config file location.
- `--repo NAME`: restrict the render to one or more registered repos
  (repeatable). Omitted = all registered repos.
- `--watch [INTERVAL]`: re-run and re-render every `INTERVAL` seconds
  (default `30`) until interrupted (Ctrl-C → clean exit 0). Full-screen
  redraw each cycle (see §5). `--watch` implies persistent terminal mode;
  incompatible with `--json`.
- `--once`: explicit alias for the default single-shot behavior (useful when
  a config sets a default watch mode, so callers can override — v1 config
  will not support that, but the flag is cheap to add now and keeps room).
- `--no-color`: disable ANSI styling (for piping/log capture).
- `--json`: skip rendering, print the merged/normalized payload (post
  schema-version check, pre-layout) as JSON instead. Useful for scripting
  and for the HTML renderer follow-up issue to reuse this CLI's fetch+merge
  layer instead of re-implementing it.

Exit codes: `0` normal (including hygiene violations present — those are
data, not alerts, matching the schema's own non-goal #2). Non-zero only for
hard failures: bad config, `flows --json` invocation failure for *all*
configured repos, or unparseable JSON from all repos. A single bad repo
among several does not fail the whole run — it renders as a per-repo error
row and the exit code stays 0 (partial-success posture matches "board
status tool", not "CI gate").

## 3. Config file format

TOML, minimal:

```toml
[[repo]]
name = "on-the-record"
path = "/home/jiwon/src/on-the-record"   # passed to `spawn.py flows --json -C <path>`

[[repo]]
name = "repo-status-board"
path = "/home/jiwon/src/repo-status-board"
```

Each entry names a local checkout; `rsb` invokes
`python spawn.py flows --json -C <path>` (or a configured `command` override
per repo, for non-default entrypoints — `command = [...]` optional field,
defaults to `["python", "spawn.py"]` relative to `path`) as a subprocess,
captures stdout, and parses it. This keeps `rsb` a pure consumer of the
documented contract — it never touches `runs/`, session logs, or `.git`
directly.

## 4. Data flow / parsing

1. For each registered repo (or the `--repo`-filtered subset), run the
   `flows --json` subprocess with a timeout (default 15s, configurable
   later if needed — not v1).
2. Parse stdout as JSON. On subprocess failure or JSON parse failure: record
   a per-repo error, continue with other repos.
3. Check `schema_version`. `rsb` is built against version `1`
   (`SUPPORTED_SCHEMA_VERSION = 1`). Mismatch → per-repo error row with a
   message like `on-the-record: unsupported schema_version=2 (rsb supports 1)`,
   not a crash — other repos still render.
4. Normalize each repo's payload into typed in-memory records: `Decision`,
   `Flow`, `Session`, `LedgerEntry`, `Unattributed`, `Hygiene`. Attach the
   source repo name to every record (config's `name`, not the payload's
   `repo` field, though the two should usually agree — mismatch is not
   fatal, just noted).
5. Merge across repos per section (decision queue is a flat list sorted by
   `age_hours` descending — oldest/most urgent first; flows/sessions/ledger
   grouped by repo then issue; hygiene grouped by repo).
6. Hand the merged model to the renderer (or dump as `--json`).

Unknown/extra JSON fields are ignored (forward-compatible with additive
schema changes, per the schema doc's versioning policy — only a
`schema_version` bump requires a `rsb` code change).

## 5. Screen layout (single-shot and watch mode share this renderer)

Terminal-width-aware, sections stacked top to bottom, each with a header
rule. Order matches issue's priority ordering (decision queue first — "사람이
지금 해야 할 일"):

```
rsb — 2026-07-31 08:00:00Z — 2 repos, 1 error
════════════════════════════════════════════════════════════════
DECISION QUEUE  (2 awaiting)
  issue  pr   phase  role            age      awaiting
  172    201  2      implementation  22.8h    approve-full   [on-the-record]
────────────────────────────────────────────────────────────────
FLOWS
  issue  stage         roles                              prs   repo
  172    implementing  implementation:scope-approved       201  on-the-record
────────────────────────────────────────────────────────────────
SESSIONS
  role            issue  elapsed  alive  verdict  last activity           repo
  implementation  172    9.5m     yes    pending   12:03:44 tool_use: Write roles/data-modeling.json  on-the-record
────────────────────────────────────────────────────────────────
ACCOUNTING
  issue  sessions  cost_usd  outcomes                repo
  172    2         3.14      progressed:1 refused:1  on-the-record
  (unattributed: 0 sessions, $0.00 — on-the-record)
────────────────────────────────────────────────────────────────
HYGIENE
  [closure-sweep] issue 170: closed_without_delivered_stage — on-the-record
  [unapproved-pr] issue 172 pr 201 (implementation, opened 2026-07-30) — on-the-record
────────────────────────────────────────────────────────────────
ERRORS
  repo-status-board: flows --json failed: <stderr excerpt>
```

Design notes:
- Each section is column-formatted (simple fixed/elastic-width table, no
  external TUI framework needed for v1 — plain ANSI + `os.get_terminal_size`
  is enough; ok to keep a dependency-light stdlib-only implementation).
- Empty sections render a one-line `(none)` rather than being omitted, so
  the screen shape is stable across watch refreshes (avoids layout jumping).
- `stage_derived: false` rows are flagged, e.g. `stage: <raw-value> (raw)`,
  per the schema's explicit instruction not to force-map unknown
  `loop_state` values.
- `last_activity: null` renders as `—`.
- Long `detail` strings are already pre-truncated to 80 chars upstream by
  the schema provider; the renderer does not re-truncate but does elide with
  terminal width if narrower than 80 cols.
- Errors section only appears when at least one repo failed; keeps the
  common case (all repos healthy) free of clutter.

## 6. `--watch` mode

- Loop: render → sleep `INTERVAL` seconds → clear screen (`\x1b[2J\x1b[H`) →
  re-fetch and re-render. No diffing/partial redraw in v1 — full redraw is
  simpler and correctness matters more than flicker for a status board
  refreshed every 30s+.
- Ctrl-C (`SIGINT`) exits cleanly (exit 0), no traceback.
- Each cycle is independent: a transient `flows --json` failure on one
  cycle doesn't kill the loop, it just shows in the ERRORS section for that
  cycle and retries next interval.
- No polling-cadence guidance exists in the schema (explicit non-goal), so
  the default interval (30s) is `rsb`'s own choice, documented in `--help`
  and overridable via the positional/optional argument to `--watch`.

## 7. Testing approach (for phase 2)

- Unit tests for: schema-version check, per-section normalization
  (including `stage_derived: false`, `last_activity: null`,
  `unattributed`, empty sections), multi-repo merge/sort, config parsing.
- Fixture JSON payloads (including the worked example from
  `docs/specs/flows-schema.md` §7) as golden inputs — no live `spawn.py`
  dependency in tests; the subprocess boundary is mocked/injected.
- A renderer smoke test asserting the plain-text output contains expected
  section headers and row content for a fixture payload (not a pixel-exact
  golden file, to avoid brittleness across minor formatting tweaks).

## 8. Open questions for phase 2 (not blocking phase-1 approval)

- Should `--json` output be the raw upstream payload(s) keyed by repo, or
  the normalized merged model? Leaning normalized (single stable shape
  regardless of schema_version, useful for the future HTML renderer).
- Exact default config path — proposal uses `~/.config/rsb/boards.toml`;
  open to `./rsb.toml` (repo-local) as an additional/fallback location.
- Whether per-repo `flows --json` calls should run concurrently
  (`asyncio`/threads) once there are enough registered repos that serial
  subprocess calls become slow — not needed for v1 with a small number of
  repos, worth revisiting if it becomes a bottleneck.
