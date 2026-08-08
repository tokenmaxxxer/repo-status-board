# Current-state survey — conformance-review, issue #44 phase 1

Read-only survey of the artifact under review and of what can actually be
verified about it from this checkout. No verdicts here: phase 1 extracts the
requirement list and names the unknowns; verdicts are phase-2 output
(role-handoff contract v3 §19).

## 1. Target artifact

Issue #44's execution plan is `step 1 test-authoring` → `step 2
execution-observation ‖ conformance-review`. Step 1 is merged, so the artifact
under review is **PR #45** (`b2f6b63`, merged 2026-08-03T12:31:44Z), which
carried the test-authoring role's phase 1 **and** phase 2 in one PR (approved
via the issue comment `APPROVE issue-44/test-authoring`, single-account mode).

Files it landed:

| Path | Role in the artifact |
|---|---|
| `test/rsb_tests/test_dashboard_dom.py` | the harness itself — 8 pytest functions + the `_run_dom_js` helper |
| `test/package.json`, `test/package-lock.json` | `jsdom ^30.0.1` (resolved `30.0.1`), 38-package closure |
| `docs/handbooks/rsb.md` (§`## Tests`, lines 48–63) | run instructions + "extend this harness instead of one-off scripts" |
| `docs/issue-44/reports/test-authoring.md` | phase-2 record (incl. AC crosswalk, Verification, Open findings) |
| `docs/issue-44/proposals/test-authoring.md` | approved phase-1 ADR (jsdom, pytest entry point) |

`src/**` was not touched. `test/rsb_tests/test_model.py`'s `_run_dashboard_js`
(`test/rsb_tests/test_model.py:170`) is unchanged and still drives 9 test
functions / 10 invocations.

## 2. Spec basis

