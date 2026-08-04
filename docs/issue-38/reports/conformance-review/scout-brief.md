# Scout brief — conformance-review of issue #38

Deliverable class scouted: an accessibility/responsive **conformance audit** of a
landed UI change. Field = how strong audits of this change class obtain and
record evidence. 2 stages (1 sweep of 4 angles + 1 deepening of 2 queries),
**parallel tool calls in one turn**, aimed at the survey's open unknowns
(`survey.md` §"Open unknowns"): rendered-layout evidence availability, jsdom
sufficiency, contrast recomputation, PR-body closing-keyword check.

**Category must-bes.** (1) Scope → explore → *sample derivation* → evaluate →
report, with outcomes recorded per criterion, is the accepted evaluation
skeleton (WCAG-EM); a stated sample derivation is required even when the answer
is "no sampling, full census." (2) A criterion an evaluator cannot observe is
reported as not-determined, not as passing. (3) Live regions must exist in the
initial DOM and be empty at load — a region created at announce time is a known
non-announcement. (4) 24×24px is checked *with* its Spacing / Inline / Essential
exceptions, not as a bare `min-width`/`min-height` grep.

**Performance axes the field competes on.** (a) Evidence class per finding
(rendered measurement > automated DOM assertion > source reading); (b)
determinacy — how few criteria end up "cannot tell"; (c) traceability — every
verdict carries a locatable pointer.

**Adopt.** Per-criterion evidence-class labelling, and the 24px-circle spacing
test as the R4 fallback path rather than a flat size check. **Skip.** Buying
determinacy by installing a browser stack (Playwright/Polypane) inside this
review — the harness decision is issue #44's, and a review that changes the repo
to grade itself stops being independent; unobservable stays Unverifiable.

**Gap line.** Current state already meets must-bes (1) and (3)'s *structural*
half — static `aria-live` sits in `index.html:13,20`, and the survey/proposal
pair supplies scope+census. Missing: must-be (2) is not yet operative (no
verdict record exists), must-be (4) is unmet as a *method* (no exception
analysis anywhere), and the field's top axis — rendered measurement — is
**unreachable here**: no browser, and jsdom implements no layout engine, so
`getBoundingClientRect`/`offsetWidth` are zeros. That gap is what forces the
proposal's evidence-class split rather than a promise of full determinacy.

**Segment fit.** Same segment: a small single-page dashboard audited against 9
plain-language criteria — WCAG-EM's site-wide sampling machinery is oversized,
its recording discipline is not.

Sources:
- https://www.w3.org/TR/WCAG-EM/
- https://w3.org/WAI/test-evaluate/conformance
- https://vispero.com/resources/how-to-test-2-5-8-target-size-minimum/
- https://wcag22aa.org/new-criteria/target-size/
- https://www.sarasoueidan.com/blog/accessible-notifications-with-aria-live-regions-part-2/
- https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA19
- https://polypane.app/blog/strategies-for-dealing-with-horizontal-overflows/
- https://www.smashingmagazine.com/2021/04/css-overflow-issues/
- https://github.com/jsdom/jsdom/issues/3621
- https://playwright.dev/java/docs/api/class-elementhandle
