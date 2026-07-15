# Dataset Card: Synthetic Agent Trace Benchmark v1

## Purpose

Safe deterministic data for testing methodology, split hygiene, calibration, thresholding, and error analysis. It is not representative telemetry.

## Composition

- records: 960
- template groups: 80
- labels: `{'benign': 384, 'data_exfiltration': 144, 'memory_poisoning': 144, 'privilege_abuse': 144, 'prompt_injection': 144}`
- splits: `{'calibration': 240, 'test': 240, 'train': 240, 'validation': 240}`
- scenarios: email, support, cloud, filesystem, CRM, and calendar
- events: user messages, retrieved untrusted content, and tool calls

## Split construction

Each label has split-specific language templates. A template group belongs to one split. Validation rejects duplicate IDs, template leakage, normalized-content leakage, missing classes, and insufficient scenario diversity.

## Labels

`benign`, `prompt_injection`, `data_exfiltration`, `privilege_abuse`, and `memory_poisoning`. Binary experiments map all non-benign labels to attack.

## Provenance and license

All examples are generated locally with synthetic identifiers and secrets under the repository MIT license. No paper benchmark or private telemetry is redistributed.

## Known biases

English-only controlled grammar, stable schemas, invented tools, balanced scenarios, high attack prevalence, and no organic user noise. Models can exploit generator regularities.

## Appropriate use

Regression testing, teaching, pipeline comparisons, and research scaffolding. Do not use these scores to justify production blocking or estimate incident prevalence.
