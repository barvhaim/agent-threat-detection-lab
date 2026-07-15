"""Command-line entry point for a fully reproducible benchmark run."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path

from agent_threat_detection.benchmark.dataset import generate_benchmark, write_benchmark
from agent_threat_detection.benchmark.reporting import (
    render_benchmark_report,
    render_dataset_card,
    render_error_analysis,
    render_model_card,
    render_model_selection_memo,
    render_production_readiness,
)
from agent_threat_detection.benchmark.runner import run_benchmark


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_reports(reports_dir: Path, result: dict[str, object]) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    renderers: dict[str, Callable[[dict[str, object]], str]] = {
        "baseline-benchmark.md": render_benchmark_report,
        "dataset-card.md": render_dataset_card,
        "error-analysis.md": render_error_analysis,
        "model-card.md": render_model_card,
        "model-selection.md": render_model_selection_memo,
        "production-readiness.md": render_production_readiness,
    }
    for filename, renderer in renderers.items():
        (reports_dir / filename).write_text(renderer(result), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and evaluate agent-threat baselines")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/benchmark"))
    parser.add_argument("--dataset-path", type=Path, default=Path("data/benchmark/traces.jsonl"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--examples-per-group", type=int, default=12)
    parser.add_argument("--bootstrap-samples", type=int, default=400)
    parser.add_argument("--precision-floor", type=float, default=0.90)
    args = parser.parse_args()

    records = generate_benchmark(seed=args.seed, examples_per_group=args.examples_per_group)
    manifest = write_benchmark(records, args.dataset_path)
    _write_json(args.dataset_path.with_name("manifest.json"), manifest)
    result = run_benchmark(
        seed=args.seed,
        examples_per_group=args.examples_per_group,
        bootstrap_samples=args.bootstrap_samples,
        precision_floor=args.precision_floor,
    )
    _write_json(args.output_dir / "results.json", result)
    _write_reports(args.reports_dir, result)
    print(
        json.dumps(
            {
                "dataset": manifest,
                "models": [
                    {"name": model["name"], "f1": model["test_metrics"]["f1"]}
                    for model in result["models"]
                ],
                "results": str(args.output_dir / "results.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
