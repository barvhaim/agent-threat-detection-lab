"""Small, serializable result types used by detection baselines."""

from dataclasses import asdict, dataclass
from typing import Literal

Decision = Literal["allow", "alert", "block"]
Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class Finding:
    """One evidence-backed detection finding."""

    rule_id: str
    label: str
    severity: Severity
    description: str
    evidence_event_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class DetectionResult:
    """The decision and findings produced for a single trace."""

    trace_id: str
    decision: Decision
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "trace_id": self.trace_id,
            "decision": self.decision,
            "findings": [finding.to_dict() for finding in self.findings],
        }
