# Fix proposal — F1–F4 (issue #13)

Status: phase-1 proposal. Fixes conform the implementation to the
frozen `docs/specs/design-system.md` / `docs/specs/screen-spec.md`; no
spec edits. Source of truth for what each finding means:
`docs/issue-4/reports/execution-observation.md` §6. Current-state
details: `docs/issue-13/reports/implementation/survey.md`.

## F1 — full-page ErrorState unreachable on total repo failure

**Root cause**: `webserver.py` always returns HTTP 200 (by design,
matching `test_webserver.py`'s partial-failure-still-200 contract —
out of scope to change). `dashboard.js`'s `renderFullError()` is only
invoked from `load()` on a non-2xx status or a `fetch` exception
(`dashboard.js:291-298`). A 200 response whose payload has every
configured repo in `errors` and none in `generated_at_by_repo` never
hits either path, so it falls into `renderData()`'s `isPageEmpty()`
branch (`dashboard.js:255-258`), which doesn't inspect `errors` at all.

**Fix**: add a payload-level total-failure check in `renderData()`,
evaluated before the `isPageEmpty()` branch (and before the partial-
banner branch, since a partial failure by definition has at least one
succeeding repo and can't also be total):

```js
const succeededRepoCount = Object.keys(data.generated_at_by_repo).length;
if (data.errors.length > 0 && succeededRepoCount === 0) {
  renderFullError(data.errors.map((e) => `${e.repo}: ${e.message}`).join("; "));
  return;
}
```

placed at the top of `renderData()`, before the summary-strip/partial-
banner code that currently runs unconditionally
(`dashboard.js:230` onward). This reuses the existing `renderFullError`
(§2.4 markup: "Couldn't load board status" heading + Retry button,
already correct) — no new render function needed. The HTTP-level checks
in `load()` stay as-is (they cover network failure / non-2xx, a
different case from "server responded but every repo failed").

Rationale for client-side (not server-side) fix: the server-always-200
contract is asserted by an existing passing test
(`test_webserver.py`) and is the correct behavior for the partial-failure
case (§2.5) — a status-code-based signal can't distinguish partial from
total failure without duplicating information already in the JSON body.
The `errors` + `generated_at_by_repo` payload already carries everything
`dashboard.js` needs; no server change is warranted.

## F2 — partial-failure banner Retry link contrast

**Root cause**: `dashboard.css:187-195` sets `.partial-banner a,
.partial-banner button.link { color: var(--color-action-primary-
foreground); }` — white text on `--color-status-warning-background`
(`#fffbeb`), ~1:1 contrast. `screen-spec.md` §2.5 named the fallback
for exactly this case: `status-warning`'s own foreground token.

**Fix**: one-property change —

```css
.partial-banner a, .partial-banner button.link {
  color: var(--color-status-warning-foreground);
  ...
}
```

`--color-status-warning-foreground` (`amber-700`) already carries a
documented 6.8:1 ratio against the warning background
(`design-system.md` §3), inherited automatically since the link sits
inside `.partial-banner` which already sets that background.

## F3 — DetailPanel breakpoint-lg layout switch

**Root cause**: `screen-spec.md` §1.6/§5 and `design-system.md` §5
specify a real layout switch at `breakpoint-lg` (1200px): side panel
at/above, expandable row below. The shipped markup renders `MAIN`'s
regions and the detail panel as one flat HTML string
(`dashboard.js:260-283`) with the panel simply appended last; the only
CSS at 1200px is `position: sticky` (`dashboard.css:230-232`), which
doesn't create a second column — there's nothing beside it to place a
sticky panel next to.

**Fix**: wrap the regions and the detail panel in a grid container so
CSS alone can switch column count at the breakpoint, without touching
region markup itself:

- `dashboard.js`: introduce a `PAGE_BODY` wrapper element (add
  `<div id="page-body">` around `MAIN` in `index.html`, or restructure
  `renderData()` to build the regions block and the detail-panel block
  as two separate strings and inject them into two sibling elements —
  `#main-content` (regions) and `#detail-panel-slot` (panel, empty
  string when `selectedIssue` is null) — both children of a
  `#page-body` grid container). This is a DOM-structure change, not a
  behavior change: same content, split across two named slots instead
  of one concatenated string.
- `dashboard.css`:

```css
#page-body {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}
@media (min-width: 1200px) {
  #page-body:has(#detail-panel-slot:not(:empty)) {
    grid-template-columns: 1fr minmax(280px, 340px);
    align-items: start;
  }
  .detail-panel { position: sticky; top: var(--space-4); }
}
```

Below 1200px, the single-column grid keeps today's behavior (detail
panel renders as a full-width block after the regions — the
"expandable row" mode screen-spec.md describes). At/above 1200px with a
panel present, the grid switches to two columns, panel on the side. The
existing `position: sticky` rule is kept (still correct at ≥1200px) but
now sits beside real second-column content rather than being the only
breakpoint effect. (`:has()` is supported in the browser baseline this
project already targets — same class of browser needed for `fetch`/ES
modules already in use; if broader compatibility is later required,
the `has(...)` selector can be replaced with a
`page-body.has-detail`-style JS-toggled class instead — noted as an
alternative, not adopted here to keep the diff minimal.)

## F4 — missing breakpoint-md (768px) rule

**Root cause**: `design-system.md` §5's `breakpoint-md` row describes
two behaviors below 768px: summary-strip chips wrap to 2 rows (already
works, incidentally, via `.summary-strip`'s unconditional
`flex-wrap: wrap`), and the detail panel forced into expandable-row
mode (already true below 1200px per F3's fix, so no separate action
needed there — F3's single-column default already covers 320–1199px,
which includes the whole sub-768px range). No `@media (max-width:
768px)` rule exists anywhere in `dashboard.css`, so the spec's stated
breakpoint token has no corresponding CSS rule at all, even though
the incidental behavior happens to match today.

**Fix**: add the explicit rule so the token is backed by real CSS
rather than incidental flex-wrap, and reserve the block for anything
breakpoint-md-specific found in review:

```css
@media (max-width: 768px) {
  .summary-strip { gap: var(--space-2); }
}
```

This keeps existing chip-wrap behavior (already correct) while making
the 768px breakpoint a real, present CSS boundary rather than an
emergent side effect — closing the literal "no such rule exists" gap
execution-observation.md flagged, without changing any visible
behavior at this width (nothing currently renders differently there
that needs to).

## Out of scope (not part of F1–F4, noted for a future issue)

- RoleChip `font-family-mono` applied to the whole `role:loop_state`
  chip text rather than only the state segment
  (`dashboard.js:128`) — flagged by execution-observation.md as a
  separate minor mismatch, not one of F1–F4; not fixed here to keep
  this PR scoped to the four findings the issue names.

## Verification plan (phase 2, after approval)

- Re-run `python3 -m pytest test/ -q` (existing 33 tests must still
  pass — none of F1–F4's fixes touch `webserver.py` or `render.py`).
- Reproduce each of the four states live via the same throwaway-script
  approach execution-observation.md used (`run_server()` with crafted
  `fetch_board_fn`s bound to distinct ports, driven with `curl`/direct
  HTML inspection), confirming: total-failure payload now renders
  `error-state` markup (F1); partial-banner Retry link text is visible
  against the warning background — verify computed contrast, not just
  that a different token is referenced (F2); detail-panel DOM at
  ≥1200px viewport width sits in a second grid column beside `MAIN`,
  and single-column below (F3); a `@media (max-width: 768px)` rule is
  present and does not regress chip wrapping (F4).
- No spec changes to diff against — `design-system.md`/`screen-
  spec.md` stay frozen throughout.
