# Scout brief (issue #62, execution-observation phase 1)

Stages used: 1 sweep round, 4 angles, genuinely concurrent dispatch
(4 `Agent` calls in one message, foreground per contract v3 s22 — no
batched-sequential fallback). Wall-clock ≈70s. Angles were aimed at
survey §5's four method unknowns, not at the issue text. Judge point
after round 1: every angle returned a named, sourced criterion directly
usable by the verdict plan; a second round would not change any check in
the proposal — stopped at 1 stage, well inside the 5-stage / 3-min cap.

## Angle 1 — post-approval mechanism change (survey §5.1, aimed at T-d)

Must-be: an approval is granted on a *procedure*, not only an end-state
— when the change can no longer be implemented by the approved
procedure, the conditions the approval rested on no longer hold and it
needs re-review [1]. Change-control scope explicitly covers process and
design alterations, not just outcomes [2]. Self-detection is a real,
named mitigating factor (voluntary self-disclosure credit) [3], not a
neutralizer.
Adopt: the standard-change-conditions test [1] as the criterion for T-d
— ask whether the approved item's *procedure* survived, and weigh
pre-landing self-detection [3] as mitigation of severity, never as
erasure of the deviation.
Skip: the SOX drift lens ("unauthorized change = finding") [4] as the
primary frame — built for undetected production drift, it would score a
pre-landing self-caught correction the same as an unnoticed one.
Assumption (unsourced, labeled): that self-detection also evidences an
under-specified original approval — no source found; not used as a
criterion.

## Angle 2 — author-attested-only evidence (survey §5.2, aimed at O-d/O-e)

Must-be: evidence reliability is hierarchical — direct observation >
external > internal > attestation [5]; written representations are
required but explicitly cannot substitute for other procedures [6]; when
no alternative procedure can corroborate a material claim, the reviewer
records a scope limitation rather than treating the claim as confirmed
[7][8].
Adopt: label every uncommitted test-run claim "attested, uncorroborated"
and carry it as a declared scope limitation of this observation.
Skip: upgrading a claim to "verified" because it is specific (exact
pass/fail counts) — specificity is not corroboration [9].

## Angle 3 — best-effort redaction (survey §5.3, aimed at S-a)

Must-be: denylist-shaped filters fail by unenumerated variants, so
reviewers are expected to enumerate residual bypass classes rather than
accept pass/fail on the reported case [10][11]; CWE-209's own remedy is
not-emitting over after-the-fact scrubbing [12]; the reference
implementation for this exact problem (Sentry's scrubber) documents its
known-uncaught cases instead of claiming completeness [13]; the Grav
denylist advisory is the canonical "handled the reported case, defeated
by the unconsidered variant" precedent [14].
Adopt: enumerate residual classes and check whether the *claim's wording*
is scoped to what the mechanism guarantees.
Skip: demanding a fix as the only acceptable resolution — sources support
scope-the-claim/document-the-limit as a legitimate alternative [13].

## Angle 4 — assertion tightness + jsdom limits (survey §5.4, aimed at S-b/S-c)

Must-be: pinning an assertion to an incidental exact value where the
contract states a minimum is the over-specification / eager-test smell
[15][16], and constraints should be as loose as confidence allows [17];
jsdom performs no layout and returns dummy values for layout-derived
properties, so `getComputedStyle` there is evidence of *declared/cascaded*
CSS only [18]; real WCAG 2.5.8 target-size checking (axe-core's
`target-size`) needs rendered geometry [19][20].
Adopt: judge the exact-equality assertion on the over-specification
criterion, and judge the jsdom evidence on the declared-vs-rendered
distinction — including whether the record's own framing states it.
Skip: treating "no browser in the sandbox" as automatically discharging
the requirement — the question is whether the substitution was declared,
not whether it was necessary.

## Gap line

Scoped to *this observation plan's* own current state, i.e. what survey
§4–§5 had before this brief — the gap line says nothing about the
observed role's artifacts, which only phase 2 may characterize. Already
met by the plan: a named target artifact per check surface, and the
no-re-execution rule inherited from the role directive. Missing before
this brief, and supplied by it: a named criterion for T-d (angle 1's
approved-procedure test), an evidence-grade label for uncommitted test
runs (angle 2's "attested, uncorroborated" + scope limitation), a
residual-class enumeration duty plus the claim-scoping question for S-a
(angle 3), and the over-specification and declared-vs-rendered
distinctions for S-b/S-c (angle 4). Each is written into the proposal's
admissibility rules and check list as a question, not as an answer.

## Segment fit

The deliverable's kind is an execution audit of one merged PR on an
internal ops tool — the bar is a defensible, cited three-level verdict,
not a compliance program. Every adopted criterion above is the plainest
one its sources support; the heavier regulatory frames (SOX drift,
sanction-severity scoring) were explicitly skipped as mis-segmented.

Sources:
[1] https://www.itilfromexperience.com/When+is+a+standard+change+no+longer+a+standard+change
[2] https://link.springer.com/chapter/10.1007/978-981-99-9271-3_13
[3] https://ofac.treasury.gov/faqs/13
[4] https://www.linfordco.com/blog/change-control-management/
[5] https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105
[6] https://pcaobus.org/oversight/standards/auditing-standards/details/AS2805
[7] https://pcaobus.org/oversight/standards/auditing-standards/details/AS3105
[8] https://en.wikipedia.org/wiki/Scope_limitation
[9] https://methodology.eca.europa.eu/aware/GAP/Pages/Audit-evidence.aspx
[10] https://top10proactive.owasp.org/the-top-10/c3-validate-input-and-handle-exceptions/
[11] https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
[12] https://cwe.mitre.org/data/definitions/209.html
[13] https://docs.sentry.io/platforms/python/guides/rq/data-management/sensitive-data/
[14] https://github.com/getgrav/grav/security/advisories/GHSA-j3v8-v77f-fvgm
[15] https://qaskills.sh/blog/test-smells-anti-patterns-guide-2026
[16] https://arxiv.org/pdf/2303.04234
[17] https://samhogy.co.uk/2021/04/making-the-most-of-contract-testing/
[18] https://github.com/jsdom/jsdom/blob/main/README.md
[19] https://www.deque.com/blog/axe-core-4-5-first-wcag-2-2-support-and-more/
[20] https://testparty.ai/blog/wcag-target-size-guide
