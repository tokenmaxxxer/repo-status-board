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
- `--allow-partial` — when some but not all configured repos fail to
  fetch, exit 0 instead of 1 (issue #58). Without this flag, `rsb`'s
  exit code reflects `model.errors` being non-empty at all, not just
  every repo failing — a 1-of-N-repo failure now fails the CI build
  step by default instead of silently deploying a partial board.
  An all-repos-failing config still exits 1 regardless of this flag,
  since there is nothing to publish either way.

## Tests

```
python -m pytest test/
```

Requires the `pip install -e .` step from "Install / run" above — run
without it and collection fails with `ModuleNotFoundError: No module
named 'rsb'` before any test executes.

No live `spawn.py` dependency — the subprocess boundary
(`rsb.fetch.run_flows_json`) is mocked via fixture payloads in
`test/rsb_tests/fixtures.py`, including the worked example from
`docs/specs/flows-schema.md` §7.

6 of `dashboard.js`'s 10 pure/DOM-free `module.exports` helpers get
`node -e` coverage via `test_model.py`'s `_run_dashboard_js`, gated by
`pytest.skip()` if `node` isn't on `PATH`. Its DOM-wiring layer — event
listeners, `<select>` population, `load()`'s fetch path — is covered
separately by `test/rsb_tests/test_dashboard_dom.py`, which loads the
actual shipped `dashboard.js` against a real jsdom DOM and dispatches
real events (issue #44). One-time prerequisite, gated the same way:

```
npm install --prefix test
```

If `test/node_modules/jsdom` isn't present, the DOM suite skips instead
of failing. Future verification/smoke-check sessions should extend this
harness (add a test function, reusing `_run_dom_js`) instead of writing
a new one-off script — this is what it exists to replace.

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
60-day clock. As of this writing (`pushed_at` 2026-08-04T10:33:16Z) the
next push-driven reset is needed by roughly **2026-10-03** — a repo
owner should either push a real change or a deliberate empty commit
before that date, or the cron silently stops firing with no other
signal (issue #58 D4). This is a recurring operational reminder, not a
one-time fix: it needs re-arming every ~60 days regardless.

### Failure notification

Both the `build` and `deploy` jobs in `deploy-board.yml` post to the
`RSB_ALERT_WEBHOOK` repo secret (a plain JSON-payload webhook URL, e.g.
Slack's incoming-webhook format) on `if: failure()`, so a red scheduled
run reaches a channel a human reads instead of only the Actions tab
(issue #58's "no failure notification" gap). If the secret is unset,
the notification step logs a message and exits 0 — a missing webhook
is a silent no-op, not a second failure mode on top of the one it's
supposed to report.

### Staleness banner

`dashboard.js`'s `staleness(generatedAt, nowIso, thresholdMs)` compares
the board payload's own `generated_at` to wall clock at render time (no
server-side flag, no schema change) and returns a non-null
age-description once the board is more than 45 minutes old — ~1.5x the
30-minute `deploy-board.yml` cron interval, so one missed run is still
"fresh" but two in a row trips the banner. `renderData()` shows it as
an unmissable banner naming the actual age (e.g. "last updated 3h12m
ago") above the partial-failure banner. Because staleness is computed
client-side on load, every open tab re-evaluates it on its own clock
without needing a redeploy.

### Sessions/Accounting panels in CI

`sessions[]`/`ledger[]` in `board.json` are sourced from `on-the-record`'s
`runs/` directory, which is gitignored there — a CI checkout never has
it, so these arrays are structurally always empty in the deployed
board (issue #58 D2). `dashboard.js`'s `renderData()` omits the
Sessions and Accounting `<section>`s entirely when both are empty,
rather than rendering tables that would otherwise misread as "nothing
is running." A local `rsb serve` against a real `runs/` directory still
renders both sections normally.
