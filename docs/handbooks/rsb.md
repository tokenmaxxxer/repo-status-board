# rsb (status board CLI) handbook

`rsb` reads `<command> flows --json -C <path>` per registered repo (see
`docs/specs/flows-schema.md` for the data contract) and renders one screen:
decision queue, flows, sessions, accounting, hygiene, errors.

## Install / run

```
pip install -e .
rsb --config path/to/boards.toml
```

## Config

TOML, one `[[repo]]` block per board repo:

```toml
[[repo]]
name = "on-the-record"
path = "/home/jiwon/src/on-the-record"
# command = ["python", "spawn.py"]   # optional, defaults shown
```

Resolved from `--config`, else `$RSB_CONFIG`, else
`~/.config/rsb/boards.toml`.

## Flags

- `--repo NAME` (repeatable) — restrict to specific registered repos.
- `--watch [INTERVAL]` — re-render every `INTERVAL` seconds (default 30);
  `Ctrl-C` exits cleanly. Incompatible with `--json`.
- `--json` — print the normalized merged model instead of rendering.
- `--no-color` — accepted, currently a no-op (v1 renderer has no ANSI
  color to disable).

## Tests

```
python -m pytest test/
```

No live `spawn.py` dependency — the subprocess boundary
(`rsb.fetch.run_flows_json`) is mocked via fixture payloads in
`test/rsb_tests/fixtures.py`, including the worked example from
`docs/specs/flows-schema.md` §7.
