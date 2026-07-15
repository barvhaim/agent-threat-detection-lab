from agent_threat_detection.benchmark.runner import run_benchmark


def test_benchmark_runs_multiple_models_on_held_out_test_split():
    result = run_benchmark(
        seed=101,
        examples_per_group=3,
        bootstrap_samples=20,
        precision_floor=0.80,
    )

    assert result["dataset"]["leakage_errors"] == []
    assert result["dataset"]["split_counts"]["test"] >= 50
    assert {model["name"] for model in result["models"]} == {
        "majority",
        "rules",
        "tfidf_logreg",
        "hybrid_logreg",
    }
    for model in result["models"]:
        assert set(model["test_metrics"]) >= {
            "precision",
            "recall",
            "f1",
            "false_positive_rate",
            "average_precision",
            "brier_score",
        }
        assert 0.0 <= model["threshold"]["threshold"] <= 1.0
        assert model["latency_ms_per_trace"] >= 0.0
        assert set(model["stress_tests"]) == {
            "long_context",
            "missing_arguments",
            "unseen_tool_names",
        }


def test_benchmark_is_reproducible():
    first = run_benchmark(seed=7, examples_per_group=2, bootstrap_samples=10)
    second = run_benchmark(seed=7, examples_per_group=2, bootstrap_samples=10)

    compact_first = [(m["name"], m["threshold"], m["test_metrics"]) for m in first["models"]]
    compact_second = [(m["name"], m["threshold"], m["test_metrics"]) for m in second["models"]]
    assert compact_first == compact_second
