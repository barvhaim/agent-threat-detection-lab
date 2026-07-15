"""Model-visible text and structured features for agent traces."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterable, Mapping


def _flatten(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for key in sorted(value):
            yield f"{key}={json.dumps(value[key], sort_keys=True)}"
    elif isinstance(value, list):
        for item in value:
            yield from _flatten(item)


def trace_to_text(record: Mapping[str, object]) -> str:
    """Serialize model-visible event semantics without labels or split metadata."""

    parts: list[str] = []
    events = record.get("events", [])
    if not isinstance(events, list):
        return ""
    for event in events:
        if not isinstance(event, Mapping):
            continue
        for key in ("kind", "source", "trust", "tool"):
            value = event.get(key)
            if isinstance(value, str):
                parts.append(f"{key}={value}")
        content = event.get("content")
        if isinstance(content, str):
            parts.append(content)
        arguments = event.get("arguments")
        if isinstance(arguments, Mapping):
            parts.extend(_flatten(arguments))
    return " [EVENT] ".join(parts)


def _contains_external_recipient(arguments: Mapping[str, object]) -> bool:
    for key in ("to", "recipient", "destination", "channel", "value"):
        value = arguments.get(key)
        if isinstance(value, str) and (
            "outside.example" in value
            or "external.example" in value
            or "untrusted.example" in value
            or "public-upload.example" in value
            or "external-webhook" in value
        ):
            return True
    return False


def structured_features(record: Mapping[str, object]) -> dict[str, float]:
    """Extract transparent capability and trust-boundary features."""

    features: dict[str, float] = defaultdict(float)
    scenario = record.get("scenario")
    if isinstance(scenario, str):
        features[f"scenario={scenario}"] = 1.0
    events = record.get("events", [])
    if not isinstance(events, list):
        return dict(features)
    for event in events:
        if not isinstance(event, Mapping):
            continue
        kind = event.get("kind")
        if isinstance(kind, str):
            features[f"kind={kind}"] += 1.0
        source = event.get("source")
        if isinstance(source, str):
            features[f"source={source}"] += 1.0
        if event.get("trust") == "untrusted":
            features["has_untrusted_content"] = 1.0
        tool = event.get("tool")
        if isinstance(tool, str):
            features[f"tool={tool}"] += 1.0
            features["tool_call_count"] += 1.0
        arguments = event.get("arguments")
        if isinstance(arguments, Mapping) and _contains_external_recipient(arguments):
            features["has_external_recipient"] = 1.0
    features["event_count"] = float(len(events))
    return dict(features)
