# Scout brief — execution-observation (issue #23)

Mode: single targeted lookup (1 stage, no parallel fan-out needed) — the
survey above already identified one directly comparable in-repo system
(the same role, same repo, earlier issue), which is a stronger comparator
than any external audit-methodology search for a repo-internal,
non-product role. Saturation reached after this one lookup: the precedent
resolves the only open build decision (verification method), so no
further round would change it.

## Comparator

`docs/issue-4/reports/execution-observation.md` +
`docs/issue-4/proposals/execution-observation.md` — this same role
verifying an earlier PR (#10, the original `rsb serve`/dashboard build).

## Category must-bes (what a strong pass of this role's own record looks like)

- Every verification claim traces to a raw, reproducible artifact
  (command + output, or file:line), never paraphrase.
- A findings section that hands off defects (with severity + concrete
  impact) rather than silently fixing them.
- An explicit accounting of what could *not* be verified in this
  environment, stated plainly rather than omitted.
- Scope notes closing the loop on what was deliberately left out.

## Performance axes

1. **Reproducibility of evidence** (raw output vs. summary).
2. **Explicit gap-disclosure** (what wasn't checkable, and why).
3. **Severity-graded, non-fixing findings.**

## Adopt

- The record shape: numbered verification sections, a findings section
  with severity + operator-facing impact per item, a scope-notes section,
  explicit citation of file/line and spec section per claim.

## Skip (deliberate deviation from the comparator)

- **Live re-execution.** Issue-4's pass re-ran `pytest` and drove a live
  `webserver.run_server()` over real HTTP. This session's role directive
  prohibits re-running the observed role's code outright — diff/commits/
  its own record are the only admissible evidence. This is a contract
  change since issue-4's pass, not an oversight; the phase-2 proposal
  below substitutes static diff/code-path tracing for live execution and
  says so explicitly rather than quietly reproducing the old method.

## Gap line

Current-state (issue #23 / PR #24) already meets the "raw artifact
citation" and "severity-graded findings" must-bes structurally (the
implementation record itself is heavily self-citing). What issue-4's
precedent has that issue-23's phase 1 must add on its own: an explicit,
up-front statement of *how* verification will happen given the
re-execution prohibition, since the old playbook (re-run + observe) is no
longer available.

## Segment fit

Same role, same repo, one issue apart — direct fit, not an analogy.

Sources:
- `docs/issue-4/reports/execution-observation.md` (this repo, this branch)
- `docs/issue-4/proposals/execution-observation.md` (this repo, this branch)
