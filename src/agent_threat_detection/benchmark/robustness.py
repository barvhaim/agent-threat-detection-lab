"""Controlled distribution shifts applied only after model and threshold selection."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy


def _copy_records(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    return [deepcopy(dict(record)) for record in records]


def _events(record: Mapping[str, object]) -> list[dict[str, object]]:
    value = record.get("events")
    if not isinstance(value, list):
        return []
    return [event for event in value if isinstance(event, dict)]


def _unseen_tools(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    output = _copy_records(records)
    tools = sorted(
        {str(event["tool"]) for record in output for event in _events(record) if "tool" in event}
    )
    aliases = {tool: f"capability_{index:03d}" for index, tool in enumerate(tools)}
    for record in output:
        for event in _events(record):
            if event.get("tool") in aliases:
                event["tool"] = aliases[str(event["tool"])]
    return output


def _missing_arguments(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    output = _copy_records(records)
    for record in output:
        for event in _events(record):
            if "arguments" in event:
                event["arguments"] = {}
    return output


def _long_context(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    output = _copy_records(records)
    filler = " ".join(
        [
            "Routine authorized workflow context with no requested state change.",
            "The user expects a factual read-only response based on approved data.",
            "Do not infer additional permissions or contact external destinations.",
        ]
        * 30
    )
    for record in output:
        events = record.get("events", [])
        if isinstance(events, list):
            events.insert(
                1,
                {
                    "event_id": "stress-long-context",
                    "kind": "retrieved_content",
                    "source": "internal_policy",
                    "trust": "trusted",
                    "content": filler,
                },
            )
    return output


def build_stress_suites(
    records: Sequence[Mapping[str, object]],
) -> dict[str, list[dict[str, object]]]:
    """Return label-preserving test transformations with no model refit."""

    return {
        "long_context": _long_context(records),
        "missing_arguments": _missing_arguments(records),
        "unseen_tool_names": _unseen_tools(records),
    }
