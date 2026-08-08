# Conformance-review scout brief (issue #56, phase 1)

Ran **parallel**, 2 stages of the 5 allowed, ~1 minute wall clock:
stage 1 swept four concurrent angles in one turn (WCAG 2.5.8 inline
exception; removal/dead-code audit practice; assertion-power and
mutation testing; requirements-traceability verdict machinery); stage 2
deepened on the single decision-relevant hit by fetching the W3C
primary source. Judge point 2 hit saturation — the fourth angle changed
no decision and was dropped rather than deepened, since this repo's
verdict vocabulary and severity bands are already fixed by house
convention. Angles were aimed at the survey's three named unknowns, not
at the issue text.

**Category must-bes (removal-class audits).** A removal is audited over
the whole repository, not over the deleted lines: search the entire
repo for references to the removed code and fix or remove every match,
and treat styles left behind for a deleted UI element as part of the
removal's unfinished work, not as harmless. [1][2][3]

**Category must-bes (regression-test audits).** A test's worth is
whether it *kills the mutant*: an assertion that holds on both correct
and mutated code is classed weak, because it states a property that a
buggy version also satisfies; passing on correct code is not evidence.
Mutation analysis is the named method for separating the two, and it
catches assertion gaps specifically, not just execution gaps. [4][5][6]

**Category must-bes (WCAG 2.5.8).** The Inline exception reads, in the
normative text: "The target is in a sentence or its size is otherwise
constrained by the line-height of non-target text." The Understanding
document extends it only to "links within a paragraph of text" and does
**not** state that a standalone link in a table cell or list item
qualifies. Size is judged as 24×24 CSS pixels on the target, with the
circle centered on the bounding box for non-rectangular shapes. [7]

**Performance axes the field competes on.** (i) Residue completeness —
code, styles, and documentation swept as one unit; (ii) assertion power
over assertion presence — can the new test actually fail; (iii)
measurement honesty — a claim about rendered geometry is either
measured or explicitly downgraded, never inferred silently.

**Adopt.** A dedicated sub-row asking whether the new test's assertion
would fail if `renderErrors` were restored (mutant-kill framing, axis
ii), and a residue row group sweeping code + CSS + spec for the removed
feature's leftovers (axis i). Both are cheap here: source-readable, no
rendering engine needed.

**Skip.** Coverage tooling (Lighthouse "reduce unused CSS", DevTools
coverage, PurifyCSS/UnCSS) — all need a live browser this environment
does not have, so adopting them would manufacture Unverifiable rows
instead of resolving them. Also skip RTM/ISO-25010 verdict machinery:
this repo already fixes a five-verdict vocabulary and four severity
bands, and a second scheme would fragment the record for no gain.

**Gap line.** Already met by the current state: per-requirement rows,
the five-verdict vocabulary, severity bands, evidence classes A/B/C,
and the "what would settle it" treatment of Unverifiable rows (issue-38
and issue-36 records). Missing: no prior record in this repo judges a
new test's *power* (only its presence and its result), and none sweeps
for residue after a removal — those two are exactly what this brief
adds, and they map onto the survey's unknowns 1 and 4.

**Segment fit.** The deliverable is an audit of a 6-file removal-plus-
sizing change, so the field scouted is audit practice, not product; the
exemplars set the bar for *what a strong audit of this change class
checks*, and the issue's own text still sets the requirement list.

Sources:
- [1] https://www.flowspark.co/blog/audit-and-clean-up-unused-css-javascript-in-webflow
- [2] https://dev.to/kui_luo/how-to-audit-your-css-for-unused-rules-and-reduce-load-time-by-60-4fbk
- [3] https://thalida.com/plans/post/code-quality/css-audit/2026-03-01-css-audit-implementation/
- [4] https://www.augmentcode.com/guides/mutation-testing-ai-generated-code
- [5] https://arxiv.org/pdf/2301.12284
- [6] https://testrigor.com/blog/understanding-mutation-testing-a-comprehensive-guide/
- [7] https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
