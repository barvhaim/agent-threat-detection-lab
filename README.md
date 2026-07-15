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

## Quick start

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python examples/run_baseline.py
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
docs/                  Learning path and design notes
examples/              Runnable examples
reports/                Benchmark and research artifacts
src/agent_threat_detection/
  rules/                Transparent detection baselines
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

The repository currently contains the initial schema, a deterministic rules baseline, sample traces, tests, and the full 12-week learning plan. Later phases intentionally remain explicit milestones rather than unverified claims.

## Responsible use

Use synthetic, public, or explicitly authorized traces. Do not test attacks against third-party systems without permission. Remove secrets and personal data before adding traces to datasets.
