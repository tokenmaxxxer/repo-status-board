# Current-state survey — issue #81

## Background/context

`docs/issue-72/reports/requirements-engineering.md` (landed) resolved
AC2's mobile-overflow item as three non-visual, structural/CSS-declaration
requirements (REQ-72-1..3), implemented against `src/rsb/web/dashboard.js`
and `dashboard.css`, verified in `test/rsb_tests/test_dashboard_dom.py`
(jsdom-tier: DOM-string and stylesheet-rule assertions, no layout
computation). That record explicitly named a residual gap it could not
close: a *different* future mobile-overflow regression — e.g. a new wide
element added inside `#main-content` whose intrinsic width the existing
`min-width: 0` override does not shrink — would not be caught, because
catching it requires real layout computation (browser rendering), which
jsdom cannot perform and which the requirements record's own scope
(범위 밖: 시각 회귀 제외) does not authorize. The record routed this
gap to "a future product decision" rather than resolving it — that
routing is this issue.

Repo-level facts checked directly, not carried over from #72:
- `rsb` (`repo-status-board`) is a single internal dashboard
  (`README.md`): "tokenmaxxxer 보드 레포들의 상황판" — a status board for
  the tokenmaxxxer team's own repos, not a customer-facing or
  multi-tenant product.
- No page-view, access-log, or analytics instrumentation exists anywhere
  under `src/` (checked via grep for `analytics|pageview|log_view|
  access_log` — zero hits). There is no recorded count of how often the
  dashboard is viewed, by whom, or how often a mobile viewport is used.
- Deployment is a single GitHub Actions workflow
  (`.github/workflows/deploy-board.yml`); no browser-automation /
  screenshot-diff tooling (Percy, Applitools, Playwright visual
  snapshots, etc.) is present in the repo today.
- `dashboard.js`/`dashboard.css`/`test_dashboard_dom.py` are 710/426/467
  lines respectively — a single small surface, not a multi-screen design
  system with a component reused across dozens of views.

## Problem stated without any solution attached (JTBD)

The issue text and the #72 record both name a candidate *technique*
(visual-regression / screenshot-diff) before stating the underlying job.
Restated in JTBD terms, fixed before any solution is named:

Job performer: whoever maintains `rsb`'s dashboard UI (currently the same
small set of contributors who fixed the P1-1 mobile-overflow defect in
#44/#72).

Job: be confident that a future code change has not reintroduced a layout
defect that makes the dashboard unusable on a mobile viewport, before
that defect reaches anyone viewing the board.

Circumstance: a change touches `dashboard.js`/`dashboard.css` (or adds
new content inside `#main-content`) through a mechanism REQ-72-1..3 do
not fingerprint — i.e., not the specific wrapper/CSS-declaration pattern
those three requirements assert on.

Desired outcome: the regression is caught by an automated check before
merge/deploy, at a cost (setup + ongoing maintenance + CI time)
proportionate to how often this failure mode actually occurs and how
much it costs when it reaches a viewer.

**Gap vs. the issue's framing**: the issue (and #72) already name the
candidate solution ("real-browser screenshot diff") as one of the two
options being decided between. The job itself is technique-agnostic —
"catch layout regressions structural checks miss, cheaply" — and could in
principle also be answered by e.g. a narrower structural fingerprint
expansion, not only full visual-regression tooling. This proposal treats
visual-regression as one candidate solution, not the job.

## Opportunity-solution tree placement

Outcome: `rsb` dashboard changes ship without reintroducing
mobile-layout defects that reach a viewer.

Opportunity: the specific gap REQ-72-1..3 leave open — layout
regressions introduced through a mechanism other than the fixed P1-1
pattern (new wide element, different override removed, etc.) are
undetectable by structural/jsdom-tier checks.

Candidate solutions (this proposal's comparison set): (a) adopt real
browser-based visual-regression coverage (screenshot diff) for the
dashboard's mobile viewport; (b) rely on structural checks (REQ-72-1..3)
plus the existing defect-report loop (someone notices, files an issue)
as sufficient at rsb's current usage scale.

Discriminating assumption test: whether the *rate and cost* of future
non-fingerprinted mobile-overflow regressions reaching a viewer exceeds
the fixed + ongoing cost of standing up and maintaining
browser-automation visual-regression infra for a single internal
dashboard with no such infra today.

## Scout: run (not skipped)

Neither skip condition applies (not a pure bugfix; the visual-regression
vs. structural-only choice is an open design decision). One sweep stage
run, single WebSearch call ("visual regression testing worth it small
internal tool vs structural DOM assertions tradeoff 2026") — parallel
fan-out was not warranted for a single well-scoped query; results and
sourcing captured in `scout-brief.md`. One judge point, no deepening
round needed (results directly answered the discriminating question with
no further ambiguity to snowball on) — saturation reached at stage 1.
Elapsed: <1min wall-clock, well under the 5-stage/3min budget.
