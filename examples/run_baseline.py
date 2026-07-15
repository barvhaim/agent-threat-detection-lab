import json
from pathlib import Path

from agent_threat_detection.rules.detector import detect_trace

fixture = Path(__file__).parents[1] / "data" / "sample_traces.jsonl"
for line in fixture.read_text(encoding="utf-8").splitlines():
    trace = json.loads(line)
    result = detect_trace(trace)
    print(json.dumps(result.to_dict(), sort_keys=True))
