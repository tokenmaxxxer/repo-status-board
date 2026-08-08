# Implementation record — touch-target/contrast/masking Major 4건 (issue #62, phase 2)

code_under_review: src/rsb/web/dashboard.css, src/rsb/fetch.py, docs/specs/design-system.md, docs/specs/screen-spec.md, test/rsb_tests/test_dashboard_dom.py, test/rsb_tests/test_fetch.py
loop_state: landed

## Why

Approved via issue #62 comment `APPROVE issue-62/implementation`
(jjongkwann, 2026-08-08T03:09:38Z, single-account mode — PR #64 author
and approver are the same account, both listed in
`docs/specs/approvers.md`; comment body checked as the exact string, no
near-match). Executes `docs/issue-62/proposals/implementation.md`'s
"What will be done" (7 items) as approved, resting on
`docs/issue-62/reports/implementation/survey.md` and
`docs/issue-62/reports/implementation/scout-brief.md`.

`git diff --stat` of `origin/main`'s 3 commits ahead of this branch
(`issue-56/execution-observation` phase 1+2, all under `docs/issue-56/`)
against this proposal's write set showed zero overlap — no rebase
needed. No `issue-61/implementation` branch or PR existed at either
phase-1 or phase-2 start (checked both sessions), so the Constraints'
rebase-coordination clause with issue #61 did not apply.

## What was done

Executed `docs/issue-62/proposals/implementation.md`'s "What will be
done" 1–7, with one content strengthening beyond the proposal's literal
regex wording found necessary by the before-landing warrant hunt (see
"Warrant hunt" and "What did not work" below) — everything else landed
exactly as proposed.

1. **`dashboard.css` R4e** (`:325-333`): `.partial-banner a, .partial-banner
   button.link` (covers `#partial-retry`, a `<button class="link">`) gained
   `min-width: 24px; min-height: 24px; display: inline-flex; align-items:
   center; justify-content: center` — the same box model `.row-toggle`/
   `.number-link` already use.
2. **`dashboard.css` R4e2** (`:342-349`, `:363-369`): `.partial-banner
   summary` and `.error-state details summary` each gained `min-height:
   24px;` only — `display` untouched (stays the UA default `list-item`),
   per the proposal's rationale that switching to flex would drop the
   native disclosure triangle in Chrome/Firefox.
3. **`dashboard.css` R6d** (`:211-213`): new rule `tr.selected-row
   td:first-child { box-shadow: inset 3px 0 0 0
   var(--color-status-info-border); }`, added directly after the existing
   `tr.selected-row { background: ... }` rule, which is kept unchanged as
   a secondary cue.
4. **`fetch.py` R5d** (`:17-40` `_redact_paths`, `:64-67` OSError branch,
   `:70-73` nonzero-exit branch): OSError branch now builds the message
   from `e.strerror` (falls back to `str(e)` only when `strerror is
   None`) plus `os.path.basename(argv[0])`, replacing the old
   `{argv[0]!r}: {e}` interpolation. The nonzero-exit branch's stderr
   `excerpt` (last non-empty line) is passed through `_redact_paths`
   before interpolation. Both sites route through the same
   `_redact_paths` helper where applicable (the OSError branch's
   `detail` too, in case a `strerror`/`str(e)` fallback embeds a path) —
   one masking implementation, not two, per the proposal.
5. **`design-system.md`**: §5's 24×24px-guaranteed-control paragraph
   (`:141-176` region) gained a sentence naming `#partial-retry` and the
   two `<summary>` controls, with the min-height-only/display-preserved
   rationale. §2.2 (`:52-89` region) gained a paragraph documenting the
   new selected-row accent's computed ratios (see "Tests" below for the
   numbers). §6's `DataTable`, `ErrorState`, and `PartialFailureBanner`
   rows were extended with the box-shadow accent, the 24×24px sizes, and
   the "masked at generation, not merely collapsed" wording.
6. **`screen-spec.md`** §2.4 and §2.5: both replaced "no longer expose
   themselves at a glance" with wording stating internal filesystem
   paths are masked at generation in `fetch.py`, not merely collapsed
   behind the `<details>`; both sections also gained a sentence naming
   the 24×24px controls each renders. `grep -n "at a glance"
   docs/specs/screen-spec.md` → 0 hits (confirmed).
