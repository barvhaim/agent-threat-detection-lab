# Data

Only synthetic, public, or explicitly authorized traces belong here.

## Versioned benchmark

`benchmark/traces.jsonl` is generated deterministically by `agent-threat-benchmark`. The current manifest records 960 traces, 80 isolated template groups, split and label counts, and a SHA-256 digest.

The four splits have separate responsibilities:

- `train`: model fitting only
- `calibration`: held-out Platt scaling only
- `validation`: operating-threshold selection only
- `test`: final metrics, slices, errors, and stress transformations

The generator validator rejects duplicate IDs, template groups crossing splits, normalized content crossing splits, missing benign or attack cases, and insufficient scenario diversity.

## Small teaching fixtures

`sample_traces.jsonl`, `sample_labels.jsonl`, and `sample_predictions.jsonl` are deterministic smoke-test fixtures. They are not representative benchmarks.

## Limitations

The benchmark is synthetic, English-only, and intentionally attack-heavy. Tool schemas are invented and stable. See `reports/dataset-card.md` before interpreting any model score.
