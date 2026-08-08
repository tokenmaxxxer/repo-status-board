---
proposal: docs/issue-72/proposals/requirements-engineering.md
---

# Hunt record — requirements-engineering

## after-proposal — stance 0: assume the gate/decision just made in this proposal is bypassable or wrong — find the bypass/flaw.

Verdict: FINDING — the proposed "structural/CSS-declaration assertion" is specified as checking that dashboard.css merely *contains* the strings `min-width: 0` and `overflow-x: auto`, not that those declarations are bound to the correct selectors (`#main-content`/`#detail-panel-slot` and `.table-scroll`); a naive/plain-text implementation of that check (which is exactly what the proposal recommends to stay jsdom-compatible) can pass while the actual mobile-overflow defect is reintroduced.
Kind: design-error
Seed: docs/issue-72/proposals/requirements-engineering.md lines 35-53, 91-97 (the recommended jsdom-compatible resolution: "assert ... dashboard.css declares min-width: 0 on #main-content/#detail-panel-slot and overflow-x: auto on .table-scroll")
cap_seconds: 60
tier: default
diff_stat_lines: 264 insertions, 3 files, docs/issue-72/ only
started_at: 2026-08-09T00:00:00Z
ended_at: 2026-08-09T00:02:30Z

### Reproduce
Take the actual current CSS that fixes the regression:
```
#main-content, #detail-panel-slot {
  min-width: 0;
}
```
(src/rsb/web/dashboard.css:412-414). Now simulate a future regression that the proposal's assertion is meant to catch: move the identical property/value text onto an unrelated, ineffective selector, e.g.
```
.unused-decoy {
  min-width: 0;
}
```
while leaving `#main-content`/`#detail-panel-slot` with no min-width override at all (the real, page-overflowing bug the proposal says AC2's 4th item exists to prevent). A test implemented per the proposal's own description — "assert ... dashboard.css declares min-width: 0" via `fs.readFileSync('dashboard.css', 'utf8').includes('min-width: 0')` (or an equivalent regex not scoped to the selector) — still returns true:
```
node -e "const css=require('fs').readFileSync('src/rsb/web/dashboard.css','utf8').replace('#main-content, #detail-panel-slot {\n  min-width: 0;\n}','.unused-decoy {\n  min-width: 0;\n}'); console.log(css.includes('min-width: 0'))"
```

### Observed
The substring/plain-text check the proposal describes as "achievable today" (line 105) evaluates to `true` even when the declaration has been moved off `#main-content`/`#detail-panel-slot` onto a selector that never matches any rendered element, i.e. the real horizontal-overflow bug (grid item's min-content inflating #page-body, per the code comment at dashboard.css:409-411) is fully present again.

### Expected
A test intended to stand in for the excluded visual-regression check should fail whenever the declaration is not bound to the selector(s) the fix actually depends on (`#main-content`, `#detail-panel-slot`, `.table-scroll`) — e.g. by parsing the stylesheet into rules and checking the declaration block for the specific selector, not by testing for the bare presence of the property/value text anywhere in the file. The proposal never specifies selector-scoped parsing; as written it leaves room for an assertion that is trivially satisfiable without the underlying layout fix being present.

## before-landing — docs-only fast path

No before-landing dispatch. Reason: docs-only, no before-landing dispatch —
the phase-2 transition (`be02a70`/proposal commit → `a5a16b9`) touches only
`docs/issue-72/reports/requirements-engineering.md` (140 insertions, 1
file, all under `docs/`). Stance-0's after-proposal finding (selector-
scoping bypass) was folded into REQ-72-2 and REQ-72-3's `verification_method`
and Given/When/Then lines in the landed record before this commit.
