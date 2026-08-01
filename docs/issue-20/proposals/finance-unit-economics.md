# Proposal — rsb SaaS 단위 경제성 분석 (issue-20, phase 1)

Status: PROPOSAL — awaiting approval per role-handoff contract v3 s19 (this is not the finished analysis; phase 2 delivers the full record after approval).

## 0. Methodology note
No prior `finance-unit-economics` methodology handbook exists in this repo (see `reports/finance-unit-economics/survey.md`). This proposal defines the methodology inline, per the issue's explicit requirements:
- **LTV** = 마진 기반 (margin-based): `LTV = ARPU_monthly × gross_margin% / monthly_churn%`
- **CAC:LTV 판정 밴드** (canonical, per `scout-brief.md`): `>=3:1` = pass (industry minimum), `>=4:1` = strong (investor-preferred), `<3:1` = fail.
- **CAC 회수 기간** = `CAC / (ARPU_monthly × gross_margin%)`, canonical bands: `<=6mo` top quartile, `<=12mo` self-funding, `<=18mo` healthy median, `>18mo` weak.
- Churn/NDR assumptions stated explicitly, labeled assumption vs. benchmark-derived.

This role's mandate (단위경제상 성립하는가) is answered directly in §3-§4: the base case does not satisfy it, therefore a source-or-assumption trail for every input is necessary (필요) before the verdict can be trusted — each metric in §2 is tagged either "Assumption" (labeled A1-A3, no external source) or "Benchmark-derived" with a source in the Sources list below, working from named-framework assumption where no measured data exists (survey §"Implication for this analysis").

## 1. Product framing (assumption, labeled A1)
rsb sold as a licensed SaaS subscription (not usage-metered) to small dev teams running multi-repo agentic-orchestration workflows — the natural buyer given the tool's decision-queue/flows/accounting screen. Packaging: per-seat monthly subscription, no added hosted backend (CLI stays local; "SaaS" = license + update/support channel), preserving the near-zero-COGS fact from the survey.

## 2. Base-case assumptions

| Input | Value | Basis |
|---|---|---|
| ARPU (monthly, per seat) | $15 | Assumption (A2) — positioned as a low-friction dev-tool add-on price, below typical $20-50/seat PM-tool pricing given rsb's narrow scope. |
| Gross margin | 88% | Architecture-derived (survey §"Cost-structure facts") — no hosted infra; COGS = payment processing + minimal support, near top of the 70-85% mature-SaaS band, adjusted up for CLI-only delivery. |
| CAC | $180 | Assumption (A3) — no existing GTM motion (survey), so CAC is modeled as founder-led content/community acquisition for a narrow dev-tool niche, benchmarked low relative to generic B2B SaaS CAC given no outbound sales cost. |
| Monthly churn | 4% (48% annualized) | Benchmark-derived (scout-brief) — SMB-focused bootstrapped dev tool segment runs 3-7%/mo, not enterprise's 1-2%; base case picks the segment's own median, not generic B2B SaaS's <1%/mo "good" bar. |
| NDR | 95% | Benchmark-derived — SMB segment typically 90-105% (scout-brief), no expansion motion (single-tier pricing) assumed, so no upsell to push above 100%. |

## 3. Base-case calculation

- LTV = $15 × 0.88 / 0.04 = **$330**
- LTV:CAC = 330 / 180 = **1.83:1** → **FAIL** against canonical 3:1 minimum band.
- CAC payback = 180 / (15 × 0.88) = 180 / 13.2 = **13.6 months** → within the "healthy" <=18mo band but above the 12mo self-funding bar.

**Base-case verdict: unit economics do not clear the canonical bar.** LTV:CAC fails (1.83:1 < 3:1); CAC payback is borderline-acceptable. The binding constraint is churn, not CAC or margin.

## 4. Sensitivity / scenario analysis

| Scenario | ARPU | Churn | CAC | LTV | LTV:CAC | Payback (mo) | Verdict |
|---|---|---|---|---|---|---|---|
| Base | $15 | 4.0% | $180 | $330 | 1.83:1 | 13.6 | FAIL |
| Churn improves to enterprise-adjacent (1.5%) | $15 | 1.5% | $180 | $880 | 4.89:1 | 13.6 | PASS (strong) |
| Churn improves to B2B-SaaS "good" (1.0%) | $15 | 1.0% | $180 | $1,320 | 7.33:1 | 13.6 | PASS (strong) |
| ARPU raised to $25/seat, churn unchanged | $25 | 4.0% | $180 | $550 | 3.06:1 | 8.2 | PASS (marginal) |
| CAC halved via community/PLG motion | $15 | 4.0% | $90 | $330 | 3.67:1 | 6.8 | PASS |
| Pessimistic: CAC doubles, churn worsens to 6% | $15 | 6.0% | $360 | $220 | 0.61:1 | 27.3 | FAIL (badly) |

