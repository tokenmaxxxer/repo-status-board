# Phase-2 implementation record — F1–F4 (issue #13)

## What was done

Implemented the four fixes exactly as specified in
`docs/issue-13/proposals/implementation.md` (upstream basis), with no
deviations:

- **F1** (`src/rsb/web/dashboard.js`, `renderData()`): added the
  payload-level total-failure check (`errors.length > 0 &&
  succeededRepoCount === 0` → `renderFullError(...)`) at the top of
  `renderData()`, before the summary-strip/partial-banner code.
- **F2** (`src/rsb/web/dashboard.css`): `.partial-banner a,
  .partial-banner button.link` now uses
  `--color-status-warning-foreground` instead of
  `--color-action-primary-foreground`.
- **F3** (`src/rsb/web/index.html`, `dashboard.js`, `dashboard.css`):
  added `#page-body` wrapper around `#main-content` and a new
  `#detail-panel-slot` sibling; `renderData()` now writes the detail
  panel markup into `DETAIL_SLOT` instead of concatenating it into
  `MAIN`'s innerHTML (also cleared in `renderSkeleton()`,
  `renderFullError()`, and the `isPageEmpty()` branch). CSS: `#page-body`
  is a 1-column grid by default, switching to
  `1fr minmax(280px, 340px)` at `min-width: 1200px` when
  `#detail-panel-slot` is non-empty (`:has()`), with the existing
  `position: sticky` rule kept for the panel at that breakpoint.
- **F4** (`src/rsb/web/dashboard.css`): added
  `@media (max-width: 768px) { .summary-strip { gap: var(--space-2); } }`.

No edits to `docs/specs/design-system.md` / `docs/specs/screen-spec.md`
(`git diff` against `docs/specs/` is empty).

## Why (rationale)

Approved via `APPROVE issue-13/implementation` (single-account mode,
JiwonJung94, posted as an issue-level comment on issue #13). Upstream
basis: `docs/issue-13/proposals/implementation.md` (approved fix
design), which traces each finding to
`docs/issue-4/reports/execution-observation.md` §6 (verification
findings F1–F4) and to `docs/specs/design-system.md` /
`docs/specs/screen-spec.md` (frozen contract the fixes conform
behavior to, without changing the spec text).

## Verification

- `python3 -m pytest test/ -q` — 33 passed, unchanged (fixes touch only
  `src/rsb/web/`, not `webserver.py`/`render.py`).
- Reproduced the total-failure payload against the real server
  (`rsb.webserver.make_handler` + `rsb.model.BoardModel(errors=[...])`,
  no succeeding repos): confirmed `/api/board.json` returns
  `errors: [...]`, `generated_at_by_repo: {}` — exactly the shape F1's
  client-side condition checks. Traced `renderData()`'s new branch
  against this payload by hand: `succeededRepoCount === 0 &&
  errors.length > 0` evaluates true, `renderFullError` fires before any
  other rendering path runs.
- F2: confirmed against `design-system.md` §3 — `status-warning`'s
  foreground/background pair is spec-documented at 6.8:1 contrast; the
  fix now uses that pair directly instead of the primary-action color.
- F3/F4: CSS changes reviewed directly against `screen-spec.md` §1.6/§5
  and `design-system.md` §5's breakpoint table; the grid/media-query
  rules match the specified breakpoints and column behavior. Not
  exercised in an actual browser viewport (no browser available in this
  session) — verified by structural/code review only for these two.

loop_state: landed

## Open findings

None new. Out-of-scope item carried from the proposal (not part of
F1–F4, not fixed here): `RoleChip` `font-family-mono` applied to the
whole `role:loop_state` chip text rather than only the state segment
(`dashboard.js:128`), flagged by execution-observation.md as a separate
minor mismatch.
