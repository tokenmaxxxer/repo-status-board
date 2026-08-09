---
proposal: docs/issue-81/proposals/product-discovery.md
---

# Hunt record — issue-81-product-discovery

## after-proposal — stance 2: assume this guard goes silent when its own input is malformed — find where that happens

Verdict: FINDING — the 90-day inconclusive fallback and the go/kill metric-counting mechanism both depend on human-run, unscheduled steps (adopting a `mobile-overflow` label, then someone manually checking issue counts after 90 days); nothing in the repo triggers, schedules, or checks this, so "no signal collected" is indistinguishable from "kill" verdict unless a human happens to notice.
Kind: silent-failure
Seed: docs/issue-81/proposals/product-discovery.md, docs/issue-81/reports/product-discovery/current-state.md, docs/issue-81/reports/product-discovery/scout-brief.md (~270 lines, docs-only)
cap_seconds: 180
tier: size:200+
diff_stat_lines: ~270
started_at: 2026-08-09T00:00:00Z
ended_at: 2026-08-09T00:05:00Z

### Reproduce
```
grep -rn "mobile-overflow" .github 2>/dev/null   # no label definition, no workflow
find . -iname "*.yml" -path "*workflows*" | xargs grep -l "label\|issue" 2>/dev/null   # no result
grep -n "Decision rule" -A5 docs/issue-81/proposals/product-discovery.md
```
The decision rule text (line 59) states: "verdict is pivot to inconclusive ... if the labeling convention below is never adopted and no count is collectible after 90 days." The "Missing-instrumentation routing" section (lines 80-88) says phase 2 "must first add" the `mobile-overflow` label before the clock "can run meaningfully" — but the label does not exist in `.github`, no CI/cron/scheduled job checks issue counts or elapsed days anywhere in the repo, and "How you'll know it worked" (lines 114-120) only says the phase-2 report is "written only after human approval" with no mechanism that fires that write.

### Observed
Silence (no label adopted, no count taken, 90 days pass with nobody looking) produces exactly the same repo state as a genuine "kill" verdict: no phase-2 report, structural checks unchanged, no visual-regression build. There is no artifact or alert distinguishing "we measured and it was below threshold" from "we never measured."

### Expected
A decision rule whose "inconclusive" branch is actually distinguishable from silent non-monitoring — e.g., a scheduled/tracked reminder or explicit owner/date for the 90-day check — rather than relying on the phase-2 author to remember and no automation to detect either the label's absence or the elapsed window.

Citation check: docs/issue-72/reports/requirements-engineering.md exists and does support the proposal's characterization (mobile-overflow named as a gap the visual-regression exclusion conflicts with, explicitly routed to "the issue author" rather than resolved) — this part of the stance did not yield a finding.
