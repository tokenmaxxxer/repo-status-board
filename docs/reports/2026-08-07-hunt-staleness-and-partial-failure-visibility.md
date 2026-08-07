---
proposal: docs/issue-58/proposals/2026-08-07-staleness-and-partial-failure-visibility.md
---

# Hunt record — staleness-and-partial-failure-visibility

## before-landing — stance 0: assume the gate just touched is bypassable — find the bypass.

Verdict: NO FINDING
Seed: src/rsb/cli.py `_run_once` exit-code gate; .github/workflows/deploy-board.yml `Generate board.json` step and new `Notify on failure` steps; .github/boards.ci.toml
cap_seconds: 180
tier: default
diff_stat_lines: >200 lines/6 files touched (per dispatcher)
started_at: 2026-08-07T00:00:00Z
ended_at: 2026-08-07T00:20:00Z

Checked: GH Actions default shell for `run:` on ubuntu-latest is `bash -eo pipefail`, so `rsb --config .github/boards.ci.toml --json > board.json` propagates rsb's exit 1 to step failure (redirection doesn't affect `-e`). `.github/boards.ci.toml` has no `--allow-partial` equivalent and the workflow never passes that flag. The two new `Notify on failure` steps use `if: failure()` with no `continue-on-error`, and internally `exit 0` only when `WEBHOOK_URL` is unset — this cannot flip a job's conclusion back to success since a step failing earlier in the job already fixes the job conclusion as failure regardless of later steps' outcomes. `model.errors` is always a `list` (`field(default_factory=list)` in model.py), so `if not model.errors` / `len(model.errors)` are type-safe; no falsy-check bug found. Ran `test/rsb_tests/test_cli.py` (10 tests, incl. `test_main_partial_failure_returns_1_without_allow_partial` / `..._with_allow_partial_returns_0`) directly against `src/` — all pass, confirming the gate behaves as specified. No reproducible bypass found.
