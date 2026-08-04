# Conformance-review survey (issue #27)

Subject: PR #28 (`issue-27/implementation`, **open, unmerged** — not on
`main`) checked against issue #27's 6 acceptance-criteria items and a
schema-relevance check against `docs/specs/flows-schema.md`. Scout: ran,
1 sweep, saturated after judging no new practice would change the
requirement list — see `scout-brief.md`.

This is phase 1 of a two-phase role. Everything below is drawn from
reading PR #28's actual diff (`gh pr diff 28`) and this repo's code
directly, not accepted from `docs/issue-27/reports/implementation.md`'s
self-report (read only to orient, per role mandate).

## What PR #28 actually changes (file-by-file, from the diff)

- **`.github/workflows/deploy-board.yml`** (new, 72 lines) — two jobs.
  `build`: `actions/checkout` this repo (root) + `tokenmaxxxer/on-the-record`
  → `_boards/on-the-record` + `tokenmaxxxer/tokenmaxxxer-core` →
  `_boards/tokenmaxxxer-core`; `actions/setup-python@v5` (3.11);
  `pip install -e .`; `rsb --config .github/boards.ci.toml --json >
  board.json` (env `GH_TOKEN`); assembles `_site/` (`cp -r
  src/rsb/web/* _site/`, `cp board.json _site/api/board.json`);
  `actions/configure-pages@v5` + `actions/upload-pages-artifact@v3`
  (path `_site`). `deploy`: `needs: build`, `environment: {name:
  github-pages, url: ...}`, single step `actions/deploy-pages@v4`.
  Triggers: `schedule: [cron: "*/30 * * * *"]` +
  `workflow_dispatch:`. `permissions: {contents: read, pages: write,
  id-token: write}`. `concurrency: {group: pages, cancel-in-progress:
  false}`. No `if:` key appears anywhere in the file — the `deploy`
  job's gating is entirely `needs: build`'s default GitHub semantics
  (a job is skipped if any of its `needs:` jobs did not succeed). Note:
  PR #28's own proposal/report text describes this as "`if:`/`needs:`
  gating" and "a job-level `if:`" in a few places, but the actual YAML
  has no `if:` — a text-vs-artifact wording mismatch worth flagging for
  phase 2 to check the *mechanism* (does `needs:`'s default behavior
  alone satisfy AC5?) rather than trust the prose description.
- **`.github/boards.ci.toml`** (new, 14 lines) — three `[[repo]]`
  blocks (`on-the-record`, `repo-status-board`, `tokenmaxxxer-core`),
  each `command = ["python3", "_boards/on-the-record/spawn.py"]`
  (single shared `spawn.py` checkout), `path` set per board
  (`_boards/on-the-record`, `.`, `_boards/tokenmaxxxer-core`).
- **`docs/handbooks/rsb.md`** (+22 lines) — new "Static deploy (GitHub
  Pages)" section: describes the build/deploy job split, the one-time
  manual **Settings → Pages → Source: GitHub Actions** prerequisite,
  and GitHub's 60-day scheduled-workflow auto-disable/reactivation
  note.
- **`src/rsb/web/dashboard.js`** (1 line changed, line 406) —
  `fetch("/api/board.json")` → `fetch("api/board.json")`. This is the
  entire code change to the dashboard itself. No other line in
  `dashboard.js`, `dashboard.css`, or `index.html` is touched.
- **`docs/issue-27/proposals/implementation.md`**,
  **`docs/issue-27/reports/implementation.md`**,
  **`docs/issue-27/reports/implementation/scout-brief.md`**,
  **`docs/issue-27/reports/implementation/survey.md`** — that role's
  own phase-1/phase-2 records, read for orientation only (per role
  mandate, not treated as verdicts).
- **Not touched at all**: `docs/specs/flows-schema.md`,
  `src/rsb/cli.py`, `src/rsb/fetch.py`, `src/rsb/config.py`,
  `src/rsb/webserver.py`, `src/rsb/render.py`, `src/rsb/model.py`,
  anything under `test/`.

## Schema-relevance check

