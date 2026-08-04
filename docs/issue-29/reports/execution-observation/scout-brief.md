# Scout brief — issue #29 (execution-observation)

Mode: parallel, 1 sweep round, 2 angles (WebSearch, dispatched in one
turn), no deepening round — both angles returned direct, high-consensus,
well-established practices that map onto the survey's specific open
gaps rather than a contested field, so a second round would not change
any verification-method decision. Aimed at the survey's gaps: this
role's re-execution prohibition rules out the obvious answer (run
ESLint/coverage tooling or a real browser), so the sweep targets how
manual/static review substitutes for those tools for the two exact
defect *classes* already named in issue #29's comments — "implemented
but never called" and "ARIA state doesn't reflect reality."

**Category must-bes** (dead-code/unwired-function detection): tooling
answer is static analysis (`no-unused-vars`, `ts-prune`-style unused-
export detection) or dynamic/coverage-based (flag functions with 0%
exercised call paths across runs); the manual substitute named
explicitly alongside those tools is targeted code review that traces
every exported function to at least one real call site, not just to a
test file. **Category must-bes** (ARIA disclosure pattern): the toggle
must be a real `<button>`; `aria-expanded` is a *state* attribute that
must flip with the actual expand/collapse it claims to describe, not a
static/dead value; `aria-controls` must reference an id that actually
exists in the rendered DOM. WebAIM's cited 2023 finding — 58% of
expandable widgets get `aria-expanded` wrong — indicates this exact
failure mode (state attribute present but not wired to real state) is
the field's single most common disclosure-pattern defect, not an
edge case.

**Chosen performance axis**: trace-to-real-usage over trace-to-test —
for both defect classes the field's own guidance is that a function
having test coverage, or a state attribute existing in markup, proves
nothing about whether it is wired into the real runtime path; only
tracing an actual call site (for JS exports) or an actual state
transition (for ARIA) does. This directly targets the specific failure
shape survey gap 1-3 already found: `filterByRepo()`/`repoList()` were
tested and still had zero real callers; `aria-expanded` exists in
markup and is spec-correct in isolation but is wired to a field
(`selectedIssue.sourceTable`) that is never set.

**Adopt**: (a) for every export in the PR #30/#33 diffs, grep its call
sites in non-test files specifically, not just confirm it appears in
`module.exports` or a test file; (b) for every `aria-expanded`/
`aria-controls` pair, hand-trace the actual JS state variable each one
reads, back to whatever last assigns it, rather than trusting the
attribute's presence in the rendered HTML string.

**Skip**: running any static-analysis tool (ESLint, `ts-prune`) or a
real browser/coverage run — both are the field's own preferred method,
but both require executing the observed role's code (or code that
would exercise it), which this role's contract prohibits; the manual
trace substitutes are adopted instead, same substitution issue-23's
own execution-observation precedent already made for its own
re-execution prohibition.

**Segment fit**: `dashboard.js` is a small (~570-line), no-build,
vanilla-JS file with an existing `module.exports`-based pure-function
test harness and no browser-only test runner — the generic dead-
export/ARIA-state guidance applies directly (grep + hand-trace is
tractable at this size); no scaling-down or tool-selection decision is
needed.

**Gap line**: current project state has no linter/static-analysis
config at all (no `.eslintrc`, no `package.json` devDependency for
JS tooling — confirmed by this file's own existing test harness being
`pytest`-driven `node -e`/subprocess calls, not a JS test runner) — so
the field's preferred *automated* detection is unavailable here
regardless of this role's own re-execution prohibition; the gap this
scout closes is method (what manual trace to run in its place), not
tool selection.

**Judge point / saturation**: would another round change a verification
decision? No — both angles returned the same two concrete, directly
applicable checks (real-call-site trace; real-state-transition trace)
with no competing method surfaced; stopped after stage 1.

Sources:
- https://blog.logrocket.com/how-detect-dead-code-frontend-project/
- https://github.com/denisoed/dead-code-checker
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-expanded
- https://www.makethingsaccessible.com/guides/accessible-basic-disclosure-widgets/
