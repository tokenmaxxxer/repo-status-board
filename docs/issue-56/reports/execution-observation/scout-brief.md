# issue-56 execution-observation — scout brief

Mode: **parallel**, genuine concurrent dispatch — stage 1 fired 4
`WebSearch` calls in one turn (one per survey §5 gap G1–G4), stage 2
fired 2 more in one turn on G1 alone, which the sweep answered only
generically. **2 stages total**, 02:44:17Z → ~02:45:30Z (`date -u`
before/after) — inside the 5-stage / 3-min budget. Stopped at judge
point 2: no further round would change how this observation is aimed.
Field scouted = strong audits/reviews of *this* deliverable class (a
two-phase, self-approved doc+code change closing a prior review's open
findings), not the product's own domain.

## Category must-bes (what a strong review of this change class assumes)

- **A regression test closing an escaped defect is scoped to where the
  defect could reappear, not to where it was found.** Container-scoped
  queries silently miss anything rendered outside the container — the
  canonical case being portals, and it is exactly why
  `eslint-plugin-testing-library` ships `prefer-screen-queries` making
  document-scoped the default. [1][2]
- **Alternative (substituted) procedures are legitimate when the planned
  one cannot be performed — but only if they yield sufficient evidence
  *and* are documented as substitutions**; where they do not, the
  standard outcome is a recorded scope limitation, not silence. [3][4]
- **Deleting a spec section obliges cleanup of what pointed at it.**
  Design-system decay is described in exactly these terms: entries
  describing "something nobody builds anymore", dead references, and
  components mapped to code that no longer exists. [5][6]
- **Separation of duties: the author does not approve their own change.**
  Where a process nonetheless permits it, the compensating expectation is
  a tamper-evident record of the approval act itself. [7][8]

## Performance axes this observation will be judged on

1. **Citation density** — every verdict-bearing sentence carries its own
   adjacent SHA / `file:line` / comment URL.
2. **Literal-criterion discipline** — each AC read as written, with any
   satisfied-with-note called out rather than rounded up or down.
3. **Independence** — conclusions from produced artifacts only, never
   from re-running the observed role's work.

## Adopt / skip

- **Adopt**: the alternative-procedures test [3][4] as the yardstick for
  the record's jsdom-instead-of-browser substitution — pre-declared in
  the approved plan and documented ⇒ satisfied; undeclared ⇒ scope
  limitation to record.
- **Adopt**: assertion-scope-vs-recurrence-surface [1][2] as the yardstick
  for the new DOM test, since issue-38 F1's root cause was precisely a
  too-narrow assertion scope.
- **Skip**: quarterly-audit / governance cadence recommendations [6] —
  process advice for a standing design system, out of scope for a
  single-issue observation.
- **Skip**: any escaped-defect *metric* framing [2] — this role reports
  findings, not defect-leakage rates.

## Gap line (what the current state already meets vs. misses)

Met already: the record documents its substitution and names the
constraint (`docs/issue-56/reports/implementation.md:90-97`), and the
approval act is tamper-evident on GitHub (comment 5177783505). Missing /
unknown: whether the new test's scope reaches the recurrence surface
rather than the found surface (survey §4 row 6), and whether the deleted
§1.9's dependents were cleaned up (survey §4 row 5) — those two are what
the phase-2 checks below aim at.

## Segment fit

Same segment: a small-diff, doc-heavy, single-repo change reviewed after
merge by a non-authoring role. Enterprise-scale audit ceremony (sampling
plans, opinions) is one segment up and is used here only for its
alternative-procedures rule, not its process weight.

Sources:
1. <https://github.com/testing-library/eslint-plugin-testing-library/blob/main/docs/rules/prefer-screen-queries.md>
2. <https://kentcdodds.com/blog/common-mistakes-with-react-testing-library>
3. <https://www.accountingtools.com/articles/alternative-procedures>
4. <https://pcaobus.org/oversight/standards/archived-standards/pre-reorganized-auditing-standards-interpretations/details/AU330>
5. <https://newsletter.baselinedesign.com/what-the-system-is-trying-to-tell-you/>
6. <https://www.uxpin.com/studio/blog/design-system-maintenance-checklist/>
7. <https://medium.com/@aneeqr25/ensuring-fair-code-reviews-how-to-block-self-approval-in-github-pull-requests-6338341e4765>
8. <https://www.propelcode.ai/blog/code-review-compliance-sox-hipaa-pci-requirements>
9. <https://en.wikipedia.org/wiki/Regression_testing>
</content>
