# Current-state survey — execution-observation (issue #4)

Status: phase-1 survey. Scope: what exists to verify, and what this
role's write surface (`docs/issue-4/reports/execution-observation.md`,
phase-2) will need to exercise. No verification is performed yet — phase 2
is gated on an approver's `APPROVE issue-4/execution-observation` comment
(role-handoff contract v3 s19), which does not exist on issue #4 as of
this survey.

## What was delivered (from main, merged PRs #9/#10)

- `src/rsb/webserver.py`: `ThreadingHTTPServer` handler serving
  `src/rsb/web/` statically plus `GET /api/board.json` (fresh
  `fetch_board()` per request, `render_json_model()` output). Appends one
  NDJSON `{ts, ua_class}` record per `/api/board.json` hit to `--log` when
  given (H1 instrument per `docs/issue-4/proposals/hypotheses.md` §3).
- `src/rsb/cli.py`: `rsb serve [--host 127.0.0.1] [--port 8420] [--log PATH]`
  subcommand, reusing `--config`/`--repo`.
- `src/rsb/web/{index.html,dashboard.css,dashboard.js}`: no-build vanilla
  JS frontend. `dashboard.css` defines `design-system.md` tokens as CSS
  custom properties. `dashboard.js` implements the states and regions
  `screen-spec.md` §1-§2 specifies.
- `test/rsb_tests/test_webserver.py`: contract tests for `/api/board.json`
  (normalized shape, partial-failure-still-200, request logging, `/`
  serving `index.html`).
- `docs/issue-4/reports/implementation.md`: implementer's own claim —
  "33 passed", "~4ms end-to-end" manual timing, states/regions traced
  1:1 to screen-spec.md.

## What this role must independently check (not re-trust the builder's claim)

Per role-handoff contract, execution-observation exists precisely
because a builder's self-report is not verification. Concretely:

1. **State reproduction** — `screen-spec.md` §2 defines six states:
   page-loading, page-empty, region-empty, page-error (total failure),
   partial-failure (banner), detail-panel-empty. None of these have been
   independently reproduced yet; only unit-test coverage of the JSON
   contract exists (`test_webserver.py`), and per implementation.md
   frontend rendering logic itself is *not* covered by any test —
   "exercised only indirectly." This is the largest verification gap:
   the states screen-spec.md most cares about (empty/error/partial) are
   exactly the ones with no automated check.
2. **H1 timing claim** — implementation.md's "~4ms" and "well inside
   3s" are one manual, unlogged measurement against the worked-example
   fixture, not a reproducible measurement this role has run itself.
   hypotheses.md §3 pre-registers "median time from web-view load to
   render ≤ 3s" as a real metric with a real threshold — an
   execution-observation record repeating the builder's own single
   anecdotal number is not independent evidence.
3. **pytest re-run** — "33 passed" is stated, not re-executed by an
   independent process in this survey (only inspected the test file's
   content, not run it — phase-1 work performs no execution). Needs a
   fresh interpreter/env run in phase 2, not a re-quote.
4. **Spec conformance** — screen-spec.md §1 defines 9 regions with exact
   populated-by/content contracts, and a traceability table (§3) tying
   every region to a hypothesis. design-system.md defines specific token
   values (contrast ratios, age-bucket thresholds `<4h`/`4-24h`/`≥24h`,
   status color mapping). No line-by-line diff between the spec and the
   shipped `dashboard.js`/`dashboard.css` has been done outside the
   implementer's own self-report.
5. **Handoff gaps flagged upstream, still open**: auth/access model
   (hypotheses.md §5, screen-spec.md §5 — still unresolved, unrelated to
   this role but worth noting if observation surfaces a live risk);
   age-bucket hour thresholds (design-system.md §7, screen-spec.md §5)
   were left as "a reviewable first cut" — in scope to check the code
   matches design-system.md's stated cutoffs, not to relitigate the
   cutoffs themselves.

## Environment available for phase-2 execution

- `python3` 3.10.12, `pytest` present at `~/.local/bin/pytest`.
- No repo config (`boards.toml`) exists yet in this checkout; the
  worked-example fixture (`test/rsb_tests/fixtures.py`, referenced by
  `test_webserver.py` as `WORKED_EXAMPLE`/`EMPTY_PAYLOAD`) is the
  available data source for reproducing states without needing live
  `flows --json`-capable repos. Full state reproduction (esp. partial-
  vs-total failure) will need either a small standalone script driving
  `webserver.make_handler` with a crafted `fetch_board_fn`, or a
  `boards.toml` pointing at fixture-backed repos.
- No editable install of the package is present in this environment
  yet (`pip show rsb` was not confirmed installed); phase 2 will need to
  install it (or run with `PYTHONPATH=src`) before `pytest`/manual
  `rsb serve` runs work.

## Skip condition check (scout-directive)

Scouting was **skipped**. This survey's task is a verification role
auditing shipped code against already-frozen, already-approved internal
specs (`hypotheses.md`, `screen-spec.md`, `design-system.md`,
`implementation.md`) — there is no open product-facing or build-stack
decision left to steer with external scouting; the spec literally leaves
no design decision open for this role (screen-spec.md/design-system.md/
implementation.md are already accepted, and this role's job is
compare-and-record, not choose). This is skip condition 2 verbatim.
