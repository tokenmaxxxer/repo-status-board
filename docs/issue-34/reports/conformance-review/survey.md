# issue-34 conformance-review survey (phase 1)

Subject: PR #35 (`issue-34/implementation`, merged to `main` at commit
`5d05b5f`). Note on the merge itself: despite the PR/merge-commit title
reading "issue-34 **phase 1**: owner/name propagation + GitHub link
proposal", the merged diff (`gh pr view 35 --json files,body`) contains
not just the proposal/survey/scout-brief/decision docs but also the
actual `src/`/`test/` changes and a phase-2
`docs/issue-34/reports/implementation.md` record with `loop_state:
landed`. This survey treats the state on `main` — i.e. the fully
implemented code — as the subject to check, not just a proposal; the
title wording is recorded here as a fact, not judged.

Scout: not run — see "Scout-skip" below.

## 1. Target-artifact identification — issue #34's 5 numbered requirements

**Req 1 (owner/name 관통 — owner/name threaded from payload to
`/api/board.json`):**
- `src/rsb/model.py:110` — `BoardModel.owner_name_by_repo: dict` field
  (parallel to the pre-existing `generated_at_by_repo:109`).
- `src/rsb/model.py:266-271` — `normalize_payload()` reads
  `payload.get("repo")` into local `owner_name`, returns it as
  `"owner_name"` in the normalized dict.
- `src/rsb/model.py:293-294` — `merge_repos()` populates
  `model.owner_name_by_repo[repo_name] = normalized["owner_name"]`
  immediately next to the existing `generated_at_by_repo` population.
