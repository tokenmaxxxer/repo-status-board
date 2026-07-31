"""Typed in-memory records normalized from `flows --json` payloads.

Only `schema_version == SUPPORTED_SCHEMA_VERSION` is accepted; a mismatch is
a per-repo error, not a crash (see proposal §4).
"""

from dataclasses import dataclass, field

SUPPORTED_SCHEMA_VERSION = 1


@dataclass
class Decision:
    repo: str
    issue: int
    pr: int
    phase: int
    role: str
    opened_at: str
    age_hours: float
    awaiting: str


@dataclass
class FlowRole:
    role: str
    loop_state: str
    verdict: str


@dataclass
class Flow:
    repo: str
    issue: int
    stage: str
    stage_derived: bool
    roles: list
    prs: list


@dataclass
class LastActivity:
    ts: str
    kind: str
    detail: str


@dataclass
class Session:
    repo: str
    role: str
    issue: int
    elapsed_min: float
    pid: int
    alive: bool
    verdict: str
    last_activity: object


@dataclass
class LedgerEntry:
    repo: str
    issue: int
    sessions: int
    cost_usd_total: float
    outcomes: dict


@dataclass
class Unattributed:
    repo: str
    sessions: int
    cost_usd_total: float


@dataclass
class HygieneClosureViolation:
    repo: str
    raw: dict


@dataclass
class HygieneUnapprovedPr:
    repo: str
    issue: int
    pr: int
    role: str
    opened_at: str


@dataclass
class RepoError:
    repo: str
    message: str


@dataclass
class BoardModel:
    """Merged model across all successfully-fetched repos."""

    generated_at_by_repo: dict = field(default_factory=dict)
    decisions: list = field(default_factory=list)
    flows: list = field(default_factory=list)
    sessions: list = field(default_factory=list)
    ledger: list = field(default_factory=list)
    unattributed: list = field(default_factory=list)
    closure_sweep: list = field(default_factory=list)
    unapproved_open_prs: list = field(default_factory=list)
    errors: list = field(default_factory=list)


class PayloadError(Exception):
    """Raised when a single repo's payload cannot be normalized."""


def normalize_payload(repo_name, payload):
    """Convert one repo's raw `flows --json` payload into typed records.

    Raises PayloadError on schema_version mismatch or a structurally
    malformed payload; callers turn that into a per-repo RepoError instead
    of failing the whole run.
    """
    schema_version = payload.get("schema_version")
    if schema_version != SUPPORTED_SCHEMA_VERSION:
        raise PayloadError(
            f"unsupported schema_version={schema_version!r} (rsb supports {SUPPORTED_SCHEMA_VERSION})"
        )

    try:
        decisions = [
            Decision(
                repo=repo_name,
                issue=d["issue"],
                pr=d["pr"],
                phase=d["phase"],
                role=d["role"],
                opened_at=d["opened_at"],
                age_hours=d["age_hours"],
                awaiting=d["awaiting"],
            )
            for d in payload.get("decision_queue", [])
        ]

        flows = [
            Flow(
                repo=repo_name,
                issue=fl["issue"],
                stage=fl["stage"],
                stage_derived=fl["stage_derived"],
                roles=[
                    FlowRole(role=r["role"], loop_state=r["loop_state"], verdict=r["verdict"])
                    for r in fl.get("roles", [])
                ],
                prs=list(fl.get("prs", [])),
            )
            for fl in payload.get("flows", [])
        ]

        sessions = [
            Session(
                repo=repo_name,
                role=s["role"],
                issue=s["issue"],
                elapsed_min=s["elapsed_min"],
                pid=s["pid"],
                alive=s["alive"],
                verdict=s["verdict"],
                last_activity=(
                    LastActivity(
                        ts=s["last_activity"]["ts"],
                        kind=s["last_activity"]["kind"],
                        detail=s["last_activity"]["detail"],
                    )
                    if s.get("last_activity")
                    else None
                ),
            )
            for s in payload.get("sessions", [])
        ]

        ledger = [
            LedgerEntry(
                repo=repo_name,
                issue=le["issue"],
                sessions=le["sessions"],
                cost_usd_total=le["cost_usd_total"],
                outcomes=dict(le.get("outcomes", {})),
            )
            for le in payload.get("ledger", [])
        ]

        unattributed_raw = payload.get("unattributed")
        unattributed = (
            [
                Unattributed(
                    repo=repo_name,
                    sessions=unattributed_raw["sessions"],
                    cost_usd_total=unattributed_raw["cost_usd_total"],
                )
            ]
            if unattributed_raw
            else []
        )

        hygiene = payload.get("hygiene", {}) or {}
        closure_sweep = [
            HygieneClosureViolation(repo=repo_name, raw=v) for v in hygiene.get("closure_sweep", [])
        ]
        unapproved_open_prs = [
            HygieneUnapprovedPr(
                repo=repo_name,
                issue=u["issue"],
                pr=u["pr"],
                role=u["role"],
                opened_at=u["opened_at"],
            )
            for u in hygiene.get("unapproved_open_prs", [])
        ]
    except (KeyError, TypeError) as e:
        raise PayloadError(f"malformed payload: missing/invalid field {e}") from e

    generated_at = payload.get("generated_at")

    return {
        "generated_at": generated_at,
        "decisions": decisions,
        "flows": flows,
        "sessions": sessions,
        "ledger": ledger,
        "unattributed": unattributed,
        "closure_sweep": closure_sweep,
        "unapproved_open_prs": unapproved_open_prs,
    }


def merge_repos(per_repo_results):
    """Merge normalized per-repo records (or errors) into one BoardModel.

    `per_repo_results` is an iterable of (repo_name, normalized_dict_or_None,
    error_message_or_None) tuples, one per fetched repo.
    """
    model = BoardModel()
    for repo_name, normalized, error_message in per_repo_results:
        if error_message is not None:
            model.errors.append(RepoError(repo=repo_name, message=error_message))
            continue
        model.generated_at_by_repo[repo_name] = normalized["generated_at"]
        model.decisions.extend(normalized["decisions"])
        model.flows.extend(normalized["flows"])
        model.sessions.extend(normalized["sessions"])
        model.ledger.extend(normalized["ledger"])
        model.unattributed.extend(normalized["unattributed"])
        model.closure_sweep.extend(normalized["closure_sweep"])
        model.unapproved_open_prs.extend(normalized["unapproved_open_prs"])

    model.decisions.sort(key=lambda d: d.age_hours, reverse=True)
    model.flows.sort(key=lambda f: (f.repo, f.issue))
    model.sessions.sort(key=lambda s: (s.repo, s.issue, s.role))
    model.ledger.sort(key=lambda le: (le.repo, le.issue))

    return model
