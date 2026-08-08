# issue-61 execution-observation — scout brief

Mode: **parallel**, genuine concurrent dispatch — stage 1 fired 4
`WebSearch` calls in one turn (one per survey §5 gap G1–G4); stage 2
fired 2 more in one turn on G1 and G3, the two the sweep answered only
generically. **2 stages total**, 03:50:02Z → ~03:54Z (`date -u` at the
survey/sweep boundary), inside the 5-stage / 3-min budget. Stopped at
judge point 2: no further round would change how this observation is
aimed. Field scouted = strong reviews of *this deliverable class* (a
two-phase self-approved change that stopped on scope-exceeded, merged
with a known-red mainline test, and closed the remainder in a second PR
under the same approval) — not the dashboard's own product domain.

## Category must-bes (what a strong review of this change class assumes)

- **An approval covers the diff it was given; new code after it is
  re-reviewed.** The mainstream mechanism is stale-review dismissal —
  approval is dismissed and re-approval required when the approved branch
  gains code-modifying commits, and OpenSSF names this as the default
  branch's baseline. Nothing in the sources extends an approval across a
  *separate later PR*; each PR is approved independently. [1][2]
- **The mainline is not knowingly left red.** Trunk-based practice treats
  the CI gate as the thing that never lets failing tests into trunk, and
  where a red main happens anyway, the expectation is an explicit, fast
  remediation (revert or a time-boxed fix-forward), not an open state. [3][4][5]
- **A fix-forward is legitimate when the cause is obvious and the window
  is short** — the field's framing is a small time box (minutes, not
  sessions) and a named owner, with revert as the default when the
  window would be exceeded. [5][6]
- **`aria-controls` must resolve, and its value must track state in real
  time**; APG requires the disclosure button's `aria-controls` to
  reference the id of the element holding the shown/hidden panel, ARIA ids
  must be unique in the document, and an `aria-controls` pointing at a
  removed or wrong element breaks the accessibility-tree relationship.
  Support is weak in screen readers, which lowers user-visible impact but
  does not remove the conformance expectation. [7][8][9][10]
- **Exact-literal assertions are a known brittleness class**: the field's
  remedy is loosening the assertion (pattern/structure), and "update the
  literal" is described as maintenance overhead that trains failures to
  read as noise, not as closing the class. [11][12]

## Performance axes this observation will be judged on

1. **Citation density** — every verdict-bearing sentence carries its own
   adjacent SHA / `file:line` / comment URL.
2. **Disclosure-vs-defect discipline** — a disclosed limit is adjudicated
   on the disclosure's adequacy, never rounded up to a defect or down to
   a non-event.
3. **Independence** — conclusions from produced artifacts only; nothing
   is re-run.

## Adopt / skip

- **Adopt** the approval-scope rule [1][2] as the yardstick for the
  later-entry route (survey row 10): the question becomes whether the
  second PR's content was inside what the human approved, and whether the
  record's own prescribed resolution path was followed or substituted.
- **Adopt** the red-main / time-boxed fix-forward rule [3][4][5][6] as the
  yardstick for survey row 9 — the window here is measurable (`3f06ba6`
  03:40:32Z → `d8082dc` 03:46:29Z, 5m57s).
- **Adopt** APG's "reference the id of the element that contains the
  panel" + real-time synchronization [7][10] for survey rows 7–8.
- **Skip** duplicate-`id` audit tooling framing [8][9] as a finding
  source: the delivery renders at most one `#detail-row` per the record's
  singleton argument, so uniqueness is a check surface, not an assumed
  violation.
- **Skip** merge-queue/branch-protection tooling recommendations [4] —
  process advice for a team CI setup, out of scope for observing one
  role's session.
- **Skip** snapshot-tooling advice (`--update`, ARIA snapshots) [11][12] —
  the repository has no snapshot harness; only the brittleness principle
  transfers.

## Gap line (what the current state already meets vs. misses)

Met already: the record discloses the red full suite in its own text
(`docs/issue-61/reports/implementation.md:111-128`) rather than hiding it,
and the remainder was closed within six minutes of the merge (§2 of the
survey) — both must-bes' *disclosure* halves. Missing / unknown: whether
the later entry's authorization is the approval it cites (survey row 10),
whether the `aria-controls` override survives a layout change with no
re-render (row 7), and whether the exact-literal class was closed or
merely re-pinned (row 18). Those three are what phase 2's checks aim at.

## Segment fit

Same segment: a small-diff, single-repo, doc-heavy change reviewed after
merge by a non-authoring role, in a repository whose only workflow is
`deploy-board.yml` (no CI test gate). Enterprise change-control ceremony
is one segment up and is borrowed only for its approval-scope rule.

Sources:
1. <https://best.openssf.org/SCM-BestPractices/github/repository/dismisses_stale_reviews.html>
2. <https://docs.github.com/articles/approving-a-pull-request-with-required-reviews>
3. <https://trunkbaseddevelopment.com/committing-straight-to-the-trunk/>
4. <https://blog.aspect.build/keeping-main-green>
5. <https://dev.to/kevincox/how-to-keep-your-master-branch-green-with-git-4o99>
6. <https://medium.com/@dingezzz/fix-forward-or-roll-back-making-the-right-call-in-software-development-df2c5e49764d>
7. <https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-card/>
8. <https://dequeuniversity.com/rules/axe/4.3/duplicate-id-aria>
9. <https://www.accessibilitychecker.org/wcag-guides/ensure-every-id-attribute-value-used-in-aria-and-in-labels-is-unique/>
10. <https://a11ysupport.io/tech/aria/aria-controls_attribute>
11. <https://webcrawlerapi.com/glossary/playwright/how-to-fix-playwright-brittle-exact-text-assertions>
12. <https://vitest.dev/guide/snapshot.html>
