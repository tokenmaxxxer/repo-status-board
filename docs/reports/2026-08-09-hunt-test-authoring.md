---
proposal: docs/issue-78/proposals/test-authoring.md
---

# Hunt record — test-authoring

## after-proposal — stance 1: assume this change and another plugin's rule cancel each other — find the pair

Verdict: FINDING — the core scout plugin's mandatory "skip record must live in the phase-1 survey" rule is silently cancelled by the adr-proposal-shape gate, which only checks that survey.md *exists* on disk, never that it contains the skip record scout requires — so a proposal can (and here does) declare a scout skip in the proposal file while the survey the rule actually targets has no such record, and no gate catches it.
Kind: composition
Seed: docs/issue-78/proposals/test-authoring.md, docs/issue-78/reports/test-authoring/survey.md (commit 04ee746, docs-only, 210 insertions)
cap_seconds: 180
tier: size:200+
diff_stat_lines: 210
started_at: 2026-08-09T00:00:00Z
ended_at: 2026-08-09T00:09:00Z

### Reproduce
```
# Core scout directive's own text (injected via UserPromptSubmit hook):
grep -n "SKIP RECORD" "/home/jwjung/.claude/plugins/marketplaces/tokenmaxxxer/runs/rulebooks/tokenmaxxxer-core/scout/hooks/directive.sh"
# => "SKIP RECORD (mandatory when skipped): if either skip condition applies,
#     the phase-1 survey MUST record the skip and its one-line reason ...
#     No skip record means scouting was not properly skipped — go back and
#     either scout or write the record."

# Where the skip is actually recorded for issue-78:
grep -n -i "skip" docs/issue-78/proposals/test-authoring.md
# => "Scout: **skipped**. Skip condition 2 applies ..." (lives in the PROPOSAL)

grep -n -i "skip" docs/issue-78/reports/test-authoring/survey.md
# => only "`pytest.skip` guards for missing `node` / ..." — an unrelated
#    mention of the pytest API, not a scout-skip record.

# The gate that runs on the proposal write and is supposed to enforce
# phase-1 shape checks only survey.md's existence, never its content:
grep -n "survey_path\|isfile" "/home/jwjung/.claude/plugins/marketplaces/tokenmaxxxer/runs/rulebooks/tokenmaxxxer-test-authoring/adr-proposal-shape/hooks/proposal-shape-gate.sh"
```

### Observed
The scout plugin's rule ("phase-1 survey MUST record the skip") and the
adr-proposal-shape gate's rule ("survey.md must already exist on disk")
compose into a check that passes even when the mandated content is
completely absent from survey.md: `docs/issue-78/reports/test-authoring/survey.md`
exists (satisfying adr-proposal-shape) but contains zero mention of the
scout skip decision or "Skip condition 2" — the skip rationale instead
sits in `docs/issue-78/proposals/test-authoring.md` under "Adopted
methodology", a file/section the scout rule never names. Nothing in the
plugin set flags this: adr-proposal-shape's Python judge (`proposal-shape-gate.sh`)
only calls `os.path.isfile(survey_path)`, never inspects survey.md's text,
so the existence check silently satisfies the requirement's letter while
cancelling its substance.

### Expected
Per the scout directive, "No skip record means scouting was not properly
skipped — go back and either scout or write the record" — i.e. either the
proposal write should have been refused/flagged until the skip record was
present in survey.md, or the adr-proposal-shape gate (the only automated
check that runs at proposal-write time) should validate survey.md's
content for the mandated skip record, not merely the file's existence.

## before-landing — stance 1: assume this change and another plugin's rule cancel each other — find the pair

Verdict: NO FINDING
Seed: test/rsb_tests/test_dashboard_dom.py new REQ-72-1..3 tests (+85 lines)
cap_seconds: 120
tier: default
diff_stat_lines: 85
started_at: 2026-08-09T00:00:00Z
ended_at: 2026-08-09T00:05:00Z

Checked whether the new CSSOM rule-lookup tests (sheet.cssRules.find(r => r.selectorText === ...))
violate the "not a whole-file substring search" constraint stated in the
REQ-72 requirements record, or collide with any other repo-wide gate
(searched for conftest.py, CI configs, lint scripts referencing
test_dashboard_dom.py, cssRules, or styleSheets -- none exist). The
selectors used (.table-scroll, #main-content plus #detail-panel-slot) match
src/rsb/web/dashboard.css exactly (lines 219, 412-413), and the two rule-
lookup tests correctly pass html=_dashboard_html_with_css() so styleSheets
is populated. Ran `python3 -m pytest test/rsb_tests/test_dashboard_dom.py -k req_72 -q`
-- all 3 pass. No sibling rule or plugin was found that this change silently
cancels.
