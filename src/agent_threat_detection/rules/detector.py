"""A deliberately small, transparent rules baseline.

This module is a teaching baseline, not a complete security control. Each rule
returns concrete evidence so later models can be compared against an
interpretable starting point.
"""

import re
from collections.abc import Iterable, Mapping
from typing import Literal

from agent_threat_detection.schema import DetectionResult, Finding

_HIGH_RISK_TOOLS = {
    "dump_database_credentials": "data_exfiltration",
    "execute_shell_command": "tool_misuse",
    "list_cloud_secrets": "data_exfiltration",
    "modify_system_prompt": "memory_poisoning",
    "read_private_files": "data_exfiltration",
}
_SECRET_PATTERN = re.compile(
    r"(?i)(api[_ -]?key|access[_ -]?token|password|private[_ -]?key|secret)\s*[:=]"
)
_INJECTION_PATTERN = re.compile(
    r"(?i)(ignore|disregard|override)\s+(all\s+)?(previous|prior|system)\s+instructions"
)


def _require_trace(trace: Mapping[str, object]) -> tuple[str, list[Mapping[str, object]]]:
    trace_id = trace.get("trace_id")
    if not isinstance(trace_id, str) or not trace_id.strip():
        raise ValueError("trace_id must be a non-empty string")
    events = trace.get("events")
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    if not all(isinstance(event, Mapping) for event in events):
        raise ValueError("every event must be an object")
    return trace_id, events


def _event_id(event: Mapping[str, object], index: int) -> str:
    value = event.get("event_id")
    return value if isinstance(value, str) and value else f"event-{index}"


def _flatten_strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for nested in value.values():
            yield from _flatten_strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _flatten_strings(nested)


def _is_external_recipient(value: object, allowed_domains: frozenset[str]) -> bool:
    if not isinstance(value, str) or "@" not in value:
        return False
    domain = value.rsplit("@", 1)[1].lower().strip()
    return domain not in allowed_domains


def detect_trace(
    trace: Mapping[str, object],
    *,
    allowed_email_domains: Iterable[str] = ("company.example",),
) -> DetectionResult:
    """Evaluate a structured agent trace with transparent high-signal rules."""

    trace_id, events = _require_trace(trace)
    allowed_domains = frozenset(domain.lower() for domain in allowed_email_domains)
    findings: list[Finding] = []

    for index, event in enumerate(events):
        evidence_id = _event_id(event, index)
        tool = event.get("tool")
        arguments = event.get("arguments", {})

        if isinstance(tool, str) and tool in _HIGH_RISK_TOOLS:
            findings.append(
                Finding(
                    rule_id="high-risk-tool",
                    label=_HIGH_RISK_TOOLS[tool],
                    severity="high",
                    description=f"High-risk tool invoked: {tool}",
                    evidence_event_ids=(evidence_id,),
                )
            )

        if tool == "send_email" and isinstance(arguments, Mapping):
            recipient = arguments.get("to")
            material = " ".join(_flatten_strings(arguments))
            if _is_external_recipient(recipient, allowed_domains) and _SECRET_PATTERN.search(
                material
            ):
                findings.append(
                    Finding(
                        rule_id="external-secret-send",
                        label="data_exfiltration",
                        severity="high",
                        description="Secret-like material sent to an unapproved email domain",
                        evidence_event_ids=(evidence_id,),
                    )
                )

        content = event.get("content")
        if isinstance(content, str) and _INJECTION_PATTERN.search(content):
            findings.append(
                Finding(
                    rule_id="instruction-override-language",
                    label="prompt_injection",
                    severity="medium",
                    description="Untrusted content contains instruction-override language",
                    evidence_event_ids=(evidence_id,),
                )
            )

    decision: Literal["allow", "alert", "block"]
    if any(finding.severity == "high" for finding in findings):
        decision = "block"
    elif findings:
        decision = "alert"
    else:
        decision = "allow"

    return DetectionResult(trace_id=trace_id, decision=decision, findings=tuple(findings))