7. **Tests** — `test_dashboard_dom.py`: two new functions,
   `test_partial_retry_and_its_summary_meet_24px_min_box` and
   `test_error_state_summary_meets_24px_min_height`, each driving
   dashboard.js's real render path (`_run_dom_js` with a new `html`
   param) against a jsdom DOM with the real, shipped `dashboard.css`
   inlined as `<style>` (`_dashboard_html_with_css()`), asserting
   `getComputedStyle(...).minWidth`/`.minHeight` — not a text grep, per
   R9e. `test_fetch.py`: `test_run_flows_json_oserror_masks_internal_path`
   and `test_run_flows_json_nonzero_exit_masks_internal_path` call
   `run_flows_json` directly with a monkeypatched `subprocess.run`
   (`FileNotFoundError` / nonzero-exit-with-stderr respectively),
   asserting a fixture absolute path is absent from the resulting
   message while the diagnosable text (`strerror`, "not found") survives.
   Both confirmed **red** against the pre-fix `fetch.py` (unmasked
   `argv[0]!r: {e}`/raw `excerpt` interpolation) before the `fetch.py`
   edit, then **green** after — see "Tests" below for the actual runs.
   A third test, `test_run_flows_json_nonzero_exit_masks_internal_path_with_spaces`,
   was added beyond the proposal's literal two cases after the
   before-landing warrant hunt found a real gap (see "Warrant hunt").

## What did not work