`docs/specs/flows-schema.md` is **not** in PR #28's diff, and nothing
in the diff changes the JSON payload shape (`board.json`'s fields, or
`flows[].plan`'s contract from issue #23). The workflow generates
`board.json` via the existing `rsb --json` code path
(`render_json_model`, unchanged), and the one dashboard.js line only
changes *where* the client fetches that JSON from, not its shape. So
unlike issue #23 (which required a schema-copy re-sync as AC1), issue
#27 has no schema-document sub-requirement — confirmed by absence in
the diff, not inferred from the issue text. This survey's requirement
list (see `proposals/conformance-review.md`) reflects that: none of
the 6 ACs decompose into a "spec doc matches upstream" sub-fact the
way issue #23's AC1 did.

## Issue #27's 6 acceptance criteria (verbatim source, for the requirement list)

1. [ ] Pages URL에서 3개 레포 병합 보드가 보인다 (Flows/Decision queue/Hygiene, plan 렌더링 포함)
2. [ ] cron 주기마다 board.json이 갱신된다 (as-of 타임스탬프로 확인)
3. [ ] sessions/ledger 빈 상태가 깔끔히 렌더된다 (기존 empty 처리 재사용)
4. [ ] 로컬 `rsb serve` 동작 회귀 없음 (기존 테스트 전부 통과)
5. [ ] 워크플로 실패 시 직전 배포 유지가 확인된다
6. 주의: PR 본문에 closing 키워드 금지 (issue #23 T2 — 백틱 인용도 파싱됨)

Item 6 is not a checkbox in the issue body — it is a process
constraint on how *this issue's own PRs* (including PR #28 and this
review's own upcoming PR) are written, not a feature of the built
artifact. It is still traced below as R6, because it is independently
checkable (PR body text either does or does not contain a
closing-keyword pattern) and this role must obey it for its own PR.

## Observations shaping requirement decomposition (not verdicts)

- **AC1** bundles at least four separable facts: (a) the static-deploy
  mechanism (relative fetch path + `_site/api/board.json` placement)
  actually resolves under a Pages project subpath; (b)
  `boards.ci.toml` actually wires all 3 repos into one merged
  `board.json`, not a subset; (c) the existing Flows/Decision
  queue/Hygiene render functions are reused unmodified (no new/altered
  rendering code in the diff for these sections — a diff fact); (d)
  plan rendering (issue #23's feature) is unbroken by this diff (the
  one changed line is unrelated to `buildPlanSteps`/
  `renderPlanSection`). A fifth fact — actually opening the live Pages
  URL and *seeing* all four render correctly — is the live-runner-only
  half (see below).
- **AC2** bundles: (a) the cron expression itself is syntactically a
  30-minute-interval trigger; (b) each run regenerates `board.json`
  fresh (`_now_iso()` is called anew per `_run_once()` invocation,
  `src/rsb/cli.py:60` — confirmed by direct read, unrelated to PR #28's
  diff since this code path is untouched); (c) the as-of timestamp is
  surfaced in the rendered UI (`dashboard.js:347`,
  `HEADER_META.textContent = \`as of ${data.generated_at} — ...\``,
  unchanged by this diff). A fourth fact — two *real* consecutive cron
  ticks on the deployed workflow actually producing two different
  published timestamps — is live-runner-only.
- **AC3** bundles: (a) whether PR #28's diff *adds* any new
  empty-state handling code (it does not — the diff touches only
  `dashboard.js:406`, nothing in the empty-state render paths
  `sessionRows`/`renderAccounting`/`renderTable`'s `emptyMessage`
  branch/the page-level all-empty guard at `dashboard.js:78-79,371`),
  which is the literal test of "기존 empty 처리 재사용" (reuses
  existing handling — reuse, not new code); (b) whether the
  `runs/`-absent-on-a-fresh-runner code path (on-the-record's
  `spawn.py`/`gates/flows.py`, outside this repo's own write set) is
  even exercised/asserted by anything in this repo rather than merely
  assumed. A third fact — the live Pages output actually *looking*
  clean for a real all-empty case — is live-runner-only.
- **AC4** bundles: (a) `src/rsb/webserver.py` (local-serve's live
  `/api/board.json` handler) is untouched by the diff — confirmed; (b)
  the changed fetch path resolves identically under local `rsb serve`
  (a code-reading fact: root-served page, absolute and relative paths
  are equivalent); (c) the existing test suite passes with PR #28's
  diff applied — independently re-runnable, not just accepted from
  `implementation.md`'s "41 passed" claim; (d) whether the one-line
  client change has any direct test coverage at all (the diff adds no
  test file) — a separate fact from (c) passing, since a suite that
  passes *without regression* is not the same claim as *this specific
  line is covered by a test*.
- **AC5** bundles: (a) the job-graph structure (`deploy` job's
  `needs: build`, no `if:` weakening it, no `continue-on-error:`/`||
  true` in the `build` job's failure-prone step) — directly checkable
  from the YAML text, independent of any run; (b) actually triggering
  a broken-config run against the live workflow and confirming the
  live Pages URL still serves the prior `board.json` — live-runner-only,
  and additionally requires Pages deployment *history* to exist (i.e.
  at least one prior successful deploy), which cannot exist in this
  sandbox at all.
- **AC6** (process constraint, not a feature) splits into: (a) PR #28's
  own current body text, fetchable and checkable directly; (b) this
  review role's own PR body (opened at the end of this phase), which
  this role must also satisfy — a self-applicable constraint, not just
  an inspection target.

## Local-verification-gap flag (mirrors issue-23's AC3 precedent)

PR #28's own body and `docs/issue-27/reports/implementation.md`
explicitly admit: "No live GitHub Actions runner in this environment
— live-runner confirmation (cron tick advance, actual Pages render,
the broken-config fail-safety scenario) happens on this workflow's
first live run after merge and after a repo admin flips Pages source
to 'GitHub Actions'." This environment (this conformance-review
session) has the identical constraint — no live Actions runner, no
live Pages deployment, no admin access to flip the Pages source
setting. Per issue-23's survey precedent (which flagged AC3's
provider-side timing claim the same way, splitting a bundled AC into a
locally-verifiable half and a provider/live-only half rather than
silently passing or silently skipping it), the following are flagged
here as **Unverifiable-within-this-repo candidates** for phase 2 to
formally record, not silently pass:

- AC1's "Pages URL 렌더" half (R1e below) — opening the actual
  deployed page.
- AC2's "cron 주기마다 갱신 확인" half (R2d below) — two real
  consecutive scheduled runs producing two different timestamps.
- AC3's "빈 상태가 깔끔히 렌더된다" visual-confirmation half (R3c
  below) — seeing the live rendered output.
- AC5's "확인된다" (confirmed) clause (R5c below) — triggering a real
  broken-config run against the live workflow and observing the prior
  deployment survive; this one additionally requires pre-existing
  Pages deployment history that cannot exist in this sandbox at all.

Each of these has a locally-verifiable code/config-level counterpart
(the mechanism that is *supposed* to produce the outcome) that phase 2
*can* check by inspection — the distinction being drawn is between
"the mechanism exists and is wired correctly" (locally checkable) and
"the mechanism was observed to actually produce the outcome in
production" (not locally checkable), same split issue-23's survey drew
for its own AC3.

## Constraints on phase 2's verification depth

- No browser, no live GitHub Actions runner, and no live GitHub Pages
  deployment are reachable from this sandbox — matches PR #28's own
  admitted limitation. This bounds AC1/AC2/AC3/AC5's live-observation
  halves (R1e, R2d, R3c, R5c) to Unverifiable-within-this-repo, not to
  a guessed pass or a silent omission.
- What **is** locally verifiable: YAML/TOML structure and syntax
  (readable directly, no runner needed); whether the diff's code
  changes are consistent with the claimed mechanism (job gating,
  relative-path fetch, config wiring); and the existing Python test
  suite, independently re-runnable in this sandbox. This survey did
  re-run it against the current `main` tip (PR #28 not applied, since
  PR #28 is unmerged and this branch does not have its diff on disk):
  `python3 -c "import sys; sys.path.insert(0,'src'); import pytest;
  sys.exit(pytest.main(['test/','-q']))"` → **41 passed**, 0 failed —
  confirms the pre-PR-28 baseline this repo's test count claim is
  measured against; PR #28's diff touches no `test/` file, so phase 2
  will need to check out or apply PR #28's diff to independently
  re-confirm its own "41 passed" claim rather than accept it as-is.
- `.github/` does not exist on `main` (or on this branch) at all prior
  to PR #28 — confirmed (`ls .github` → no such directory). Everything
  in `.github/workflows/deploy-board.yml` and `.github/boards.ci.toml`
  is wholly new surface, not an edit to pre-existing CI config.

## Write-set for this role

This role only reads `src/`, `test/`, `docs/specs/`, and issue #27; it
writes only `docs/issue-27/reports/conformance-review/`,
`docs/issue-27/proposals/conformance-review.md`, and (phase 2, after
approval) `docs/issue-27/reports/conformance-review.md`. No `src/`/
`test/` change is proposed or made by this role.
