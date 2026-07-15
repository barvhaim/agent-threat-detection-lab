"""Dependency-free binary metrics with explicit missing-record semantics."""

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from math import sqrt


@dataclass(frozen=True)
class BinaryEvaluation:
    """Confusion counts, derived metrics, and record-alignment diagnostics."""

    tp: int
    fp: int
    fn: int
    tn: int
    precision: float
    recall: float
    f1: float
    false_positive_rate: float
    accuracy: float
    matthews_correlation: float
    missing_prediction_ids: tuple[str, ...]
    unexpected_prediction_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def evaluate_binary_records(
    expected: Mapping[str, bool], predicted: Mapping[str, bool]
) -> BinaryEvaluation:
    """Score keyed records.

    Missing predictions are treated as negative so missing attack cases enter the
    false-negative denominator. Predictions with unknown IDs are reported but
    excluded from the score because they have no ground truth.
    """

    missing = tuple(sorted(set(expected) - set(predicted)))
    unexpected = tuple(sorted(set(predicted) - set(expected)))
    tp = fp = fn = tn = 0

    for record_id, truth in expected.items():
        guess = predicted.get(record_id, False)
        if truth and guess:
            tp += 1
        elif not truth and guess:
            fp += 1
        elif truth and not guess:
            fn += 1
        else:
            tn += 1

    precision = _ratio(tp, tp + fp)
    recall = _ratio(tp, tp + fn)
    f1 = _ratio(2 * precision * recall, precision + recall)
    false_positive_rate = _ratio(fp, fp + tn)
    accuracy = _ratio(tp + tn, tp + fp + fn + tn)
    mcc_denominator = sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = _ratio(tp * tn - fp * fn, mcc_denominator)

    return BinaryEvaluation(
        tp=tp,
        fp=fp,
        fn=fn,
        tn=tn,
        precision=precision,
        recall=recall,
        f1=f1,
        false_positive_rate=false_positive_rate,
        accuracy=accuracy,
        matthews_correlation=mcc,
        missing_prediction_ids=missing,
        unexpected_prediction_ids=unexpected,
    )
