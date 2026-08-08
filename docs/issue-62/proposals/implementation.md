---
status: proposed
files:
  - src/rsb/web/dashboard.css
  - src/rsb/fetch.py
  - docs/specs/design-system.md
  - docs/specs/screen-spec.md
  - test/rsb_tests/test_dashboard_dom.py
  - test/rsb_tests/test_fetch.py
---

# Proposal — implementation, issue #62 (#38 conformance-review Major 4건)

## Request

Resolve four Major findings `docs/issue-38/reports/conformance-review.md`
left open, addressed to this role: `#partial-retry` has no minimum touch
target (R4e); the two `<summary>` disclosure controls issue #38's own commit
added are under 24px tall (R4e2); the selected-row highlight is 1.09:1
against an unselected row and 1.01:1 against hover, and loses outright to
`tr:hover` on CSS specificity (R6d); internal filesystem paths from
`fetch.py` reach the dashboard collapsed-but-unredacted (R5d). Issue #62
asks this proposal to pick, with recorded tradeoffs: a contrast target and
mechanism for R6d plus its specificity ordering against hover, and a
masking point (generation vs. render) and form for R5d.

## Constraints

- No new design tokens, no new hex values, no new dependency — every fix
  reuses a token already defined in `dashboard.css`'s `:root` block.
- Contrast is verified by declared-value computation from the file's own
  hex values (WCAG relative-luminance formula), not visual-regression
  tooling — out of scope per the issue body, same method the source review
  used.
- If this branch's phase 2 starts after issue #61's, coordinate via rebase
  where `dashboard.css`/`design-system.md` overlap (issue #61 touches only
  `dashboard.js`; this proposal's write set has no `dashboard.js` line, so
  overlap risk is limited to those two shared files).

## Rationale

**R5d masking point — server-side (`fetch.py`) over client-side
(`dashboard.js`).** Rejected: masking only where `dashboard.js` renders the
message (a regex strip immediately before `collapsibleDetailHtml(...)`).
The reason for rejection: `webserver.py`'s `api/board.json` endpoint
serializes `BoardModel.errors[].message` verbatim, and that JSON response is
an independently fetchable surface (`curl`, browser devtools, view-source) —
a client-side-only fix leaves the raw internal path exposed there even
while the rendered HTML looks clean, which does not satisfy the issue's
explicit "엄격 독해" (strict reading) framing of "내부 경로 비노출." Masking
at generation in `fetch.py` fixes the field once, before it is ever stored
in `BoardModel` or serialized, closing both surfaces with one change (and,
as a side effect of fixing a shared field, also cleans up `render.py`'s CLI
text output without editing that out-of-scope file). Confirmed via scout
(CWE-209 / OWASP Error Handling Cheat Sheet: sanitize before crossing the
trust boundary, not only at the render layer).

**R6d indicator — a hover-immune `box-shadow` accent over a background
specificity war.** Rejected: bumping `tr.selected-row`'s selector
specificity (e.g. `table.data-table tbody tr.selected-row`) to tie or beat
`tr:hover`'s (0,2,3) on the `background` property. The reason for
rejection: no existing token reaches the 3:1 non-text-contrast floor as a
*background* against white — every `--color-status-*-background` and
`--color-neutral-100/300` was checked (see survey) and all are light tints
deliberately chosen for chip/badge fills, not state indicators; the repo's
own S5 precedent (`--color-neutral-500` at 4.83:1) shows the pattern that
does work is a stronger-weight token used as a border/accent, not a fill.
Chosen instead: `box-shadow: inset 3px 0 0 0 var(--color-status-info-border)`
(already-defined, = `--color-blue-500`, ≈5.17:1 against white, ≈4.70:1
against the hover grey) on `tr.selected-row td:first-child`, reusing this
file's own existing left-accent idiom (`.hygiene-list li`/`.error-list li`,
`border-left: 3px solid var(--color-status-error-border)`). `box-shadow` is
immune to the hover specificity fight by construction — `tr:hover` sets only
`background`, a different property — so no specificity contest needs
winning at all, and `inset` avoids `border-collapse` interactions a real
`border-left` on a collapsed table can trigger (scout-confirmed idiom).

