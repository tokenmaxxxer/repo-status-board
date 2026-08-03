# Scout brief — issue #23 conformance-review

Mode: parallel (2 WebSearch calls, one turn). Stages used: 1 sweep + 1
judge point, no deepening round — saturation reached immediately (see
below). Survey-first order followed: the current-state survey (this
role's own read of PR #24's diff, issue #23's 6 acceptance criteria, and
`flows-schema.md` §2.2) ran first and found no open product/design
decision — the review's method is contract-mandated (verdict enum
Present/Surface/Absent/Incorrect/Unverifiable via `review-traceability`'s
`finding-record` skill; severity via `review-severity` only if findings
warrant it), matching this repo's own prior conformance-review precedent
(`docs/issue-4/proposals/conformance-review.md`, which recorded scouting
as explicitly skipped for the same reason). This pass ran one sweep
anyway per the directive's explicit "a review plan scouts what strong
audits of this change-class check" guidance, to check whether external
practice would change the requirement-list shape.

**Category must-bes** (requirements-traceability / conformance-audit
practice): bidirectional traceability — every requirement traces to the
evidence used to verify it, and every check traces back to a named
requirement; requirements decomposed to a testable/verifiable level
(a bundled criterion like "steps show order + roles + done" is checked
as separable sub-items, not one opaque pass/fail); each row carries a
verification method (inspection/analysis/demonstration/test) and
pass/fail evidence, not just a verdict word.

**Performance axes**: (1) audit-grade traceability matrix (full
bidirectional row-per-requirement, evidence-linked, reproducible) vs.
(2) lightweight code-review checklist (scope-limited to the diff, faster,
less formal). This review sits on axis (1) — the harness's own
`review-traceability`/`review-severity` skills and the Present/Surface/
Absent/Incorrect/Unverifiable enum already are the audit-grade shape,
not the lightweight-checklist shape.

**Adopt**: decompose each of the 6 acceptance criteria (and the schema
§2.2 contract check) into discrete, independently-checkable sub-rows
where a criterion bundles more than one verifiable fact (e.g. AC1 bundles
"§2.2 row matches" + "§7 worked example updated" + "as-of date bumped");
name the verification method per row (code inspection vs. test-run vs.
unable-to-observe-live) up front in the proposal, before phase 2 assigns
verdicts.

**Skip**: inventing a new verdict vocabulary or checklist template —
the harness already fixes this (Present/Surface/Absent/Incorrect/
Unverifiable + evidence + rationale), and this repo's own issue-4
precedent already instantiates it; adopting an RTM tool/template style
foreign to this repo's plain-markdown record convention would add
process theater without changing what gets checked.

**Segment fit**: this is an internal single-PR conformance check against
a small (~350-line), already-merged diff and a 6-item acceptance list —
not an external-facing compliance audit. Scout target was audit
*structure* (row decomposition, evidence-linking), not the exemplars'
tooling or organizational process, which are out of scope by scale
mismatch.

**Gap line**: current state (this role's harness contract) already
supplies the verdict vocabulary and evidence/rationale row shape that
strong RTM practice recommends — the gap is narrow: only the
requirement-decomposition step (splitting bundled ACs into
independently-checkable sub-rows) needed explicit scouted confirmation,
and the search confirmed it's standard practice, not a repo-specific
invention.

**Judge point / saturation**: would another round change a build
decision? No — the search confirmed the row/evidence/traceability shape
already fixed by contract and precedent; no new practice surfaced that
would change the requirement list's decomposition. Stopped after stage 1.

Sources:
- https://stell-engineering.com/blog/requirements-traceability-matrix
- https://www.compliancequest.com/cq-guide/creating-maintaining-requirements-traceability-matrix/
- https://www.parallelhq.com/blog/what-acceptance-criteria
- https://exaud.com/blog/code-audit-vs-code-review