- First `_redact_paths` implementation was a single regex,
  `(?<!\S)/(?:[^\s/]+/)+[^\s/]*` (whitespace-free path tokens only, per
  the proposal's own wording). The before-landing warrant hunt
  reproduced a real bypass: a path with an embedded space (e.g. a macOS
  `/Users/Jane Doe/...` home directory) only had its first
  whitespace-delimited fragment redacted — the remainder
  (`.secret-checkout/repo/flows.json`) survived verbatim in the
  `RuntimeError` message. Replaced with a word-scan that merges a
  leading `/`-starting word with every immediately-following
  still-`/`-containing word before taking `os.path.basename` of the
  joined run (`fetch.py:17-40`). Added
  `test_run_flows_json_nonzero_exit_masks_internal_path_with_spaces` to
  cover it; confirmed red against the old regex, green after the
  replacement (see "Tests").
- `git fetch origin` at phase-2 start returned `failed to store: 100001`
  (this sandbox's constrained git-credential/network path) but the local
  `origin/main` ref was already current from a prior fetch, so `git log
  origin/main`/`git diff --stat` against it still worked — no impact on
  the coordination check.

## Rationale for deviations

None against the approved proposal's *content* — the write set, the
`.row-toggle`-pattern box model, the `min-height`-only `<summary>`
sizing, the `box-shadow` accent choice and token, and the
generation-point masking choice all landed exactly as proposed. The one
change beyond the proposal's literal text is the `_redact_paths`
*mechanism* (regex → word-scan), which is not a swapped alternative but
a strengthening of the same approved mechanism after the before-landing
warrant hunt found the literal proposed regex under-redacts
space-containing paths — recorded here per the deviation-tracking
requirement since it is a change from the proposal's literal wording,
even though the goal ("no internal path exposed," "one masking
implementation") is unchanged and the write set is unchanged (same
file, same function, no new file added).

## Doc-placement ladder

- [x] `docs/specs/design-system.md` §5/§2.2/§6 — same turn as the code
      (see "What was done" §5).
- [x] `docs/specs/screen-spec.md` §2.4/§2.5 — same turn as the code
      (see "What was done" §6).
- [x] `docs/issue-62/reports/implementation.md` (this file).

## Tests

`cd src && python3 -m pytest ../test/ -q` — **69 passed, 2 failed**
(jsdom present this session — `npm install --prefix test` succeeded,
`registry.npmjs.org` is on this sandbox's allowed-hosts list). The 2
failures (`test_row_toggle_click_opens_detail_and_flips_aria_expanded`,
`test_row_toggle_reactivating_open_button_closes_it`) are **pre-existing
on `main`, unrelated to this issue's write set** — same root cause
`docs/issue-56/reports/implementation.md`'s "Tests" section already
disclosed (`f353910`'s unguarded `window.matchMedia(WIDE_LAYOUT_QUERY)`
call, `dashboard.js:508`, confirmed still present and untouched by this
diff via `git diff --stat src/rsb/web/dashboard.js` → empty). This is
issue #61's concern, out of scope here.

Red-green, run individually:
- `test_run_flows_json_oserror_masks_internal_path`,
  `test_run_flows_json_nonzero_exit_masks_internal_path`: **red** against
  unmodified `fetch.py` (`assert fixture_path not in message` failed,
  both sites interpolated the raw path) — 2 failed. **Green** after the
  `fetch.py` R5d edit — all `test_fetch.py` tests passed (12/12 at that
  point).
- `test_run_flows_json_nonzero_exit_masks_internal_path_with_spaces`:
  **red** against the first (regex) `_redact_paths` — `.secret-checkout`
  survived in the message. **Green** after the word-scan replacement —
  `test_fetch.py` 13/13 passed.

New DOM tests, run individually with jsdom installed:
`test_partial_retry_and_its_summary_meet_24px_min_box` and
`test_error_state_summary_meets_24px_min_height` — **2 passed** (real
`getComputedStyle` against the real, shipped `dashboard.css`, resolving
`minWidth`/`minHeight` to exactly `"24px"` in each element's real
rendered DOM context via `dashboard.js`'s actual `renderData()` /
`renderFullError()` paths).

Contrast recomputation (declared hex values, WCAG relative-luminance
formula, same method `docs/issue-38/reports/conformance-review.md` and
this proposal's survey used):
- `--color-status-info-border` (`#2563eb`) vs `--color-surface-raised`
  (`#ffffff`): **≈5.17:1**.
- `--color-status-info-border` (`#2563eb`) vs `--color-neutral-100`
  (`#f3f4f6`, `tr:hover`'s background): **≈4.70:1**.
- `--color-status-info-border` (`#2563eb`) vs `--color-status-info-background`
  (`#eff6ff`, the row's own existing tint): **≈4.75:1**.
All three clear the 3:1 WCAG 1.4.11 non-text floor `design-system.md`
§2.2 already adopts (reused, unmodified, from the survey's identical
computation).

grep verification (matches proposal's "How you'll know it worked"):
- `grep -n "24" docs/specs/design-system.md` — `#partial-retry` and both
  `<summary>` controls present in §5/§6.
- `grep -n "at a glance" docs/specs/screen-spec.md` — 0 hits.
- `grep -n "_redact_paths\|basename" src/rsb/fetch.py` — helper defined,
  both call sites route through it.

## Warrant hunt

### before-landing — stance 0: assume the gate just touched is bypassable — find a path where the claimed guarantee does not hold

Full record: `docs/reports/2026-08-08-hunt-issue-62-implementation.md`
(the dispatch prompt named a path under this issue's own reports tree,
but the repo's `board-gate.sh` hook refused that filename for the
`implementation` role per contract v3 s11 — that path belongs to
another role's record area — so the hunter filed under the standing
top-level `docs/reports/` bucket instead, which the same gate allows;
noted here since the file lives outside this issue's own tree).

Verdict: **FINDING**, confirmed and fixed before landing. `_redact_paths`'s
first implementation (a single regex requiring whitespace-free path
tokens) left a directory name containing a space
(`/Users/Jane Doe/.secret-checkout/repo`) only partially redacted —
`.secret-checkout` survived verbatim in the `RuntimeError` message, the
exact sink (`BoardModel.errors[].message` → `api/board.json` / rendered
HTML) the R5d claim says never sees an internal path. Reproduced by the
hunter with a runnable repro (fixture path in a monkeypatched
`subprocess.run`'s stderr); reproduced again locally via
`test_run_flows_json_nonzero_exit_masks_internal_path_with_spaces`
(red). Fixed by replacing the regex with a word-scan merge (see "What
did not work" / "What was done" §4/§7); the same test is green after
the fix, and the fix is part of this record's `code_under_review`.

cap_seconds: 180, tier: size:large (diff was 216 insertions/14
deletions across 6 files at dispatch time). Dispatched via
`run_in_background: false` (foreground) per contract v3 s22 —
headless/single-shot session, result consumed in the same turn before
any commit.

closed_checks:
- full-test-suite: `cd src && python3 -m pytest ../test/ -q` — 69
  passed, 2 pre-existing failures (matchMedia gap, `f353910`, out of
  scope — see "Tests" above). code_sha: this branch's pending commit
  (code_under_review: as listed above).
- fetch-masking-red-green: `test_fetch.py`'s 3 masking tests confirmed
  red pre-fix, green post-fix (see "Tests" above).
- dashboard-dom-24px-getComputedStyle: 2 new tests, real jsdom, real
  dashboard.css, both green (see "Tests" above).
- contrast-recomputation: 3 ratios recomputed from declared hex values
  (see "Tests" above), all clear the 3:1 floor.
- grep-at-a-glance-removed: `grep -n "at a glance"
  docs/specs/screen-spec.md` — 0 hits.
- before-landing-warrant-hunt: stance 0 (bypass claimed guarantees) —
  FINDING, fixed, re-verified green (see above).

## Open findings

None — the one finding the before-landing warrant hunt returned was
fixed and re-verified (red→green) within this same phase-2 session,
before any commit. No other check surfaced an issue.

## Next steps

None — phase 2 is complete. This record is finalized (`loop_state:
landed`); commit follows immediately.

## Open-finding resolution path

N/A — no open findings (the one finding raised was resolved in-session,
see "Warrant hunt" above).
