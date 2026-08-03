# Scout brief — issue #27 conformance-review

Mode: parallel (2 WebSearch calls, one turn). Stages used: 1 sweep, no
deepening round. Survey-first order followed: the current-state survey
(this role's own read of PR #28's diff and issue #27's 6 acceptance
criteria) ran first and found the review's method is contract-mandated
(verdict enum Present/Surface/Absent/Incorrect/Unverifiable via
`review-traceability`'s `finding-record` skill; severity via
`review-severity` only if findings warrant it) — same as issue-23's
prior pass for this exact role. What differs this time: issue #27's
subject is an infra/deployment PR (GitHub Actions + Pages), not a
data-rendering PR, and several of its acceptance criteria bundle a
claim that can only be observed on a live runner/live deployment — a
shape issue-23's scout pass didn't need to weigh. This scout targeted
that specific gap: does audit/traceability practice for
infra-deployment changes handle "can't verify without a live
environment" any differently than issue-23's plain
"provider-side/Unverifiable" treatment did?

**Category must-bes** (from CI/CD audit and RTM-untestable-requirement
practice): audit evidence for pipeline controls is meant to be
generated continuously by the pipeline itself and reviewed against a
verifiable chain from change → build → deploy, but multiple sources
note certain control validations still require observing a live
runner/environment in execution — a static-only read of pipeline
config is evidence of *intended* mechanism, not evidence the mechanism
*fired* correctly. Separately, RTM practice distinguishes a
verification-status vocabulary of "satisfied / failed / **unverified**"
— "unverified" is its own first-class status (not the same as
"deferred," which implies a change was authorized but scheduled for
later), used exactly for a requirement that has not yet been tested
against real evidence, regardless of how confident the design looks on
paper.

**Chosen performance axis**: this scout weighed rigor (splitting every
live-only claim into a locally-checkable mechanism-fact plus a
separately-flagged live-only outcome-fact) over expedience (accepting
a design read as equivalent to a live-run confirmation). Rigor wins
here because the harness's own verdict vocabulary already has
"Unverifiable" as a distinct value from "Present" — collapsing a
mechanism-looks-correct read into "Present" would misuse that value.

**Adopt**: confirms the survey's approach is correct, not just
convenient — for each of AC1/AC2/AC3/AC5's live-only clause, decompose
into (a) a locally-checkable "does the mechanism that's supposed to
produce this outcome exist and look correctly wired" sub-fact, and (b)
a separately-tracked "was the outcome actually observed in a live
run" sub-fact flagged as an Unverifiable-within-this-repo candidate —
exactly the split issue-23's survey already used for its own AC3, now
confirmed by external practice to be the standard way RTM handles a
requirement whose evidence requires an environment the auditor doesn't
have, rather than a repo-specific invention.

**Skip**: adopting a distinct "Deferred" status alongside "Unverifiable"
— the search surfaced this as a related-but-different RTM concept
(authorized-but-scheduled-later), which does not describe this
review's situation (the requirement isn't scheduled for later, it's
present now but the evidence to confirm it needs an environment this
role doesn't have). The harness's existing "Unverifiable" verdict
already fits; inventing a parallel status would fragment the
vocabulary this role's contract already fixes.

**Segment fit**: this is a small (~2 new config/workflow files, 1
changed line), internal, single-PR infra check — not an external
compliance audit (SOC2/ISO27001, the dominant hits for "CI/CD audit").
Scout target was the narrow question of live-vs-static verification
status vocabulary, not those frameworks' control catalogs or evidence-
retention policies, which are out of scope by scale and applicability
mismatch.

**Gap line**: current state (this role's harness contract plus
issue-23's own precedent) already supplies the requirement-decomposition
method and the "Unverifiable" verdict value. The one thing genuinely
new to this issue versus issue-23 — several ACs bundling a live-only
claim rather than just one (issue-23 had exactly one, AC3) — needed
confirmation that decomposing *each* of them the same way is still the
right shape, not an overreach. The search confirms it is: "unverified"
is meant to be used per-requirement, not collapsed across multiple
requirements into one blanket caveat.

**Judge point / saturation**: would another round change a build
decision? No — the search confirmed the mechanism-fact vs.
outcome-fact split is standard RTM/audit practice, not something that
needs a repo-specific process; no new verdict vocabulary or tooling
surfaced that would change the requirement list's shape. Stopped after
stage 1.

Sources:
- https://www.stepsecurity.io/blog/why-compliance-auditors-are-looking-at-your-ci-cd-runners-and-how-to-prepare
- https://cicd.watch/blog/iso-27001-ci-cd-controls
- https://www.mathworks.com/help/slrequirements/ug/review-requirement-verification-status-metrics-data.html
- https://tynerblain.com/blog/2005/11/30/how-to-deal-with-untestable-requirements-rewrite-them/
