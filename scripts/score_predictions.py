#!/usr/bin/env python3
"""Score keyed JSONL predictions without third-party dependencies."""

import argparse
import json
from pathlib import Path
from typing import Any

from agent_threat_detection.evaluation.metrics import evaluate_binary_records


def load_keyed_boolean(path: Path, value_field: str) -> dict[str, bool]:
    records: dict[str, bool] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record: dict[str, Any] = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
        record_id = record.get("trace_id")
        value = record.get(value_field)
        if not isinstance(record_id, str) or not record_id:
            raise ValueError(f"{path}:{line_number}: trace_id must be a non-empty string")
        if record_id in records:
            raise ValueError(f"{path}:{line_number}: duplicate trace_id {record_id!r}")
        if not isinstance(value, bool):
            raise ValueError(f"{path}:{line_number}: {value_field} must be boolean")
        records[record_id] = value
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=Path, required=True)
    parser.add_argument("--predicted", type=Path, required=True)
    args = parser.parse_args()
    expected = load_keyed_boolean(args.expected, "is_attack")
    predicted = load_keyed_boolean(args.predicted, "predicted_attack")
    result = evaluate_binary_records(expected, predicted)
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
