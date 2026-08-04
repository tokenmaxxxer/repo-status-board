# Scout brief — execution-observation (issue #38)

Mode: **parallel fan-out**, 2 stages. Stage 1 = 4 concurrent search angles
(jsdom fidelity limits; audit practice for a substituted verification
procedure; what automated DOM testing can/can't establish for live
regions + focus; how audits judge self-reported test results). Stage 2 =
2 concurrent deepening searches aimed at the survey's open questions 7
and 4 (WCAG 2.5.8 static checkability; `min-width: 0` / table `min-width`
overflow mechanics). Saturation declared after stage 2 — a third round
would not change any decision in the proposal.

Angles were aimed at `survey.md` §5's open questions, chiefly Q2
(approved proposal promised live-browser verification; record delivered a
jsdom substitute) and Q3 (the record's own assertion counts disagree).

## Category must-bes

- Evidence is *verifiable records/statements*, and only information that
  can be subjected to some degree of verification counts as evidence
  (ISO 19011 6.4.7).
- When a planned procedure cannot be performed, proposing an alternative
  is legitimate — but it must be surfaced to the client/auditee and the
  sufficiency of what it collects re-assessed against the criteria, not
  swapped silently (ISO 19011 guidance; PCAOB AS 1105 "sufficient
  appropriate").
- Checking a *reported number against the actual output artifact* is a
  named audit step: "phantom results — claimed numbers that do not match
  actual output files" is one of the catalogued integrity failure modes.
- Automated/DOM-level tooling can confirm a live region's attributes
  exist; it cannot confirm the announcement behavior — that needs a real
  screen reader. Same shape for layout: jsdom has no layout engine and
  returns zeros for layout properties, and does not implement
  `matchMedia`.
- `min-width`/`min-height: 24px` genuinely creates a 24×24 target *given*
  a box type that honors it (`display: inline-flex` does); WCAG 2.5.8's
  inline exception covers in-sentence text links.

## Performance axes

1. Evidence traceability — every verdict sentence carries its own
   adjacent citation.
2. An explicit three-way partition: verified here / claimed by the
   observed role / not establishable by anyone in this environment.
3. Internal-consistency auditing of the record itself, not just of its
   conclusions.

## Adopt

- Issue-34's settled record shape (independence statement first,
  three-level verdict, AC table, four-part blameless finding,
  `loop_state`) — `docs/issue-34/proposals/execution-observation.md`.
- The audit frame for Q2: judge the *substitution* on disclosure +
  re-assessed sufficiency per criterion, rather than on whether jsdom is
  "as good as" a browser.
- The phantom-number check as a concrete step-level probe for Q3.
- Static CSS reading for Q7: the field says target-size and overflow
  outcomes are determined by properties readable in the stylesheet
  (`display` + `min-width`/`min-height`; `min-width: 0` on the flex/grid
  ancestor), so phase 2 reads the `dashboard.css` hunk instead of
  deferring both criteria to "unverifiable".

## Skip

- The execution-based claim verification the audit literature recommends
  (re-run the artifact, compare to reported numbers). This role's
  directive prohibits re-executing the observed work outright; phase 2
  substitutes static tracing plus internal-consistency checks and labels
  the observed role's pytest/jsdom results *claimed*.
- Treating the jsdom substitution as deficient by default. The same
  sources say DOM-level checks are legitimate for attribute/wiring
  facts — so phase 2 partitions the acceptance criteria by what a jsdom
  harness can support rather than rejecting the method wholesale.

## Gap line

Already met by the observed record: disclosure of the substitution and of
the `matchMedia` polyfill (`docs/issue-38/reports/implementation.md`
lines 104–123), and self-citing `closed_checks`. Missing against the
field's must-bes: (a) no per-acceptance-criterion re-assessment of what
the substitute procedure leaves unestablished — the disclosure is global,
not mapped to AC1/AC3/AC4; (b) the reported assertion counts are not
reconciled internally (survey Q3); (c) the two layout criteria are
treated as unmeasurable when the deciding properties are in fact
statically readable. Those three gaps are what the proposal's method
targets.

## Segment fit

Same role, same repo, same contract — the issue-34/issue-27 passes are a
direct comparator, not an analogy; the external sources supply only the
evidence-sufficiency lens the comparator never needed.

Sources:
- https://github.com/jsdom/jsdom/blob/main/README.md
- https://levelup.gitconnected.com/when-jsdom-for-testing-ui-its-not-enough-c53a8f8c4638
- https://preteshbiswas.com/2023/12/05/6-4-7-collecting-and-verifying-information/
- https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105
- https://www.tpgi.com/screen-reader-support-aria-live-regions/
- https://softwaretestingreviews.com/how-to-test-aria-live-regions-toasts-and-dynamic-alerts-without-missing-accessibility-regressions/
- https://arxiv.org/html/2604.04074v3 (FactReview — execution-based claim verification, incl. the "phantom results" failure-mode list)
- https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA19
- https://testparty.ai/blog/wcag-target-size-guide
- https://defensivecss.dev/tip/flexbox-min-content-size/
- `docs/issue-34/proposals/execution-observation.md` (this repo, `main`)
- `docs/issue-34/reports/execution-observation/scout-brief.md` (this repo, `main`)
</content>
