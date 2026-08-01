# Current-state survey — rsb as a SaaS: unit economics

## Scope
issue-20, phase 1. Survey only; no execution/build.

## What exists today (from `main`)
- `docs/handbooks/rsb.md`: rsb is a local CLI (`pip install -e .`, `rsb --config ...`). It reads `<command> flows --json -C <path>` from registered repos via a subprocess boundary and renders a TUI-ish screen (decision queue, flows, sessions, accounting, hygiene, errors). No server, no multi-tenant backend, no auth, no billing.
- `pyproject.toml`: single dependency (`tomli` conditional shim). No SaaS infra (no DB driver, no web framework, no auth lib).
- `README.md`: one-line description, no pricing/target-customer language.
- No pricing page, no cost model, no user-count assumption anywhere in the repo.
- No existing finance/unit-economics methodology handbook under `docs/handbooks/` or `docs/specs/` — searched both trees, found none. The issue references "승인된 finance-unit-economics 방법론 규범" but no such artifact currently exists in this repo; this proposal must therefore define the methodology inline (LTV:CAC formula, canonical bands, CAC payback formula) rather than cite a prior standard, and flags this as a gap for a future `docs/handbooks/finance-unit-economics.md` if the role is used again.
- Current release state: v0.1.0-pilot (per recent commit `63eaac1`), i.e. pre-revenue, no paying users, no observed churn/CAC/ARPU data.

## Implication for this analysis
Every quantitative input (ARPU, CAC, gross margin, churn, NDR) is necessarily a **stated assumption**, not an observed metric — there is no billing/usage telemetry to derive them from. The proposal grounds each assumption against external dev-tool-SaaS benchmarks (see `scout-brief.md`) and labels which are architecture-derived facts (e.g. near-zero COGS because there's no hosted backend) vs. market-benchmark analogies (e.g. churn rate).

## Cost-structure facts derivable from the codebase (not assumptions)
- No hosted service = no per-customer serving cost from rsb itself. If sold as SaaS, the seller would need to *add* infrastructure (e.g. a hosted config/relay service) that doesn't exist today — or sell the CLI as a licensed product with no added hosting, which is the cheaper-COGS path this proposal assumes as the SaaS packaging.
- Distribution is currently a pip package; no license-gating, seat-tracking, or payment integration exists — CAC/billing infra would be net-new build cost, out of scope for this unit-economics analysis but relevant context for whether the numbers are achievable without further engineering investment.

## Gaps this proposal must fill (assumption-labeled)
- Target ARPU / pricing tier
- CAC (paid acquisition cost per customer, given no current GTM motion)
- Gross margin % (derived from the near-zero-COGS fact above, not a benchmark)
- Monthly churn / NDR
- Sales/support cost per account
