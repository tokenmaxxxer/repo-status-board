# Scout brief — issue #81

Stage count: 1 (sweep only; saturation reached, no deepening needed).
Mode: single WebSearch call — not parallel fan-out (one well-defined
question, not multiple independent angles). Wall-clock: <1min, inside
budget.

## Category must-bes (field consensus)

- DOM/structural assertions are considered adequate, low-noise coverage
  for markup/CSS-declaration correctness, but are explicitly known to
  miss anything that only manifests visually (color/contrast, rendering,
  layout not captured by the asserted declarations) [1][4].
- Visual-regression tooling's stated value proposition is strongest when
  a component/pattern is *reused across many screens* — one baseline
  approval verifies all of them at once — and weakest for a single
  small, low-reuse surface, where its main cost (flakiness from
  anti-aliasing/font-rendering noise, baseline maintenance) has less to
  offset against [1][3].

## Performance axes field tools compete on

1. Setup/maintenance cost (headless browser infra, baseline storage,
   CI time) vs. false-positive rate from rendering noise.
2. Catch-rate for layout-only defects (only real-browser tools resolve
   intrinsic-width/overflow correctly — jsdom-tier structural checks
   cannot compute layout, confirmed in `docs/issue-72/reports/
   requirements-engineering.md`'s own residual-gap note).
3. Reuse scale of the UI surface under test (single-page vs. multi-screen
   design system) — determines how much one visual-regression baseline
   amortizes.

## Pattern to adopt / pattern to skip

- Adopt: treat "reuse scale" and "occurrence rate of the uncaught failure
  mode" as the deciding variables, not "is visual regression better in
  the abstract" (it is, on catch-rate, but that is not the question).
- Skip: standing up full pixel-diff infra (Percy/Applitools/Playwright
  visual snapshots) speculatively, absent an occurrence-rate or
  cost-per-incident number — the field sources frame that investment as
  paying off at multi-screen/component-reuse scale, which rsb's single
  4-table dashboard does not exhibit today (`dashboard.js`/`.css` at
  710/426 lines, no design-system reuse pattern found).

## Segment fit

`rsb` is a single internal team dashboard, not a customer-facing product
with a design system — closer to the field's "small internal tool"
segment than the "50-screen component reuse" segment the visual-tooling
case study cited.

## Gap line

REQ-72-1..3 already meet the field's "structural/DOM assertion" must-be
(low-noise, catches the known fingerprint). What they do not meet — and
what the field explicitly says only real-browser tooling can — is
catching layout regressions from an *unfingerprinted* mechanism (new
element pushing width) and any non-layout visual defect (contrast,
rendering). This proposal's hypothesis test targets exactly that
uncovered mechanism, not a general "is visual regression good" question.

## Assumption (labeled, not sourced)

rsb has no page-view or defect-report volume instrumentation (verified:
zero grep hits for analytics/pageview/access-log in `src/`), so
occurrence-rate and cost-per-incident cannot be looked up — they must be
measured going forward. This is stated as a missing-instrumentation
finding in the proposal, not assumed away.

## Sources

- [1] [What is Visual Regression Testing? | BrowserStack](https://www.browserstack.com/percy/visual-regression-testing)
- [2] [Guide To Visual Regression Testing With Visual Testing Tools](https://www.softwaretestinghelp.com/visual-validation-testing/)
- [3] [Visual Regression Testing: Catch Bugs Tests Miss](https://bugbug.io/blog/software-testing/visual-regression-testing/)
- [4] [What Is Visual Regression Testing? A Complete Guide | TestMu AI](https://www.testmuai.com/learning-hub/visual-regression-testing/)
