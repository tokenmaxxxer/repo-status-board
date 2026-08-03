# issue-36 scout brief

Mode: parallel sweep, 4 angles in one turn (Adrian Roselli's expando-table
leading-column pattern; accessible data-table row-expand-vs-link-column
precedent generally; W3C ARIA APG disclosure-pattern button placement;
2025-era issue-tracker/data-table row link+chevron UI precedent). 1 stage
total — all four angles converged on the same shape (separate control,
leading position, native `<button>`, arrow/triangle glyph that flips with
state), so judge point 1 found no exemplar mismatch and judge point 2
(saturation) stopped before any deepening round: another round would not
change the placement decision below.

## Must-bes (Kano) the field assumes

- The expand/collapse control is a **native `<button>`**, kept **separate
  from** any link in the same row/cell — not overlaid, not nested (Adrian
  Roselli's expando-rows pattern; reinforced by the accessible
  data-table sweep's general finding that "the expand/collapse button
  should be kept separate as its own interactive control, distinct from
  any link columns in the table").
- `aria-expanded` communicates state on the button itself; `aria-controls`
  references the id of the container it toggles (W3C ARIA APG disclosure
  pattern).
- **Leading position, not trailing**: W3C APG discussion on expandable
  table rows notes it's "better placed at the start, so a screen-reader
  user hitting the down arrow key would be able to easily navigate
  across the newly-exposed rows" — this is the one point where issue-36's
  decision differs from issue #34's own scout-brief (which placed the
  *external-link* icon trailing, after the button). Carbon Design
  System's own row-expansion column follows the same leading convention
  (its open issue asking to *also* allow trailing placement confirms
  leading is the shipped/default choice, not an oversight).
- Glyph state pairs with `aria-expanded`: right-pointing arrow/triangle
  when collapsed, down-pointing when expanded — decorative
  (`aria-hidden="true"`), the accessible name comes from `aria-label`,
  not the glyph (W3C APG disclosure pattern examples).

## Performance axes strong exemplars compete on

1. Screen-reader navigation flow after activating the toggle — leading
   position lets the newly-revealed content be reached by continuing
   forward, not by reversing direction.
2. Visual density — in a dense data table, the toggle reads as a small,
   low-weight glyph, not a labeled button competing with the row's data.

## Adopt / skip

- **Adopt**: keep the disclosure control at the **start** of the Issue
  cell (before the new `#<n>` link), as an icon-only `<button
  class="row-toggle">` holding a decorative `▸`/`▾` glyph
  (`aria-hidden="true"`) that flips with `aria-expanded`, plus an
  explicit `aria-label` (e.g. "Toggle details for issue 42") carrying the
  accessible name the glyph no longer can. Both control and link stay
  siblings inside one no-wrap inline wrapper, matching the must-be above
  and directly fixing the line-wrap defect the issue body reports
  (survey §4).
- **Adopt**: a dedicated new leading table *column* (Carbon Design
  System's shipped convention) is available but not adopted here —
  **skipped** in favor of keeping the toggle inside the existing Issue
  cell. Reasoning in the proposal's Rationale (segment-fit argument
  below applies directly).
- **Skip**: trailing placement (after the link, mirroring issue #34's
  external-link position) — contradicts the leading-position must-be
  found independently in both the APG-focused and general-accessible-
  table search angles.
- **Skip**: whole-`<tr>` click or wrapping the link around the button —
  already excluded by the issue body itself and by the must-be above;
  restated here only because it was the literal alternative the sweep
  was checking for and none of the four angles supported it.

## Segment fit

Same conclusion issue #34's own scout-brief reached and still true here:
this is a small internal ops dashboard, not a dense enterprise grid
product (Carbon's target). Carbon's dedicated expand-column convention
is real precedent that a leading position is right, but adopting a whole
extra table column across four tables (with header-row and
`screen-spec.md` column-list changes in all of them) is disproportionate
scope for a segment that doesn't need a formal grid system — an in-cell
leading button reaches the same accessible-name/position must-bes with a
one-line markup change per row instead of a table-structure change.

## Gap line

Current state already meets: a real disclosure `<button>` exists per
cell, `.external-link`'s icon-only + `aria-hidden` + `aria-label`
convention is already established in this codebase (issue #34) and
transfers directly to the relocated toggle's glyph. Missing, and what
this scout aims the proposal at: the toggle's *new* position relative to
the link (resolved: leading, in-cell — not a new column, not trailing),
its glyph/state convention (resolved: `▸`/`▾` paired with
`aria-expanded`), and whether relocating it is also the moment to correct
the `aria-controls`/`aria-expanded` wiring gaps survey §2 found (a
judgment call the proposal makes, not something scout resolves — no
field precedent applies to "should you fix a bug you're already touching
files for").

## Sources

- [Table with Expando Rows — Adrian Roselli](http://adrianroselli.com/2019/09/table-with-expando-rows.html)
- [Table with Expando Rows | CSS-Tricks](https://css-tricks.com/table-with-expando-rows/)
- [Expanding Table rows - Can this be made accessible? — WebAIM discussion](https://webaim.org/discussion/mail_thread?thread=10795)
- [Accessibility - Data table — Carbon Design System](https://carbondesignsystem.com/components/data-table/accessibility/)
- [Data Table: Allow alternative locations for expand chevron button · Issue #7098 — carbon-design-system/carbon](https://github.com/carbon-design-system/carbon/issues/7098)
- [Disclosure Pattern | APG | WAI | W3C](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)
- [Example Disclosure (Show/Hide) for Image Description | APG | WAI | W3C](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-image-description/)
