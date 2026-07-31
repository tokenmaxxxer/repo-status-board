# issue-1 implementation report — status board CLI v1

Phase-2 deliverable, built per the approved proposal
(`docs/issue-1/proposals/cli-design.md`, approved via `APPROVE
issue-1/implementation` on the issue) and the frozen data contract
(`docs/specs/flows-schema.md`).

## What was built

- `src/rsb/config.py` — TOML config loading (`[[repo]]` entries, `name`,
  `path`, optional `command`), `~/.config/rsb/boards.toml` / `$RSB_CONFIG`
  resolution.
- `src/rsb/model.py` — typed records (`Decision`, `Flow`, `Session`,
  `LedgerEntry`, `Unattributed`, hygiene records), `normalize_payload()`
  (schema-version check + payload→records, per proposal §4), `merge_repos()`
  (per-repo error collection, decision-queue sort by `age_hours` desc).
- `src/rsb/fetch.py` — subprocess boundary running `<command> flows --json
  -C <path>` per repo with a 15s timeout; injectable `run_json_fn` so tests
  never shell out. Never raises past `fetch_board()` — failures become
  per-repo error rows.
- `src/rsb/render.py` — single-screen plain-text renderer (decision queue →
  flows → sessions → accounting → hygiene → errors, in that order); empty
  sections render `(none)`; `stage_derived: false` flagged as `(raw)`;
  `last_activity: null` renders `—`; `--json` mode via
  `render_json_model()` (normalized merged model, not raw per-repo
  payloads — resolves proposal §8 open question in favor of "normalized").
- `src/rsb/cli.py` — `rsb` entrypoint: `--config`, `--repo` (repeatable),
  `--watch [INTERVAL]` (default 30s, full-screen clear + redraw, clean
  `Ctrl-C` exit), `--once`, `--no-color` (accepted; no ANSI color used in v1
  since the renderer is plain-text/table-only — flag is a no-op reserved for
  a future color pass), `--json` (rejected together with `--watch`). Exit
  codes: `0` normal (including partial per-repo failures), `2` on config
  error, `1` only when every configured repo failed to fetch.
- `pyproject.toml` — packages `rsb` from `src/`, registers the `rsb`
  console script, depends on `tomli` for Python < 3.11 (`tomllib` used
  natively on 3.11+).

## Deviations from the proposal

None. `--json` normalized-model choice and default config path
(`~/.config/rsb/boards.toml`) both follow the proposal's stated leaning
(§8); concurrent per-repo fetching was left serial as the proposal notes is
fine for v1.

## Testing

`test/rsb_tests/` (stdlib `pytest`, no live `spawn.py` — subprocess boundary
mocked per proposal §7):

- `test_model.py` — schema-version rejection, malformed-payload rejection,
  worked-example normalization, empty sections, `stage_derived: false`,
  `last_activity: null` (both populated and null), multi-repo merge sort,
  per-repo error collection.
- `test_fetch.py` — subprocess failure, unparseable JSON, schema mismatch,
  multi-repo partial-failure merge — all via injected fake `run_json_fn`.
- `test_render.py` — section headers present, `(none)` empty-section
  rendering, ERRORS section only appears when populated, `--json` output is
  valid JSON matching the normalized model.
- `test_config.py` — multi-repo TOML parsing, missing file/fields,
  duplicate names, `$RSB_CONFIG`/`--config`/default precedence.
- `test_cli.py` — end-to-end `main()` with `fetch_board` mocked: text
  render exit 0, `--json` output, `--watch`+`--json` mutual exclusion,
  missing-config exit 2, unknown `--repo` exit 2, all-repos-failed exit 1.

Renamed the test package directory to `test/rsb_tests` (not `test/rsb`) —
pytest's rootdir import made a same-named `test/rsb` package shadow the
installed `src/rsb` package, breaking every `from rsb...` import; this test
directory name has no bearing on the CLI's own module name.

29/29 tests pass:

```
$ .venv/bin/python -m pytest test/ -q
29 passed in 0.04s
```

Manual smoke test: built a fake `spawn.py` emitting a minimal valid
`schema_version: 1` payload, ran `rsb --config <path>` (rendered all five
sections as `(none)`, exit 0) and `rsb --config <path> --json` (valid JSON,
`generated_at_by_repo` populated) against it — confirmed the real
config→subprocess→parse→render path works end to end, not just against
mocked fixtures.
