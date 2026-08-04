# issue-36 current-state survey

## 1. where the ↗ icon and the row-toggle button live today

`externalLinkHtml(ownerName, kind, number, label)` (`dashboard.js:219-223`,
added by issue #34) renders `<a class="external-link" ...
target="_blank" rel="noopener noreferrer"><span
aria-hidden="true">↗</span></a>` — this whole function plus its CSS rule
(`.external-link`, `dashboard.css:176-188`) is what requirement 3 removes.

`issueToggleCell(sourceTable, issue, repo, ownerName)` (`dashboard.js:225-229`)
is the single shared helper behind all four tables' Issue cell: it
concatenates the existing `<button class="row-toggle" aria-expanded
aria-controls data-issue data-repo data-table>${issue}</button>` with
`externalLinkHtml(...)` as a trailing sibling. Because the issue *number*
is the button's own visible/accessible-name content
(`>${issue}</button>`), turning that number into an `<a href>` cannot
reuse the button element — confirms the issue body's own framing:
number-as-link and number-as-button-label are mutually exclusive on the
same text node, so the disclosure trigger genuinely has to move
somewhere else in the cell, not just get a new class.

`prCellHtml(ownerName, prNumbers)` (`dashboard.js:234-239`) is the PR-cell
counterpart — plain `<span class="mono">${prNumber}${externalLinkHtml(...)}</span>`
per PR number, joined with `", "`. No `row-toggle` here — PR cells have
no disclosure control to relocate, so requirement 1/3 apply to PR cells
with no requirement-4 complication.

## 2. the detail-panel trigger's actual wiring has two pre-existing gaps

Read end-to-end (`dashboard.js:190-202`, `412-465`, `533-535`) rather
than trusting the comments describing it:

- **`attachRowClickHandlers` (`dashboard.js:458-465`) is the only click
  listener involved** — it binds to every `tr[data-issue]`, not to
  `.row-toggle` itself. `row-toggle` clicks only work because the click
  event bubbles up from the button to the row. The handler sets
  `selectedIssue = { issue, repo }` — **it never reads `data-table`**, so
  `selectedIssue.sourceTable` is always `undefined`.
- `isRowExpanded(sourceTable, issue, repo)` (`dashboard.js:195-202`)
  checks `selectedIssue.sourceTable === sourceTable`. Since
  `selectedIssue.sourceTable` is always `undefined` and `sourceTable` is
  always one of the four literal table names, this comparison is always
  `false` — **`aria-expanded` on every `row-toggle` button always
  renders `"false"`**, even for the row currently shown in the detail
  panel.
- `rowToggleId(sourceTable, repo, issue)` (`dashboard.js:190-193`) builds
  an `aria-controls` value like `detail-row-decisions-<repo>-42`. No
  element with that id is ever created anywhere in `dashboard.js` —
  `grep -n "insertDetailRow"` matches only two *comments*
  (`dashboard.js:15,187`) that describe a function that does not exist.
  The only rendered detail container is `DETAIL_SLOT`
  (`id="detail-panel-slot"`, `index.html:25`), used unconditionally
  regardless of viewport width (`renderData`, `dashboard.js:533`:
  `DETAIL_SLOT.innerHTML = selectedIssue ? renderDetailPanel(...) : ""`).
  **`aria-controls` on every `row-toggle` button points at an id that
  does not exist in the DOM.**
- `dashboard.css:190-196`'s `.detail-row` rule and the narrow-layout
  "expandable row" behavior documented in `screen-spec.md` §1.6
  (`"expandable row below breakpoint-lg"`, confirmed also in
  `design-system.md` §5 breakpoint table) describe a second, per-table
  inline rendering path that has no corresponding JS. Only the
  side-panel/`DETAIL_SLOT` path is actually implemented; the CSS layout
  switch (`dashboard.css:287-293`, `@media (min-width: 1200px)`) only
  changes whether `DETAIL_SLOT` renders as a sticky side column or a
  block below `MAIN` — it never triggers a different render function.

None of this is caused by issue-36; it predates this issue (issue #34's
own scout-brief asserted "correct `aria-expanded`/`aria-controls`
wiring" as already-met current state — that assertion is not accurate on
inspection). It is directly relevant here because requirement 4 requires
rewriting exactly the functions carrying these gaps
(`issueToggleCell`, `isRowExpanded`, `rowToggleId`,
`attachRowClickHandlers`) to relocate the trigger — the proposal has to
decide whether to reproduce the gaps as-is or correct them in the same
edit (see proposal Rationale).

## 3. styling/tokens available, no new ones needed

`dashboard.css:9,23-24`: `--color-blue-500: #2563eb` →
`--color-action-primary-background`. `design-system.md:61` already
documents this token's use as covering "refresh button, links" —
requirement 2 needs no new token, just a new selector applying an
existing one as the link's resting-state color (today
`.external-link`'s only blue state is hover/focus, `dashboard.css:181-187`
— for issue-36 the link must be blue at rest, not only on
hover/focus, which is a materially different rule, not a rename of the
existing one).

