# Scout brief — execution-observation (issue #27)

Mode: single targeted lookup (1 stage, no parallel fan-out) — the survey
above already identified the strongest possible comparator: the same
role, same repo, one issue apart (`issue-23/execution-observation`),
which itself already resolved the one open build decision this pass
shares (verification method under the re-execution prohibition).
Saturation reached after this one lookup — a second round (e.g. an
external audit-methodology search) would not change any build decision
for a repo-internal, non-product role.

## Comparator

`docs/issue-23/reports/execution-observation/survey.md`,
`scout-brief.md`, `docs/issue-23/proposals/execution-observation.md`,
and the landed `docs/issue-23/reports/execution-observation.md` — this
same role verifying an earlier PR (#24), all read in full this session.

## Category must-bes (carried over, still true for this pass)

- Every verification claim traces to a raw, reproducible artifact
  (command + output, or file:line), never paraphrase.
- A findings section that hands off defects (severity + concrete impact)
  rather than silently fixing them.
- Explicit accounting of what could *not* be verified in this
  environment, stated plainly rather than omitted.
- Independence statement precedes any verdict language.

## Performance axes

1. Reproducibility of evidence (raw output vs. summary).
2. Explicit gap-disclosure (what wasn't checkable, and why).
3. Severity-graded, non-fixing findings.

## Adopt

- The record shape issue-23 established: independence statement first,
  three-level verdict each with adjacent citation, per-acceptance-
  criterion table, four-part blameless finding shape, `loop_state` field.
- The re-execution substitute method issue-23 already settled: static
  diff/config tracing by hand through each named case, test-suite
  results reported as *claimed*, not independently reproduced.

## Skip (deliberate deviation from the comparator)

- **Treating "merged" as the baseline state.** Issue-23's PR #24 was
  already merged to `main` before execution-observation's phase 1
  started, so its proposal only had to plan around the re-execution
  prohibition. PR #28 is still **open/unmerged** — this pass's proposal
  must additionally plan around acceptance criteria that are structurally
  unverifiable pre-merge (live Pages render, cron-tick advance,
  fail-safety demonstration), marking them "not yet verifiable" rather
  than forcing a pass/fail. This is a genuinely new decision the
  comparator doesn't cover, not an oversight to copy past.

## Gap line

Current state (issue #27 / PR #28) already meets the "raw artifact
citation" must-be structurally — the implementation record is heavily
self-citing with its own `closed_checks` section, similar to issue-23's
precedent. What issue-23's precedent does *not* cover and this pass's
proposal must add on its own: (1) explicit unmerged-PR handling for the
3 live-runner-only acceptance criteria, and (2) explicit handling of a
PR comment (the `fetch.py` timeout finding) that arrived after the
phase-2 commit and is deployment-readiness-relevant but not a step
deficiency in PR #28 itself.

## Segment fit

Same role, same repo, one issue apart — direct fit, not an analogy.

Sources:
- `docs/issue-23/reports/execution-observation/survey.md` (this repo, `main`)
- `docs/issue-23/reports/execution-observation/scout-brief.md` (this repo, `main`)
- `docs/issue-23/proposals/execution-observation.md` (this repo, `main`)
- `docs/issue-23/reports/execution-observation.md` (this repo, `main`)
