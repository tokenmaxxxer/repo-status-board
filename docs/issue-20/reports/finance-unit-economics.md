# Record — rsb SaaS 단위 경제성 분석 (issue-20, phase 2)

Status: FINAL — approved via `APPROVE issue-20/finance-unit-economics` (single-account mode, issue #20 comment). Approver feedback (2건) reflected below; see §2a (NDR), §3 (연환산 churn).

loop_state: reported

Carries forward the methodology and base case from `docs/issue-20/proposals/finance-unit-economics.md` §0-§4, with the two corrections the approval comment required.

## What was done

Finalized the phase-1 base-case/sensitivity analysis into this record per the approved proposal's §6 REQUIRED_FIELDS, applying the two approver-required corrections: (1) NDR 95% was previously declared but unused in the LTV calc — §2a now states explicitly why (margin-based/logo-churn LTV formula, no expansion revenue to justify a revenue-retention formula) and reconciles it against the churn assumption as a consistency check rather than a calc input. (2) The proposal's 48%/yr "annualized churn" was a linear (non-compounding) approximation of 4%/mo churn — §3 replaces it with the compound figure, `1 − 0.96^12 ≈ 38.7%/yr`, and the sensitivity table's annual-churn column is recomputed the same way for every scenario.

## Upstream basis

Rests on `docs/issue-20/proposals/finance-unit-economics.md` (approved phase-1 proposal, this role's own), its cited benchmark sources, and `docs/issue-20/reports/finance-unit-economics/survey.md` / `scout-brief.md` (both written by this role in phase 1). No new research was needed since both approver-required corrections are arithmetic/presentation fixes to already-approved inputs, not new assumptions.

## 1. assumptions_finalized

A1 (product framing), A2 (ARPU $15/seat/mo), A3 (CAC $180) — re-confirmed unchanged; approver feedback targeted only the churn/NDR presentation (§2a, §3 below), not A1-A3.

| Input | Value | Basis |
|---|---|---|
| ARPU (monthly, per seat) | $15 | Assumption (A2), unchanged |
| Gross margin | 88% | Architecture-derived, unchanged |
| CAC | $180 | Assumption (A3), unchanged |
| Monthly churn | 4.0% | Benchmark-derived (SMB dev-tool segment, 3-7%/mo), unchanged |
| NDR | 95% (monthly) | Benchmark-derived — see §2a for how it's used |

## 2a. NDR — reconciliation with churn (approver feedback ①)

The proposal declared NDR 95% but never fed it into the LTV formula. Reason, made explicit: this analysis's canonical LTV formula (proposal §0) is **margin-based and logo-churn-driven** (`LTV = ARPU × gross_margin / monthly_churn`), not a revenue-cohort/expansion-adjusted formula — NDR is the input a revenue-retention-based LTV formula would use instead. Since packaging is single-tier per-seat with no expansion motion (A1), there is no upsell/cross-sell revenue for a revenue-retention LTV model to capture, so switching formulas would add no information the logo-churn formula doesn't already carry.

NDR is therefore not substituted into §3's LTV calculation. Instead it is used here as a **consistency check** on the churn assumption: for a single-tier product with no expansion revenue, expected monthly NDR ≈ `1 − monthly_churn − net_contraction` (contraction = partial downgrades/seat reductions among retained accounts, since there's no upgrade path to offset them). At 4.0%/mo churn and 0% expansion, a "clean" NDR would read ≈96%. The assumed 95% is ~1pp below that, implying a small net-contraction component (~1%/mo, e.g. accounts trimming seats before cancelling) on top of logo churn — consistent with, not contradicting, the 4%/mo churn assumption. No input in §3 changes as a result; NDR's role is confirming the churn assumption is not understated, not feeding the LTV formula.

## 3. base_case_ltv_cac

- LTV = $15 × 0.88 / 0.04 = **$330**
- LTV:CAC = 330 / 180 = **1.83:1** → **FAIL** against canonical 3:1 minimum band (also fails the 4:1 strong band).

**Annualized churn — correction (approver feedback ②):** the proposal's 48% annualized figure (`4% × 12`) was a non-compounding linear approximation and materially overstates the compound figure. Correct compound annualized churn:

`annual_churn = 1 − (1 − monthly_churn)^12 = 1 − 0.96^12 ≈ 1 − 0.6127 ≈ 38.7%/yr`

38.7%/yr (compound) replaces 48%/yr (linear) everywhere in this record and any downstream reference. This does not change the base-case LTV:CAC verdict — §3's LTV formula uses *monthly* churn (4.0%) directly, so the annualized figure was descriptive context only, not a calculation input; only the reported annualized-churn number itself was wrong.

## 4. cac_payback_months

CAC payback = 180 / (15 × 0.88) = 180 / 13.2 = **13.6 months** → within the "healthy" ≤18mo band, above the 12mo self-funding bar, well above the 6mo top-quartile bar. Verdict: **borderline-acceptable**, unchanged from proposal.

## 5. sensitivity_table

| Scenario | ARPU | Monthly churn | Annual churn (compound) | CAC | LTV | LTV:CAC | Payback (mo) | Verdict |
|---|---|---|---|---|---|---|---|---|
| Base case | $15 | 4.0% | 38.7% | $180 | $330 | 1.83:1 | 13.6 | FAIL |
| Upside: churn improves to enterprise-adjacent (1.5%/mo) | $15 | 1.5% | 16.5% | $180 | $880 | 4.89:1 | 13.6 | PASS (strong) |
| Upside: churn improves to B2B-SaaS "good" (1.0%/mo) | $15 | 1.0% | 11.4% | $180 | $1,320 | 7.33:1 | 13.6 | PASS (strong) |
| Upside: ARPU raised to $25/seat, churn unchanged | $25 | 4.0% | 38.7% | $180 | $550 | 3.06:1 | 8.2 | PASS (marginal) |
| Upside: CAC halved via community/PLG motion | $15 | 4.0% | 38.7% | $90 | $330 | 3.67:1 | 6.8 | PASS |
| Downside: CAC doubles, churn worsens to 6%/mo | $15 | 6.0% | 1 − 0.94^12 ≈ 51.7% | $360 | $220 | 0.61:1 | 27.3 | FAIL (badly) |

(Annual-churn column recomputed compound per §3's corrected formula; ratio/payback/verdict columns unchanged from proposal since they were always driven by monthly churn, not the annualized figure.)

## 6. recommendation

**Base-case verdict: unit economics do not clear the canonical bar.** LTV:CAC fails (1.83:1 < 3:1); CAC payback is borderline-acceptable (13.6mo, inside ≤18mo but outside ≤12mo). The binding constraint is churn, not CAC or margin — margin is already near-optimal for this architecture (88%, near-zero COGS), and NDR (§2a) confirms the churn assumption is not overstated.

Two independent levers each individually clear the 3:1 bar (§5): (a) cut monthly churn to ~2.5% or below — retention-focused product work: stickiness features, annual billing to raise switching cost; or (b) raise ARPU to ~$25/seat (still below competing dev-tooling categories) while holding churn flat.

**Go/no-go:** rsb is **not SaaS-unit-economics-viable** at the $15/seat, 4%/mo-churn base case. Before any billing/licensing build work, the two testable levers to validate against real users are:
1. Actual willingness-to-pay above $15/seat.
2. Achievable retention below the SMB-segment median (target ≤2.5%/mo).

CAC is the least sensitive lever — halving it only moves LTV:CAC from 1.83 to 3.67:1 — so GTM/acquisition-cost work should not be prioritized over churn reduction or pricing validation.

## Out of scope (unchanged from proposal §5)
No commitment to build billing/licensing infrastructure. No claim these are measured numbers — all are labeled assumptions or benchmark analogies pending real pricing/telemetry data from a paying pilot cohort.

## 7. Open findings

- The base case FAILS the canonical 3:1 LTV:CAC bar (1.83:1) — SaaS packaging at $15/seat, 4%/mo churn is not viable as modeled; this is a substantive finding for the requester, not a gap in the analysis.
- All inputs remain labeled assumptions or benchmark analogies (survey §"cost-structure facts": rsb has no paying users yet) — no measured pricing, CAC, or retention data exists to replace A1-A3 or the churn/NDR benchmarks. A real pilot cohort would be needed to convert these to measured figures.
- NDR's monthly-vs-annual convention was inferred (§2a treats it as monthly to reconcile against monthly churn); the original benchmark source states SMB NDR ranges without specifying period explicitly. If NDR were intended as an annual figure, the §2a reconciliation would need rework — flagged for any future revision of this record, not resolved here since it does not change §3-§6's numbers.

**Open-finding resolution path / next-steps:**

- Base-case FAIL verdict: the two testable levers (churn ≤2.5%/mo, ARPU ~$25/seat) are the concrete next steps — validating either requires a real pilot cohort with paying users, which is outside this role's phase-2 scope (analysis only, no billing/licensing build).
- Assumption-to-measurement gap: resolved when a future phase collects actual pricing/CAC/retention telemetry from paying users; until then, A1-A3 and the churn/NDR benchmarks stand as the working inputs for any downstream decision.
- NDR period ambiguity: low-priority — does not change any number in §3-§6 — but should be re-checked against source data (or a clarified benchmark) if NDR is ever promoted from a consistency check into a direct model input.

No further iteration is planned by this role unless the approver requests a scope change; this record is the terminal phase-2 deliverable per the proposal's phase-2 plan (documentation-only, no code changes anticipated).

## Sources
Carried forward from `docs/issue-20/proposals/finance-unit-economics.md` §Sources — no new sources introduced in phase 2 (this record only corrects arithmetic and clarifies an unused-input rationale, per approver feedback).
