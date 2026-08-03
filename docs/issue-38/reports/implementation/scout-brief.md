# issue-38 scout brief

Mode: parallel sweep, 4 angles in one turn (CSS grid/flex `min-width: 0`
overflow fix; WAI-ARIA live-region/`aria-busy` practice; WCAG 2.5.8
target-size CSS implementation; accessible expandable-table-row
insertion + focus order). 1 stage total — all four angles returned
converged, well-established platform/WCAG guidance with no competing
exemplars to reconcile, so judge point 1 found nothing to swap and judge
point 2 (saturation) stopped before any deepening round: another round
would not change any of the four build decisions below. Elapsed:
~25s wall-clock (well inside the 3-min budget).

## Must-bes the field assumes

- **Overflow**: a CSS grid/flex item's automatic minimum size is its
  content's min-content size, not `0` — a wide child (like a
  `.table-scroll` wrapping a wide `<table>`) inflates its ancestor grid/
  flex item unless that item is explicitly given `min-width: 0`
  (or `overflow` other than `visible`). This is the textbook fix, not a
  workaround — Firefox/Chrome both document the same root cause.
- **Live regions**: `aria-live="polite"` for non-interrupting status
  changes (loading, partial-failure), `aria-live="assertive"` or
  `role="alert"` for errors needing immediate attention, `role="status"`
  for advisory-but-less-urgent updates, `aria-busy="true"`→`"false"`
  bracketing a region while its contents are still being assembled so
  AT doesn't announce a half-built DOM.
- **Touch targets**: WCAG 2.5.8 (AA) sets 24×24 CSS px as the floor,
  achievable via `min-width`/`min-height` or padding around a smaller
  visual glyph (a 16px icon + 4px padding on all sides = 24×24) — and
  explicitly exempts targets that are inline within a sentence/block of
  text, which is a real, named exception, not an edge case to ignore.
- **Expandable rows**: the newly-revealed row's `<tr>` should be
  positioned as the very next sibling of the row that triggered it, so
  a keyboard/screen-reader user moving forward from the trigger reaches
  the new content immediately — the same leading/forward-navigation
  principle issue-36's own scout-brief already established for the
  toggle button's position inside the cell.

## Performance axes strong exemplars compete on

1. Whether the live-region container is present in the DOM at page load
   (preferred) vs. injected dynamically (needs a delay before AT
   reliably picks it up) — favors static containers that just start
   empty.
2. Precision of the touch-target fix: invisible padding that enlarges
   the hit area without changing the visual glyph size, vs. visually
   enlarging the control itself and disturbing the page's existing
   density.
3. Whether the expandable-row insertion keeps a single source of truth
   for the detail content (one render function called from two
   insertion sites) vs. forking the markup.

## Adopt / skip

- **Adopt**: `min-width: 0` on `#main-content` (the grid item that
  contains the tables) as the primary fix — matches the survey's own
  root-cause read (survey §1) exactly, no alternative pattern needed for
  a single-column grid at this width.
- **Adopt**: `aria-live="polite"` on the header-meta/loading text and the
  partial-failure banner container (non-blocking status), `role="alert"`
  (implicitly assertive) on the full-page error state, and `aria-busy`
  toggling around `#main-content` while `renderSkeleton()`/`renderData()`
  are rebuilding it — matches the must-bes above one-for-one, no
  alternative live-region taxonomy considered since this maps cleanly
  onto the four states `screen-spec.md` §2 already names.
- **Adopt**: padding-based sizing for `.row-toggle` and explicit
  `min-height` for `#repo-filter`, keeping the visible glyph/text size
  unchanged — preserves this page's existing density (design-system.md
  §3's 4px dense-table spacing scale, not an 8px marketing scale) while
  meeting 24×24. **Skip**: enlarging `.number-link`'s visual size —
  treated as inline-text-exempt per the must-be above; phase-2 measures
  it to confirm rather than assuming further CSS changes needed here.
- **Adopt**: narrow-screen row insertion via a single render function
  (the existing `renderDetailPanel`) invoked from two call sites — one
  wrapping the result in a `<tr><td colspan>` inserted after the
  toggled row (narrow), one keeping today's `DETAIL_SLOT` assignment
  (wide) — never both at once. **Skip**: a fully separate/duplicated
  narrow-layout render path, which would fork the two rendering
  branches the field's single-source-of-truth axis above warns against.

## Segment fit

Same conclusion issue-36's own scout-brief reached: an internal ops
dashboard, not a consumer product needing bespoke interaction design —
every one of the four decisions above is "apply the documented
WCAG/ARIA/CSS-layout mechanism as specified," not a product-differentiation
choice. No exemplar product comparison was useful or attempted; the
right reference class here is the platform spec itself, which is what
the sweep searched.

## Gap line

Current state already meets: per-table `.table-scroll` isolation (issue
#29), a real `<button>` disclosure trigger with correct `aria-expanded`/
`aria-controls` wiring (issue-36), an existing `.detail-row` CSS rule
shape to build the narrow-layout `<tr>` from (unused today, survey §2),
and an established icon+`aria-label`+`aria-hidden` glyph convention
(issue-36) directly reusable for any new icon-only controls. Missing,
and what this brief aims the proposal at: the `min-width: 0` overflow
fix itself (nothing in the CSS does this today), any live region at all
(zero `aria-live`/`aria-busy`/`role="alert"` in the codebase), explicit
touch-target sizing (zero rules for `#repo-filter`, `.row-toggle` is
glyph-sized only), the narrow-screen row-insertion JS (`insertDetailRow`
is a comment, not a function), `<caption>`/`scope="col"`/detail-panel
heading (zero instances), and the duplicate-`<h1>` full-error bug (a
correctness gap the sweep's live-region angle surfaced as a side effect,
not something requiring its own search — fixing it is folded into the
error-state live-region work since both touch the same
`renderFullError` function).

## Sources

- [Grid and flexbox min-width — Miragecraft](https://www.miragecraft.com/blog/grid-and-flexbox-min-width)
- [Preventing a Grid Blowout | CSS-Tricks](https://css-tricks.com/preventing-a-grid-blowout/)
- [The Minimum Content Size In CSS Grid](https://ishadeed.com/article/min-content-size-css-grid/)
- [1114904 - Nested flexbox does not shrink overflowing content with overflow:auto — Mozilla Bugzilla](https://bugzilla.mozilla.org/show_bug.cgi?id=1114904)
- [ARIA: aria-busy attribute — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy)
- [The Complete Guide to ARIA Live Regions for Developers — The A11Y Collective](https://www.a11y-collective.com/blog/aria-live/)
- [ARIA-live announcements cheatsheet - assertive, polite or none?](https://rightsaidjames.com/2025/08/aria-live-regions-when-to-use-polite-assertive/)
- [WCAG 2.5.8 Target Size (Minimum): Complete Implementation Guide — AllAccessible](https://www.allaccessible.org/blog/wcag-258-target-size-minimum-implementation-guide)
- [WCAG 2.5.8: Target size (Minimum) (Level AA) — Silktide](https://silktide.com/accessibility-guide/the-wcag-standard/2-5/input-modalities/2-5-8-target-size-minimum/)
- [How to Create an Accessible Table with Clickable Rows](https://www.oidaisdes.org/blog/table-with-clickable-rows/)
- [Expanding Table rows - Can this be made accessible? — WebAIM discussion](https://webaim.org/discussion/mail_thread?thread=10795)
