# Scout brief — conformance-review, issue #44 phase 1

Segment: auditing a **test-harness deliverable** (test code + its docs + a first
runtime dependency), not a product surface. So the field scouted is what strong
audits of test artifacts check, not what strong dashboards look like.

Mode: parallel WebSearch fan-out, 4 angles in one turn (test-code review /
false-negative tests; pre-fix failure + mutation evidence; ISO 29119-3
traceability; test-only npm dependency placement), then 1 deepening round on
skip-vs-fail semantics. **2 stages**, 16:23:13→16:23:40, aimed at survey
unknowns U1–U9.

## Category must-bes

- A defect-tracing test's evidence is *retest semantics*: it must be shown to
  fail on the pre-fix code and pass after — asserted-in-prose is not shown.
  Mutation-guided work makes the same point from the other side: suites that
  never fail against a mutated/pre-fix program are silently accepting incorrect
  implementations.
- Traceability runs test basis → test case → **result**, with explicit evidence
  links; that link, not the test's existence, is what makes it auditable.
- No always-passing tests: assertion strength is the primary review target,
  because a test that cannot fail reads exactly like a passing one.
- Executed ≠ collected. Silent skips on a missing dependency give false
  assurance; rails/rails deliberately makes skip fail in CI, and
  `pytest-error-for-skips` exists for the same reason.
- A test-only package belongs in `devDependencies`, not `dependencies`.

## Performance axes the field competes on

1. **Evidence reproducibility** — a re-runnable command beats a claim.
2. **Traceability granularity** — 1:1 requirement↔test↔result, no bundling.
3. **Failure visibility** — how loudly the suite reports "did not actually run".

## Adopt / skip

- **Adopt:** re-derive AC2's pre-fix failures myself rather than scoring the
  record's account of them, and record the exact command per requirement
  (issue-34's method-per-requirement form already fits this).
- **Adopt:** an executed-vs-skipped count as evidence for AC1/AC3, never a bare
  "passed".
- **Skip:** a mutation-testing sweep / mutation score. Issue #44 asks for four
  specific defect-tracing tests, not a suite-wide adequacy metric; that would be
  a different deliverable and outside this role's remit.

## Gap line

Already met by the current state: per-test defect mapping and an AC crosswalk
exist in the merged record; traceability form is present. Missing against the
field's must-bes: **reproducible** pre-fix failure evidence (scratch files
deleted, U2), the executed-vs-skipped distinction (all 8 tests skip here today,
U4), and `devDependencies` placement (U5). Those three are exactly where this
review's verification effort goes.

Sources:
- https://www.browserstack.com/guide/false-positives-and-false-negatives-in-testing
- https://octomind.dev/blog/did-you-break-your-code-or-is-the-test-flaky
- https://arxiv.org/pdf/2604.01518 (mutation-guided diagnosis of regression suites)
- https://cdn.standards.iteh.ai/samples/79429/27623aa24dba41a2876884c0ec57f5d7/ISO-IEC-IEEE-29119-3-2021.pdf
- https://quality.arc42.org/standards/iso-iec-ieee-29119
- https://docs.npmjs.com/specifying-dependencies-and-devdependencies-in-a-package-json-file/
- https://github.com/dperini/nwsapi/issues/25
- https://railsatscale.com/2026-06-08-how-i-think-about-tests-skips/
- https://pypi.org/project/pytest-error-for-skips/2.0.0/
- https://docs.pytest.org/en/stable/how-to/skipping.html
