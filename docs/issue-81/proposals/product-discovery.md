---
status: proposed
files:
  - docs/issue-81/reports/product-discovery/current-state.md
  - docs/issue-81/reports/product-discovery/scout-brief.md
  - docs/issue-81/proposals/product-discovery.md
  - docs/issue-81/reports/product-discovery.md
---

## Intent

Decide, as a pre-registered hypothesis, whether `rsb` needs real
browser-based visual-regression coverage for the dashboard's mobile
viewport, or whether the existing structural checks (REQ-72-1..3) plus
the human defect-report loop are sufficient at `rsb`'s actual usage
scale — resolving the residual gap
`docs/issue-72/reports/requirements-engineering.md` named but explicitly
declined to close.

## Constraints

- REQ-72-1..3 and their jsdom-tier structural tests are not being
  revisited or reopened by this decision.
- The 범위 밖 visual-regression exclusion from #72 stays as-is unless
  this decision's own registered rule says otherwise.
- No page-view, defect-report-rate, or mobile-usage instrumentation
  exists in `rsb` today (verified: zero grep hits for
  analytics/pageview/access-log under `src/`) — the decision cannot be
  made on invented usage-scale numbers.

## What will be done

Because the discriminating variable (occurrence rate and cost of a
non-fingerprinted mobile-overflow regression reaching a viewer) has no
existing instrumentation, this proposal registers the hypothesis and
decision rule now and routes the *measurement gap itself* to an
observability fix, rather than guessing a verdict from absent data.

Hypothesis: structural checks (REQ-72-1..3) plus the manual
defect-report loop are sufficient at `rsb`'s current scale (single
internal team dashboard, no design-system-wide component reuse) — i.e.,
unfingerprinted mobile-overflow regressions reaching a viewer are rare
and cheap enough that standing up browser-automation visual-regression
infra is not yet worth its setup/maintenance cost.

Metric: count of distinct mobile-overflow-class GitHub issues opened
against `rsb` (any regression where a dashboard element is not fully
visible/scrollable on a mobile viewport) that the structural checks did
not catch (i.e., landed after REQ-72-1..3 existed). This reuses the same
signal channel the P1-1 defect itself arrived through
(`docs/issue-44/reports/conformance-review.md`), requiring no new
tooling beyond consistent labeling of such issues.

Threshold: 2 issues within any rolling 90-day window after this record
lands.

## Decision rule

Mechanical, applied to the metric against the threshold above: verdict is go if the metric crosses the threshold (2 or more qualifying issues in a rolling 90-day window) — build real browser-based visual-regression coverage for the dashboard's mobile viewport; verdict is kill if the metric stays below the threshold (under 2 in 90 days) — structural checks plus the defect-report loop remain sufficient, re-measure at the next occurrence or in 180 days; verdict is pivot to inconclusive, routed back to observability, if the labeling convention below is never adopted and no count is collectible after 90 days.

## Guardrail metric

CI wall-clock time and flakiness rate for the `rsb` test suite must not
regress if/when visual-regression tooling is adopted under the go
branch. A real-browser screenshot-diff suite is known (scout-brief.md,
sources [1][3]) to introduce rendering-noise flakiness. A validated
verdict that also breaches this guardrail is a reduced-trust result, not
a clean win, and should trigger a narrower solution (e.g. a targeted
layout assertion for the specific new mechanism) before full
visual-regression infra is built.

## ITWWS

If this works (validated) — the visual-regression build becomes
REQ-required for the dashboard's mobile viewport going forward, and its
baseline-approval step is added to the PR review checklist so future
dashboard changes don't reintroduce noise-driven false confidence in the
new suite.

## Missing-instrumentation routing

Required by issue #81's acceptance criteria: since no mechanism today
reliably surfaces "was this GitHub issue a mobile-overflow regression the
structural checks missed," phase 2 of this record must first add a
lightweight labeling convention (e.g. a `mobile-overflow` issue label
applied at triage) before the 90-day clock can run meaningfully. Absent
that label, the metric cannot be counted from GitHub issue history
alone.

Nothing in this repo schedules or automates the 90-day check — it is not
CI-driven. Silence past 90 days (nobody opens phase 2 to count the
label) must never be read as a "kill" verdict by default: it is
indistinguishable, in repo state, from the label never having been
adopted. Whoever opens phase 2 for this record is responsible for
stating explicitly which case applies (label adopted and counted →
mechanical go/kill; label never adopted or nobody counted →
inconclusive) rather than letting elapsed time alone imply a verdict.

## RICE comparison of the two candidate solutions

| Candidate | Reach | Impact | Confidence | Effort | RICE |
|---|---|---|---|---|---|
| (a) Build visual-regression coverage now | 1 (single dashboard, one viewport class) | 2 (moderate — closes a real but unmeasured gap) | 1 (low — occurrence rate unknown, scout sources flag flakiness risk at this reuse scale) | 3 (headless-browser CI infra + baseline maintenance) | 0.67 |
| (b) Keep structural checks + measure before building | 1 | 2 | 3 (high — matches scout-brief's field consensus for single low-reuse surfaces, and reuses an existing signal channel) | 1 (label convention only) | 6.0 |

(Reach/Impact/Confidence scored 1-3, low-medium-high; Effort scored 1-3,
inverted per standard RICE convention so lower effort scores higher —
higher total is better.) Option (b) — measure first, decided by the
registered rule above — scores higher primarily on Confidence and
Effort: it defers the expensive, uncertain build until the registered
metric says it is warranted, per the scout-brief's finding that
visual-regression tooling's value proposition is weakest for a single
low-reuse surface exactly like `rsb`'s dashboard.

## Out of scope

- Reopening REQ-72-1..3 or their verification methods.
- Selecting a specific visual-regression tool/vendor — deferred to the
  go branch's own build issue if the threshold is crossed.
- Any non-layout visual defect class (color/contrast) — out of this
  issue's stated scope (mobile-overflow only).

## How you'll know it worked

The record at `docs/issue-81/reports/product-discovery.md` (phase 2,
written only after human approval) states the registered metric value
next to its threshold, the guardrail status at that same measurement
moment, and a verdict mechanically derived from the rule above — never
fresh judgment at measurement time.

## What did not work

(none yet — appended during phase 2 if applicable)
