from agent_threat_detection.benchmark.dataset import (
    generate_benchmark,
    normalized_trace_fingerprint,
    validate_benchmark,
)


def test_generation_is_deterministic_and_valid():
    first = generate_benchmark(seed=17, examples_per_group=3)
    second = generate_benchmark(seed=17, examples_per_group=3)

    assert first == second
    assert len(first) >= 240
    assert validate_benchmark(first) == []


def test_templates_and_fingerprints_do_not_cross_splits():
    records = generate_benchmark(seed=23, examples_per_group=3)
    template_splits: dict[str, set[str]] = {}
    fingerprint_splits: dict[str, set[str]] = {}

    for record in records:
        template_splits.setdefault(record["template_id"], set()).add(record["split"])
        fingerprint = normalized_trace_fingerprint(record)
        fingerprint_splits.setdefault(fingerprint, set()).add(record["split"])

    assert all(len(splits) == 1 for splits in template_splits.values())
    assert all(len(splits) == 1 for splits in fingerprint_splits.values())


def test_each_split_contains_attacks_benign_and_all_scenarios():
    records = generate_benchmark(seed=31, examples_per_group=3)
    splits = {record["split"] for record in records}

    assert splits == {"train", "calibration", "validation", "test"}
    for split in splits:
        subset = [record for record in records if record["split"] == split]
        assert {record["is_attack"] for record in subset} == {False, True}
        assert len({record["scenario"] for record in subset}) >= 4
