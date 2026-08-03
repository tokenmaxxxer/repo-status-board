# Scout brief — issue #29 conformance-review

Mode: parallel (2 WebSearch calls, one turn — genuine concurrent
dispatch, not serialized). Stages used: 1 sweep + 1 judge point, no
deepening round — saturation reached immediately. Survey-first order
followed: the current-state survey (this role's own read of PR #30/#33's
merged code against issue #29's 8 acceptance criteria and the two logged
defect comments) ran first and found no open product/design decision —
the review's method is contract-mandated (verdict enum Present/Surface/
Absent/Incorrect/Unverifiable via `review-traceability`'s `finding-record`
skill; severity via `review-severity` only if findings warrant it),
matching this repo's own prior conformance-review precedent
(`docs/issue-23/reports/conformance-review/scout-brief.md`, same role,
same repo, same conclusion). This pass ran one sweep anyway per the
directive's "a review plan scouts what strong audits of this
change-class check" guidance, aimed at the two genuinely new
decision-relevant surfaces this issue adds beyond issue-23's precedent
(which was about plan-rendering, not filtering/banners): (1) whether
decomposing bundled acceptance criteria into independently-checkable
sub-facts is itself standard RTM practice (re-confirming, not
re-deriving, since issue-23 already scouted this exact question for the
same role); (2) whether the AC5 "N of M repos failed + collapsed detail"
pattern this review found only partially wired (survey.md's AC5
observation) is itself a recognized, well-grounded UX pattern worth
holding the implementation to, or an idiosyncratic ask.

**Category must-bes** (requirements-traceability / conformance-audit
practice — re-confirms issue-23's finding): decompose bundled/broad
acceptance criteria into a testable level before scoring: "the platform
must be secure and fast" isn't traceable to acceptance evidence, but
"secure: encrypts X" + "fast: responds under Yms" is; skipping straight
from a business requirement to a test case with no acceptance-criteria
layer in between is a traceability red flag; each row should carry a
verification method (inspection/analysis/demonstration/test), not just a
verdict word.

**Category must-bes** (partial-failure / error-banner UX): collapse
lengthy/itemized error detail behind an accordion-style disclosure
(directly matches the `<details>/<summary>` pattern issue #29's AC5 and
the approved proposal specify) rather than dumping every item inline;
don't collapse *all* failures into one undifferentiated message (i.e.
the always-visible summary line must still name the count, which the
current shipped banner already does); place the always-visible summary
where it won't be scrolled past.

**Performance axes**: (1) audit-grade traceability matrix (full
bidirectional row-per-requirement, evidence-linked) vs. (2) lightweight
code-review checklist. Same axis choice as issue-23 — this review sits
on (1), fixed by the harness's own skills, not a fresh choice.

**Adopt**: decompose each of the 8 acceptance criteria into discrete,
independently-checkable sub-rows where a criterion bundles more than one
verifiable fact (AC3's "table AND chips recompute together" is two
facts that could desync; AC5's "summary line" and "collapsed detail" are
two facts, and the search confirms the collapsed-detail expectation
matches standard error-banner UX practice rather than being an
unusually strict reading of the AC text); keep Defect A/B's own
enumerated sub-items (the comments already did this decomposition work
for AC3 and AC6) as the sub-row boundaries for those two ACs rather than
inventing a different split.

**Skip**: inventing a new verdict vocabulary — same conclusion as
issue-23, the harness already fixes this and this repo's own precedent
(issue-4, issue-23) already instantiates it twice.

**Segment fit**: internal single-issue conformance check against two
merged PRs (~500-line combined diff) and an 8-item acceptance list, not
an external-facing compliance audit or a general error-UX redesign.
Scout targets were audit *structure* (decomposition) and one narrow UX
question (is collapsed-detail-on-partial-failure a real pattern worth
holding AC5 to) — not tooling, process, or broader banner redesign.

**Gap line**: current state (this role's harness contract + this repo's
own issue-4/issue-23 precedent) already supplies the verdict vocabulary,
evidence/rationale row shape, and decomposition practice — nothing new
needed there. The one genuinely new question (AC5's collapsed-detail
expectation) is confirmed by the search as standard practice, not an
overreading of the AC text — so the gap this survey found (shipped
banner has the summary line but not the collapse) is a real,
well-grounded miss to carry into the requirement list, not scout-brief
material to soften.

**Judge point / saturation**: would another round change a build
decision? No — this role doesn't build anything (findings hand off, per
contract), and the search confirmed both the decomposition method and
the AC5 pattern's legitimacy without surfacing anything that would
reshape the requirement list further. Stopped after stage 1.

Sources:
- https://stell-engineering.com/blog/requirements-traceability-matrix
- https://www.coleyconsulting.co.uk/tracerequirements.htm
- https://www.testrail.com/blog/requirements-traceability-matrix/
- https://medium.com/design-bootcamp/error-handling-ux-design-patterns-c2a5bbae5f8d
- https://smart-interface-design-patterns.com/articles/error-messages-ux/