**Evidence → recommendation chain:**
1. Survey shows rsb has zero hosted infra → gross margin can legitimately sit near the top of the SaaS band (88%), which is the analysis's strongest asset.
2. Scout brief shows canonical LTV:CAC floor is 3:1 and this segment's churn reality (SMB dev tools) is 3-7%/mo, materially worse than the <1%/mo needed to hit 3:1 at $15 ARPU and $180 CAC.
3. Base-case arithmetic (§3) shows the model fails on churn, not on margin or CAC — margin is already near-optimal for this architecture, so the lever that moves the ratio most is churn reduction or price increase, not cost-cutting.
4. Sensitivity table shows **two independent levers each individually clear the bar**: (a) cut monthly churn to ~2.5% or below (retention-focused product work: stickiness features, annual billing to lock in switching cost), or (b) raise ARPU to ~$25/seat (still low relative to competing dev-tooling categories) while holding churn flat.
5. **Recommendation**: rsb is not SaaS-unit-economics-viable at low-price/high-churn assumptions. Before phase 2 execution work (if approved), the two testable levers to validate are: (a) actual willingness-to-pay above $15/seat, and (b) achievable retention below the SMB-segment median — both are currently assumptions, not measurements, because rsb has no paying users yet (survey §"cost-structure facts"). The CAC assumption ($180) is the least sensitive lever (halving it only moves LTV:CAC from 1.83 to 3.67, i.e. it matters, but churn/ARPU dominate the outcome more directly per unit of assumption-uncertainty).

## 5. Explicitly out of scope for phase 1
- No commitment to build billing/licensing infrastructure — that's a build decision, not covered here.
- No claim these are measured numbers; all are labeled assumptions or benchmark analogies pending real pricing/telemetry data (would require phase-2 or later a real pilot cohort).

## 6. Phase 2 reflection plan

Phase 2, on approval, produces: `docs/issue-20/reports/finance-unit-economics.md`, the finalized unit-economics record.

REQUIRED_FIELDS:
- `assumptions_finalized`: A1-A3 (product framing, ARPU, CAC) re-confirmed or revised per approver feedback captured in the PR review.
- `base_case_ltv_cac`: restated LTV:CAC ratio and verdict against the 3:1/4:1 canonical bands, carried forward from §3 unless approver feedback changes an input.
- `cac_payback_months`: restated payback figure and verdict against the 6/12/18-month canonical bands.
- `sensitivity_table`: the §4 scenario table, extended with any additional scenario an approver requests.
- `recommendation`: the final go/no-go read on SaaS viability, plus the two testable levers (churn reduction, ARPU increase) named as the next validation step.
- No code changes are anticipated in phase 2 — this is a pure analysis deliverable; phase 2 is documentation-only unless the approver redirects scope.

## Decision requested

Approve this phase-1 proposal (survey + methodology + base-case + sensitivity analysis) so phase 2 can finalize `docs/issue-20/reports/finance-unit-economics.md` from the same assumptions, or return feedback on any of A1 (SaaS packaging), A2 (ARPU/CAC), or the churn/NDR benchmarks in §2 for revision before phase 2 starts.

## Sources
- [B2B SaaS LTV Benchmarks — Optifai](https://optif.ai/learn/questions/b2b-saas-ltv-benchmark/)
- [SaaS CAC Benchmarks 2025 — Proven SaaS](https://proven-saas.com/blog/saas-cac-benchmarks-2025)
- [CAC Payback Period benchmarks — Aleph](https://www.getaleph.com/answers/cac-payback-period-saas-2026)
- [2025 SaaS Benchmarks: CAC Payback — ScaleXP](https://www.scalexp.com/blog/blog-saas-benchmarks-cac-payback-2025/)
- [B2B SaaS Churn Rate Benchmarks — Optifai](https://optif.ai/learn/questions/b2b-saas-churn-rate-benchmark/)
- [2025 SaaS Churn Rate — Vena](https://www.venasolutions.com/blog/saas-churn-rate)
- [B2B SaaS NRR Benchmarks — Optifai](https://optif.ai/learn/questions/b2b-saas-net-revenue-retention-benchmark/)
- [SaaS gross margin benchmark — Aleph](https://www.getaleph.com/answers/saas-gross-margin-2026)
- [2026 Benchmarking Metrics for Bootstrapped SaaS — SaaS Capital](https://www.saas-capital.com/blog-posts/benchmarking-metrics-for-bootstrapped-saas-companies/)
