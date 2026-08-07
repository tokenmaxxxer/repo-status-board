# Survey — issue #58

Skip condition: N/A — scouting was run (product-shaped UI surface: staleness banner).

## Current state

- `src/rsb/cli.py:73-74` — `_run_once` computes `all_failed` and returns
  `1 if all_failed else 0`. Non-`all_failed` partial errors return 0.
  `main()` returns this value straight to `sys.exit` (bottom of file, not
  shown above but confirmed by `test_main_all_repos_failed_returns_1`).
- `src/rsb/web/dashboard.js`:
  - `renderErrors()` (:355) and the `PARTIAL_BANNER` block in
    `renderData()` (:594-604) **already render `errors[]`** — a partial
    banner with per-repo detail and a Retry button. The issue text's claim
    that `errors[]` "is never rendered anywhere" is stale relative to the
    current tree; D1's live defect is only the CLI exit code / CI gate.
  - No code anywhere compares `data.generated_at` to wall-clock time. No
    staleness banner exists. `HEADER_META` just prints `as of
    ${data.generated_at}`.
  - `selectSummary()` (:74-92) computes a `sessions` chip
    (`${data.sessions.length} sessions active`) and `isPageEmpty()` — both
    read `sessions`/`ledger` as ordinary board content, not as "unknown in
    this environment."
  - `renderData()` unconditionally renders a `<h2>Sessions</h2>` table
    (:625-628) and an `<h2>Accounting</h2>` ledger table (:637-640).
- `gates/flows.py:141-142` `_ledger_read()` and `spawn.py:1275,1291-1295`
  `_roster_load()` both read from `ROOT/runs/...`, which is
  `.gitignore`d in `on-the-record` (confirmed: first line of that repo's
  `.gitignore`, `git ls-files runs/` empty). CI's `actions/checkout` of
  `on-the-record` never has this path — sessions/ledger are structurally
  `[]` in every CI-built board, permanently.
- `.github/workflows/deploy-board.yml` — single `build`+`deploy` job pair,
  `schedule: */30 * * * *` + `workflow_dispatch`. No failure notification
  step; a red run is only visible to someone who checks the Actions tab.
  `pushed_at` 2026-08-04T10:33:16Z; GitHub disables schedules after 60
  days with no push (confirmed via issue text, not independently
  re-checked here since it requires no code read).
- `test/rsb_tests/test_cli.py` already has
  `test_main_all_repos_failed_returns_1` (partial-not-all-failed is
  untested) — the exit-code fix's test slot is obvious.
- No JS test harness exists for `dashboard.js` beyond
  `test/rsb_tests/test_model.py`'s `require()` of exported pure functions
  (see the bottom `module.exports` guard) — staleness logic should be
  written as a small pure function (`isStale(generatedAt, now, thresholdMs)`)
  exported the same way, so it's testable from Python via the same
  `require()` pattern already in use.

## Scout brief (skip record)

This is a defensive/reliability fix to an internal ops dashboard with one
external reader convention (the orchestrator routes off this board) and
no public users — not a category with meaningful "best-in-class" product
exemplars to benchmark against (a staleness banner's shape is dictated
entirely by the existing page's own visual language in
`src/rsb/web/index.html`/CSS, not by market convention). Per the scout
directive's skip conditions, this also reduces to a near-bugfix: the
issue text already names the exact defect lines, the fix mechanism per
defect, and the acceptance criteria — there is no open design decision
about *what* to build, only *how* to fit it into the existing render
pipeline. Scouting is skipped on that basis; one line: "spec leaves no
material design decision open — the issue pins mechanism and acceptance
criteria for every defect."

## Write-set implications

Confirmed write set (see proposal): `src/rsb/cli.py`,
`test/rsb_tests/test_cli.py`, `src/rsb/web/dashboard.js`,
`test/rsb_tests/test_model.py` (or a new
`test/rsb_tests/test_dashboard_staleness.py`), `.github/workflows/deploy-board.yml`,
`docs/handbooks/` (cron re-arm reminder — D4 is a process fact, not code;
belongs in a handbook per the doctrine ladder, not invented as a script).
