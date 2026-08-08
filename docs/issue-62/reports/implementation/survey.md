# Current-state survey (issue #62, implementation phase 1)

## Source of the four findings

All four are open findings from `docs/issue-38/reports/conformance-review.md`
(loop_state: reported, 13 open findings total), addressed to the
implementation role. Issue #62 picks up the four the issue body names: R4e,
R4e2, R6d, R5d (all Major). The other nine open findings (R2f, R4f, R9a; R4g,
R9c, R9e; R3b, R4i; plus R5f already closed by issue #56) are out of scope
here — R2f/R4f/R9a and the Minor/Note rows are not named by issue #62's body.

## Write set this proposal will freeze

- `src/rsb/web/dashboard.css` — `#partial-retry` sizing (R4e), the two
  `<summary>` rules (R4e2), `tr.selected-row` indicator (R6d).
- `src/rsb/fetch.py` — path masking at the two message-construction sites
  (R5d).
- `docs/specs/design-system.md` — §5 24×24px list, §2 contrast note, §6
  component-inventory rows touched by the above.
- `docs/specs/screen-spec.md` — §2.4/§2.5 error-copy wording (currently says
  paths "no longer expose themselves at a glance" — a strict reading this
  issue's own body rejects) and §1.3 selected-row wording if present.
- `test/rsb_tests/test_dashboard_dom.py` — new touch-target assertions
  (R4e, R4e2), following the jsdom `getComputedStyle` pattern issue-56 used
  for `.number-link`, not a text grep.
- `test/rsb_tests/test_fetch.py` — new red-green cases for path masking
  (R5d), calling `run_flows_json` directly (no existing test does).
- `docs/issue-62/reports/implementation.md` — phase-2 record (not written
  this phase).

No `src/rsb/web/dashboard.js` change is anticipated: R5d's fix point (see
below) is server-side in `fetch.py`, so `dashboard.js:600`'s consumption of
`data.errors[].message` needs no edit if the string arrives already masked.

## R4e — `#partial-retry` (dashboard.css:302-318 in current file)

Current rule: `.partial-banner a, .partial-banner button.link { color: ...;
background: none; border: none; text-decoration: underline; cursor: pointer;
padding: 0; font: inherit; }` — no `min-height`/`min-width`. `#partial-retry`
is `<button class="link" id="partial-retry">Retry</button>`
(`dashboard.js:592`, one line before its own `document.getElementById(...)`
listener at `:595`). It sits inline after the `collapsibleDetailHtml(...)`
call in the same sentence, same shape as `.number-link` before issue #56
sized it. `.row-toggle`'s box model (`dashboard.css:220-227`): `min-width:
24px; min-height: 24px; display: inline-flex; align-items: center;
justify-content: center;` — issue #62's body names this exact pattern for
reuse.

## R4e2 — the two `<summary>` rules

`.partial-banner summary` (`dashboard.css:320-323` block) and `.error-state
details summary` (`:338-341`) each declare only `cursor: pointer;
margin-top: ...` (plus `.partial-banner details[open] summary` adds
`margin-bottom`). Both are full-width by default (`<summary>`'s UA style is
`display: list-item`, a block-level box) — the conformance-review record
(R4e2 rationale) already established the horizontal axis passes and only the
vertical (line-height-only height) axis fails. `.row-toggle`'s pattern is not
a drop-in fit: it is `inline-flex` sized for a glyph-only inline button,
whereas these are full-width block disclosure triggers with native marker
rendering that `display: flex`/`inline-flex` would risk removing (see
scout-brief angle 1).

## R6d — selected-row contrast + hover specificity loss

`dashboard.css:197-199`: `tr.selected-row { background:
var(--color-status-info-background); }` = `#eff6ff` on the table's
`--color-surface-raised` = `#ffffff`. Recomputing WCAG relative luminance
from these hex values (same method the conformance-review record used, and
reproduces its published 1.09:1/1.01:1 figures exactly):

- `#eff6ff` vs `#ffffff`: L≈0.9150 vs 1.0 → contrast ≈ **1.09:1** (confirms
  the review's figure).
- `#eff6ff` vs `--color-neutral-100` (`#f3f4f6`, the `tr:hover` background,
  L≈0.9043): contrast ≈ **1.01:1** (confirms the review's figure).

Both are far under `design-system.md:69-70`'s adopted 3:1 WCAG 1.4.11 floor.
Specificity: `table.data-table tbody tr:hover` = (0,2,3) vs `tr.selected-row`
= (0,1,1) — hover's rule wins outright on any selected+hovered row,
regardless of source order, so the highlight visibly disappears on hover
today.

Existing tokens available as a background fill (`--color-status-*-background`,
all light tints; `--color-neutral-100/300`) were checked and **none** reaches
3:1 against white — they are deliberately light tints for chip/badge fills
(design-system.md §2.3), not state-indicator fills. The one existing token
combination that does reach 3:1 as a *foreground-weight* color is
`--color-blue-500` (`#2563eb`, already defined as `--color-status-info-border`)
— recomputed at ≈**5.17:1** against white, ≈**4.70:1** against the hover
grey, ≈**4.75:1** against the existing `#eff6ff` tint. This is not usable as
a full-row *background* (too dark for body text legibility at that size) but
is already used elsewhere in this file as a border/accent color
(`.hygiene-list li`/`.error-list li` reuse the same idiom: `border-left: 3px
solid var(--color-status-error-border)`, `dashboard.css:349-350`).

## R5d — internal path exposure

`src/rsb/fetch.py:35`: `raise RuntimeError(f"failed to launch {argv[0]!r}:
{e}") from e` — `argv[0]` is `repo_config.command[0]` (config-supplied,
defaults to `"python"` but can be an absolute path per `config.py:60`); `e`
is an `OSError`/`FileNotFoundError` whose `str(e)` embeds the OS-formatted
message *including* the attempted path (Python's own `.strerror`/`.filename`
attributes are separate from this string — see scout-brief angle 3).
`fetch.py:40`: `raise RuntimeError(f"flows --json failed: {excerpt}")` —
`excerpt` is the last non-empty line of the subprocess's own captured
stderr (arbitrary text from an external tool, not structured).

Both messages flow unmodified: `fetch_and_normalize_one` returns them as
`error_message` (`fetch.py:53-54`, `:63-64`... consistent with the
conformance-review's cited chain), `merge_repos` carries them into
`BoardModel.errors[].message`, `webserver.py`'s `api/board.json` serializes
them verbatim, and `dashboard.js:588-591` interpolates the raw string into
`collapsibleDetailHtml("Details", detail)` — which escapes for HTML and
hides behind a closed `<details>`, but does not redact. `render.py:154` (CLI
text renderer, explicitly out of scope per issue #38's review) prints the
same `.message` verbatim to stdout — masking at generation
(`fetch.py`) would also clean up the CLI's output as a side effect of fixing
the shared field, without editing `render.py` itself.

**Two fix-point candidates, as the issue asks the proposal to decide:**
1. **Client-side, in `dashboard.js`** (regex-strip before interpolation).
   Rejected: `api/board.json` is a second, independently fetchable exposure
   surface (`curl`/devtools/view-source) that a client-side-only fix leaves
   completely unmasked — the literal internal path would still cross the
   trust boundary in the JSON response even if the rendered HTML looked
   clean. This does not satisfy the issue's "엄격 독해" framing (screen-spec's
   own "no longer expose themselves at a glance" wording is exactly the
   narrower reading issue #38's review already flagged as insufficient).
2. **Server-side, in `fetch.py`** (this proposal's choice) — masks the
   message once, before it is ever stored in `BoardModel` or serialized,
   closing both the API and the rendered-HTML exposure with one change.

## Coordination: issue #61

`gh issue view 61` (checked this session): OPEN, no `issue-61/implementation`
branch or PR exists yet (`gh pr list --state open` shows only #59 issue-58 and
#60 issue-56/execution-observation). Issue #61 touches `dashboard.js` (a
`matchMedia` guard and an `aria-controls` fix, lines ~238/519-525) and
explicitly names issue #62 as the parallel-file-overlap case needing a
phase-2 rebase. This proposal's write set does not include `dashboard.js` at
all (see "Write set" above), so the overlap risk is confined to
`dashboard.css`/`design-system.md` at most, and issue #61's own body places
the rebase obligation on whichever phase 2 starts second — noted here, acted
on at phase-2 start.

## Test infrastructure state (checked this session)

`cd src && python3 -m pytest ../test/ -q` → **57 passed, 9 skipped** (all 9
skips are `test_dashboard_dom.py`'s jsdom-dependent tests — `test/node_modules/`
is absent in this sandbox, same constraint issue-38's conformance-review and
issue-56's implementation record both hit and disclosed). New DOM-assertion
tests for R4e/R4e2 will be added to `test_dashboard_dom.py` following the
`.number-link` precedent (jsdom `getComputedStyle` against the real
`dashboard.css`, not a text grep) — whether they run green in *this* sandbox
depends on `npm install --prefix test` succeeding, which is outside this
role's network access; if it fails, phase 2 discloses the skip exactly as
precedent does, rather than substituting a weaker (grep-based) assertion that
issue #38's review already named as structurally unable to catch this class
of defect (R9e).

Path-masking tests (R5d) are plain `pytest` (no jsdom dependency) added to
`test/rsb_tests/test_fetch.py`, calling `run_flows_json` directly with a
monkeypatched `subprocess.run` — no existing test exercises that function's
own error-message construction (existing failure-path tests in
`test_fetch_and_normalize_one_*` inject a pre-built `RuntimeError` via a fake
`run_json_fn`, bypassing `run_flows_json` entirely).

## Warrant hunt (end of phase 1)

Docs-only fast path applied: every path this phase-1 transition touches
(`docs/issue-62/reports/implementation/scout-brief.md`,
`.../survey.md` (this file), `docs/issue-62/proposals/implementation.md`) is
under `docs/`, and no `src/`/`test/` line has changed yet — no code exists
for a bypass-hunt to probe. No before-landing-style dispatch made for this
transition; the next warrant-hunt dispatch is due before phase-2 completion,
once the write set above actually lands in `src/`/`test/`.

## Constraints re-confirmed from the issue body

- No new design tokens, no new hex values, no new dependency — confirmed
  every fix above reuses tokens already defined in `dashboard.css`'s
  `:root` block.
- Contrast verified by declared-value computation (WCAG relative-luminance
  formula from the file's own hex values), not visual regression — same
  method `docs/issue-38/reports/conformance-review.md` used, reproduced
  above to confirm methodology parity.
