# issue-34 scout brief

Mode: parallel sweep, 3 angles in one turn (external-link-icon-next-to-
button a11y pattern; dashboard/tracker issue-number-link UX precedent;
WAI-ARIA icon-only-link accessible-name guidance). 1 stage total — the
combined sweep results converged on the same shape from all three angles,
so judge point 1 found no exemplar mismatch and judge point 2 (saturation)
stopped before any deepening round: another round would not have changed
the placement or accessible-name decision below.

## Must-bes (Kano) the field assumes

- A disclosure/toggle `<button>` and an external-navigation control are
  kept as **separate, sibling focusable elements**, never one overlaid on
  the other or nested inside each other — confirmed by the Adrian Roselli
  expando-table pattern and reinforced by GitLab's own "icon/link to
  issues... even outside GitLab" pattern next to (not replacing) the row
  identifier.
- Icon-only link controls carry an explicit accessible name (`aria-label`)
  describing the destination and action; the icon glyph itself is
  `aria-hidden="true"` (decorative) since the label already carries the
  meaning (W3C APG Button Pattern / eBay evo-web icon-button a11y docs).
- Source order matters for assistive tech: a new/adjacent control belongs
  immediately after the element it relates to, not before.

## Performance axes strong exemplars compete on

1. Clarity of *why* two controls sit in the same cell (label wording
   disambiguates "expand detail" vs. "open on GitHub").
2. Minimal visual weight — external-link affordance reads as secondary to
   the primary row action, not competing for attention.

## Adopt / skip

- **Adopt**: place a small, separate `<a>` immediately after the existing
  `row-toggle` button (issue cells) / after the plain PR number (PR
  cells), each with its own `aria-label` ("Open issue N on GitHub" /
  "Open PR N on GitHub") and a decorative `aria-hidden="true"` glyph
  inside — matches the must-bes above and needs no new dependency (no SVG
  asset, a text glyph is enough for this internal tool's scope).
- **Skip**: overlaying/wrapping the link around the existing `row-toggle`
  button, or making the whole `<tr>` a link — both were the exact
  ambiguity the issue body itself already warned against, and both
  contradict the separate-sibling-elements must-be found across all three
  search angles.

## Segment fit

This is an internal ops status board (not a consumer product) — the
external-link affordance only needs to clear the accessibility must-bes
above; it does not need a polished icon system, animation, or a design
review beyond what `design-system.md`'s already-reserved tokens
(`--space-1` icon-to-label gap, `color-action-primary-*` for links)
support.

## Gap line

Current state already meets: real `<button>` disclosure pattern, correct
`aria-expanded`/`aria-controls` wiring, table-cell text conventions
(`.mono`, `escapeHtml`). Missing, and what this scout aims the proposal
at: any external-link control at all (first one in this codebase), its
placement relative to `row-toggle`, and its accessible-name convention —
all three now have a concrete adopt decision above.

## Sources

- [Table with Expando Rows — Adrian Roselli](http://adrianroselli.com/2019/09/table-with-expando-rows.html)
- [Display link to Jira from vulnerability Dashboard — GitLab #505612](https://gitlab.com/gitlab-org/gitlab/-/issues/505612)
- [Button Pattern | APG | WAI | W3C](https://www.w3.org/WAI/ARIA/apg/patterns/button/)
- [icon-button accessibility — eBay evo-web](https://opensource.ebay.com/evo-web/components/icon-button/accessibility)
