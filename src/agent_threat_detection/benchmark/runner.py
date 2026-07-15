"""End-to-end benchmark runner with held-out calibration and threshold selection."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from time import perf_counter
from typing import Any

import numpy as np

from agent_threat_detection.benchmark.dataset import generate_benchmark, validate_benchmark
from agent_threat_detection.benchmark.evaluate import (
    binary_metrics,
    error_records,
    group_bootstrap_intervals,
    slice_metrics,
)
from agent_threat_detection.benchmark.models import (
    fit_calibrated,
    majority_scores,
    make_logistic_model,
    rule_scores,
    top_logistic_features,
)
from agent_threat_detection.benchmark.robustness import build_stress_suites
from agent_threat_detection.benchmark.thresholds import select_operating_threshold


def _subset(records: Sequence[Mapping[str, object]], split: str) -> list[Mapping[str, object]]:
    return [record for record in records if record["split"] == split]


def _labels(records: Sequence[Mapping[str, object]]) -> list[int]:
    return [int(bool(record["is_attack"])) for record in records]


def _timed_scores(
    predict: Any, records: Sequence[Mapping[str, object]]
) -> tuple[np.ndarray, float]:
    predict(records[: min(8, len(records))])
    started = perf_counter()
    scores = np.asarray(predict(records), dtype=float)
    return scores, round(1_000 * (perf_counter() - started) / len(records), 6)


def run_benchmark(
    *,
    seed: int = 20260715,
    examples_per_group: int = 12,
    bootstrap_samples: int = 400,
    precision_floor: float = 0.90,
) -> dict[str, Any]:
    """Generate data, fit four baselines, select thresholds, and score test once."""
    records = generate_benchmark(seed=seed, examples_per_group=examples_per_group)
    leakage_errors = validate_benchmark(records)
    if leakage_errors:
        raise ValueError("benchmark validation failed: " + "; ".join(leakage_errors))
    splits = {
        split: _subset(records, split) for split in ("train", "calibration", "validation", "test")
    }
    labels = {split: _labels(rows) for split, rows in splits.items()}
    attack_rate = sum(labels["train"]) / len(labels["train"])
    predictors: list[tuple[str, Any, Any]] = [
        ("majority", lambda rows: majority_scores(rows, attack_rate), None),
        ("rules", rule_scores, None),
    ]
    for name, structured in (("tfidf_logreg", False), ("hybrid_logreg", True)):
        base = make_logistic_model(structured=structured, seed=seed)
        calibrated = fit_calibrated(
            base, splits["train"], labels["train"], splits["calibration"], labels["calibration"]
        )
        predictors.append(
            (name, lambda rows, model=calibrated: model.predict_proba(rows)[:, 1], base)
        )
    model_results = []
    stress_suites = build_stress_suites(splits["test"])
    for index, (name, predict, base) in enumerate(predictors):
        validation_scores = np.asarray(predict(splits["validation"]), dtype=float)
        threshold = select_operating_threshold(
            labels["validation"], validation_scores.tolist(), precision_floor=precision_floor
        )
        test_scores, latency = _timed_scores(predict, splits["test"])
        test_metrics = binary_metrics(labels["test"], test_scores.tolist(), threshold.threshold)
        stress_tests = {}
        for suite_name, stressed_records in stress_suites.items():
            stressed_scores = np.asarray(predict(stressed_records), dtype=float)
            stressed_metrics = binary_metrics(
                labels["test"], stressed_scores.tolist(), threshold.threshold
            )
            stress_tests[suite_name] = {
                "metrics": stressed_metrics,
                "f1_delta": round(float(stressed_metrics["f1"]) - float(test_metrics["f1"]), 6),
                "recall_delta": round(
                    float(stressed_metrics["recall"]) - float(test_metrics["recall"]), 6
                ),
            }
        result: dict[str, Any] = {
            "name": name,
            "threshold": {
                "threshold": round(threshold.threshold, 6),
                "validation_precision": round(threshold.precision, 6),
                "validation_recall": round(threshold.recall, 6),
                "validation_false_positive_rate": round(threshold.false_positive_rate, 6),
                "validation_review_rate": round(threshold.review_rate, 6),
            },
            "test_metrics": test_metrics,
            "confidence_intervals_95": group_bootstrap_intervals(
                splits["test"],
                labels["test"],
                test_scores.tolist(),
                threshold.threshold,
                samples=bootstrap_samples,
                seed=seed + index,
            ),
            "slices": slice_metrics(
                splits["test"], labels["test"], test_scores.tolist(), threshold.threshold
            ),
            "errors": error_records(
                splits["test"], labels["test"], test_scores.tolist(), threshold.threshold
            ),
            "stress_tests": stress_tests,
            "latency_ms_per_trace": latency,
        }
        if base is not None:
            result["top_features"] = top_logistic_features(base)
        model_results.append(result)
    return {
        "experiment": {
            "seed": seed,
            "examples_per_template_group": examples_per_group,
            "bootstrap_samples": bootstrap_samples,
            "precision_floor": precision_floor,
            "split_policy": (
                "language template groups are isolated across train/calibration/validation/test"
            ),
            "calibration_policy": "Platt scaling on held-out calibration split",
            "threshold_policy": "maximize validation recall subject to precision floor",
        },
        "dataset": {
            "records": len(records),
            "split_counts": dict(sorted(Counter(str(r["split"]) for r in records).items())),
            "label_counts": dict(sorted(Counter(str(r["label"]) for r in records).items())),
            "template_groups": len({str(r["template_id"]) for r in records}),
            "leakage_errors": leakage_errors,
            "synthetic": True,
        },
        "models": model_results,
    }
