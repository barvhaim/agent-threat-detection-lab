"""Metrics, group-bootstrap uncertainty, slices, and compact error records."""

from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score


def expected_calibration_error(labels: np.ndarray, scores: np.ndarray, bins: int = 10) -> float:
    total, error = len(labels), 0.0
    boundaries = np.linspace(0.0, 1.0, bins + 1)
    for index in range(bins):
        lower, upper = boundaries[index], boundaries[index + 1]
        mask = (scores >= lower) & (scores <= upper if index == bins - 1 else scores < upper)
        if np.any(mask):
            error += (
                float(np.sum(mask))
                / total
                * abs(float(np.mean(labels[mask])) - float(np.mean(scores[mask])))
            )
    return error


def binary_metrics(
    labels: Sequence[int], scores: Sequence[float], threshold: float
) -> dict[str, float | int]:
    y, p = np.asarray(labels, dtype=int), np.asarray(scores, dtype=float)
    pred = p >= threshold
    tp, fp = int(np.sum((y == 1) & pred)), int(np.sum((y == 0) & pred))
    fn, tn = int(np.sum((y == 1) & ~pred)), int(np.sum((y == 0) & ~pred))

    def ratio(a: float, b: float) -> float:
        return a / b if b else 0.0

    precision, recall = ratio(tp, tp + fp), ratio(tp, tp + fn)
    denominator = ((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) ** 0.5
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(ratio(2 * precision * recall, precision + recall), 6),
        "false_positive_rate": round(ratio(fp, fp + tn), 6),
        "accuracy": round(ratio(tp + tn, len(y)), 6),
        "matthews_correlation": round(ratio(tp * tn - fp * fn, denominator), 6),
        "average_precision": round(float(average_precision_score(y, p)), 6),
        "brier_score": round(float(brier_score_loss(y, p)), 6),
        "expected_calibration_error": round(expected_calibration_error(y, p), 6),
        "roc_auc": round(float(roc_auc_score(y, p)), 6) if len(set(y)) == 2 else 0.0,
    }


def group_bootstrap_intervals(
    records: Sequence[Mapping[str, object]],
    labels: Sequence[int],
    scores: Sequence[float],
    threshold: float,
    *,
    samples: int,
    seed: int,
) -> dict[str, dict[str, float]]:
    if samples < 1:
        return {}
    group_indices: dict[str, list[int]] = defaultdict(list)
    for index, record in enumerate(records):
        group_indices[str(record["template_id"])].append(index)
    groups, rng = sorted(group_indices), random.Random(seed)
    distributions: dict[str, list[float]] = defaultdict(list)
    for _ in range(samples):
        indices = [
            i for group in [rng.choice(groups) for _ in groups] for i in group_indices[group]
        ]
        metrics = binary_metrics(
            [labels[i] for i in indices], [scores[i] for i in indices], threshold
        )
        for name in ("precision", "recall", "f1", "false_positive_rate"):
            distributions[name].append(float(metrics[name]))
    return {
        name: {
            "low": round(float(np.quantile(values, 0.025)), 6),
            "high": round(float(np.quantile(values, 0.975)), 6),
        }
        for name, values in distributions.items()
    }


def slice_metrics(
    records: Sequence[Mapping[str, object]],
    labels: Sequence[int],
    scores: Sequence[float],
    threshold: float,
) -> dict[str, dict[str, float | int]]:
    slices: dict[str, list[int]] = defaultdict(list)
    for index, record in enumerate(records):
        slices[f"scenario:{record['scenario']}"].append(index)
        slices[f"label:{record['label']}"].append(index)
    output = {}
    for name, indices in sorted(slices.items()):
        y, p = [labels[i] for i in indices], [scores[i] for i in indices]
        pred, attacks = [score >= threshold for score in p], sum(y)
        benign = len(y) - attacks
        output[name] = {
            "count": len(indices),
            "attack_count": attacks,
            "recall": round(
                sum(label and guess for label, guess in zip(y, pred, strict=True)) / attacks, 6
            )
            if attacks
            else 0.0,
            "false_positive_rate": round(
                sum(not label and guess for label, guess in zip(y, pred, strict=True)) / benign, 6
            )
            if benign
            else 0.0,
            "mean_score": round(float(np.mean(p)), 6),
        }
    return output


def error_records(
    records: Sequence[Mapping[str, object]],
    labels: Sequence[int],
    scores: Sequence[float],
    threshold: float,
    *,
    limit: int = 12,
) -> dict[str, list[dict[str, Any]]]:
    errors: dict[str, list[dict[str, Any]]] = {"false_positives": [], "false_negatives": []}
    for record, label, score in zip(records, labels, scores, strict=True):
        predicted = score >= threshold
        if predicted != bool(label):
            key = "false_positives" if predicted else "false_negatives"
            errors[key].append(
                {
                    "trace_id": record["trace_id"],
                    "label": record["label"],
                    "scenario": record["scenario"],
                    "template_id": record["template_id"],
                    "score": round(float(score), 6),
                }
            )
    errors["false_positives"] = sorted(errors["false_positives"], key=lambda item: -item["score"])[
        :limit
    ]
    errors["false_negatives"] = sorted(errors["false_negatives"], key=lambda item: item["score"])[
        :limit
    ]
    return errors
