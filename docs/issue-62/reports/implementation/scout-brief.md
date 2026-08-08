# Scout brief (issue #62, implementation phase 1)

Stages used: 1 sweep round, 3 parallel angles (general-purpose agents, genuinely
concurrent dispatch in one message — no batched-sequential fallback needed).
Wall-clock: ~2.6min (03:02:43Z–03:05:19Z). Judge point after round 1: all three
angles converged on a clear, sourced answer directly usable for a build
decision; a second round would not change any decision — stopped here.

## Angle 1 — `<summary>` 24px sizing without losing the native marker

Must-be: keep `display: list-item` (the default) on `<summary>`; add
`min-height`/padding only. Switching to `display: flex`/`inline-flex` removes
the native disclosure triangle in Chrome and Firefox (both tie it to
`::marker`/`list-item` rendering) and is explicitly warned against by CSS-Tricks
and Mozilla's own bug tracker; no authoritative source shows a flex-based
pattern that keeps the marker cross-browser.
Adopt: `min-height: 24px` on both `<summary>` rules, `display` untouched.
Skip: `.row-toggle`'s exact `inline-flex` box model — wrong fit here (these
are full-width block controls, not glyph-only inline buttons).
Sources: https://css-tricks.com/careful-when-changing-the-display-of-summary/ ,
https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/summary ,
https://bugzilla.mozilla.org/show_bug.cgi?id=1270163

## Angle 2 — persistent, hover-proof selected-row indicator

Must-be (WCAG 1.4.11 Understanding doc, verbatim): a hover effect "does not...
cause the visual indicators for other states, such as focus or selection, to
lose sufficient contrast." Performance axes seen across real systems: (a)
background-tint-only (fails here — no existing token reaches 3:1 on white),
(b) a dedicated combined selected+hover token (Carbon Design System) — not
available under the no-new-token constraint, (c) a hover-immune property for
the indicator (box-shadow/border, untouched by `:hover`) — a real, sourced CSS
idiom for border-like effects specifically because it sidesteps table
`border-collapse` interactions.
Adopt: `box-shadow: inset 3px 0 0 0 <existing blue-500 token>` accent, immune
to the `tr:hover` specificity fight because hover never sets `box-shadow`.
Skip: chasing a specificity war on `background` (Carbon-style combined token
would need a new hex value, which the issue's constraints forbid).
Sources: https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html ,
https://makandracards.com/makandra/12019-css-emulate-borders-inset-box-shadows ,
https://github.com/carbon-design-system/carbon (issues #3141/#7926, combined-state precedent, not adopted here)

## Angle 3 — internal path redaction in error strings

Must-be (CWE-209 / OWASP Error Handling Cheat Sheet): minimal detail to the
client, sanitize before crossing the trust boundary — not only at render time.
Concretely: this app's raw JSON API (`api/board.json`) is a second exposure
surface beyond the rendered HTML, so client-side-only masking (in dashboard.js)
would leave the API response unredacted — masking belongs server-side, at or
before message construction in `fetch.py`.
Adopt: build the known-path message (`argv[0]` launch failure) from
`OSError.strerror` + `os.path.basename(...)`, not raw `str(e)` (Python's own
attribute split exists for exactly this). For the unstructured subprocess-stderr
excerpt, best-effort regex substitution of absolute-path-looking substrings is
a recognized (if inherently incomplete) defense-in-depth pattern, same class as
Sentry's `event_scrubber`.
Skip: full suppression of the stderr excerpt (would remove genuinely useful
diagnostic detail the issue doesn't ask to remove); masking only in
`dashboard.js` (leaves the API response exposed).
Sources: https://cwe.mitre.org/data/definitions/209.html ,
https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html ,
https://docs.python.org/3/library/exceptions.html#OSError

## Gap line

Current state already meets: focus-visible outlines, `.row-toggle`/`.number-link`
24×24px precedent to reuse, `collapsibleDetailHtml`'s escape+collapse structure
(reusable, just not sufficient alone for R5d). Missing: any hover-immune state
indicator anywhere in `dashboard.css` (all existing state cues are
background-only), and any path-redaction helper in `fetch.py` (raw `str(e)`/
raw stderr excerpt used verbatim throughout).

## Segment fit

This is an internal single-operator ops tool, not a public product — the bar is
"meets the repo's own adopted WCAG floors with existing tokens," not visual
polish or a branded design system. All three adopted patterns are the plainest
option each angle's sources support, not the most elaborate one available
(explicitly skipped Carbon's combined-state token and any new `::marker`
restyling).
