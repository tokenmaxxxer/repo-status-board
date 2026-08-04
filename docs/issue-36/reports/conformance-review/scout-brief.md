# Scout brief — issue #36 conformance-review

Mode: **parallel**, 4 angles dispatched concurrently in one turn (a11y
must-bes for link+disclosure changes; conformance-evidence norms; link-vs-button
review checks; doc/token-drift audit practice). **2 stages total** (1 sweep +
1 judge point); saturation reached — a further deepening round would not
change a method decision, so deepening was not run. Angles were aimed at the
survey's §5 gaps (no browser, skipped DOM tests, self-ratifying spec edit).

**Category must-bes (audits of a colour-only link + icon disclosure).** A link
distinguished from body text by colour alone must clear **3:1 against the
surrounding text** *and* 4.5:1 against the background, plus a non-colour cue on
hover **and** focus [G183]. Icon-only buttons must be named on the button with
the glyph `aria-hidden` [Soueidan], and the name must **disambiguate per row**
[Level Access]. `aria-expanded` must be present in both states; Enter *and*
Space must activate [APG disclosure]. `aria-controls` is *optional* per APG and
weakly supported [Pickering, a11ysupport] — so "missing" is not a violation,
but an IDREF that resolves to the **wrong or empty** element is one, since it
asserts a false programmatic relationship [WAI-ARIA 1.2 §aria-controls].

**Category must-bes (conformance-evidence norms).** A test that did not execute
is **blocked**, not passed [ISTQB]; treating skips as passes is a reported
defect class, not a reporting style [dorny/test-reporter #539, pytest #3730].
Multi-valued verdicts are standard practice: ISO/IEC 9646's *inconclusive* is
exactly "neither pass nor fail can be assigned" — the ancestor of this role's
`Unverifiable`. For rendered-layout claims, screenshots and CSS rules carry
non-substitutable information; rule inspection is analysis of a cause, not
observation of the outcome [Vitest visual-regression, desplega.ai].

**Performance axes** (what separates a strong audit here from a weak one):
(1) evidence *executed* vs merely *present*; (2) verdict granularity — refusing
to collapse "shipped but unobservable" into pass or fail; (3) scope discipline —
judging the issue's enumerated targets, not the whole file.

**Adopt.** (a) Run `npm install --prefix test` before the suite and report
skip counts before/after, because the four disclosure tests otherwise silently
skip (survey O3) — grounded in the blocked-≠-passed rule [ISTQB, pytest #3730].
(b) Compute the G183 3:1 link-vs-body-text ratio from the declared tokens
(`#2563eb` vs `#111827`) rather than eyeballing "it's blue" [G183]. (c) Judge
`aria-controls` on *IDREF correctness per layout branch*, not presence
[WAI-ARIA 1.2]. (d) Check docs **bidirectionally** — spec→code and code→spec,
with a residual-mention sweep for the removed ↗ — per the docs-audit
outdated-vs-undocumented two-class split [Docuwriter].

**Skip.** (a) Deliberately **not** scoring `aria-controls` presence as a
requirement, and not importing WCAG 2.5.5 AAA (44px) or 3.2.5 new-tab-warning
as pass/fail criteria — issue #36 asks for none of them, and APG/Roselli show
both are contested; they belong in an observation, not a verdict. (b) Not
adopting visual-regression tooling — outside this role's write-set and the
sandbox's means; the honest output is `Unverifiable`, not a proxy metric.

**Segment fit.** The exemplars are conformance/a11y *audit* practice, the same
deliverable kind as this role's phase-2 record — not product UI work.

**Gap line.** Already met by the current state: `aria-expanded` in both states,
native `<button type="button">`, `aria-hidden` glyph, per-row-disambiguating
`aria-label`, 24×24 target, non-colour cue on hover+focus. Not met / unknown:
executed evidence for the disclosure behaviour (tests skip), rendered evidence
for the no-wrap claim (no layout engine), and IDREF correctness in the
narrow-layout branch. Those three gaps are what the requirement list's methods
aim at.

Sources:
- https://www.w3.org/WAI/WCAG22/Techniques/general/G183
- https://webaim.org/blog/wcag-2-0-and-link-colors/
- https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/
- https://www.w3.org/TR/wai-aria-1.2/#aria-controls
- https://heydonworks.com/article/aria-controls-is-poop/
- https://a11ysupport.io/tech/aria/aria-controls_attribute
- https://www.sarasoueidan.com/blog/accessible-icon-buttons/
- https://www.levelaccess.com/blog/aria-labels-and-accessible-names-a-developers-guide/
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- https://adrianroselli.com/2020/02/link-targets-and-3-2-5.html
- https://glossary.istqb.org/
- https://github.com/pytest-dev/pytest/issues/3730
- https://github.com/dorny/test-reporter/issues/539
- https://www.iso.org/standard/17473.html
- https://vitest.dev/guide/browser/visual-regression-testing
- https://www.desplega.ai/blog/deep-dive-7-visual-regression-testing-ui-bugs
- https://www.docuwriter.ai/posts/documentation-audit
- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