- `src/rsb/render.py:174` — `render_json_model()` adds
  `"owner_name_by_repo": model.owner_name_by_repo` to its output dict
  (the same function serializes both `/api/board.json`
  (`src/rsb/webserver.py`, unmodified per PR #35's file list) and the
  static Pages `rsb --json` output consumed by
  `.github/workflows/deploy-board.yml:47`).
- Short config name stays the record/filter/join key: no change to any
  of the 8 record dataclasses (`Decision`, `Flow`, `Session`,
  `LedgerEntry`, `Unattributed`, `HygieneClosureViolation`,
  `HygieneUnapprovedPr`, `RepoError`, all in `model.py:12-102`) — each
  still stamps `repo=repo_name` (the config short name), unchanged from
  before PR #35.
- Decision doc: `docs/issue-34/decisions/owner-name-wire-format.md`
  records this as an additive `board.json` wire-format change.

**Req 2 (이슈 링크 — issue-number links, link placement distinct from the
existing `row-toggle` disclosure button):**
- `src/rsb/web/dashboard.js:211-213` — `buildGithubUrl(ownerName, kind,
  number)`, `kind="issues"` case.
- `src/rsb/web/dashboard.js:219-223` — `externalLinkHtml(...)`, returns
  `""` when `buildGithubUrl` returns `null`, else an `<a
  class="external-link" ...>` with an `aria-hidden="true"` glyph.
- `src/rsb/web/dashboard.js:225-229` — `issueToggleCell(sourceTable,
  issue, repo, ownerName)` gained a 4th parameter; the existing `<button
  class="row-toggle" ...>` markup is unchanged, with
  `externalLinkHtml(ownerName, "issues", issue, ...)` appended
  immediately after the button's closing tag (not wrapping/nesting it).
- Four call sites (all four tables) pass their own `ownerNameByRepo[...]`
  lookup into `issueToggleCell`: `decisionRows` (`dashboard.js:249`),
  `flowRows` (`dashboard.js:283`), `sessionRows` (`dashboard.js:299`),
  `renderAccounting` (`dashboard.js:316`).
- `src/rsb/web/dashboard.css:173-188` — `.external-link` rule block
  (margin/color/hover/focus/`:focus-visible` outline), comment states
  "separate sibling control ... never overlapping it".

**Req 3 (PR 링크 — decision-queue PR number, Flows PRs column):**
- `src/rsb/web/dashboard.js:231-239` — `prCellHtml(ownerName,
  prNumbers)`: `"-"` on empty/falsy, else each number wrapped in
  `<span class="mono">` + `externalLinkHtml(ownerName, "pull", ...)`,
  joined `", "`.
- `src/rsb/web/dashboard.js:250` — `decisionRows` calls
  `prCellHtml(ownerNameByRepo[d.repo], [d.pr])` (single PR wrapped in a
  1-element array).
- `src/rsb/web/dashboard.js:287` — `flowRows` calls
  `prCellHtml(ownerNameByRepo[f.repo], f.prs)` (`f.prs` already an
  array).
- `src/rsb/web/dashboard.js:211-213` — `buildGithubUrl(..., "pull",
  ...)` is the same helper as the issue-link case, `kind` parameterized.

**Req 4 (접근성 — real `<a href>`, new-tab decision documented, keyboard
order not colliding with `row-toggle`):**
- `src/rsb/web/dashboard.js:222` — emitted anchor is a real
  `<a href="...">` (not a `javascript:`/`onclick` pseudo-link),
  `target="_blank" rel="noopener noreferrer"` (new-tab choice is present
  in the code but is not written down anywhere as a documented decision
  — see AC evidence table below, R4).
- `src/rsb/web/dashboard.js:228` (`issueToggleCell`) — link markup
  appended strictly after `</button>` in source order, so in DOM/tab
  order the `row-toggle` button and the `external-link` anchor are two
  separate, sequential focusable elements, never nested/overlapping.
- `docs/specs/screen-spec.md:54-57,74-75` (§1.3, §1.4) documents the
  `row-toggle` button pattern but has **not** been updated to mention
  `.external-link` or the new tab-order relationship — the only written
  description of the two controls' relationship is the code comment at
  `dashboard.js:204-210,216-218`, not a spec doc.

**Req 5 (owner/name 부재 시 텍스트로만 표시, 깨진 링크 금지):**
- `src/rsb/web/dashboard.js:211-212` — `buildGithubUrl` returns `null`
  when `ownerName` is falsy or not a string.
- `src/rsb/web/dashboard.js:221` — `externalLinkHtml` returns `""` (no
  anchor at all) when `buildGithubUrl` returns `null` — the issue number/
  PR number itself still renders as plain text via the unchanged
  `${issue}`/`${prNumber}` interpolation in `issueToggleCell`/
  `prCellHtml`, so the cell falls back to text-only, not a broken
  `href="undefined"` or similar.
- `src/rsb/model.py:266-271` — Python side stores `None` (no validation)
  when `payload.get("repo")` is absent; no exception path exists for a
  missing/malformed `repo` field.

## 2. Evidence-location map for the 7 acceptance-criteria checkboxes

Verbatim checkboxes, in the issue's own order:

**AC1 — "board.json 의 각 레코드에서 owner/name 을 얻을 수 있다"**
(owner/name is obtainable from each record in board.json).
- `src/rsb/model.py:110,266-271,293-294`; `src/rsb/render.py:174`;
  `docs/issue-34/decisions/owner-name-wire-format.md` (states the
  mechanism: a per-repo lookup map keyed by short name, not a field
  embedded directly on each of the 8 record dataclasses — a record
  obtains owner/name indirectly by looking its own `.repo` up in
  `owner_name_by_repo`, mirroring `generated_at_by_repo`).
- Test evidence: `test/rsb_tests/test_model.py:89-107` (3 tests:
  `normalize_payload` returns `owner_name` present/absent,
  `merge_repos` fills `owner_name_by_repo`); `test/rsb_tests/
  test_render.py:50-54` (`render_json_model` output includes the key);
  `test/rsb_tests/test_webserver.py:41` (`/api/board.json` response spot
  check).
- Not locally checkable: whether the **live** deployed
  `https://tokenmaxxxer.github.io/repo-status-board/api/board.json`
  actually carries non-null `owner_name_by_repo` values for its 3
  configured repos (`.github/boards.ci.toml:1-14`: `on-the-record`,
  `repo-status-board`, `tokenmaxxxer-core`) depends on whether each
  repo's `flows --json` payload (produced by `spawn.py`, which lives in
  the `on-the-record` checkout per `.github/workflows/deploy-board.yml:
  24-34`, outside this repo) actually sets a top-level `repo` key —
  no fixture/test in this repo exercises that live path end to end.

