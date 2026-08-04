# Scout brief — execution-observation (issue #36)

Pass shape: **2 stages** (stage 1 sweep = 4 angles dispatched as
concurrent `WebSearch` calls in a single turn — genuine parallel tool
calls, not a serialized loop; stage 2 = judge point, saturation reached,
no deepening round run). Angles were aimed at survey §5's gaps, not at
the issue text: gap 1/6 → audit-evidence standards; gap 2/3 → jsdom's
limits as a browser substitute; gap 2/5 → what an ARIA disclosure audit
actually checks; gap 4 → how strong reviews treat scope beyond plan.

## Category must-bes (what strong audits of this class assume)

- **Evidence vs. assertion is a hard line.** Without a traceable record
  of who produced a result, when, and how its integrity held, the result
  is an assertion, not evidence — and independent confirmation outranks
  self-attestation in every evidence hierarchy surveyed.
- **jsdom settles no layout and only approximates focus/keyboard.**
  jsdom does no layout and no rendering, so anything depending on what
  paints cannot be checked there; synthetic-event approaches break down
  precisely at "what happens when Tab is pressed" (`jsdom#1634` is the
  long-standing keyboard-dispatch case).
- **Disclosure audits check three concrete things:** the control is a
  real `<button>`; `aria-expanded` stays synchronized with *actual*
  visibility; `aria-controls` references the id of the container that is
  really toggled.
- **Scope is judged relationally, not absolutely.** Google's review
  guidance permits addressing related concerns in the same change so
  long as the change stays small — so a scope finding must argue
  relatedness and size, never "unrequested therefore wrong".

## Performance axes strong audits compete on

1. Per-verdict traceability to a primary artifact (SHA / file:line / URL).
2. Explicit separation of *demonstrated* from *asserted-only* claims.
3. Scope discipline measured against the approved plan, not taste.

## Adopt / skip

- **Adopt:** an explicit demonstrated-vs-asserted label on every one of
  issue #36's seven acceptance criteria, and the three-item disclosure
  checklist above as the literal a11y check list for AC3.
- **Skip:** running axe-core, a real browser, or the test suite myself.
  This role's rules forbid re-executing the observed task, and the field
  already supplies a third-party artifact for the same wiring — issue
  #44's `test/rsb_tests/test_dashboard_dom.py` (commit `b2f6b63`, on
  `main`), whose own message states its tests were verified to fail
  against `b621082^`.

## Gap line

Present in the observed state: the disclosure checklist's three concrete
items each appear as a claim in
`docs/issue-36/reports/implementation.md`, and the jsdom-vs-browser
substitution is stated there in the open, with raw run output inline —
so must-be 1's traceability question ("who, when, how") has material to
work with. Absent: any independent confirmation of those claims
(must-be 1's top tier), and any artifact at all bearing on the
layout-dependent criterion (must-be 2). Those two absences are what this
role's phase 2 aims its method at.

## Segment fit

This is a small internal single-repo status dashboard with no CI
accessibility gate, not a product shipping to external users — so the
bar this brief sets is "does each claim's evidence support it", not a
full WCAG conformance audit.

Sources:
- https://audit-ready.eu/en/blog/audit-evidence
- https://www.zengrc.com/blog/role-of-self-attestation-in-compliance-benefits-challenges/
- https://github.com/jsdom/jsdom
- https://github.com/jsdom/jsdom/issues/1634
- https://dev.to/kevinccbsg/automated-accessibility-testing-axe-core-keyboard-navigation-and-wcag-in-the-browser-2eib
- https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-card/
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-expanded
- http://adrianroselli.com/2019/09/table-with-expando-rows.html
- https://abseil.io/resources/swe-book/html/ch09.html
- https://github.com/google/eng-practices
