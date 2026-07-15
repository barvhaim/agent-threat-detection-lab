# Guided Course Syllabus

## Learning outcome

By the end of the course, you should be able to take a threat report, identify observable signals, create a defensible benchmark, compare detection paradigms, ship a bounded service, and define monitoring and rollback policies.

## Weekly map

| Week | Topic | Main artifact |
|---|---|---|
| 1 | Agent security and threat modeling | Threat model and attack chains |
| 2 | Data contracts, labels, and leakage | Dataset card and grouped splits |
| 3 | Transparent rules and classical ML | Baseline benchmark |
| 4 | Operational evaluation | Threshold decision memo |
| 5 | Small transformer detector | Reproducible model card |
| 6 | Robustness and long traces | Slice-based error analysis |
| 7 | Structured LLM detector | Judge benchmark and threat model |
| 8 | Bounded agentic investigation | Cascade ablation |
| 9 | Service and release engineering | Runnable detection API |
| 10 | Monitoring and feedback | Drift and rollback exercise |
| 11 | End-to-end attack chains | Multi-stage detection demo |
| 12 | Portfolio packaging | Technical presentation and evidence pack |

## Rules for completing the course

1. Every week must produce an artifact, not only reading notes.
2. Every model must be compared with a simpler baseline.
3. Every benchmark must document provenance and split logic.
4. Every score must name the dataset version and threshold.
5. Every production control must name its failure response.
6. Every security experiment must use synthetic, public, or authorized data.

## Recommended workload

- 1 hour: required reading
- 1 hour: inspect an existing implementation
- 4 to 6 hours: build
- 1 hour: evaluation and error analysis
- 1 hour: write the decision and update the demo

Use the [progress log](../templates/progress-log.md) after each week.