`gh issue view 44`: four numbered 요구사항, six 수용 기준 checkboxes, three
범위 밖 exclusions. The 배경 section names three defects (repo-filter wiring,
row-toggle wiring, mobile overflow / issue #38 P1-1) plus one independent
**Absent** ruling (issue #27 conformance-review, on `fetch("api/board.json")`).

## 3. What is in the harness now

`_run_dom_js` (`test/rsb_tests/test_dashboard_dom.py:51-95`) generates a Node
program per test: `require("jsdom")` → `new JSDOM(DASHBOARD_HTML, {url:
"http://localhost/"})` → assigns `global.window`/`global.document` → installs a
recording `global.fetch` that appends to `global.__fetchCalls` → busts
`require.cache` and `require`s the shipped `src/rsb/web/dashboard.js` fresh →
awaits one macrotask tick → runs the caller's JS, which dispatches real events
(e.g. `btn.click()`) and `console.log(JSON.stringify(...))`s the resulting DOM
state back. Python side: `subprocess.run(["node", "-e", program], …,
timeout=10)`, `assert result.returncode == 0`, `json.loads(result.stdout)`.

Eight tests, mapped by the artifact to issue #44's three minimum-coverage
bullets:

- repo-filter `<select>` population — lines 128, 137, 146 (zero / one / multiple
  repos incl. an errored-only repo)
- `.row-toggle` wiring — lines 177 (`aria-expanded` false→true + detail slot
  filled), 197 (plain `<td>` click opens nothing), 214 (cross-table isolation),
  231 (BVA: re-click closes)
- `load()` relative fetch path — line 254 (`__fetchCalls == ["api/board.json"]`)

Corresponding production seams in the shipped file: auto-init guard
`src/rsb/web/dashboard.js:671`, `updateRepoFilterOptions` defined :535 called
:658, `attachRowToggleHandlers` defined :549 called :643, `fetch("api/board.json")`
:651, `module.exports` :680-682 (10 names).

## 4. Verifiability of this checkout — what phase 2 will and will not be able to run

Measured here, read-only:

- `node v26.5.1`, `npm 11.17.0`, `python3 3.11.8`, `pytest 8.4.1` — all present.
- `test/node_modules` **does not exist**; jsdom is not installed anywhere in the
  tree.
- The DOM suite still *collects* fine: `pytest test/rsb_tests/test_dashboard_dom.py
  --collect-only -q` → `8 tests collected`. But the guards at
  `test/rsb_tests/test_dashboard_dom.py:62-65` (`shutil.which("node")`,
  `JSDOM_MODULE.exists()`) fire at call time, so with jsdom absent all 8 would
  report **skipped**, not failed.
- `python3 -m pytest test/ -q` currently **aborts at collection**: 6 collection
  errors, `ModuleNotFoundError: No module named 'rsb'` — the handbook's
  `pip install -e .` step has not been run in this container. This is an
  environment state, not an artifact defect, but it means "the suite passes"
  cannot be observed here without setup.
- `npm view jsdom version` → `30.0.1`; the npm registry **is** reachable, so
  `npm install --prefix test` is expected to be possible in phase 2.
- `.gitignore` (5 lines) has **no** `node_modules` entry; `git status --short`
  is clean.

Pre-fix revisions cited by the record all resolve and all contain
`src/rsb/web/dashboard.js`: `c94e12d^` → `3ebecae`, `b621082^` → `5d05b5f`,
`3ebecae^` → `b630292`. Note `c94e12d^` and the separately-cited `3ebecae` are
the **same commit** — consistent with the history (the fetch-path fix landed in
`3ebecae`, the repo-filter wiring in its child `c94e12d`), not in itself a
discrepancy, but it means one revision serves two different pre-fix roles and
phase 2 should not treat "three distinct pre-fix states" as given.

## 5. Open unknowns — what phase 2 has to resolve, and what aimed the scout

- **U1 — AC2's arity.** AC2 reads "배경의 결함 3건 + Absent 1건에 **각각**
  대응하는 테스트", i.e. four items; 요구사항 2's bullet list enumerates only
  three (filter / toggle / fetch path), omitting mobile overflow. The artifact
  covers three and declares the fourth intentionally uncovered
  (`docs/issue-44/reports/test-authoring.md:251-259`), citing 범위 밖's
  visual-regression exclusion. This is the review's central adjudication and is
  deliberately left open here.
- **U2 — pre-fix failure evidence is prose, not artifact.** The record states
  each defect-tracing test was re-run against its pre-fix revision and failed
  (`docs/issue-44/reports/test-authoring.md:206-216`), but the scratch files
  were "deleted after use, never committed". Nothing in the repo reproduces it;
  AC2's "실제로 실패함이 **확인**된다" therefore has no standing evidence unless
  phase 2 re-derives it. The record also states the BVA close-toggle test was
  *not* separately re-verified (lines 217-221).
- **U3 — this container cannot run the suite as-is** (§4). Phase 2 needs
  `pip install -e .` (or `PYTHONPATH=src`) and `npm install --prefix test`
  before any execution evidence exists; if either fails, the affected
  requirements are Unverifiable, not favorably assumed.
- **U4 — skip-not-fail.** Because the missing prerequisite skips rather than
  fails, a green run does not by itself show the DOM layer was exercised. Any
  AC1/AC3 evidence must distinguish *executed* from *collected*.
- **U5 — dependency placement.** `jsdom` is declared under `"dependencies"`
  (`test/package.json:6`), with no `devDependencies` key, while the record
  describes it as "dev/test-only" (`docs/issue-44/reports/test-authoring.md:185`).
- **U6 — citation drift in the artifact's own docs.** The auto-init seam is
  cited as `dashboard.js:584-591` (`docs/issue-44/proposals/test-authoring.md:41-43`,
  `test/rsb_tests/test_dashboard_dom.py:9-10`) but sits at
  `src/rsb/web/dashboard.js:671`; the export list is described as "8 pure
  functions" while `module.exports` names 10.
- **U7 — AC5 rationale location.** The record records the dependency but routes
  its selection rationale to the phase-1 proposal and states it is "not
  re-litigated here" (`docs/issue-44/reports/test-authoring.md:186-189`).
  Whether a pointer satisfies "근거가 **record** 에 남는다" is a phase-2 call.
- **U8 — 요구사항 4** (relationship to the existing pytest suite) has no
  matching 수용 기준 checkbox, so it needs its own requirement rather than
  riding on an AC.
- **U9 — unresolved hand-off.** The record flags a `.gitignore` `node_modules/`
  entry as out of its `test/**` write scope
  (`docs/issue-44/reports/test-authoring.md:243-250`); confirmed still absent.

## 6. House form this review will match

Existing conformance-review chains: issues 4, 23, 27, 29, 34. Settled
conventions found there — phase-1 writes
`docs/issue-N/proposals/conformance-review.md` +
`docs/issue-N/reports/conformance-review/{survey,scout-brief}.md`; phase-2
writes only `docs/issue-N/reports/conformance-review.md`; report tables are
`| Requirement | Verdict | Evidence | Rationale |`; verdict enum is
`Present / Surface / Absent / Incorrect / Unverifiable` (from
`review-traceability`'s `finding-record` skill — no in-repo spec defines it);
every prior proposal enumerated all requirements rather than sampling; issue-34
is the precedent for stating a verification *method* per requirement, which
this proposal follows.

## 7. Scout

Not skipped. Scouting ran after this survey and aimed at U1–U9; see
`scout-brief.md` in this directory.
