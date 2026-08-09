# Current-state survey — issue #82 (44→72→78 chain)

loop_state: gathering

## Records read (subject's own history, records-only)

- `docs/issue-44/reports/conformance-review.md` — scored PR #45 against
  issue #44's 32 sub-requirements. R5a (line 93) verdicts AC2's fourth
  coverage item (mobile-overflow) **Absent** and names a three-way
  contradiction: AC2's `## Acceptance` text counts four defect-tracing
  items ("결함 3건 + Absent 1건에 각각"), 요구사항 2's 최소 커버리지 list
  enumerates only three bullets, and 범위 밖 excludes the visual-regression
  technique (screenshot/pixel comparison) the fourth item would need to
  use jsdom's zero layout engine. Finding 5 (lines 178-188) routes this
  explicitly to `addressed_to: the issue author` — the review scores the
  contradiction but does not resolve it.
- `docs/issue-44/reports/execution-observation.md` (cited by issue-72's
  own upstream basis, not independently re-read here since this survey's
  job is to confirm the chain's stated linkage, not re-derive
  execution-observation's own verdicts) — O7 (lines 136-146 per issue-72's
  citation) independently confirms the mobile-overflow exclusion is
  dispositioned (a reason is recorded) but AC2's literal text stays
  unmet.
- `docs/issue-72/reports/requirements-engineering.md` — opens by quoting
  both R5a and O7 as its entire upstream basis (lines 3-16). Adopts
  option (a), "non-visual reformulation": restates the mobile-overflow
  item as three EARS-pattern requirements (REQ-72-1..3 — table-scroll
  wrapper, `min-width: 0` on `#main-content, #detail-panel-slot`,
  `overflow-x: auto` on `.table-scroll`) that stay inside 범위 밖's
  visual-regression exclusion by asserting DOM/CSSOM structure instead of
  computed layout. Names a residual gap explicitly (lines 94-105): a
  *different* future overflow regression that needs real layout
  computation still would not be caught. Records (Ambiguity list,
  lines 80-92) that the after-proposal hunt caught a
  selector-scoping imprecision in the first draft's verification method
  (a substring search would false-pass) and folded the fix into REQ-72-2/3
  before landing — a contradiction-adjacent defect caught inside this same
  role's own phase, not by a downstream role.
- `docs/issue-78/reports/test-authoring.md` — implements REQ-72-1..3 as
  three traced tests in `test_dashboard_dom.py`, one per requirement, using
  CSSOM rule-block lookup (not whole-file substring search) per the
  selector-scoping constraint issue-72 wrote down. Verification run: full
  suite 80 passed. "What did not work" (lines 103-115) records two
  unrelated implementation slips (wrong payload field names; jsdom CSSOM
  normalizing `0` to `0px`), not spec-contradiction issues — the REQ-72
  contradiction itself did not recur at this stage.

## What the records establish, in sequence

1. Issue #44 shipped a spec (요구사항/AC2/범위 밖) that was internally
   contradictory on one item (mobile-overflow) at authoring time.
2. Conformance-review (a downstream verification role, not the author)
   discovered and named the contradiction while scoring the shipped
   artifact — not before implementation started.
3. The contradiction was routed to a separate issue (#72) and a separate
   role (requirements-engineering) to resolve, rather than being fixed by
   re-opening issue #44.
4. Requirements-engineering resolved it by reformulation (avoid the
   conflict) rather than by choosing one side of AC2 vs. 요구사항 2 vs.
   범위 밖 over the others.
5. Test-authoring (issue #78) then implemented against the *resolved*
   requirements (REQ-72-1..3) cleanly — no recurrence of a
   contradiction-shaped defect in that phase's own record.

## Gaps this survey found (aimed at by scout, per scout-directory order)

- **No prior issue-retrospective record exists anywhere in this repo**
  (`find docs -iname '*retrospective*'` → empty; no
  `docs/issue-*/reports/issue-retrospective.md` file predates this one).
  This role's own directive asks: did an earlier issue-retrospective
  record predict a failure mode that recurred in this issue? There is no
  earlier record to have predicted anything — this is the first
  application of the role in this repo. That absence is itself a
  gap for scout to aim at: an external exemplar (how do external
  postmortem practices structure contributing-factor analysis for a
  requirements-ambiguity-shaped incident) substitutes for the missing
  internal one.
- **No `docs/handbooks/round-end-value-gates.md` file exists** — the role
  directive names it as "the checklist" for round-end value gates, but
  `ls docs/handbooks/` shows only `rsb.md`. This is a records-only survey
  finding, not something this role fixes; it is folded into the
  round-end value-gates judgment call itself (gate A, procedure-value)
  rather than treated as a blocking absence, since the directive's gate A
  and B are stated as this role's own judgment calls, not as requiring
  the external checklist file to exist.
- **No spec-authoring gate exists between issue-drafting and
  implementation** — searched `docs/handbooks/rsb.md` and
  `docs/specs/` for any pre-implementation AC-consistency check; none
  found. The contradiction in issue #44 was caught only by a role
  (conformance-review) that runs *after* the artifact is built, which is
  the structural fact this record's "what we learned" section is aimed
  at.

## Mandatory skip-line check

Scouting was NOT skipped: this is not a pure bugfix and the spec (issue
#82's body) leaves an open design decision — what lesson to draw and how
to phrase it as a testable habit/gate. Scout ran; see
`scout-brief.md`.
