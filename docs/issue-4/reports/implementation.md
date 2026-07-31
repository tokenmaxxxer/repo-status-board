# Implementation record (issue #4)

Status: phase-2 delivered. Approved via issue #4 comment
`APPROVE issue-4/implementation` (JiwonJung94, approvers.md), against
`docs/issue-4/proposals/implementation.md`.

## What was built

- `rsb serve [--host] [--port] [--log PATH]` (`src/rsb/cli.py`): new
  argparse subcommand alongside the existing default board-render
  invocation. Reuses `--config`/`--repo` from the parent parser.
- `src/rsb/webserver.py`: `ThreadingHTTPServer` serving `src/rsb/web/`
  as static files and `GET /api/board.json`, which runs `fetch_board()`
  fresh per request and returns `render_json_model()`'s JSON — no
  caching layer, matching `flows --json`'s on-demand contract. Every
  `/api/board.json` request is appended as `{ts, ua_class}` NDJSON to
  `--log`'s path when given (H1 instrument, hypotheses.md §3).
- `src/rsb/web/{index.html,dashboard.css,dashboard.js}`: no-build
  vanilla JS frontend. `dashboard.css` defines every design-system.md
  token (§2-§5) once as CSS custom properties; no raw hex/px literal
  appears outside that block. `dashboard.js` implements loading
  (per-region skeletons), page-empty, region-empty, full-page error +
  retry, and partial-failure-banner states per screen-spec.md §2, plus
  the decision-queue/flows/sessions/accounting/hygiene/errors regions
  (§1.1-§1.9) and a click-to-open detail panel (side panel at
  `--breakpoint-lg` via a CSS media query, expandable block below it).
  `stage_derived: false` flows render the raw `stage` string with a
  `(raw)` suffix, no forced color/label.

## Tests

`test/rsb_tests/test_webserver.py`: `/api/board.json` returns the
normalized shape; partial-repo-failure still returns 200 with
per-repo `errors` populated; request logging writes one NDJSON record
per hit; `/` serves `index.html`. Full suite: 33 passed
(`pytest test/`, package resolved via editable install pointing at
this checkout's `src/`).

Frontend logic is exercised only indirectly (via the JSON contract
tests above) — no browser test runner was added, per the proposal's
stated scope (no CI browser environment in this repo).

## Verification

Manually timed a local request cycle (`/` + `/api/board.json` against
the worked-example fixture): ~4ms end-to-end, well inside H1's 3s
target. `python -m pytest test/ -q` run against this branch: 33/33
pass.

## Traceability

Every screen-spec.md region/state cited in the proposal has a 1:1 code
location in `src/rsb/web/dashboard.js`; no UI element beyond
screen-spec.md/design-system.md was added.

## Deferred (unchanged from proposal/spec, not this delivery's scope)

- Auth/access model for exposing this data over the web.
- Auto-refresh/poll interval (manual refresh button only).
- Age-bucket hour thresholds and H3 (design-system.md §7).
