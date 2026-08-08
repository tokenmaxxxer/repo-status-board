# Scout brief — issue #72

Mode: single WebSearch call (breadth was unnecessary — the survey already
located the fix mechanism in-repo; scouting here checks whether the
field's accepted practice for "responsive bug, no browser layout engine"
matches option (a) before recommending it). Stages used: 1 (sweep only;
saturated immediately — the top hits converged on one answer, judge point
1 found no disagreement worth a deepening round).

## Must-be (category consensus)

jsdom performs no CSS layout, so `offsetWidth`/`scrollWidth`/
`getBoundingClientRect` are always 0 there regardless of real markup —
confirmed independently of this repo's own finding. Assertions built on
those APIs in a jsdom test are not meaningful. Source:
[Testing element dimensions without the browser](https://dev.to/tmikeschu/testing-element-dimensions-without-the-browser-5532).

## Performance axes / adopt-skip

- **Adopt**: assert the *CSS declarations* (e.g. `overflow-x: auto`,
  `min-width: 0`) and DOM structure (wrapper class) that the fix depends
  on are present — this is the accepted jsdom-tier check when real layout
  can't be computed. Source: [Testing element dimensions without the browser](https://dev.to/tmikeschu/testing-element-dimensions-without-the-browser-5532)
  ("you can verify truncation by asserting the expected CSS properties are
  present").
- **Skip**: comparing `offsetWidth`/`scrollWidth` inside jsdom — both are
  always 0, so the comparison is a tautology, not a regression check.
  Same source.
- **Boundary named by the field, not just this repo**: real pixel-level
  overflow regression detection needs an actual rendering engine
  (Cypress/Playwright-class tooling) — exactly the "visual regression"
  class issue #44's 범위 밖 already excludes. Source: same article,
  "Best Practices for jsdom Testing" section.

## Gap line

The current artifact already meets the field's jsdom-tier must-be for
*other* wiring defects (DOM event dispatch, attribute assertions — see
R1-R4 in `docs/issue-44/reports/conformance-review.md`). It is missing the
CSS/structure-assertion pattern specifically for the layout-dependent
defect class (mobile-overflow), which the field treats as a distinct,
addressable sub-case of DOM testing rather than something that must be
pushed to visual regression. That gap is what option (a) in the survey
closes.

## Sources

- https://dev.to/tmikeschu/testing-element-dimensions-without-the-browser-5532
