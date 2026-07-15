from agent_threat_detection.benchmark.dataset import generate_benchmark
from agent_threat_detection.benchmark.robustness import build_stress_suites


def test_stress_suites_preserve_labels_and_trace_count():
    records = [r for r in generate_benchmark(seed=13, examples_per_group=2) if r["split"] == "test"]

    suites = build_stress_suites(records)

    assert set(suites) == {"long_context", "missing_arguments", "unseen_tool_names"}
    for stressed in suites.values():
        assert len(stressed) == len(records)
        assert [r["is_attack"] for r in stressed] == [r["is_attack"] for r in records]
        assert [r["trace_id"] for r in stressed] == [r["trace_id"] for r in records]


def test_unseen_tool_suite_removes_original_tool_names():
    records = [r for r in generate_benchmark(seed=19, examples_per_group=1) if r["split"] == "test"]
    stressed = build_stress_suites(records)["unseen_tool_names"]

    original_tools = {
        event["tool"] for record in records for event in record["events"] if "tool" in event
    }
    stressed_tools = {
        event["tool"] for record in stressed for event in record["events"] if "tool" in event
    }
    assert original_tools.isdisjoint(stressed_tools)
