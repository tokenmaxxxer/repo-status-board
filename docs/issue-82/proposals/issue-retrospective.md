---
status: proposed
files:
  - docs/issue-82/reports/issue-retrospective.md
---

# Proposal — issue #82 retrospective of the 44→72→78 chain

## Intent

Retrospect the completed issue-44 → issue-72 → issue-78 chain (an
AC-internal contradiction found by conformance-review, resolved by
requirements-engineering, then implemented by test-authoring) and extract
what it teaches about spec-authoring on this repo: why AC2 / 요구사항 2 /
범위 밖 diverged at authoring time, and which habit or gate would have
prevented it.

## Constraints stated so far

- Record cites at least `docs/issue-44/reports/conformance-review.md`,
  `docs/issue-72/reports/requirements-engineering.md`,
  `docs/issue-78/reports/test-authoring.md`.
- Lessons must be testable habit/gate changes, each naming where it would
  apply — not platitudes.
- Read records only; if no generalizable lesson exists, say so with
  reasoning (empty-state permitted).
- This role never re-litigates other roles' verdicts and never fixes
  anything — advisory only.

## Input records to be read

- `docs/issue-44/reports/conformance-review.md` (R5a, finding 5) — names
  the AC2/요구사항 2/범위 밖 contradiction and its Absent verdict.
- `docs/issue-44/reports/execution-observation.md` (O7, as cited by
  issue-72's own record) — independent confirmation the exclusion is
  dispositioned.
- `docs/issue-72/reports/requirements-engineering.md` — the resolution:
  option (a) reformulation into REQ-72-1..3, plus its Ambiguity list and
  residual-gap section.
- `docs/issue-78/reports/test-authoring.md` — the downstream
  implementation against the resolved requirements, plus its "What did
  not work" section (whether a contradiction-shaped defect recurred at
  this stage).
- `docs/issue-82/reports/issue-retrospective/survey.md` and
  `.../scout-brief.md` (this role's own phase-1 output) — the
  current-state survey and the internal/external scout sweep.

Each record section answers one question:
- conformance-review R5a/finding-5: what was the contradiction, and who
  was it routed to?
- execution-observation O7: does an independent role confirm the same
  gap?
- requirements-engineering: how was it resolved, and what residual gap
  is named rather than hidden?
- test-authoring: did the resolved requirements implement cleanly, or did
  a related defect recur?
- survey/scout-brief: is there a prior issue-retrospective record that
  predicted this, and what does an external exemplar (blameless
  postmortem practice) say a contributing-factors analysis of a
  requirements-ambiguity incident should contain?

## Synthesis (not raw paste of the four records)

Read together, the four records show a single-direction pipeline, not a
loop: conformance-review (issue #44) is the *only* point in the chain
that inspects the issue text itself for internal consistency, and it does
so only after PR #45 already shipped against that text — the check is
downstream of authoring, not upstream of it. Once the contradiction is
named, resolution happens in a *new* issue (#72) rather than by reopening
#44, and requirements-engineering's own record (lines 3-16) treats R5a
and O7 as its entire input — it does not re-read issue #44's original
text independently, it re-reads the two downstream verdicts about that
text. Test-authoring (#78) then closes the loop cleanly: its own "What
did not work" section names two implementation-level slips, not a
recurrence of the spec-contradiction shape, which is the direct evidence
that requirements-engineering's reformulation held. The scout sweep found
no earlier issue-retrospective record and no pre-authoring consistency
gate anywhere in `docs/handbooks/` or `docs/specs/` (survey.md) — so the
single reusable structural fact this chain demonstrates is: this repo's
only defense against an internally contradictory issue is a role that
runs after implementation, and the cost of that ordering was one extra
issue (#72) and two extra role-sessions (requirements-engineering,
downstream test-authoring) to reach the requirement set issue #44 could
have shipped with initially.

## Adopted norms, with sourced rationale

- **Contributing-factors framing, not single-cause / root-cause
  language.** Adopted directly from this role's own contract (PHASE 2
  STEP 2: "the phrase 'root cause' ... is a methodology violation") and
  independently corroborated by the external exemplar swept in
  `scout-brief.md`: blameless postmortem practice frames incidents as
  systemic — "understand what systemic factors led to the incident...
  without indicting any individual or team" (source:
  https://sre.google/sre-book/postmortem-culture/). This repo's own
  conformance-review record already practices this (finding 5 names the
  contradiction as a property of the issue text, routed to a role/author,
  not a person) — the norm is confirmed as already-adopted upstream, not
  imported new.
- **Named-owner, checkable action items.** Adopted from the same external
  exemplar — "a post mortem action item needs... a specific owner (a
  named person, not a team)" (source:
  https://postmortems.pagerduty.com/culture/blameless/) — and matches
  this role's own contract requirement that action items "name an owner
  (a person/role, not 'the team')". Both sources converge on the same
  norm; no conflict to reconcile.
- **Skipped deliberately:** the postmortem-literature two-tier action
  item split (immediate mitigation vs. long-term fix). Considered per
  scout-brief's Angle 2, not adopted: this role's contract states action
  items are advisory-only and never gate landing, so a mitigation/
  long-term urgency split would add structure this role's own contract
  has no mechanism to act on. Noted so the decision reads as considered,
  not overlooked.

## Round-end value gates

Will run both judgment calls (docs/handbooks/round-end-value-gates.md is
absent from this repo — see survey.md — so the gates are applied as this
role's own directive-stated judgment calls, not read from that file):
(A) procedure-value — for each role in the chain, cite evidence it
changed the issue's outcome or mark it `ritual`.
(B) blind-onboarding — could a zero-context reader reconstruct what was
asked, built, decided, and what is next, from the four records above
alone?

## What will be done

Write `docs/issue-82/reports/issue-retrospective.md` with: Timeline
(records-only, chronological) before any causal claim; Impact summary
(what the contradiction actually cost, in records-only terms — a
follow-up issue and two extra role-sessions, not a shipped defect that
reached a user, since conformance-review's Absent verdict caught it
before any further downstream consumption); Contributing factors (plural,
structural, no "root cause" language); What we learned (explicit answer
to the recurred-prediction question — expected answer: no prior
issue-retrospective record existed, so nothing could have predicted this,
which is itself a finding); Action items (structurally required section,
named owners, advisory-only).

## Out of scope

- No re-scoring of conformance-review's, requirements-engineering's, or
  test-authoring's own verdicts.
- No fix to the missing `docs/handbooks/round-end-value-gates.md` file or
  to any spec-authoring gate this record recommends — this role proposes,
  never builds.
- No new source reads beyond the four cited records plus this role's own
  phase-1 files; no re-opening of issue #44/#72/#78's running system
  (contract prohibition: records-only).

## How it will be known to work

- Record cites all three mandatory paths by exact path.
- Each lesson in "What we learned" / Action items names a concrete
  habit or gate and the point in the workflow (e.g. "issue-authoring,
  before an issue is opened for implementation") where it would apply.
- Round-end value gates A and B are answered explicitly, not skipped.
