# Scout brief — issue #29 (parallel fetch, repo filter, accessible tables)

Mode: parallel (2 web-search-backed subagents, one turn). Stages used: 1
sweep, no deepening round — both angles returned concrete,
non-conflicting, actionable guidance on the survey's open questions;
saturation reached immediately (see Judge point below). Angles aimed at
the survey's identified gaps: (a) how parallel-fetch/failure UX is done in
comparable ops dashboards (survey §1/§4 — timeout default, banner
collapsing), (b) accessible disclosure/filter/responsive-table patterns
(survey §2/§3/§5 — button-based row toggle, `<select>` filter, scroll vs.
mobile cards).

## Category must-bes

- Parallel dashboards (Grafana) render the page shell immediately and let
  each source's panel resolve independently rather than blocking on the
  slowest — no full-page spinner gating on every source.
- Status pages (GitHub) keep a tiered, always-visible severity summary;
  raw/verbose detail is what gets hidden, never the fact-of-failure count
  itself (GOV.UK error-summary pattern: summary line stays visible, only
  the log/traceback goes behind a fold).
- WAI-ARIA APG disclosure pattern: a real `<button>` with
  `aria-expanded`/`aria-controls` is the only correct trigger for
  expand/collapse, regardless of container.
- Accessible expandable table rows: the disclosure panel must be a real
  sibling `<tr><td colspan="N">` kept `display: table-row` (Adrian
  Roselli), not a `<div>` inserted elsewhere — preserves header/cell
  association for assistive tech and keeps the panel inside the same
  horizontally-scrolling container as the row it belongs to.
- Responsive data tables at this scale: a plain `overflow-x: auto` wrapper
  per table beats reflowing into a mobile card layout (Roselli,
  "Under-Engineered Responsive Tables") — no JS needed.

## Performance axes

- Failure surfacing: binary "show everything inline" vs. tiered
  (always-visible count + collapsed verbose detail) — the tiered pattern
  is what both GitHub's status page and GOV.UK's error-summary use.
- Disclosure placement: block-appended detail (anti-pattern, breaks table
  semantics) vs. same-row colspan `<tr>` (correct, AT-compatible) — this
  is the axis strong implementations visibly compete on; weak ones use the
  block-append shortcut.
- Responsive strategy: reflow-to-cards (heavier, a second layout to
  maintain) vs. scroll-container-only (lighter, one layout) — for a small
  internal tool the lighter axis wins per Roselli's explicit argument.

## Adopt / Skip

**Adopt**: page-shell-first + per-source resolve (parallel fetch already
matches this once `ThreadPoolExecutor` lands); always-visible "N of M
repos failed" line with per-repo detail inside `<details>` (matches the
issue's own explicit ask, and satisfies GOV.UK's "summary never fully
hidden" constraint since the count *is* the summary); `<button
aria-expanded aria-controls>` in the Issue cell, panel as a sibling
`colspan` `<tr>` on narrow screens; plain `overflow-x: auto` wrapper per
table, no sticky-column, no mobile card layout; no debounce on the
`<select>`'s `change` handler (MDN: `change` fires once per commit, not a
high-frequency event — debounce guidance targets `input`/`scroll`/`keydown`
class events only).

**Skip**: sticky first column (`position: sticky; left: 0`) — a real
CSS-Tricks-documented enhancement, but beyond what the issue's AC actually
asks for ("표별 가로 스크롤만 허용", not "pin the repo column"); adds
background-color edge-case handling the sources themselves flag. Dynamic
p99-based timeout tuning — no authoritative multiplier rule exists in the
literature searched (thin/generic results), and the issue already supplies
a real measured worst case (26.7s) to ground the default off of directly,
making generic heuristics unnecessary.

## Segment fit

`rsb` is a small internal ops dashboard for ~3-10 git repos, not a public
status page or a general-purpose data-grid product — the scout target was
UI/UX *pattern* (how to structure disclosure, filtering, scroll), not
feature parity with Grafana/GitHub's operational scale (alerting,
multi-tenant severity weighting, etc.), which stays out of scope by
category mismatch.

## Gap line

Current state already meets: nothing on the disclosure/filter/scroll
must-bes (survey confirms zero `<button>`-based disclosure, zero
`<select>`, zero `overflow-x` anywhere in `dashboard.css` today) — full
gap on all three UI must-bes, but the supporting primitives already exist
(`.badge`/status tokens, the `renderTable`/`attachRowClickHandlers`
structure to build the button-and-colspan-row version on top of, per
survey §5). On the failure-banner must-be, the gap is narrower: an
always-visible summary line already exists (`"{N} of {M} repos failed to
load"`), the only missing piece is moving the per-repo detail behind
`<details>` — a small, contained diff (survey §4), not new UI language.

## Judge point / saturation

Would another round change a build decision? No — the issue's own
requirements text already names the target shape for all five areas
(select filter, Repo-first columns, `N of M` banner, button-based row
disclosure); the sweep's job was confirming *how* to implement each
correctly (ARIA attributes, DOM placement, scroll strategy, timeout
grounding), not *whether* to — and both angles returned clear, mutually
reinforcing answers with no open disagreement to deepen on. Stopped after
stage 1.

Sources:
- https://community.grafana.com/t/beginner-needs-tool-to-help-himself-panel-with-no-data/86362
- https://github.com/grafana/grafana/issues/80171
- https://github.blog/news-insights/company-news/bringing-more-transparency-to-githubs-status-page/
- https://design-system.service.gov.uk/patterns/validation/
- https://design-system.service.gov.uk/components/error-message/
- https://www.nngroup.com/videos/progressive-disclosure/
- https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-card/
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-expanded
- http://adrianroselli.com/2019/09/table-with-expando-rows.html
- https://css-tricks.com/table-with-expando-rows/
- https://webaim.org/discussion/mail_thread?thread=10795
- https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/change_event
- https://developer.mozilla.org/en-US/docs/Web/API/Element/input_event
- https://css-tricks.com/a-table-with-both-a-sticky-header-and-a-sticky-first-column/
- https://adrianroselli.com/2020/11/under-engineered-responsive-tables.html
- http://adrianroselli.com/2017/11/a-responsive-accessible-table.html
