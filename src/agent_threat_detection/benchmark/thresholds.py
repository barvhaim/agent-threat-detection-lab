"""Operational threshold selection with explicit constraints."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ThresholdSelection:
    threshold: float
    precision: float
    recall: float
    false_positive_rate: float
    review_rate: float
    predicted_positive_rate: float


def _metrics(
    labels: list[int], scores: list[float], threshold: float
) -> tuple[float, float, float]:
    predictions = [score >= threshold for score in scores]
    tp = sum(label == 1 and pred for label, pred in zip(labels, predictions, strict=True))
    fp = sum(label == 0 and pred for label, pred in zip(labels, predictions, strict=True))
    fn = sum(label == 1 and not pred for label, pred in zip(labels, predictions, strict=True))
    tn = sum(label == 0 and not pred for label, pred in zip(labels, predictions, strict=True))
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return precision, recall, fpr


def select_operating_threshold(
    labels: list[int],
    scores: list[float],
    *,
    precision_floor: float = 0.90,
    abstain_margin: float = 0.05,
) -> ThresholdSelection:
    """Maximize recall subject to precision, then minimize FPR and threshold."""

    if len(labels) != len(scores) or not labels:
        raise ValueError("labels and scores must have equal non-zero length")
    if set(labels) - {0, 1}:
        raise ValueError("labels must be binary")
    candidates = sorted({0.0, 1.0, *scores})
    feasible: list[tuple[float, float, float, float]] = []
    for threshold in candidates:
        precision, recall, fpr = _metrics(labels, scores, threshold)
        if precision >= precision_floor:
            feasible.append((threshold, precision, recall, fpr))
    if not feasible:
        feasible = [(threshold, *_metrics(labels, scores, threshold)) for threshold in candidates]
    threshold, precision, recall, fpr = max(
        feasible,
        key=lambda item: (item[2], -item[3], -item[0]),
    )
    review = sum(abs(score - threshold) <= abstain_margin for score in scores) / len(scores)
    positive = sum(score >= threshold for score in scores) / len(scores)
    return ThresholdSelection(
        threshold=threshold,
        precision=precision,
        recall=recall,
        false_positive_rate=fpr,
        review_rate=review,
        predicted_positive_rate=positive,
    )
