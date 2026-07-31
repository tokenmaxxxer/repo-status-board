# Current-state survey — implementation (issue #13)

Status: phase-1 survey. Scope: fixing verification findings F1–F4 from
`docs/issue-4/reports/execution-observation.md` §6, against the frozen
specs `docs/specs/design-system.md` and `docs/specs/screen-spec.md`
(no spec edits in scope).

## Skip condition check (scout-directive)

Scouting **skipped** — condition 1 (pure bugfix). Each of F1–F4 is a
defect against an already-frozen, already-approved spec pair
(`design-system.md`, `screen-spec.md`); the fix's shape (what correct
looks like) is dictated line-by-line by those specs and by the verifier's
findings themselves, leaving no open product/design decision for this
role to steer with external research.

## Write surface

- `src/rsb/web/dashboard.js` — client-side dispatch logic.
- `src/rsb/web/dashboard.css` — token usage, breakpoint rules.
- No changes anticipated to `src/rsb/webserver.py` (see F1 analysis below
  — server already returns the data needed; the gap is client-side).
- Test coverage: `test/rsb_tests/test_webserver.py` covers the JSON
  contract only; no existing test drives `dashboard.js` rendering logic
  (execution-observation.md §1's "not possible without a browser" note
  still holds in this environment — no Node/browser execution available
  per that record). Phase 2 will need to decide how (if at all) to add
  regression coverage for the pure-function parts of `dashboard.js`
  (`ageBucket`, `isPageEmpty`-style helpers) already exported via
  `module.exports` at the bottom of the file, since those *can* run
  under plain Node/CommonJS without a DOM.

## Findings recap (from execution-observation.md §6, verbatim source of truth)

- **F1** (significant): total-repo-failure payload (`errors` populated,
  `generated_at_by_repo` empty) is indistinguishable client-side from a
  genuinely empty board — `isPageEmpty()` doesn't inspect `errors`, and
  `renderFullError()` is only invoked on HTTP non-2xx/network exception,
  never on a 200 response with an all-error payload (server intentionally
  always returns HTTP 200 per `test_webserver.py`'s
  partial-failure-still-200 contract, which is out of scope to change).
- **F2** (significant): `.partial-banner a, .partial-banner
  button.link` in `dashboard.css` uses
  `--color-action-primary-foreground` (`neutral-0` / white) as text
  color on `--color-status-warning-background` (`#fffbeb`, near-white)
  — effectively invisible. `screen-spec.md` §2.5 anticipated exactly
  this and named the fallback: warning's own foreground token.
- **F3** (minor): `screen-spec.md` §1.6/§5 and `design-system.md` §5
  specify a real layout switch at `breakpoint-lg` (1200px) — side panel
  above, expandable row below. Shipped CSS only adds `position: sticky`
  above 1200px; `DetailPanel` is a single always-full-width block
  appended after `MAIN` at every width, so there is no side-panel layout
  to switch to.
- **F4** (minor): `design-system.md` §5's `breakpoint-md` (768px) row
  describes chip 2-row wrap (works today, incidentally, via
  unconditional `flex-wrap`) and forced expandable-row detail-panel mode
  below 768px. No `@media (max-width: 768px)` rule exists in
  `dashboard.css` at all.

## Current code, exact locations

- `src/rsb/web/dashboard.js:230-258` (`renderData`) — where F1's branch
  needs to land: `isPageEmpty(data)` check at line 255 short-circuits
  before any error-vs-empty distinction is made; `PARTIAL_BANNER` logic
  above it (lines 240-253) already computes `Object.keys(data.
  generated_at_by_repo).length` (`repoCount`-style), so the "zero
  succeeding repos, at least one error" condition is cheap to add
  alongside it.
- `src/rsb/web/dashboard.js:287-300` (`load`) — where the HTTP-level
  `renderFullError` calls already live (non-2xx / fetch exception); F1's
  new payload-level branch is a sibling condition, not a replacement.
- `src/rsb/web/dashboard.css:187-195` (`.partial-banner a, .partial-banner
  button.link`) — F2's single-property fix site.
- `src/rsb/web/dashboard.css:221-232` (`.detail-panel`, the 1200px media
  query) and `dashboard.js:260-283` (`renderData`'s template, where
  `MAIN` and the detail panel are both written into one HTML string with
  no wrapping element to apply a two-column grid to) — F3 needs both a
  DOM-structure change (a wrapping element grouping `MAIN`'s regions and
  the detail panel as CSS grid siblings) and a CSS rule.
- `src/rsb/web/dashboard.css` — no existing 768px rule anywhere; F4 is a
  net-new `@media (max-width: 768px)` block.

## Constraints carried forward

- `docs/specs/design-system.md`, `docs/specs/screen-spec.md`: frozen,
  no edits.
- `docs/issue-4/reports/execution-observation.md`: verification record,
  read-only source of truth for what F1–F4 mean; not re-litigated here.
- This PR is phase-1 only per role-handoff contract v3 s19: this survey
  and `docs/issue-13/proposals/implementation.md` are the only files
  this phase adds. No `src/`/`test/` changes, no
  `docs/issue-13/reports/implementation.md` (that is phase-2 output,
  gated on an approvers.md account's `APPROVE issue-13/implementation`).
