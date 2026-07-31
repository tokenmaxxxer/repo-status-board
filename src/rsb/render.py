"""Renders a BoardModel into the single-screen plain-text layout (proposal §5)."""

import dataclasses
import os
import shutil

CLEAR_SCREEN = "\x1b[2J\x1b[H"


def _term_width():
    try:
        return shutil.get_terminal_size(fallback=(100, 24)).columns
    except OSError:
        return 100


def _fit(text, width):
    if width <= 0 or len(text) <= width:
        return text
    if width <= 1:
        return text[:width]
    return text[: width - 1] + "…"


def _fmt_row(cells, widths):
    return "  ".join(str(c).ljust(w) for c, w in zip(cells, widths))


def _table(headers, rows, width):
    if not rows:
        return "  (none)"
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    lines = ["  " + _fmt_row(headers, widths)]
    for row in rows:
        lines.append("  " + _fit(_fmt_row(row, widths), max(width - 2, 10)))
    return "\n".join(lines)


def _fmt_roles(roles):
    return " ".join(f"{r.role}:{r.loop_state}" for r in roles)


def _fmt_prs(prs):
    return ",".join(str(p) for p in prs) if prs else "-"


def _fmt_last_activity(la):
    if la is None:
        return "—"
    ts = la.ts.split("T")[-1].rstrip("Z") if "T" in la.ts else la.ts
    return _fit(f"{ts} {la.kind}: {la.detail}", 80)


def _fmt_outcomes(outcomes):
    if not outcomes:
        return "(none)"
    return " ".join(f"{k}:{v}" for k, v in sorted(outcomes.items()))


def render_text(model, generated_at):
    width = _term_width()
    repo_count = len(model.generated_at_by_repo) + len(model.errors)
    error_count = len(model.errors)
    lines = []
    header = f"rsb — {generated_at} — {repo_count} repos, {error_count} error"
    header += "" if error_count == 1 else "s"
    lines.append(header)
    lines.append("═" * min(width, 80))

    lines.append(f"DECISION QUEUE  ({len(model.decisions)} awaiting)")
    lines.append(
        _table(
            ["issue", "pr", "phase", "role", "age", "awaiting", "repo"],
            [
                [d.issue, d.pr, d.phase, d.role, f"{d.age_hours:.1f}h", d.awaiting, d.repo]
                for d in model.decisions
            ],
            width,
        )
    )
    lines.append("─" * min(width, 80))

    lines.append("FLOWS")
    lines.append(
        _table(
            ["issue", "stage", "roles", "prs", "repo"],
            [
                [
                    f.issue,
                    f.stage if f.stage_derived else f"{f.stage} (raw)",
                    _fmt_roles(f.roles),
                    _fmt_prs(f.prs),
                    f.repo,
                ]
                for f in model.flows
            ],
            width,
        )
    )
    lines.append("─" * min(width, 80))

    lines.append("SESSIONS")
    lines.append(
        _table(
            ["role", "issue", "elapsed", "alive", "verdict", "last activity", "repo"],
            [
                [
                    s.role,
                    s.issue,
                    f"{s.elapsed_min:.1f}m",
                    "yes" if s.alive else "no",
                    s.verdict,
                    _fmt_last_activity(s.last_activity),
                    s.repo,
                ]
                for s in model.sessions
            ],
            width,
        )
    )
    lines.append("─" * min(width, 80))

    lines.append("ACCOUNTING")
    accounting_rows = [
        [le.issue, le.sessions, f"{le.cost_usd_total:.2f}", _fmt_outcomes(le.outcomes), le.repo]
        for le in model.ledger
    ]
    lines.append(_table(["issue", "sessions", "cost_usd", "outcomes", "repo"], accounting_rows, width))
    for u in model.unattributed:
        lines.append(f"  (unattributed: {u.sessions} sessions, ${u.cost_usd_total:.2f} — {u.repo})")
    lines.append("─" * min(width, 80))

    lines.append("HYGIENE")
    hygiene_lines = []
    for v in model.closure_sweep:
        raw = v.raw
        issue = raw.get("issue", "?")
        violation = raw.get("violation", "?")
        detail = raw.get("detail", "")
        hygiene_lines.append(f"  [closure-sweep] issue {issue}: {violation} — {detail} — {v.repo}")
    for u in model.unapproved_open_prs:
        hygiene_lines.append(
            f"  [unapproved-pr] issue {u.issue} pr {u.pr} ({u.role}, opened {u.opened_at}) — {u.repo}"
        )
    lines.append("\n".join(hygiene_lines) if hygiene_lines else "  (none)")

    if model.errors:
        lines.append("─" * min(width, 80))
        lines.append("ERRORS")
        for e in model.errors:
            lines.append(f"  {e.repo}: {e.message}")

    return "\n".join(lines) + "\n"


def _dataclass_to_dict(obj):
    if dataclasses.is_dataclass(obj):
        return {k: _dataclass_to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, list):
        return [_dataclass_to_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    return obj


def render_json_model(model, generated_at):
    """Normalized merged model as a JSON-serializable dict (proposal §4, §8)."""
    return {
        "generated_at": generated_at,
        "generated_at_by_repo": model.generated_at_by_repo,
        "decisions": _dataclass_to_dict(model.decisions),
        "flows": _dataclass_to_dict(model.flows),
        "sessions": _dataclass_to_dict(model.sessions),
        "ledger": _dataclass_to_dict(model.ledger),
        "unattributed": _dataclass_to_dict(model.unattributed),
        "closure_sweep": _dataclass_to_dict(model.closure_sweep),
        "unapproved_open_prs": _dataclass_to_dict(model.unapproved_open_prs),
        "errors": _dataclass_to_dict(model.errors),
    }
