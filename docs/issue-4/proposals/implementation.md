# Implementation proposal — web dashboard (issue #4)

Status: phase-1 proposal, awaiting `APPROVE issue-4/implementation`.
Scope: `src/`, `test/` only — building screen-spec.md/design-system.md as
running code. No spec renegotiation; all layout/token/state decisions
below cite the frozen specs verbatim.

Scouting: `docs/issue-4/reports/implementation/scout-brief.md`. Adopted:
no-build vanilla JS + `fetch()` + `setInterval` polling, static-file
servable. Skipped: htmx (no server-rendered-fragment backend to target),
React/Vite (unjustified build tooling for one route/one operator).

## 1. Architecture

Two new pieces, additive to existing `src/rsb/`:

- **`rsb serve`** (new CLI subcommand in `cli.py`, using stdlib
  `http.server`/`socketserver` — no new dependency): a tiny HTTP server
  that (a) serves the static frontend directory, and (b) exposes
  `GET /api/board.json` returning `render_json_model(fetch_board(...))`
  freshly computed per request (mirrors the CLI's one-shot fetch — no
  caching layer, no background poller; matches `flows --json`'s
  documented read-only, on-demand contract).
- **`src/rsb/web/`** static assets: `index.html`, `dashboard.css`,
  `dashboard.js`. Plain HTML/CSS/JS, no build step, no bundler,
  no runtime dependency.

## 2. Frontend behavior (screen-spec.md → code mapping)

- `dashboard.js`: one `render(state)` function switching on
  `{loading, error, partial, data}` — implements screen-spec.md §2.1
  (loading skeletons), §2.2 (page-empty), §2.3 (region-empty per table),
  §2.4 (full-page error + retry), §2.5 (partial-failure banner). Manual
  refresh via the header `RefreshButton` triggers one `fetch()`; no
  auto-poll timer is added (screen-spec.md §5 marks auto-refresh cadence
  as still-deferred/out of scope — this proposal does not decide it).
- All colors/spacing/type sizes are CSS custom properties named after
  design-system.md's token names verbatim (`--color-status-error`,
  `--space-4`, `--font-size-body`, etc.) defined once in `dashboard.css`
  — no raw hex/px literals outside that one token block, per issue's
  "reference tokens by name, no raw values outside primitives" requirement.
- Regions (§1.1–§1.9 of screen-spec.md) map 1:1 to DOM sections built
  from `board.json`'s `decision_queue`, `flows`, `sessions`, `ledger` +
  `unattributed`, `hygiene.closure_sweep`, per-repo `errors`. Detail
  panel (§1.6): side panel ≥1200px / expandable row below, via a CSS
  media query at `--breakpoint-lg`.
- `stage_derived: false` flows render the raw `stage` string with an
  "(raw)" suffix per screen-spec.md §1.4 — no fixed color/label forced
  onto unmapped stages (flows-schema.md §2.2 requirement).

## 3. H1 instrumentation (hypotheses.md hand-off)

Each `GET /api/board.json` request is timestamped and appended
(newline-delimited JSON: `{ts, ua_class}`) to a local log file, per
hypotheses.md §3's pre-registered instrument — no accounts, no
third-party analytics, matching the stated single-user-pilot scope.
`ua_class` is a coarse bucket (`terminal-tool` vs `browser`) derived from
the `User-Agent` header, best-effort only.

## 4. Tests (`test/rsb_tests`)

New test module for `serve`: `/api/board.json` returns valid JSON
matching `render_json_model`'s shape; partial-repo-failure path still
returns 200 with per-repo `errors` populated (mirrors `fetch_board`'s
existing partial-failure behavior, already covered for the CLI path).
Frontend logic (`dashboard.js`) is data-transform/render-state functions
kept testable without a DOM by structuring state-selection as pure
functions; no browser test runner is added for this pilot (out of
scope — no CI browser environment presently in this repo).

## 5. Traceability

Every screen-spec.md region/state cited above has a 1:1 code location;
no new UI element is invented beyond what screen-spec.md and
design-system.md already specify.
