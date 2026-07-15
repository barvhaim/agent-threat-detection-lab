"""Render benchmark results as reviewer-friendly Markdown."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

Result = Mapping[str, Any]


def render_benchmark_report(result: Result) -> str:
    dataset = result["dataset"]
    lines = [
        "# Baseline Benchmark",
        "",
        "> Reproducible synthetic benchmark. It validates methodology and code, "
        "not production performance.",
        "",
        "## Experimental protocol",
        "",
        f"- Records: **{dataset['records']}**",
        f"- Template groups: **{dataset['template_groups']}**",
        f"- Splits: `{dataset['split_counts']}`",
        "- Language-template groups are disjoint across all four splits.",
        "- Calibration and threshold selection occur before test evaluation.",
        f"- Threshold policy: {result['experiment']['threshold_policy']}.",
        "- Confidence intervals resample template groups rather than rows.",
        "",
        "## Test results",
        "",
        "| Model | Precision | Recall | F1 | FPR | AP | Brier | ECE | ms/trace |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for model in result["models"]:
        metrics = model["test_metrics"]
        lines.append(
            f"| `{model['name']}` | {metrics['precision']:.3f} | "
            f"{metrics['recall']:.3f} | {metrics['f1']:.3f} | "
            f"{metrics['false_positive_rate']:.3f} | "
            f"{metrics['average_precision']:.3f} | {metrics['brier_score']:.3f} | "
            f"{metrics['expected_calibration_error']:.3f} | "
            f"{model['latency_ms_per_trace']:.3f} |"
        )

    lines.extend(["", "## Operating points", ""])
    for model in result["models"]:
        threshold = model["threshold"]
        metrics = model["test_metrics"]
        interval = model["confidence_intervals_95"].get("f1", {})
        lines.extend(
            [
                f"### {model['name']}",
                "",
                f"- threshold: `{threshold['threshold']}`",
                "- validation precision / recall: "
                f"`{threshold['validation_precision']}` / "
                f"`{threshold['validation_recall']}`",
                "- test F1 95% group-bootstrap interval: "
                f"`{interval.get('low', 'n/a')}` to `{interval.get('high', 'n/a')}`",
                f"- confusion matrix: TP={metrics['tp']}, FP={metrics['fp']}, "
                f"FN={metrics['fn']}, TN={metrics['tn']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Stress tests",
            "",
            "Thresholds are frozen and no model is refit on these transformations.",
            "",
            "| Model | Shift | Precision | Recall | F1 | F1 delta |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for model in result["models"]:
        for suite_name, stress in model["stress_tests"].items():
            metrics = stress["metrics"]
            lines.append(
                f"| `{model['name']}` | `{suite_name}` | {metrics['precision']:.3f} | "
                f"{metrics['recall']:.3f} | {metrics['f1']:.3f} | "
                f"{stress['f1_delta']:+.3f} |"
            )

    hybrid = next(model for model in result["models"] if model["name"] == "hybrid_logreg")
    precision_gate = float(hybrid["test_metrics"]["precision"]) >= float(
        result["experiment"]["precision_floor"]
    )
    lines.extend(
        [
            "",
            "## Model-selection decision",
            "",
            f"- Hybrid blocking precision gate: **{'PASS' if precision_gate else 'FAIL'}**.",
            "- Validation precision was "
            f"`{hybrid['threshold']['validation_precision']}`, while test precision was "
            f"`{hybrid['test_metrics']['precision']}`.",
            "- Keep deterministic high-confidence rules for blocking.",
            "- Keep the hybrid in shadow or analyst-review mode until representative data passes.",
            "- Compare any LLM judge against these frozen baselines before adoption.",
            "",
            "## Limitations",
            "",
            "- All traces are synthetic and share a controlled generator.",
            "- Template isolation does not reproduce organic enterprise distributions.",
            "- Stress transformations are controlled probes, not adaptive red-team attacks.",
            "- Latency is local CPU inference, not service-level p95 latency.",
            "- The binary target collapses impact and severity classes.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_error_analysis(result: Result) -> str:
    lines = [
        "# Error Analysis",
        "",
        "Errors below come from the untouched synthetic test split.",
        "",
    ]
    for model in result["models"]:
        lines.extend([f"## {model['name']}", ""])
        for kind in ("false_positives", "false_negatives"):
            errors = model["errors"][kind]
            lines.extend([f"### {kind.replace('_', ' ').title()} ({len(errors)} shown)", ""])
            if not errors:
                lines.append("None at the selected operating point.")
            else:
                lines.extend(
                    [
                        "| trace | label | scenario | template | score |",
                        "|---|---|---|---|---:|",
                    ]
                )
                for error in errors:
                    lines.append(
                        f"| `{error['trace_id']}` | `{error['label']}` | "
                        f"`{error['scenario']}` | `{error['template_id']}` | "
                        f"{error['score']:.3f} |"
                    )
            lines.append("")
    lines.extend(
        [
            "## Analysis protocol",
            "",
            "Assign each failure to label ambiguity, generator artifact, representation gap, "
            "model failure, threshold policy, or missing telemetry before adding a "
            "regression case.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_model_card(result: Result) -> str:
    chosen = next(model for model in result["models"] if model["name"] == "hybrid_logreg")
    metrics = chosen["test_metrics"]
    lines = [
        "# Model Card: Hybrid Logistic Baseline",
        "",
        "## Intended use",
        "",
        "Research baseline for binary attack detection in structured AI-agent traces. It "
        "combines word and character TF-IDF with event, trust, tool, and destination features.",
        "",
        "## Not intended for",
        "",
        "Production blocking, autonomous incident response, attribution, malware detection, "
        "or claims about real-world attack prevalence.",
        "",
        "## Training and evaluation data",
        "",
        f"- synthetic records: {result['dataset']['records']}",
        f"- isolated template groups: {result['dataset']['template_groups']}",
        f"- split policy: {result['experiment']['split_policy']}",
        f"- calibration: {result['experiment']['calibration_policy']}",
        "",
        "## Untouched test result",
        "",
        f"- precision: {metrics['precision']}",
        f"- recall: {metrics['recall']}",
        f"- F1: {metrics['f1']}",
        f"- false-positive rate: {metrics['false_positive_rate']}",
        f"- average precision: {metrics['average_precision']}",
        f"- Brier score: {metrics['brier_score']}",
        f"- selected threshold: {chosen['threshold']['threshold']}",
        "",
        "## Explainability",
        "",
        "`artifacts/benchmark/results.json` records largest signed logistic coefficients. "
        "Association in generated data is not causal security importance.",
        "",
        "## Known risks",
        "",
        "Generator artifacts, stable schemas, adversarial paraphrase, multilingual input, "
        "malformed events, policy drift, and confidence shift outside this distribution.",
        "",
        "## Release gate",
        "",
        "Do not enable blocking until representative traces meet precision, critical-family "
        "recall, latency, review-budget, privacy, and rollback gates.",
    ]
    return "\n".join(lines) + "\n"


def render_dataset_card(result: Result) -> str:
    dataset = result["dataset"]
    lines = [
        "# Dataset Card: Synthetic Agent Trace Benchmark v1",
        "",
        "## Purpose",
        "",
        "Safe deterministic data for testing methodology, split hygiene, calibration, "
        "thresholding, and error analysis. It is not representative telemetry.",
        "",
        "## Composition",
        "",
        f"- records: {dataset['records']}",
        f"- template groups: {dataset['template_groups']}",
        f"- labels: `{dataset['label_counts']}`",
        f"- splits: `{dataset['split_counts']}`",
        "- scenarios: email, support, cloud, filesystem, CRM, and calendar",
        "- events: user messages, retrieved untrusted content, and tool calls",
        "",
        "## Split construction",
        "",
        "Each label has split-specific language templates. A template group belongs to one "
        "split. Validation rejects duplicate IDs, template leakage, normalized-content "
        "leakage, missing classes, and insufficient scenario diversity.",
        "",
        "## Labels",
        "",
        "`benign`, `prompt_injection`, `data_exfiltration`, `privilege_abuse`, and "
        "`memory_poisoning`. Binary experiments map all non-benign labels to attack.",
        "",
        "## Provenance and license",
        "",
        "All examples are generated locally with synthetic identifiers and secrets under "
        "the repository MIT license. No paper benchmark or private telemetry is redistributed.",
        "",
        "## Known biases",
        "",
        "English-only controlled grammar, stable schemas, invented tools, balanced scenarios, "
        "high attack prevalence, and no organic user noise. Models can exploit "
        "generator regularities.",
        "",
        "## Appropriate use",
        "",
        "Regression testing, teaching, pipeline comparisons, and research scaffolding. Do not "
        "use these scores to justify production blocking or estimate incident prevalence.",
    ]
    return "\n".join(lines) + "\n"


def render_model_selection_memo(result: Result) -> str:
    rules = next(model for model in result["models"] if model["name"] == "rules")
    hybrid = next(model for model in result["models"] if model["name"] == "hybrid_logreg")
    floor = float(result["experiment"]["precision_floor"])
    test_precision = float(hybrid["test_metrics"]["precision"])
    status = "PASS" if test_precision >= floor else "FAIL"
    lines = [
        "# Model Selection Memo",
        "",
        "## Decision",
        "",
        "Use deterministic rules for high-confidence blocking. Keep the hybrid logistic model "
        "in shadow or analyst-review mode. Do not promote it to automatic blocking.",
        "",
        "## Evidence",
        "",
        f"- rules precision / recall / F1: `{rules['test_metrics']['precision']}` / "
        f"`{rules['test_metrics']['recall']}` / `{rules['test_metrics']['f1']}`",
        f"- hybrid precision / recall / F1: `{hybrid['test_metrics']['precision']}` / "
        f"`{hybrid['test_metrics']['recall']}` / `{hybrid['test_metrics']['f1']}`",
        f"- required blocking precision: `{floor}`",
        f"- hybrid blocking gate: **{status}**",
        "- validation-to-test precision: "
        f"`{hybrid['threshold']['validation_precision']}` to `{test_precision}`",
        "",
        "## Interpretation",
        "",
        "The hybrid materially improves coverage, but its selected threshold does not transfer "
        "at the required precision. This gap matters more than aggregate F1.",
        "",
        "## Deployment posture",
        "",
        "1. Rules may block only explicit high-severity conditions.",
        "2. Hybrid scores create shadow telemetry and analyst-review candidates.",
        "3. Evaluate authorized labels per tool, tenant, language, and attack family.",
        "4. Recalibrate and freeze thresholds before a prospective shadow period.",
        "5. Promote only after precision, recall, volume, latency, and rollback gates pass.",
        "",
        "## Rejected alternatives",
        "",
        "- Majority: no useful detection capability.",
        "- Rules only: excellent precision but insufficient recall.",
        "- TF-IDF only: slightly weaker than the hybrid without operational advantage.",
        "- LLM judge or investigator: deferred until compared for injection, cost, latency, "
        "and stability on the same benchmark.",
    ]
    return "\n".join(lines) + "\n"


def render_production_readiness(result: Result) -> str:
    hybrid = next(model for model in result["models"] if model["name"] == "hybrid_logreg")
    precision_pass = float(hybrid["test_metrics"]["precision"]) >= float(
        result["experiment"]["precision_floor"]
    )
    lines = [
        "# Production Readiness",
        "",
        "Current verdict: **NOT READY FOR PRODUCTION BLOCKING**",
        "",
        "| Gate | Status | Evidence |",
        "|---|---|---|",
        "| Reproducible evaluation | PASS | deterministic generator, seed, and CLI |",
        "| Split leakage checks | PASS | template and normalized-content isolation |",
        "| Held-out calibration | PASS | dedicated calibration split |",
        "| Frozen-threshold test | PASS | untouched test split |",
        f"| Blocking precision | {'PASS' if precision_pass else 'FAIL'} | "
        f"test precision {hybrid['test_metrics']['precision']} |",
        "| Representative authorized data | FAIL | synthetic data only |",
        "| Prospective shadow evaluation | FAIL | not run |",
        "| Service load and failure testing | FAIL | model-only latency measured |",
        "| Monitoring and rollback drill | FAIL | design only |",
        "| Privacy and retention review | FAIL | required before real telemetry |",
        "",
        "## Promotion criteria",
        "",
        "Pass numerical gates for representative precision, critical-family recall, analyst "
        "volume, latency, availability, privacy, and rollback. Synthetic F1 is not a gate.",
    ]
    return "\n".join(lines) + "\n"
