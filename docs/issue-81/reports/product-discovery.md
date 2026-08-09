---
kind: hypothesis
loop_state: inconclusive
Subject: issue-81
---

# Product decision: visual-regression coverage vs structural checks (REQ-72 residual gap)

## Summary of work

Applied the approved proposal (`docs/issue-81/proposals/product-discovery.md`,
approved via issue comment `APPROVE issue-81/product-discovery`) as this
pre-registered decision record. Created the `mobile-overflow` GitHub
label (the missing-instrumentation fix the proposal required before the
90-day clock can run) and evaluated the registered rule against the
evidence available today.

## Why

Requirement: `docs/issue-72/reports/requirements-engineering.md` routed
a residual gap — REQ-72-1..3's structural (jsdom-tier) checks cannot
catch a future mobile-overflow regression introduced through a
mechanism other than the one they assert on — to this product decision.
Rather than guess a go/kill verdict from absent usage-scale data, the
proposal pre-registered a metric, threshold, and decision rule, and
routed the measurement gap itself to an observability fix.

## Upstream

- Basis: `docs/issue-81/proposals/product-discovery.md`
- Basis: `docs/issue-72/reports/requirements-engineering.md`

## Pre-registered decision rule (unchanged from proposal)

- **Metric**: count of distinct mobile-overflow-class GitHub issues
  opened against `rsb` (dashboard element not fully visible/scrollable
  on a mobile viewport) that REQ-72-1..3 did not catch, labeled
  `mobile-overflow` at triage.
- **Threshold**: 2 issues within any rolling 90-day window after this
  record lands (today).
- **Decision rule**: go (build real browser-based visual-regression
  coverage) if metric >= 2 in a 90-day window; kill (structural checks
  + defect-report loop remain sufficient, re-measure at next occurrence
  or in 180 days) if metric stays < 2 in 90 days; inconclusive, routed
  to observability, if the labeling convention is never adopted and no
  count is collectible after 90 days.
- **Guardrail**: CI wall-clock time and flakiness rate for the `rsb`
  test suite must not regress if/when visual-regression tooling is
  built under the go branch.

## Measurement at this moment

| | Value |
|---|---|
| Metric (labeled `mobile-overflow` issues, rolling 90d) | 0 — measurable window has not started |
| Threshold | 2 / 90 days |
| Guardrail (CI wall-clock/flakiness) | N/A — no visual-regression tooling exists yet to regress; not breached |

Evidence checked: `gh issue list --search "mobile-overflow"` and `gh
label list --search mobile` on 2026-08-09 returned no prior
`mobile-overflow`-labeled issues and no such label — the labeling
convention required to count this metric did not exist before this
record.

## Verdict: inconclusive

Per the acceptance criterion's empty-state clause ("if evidence for
usage scale is unavailable, the record must say what instrumentation is
missing and route it") and the proposal's own third rule branch: no
count was collectible because the `mobile-overflow` label did not exist
until this record's phase 2 created it today. This is the
zero-elapsed-time case of the registered "inconclusive" branch, not a
fresh judgment call — the rule is mechanically applied to the only
evidence that exists (none, because the channel didn't exist).

Routed to observability: the `mobile-overflow` label now exists
(created 2026-08-09) as the triage convention the metric depends on.
The 90-day rolling-window clock starts now.

## Opportunity-solution tree disposition

Outcome: `rsb` dashboard changes ship without reintroducing
mobile-layout defects that reach a viewer (unchanged).

Opportunity: the REQ-72-1..3 residual gap — layout regressions via a
mechanism other than the fixed P1-1 pattern are undetectable by
structural/jsdom-tier checks (unchanged, still open).

Candidate solutions: (a) real browser-based visual-regression coverage,
(b) structural checks + defect-report loop as-is.

Discriminating assumption test: whether the rate/cost of future
non-fingerprinted regressions exceeds visual-regression infra's
setup+maintenance cost — **neither branch pruned nor promoted this
round**. The test itself could not run: the evidence channel (labeled
`mobile-overflow` issue count) did not exist, so both candidate
solutions (a) and (b) stay open rather than either being killed or
promoted. What changed: the discriminating-assumption test now has an
instrumented channel (`mobile-overflow` label, created 2026-08-09) and
a scheduled re-check (2026-11-07 or second qualifying issue,
whichever first) that will actually prune or promote a branch next
time this record is opened.

## ITWWS status

Deferred — validated is not yet reached. No REQ-required build or PR
checklist change happens at this decision; the ITWWS activates only on
a future `validated` verdict.

## Next steps

- Whoever next opens this record (occurrence of a qualifying issue, or
  at the 90-day mark, whichever first) must apply the same mechanical
  rule to the then-current count of `mobile-overflow`-labeled issues
  opened since 2026-08-09, and update `loop_state`: `validated` if the
  metric crosses threshold (promotes candidate (a): build
  visual-regression coverage), `invalidated` if it stays below
  threshold after the 90-day window elapsed with the label in active
  use (promotes candidate (b): structural checks + defect loop stand),
  or `inconclusive` again if the label still saw no adoption/triage.
- If nobody triages issues with the `mobile-overflow` label going
  forward, the count stays uncollectible and the next opener must
  restate this same `inconclusive` verdict explicitly rather than
  reading elapsed silence as a kill.

## Resolution path

Re-open this record (`docs/issue-81/reports/product-discovery.md`) when
either (a) a second `mobile-overflow`-labeled issue lands within 90
days of another such issue, making the metric >= 2, or (b) 90 days pass
from 2026-08-09 (i.e. by 2026-11-07) with the label convention in use —
apply the decision rule mechanically to the collected count at that
point.

## Open findings

- The `mobile-overflow` label exists as of 2026-08-09 but has no
  enforcement mechanism (no CI check, no PR template line) ensuring
  triagers actually apply it — a silent-adoption-failure risk the
  proposal already flagged. No action taken on this beyond noting it;
  out of this record's scope per the proposal's "Out of scope" section
  (tool/process selection deferred).

## What did not work

(none — proposal's registered rule applied directly; no revisions
needed during phase 2)