**R4e2 sizing — `min-height` only, `display` left untouched, over the exact
`.row-toggle` pattern.** Rejected: reusing `.row-toggle`'s
`inline-flex`/`min-width`+`min-height` block verbatim, which issue #62's
body suggests for R4e but names no such requirement for R4e2. The reason
for rejection: `<summary>`'s default UA style is `display: list-item`, and
switching it to `flex`/`inline-flex` removes the native disclosure triangle
in Chrome and Firefox (both tie the marker to `list-item`/`::marker`
rendering — scout-confirmed, CSS-Tricks + MDN + Mozilla bugzilla #1270163).
The review's own R4e2 rationale already establishes the horizontal axis
passes (full-width) and only the vertical axis fails, so only `min-height:
24px` is needed; `display` stays at its default.

## What will be done

1. **`dashboard.css` — R4e.** Add `min-width: 24px; min-height: 24px;
   display: inline-flex; align-items: center; justify-content: center;` to
   the existing `.partial-banner a, .partial-banner button.link` rule (the
   rule `#partial-retry` already resolves to via its `class="link"`).
2. **`dashboard.css` — R4e2.** Add `min-height: 24px;` to `.partial-banner
   summary` and to `.error-state details summary`.
3. **`dashboard.css` — R6d.** Add `tr.selected-row td:first-child {
   box-shadow: inset 3px 0 0 0 var(--color-status-info-border); }`. Leave
   the existing `background: var(--color-status-info-background)` on
   `tr.selected-row` as-is (harmless secondary cue, not the sole
   conformance mechanism).
4. **`fetch.py` — R5d.** At the `OSError` branch (current line 35): build
   the message from `e.strerror` (falls back to `str(e)` only if `strerror`
   is `None`) plus `os.path.basename(argv[0])` instead of interpolating
   `argv[0]!r` and `str(e)` directly. At the nonzero-exit branch (current
   line 40): apply a small `_redact_paths(text)` helper — a regex
   substituting absolute-path-looking substrings (`/`-separated tokens with
   no whitespace) with their final path segment — to the stderr `excerpt`
   before it is interpolated. Both sites route through the same helper
   where applicable, so there is one masking implementation, not two.
5. **`design-system.md`.** Extend §5's 24×24px-guaranteed-control list
   (currently naming `row-toggle`/`repo-filter`/`refresh-button`, then
   `.number-link` per issue #56) with `#partial-retry` and the two
   `<summary>` disclosure controls; add a sentence next to the existing
   `neutral-500` contrast note (§2.2) documenting the new selected-row
   accent's computed ratios; update the `DataTable`/`PartialFailureBanner`/
   `ErrorState` component-inventory rows (§6) accordingly.
6. **`screen-spec.md`.** Tighten §2.4/§2.5's "internal paths/provider
   errors no longer expose themselves at a glance" wording to state they
   are masked, not merely collapsed.
7. **Tests.** `test_dashboard_dom.py`: two jsdom `getComputedStyle`
   assertions (`#partial-retry`, both `<summary>` elements resolve to
   `min-height: 24px` or greater in their real DOM context), following the
   `.number-link` precedent — not a text grep, per R9e's finding that grep
   structurally cannot catch this defect class. `test_fetch.py`: red-green
   cases calling `run_flows_json` with a monkeypatched `subprocess.run`
   raising `FileNotFoundError` (assert a fixture absolute path is absent
   from the resulting message, `strerror` text is present) and returning a
   nonzero exit with a stderr line containing a fixture absolute path
   (assert the same absence/redaction).

## Out of scope

- The other nine open findings from `docs/issue-38/reports/conformance-review.md`
  not named by issue #62's body (R2f, R4f, R9a, R4g, R9c, R9e, R3b, R4i) —
  R5f already closed by issue #56.
- `src/rsb/render.py` (CLI text renderer) — not edited; its output improves
  as an incidental side effect of the shared-field fix in `fetch.py`, per
  the Rationale above, but no `render.py` line is touched.
- Rendered/pixel verification (real touch-target geometry, real screenshot
  contrast) — no browser/layout engine in this sandbox; declared-value
  computation and jsdom `getComputedStyle` substitute, per this repo's
  standing convention, disclosed rather than silently assumed.
- `dashboard.js` — no line in it needs to change for any of the four
  findings (R5d's fix is upstream in `fetch.py`; R4e/R4e2/R6d are CSS-only).
- Issue #61's `matchMedia`/`aria-controls` work — separate issue, separate
  file (`dashboard.js`), coordinated by rebase only if needed.

## How you'll know it worked

- `test/rsb_tests/test_fetch.py`: new masking tests fail against
  today's `fetch.py` (red) and pass after the change (green); a fixture
  absolute path string is asserted absent from the resulting error message
  in both the `OSError` and nonzero-exit paths.
- `test/rsb_tests/test_dashboard_dom.py`: new assertions read
  `getComputedStyle(...).minHeight`/`.minWidth` for `#partial-retry` and
  both `<summary>` elements against the real, shipped `dashboard.css` and
  assert `>= 24px`; disclosed if `npm install --prefix test` cannot run in
  the build sandbox, per precedent.
- Contrast recomputation from `dashboard.css`'s own hex values, recorded in
  the phase-2 record: `#2563eb` (via `--color-status-info-border`) against
  `#ffffff` (≈5.17:1), against `--color-neutral-100` (≈4.70:1), and against
  `--color-status-info-background` (≈4.75:1) — all clear the 3:1 floor
  `design-system.md:69-70` already adopts.
- `python3 -m pytest test/ -q` run from `src/` (this sandbox's working
  invocation) shows no regression against the current 57 passed / 9 skipped
  baseline, plus the new tests included.
- `grep -n "24" docs/specs/design-system.md` shows `#partial-retry` and the
  two `<summary>` controls added to §5's list; `grep -n "path" docs/specs/screen-spec.md`
  no longer reads "at a glance" for §2.4/§2.5.
