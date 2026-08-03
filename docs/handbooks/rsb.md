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

## Static deploy (GitHub Pages)

`.github/workflows/deploy-board.yml` runs on a 30-minute `schedule` plus
`workflow_dispatch`. The `build` job checks out this repo and the two
other board repos (`on-the-record`, `tokenmaxxxer-core`, both public),
runs `rsb --config .github/boards.ci.toml --json > board.json`, and
assembles a `_site/` directory (the dashboard's static files plus
`board.json` at `api/board.json`). The `deploy` job publishes `_site/`
to GitHub Pages only if `build` succeeded, so a broken generation run
never overwrites the last good deployment.

One-time manual prerequisite: a repo admin must set **Settings → Pages
→ Build and deployment → Source: GitHub Actions** once. The workflow's
default `GITHUB_TOKEN` cannot flip this setting itself (it lacks
repo-admin scope), so `deploy-pages` will fail until this is done.

GitHub auto-disables a `schedule`-triggered workflow after 60 days with
no repository activity. If the Pages board stops updating, check the
Actions tab for a disabled workflow and re-enable it there (or trigger
`workflow_dispatch` manually) — any repo commit activity also resets the
60-day clock.
