# Scout brief — execution-observation (issue #34)

Mode: single targeted lookup (1 stage, no parallel fan-out) — the survey
above already identified the strongest possible comparator: this same
role, same repo, its two prior passes (`issue-23/execution-observation`
and `issue-27/execution-observation`), which between them already settled
the re-execution-prohibition method and the record shape. Saturation
reached after this one lookup — a second round (e.g. an external audit-
methodology search) would not change any build decision for a repo-
internal, non-product role whose record format is dictated by this
session's own role-handoff contract, not by external audit conventions.

## Comparator

`docs/issue-23/reports/execution-observation/{survey.md,scout-brief.md}`,
`docs/issue-23/proposals/execution-observation.md`,
`docs/issue-23/reports/execution-observation.md` (landed, `main`), and —
via `git show origin/issue-27/execution-observation:<path>` —
`docs/issue-27/reports/execution-observation/scout-brief.md` and
`docs/issue-27/proposals/execution-observation.md` (not yet landed on
`main`). All read in full this session.

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

- The record shape both prior passes established: independence statement
  first, three-level verdict each with adjacent citation, per-acceptance-
  criterion table, four-part blameless finding shape, `loop_state` field.
- The re-execution substitute method both prior passes already settled:
  static diff/config tracing by hand through each named case, test-suite
  results reported as *claimed*, not independently reproduced.
- Issue-27's precedent for handling a caveat that is real but not this
  PR's own defect (its `fetch.py` timeout finding, cited by PR-comment URL
  and treated as outcome-level context rather than a step finding): the
  same shape applies here to issue #36 (see "Skip" below for why it is
  *not* a direct copy of that precedent).

## Skip (deliberate deviation from the comparator)

- **Treating a post-merge-discovered, already-split-off issue as pre-
  decided "not this PR's defect."** Issue-27's `fetch.py` finding was
  reported by a PR *comment*, on the *same* PR, before merge, and the
  commenter explicitly framed it as out-of-scope for that PR. Issue #36 is
  different in kind: it is a **separate, user-filed GitHub issue**, opened
  **after** PR #35 merged, reporting a **real-browser** observation
  (column-width wrapping) that PR #35's own record disclosed it could not
  check in this sandbox and recommended checking "before or shortly after
  merge." Copying issue-27's shortcut (cite and move on) would skip the
  actual open question this pass must answer: whether PR #35's own
  disclosed gap is what let the issue #36 defect ship, which is a
  trajectory/step question this comparator's precedent never had to
  answer (its unmerged-PR ACs were marked not-yet-verifiable, never
  reported as *shipped-and-wrong*). This pass's proposal must state
  explicitly how it will trace whether the implementation record's stated
  rationale for the *other* known gap (row-to-row alignment when a link is
  missing) is consistent with, or actually addresses, the wrap defect
  issue #36 reports — not assume they're the same finding just because
  both involve the ↗ glyph.

## Gap line

Current state (issue #34 / PR #35) already meets the "raw artifact
citation" must-be structurally — the implementation record is heavily
self-citing with its own `closed_checks` section and an explicit "Open
findings" disclosure, matching both prior passes' adopted shape. What
neither issue-23's nor issue-27's precedent covers, and this pass's
proposal must add on its own: a method for judging a *shipped* defect
that was disclosed as an open risk pre-merge and then materialized
exactly as predicted post-merge and was — correctly or not — routed to a
brand-new issue rather than reopening PR #35.

## Segment fit

Same role, same repo — direct fit, not an analogy.

Sources:
- `docs/issue-23/reports/execution-observation/survey.md` (this repo, `main`)
- `docs/issue-23/reports/execution-observation/scout-brief.md` (this repo, `main`)
- `docs/issue-23/proposals/execution-observation.md` (this repo, `main`)
- `docs/issue-23/reports/execution-observation.md` (this repo, `main`)
- `docs/issue-27/reports/execution-observation/scout-brief.md` (this repo, `origin/issue-27/execution-observation`)
- `docs/issue-27/proposals/execution-observation.md` (this repo, `origin/issue-27/execution-observation`)
