# Execution observation record — issue #29

loop_state: landed

Scope: this record renders the three-level verdict this role's contract
requires, on the two merged PRs that delivered issue #29's implementation
step — PR #30 (`issue-29/implementation` → `main`, commits `cc3466a1`
docs-only phase 1 + `05d632f5` phase 2, merged `b630292`) and PR #33
(`issue-29/implementation` → `main`, commit `d462b6d0`, merged `c94e12d9`)
— against issue #29's own 7 acceptance-criteria checkboxes and the method
frozen in `docs/issue-29/proposals/execution-observation.md`. Phase 2
opened via the issue-level comment whose entire body is the exact string
`APPROVE issue-29/execution-observation`, posted by `jjongkwann` (an
`docs/specs/approvers.md` account) at 2026-08-03T11:53:58Z
(https://github.com/tokenmaxxxer/repo-status-board/issues/29#issuecomment-5165967281)
— single-account mode, since this branch's own PR #42 is also authored by
`jjongkwann`.

## Independence statement

This role did not author or edit PR #30, PR #33, `src/rsb/fetch.py`,
`src/rsb/cli.py`, `src/rsb/web/dashboard.js`, `src/rsb/web/index.html`,
`src/rsb/web/dashboard.css`, `test/rsb_tests/*`, or
`docs/issue-29/reports/implementation.md` this session or any prior one.
Every finding below rests on reading those artifacts as they stand
(`git show <sha>:<path>` for merge-time state, `git show origin/main:<path>`
for current state, `gh pr view`/`gh issue view` for GitHub-side metadata),
never on re-running `pytest`, `node`, or `rsb serve`, and never on this
role's own prior survey/proposal prose taken as already-established fact.
No verdict below precedes this statement.

## What was done

This session executed the method frozen in
`docs/issue-29/proposals/execution-observation.md` §1: real-call-site and
real-state-transition tracing (not re-execution) against `git show
<sha>:<path>` for PR #30/#33's merge-time state and `git show
origin/main:<path>` for current state, for every function the
implementation record claims is wired up (`filterByRepo`, `repoList`,
`updateRepoFilterOptions`, `attachRowClickHandlers`/`attachRowToggleHandlers`,
`isRowExpanded`, `rowToggleId`); independent re-verification of both issue
comments' specific `dashboard.js` line citations against the actual code
at the commit they describe; a fresh check of `PARTIAL_BANNER.innerHTML`
against AC5 (the gap `implementation.md` self-disclosed but neither issue
comment mentions); a hand trace of `fetch.py`'s `ThreadPoolExecutor`
construction and `cli.py`'s `--timeout` flag threading for the backend
ACs; a verbatim re-read of both PR bodies for AC7's closing-keyword rule;
and a `git show --stat`/timestamp ordering check across `cc3466a1`,
`05d632f5`, and `d462b6d0` plus the issue's own comment timestamps for the
trajectory verdict. No `pytest`/`node`/`rsb serve` was run, per this
role's re-execution prohibition. Results are recorded in §1-§3 below.

## 0. Verdict-level applicability

All three levels required by this role's contract apply to this subject;
none is N/A. Outcome and step both apply because PR #30/#33 shipped code
changes checkable against issue #29's ACs. Trajectory applies because two
separate PRs, an inherited crashed-session working tree, and a PR without
its own approval token are all present and checkable.

## 1. Outcome verdict — did PR #30/#33 land what issue #29 asked

Per-AC table, each row scoped first to what PR #30/#33 *themselves*
shipped, with current-`main` state noted separately and attributed where a
different issue's PR changed it.

| AC | Requirement | Verdict at PR #30/#33 merge | Current `main` | Citation |
|---|---|---|---|---|
| 1 | 3-repo parallel fetch, no truncation on the slowest repo (26.7s measured) | **Met.** `fetch_board()` uses `concurrent.futures.ThreadPoolExecutor(max_workers=min(len(repo_configs), 8) or 1)` via `.map()`; `DEFAULT_TIMEOUT_SECONDS` raised from the issue's own cited 15s hard-code to `60` (2.25x the measured 26.7s worst case), with a `--timeout` CLI override threaded through `_run_once()`/`serve`. | Unchanged since PR #30. | `src/rsb/fetch.py:14,69,82-86` and `src/rsb/cli.py:35-40,66-67,93-95,109` at `05d632f5` (identical at `origin/main`, confirmed by re-diffing both) |
| 2 | One failing repo doesn't block the others | **Met.** `fetch_and_normalize_one()` never raises — it catches `RuntimeError`/`json.JSONDecodeError`/`PayloadError` per repo and returns `(repo_name, None, error_message)`, so `ThreadPoolExecutor.map()` collects one tuple per repo regardless of individual failure. | Unchanged. | `src/rsb/fetch.py:45-66` at `origin/main` |
| 3 | `All repos` ↔ individual repo recomputes table + chips | **Unmet at PR #30 merge, met only after PR #33.** PR #30 shipped `filterByRepo()`/`repoList()` as pure, tested, but zero-call-site functions — `<select id="repo-filter">` existed with no `change` listener and no code populating its `<option>`s, exactly as issue comment 2 reported after live-deployment verification (2026-08-03T07:15:26Z, https://github.com/tokenmaxxxer/repo-status-board/issues/29#issuecomment-5163403356) and as `implementation.md`'s own "Open findings" #1 had already self-disclosed before that comment was posted. PR #33 (`d462b6d0`) added `updateRepoFilterOptions()`, wrote `load()`'s fetched payload to module-scope `boardData`, and added a `change` listener calling `renderData(filterByRepo(boardData, REPO_FILTER.value))`. | Met. | Unmet-state: `docs/issue-29/reports/implementation.md:176-184` ("Open findings" #1). Fix: `src/rsb/web/dashboard.js:465-474,573-574,586-588` at `origin/main` (== `d462b6d0`'s diff, `+24/-1` per `git show --stat d462b6d0`) |
| 4 | `Repo` first column on all tables; per-table horizontal scroll, no page-body scroll | **Met, by PR #30 itself.** At `05d632f5`, `renderTable()`'s Flows/Sessions header arrays were reordered to `["Repo", ...]` to match `flowRows()`/`sessionRows()`'s already-Repo-first `cells:` arrays (Decisions/Ledger were already correct); `.table-scroll { overflow-x: auto }` wraps every table. | Unchanged (headers still `["Repo", ...]` for all four tables). | `git show 05d632f5:src/rsb/web/dashboard.js` renderTable calls (decisions/flows/sessions all `["Repo", ...]`); confirmed unchanged at `origin/main:src/rsb/web/dashboard.js:539,543,547` |
| 5 | `N of M repos failed` banner, per-repo detail collapsed | **Unmet — still unmet on current `main`, unreported by either issue comment.** `PARTIAL_BANNER.innerHTML` renders one always-visible line with every `{repo}: {message}` pair comma-joined; no `<details>/<summary>` collapse exists anywhere in the file. This is `implementation.md`'s self-disclosed "Open findings" #4, which neither issue comment (2 or 3) mentions — this role's own proposal (gap 2) flagged this as needing independent verification rather than relying on the two comments' coverage as exhaustive; that verification now confirms the gap is real and still open. | Unmet. | `docs/issue-29/reports/implementation.md:204-216` ("Open findings" #4); confirmed live at `src/rsb/web/dashboard.js:511-524` at `origin/main` (no `<details>` anywhere in file, confirmed by full-file grep) |
| 6 | Keyboard-only row-detail open | **Substantially unmet at PR #30/#33 merge — fixed later by a different issue's PR, not by PR #30/#33.** At `05d632f5`, `attachRowClickHandlers()` binds `click` only to `tbody tr[data-issue]`; the row-toggle `<button>` itself has no listener. Tracing `rowToggleId(sourceTable, repo, issue)` → `` `detail-row-${sourceTable}-${safeRepo}-${issue}` `` used as `aria-controls`: no element with that id pattern exists anywhere in `index.html` or any rendered output (only `DETAIL_SLOT`'s fixed `id="detail-panel-slot"` exists) — `aria-controls` points at a real DOM id that is never created, confirming issue comment 3's claim independently. Tracing `selectedIssue` assignment in the same `attachRowClickHandlers()` (`{ issue, repo }`, no `sourceTable`) through to `isRowExpanded()`'s `selectedIssue.sourceTable === sourceTable` check: `sourceTable` is always `undefined`, so the comparison is always false — `aria-expanded` is permanently `"false"` regardless of actual panel state, confirming issue comment 3's second claim independently. Note: because the `<button>` is a DOM descendant of the `<tr>` and native `click` events bubble, a keyboard Enter/Space on the focused button *would* still fire the row's click listener and open the panel — so the panel is likely still keyboard-*operable* in practice, but the ARIA state a screen-reader user receives while operating it is wrong (permanently "collapsed", pointing at a nonexistent target), which is exactly the WAI-ARIA-disclosure-pattern defect requirement 5 was written to eliminate. | Met (via a different issue's PR). Current `attachRowToggleHandlers()` binds directly to `.row-toggle` buttons, `selectedIssue` includes `sourceTable`, `aria-controls="detail-panel-slot"` (a real, existing id). | Unmet-state citations: `git show 05d632f5:src/rsb/web/dashboard.js:190-193` (`rowToggleId`), `:195-201` (`isRowExpanded`), `:411-414` (`attachRowClickHandlers`). Fix, attributed to issue #36/PR #37, **not** PR #30/#33: `origin/main:src/rsb/web/dashboard.js:474-487`, landed in commit `b621082` ("issue-36 phase 1: link-as-text proposal + row-toggle relocation (#37)", 2026-08-03T20:30:29+09:00), whose own commit message states the fix was folded in "per the approved proposal's rationale" for issue #36's unrelated icon-relocation feature, not as an issue-29 delivery |
| — (requirement 5, narrow-screen inline expansion — not its own AC checkbox, folded into AC6 by the issue body) | Detail expands inline below the row on narrow screens instead of `DETAIL_SLOT` | **Unmet, still unmet on current `main`, and explicitly out of scope for issue #36's fix too.** Neither `matchMedia()` nor `insertDetailRow()` exist anywhere in the file at any point checked (`05d632f5`, `d462b6d0`, or current `origin/main`) — only two code comments reference `insertDetailRow()` by name. `DETAIL_SLOT` renders unconditionally regardless of viewport width. | Unmet. | `origin/main:src/rsb/web/dashboard.js:10-19` (comment: "no insertDetailRow() exists... remains unimplemented, issue-36 survey §2 — out of scope for this change"); full-file grep for `insertDetailRow`/`matchMedia` returns only that comment, no definition or call site, at all three points checked |
| 7 | No GitHub closing keyword in either PR body (issue #23 T2 — backtick-quoted still parses) | **Met, both PRs, re-checked verbatim this session.** PR #30 body's literal final line: "This PR references #29 for context only; it does not close it." — no `close(s/d)`, `fix(es/ed)`, or `resolve(s/d)` token anywhere in the body. PR #33 body contains a single bare `#29` line with no keyword prefix, and its other 3 references to "#29" are all inside the phrase "issue #29's" (prose, not a bare closing reference). Neither body contains a backtick-quoted keyword either. | Unchanged (bodies are immutable history). | `gh pr view 30 --json body` and `gh pr view 33 --json body`, both read verbatim this session |

**Outcome summary:** issue #29's 5 requirement areas map to the 7 ACs
above. Requirement 1 (AC1) and requirement 2 (AC2, implicit in the issue
body's "지금처럼" framing) are fully and correctly delivered by PR #30
alone. Requirement 2/AC3 (repo filter) was delivered non-functionally by
PR #30 and only completed by PR #33 — outcome for the pair is met, but
PR #30 in isolation shipped a requirement described in the issue as "이
이슈의 핵심" (the primary point of the issue) in a non-working state.
Requirement 3/AC4 (Repo-first columns + scroll) is fully met by PR #30.
Requirement 4/AC5 (failure banner collapse) is **unmet, on current `main`,
by anyone** — this is a real outstanding gap, not just a PR #30/#33-scoped
one. Requirement 5/AC6 (button-based keyboard-accessible row detail) was
substantially unmet by PR #30/#33 at merge time and was fixed by a
different issue's PR (#37/issue-36) as a side effect of unrelated work,
with the narrow-screen inline-expansion half of requirement 5 still unmet
by anyone. AC7 (process rule) is met by both PRs.

## 2. Trajectory verdict — was the implementation role's phase-1→phase-2 path sound, across both PRs

**PR #30's own phase-1→phase-2 ordering: sound.** `cc3466a1` (phase 1)
touched only `docs/issue-29/proposals/implementation.md`,
`docs/issue-29/reports/implementation/{survey,scout-brief}.md` — 3 files,
0 `src/`/`test/` changes (`git show --stat cc3466a1`, read this session).
Its timestamp, `2026-08-03T15:00:25+09:00` (`= 2026-08-03T06:00:25Z`),
precedes the `APPROVE issue-29/implementation` issue comment at
`2026-08-03T06:12:32Z`
(https://github.com/tokenmaxxxer/repo-status-board/issues/29#issuecomment-5162934064),
which precedes `05d632f5`'s (phase 2) timestamp
`2026-08-03T15:59:37+09:00` (`= 2026-08-03T06:59:37Z`) — survey/scout/
proposal, then real human approval, then build, in that order. A scout
pass did run (`docs/issue-29/reports/implementation/scout-brief.md`
exists in `cc3466a1`'s file list).

**The `max_workers` cap was a legitimate PR-review-shaped feedback item,
correctly folded in before build, not an approval token.** PR #30 carries
one comment, at `2026-08-03T06:12:33Z`
(https://github.com/tokenmaxxxer/repo-status-board/pull/30#issuecomment-5162934223),
one second after the issue-level approval — requiring the `min(...,8)`
cap. `implementation.md`'s "Rationale for deviations" section documents
this was the only intentional deviation from the approved proposal text,
and `05d632f5`'s `fetch.py:82` shows the capped form actually shipped —
the feedback was read and applied, not silently dropped.

**Crash-recovery correlates with every specific defect found, across both
PRs.** `implementation.md` discloses the frontend build unit (`index.html`
/`dashboard.js`/`dashboard.css`) "had already landed in the working tree
from a prior session that crashed before committing," and this session's
phase-2 build "picked that tree up" rather than writing it fresh
(`docs/issue-29/reports/implementation.md:21-27`). Both issue comments
independently note their findings overlap the same crash window (comment
2: "세션이 두 차례 비정상 종료된 구간과 겹침"). Every specific frontend
defect this record traces — the AC3 non-wiring, the AC6 ARIA-state bugs,
and the AC5 banner-collapse gap — originates in that one inherited,
uncommitted build unit, not in fresh work written during either PR #30's
or PR #33's own phase-2 session (`implementation.md`'s "What did not
work" section fixes only 2 defects — the header/cell mismatch and the
missing `module.exports` entry — both also in that same inherited unit).
This is a real trajectory signal: picking up uncommitted, never-reviewed
code from a crashed session and shipping it with only a partial defect
sweep (2 of 6 total defects in that unit caught before commit) is a
weaker phase-2 practice than building fresh against a reviewed proposal,
even though the two rationale/deviation-tracking sections themselves
(rare in quality) are sound.

**PR #33's authorization path is a genuine gap against a literal reading
of the approval-gate text, though not against this repo's own mechanical
definition of "approved."** PR #33 carries zero comments and zero reviews
(`gh pr view 33 --json comments,reviews`, read this session) — no PR
review Approve, and no fresh `APPROVE issue-29/implementation` comment
posted after PR #33 opened. It proceeds on the original phase-1 approval
(`2026-08-03T06:12:32Z`) plus `implementation.md`'s own prior-session
self-recommendation ("fast-follow on this same approved proposal, not a
new proposal round"). Read literally, this role's contract text —
"Phase 2 opens ONLY when a human approver... submits a PR review Approve;
then do your actual work on the same branch, reported through the same
PR" — describes one phase-1-PR → phase-2-work → same-PR cycle; PR #33 is
a *different* PR object from PR #30 (PR #30 was already merged and
closed), so "the same PR" no longer literally applies, and no fresh
approval event exists for this second PR. Read against this repo's own
codified operational definition instead
(`docs/specs/flows-schema.md:198`'s `unapproved_open_prs`: an open PR
lacks approval only if there is "neither a matching `APPROVE
issue-<n>/<role>` comment... nor a PR review Approve" — scoped to the
comment's exact string, not to a specific PR number), the original
`APPROVE issue-29/implementation` comment *does* mechanically satisfy
that check for PR #33 too, since the string names the role, not a PR.
This record does not treat this as an outcome-affecting deficiency — the
fast-follow diff was small, scoped to an already-approved, already
self-disclosed open item, and its own jsdom verification (`implementation
.md`'s "Fast-follow" section) was substantive — but it is a real
trajectory finding: no human ever looked at PR #33's specific 24-line
diff before it merged, and that is a materially weaker check than what
PR #30 received (a live PR-review-shaped comment). This finding is not
given the four-part deficiency shape below because it produced no
incorrect outcome and is arguably contract-compliant by the repo's own
mechanical definition — it is recorded as a trajectory observation, not a
step deficiency.

**Conformance-review's parallel step-2 pass is out of this record's
scope**, per this role's proposal §3 — noted only because issue #29's own
"실행 계획" names both roles running in parallel (`gh issue view 29`,
read this session), and both step-2 roles' approval comments landed one
second apart (`conformance-review` at `11:53:57Z`, this role at
`11:53:58Z`).

## 3. Step verdict — which specific artifact, if any, is deficient

Two deficiencies survive independent re-tracing (both already named in
§1's outcome table, restated here in blameless four-part shape); one
already-reported defect-set is confirmed accurate against the code, not
just taken on the issue comments' word; one item is confirmed already
fixed and correctly out of this role's write surface.

**Deficiency 1 — partial-failure banner never got its `<details>`/
`<summary>` collapse (AC5).**
- *Impact*: users see one long, always-visible comma-joined line of every
  failed repo's raw error message on any partial failure, instead of the
  issue's specified `N of M repos failed` summary + collapsed detail —
  the exact UX regression risk the issue's own background section was
  written to prevent at scale. Still true on current `main`; no PR or
  issue comment currently tracks it as open.
- *Timeline*: present in the frontend build unit from the crashed prior
  session, self-disclosed in `implementation.md`'s "Open findings" #4
  before PR #30 merged (`05d632f5`, 2026-08-03T06:59:37Z), never
  mentioned in either subsequent issue comment (07:15:26Z, 11:05:52Z),
  never touched by PR #33 or by issue #36/PR #37.
- *Root cause*: the frontend build unit inherited from the crashed
  session implemented the banner's summary line but not its collapse
  wrapper; the phase-2 session that picked up that tree fixed 2 of the
  unit's defects but did not implement this one, and no later pass
  (issue comment review, PR #33, or issue #36) happened to touch this
  specific piece of markup since none of them were looking at the
  banner.
- *Action item*: hand-off only, per this role's prohibition on editing
  `src/`/`test/` — a human should open a follow-up PR against
  `issue-29/implementation`'s branch lineage (or a new fast-follow)
  implementing the `<details>/<summary>` wrap `implementation.md`'s own
  "Open findings" #4 already specifies.

**Deficiency 2 — narrow-screen inline row-detail expansion never
implemented (requirement 5's second half).**
- *Impact*: on narrow viewports, the detail panel always renders into the
  same `DETAIL_SLOT` regardless of width, rather than expanding inline
  below the triggering row as the issue's requirement 5 and
  `screen-spec.md` §1.6 specify — a real gap on the exact device class
  (narrow screens) requirement 5 was written for.
- *Timeline*: `matchMedia`/`insertDetailRow()` never existed at `05d632f5`,
  `d462b6d0`, or current `origin/main` — confirmed absent at all three
  points this session.
- *Root cause*: `implementation.md`'s own "Open findings" #2 explicitly
  deferred this as "outside this session's explicitly bounded task,"
  and issue #36/PR #37's survey explicitly named it out of scope for that
  issue's own unrelated fix (`origin/main:src/rsb/web/dashboard.js:16-18`'s
  comment cites "issue-36 survey §2 — out of scope for this change").
  Nobody has picked it up since.
- *Action item*: hand-off only — a human should scope a follow-up
  (new issue or fast-follow) implementing `insertDetailRow()` and the
  `matchMedia(WIDE_LAYOUT_QUERY)` branch already stubbed by the constant
  and comment at `origin/main:src/rsb/web/dashboard.js:16-19`.

**Already-reported defect-set, independently re-verified (not a new
finding — issue comment 3's citations checked out, with corrected line
numbers):** the `dashboard.js:458-465`/`:461` citations in issue comment 3
(https://github.com/tokenmaxxxer/repo-status-board/issues/29#issuecomment-5165528677)
describe real bugs; this session's own line numbers against `05d632f5`
differ slightly (`:190-193`, `:195-201`, `:411-414`) because of file-length
drift between when the comment was written (against a possibly
locally-edited pre-commit view) and the merged commit — the underlying
logic (dangling `aria-controls` id, permanently-false `aria-expanded`,
row-level rather than button-level click binding) is identical to what
this record traced independently in §1's AC6 row. Already fixed on
current `main`, correctly attributed to issue #36/PR #37, not to PR #30
or PR #33 — no action item here; re-judging issue #36/PR #37's own
trajectory is out of this role's scope per this role's proposal §3.

## 4. Explicitly out of scope (per this role's proposal §3, restated)

- No code fix applied for either deficiency above — this role never
  edits the observed role's `src/`/`test/`.
- No verdict rendered on issue #36/PR #37's own trajectory or outcome —
  separate issue, separate role's write surface; it is only cited above
  for attribution of a fix's origin.
- No re-judging of `conformance-review`'s parallel issue-29 step-2 work —
  separate branch/PR, not this role's write surface.
- No `pytest`, `node`, or live `rsb serve`/browser instance was run this
  session; `implementation.md`'s "49 passed" claim and its jsdom/curl
  manual-check narrative are reported above as *claimed, not
  independently reproduced*.

## loop_state transitions

- `scope-approved` — 2026-08-03T11:53:58Z, on receipt of the
  `APPROVE issue-29/execution-observation` issue comment
  (https://github.com/tokenmaxxxer/repo-status-board/issues/29#issuecomment-5165967281).
  the enter of phase 2.
- `landed` — this record committed and pushed on
  `issue-29/execution-observation`, reported through PR #42.