**AC2 — "이슈 번호에서 GitHub 이슈로 이동한다 (3개 레포 모두)"**
(issue number navigates to the GitHub issue, all 3 repos).
- `src/rsb/web/dashboard.js:211-213,219-223,225-229` (link-building
  logic, generic across any `ownerName` string — no per-repo
  branching).
- No committed automated test exercises `issueToggleCell`,
  `decisionRows`, `flowRows`, `sessionRows`, or `renderAccounting`
  directly: `module.exports` (`dashboard.js:568`) only exposes
  `buildGithubUrl`/`externalLinkHtml` (plus the pre-existing
  `ageBucket`/`ageBucketStatus`/`selectSummary`/`isPageEmpty`/
  `buildPlanSteps`/`filterByRepo`) for `node -e`/subprocess coverage
  (`test/rsb_tests/test_render.py:155-178` is the harness pattern used
  for other exported functions); no `test/rsb_tests/test_*.py` file
  calls `buildGithubUrl` or `externalLinkHtml` via that harness the way
  `test_render.py:182-296` does for `buildPlanSteps`/`filterByRepo`. The
  only recorded exercise of `buildGithubUrl`/`externalLinkHtml` is the
  manual `node -e` transcript in
  `docs/issue-34/reports/implementation.md:124-135` (a self-report, not
  a committed/re-runnable test).
