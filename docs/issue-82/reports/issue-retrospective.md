# Issue retrospective — issue-82

retro_id: issue-82

loop_state: writing

## What was done

Read the three mandatory records plus `docs/issue-44/reports/
execution-observation.md`, reconstructed the timeline below, and derived
the sections that follow it from those records only — no other role's
verdict was re-scored and no code, test, or running system was touched.

## Timeline

Records-only, chronological, no causal claim before this section:

1. Issue #44 is opened with 요구사항 1-4, 범위 밖, and AC1-AC6, including
   AC2's text: "결함 3건 + Absent 1건에 각각" (four defect-tracing coverage
   items), while 요구사항 2's 최소 커버리지 list enumerates three bullets,
   and 범위 밖 excludes visual-regression (screenshot/pixel-comparison)
   testing.
2. PR #45 (test-authoring on issue #44) ships `test_dashboard_dom.py`
   against that text, covering the three 요구사항-2-listed bullets; no
   mobile-overflow (fourth AC2 item) test exists, jsdom having no layout
   engine to write one with under the 범위 밖 exclusion
   (`docs/issue-44/reports/test-authoring.md:251-259`, per
   `docs/issue-44/reports/conformance-review.md:93`).
3. Conformance-review (issue #44, `docs/issue-44/reports/
   conformance-review.md`) scores R5a **Absent**, and finding 5
   (lines 178-188) names the AC2/요구사항 2/범위 밖 three-way contradiction
   explicitly, routing it `addressed_to: the issue author` — the review
   scores the gap but does not resolve it.
4. `docs/issue-44/reports/execution-observation.md` (O7, as cited at
   `docs/issue-72/reports/requirements-engineering.md:9-12`)
   independently confirms the same exclusion is dispositioned (a reason
   is on record) but AC2's literal text stays unmet.
5. Issue #72 is opened. Requirements-engineering
   (`docs/issue-72/reports/requirements-engineering.md`) takes R5a and O7
   as its entire upstream basis (lines 3-16), adopts option (a)
   "non-visual reformulation," and restates the fourth AC2 item as three
   EARS-pattern requirements, REQ-72-1..3 (table-scroll wrapper,
   `min-width: 0`, `overflow-x: auto`), each verified by DOM/CSSOM
   structure rather than computed layout — staying inside 범위 밖's
   exclusion while satisfying 요구사항 2's now four-bullet list. An
   after-proposal hunt inside that same role's own phase caught a
   selector-scoping imprecision in the first verification-method draft
   (a whole-file substring search could false-pass) and it was folded
   into REQ-72-2/3 before landing (lines 52-59). A residual gap is named
   explicitly and not hidden: a *different* future overflow regression
   needing real layout computation still would not be caught
   (lines 94-105).
6. Issue #78 is opened. Test-authoring
   (`docs/issue-78/reports/test-authoring.md`) implements REQ-72-1..3 as
   three traced tests using CSSOM rule-block lookup, per the
   selector-scoping constraint issue #72 wrote down. Full suite: 80
   passed. "What did not work" (lines 103-115) names two
   implementation-level slips (wrong payload field names; jsdom
   normalizing `min-width: 0` to `0px`) — neither is a recurrence of a
   spec-contradiction shape.
7. Issue #82 is opened, dispatched to issue-retrospective per a validator
   orchestrator comment: "work landed and verification settled for the
   44→72→78 chain; reads records only."

## Impact summary

Established from the timeline above, in records-only terms: the
contradiction did not reach a shipped defect visible to an end user — it
was caught by conformance-review before any further downstream role
consumed issue #44's text as-is. Its cost was structural, not
functional: one additional issue (#72) and two additional role-sessions
(requirements-engineering to reconcile the AC2 item, a downstream
test-authoring session on issue #78 to implement the reconciled
requirements) that would not have been needed had 요구사항 2, AC2, and
범위 밖 been mutually consistent when issue #44 was opened. No record
shows rework of already-shipped code — PR #45's tests were not modified
or reverted; REQ-72-1..3 are pure additions. The cost is round-trip
latency and role-session count, not defect cost.

## Synthesis

Read together (not pasted from any one record), the four upstream
records show a single-direction pipeline, not a loop: conformance-review
is the only point in the chain that inspects issue #44's own text for
internal consistency, and it does so only after PR #45 already shipped
against that text. Resolution then happens in a fresh issue (#72) rather
than by reopening #44, and requirements-engineering's own record treats
R5a and O7 as its entire input rather than re-reading issue #44's
original text independently. Test-authoring (#78) closes the loop
cleanly — its "What did not work" names two implementation-level slips,
not a recurrence of the spec-contradiction shape, which is direct
evidence the reformulation held. This synthesis is what the Contributing
factors section below is built from, not a summary of any single record.

## Contributing factors

Three plural, structural contributing factors together produced this
outcome; no single one is sufficient alone and none is a person's error:

1. **Contributing factor — no internal-consistency check at
   issue-authoring time.** Issue #44's AC2 (item count: four), 요구사항 2
   (bullet count: three), and 범위 밖 (technique exclusion) were each
   written as if independently correct, and nothing in this repo's
   handbooks or specs (searched: `docs/handbooks/`, `docs/specs/`; see
   `docs/issue-82/reports/issue-retrospective/survey.md`) cross-checks an
   AC item's count against its 요구사항 list, or an AC item's implied
   verification technique against 범위 밖's exclusions, before the issue
   is handed to implementation.
2. **Contributing factor — every existing check in this repo's role
   chain runs after an artifact exists, not before authoring.**
   Conformance-review — the role that actually caught R5a — is, by this
   repo's own contract, a downstream verification role scored against a
   shipped PR (`docs/issue-44/reports/conformance-review.md:5-11`,
   `code_under_review` is a merged commit). No role in the chain runs *on
   the issue text itself*, before an implementation branch opens,
   checking that its own sections agree with each other.
3. **Contributing factor — the correct resolution path itself adds a
   full extra issue-cycle.** Requirements-engineering resolving the
   contradiction in a fresh issue (#72) rather than by reopening #44 is
   consistent with this repo's contract (role-handoff boundaries, one
   branch per issue x role) — it is not a process error. But it means the
   round-trip cost of an authoring-time contradiction is, structurally,
   never smaller than one full downstream-discovery-issue plus one
   reconciliation-issue, because no earlier point in the pipeline is
   positioned to catch it more cheaply. All three factors compound: factor
   1 lets the contradiction into the issue text, factor 2 delays its
   discovery to after implementation, and factor 3 sets the minimum cost
   of discovery that late.

## What we learned

Explicit answer to the recurred-prediction question this role's own
directive asks: **no earlier issue-retrospective record existed to have
predicted this.** `find docs -iname '*retrospective*'` and a search of
every `docs/issue-*/reports/*.md` filename in this repo
(`docs/issue-82/reports/issue-retrospective/survey.md`) confirm this is
the first issue-retrospective record in the repo's history. There is
therefore no "recurred prediction" to report — the answer is not "no
recurrence," it is "no prior record capable of predicting anything." That
absence is itself the finding: this repo has run the 44→72→78 chain, and
others before it, without a standing mechanism that would let a later
issue benefit from an earlier one's lesson about *this specific failure
shape* (AC/요구사항/범위밖 internal inconsistency). Issue #82 is that
mechanism's first use.

## Adopted norms, with sourced rationale

- **Contributing-factors framing, not single-cause / root-cause
  language.** Adopted from this role's own contract (PHASE 2 STEP 2:
  "the phrase 'root cause' ... is a methodology violation") and
  independently corroborated by the external exemplar swept in
  `docs/issue-82/reports/issue-retrospective/scout-brief.md` — blameless
  postmortem practice frames incidents systemically: "understand what
  systemic factors led to the incident... without indicting any
  individual or team" (source:
  https://sre.google/sre-book/postmortem-culture/). This repo's own
  conformance-review record already practices this — finding 5 names the
  contradiction as a property of the issue text, routed to a role/author,
  not a person — so the norm is confirmed already-adopted upstream, not
  imported new; this record applies it one step earlier, at the issue
  chain's own retrospective level.
- **Named-owner, checkable action items.** Adopted from the same external
  exemplar — "a post mortem action item needs... a specific owner (a
  named person, not a team)" (source:
  https://postmortems.pagerduty.com/culture/blameless/) — and matches
  this role's own contract requirement that action items "name an owner
  (a person/role, not 'the team')." Both sources converge on the same
  norm; applied directly in the Action items section below (owner:
  JiwonJung94, the repo's issue-authoring party).
- **Skipped deliberately:** the postmortem-literature two-tier action
  item split (immediate mitigation vs. long-term fix). Considered per
  `scout-brief.md` Angle 2, not adopted: this role's contract states
  action items are advisory-only and never gate landing, so a
  mitigation/long-term urgency split would add structure this role's own
  contract has no mechanism to act on.

## Action items

1. **Add a self-consistency check to issue-authoring, run before an issue
   is opened for implementation: an AC item's count/coverage claim must
   match the count of items its own 요구사항 list enumerates, and any AC
   item implying a verification technique must be checked against 범위
   밖's stated exclusions.** *Owner: JiwonJung94* (issue author role, per
   `docs/specs/approvers.md` — the same role finding 5 in
   `docs/issue-44/reports/conformance-review.md:178-188` addressed this
   exact class of contradiction to). *Applies at: the point an issue's
   body is drafted, before it is dispatched to any implementation role* —
   this is advisory only, per this role's contract; it does not gate
   issue #82's own landing or any other issue.
2. **Write `docs/handbooks/round-end-value-gates.md`, referenced by this
   role's own contract but absent from the repo** (confirmed absent in
   `docs/issue-82/reports/issue-retrospective/survey.md`). *Owner:
   JiwonJung94.* *Applies at: any future issue-retrospective session's
   PHASE 2 STEP 3* — without the file, every future retrospective must
   re-derive the two judgment-call gates from the role directive text
   alone, as this record did.

## Round-end value gates

(A) Procedure-value, per role in the chain:
- **conformance-review (issue #44):** cites evidence it changed the
  outcome — it is the only role that discovered R5a/finding-5 at all;
  without it, AC2's fourth item would have shipped silently unmet. Not
  ritual.
- **requirements-engineering (issue #72):** cites evidence — REQ-72-1..3
  exist and trace directly to R5a/O7; the after-proposal hunt inside its
  own phase caught a selector-scoping defect before landing (lines 52-59
  of its own record). Not ritual.
- **test-authoring (issue #78):** cites evidence — three tests trace 1:1
  to REQ-72-1..3, verified by `grep -r "REQ-72-" test/`; full suite green
  (80 passed). Not ritual.
- **execution-observation (issue #44, O7):** its citation here is
  indirect — this record did not independently re-read
  `docs/issue-44/reports/execution-observation.md` (see
  `docs/issue-82/proposals/issue-retrospective.md`, scope note), relying
  instead on issue-72's own citation of it as corroboration alongside
  R5a. Evidence of independent value beyond confirming conformance-
  review's finding is not established by this record; not marked
  `ritual` outright, but flagged as **unverified-by-this-record** rather
  than confirmed.

(B) Blind-onboarding: yes, with one caveat. A zero-context reader given
only the four cited records (`docs/issue-44/reports/
conformance-review.md`, `docs/issue-72/reports/
requirements-engineering.md`, `docs/issue-78/reports/test-authoring.md`,
and this record) can reconstruct what was asked (issue #44's AC2), what
was found (R5a's contradiction), what was decided (option (a)
reformulation into REQ-72-1..3), what was built (three traced tests), and
what is next (the two action items above — no further work is scheduled
on issue #44/#72/#78 themselves; all three are closed per the chain's own
records). The caveat: `docs/issue-44/reports/execution-observation.md`
itself was not independently re-read by this record (see gate A note
above) — a reader wanting O7's own reasoning, not just issue-72's
citation of it, has one extra hop this record does not close.

## Open findings

None against any role's prior verdict — this role never re-scores
another role's work. The two action items above are the only forward-
facing items, both advisory and neither blocking.

## Next steps

1. This record ships as phase-2 output of the PR on
   `issue-82/issue-retrospective`. Nothing further is built in this
   branch.
2. The human decides the PR by GitHub act — merge accepts this record
   onto the board, closed-unmerged refuses it.
3. Action item 1 (issue-authoring self-consistency check) and action item
   2 (write `docs/handbooks/round-end-value-gates.md`) are both advisory
   and unowned by this role to build; their resolution path is a future
   session the repo owner opens, naming the applicable role.

## Why

Both upstream records that first touched this contradiction (R5a,
finding 5) explicitly declined to resolve it and routed it forward
instead — the chain therefore never produced a record answering "what
does the whole 44→72→78 sequence, taken together, teach about
spec-authoring on this repo." Issue #82 requests exactly that reading,
across the completed chain, from records only.

## Upstream / basis

`docs/issue-44/reports/conformance-review.md`,
`docs/issue-44/reports/execution-observation.md` (cited, not
independently re-read — see gate A),
`docs/issue-72/reports/requirements-engineering.md`,
`docs/issue-78/reports/test-authoring.md`,
`docs/issue-82/proposals/issue-retrospective.md` (this role's approved
phase-1 proposal), `docs/issue-82/reports/issue-retrospective/survey.md`
and `.../scout-brief.md`.

## kind / loop_state

kind: report
loop_state: landed
