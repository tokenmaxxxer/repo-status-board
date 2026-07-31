# Verification proposal — execution-observation (issue #4)

Status: phase-1 proposal. Scope: this role only — plan for
independently reproducing and observing the shipped web dashboard
(`rsb serve`, `src/rsb/web/`), timing H1, re-running the test suite, and
recording conformance against `screen-spec.md`/`design-system.md`. No
code changes. Grounded in the gaps listed in
`docs/issue-4/reports/execution-observation/survey.md`.

## 1. What will be run, and how

1. **pytest re-run**: `python -m pytest test/ -q` against this checkout
   (installing the package editable or setting `PYTHONPATH=src` as
   needed), recording the actual pass/fail count independently of
   implementation.md's stated "33 passed."
2. **Live `rsb serve` run**: start the server against a small
   `boards.toml`/fixture-backed config (or a temporary script driving
   `webserver.make_handler` directly, per survey's environment note),
   then drive it with real HTTP requests (`curl`/`urllib`) and a headless
   browser check of `index.html` if one is available in this environment,
   falling back to direct HTML/CSS/JS inspection plus `/api/board.json`
   response inspection if no browser automation is available.
3. **State reproduction**, one at a time, per screen-spec.md §2:
   - Loading: observed at first paint before `/api/board.json` resolves.
   - Page-empty: all-empty payload (`EMPTY_PAYLOAD` fixture or equivalent).
   - Region-empty: a payload with only some arrays empty.
   - Page-error (total failure): a `fetch_board_fn` that raises for every
     configured repo, or a repo_configs list where every repo errors.
   - Partial-failure banner: a `fetch_board_fn` returning errors for some
     but not all repos.
   - Detail-panel-empty: click a row, then simulate a stale selection
     (data refreshed without that issue) if feasible from the client-side
     code path; otherwise recorded as inspected-by-code-reading, not
     reproduced live, and flagged as such.
4. **H1 timing**: measure wall-clock from request send to
   `/api/board.json` response received, and separately page-load-to-
   render if a browser/automation path is available, across a handful of
   repeated requests (not a single anecdotal sample as implementation.md
   did) — report min/median/max, compared against the ≤3s threshold.
5. **Spec conformance pass**: read `dashboard.js`/`dashboard.css` against
   `screen-spec.md` §1 (9 regions) and `design-system.md` §2.4 (age-bucket
   thresholds, status color mapping) line by line, recording
   match/mismatch per item — not re-trusting implementation.md's
   traceability claim.

## 2. Record format

`docs/issue-4/reports/execution-observation.md` (phase-2 output) will
contain, per role-handoff contract v3 s19's rigor expectations: what was
run (exact commands), what was observed (raw output/timings, not
paraphrase), a state-by-state table (state → reproduced? → matches spec?
→ note), the H1 timing table, the pytest result, and any friction/gaps
surfaced (fed back as on-the-record hand-offs per the issue's pilot
purpose) — explicitly including anything that could not be reproduced in
this environment (e.g. no real browser automation available) rather than
silently skipping it.

## 3. Out of scope

- Any code fix for a discovered defect — this role observes and records;
  a fix, if warranted, is a hand-off to implementation or a new issue,
  not this role's write surface.
- The unresolved auth/access-model and age-bucket-threshold-value
  decisions flagged upstream (hypotheses.md §5, screen-spec.md §5,
  design-system.md §7) — noted if relevant to an observed risk, not
  re-decided here.
- H1's full 14-day pilot-window metrics (off-terminal views/week,
  terminal-fallback rate) — those require real usage over time, not a
  single verification session; this role's H1 check is limited to the
  "≤3s median render" sub-metric, which is testable synchronously.
