# issue-56 scout brief

Angles derived from survey §5's two open decisions. Stage 1 (sweep):
3 parallel `WebSearch` calls, one turn — genuine concurrent dispatch, not
serialized. Stage 2 (deepening): 1 `WebFetch` against the primary W3C
source, run after judge point 1 found the secondary sources converging
but wanting a primary-source quote. 2 stages total, ~35s wall-clock
(`date +%s` before/after) — well under the 5-stage/3min budget; stopped
at judge point 2 (saturation) since the primary source confirmed the
secondary consensus with no disagreement to chase.

## Requirement 2 (.number-link / WCAG 2.5.8 inline exception)

**Must-be**: the inline exception text is precise and narrow — "the
target is in a sentence or its size is otherwise constrained by the
line-height of non-target text" (verbatim from the primary source). It
exists because reflow makes link position within a text flow
unpredictable, not because "the link is short" or "the link is small
text" generically.

**Must-be**: standalone links that are the sole content of a table cell
or list item — no surrounding prose, no non-target text setting the
line-height — are the case guides explicitly call out as **not**
qualifying: "the exception doesn't universally apply to all text links,
only to those which actually are constrained by line-height... links
inside table cells or list items would need to meet the 24×24
requirement unless they are genuinely constrained by surrounding text
formatting." `.number-link`'s two DOM contexts (survey §2) are exactly
this case: `.issue-cell` pairs it only with a `.row-toggle` button (a
target, not text), and `.mono` contains nothing but the link itself.
Neither has non-target prose around it.

**Pattern to adopt**: this codebase already has a working 24×24px
technique for an inline-ish control at `.row-toggle`
(`min-width`/`min-height` + `display: inline-flex` +
`align-items`/`justify-content: center`) — the natural fix mirrors that
rather than introducing a second technique (e.g. padding-based
enlargement, which would visually inflate the glyph instead of just its
hit box).

**Pattern to skip**: treating the pre-existing 8×17px figure in issue
#38's body as itself satisfying "실측" for this issue — that number was
a real-device measurement of the *problem*, not a determination of
*whether the exception applies*, which is the actual open condition
issue-38's approved proposal deferred.

## Requirement 1 (duplicate error surface)

**Must-be**: single-source-of-truth is the standard guidance for
multiple-surface error states — showing the same failure through two UI
elements risks exactly the inconsistency GitLab's own tracked issue
describes for its Metrics view (a warning and an error competing for
one surface, resolved by picking one to show). Error-UX literature
converges on "put the message near the problem, once," not duplicated
at two page positions.

**Gap line**: the current codebase already meets the "summary + collapsed
detail, no raw path exposed" must-be for 2 of 3 error surfaces
(`renderFullError`, the partial banner) — issue #38 P2-6 built exactly
that pattern. The one surface still missing it is `renderErrors`, which
survey §1 shows is not an independent surface needing the same fix
applied twice, but a literal duplicate of the banner's own data on every
reachable path — so the gap here is redundancy, not a missing pattern.

## Segment fit

Internal ops/status dashboard, not a public consumer product — the bar
this scout applies is "match the accessibility rigor this repo's own
issue-38 already set" (AC4/AC5, WCAG 2.5.8 + no-raw-path-disclosure),
not a broader consumer-dashboard feature comparison. No new pattern
needs importing from outside the codebase; both fixes reuse conventions
already proven here (`.row-toggle`'s box model, `collapsibleDetailHtml`).

Sources:
- https://w3c.github.io/wcag/understanding/target-size-minimum.html
- https://testparty.ai/blog/wcag-2-5-8-target-size-minimum-2025-guide
- https://www.allaccessible.org/blog/wcag-258-target-size-minimum-implementation-guide
- https://gitlab.com/gitlab-org/gitlab/-/issues/222320
- https://en.wikipedia.org/wiki/Single_source_of_truth
