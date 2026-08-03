files:
- .github/workflows/deploy-board.yml
- .github/boards.ci.toml
- src/rsb/web/dashboard.js
- docs/handbooks/rsb.md

## Request

Take the dashboard fully remote: a GitHub Actions cron workflow
generates `board.json` for the merged 3-board view (on-the-record,
repo-status-board, tokenmaxxxer-core) and publishes it together with
the existing static dashboard files to GitHub Pages, so an operator can
see the board from any device without a terminal or a local `rsb serve`
process. All three board repos are public, so the runner's default
`GITHUB_TOKEN` is sufficient — no PAT or secrets needed. `sessions[]`
and `ledger[]` are accepted to render empty in the Pages output (they
are local-orchestrator-only data per `flows-schema.md` §5), which
exposes no new information beyond what is already public via issues/PRs.
The dashboard is already no-build static HTML+JS, so no structural
rewrite is implied — only a static-generation path added alongside the
existing local `rsb serve` path, which must keep working unchanged.

## Constraints

- Workflow must combine `schedule` (cron) and `workflow_dispatch`
  (requirement 1).
- Generation must checkout all 3 board repos plus the on-the-record
  checkout that provides `spawn.py`, run `flows --json` per repo, and
  reuse this repo's existing fetch/merge/render logic
  (`fetch_board` → `merge_repos` → `render_json_model`) rather than
  reimplementing it — the choice of generation entrypoint (existing
  `--json` flag vs. a new CLI verb) is left open by the issue and must
  be decided in this proposal (see Rationale).
- The dashboard's board-fetch path (`/api/board.json` in
  `dashboard.js`) must work against a static `board.json` file as well
  as the existing live local-serve endpoint, with zero regression to
  local `rsb serve` behavior (requirement 2).
- Pages output must include both the static dashboard files and
  `board.json`, and must preserve the existing `generated_at` /
  `generated_at_by_repo` timestamps so data freshness stays visible
  (requirement 3).
- `runs/`-absence behavior (no prior orchestrator state on a fresh
  runner checkout) must not error `flows --json`; if it does, the issue
  is blocked and on-the-record must be notified (requirement 4).
- A failed generation run must never overwrite the last good Pages
  deployment — no publishing partial/broken `board.json` (requirement
  5).