- "3개 레포 모두" (all 3 repos): no per-repo distinction exists in code
  to check per-repo — this reduces to whether all 3 repos' records
  carry a non-null `owner_name` (AC1's evidence) and whether a browser
  actually navigates correctly, which is a live/manual check (no
  browser available locally; see `docs/issue-34/reports/
  implementation.md:137-171`, "What did not work" / "Open findings",
  which records the same limitation for this same PR's own author-side
  verification).

**AC3 — "PR 번호(decision queue, flows PRs 열)에서 GitHub PR 로 이동한다"**
(PR number navigates to the GitHub PR, decision-queue + Flows PRs
column).
- `src/rsb/web/dashboard.js:231-239` (`prCellHtml`), call sites at
  `dashboard.js:250` (`decisionRows`) and `dashboard.js:287`
  (`flowRows`).
- Same test-coverage gap as AC2: no committed test calls `prCellHtml`
  directly; only the implementation record's manual `node -e` transcript
  covers the lower-level `buildGithubUrl`/`externalLinkHtml` it's built
  from, not `prCellHtml` itself.

**AC4 — "상세 패널을 여는 기존 동작이 회귀하지 않는다 (클릭·키보드 모두)"**
(the existing detail-panel-opening behavior does not regress, both click
and keyboard).
- `src/rsb/web/dashboard.js:225-229` (`issueToggleCell`'s `<button
  class="row-toggle" ...>` markup is byte-for-byte the pre-existing
  button markup, per a diff against the pre-PR-#35 version implied by
  `docs/issue-34/reports/implementation/survey.md` §4's description of
  the button before this change) with the new anchor appended only as
  trailing sibling markup.
- `src/rsb/web/dashboard.js:458-465` (`attachRowClickHandlers`) and
  `:190-202` (`rowToggleId`/`isRowExpanded`) are unmodified by this PR
  per PR #35's file list (only `dashboard.js` and `dashboard.css` under
  `src/rsb/web/` were touched, and the diff stat for `dashboard.js` is
  `+54/-17` lines — consistent with an additive change plus signature
  edits to `issueToggleCell`/`decisionRows`/`flowRows`/`sessionRows`/
  `renderAccounting`, not a rewrite of the click-handler/toggle-state
  functions).
- No committed test (Python or `node -e`) asserts on click or keyboard
  behavior/tab order for either the pre-existing `row-toggle` or the new
  `external-link`; `docs/issue-34/reports/implementation.md:152-171`
  ("Open findings") records that no real browser was available to this
  session to check keyboard tab order in practice, and recommends a
  follow-up manual check.

**AC5 — "owner/name 없는 레코드가 깨진 링크를 만들지 않는다"**
(a record without owner/name does not produce a broken link).
- `src/rsb/web/dashboard.js:211-212,221` (falsy/non-string guard in
  `buildGithubUrl`; `""` short-circuit in `externalLinkHtml`).
- `test/rsb_tests/fixtures.py:190` — `MISSING_OWNER_NAME_PAYLOAD` (a
  copy of `EMPTY_PAYLOAD` with the `repo` key removed).
- `test/rsb_tests/test_model.py:94-107` — asserts `owner_name is None`
  and `owner_name_by_repo` maps that repo to `None` when `repo` is
  absent from the payload.
- No committed JS-side test exercises `externalLinkHtml(null, ...)` or
  `buildGithubUrl(null, ...)` returning `null`/`""` (same gap noted under
  AC2/AC3) — only the manual `node -e` transcript in
  `docs/issue-34/reports/implementation.md:124-135` shows
  `externalLinkHtml(null,'issues',5,...) -> ""`.
- `docs/issue-34/reports/implementation.md:92-113` ("PR #35 feedback
  resolution") records a judgment call about `""` vs. a width-reserving
  empty `<span>` when the link is omitted — relevant context for
  whether "no broken link" also holds for layout, not just markup
  validity.

**AC6 — "기존 테스트 전부 통과"** (all existing tests pass).
- Full suite location: `test/` (four files touched by PR #35:
  `test_model.py`, `test_render.py`, `test_webserver.py`,
  `fixtures.py`).
- Documented invocation (used by this and prior conformance-adjacent
  reviews in this repo, e.g. `docs/issue-23/reports/conformance-review/
  survey.md:31-37`): `python3 -c "import sys; sys.path.insert(0, 'src');
  import pytest; sys.exit(pytest.main(['test/', '-q']))"` — bare
  `pytest test/ -q` is documented elsewhere in this repo to fail
  collection (`ModuleNotFoundError: rsb`) without the `sys.path` prefix.
- Self-reported count: `docs/issue-34/reports/implementation.md:115-122`
  claims "53 passed, 0 failed, 0 skipped" (33 pre-existing + 20 new).
  This survey does not re-run the suite (see "Scout-skip" below on this
  phase's scope) — the actual pass/fail state on `main` is left for
  phase 2 to (re-)run and verify directly, not accepted from the
  self-report.

**AC7 — "주의: PR 본문에 closing 키워드 금지 (issue #23 T2 — 백틱 인용도
파싱됨)"** (caution: no closing keywords in the PR body — issue #23 T2,
backtick-quoted ones are parsed too).
- This is a constraint on how PR #35's *own PR body* was written, not on
  the shipped code. Evidence location: PR #35's body text itself
  (`gh pr view 35 --json body`) — this survey observed no
  `Closes`/`Fixes`/`Resolves #34` (plain or backtick-quoted) in the PR
  #35 body text as fetched; `docs/issue-34/reports/implementation.md:
  207-210` ("pr-body-no-closing-keywords") self-reports the same check.
  Phase 2's evidence pointer for this AC is the PR body text on GitHub,
  not a file in this repo.

## 3. Scout-skip

Per the scout-directive, scouting was skipped for this review: issue
#34's spec text already lists all 7 acceptance criteria as explicit
checkboxes with no open design decision in *what* to check — there is
no ambiguous-scope judgment call for a scout sweep to resolve here (that
kind of judgment call belonged to the *implementation* role's own scout,
already spent in `docs/issue-34/reports/implementation/scout-brief.md`).

## 4. Judgment calls made while writing this survey

- Treated PR #35's merged content (including its own phase-2
  `implementation.md` record and the actual `src/`/`test/` diff) as the
  subject under review, despite the PR/merge-commit title saying "phase
  1" — the merge commit is what's actually on `main`, and this role's
  mandate is to check `main`'s current state (see task framing), not the
  title string.
- AC7 is treated as a distinct, separately-evidenced checkbox (pointing
  at the PR body on GitHub) rather than folded into AC6 or dropped as
  "not code" — the task's own framing counts 7 acceptance-criteria
  checkboxes, and the issue body itself lists it as the 7th `- [ ]` item.
