# Scout brief — issue #4, ux-engineering phase 1

Stages used: 1 sweep (3 parallel WebSearch angles: token architecture/
naming, dense-admin-dashboard systems, accessible color pairing) + 1
judge point, no deepening round needed (sources converged strongly on
one architecture — saturation reached at judge point 1). Mode: parallel
(3 WebSearch calls in one turn). Wall-clock: well under budget.

## Must-bes (Kano) — every serious system has these
- Three-layer token hierarchy: primitive → semantic → component
  (e.g. `blue-500` → `action-color` → `button-primary-background`).
  Convergent across all three angles.
- Explicit foreground/background (on-color) pairing as a naming
  contract, not an afterthought: seeing `button-primary-background`
  should predict `button-primary-foreground` exists.
- WCAG contrast floor on every color pair: 4.5:1 normal text, 3:1
  large text/large UI elements.
- Semantic naming by purpose, not appearance (`color-alert-error`, not
  `red`).

## Performance axes (where strong systems visibly compete)
1. **Density control** — dense admin/data systems (Carbon, this
   project's own five-table layout) give the data table the most page
   width and treat density as a first-class scale choice, not an
   afterthought of the marketing-page spacing scale.
2. **Governance/discoverability** — token docs as a live reference
   surface, not static; a single naming convention holds cross-
   discipline. (Adopted lightly: this repo's proposal doc itself is
   the reference surface — no separate tooling exists to build.)
3. **Status-color completeness** — enterprise dashboards define a
   full semantic status set (info/success/warning/error/neutral) with
   pre-validated on-color pairs, not just a couple of ad hoc colors.

## Adopt
- Primitive→semantic→component three-layer token structure (near-
  universal convergence; this repo has zero legacy tokens to
  reconcile against, so adopting it cleanly costs nothing).
- Foreground/background pairing convention for every color token.
- WCAG 4.5:1 / 3:1 contrast floor, checked by hand for each pair
  defined (no build-time validator exists in this token-less repo yet
  — that tooling is out of scope for a docs-only proposal).

## Skip
- Style Dictionary / automated cross-platform token build pipeline
  (Contentful, zeroheight pattern) — this pilot ships one web surface
  from one team; a build pipeline is premature infrastructure for a
  docs proposal with no consuming build step yet.
- Multi-density-mode switcher (some dashboards ship 3 density levels)
  — screen-spec.md defines one screen, one density; a mode switcher is
  unrequested scope.

## Gap line
Current state (per survey.md) has zero tokens of any kind — every
must-be above is missing, not partially met. The proposal must supply
all four must-bes from scratch; there is no legacy convention to
reconcile, which simplifies the primitive/semantic split (no renaming
debt).

## Segment fit
This is an internal ops status dashboard (data-dense, read-only,
single operator persona), not a consumer or marketing product —
closest fit is enterprise/admin systems (Carbon, Primer), not
consumer design systems (Material's broader animation/elevation
apparatus is over-scoped for this pilot and is skipped).

Sources:
- https://timgraf.com/ui/design-token-architecture-2026-the-strategic-blueprint-for-scalable-design-systems/
- https://zeroheight.com/blog/how-to-start-a-design-token-system-with-confidence/
- https://www.netguru.com/blog/design-token-naming-best-practices
- https://carbondesignsystem.com/components/data-table/usage/
- https://github.com/carbon-design-system/carbon
- https://www.aufaitux.com/blog/color-tokens-enterprise-design-systems-best-practices/
- https://designsystem.digital.gov/design-tokens/color/overview/
- https://supercharge.design/blog/a-guide-to-colors-in-design-systems