- Acceptance criteria (6, verbatim from the issue): merged 3-repo board
  renders at the Pages URL (Flows/Decision queue/Hygiene, plan
  rendering included); `board.json` refreshes every cron tick
  (as-of timestamp visibly changes); empty sessions/ledger render
  cleanly via existing empty-state handling; local `rsb serve` has no
  regression (existing test suite passes); a failed workflow run is
  confirmed to leave the prior deployment live; and the PR body for
  this work must never contain a closing keyword (`close(s/d)`,
  `fix(es/ed)`, `resolve(s/d)`) immediately followed by `#27`, in any
  form including backticks or quotes (issue #23 T2 precedent).

## Rationale

**Generation entrypoint — reuse existing `--json` flag vs. add a new
CLI verb (e.g. `rsb build-static`).** Chosen: reuse the existing
`--json` flag with a CI-only config file, wired up by a couple of shell
lines (`mkdir`, `cp`, redirect) in the workflow, no new rsb code.

Alternative considered and rejected: add a dedicated `rsb build-static`
(or similar) subcommand that writes the `_site/` layout directly.
Rejected because — `--json` is already stdout-safe, already has the
right exit-code semantics for gating (survey §1: 0 = usable output,
1 = total failure, 2 = config error), and already emits byte-for-byte
the same payload the local-serve `/api/board.json` handler returns
(survey §5, both call `render_json_model`). A new subcommand would need
new argparse wiring, a new code path, and new tests to cover something
that a 2-line shell assembly step on top of an already-correct,
already-tested code path covers just as well. Adding CLI surface for a
one-time infra need is complexity without a matching benefit.

**Job structure — split build/deploy jobs with `if:`/`needs:` gating vs.
a single combined job.** Chosen: two jobs (`build`, `deploy`), with
`deploy` gated on `build`'s success via `needs:` + a job-level `if:`.

Alternative considered and rejected: one job that generates, assembles,
and deploys in a linear sequence of steps. Rejected because — this is
GitHub's own documented pattern specifically because job-level failure
isolation is what guarantees requirement 5 (scout-brief.md): if
generation fails inside a single job, later steps in the *same* job
still don't run, but a single job with an unconditional Pages-deploy
step still risks becoming order-fragile as the workflow grows (e.g. a
future step reordering could accidentally deploy before a check runs).
A distinct `deploy` job whose entire existence is contingent on
`build`'s job-level success is a stronger, more legible guarantee, and
matches the idiomatic shape every current GitHub Pages custom-workflow
example uses.

## What will be done

1. Add `.github/workflows/deploy-board.yml`:
   - Triggers: `schedule: [{cron: '*/30 * * * *'}]` (30-minute default,
     per the issue's own suggestion — cheap since all 3 repos are
     public/free) + `workflow_dispatch:`.
   - `permissions: contents: read, pages: write, id-token: write`.
   - `concurrency: { group: pages, cancel-in-progress: false }` so an
     overlapping cron tick can't race a slow in-flight run.
   - Job `build`: checkout this repo (default, root) + checkout
     `tokenmaxxxer/on-the-record` to `_boards/on-the-record` + checkout
     `tokenmaxxxer/tokenmaxxxer-core` to `_boards/tokenmaxxxer-core`
     (all public, default `GITHUB_TOKEN` is sufficient — no PAT); set up
     Python 3.11; `pip install -e .`; run
     `rsb --config .github/boards.ci.toml --json > board.json` (env
     `GH_TOKEN: ${{ github.token }}` for the `gh pr/issue list` calls
     inside `spawn.py`), and check `rsb`'s own exit code — nonzero fails
     the step and the rest of the job (and thus the whole `build` job)
     is skipped. On success, assemble `_site/` (copy
     `src/rsb/web/*` into `_site/`, write the generated JSON to
     `_site/api/board.json`), then `actions/configure-pages@v5` +
     `actions/upload-pages-artifact@v3` (path `_site`).
   - Job `deploy`: `needs: build`, `environment: { name: github-pages,
     url: ${{ steps.deployment.outputs.page_url }} }`, single step
     `actions/deploy-pages@v4`. Because this job only runs when `build`
     succeeded, a failed generation run never reaches `deploy-pages` at
     all — the last successful publish stays live untouched. This is
     the concrete mechanism satisfying requirement 5.
2. Add `.github/boards.ci.toml` (checked in, no secrets — paths/commands
   only), pointing all three board entries at the single shared
   on-the-record `spawn.py` checkout (issue's background note: one
   `spawn.py` source serves all three boards):
   ```toml
   [[repo]]
   name = "on-the-record"
   path = "_boards/on-the-record"
   command = ["python3", "_boards/on-the-record/spawn.py"]

   [[repo]]
   name = "repo-status-board"
   path = "."
   command = ["python3", "_boards/on-the-record/spawn.py"]

   [[repo]]
   name = "tokenmaxxxer-core"
   path = "_boards/tokenmaxxxer-core"
   command = ["python3", "_boards/on-the-record/spawn.py"]
   ```
3. Fix `src/rsb/web/dashboard.js` line 406:
   `fetch("/api/board.json")` → `fetch("api/board.json")` (relative
   path). This resolves correctly against the current document URL in
   both local `rsb serve` (page served at root, identical behavior,
   zero regression — survey §6) and a GitHub Pages project subpath
   (`https://tokenmaxxxer.github.io/repo-status-board/`). This is the
   entire fix for requirement 2 — `index.html`/`dashboard.css` are
   already relative-path-safe (survey §6).
4. Document in `docs/handbooks/rsb.md`: the one-time manual prerequisite
   (repo admin must set **Settings → Pages → Build and deployment →
   Source: GitHub Actions** once, before `deploy-pages` can succeed —
   the default `GITHUB_TOKEN` lacks repo-admin scope to flip this itself
   and it cannot be scripted from inside the workflow) and a short
   section describing the static-deploy path alongside the existing
   local-serve instructions.

## Out of scope

- Flows fully-remote optimization (going straight from GitHub API calls
  to `flows --json`-equivalent output without an `actions/checkout`
  clone) — the issue explicitly punts this to a separate issue
  ("클론 없이 API만으로 가는 최적화는 별도 이슈").
- Actually flipping the repo's Pages source setting to "GitHub Actions"
  — a one-time manual action for a repo admin, documented as a
  prerequisite but not something this workflow (or any workflow) can
  perform on itself.
- Live-runner empirical confirmation of `runs/`-absence behavior
  (requirement 4) — confirmed at the code level this phase by direct
  source reading (survey §7, exact file:line citations); empirical
  confirmation on a real empty-`runs/` runner happens naturally on the
  workflow's first live run in phase 2, not as a phase-1 blocker.
- Any change to on-the-record's `spawn.py` or `gates/flows.py` — not
  needed; requirement 4 is already satisfied by existing behavior there.

## How you'll know it worked

Mapped directly to the issue's 6 acceptance-criteria checkboxes:

- [ ] The Pages URL shows the merged 3-repo board (Flows/Decision
  queue/Hygiene, plan rendering included) — verified by opening the
  published Pages URL after a successful workflow run.
- [ ] `board.json`'s `generated_at` (and `generated_at_by_repo`)
  timestamp visibly advances on each cron tick — verified by comparing
  two consecutive scheduled runs' published `board.json`.
- [ ] Empty `sessions[]`/`ledger[]` render cleanly via the dashboard's
  existing empty-state handling — verified visually against the Pages
  output, since a runner checkout has no `runs/` (requirement 4's
  premise).
- [ ] Local `rsb serve` has no regression — verified by running the
  existing test suite (`python -m pytest test/`) unchanged and green,
  plus a manual local `rsb serve` smoke check.
- [ ] A deliberately-broken generation step (e.g. a temporarily invalid
  `.github/boards.ci.toml`) is confirmed to leave the previously
  published Pages deployment untouched — verified by triggering
  `workflow_dispatch` against a broken config and checking the live URL
  still serves the prior `board.json`.
- [ ] The PR body for this and all subsequent issue #27 work contains no
  closing-keyword-plus-`#27` pattern, in plain text, quotes, or
  backticks — verified by re-reading the PR body text before submission
  (this proposal PR itself follows this rule).
