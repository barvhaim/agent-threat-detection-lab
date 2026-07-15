"""Transparent rule and statistical baselines for structured agent traces."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from agent_threat_detection.benchmark.features import structured_features, trace_to_text
from agent_threat_detection.rules.detector import detect_trace


class TraceTextExtractor(TransformerMixin, BaseEstimator):
    def fit(self, X: Sequence[Mapping[str, object]], y: object = None) -> TraceTextExtractor:
        return self

    def transform(self, X: Sequence[Mapping[str, object]]) -> list[str]:
        return [trace_to_text(record) for record in X]


class StructuredFeatureExtractor(TransformerMixin, BaseEstimator):
    def fit(
        self, X: Sequence[Mapping[str, object]], y: object = None
    ) -> StructuredFeatureExtractor:
        return self

    def transform(self, X: Sequence[Mapping[str, object]]) -> list[dict[str, float]]:
        return [structured_features(record) for record in X]


def make_logistic_model(*, structured: bool, seed: int) -> Pipeline:
    branches: list[tuple[str, Pipeline]] = [
        (
            "word",
            Pipeline(
                [
                    ("extract", TraceTextExtractor()),
                    (
                        "vectorizer",
                        TfidfVectorizer(
                            ngram_range=(1, 2), min_df=2, max_features=12_000, sublinear_tf=True
                        ),
                    ),
                ]
            ),
        ),
        (
            "char",
            Pipeline(
                [
                    ("extract", TraceTextExtractor()),
                    (
                        "vectorizer",
                        TfidfVectorizer(
                            analyzer="char_wb",
                            ngram_range=(3, 5),
                            min_df=2,
                            max_features=18_000,
                            sublinear_tf=True,
                        ),
                    ),
                ]
            ),
        ),
    ]
    if structured:
        branches.append(
            (
                "structured",
                Pipeline(
                    [("extract", StructuredFeatureExtractor()), ("vectorizer", DictVectorizer())]
                ),
            )
        )
    return Pipeline(
        [
            ("features", FeatureUnion(branches)),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced", max_iter=2_000, random_state=seed, solver="liblinear"
                ),
            ),
        ]
    )


def fit_calibrated(
    model: Pipeline,
    train_records: Sequence[Mapping[str, object]],
    train_labels: Sequence[int],
    calibration_records: Sequence[Mapping[str, object]],
    calibration_labels: Sequence[int],
) -> CalibratedClassifierCV:
    """Fit on train and perform held-out Platt calibration."""
    model.fit(train_records, train_labels)
    calibrated = CalibratedClassifierCV(FrozenEstimator(model), method="sigmoid")
    calibrated.fit(calibration_records, calibration_labels)
    return calibrated


def rule_scores(records: Sequence[Mapping[str, object]]) -> np.ndarray:
    mapping = {"allow": 0.05, "alert": 0.65, "block": 0.95}
    return np.asarray([mapping[detect_trace(record).decision] for record in records], dtype=float)


def majority_scores(records: Sequence[Mapping[str, object]], attack_rate: float) -> np.ndarray:
    return np.full(len(records), attack_rate, dtype=float)


def top_logistic_features(model: Pipeline, limit: int = 12) -> dict[str, list[dict[str, Any]]]:
    names: list[str] = []
    union = model.named_steps["features"]
    for branch_name, branch in union.transformer_list:
        vectorizer = branch.named_steps["vectorizer"]
        names.extend(f"{branch_name}:{name}" for name in vectorizer.get_feature_names_out())
    coefficients = model.named_steps["classifier"].coef_[0]
    ordered = np.argsort(coefficients)

    def serialize(indices: np.ndarray) -> list[dict[str, Any]]:
        return [
            {"feature": names[int(index)], "coefficient": round(float(coefficients[index]), 6)}
            for index in indices
        ]

    return {"negative": serialize(ordered[:limit]), "positive": serialize(ordered[-limit:][::-1])}