`.row-toggle` (`dashboard.css:159-171`) currently strips button chrome
and inherits table typography so its text (the bare issue number) reads
like a plain cell; it will need a different treatment once it holds only
a glyph.

## 4. line-wrap defect named in the issue is reproducible from the CSS alone

`.table-scroll` (`dashboard.css:154`) gives each table independent
horizontal scroll, but nothing forces the button+icon pair inside a
single Issue cell onto one line — `<td class="mono">` has no
`white-space: nowrap` or inline-flex wrapper, so `42↗` can break between
the button and the icon whenever the Flows table's Issue column is
narrower than both pieces combined. Confirms the issue body's own
observation (Flows wraps, Decision queue's wider column does not) is a
layout-width symptom, not a markup-order symptom — the fix needs an
explicit no-wrap container around whatever ends up in the cell, not just
different content.

## 5. spec documents to update (requirement 6)

- `docs/specs/design-system.md`: §5 breakpoint table already asserts the
  expandable-row narrow-layout behavior that §2 (gap above) shows isn't
  implemented — pre-existing inaccuracy, not introduced here, but
  touching this row is in scope only if the proposal's relocation choice
  changes what's true about it. §6 component inventory's `DetailPanel`
  row and any row-toggle-adjacent wording.
- `docs/specs/screen-spec.md`: §1.3/§1.4 "Issue-cell button click opens
  `DetailPanel`" wording (currently describes the button as holding the
  issue number); §1.3 lists `PR` as a plain column, needs the same `#<n>`
  link note as Issue.

## 6. test surface

`test/rsb_tests/test_model.py:155-171` documents and uses the only JS
test harness in this repo: shelling out to a plain `node` binary against
the *shipped* `dashboard.js` (via its `module.exports` guard,
`dashboard.js:567-569` — currently exports `ageBucket`,
`ageBucketStatus`, `selectSummary`, `isPageEmpty`, `buildPlanSteps`,
`filterByRepo`, `buildGithubUrl`, `externalLinkHtml`). No package.json,
no JS framework, no new dependency — issue #23's approved phase-1
proposal explicitly ruled this out, still true (`find . -name
package.json` → no matches outside caches). Any new pure helper this
issue adds should follow the same `module.exports` convention to get
`node -e` coverage in `test_model.py`, matching `buildGithubUrl`/
`externalLinkHtml`'s own precedent. `render.py` (CLI text renderer) has
no link/button concept at all — out of scope, same as issue #34.

## 7. approvers

`docs/specs/approvers.md`: `JiwonJung94`, `jjongkwann` (unchanged since
issue #34).

## gaps this survey leaves for scout to aim at

- Where exactly the relocated disclosure trigger should sit relative to
  the new link (leading vs. trailing, own column vs. same cell) — the
  issue body gives an example ("행 앞/뒤의 별도 disclosure 버튼") but
  explicitly leaves the choice open.
- What glyph/accessible-name convention a relocated, icon-only disclosure
  button should use (distinct question from issue #34's external-link
  icon convention — that scout covered *link* icons next to a button
  that still held the number; this issue is the reverse shape).
- Whether real-world/standards precedent favors fixing the aria-expanded/
  aria-controls gaps (§2) in the same edit, given the trigger's markup is
  being rewritten regardless.
