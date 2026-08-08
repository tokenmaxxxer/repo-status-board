---
status: proposed
files:
  - src/rsb/cli.py
  - test/rsb_tests/test_cli.py
  - src/rsb/web/dashboard.js
  - test/rsb_tests/test_model.py
  - .github/workflows/deploy-board.yml
  - docs/handbooks/rsb.md
---

## Request

The published board renders identically whether it is fresh, stale,
partially failed, or structurally missing sessions/ledger data — a 9.5h
runner outage was invisible because nothing on the page compares its own
age to wall clock, and a partial repo-fetch failure still exits 0 and
deploys green. Fix per issue #58's stated fix direction: a staleness
banner, a loud partial-failure exit code, an explicit decision on the
sessions/ledger panels, and a failure notification on the cron.

## Constraints

- `board.json`'s existing shape (`generated_at`, `generated_at_by_repo`,
  `errors[]`, `sessions[]`, `ledger[]`) is frozen; only the CLI's exit
  code and the JS render layer change, not the payload schema.
- `dashboard.js` has no test framework beyond the `require()`-under-Node
  pattern already used for its exported pure functions
  (`test/rsb_tests/test_model.py`); new logic must fit that pattern, not
  introduce a new one.
- `errors[]` is already rendered (survey.md) — this proposal must not
  duplicate that UI, only make the underlying exit code match it.

## Rationale

For the sessions/ledger panels (D2), the issue's fix direction offers two
options: drop the panels from the CI payload, or publish `runs/` state
somewhere the CI clone can read. The second — teaching CI to read
`on-the-record`'s gitignored `runs/` state — was considered and rejected:
it requires either committing runtime session state to a repo whose
`.gitignore` deliberately excludes it (reverses someone else's design
decision unrelated to this issue) or standing up a new artifact-passing
channel between `on-the-record`'s own workflows and this repo's cron,
which is a cross-repo pipeline change outside a single dashboard fix.
Hiding the panels when their backing data is structurally unavailable is
a same-repo, same-payload-shape change that removes the "nothing is
running" misread without touching another repo's design.

For the staleness threshold, a fixed banner triggered by comparing
`generated_at` to wall clock (issue's own fix direction #1) was chosen
over server-side injection of a `stale: true` flag into `board.json`:
computing staleness at read time means every open tab re-evaluates
staleness on its own clock without needing a new deploy, and it needs no
schema change to `board.json`.

## What will be done

1. `src/rsb/cli.py`: `_run_once` returns `1 if model.errors else 0`
   (was: only on *all* repos failing). Add `--allow-partial` to
   `build_arg_parser`/`main` — when set, a partial failure (some but not
   all repos erroring) still exits 0; an all-repos failure still exits 1
   regardless of the flag (nothing to publish either way).
2. `test/rsb_tests/test_cli.py`: add
   `test_main_partial_failure_returns_1_without_allow_partial` and
   `test_main_partial_failure_with_allow_partial_returns_0`, exercised at
   `cli.main()` level per the issue's acceptance criterion (not just
   `fetch_board()`).
3. `src/rsb/web/dashboard.js`:
   - Add an exported pure function `staleness(generatedAt, nowIso,
     thresholdMs)` returning `null` when fresh or an age-description
     object when stale (threshold: ~1.5 cron periods = 45 min, matching
     the issue's "past ~1.5 cron periods" fix direction against the
     30-min cron in `deploy-board.yml`).
   - Render its result as an unmissable banner (reusing the existing
     `.partial-banner`-style block, new `.staleness-banner` class) above
     `PARTIAL_BANNER` in `renderData()`, naming the actual age (e.g. "last
     updated 3h12m ago").
   - Hide the Sessions and Accounting `<section>`s from `renderData()`'s
     template when `data.sessions.length === 0 && data.ledger.length ===
     0` (structurally-empty-in-CI case) instead of rendering empty
     tables; `isPageEmpty()` and `selectSummary()`'s sessions chip stay as
     they are today since a config with a real local `runs/` (non-CI use
     of `rsb serve`) still needs them.
4. `test/rsb_tests/test_model.py` (or a sibling test file — decided
   during build to whichever keeps the `require()` fixture DRY): tests
   for `staleness()` covering fresh/exactly-at-threshold/stale, driven
   through the same `require("dashboard.js")` pattern already in that
   file.
5. `.github/workflows/deploy-board.yml`: add an `if: failure()` step at
   the end of the `build` job (and the `deploy` job) that posts to a
   webhook URL read from a repo secret (`RSB_ALERT_WEBHOOK`), so a red
   run notifies a channel a human reads instead of only the Actions tab.
   No new dependency — a `curl` step, guarded so a missing secret is a
   silent no-op (documented in the handbook) rather than a second
   failure mode.
6. `docs/handbooks/rsb.md`: document the `RSB_ALERT_WEBHOOK` secret,
   the 45-min staleness threshold and its relation to the 30-min cron,
   and D4's 60-day cron auto-disable fact with an owner note to re-arm
   via any push (or a deliberate empty commit) before ~2026-10-03.

## Out of scope

- D4's actual keepalive mechanism (a scheduled empty-commit workflow or
  similar) is not built — the issue's own fix direction #5 frames this as
  "needs re-arming every 60 days regardless," i.e. an operational
  reminder, not a code defect this issue's acceptance criteria require;
  a keepalive workflow is a separate, riskier change (a workflow that
  commits to `main` on a schedule) better proposed on its own. Documented
  as a dated reminder in the handbook instead, per the doctrine ladder.
- No change to `board.json`'s schema or to `fetch_board`/`gates/flows.py`
  /`spawn.py` — D2 is resolved entirely in the render layer per the
  chosen alternative in Rationale.
- No change to `on-the-record`'s `.gitignore` or `runs/` handling.

## How you'll know it worked

- `rsb --json` against a 1-of-2-repo-failing config exits 1 (was 0);
  the same config with `--allow-partial` exits 0; an all-repos-failing
  config still exits 1 either way. Verified by the new `cli.main()`-level
  tests, not just `fetch_board()`.
- `staleness()` returns non-null for a `generated_at` older than 45 min
  and null for one within it; the rendered page shows the age-naming
  banner only in the stale case.
- With `sessions: []` and `ledger: []`, `renderData()`'s output no longer
  contains the Sessions/Accounting `<section>` markup.
- `deploy-board.yml`'s `build`/`deploy` jobs each carry an `if:
  failure()` notification step.
