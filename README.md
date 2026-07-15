# Agent Threat Detection Lab

A hands-on learning repository for turning AI-agent security threats into measurable, production-oriented detection capabilities.

## What you will build

The repository grows through a complete detection lifecycle:

1. Threat taxonomy and trace schema
2. Leakage-resistant datasets and splits
3. Deterministic and classical ML baselines
4. Transformer and LLM-based detectors
5. Bounded agentic investigation
6. Calibration, thresholding, and abstention
7. Production service, monitoring, and feedback loops

The first runnable baseline is deliberately small and dependency-free. It detects high-signal tool-use patterns in structured agent traces and provides evidence for every finding.

## Learning materials

- **New here:** [`START_HERE.md`](START_HERE.md)
- **Guided 12-week course:** [`course/syllabus.md`](course/syllabus.md)
- **Hands-on labs:** [`labs/`](labs/00-first-15-minutes.md)
- **Research source notes:** [`resources/source-notes.md`](resources/source-notes.md)
- **Benchmarks and datasets:** [`resources/benchmarks-and-datasets.md`](resources/benchmarks-and-datasets.md)
- **Evaluation playbook:** [`docs/concepts/evaluation-playbook.md`](docs/concepts/evaluation-playbook.md)
- **Capstone:** [`capstone/brief.md`](capstone/brief.md)

## Quick start

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python examples/run_baseline.py
PYTHONPATH=src python scripts/score_predictions.py \
  --expected data/sample_labels.jsonl \
  --predicted data/sample_predictions.jsonl
```

Optional development setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check .
```

## Repository structure

```text
data/                  Dataset documentation and deterministic fixtures
course/                Guided weekly modules
docs/                  Learning path and concept guides
examples/              Runnable examples
labs/                  Hands-on exercises
resources/             Source notes, benchmarks, and tooling
reports/                Benchmark and research artifacts
src/agent_threat_detection/
  evaluation/           Dependency-free teaching metrics
  rules/                Transparent detection baselines
templates/              Research and decision artifacts
tests/                  Automated behavior tests
```

## Initial taxonomy

- `benign`
- `prompt_injection`
- `tool_misuse`
- `data_exfiltration`
- `memory_poisoning`
- `privilege_abuse`

See [`data/taxonomy.md`](data/taxonomy.md) for operational definitions.

## Evaluation principles

- Split by attack family, source, or template rather than near-duplicate prompts.
- Establish transparent baselines before adding complex models.
- Optimize for operational precision-recall trade-offs, not accuracy alone.
- Evaluate calibration, latency, cost, and important failure slices.
- Preserve evidence and document false positives and false negatives.

## Status

The repository contains a researched 12-week course, concept guides, labs, quizzes, templates, a deterministic rules baseline, sample traces, and a dependency-free scoring exercise. Model-training and production phases remain explicit milestones rather than unverified claims.

## Responsible use

Use synthetic, public, or explicitly authorized traces. Do not test attacks against third-party systems without permission. Remove secrets and personal data before adding traces to datasets.
