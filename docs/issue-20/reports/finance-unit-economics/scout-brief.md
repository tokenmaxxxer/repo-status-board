# Scout brief — dev-tool SaaS unit-economics benchmarks

Mode: parallel WebSearch (4 angles, 1 sweep round), no snowball round needed — signal converged across sources on first pass. Stages used: 1 (sweep) + judge point, saturation reached (another round would not change build decisions). Wall-clock: well under budget.

## Angles run
1. LTV:CAC ratio canonical band
2. CAC payback period
3. Churn / NRR
4. Gross margin (per-seat SaaS)

## Must-bes (category floor a benchmarkable SaaS is expected to clear)
- LTV:CAC >= 3:1 is the accepted minimum; 4:1+ preferred by investors.
- CAC payback under ~18 months is "healthy"; under 12 months = self-funding growth; top quartile <=6 months.
- Gross margin 70-85% is the mature-SaaS band for subscription (non-usage-billed) products; early-stage/small teams can be lower (50-65%) but a CLI tool with no hosted infra should sit at the high end (minimal COGS).
- Annual churn <5% (monthly <1%) is "good" for B2B SaaS; SMB-focused tools commonly run 3-7% monthly, i.e. worse.

## Performance axes competitors are judged on
- CAC payback speed (6 vs 16 vs 24 months = top/median/bottom quartile)
- NRR (best-in-class >130%, good 100-120%, concerning <100%; SMB typically 90-105%)
- Gross margin efficiency (subscription vs usage-billed spread: 76-84% vs 62%)

## Adopt / skip
- Adopt: treat 3:1 LTV:CAC and <=18mo CAC payback as canonical pass/fail bands for the verdict (matches issue's "canonical 밴드 대비 판정" requirement).
- Adopt: given rsb has no server-side hosting cost (local CLI reading local/subprocess data), model gross margin at the high end of the SaaS band (85-90%) rather than the 70-85% "mature SaaS" default — the product's COGS is near-zero (no infra to scale), which is a genuine dev-tool-CLI differentiator, not a generic SaaS assumption.
- Skip: usage-based/consumption pricing benchmarks — rsb is a per-seat/flat-fee candidate given its config model, not a metered product; those benchmarks (Orb, usage-COGS heavy) don't fit.

## Segment fit
rsb is a solo/small-team internal-tooling CLI (no multi-tenant hosting), closest analog = "SMB-focused bootstrapped dev tool," which the survey flags as running worse-than-median churn (3-7%/mo) and thinner NRR (90-105%) than enterprise SaaS — this segment reality, not generic SaaS medians, should anchor the base-case churn/NRR assumption.

## Gap line
Current state (docs/handbooks/rsb.md, pyproject.toml) has **no pricing, no cost model, no user-count assumption at all** — none of the must-bes above are met today because the product has never been priced or costed as a SaaS. Everything in the proposal is necessarily assumption-driven (labeled), grounded against these external bands rather than any internal baseline.

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
