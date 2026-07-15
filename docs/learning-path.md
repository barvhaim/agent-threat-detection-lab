# Applied AI Security Detection: 12-Week Learning Path

**Workload:** 8 to 10 focused hours per week

**Outcome:** Build evidence that you can turn agent-security threat intelligence into evaluated, production-ready detection capabilities.

## Operating loop

Every phase follows the same loop:

1. Learn the minimum concept needed for the next boundary.
2. Inspect a working implementation or official reference.
3. Build one measurable increment.
4. Change one component at a time.
5. Evaluate and analyze failures.
6. Record what the result means for a production decision.

## Week 1: Threat model and detection taxonomy

Map an enterprise agent across inputs, tools, permissions, identity, memory, and outputs. Write six attack chains and convert them into operational labels.

**Artifact:** `reports/threat-model.md` and an updated `data/taxonomy.md`.

## Week 2: Dataset and annotation design

Create versioned synthetic or authorized traces, provenance fields, grouped splits, annotation guidance, duplicate checks, and an out-of-distribution test split.

**Artifact:** dataset card and reproducible split script.

## Week 3: Rules and classical ML baselines

Extend the deterministic detector, then add TF-IDF plus logistic regression and structured event features. Compare quality, latency, and interpretability.

**Artifact:** `reports/baseline-benchmark.md`.

## Week 4: Production-oriented evaluation

Add precision-recall curves, cost-sensitive thresholds, calibration, bootstrap confidence intervals, abstention, and slice-based evaluation.

**Artifact:** reusable evaluation harness and decision memo.

## Week 5: Fine-tuned transformer

Fine-tune a compact encoder classifier with reproducible configuration, dataset version, seed, and model card.

**Artifact:** training command, model card, and baseline comparison.

## Week 6: Robustness and evidence

Handle long traces, attribute evidence events, and test paraphrase, obfuscation, benign security language, long-context distraction, and conflicting tool outputs.

**Artifact:** `reports/robustness-and-error-analysis.md`.

## Week 7: Structured LLM detector

Build a schema-validated LLM judge. Separate trusted policy from untrusted trace content. Measure stability, cost, latency, and injection resistance.

**Artifact:** LLM detector benchmark and detector threat model.

## Week 8: Bounded investigation and cascade

Create read-only investigation tools and a bounded cascade that escalates uncertain or high-impact cases. Keep strict step, time, and cost budgets.

**Artifact:** `reports/cascade-ablation.md`.

## Week 9: Detection service

Expose prediction, health, and version endpoints. Add container packaging, golden-set tests, CI, versioned contracts, and shadow mode.

**Artifact:** runnable service and load-test report.

## Week 10: Monitoring and feedback

Monitor prediction shifts, confidence, alert rate, analyst overrides, latency, slice drift, and delayed labels. Simulate degradation and rollback.

**Artifact:** `reports/production-readiness.md`.

## Week 11: End-to-end attack chain

Model an indirect injection that enters through enterprise content and ends in a tool call. Compare detection at content, tool-choice, policy, and impact stages.

**Artifact:** five-minute end-to-end demo.

## Week 12: Portfolio packaging

Finalize the README, benchmark, error analysis, model-selection memo, production-readiness memo, five-minute demo, and fifteen-minute deep dive.

**Artifact:** a repository that can be cloned, tested, evaluated, and explained without hidden context.

## Completion criteria

- [ ] Threat model tied to concrete telemetry
- [ ] Annotation guide and leakage-resistant benchmark
- [ ] Rules, classical ML, deep-learning, LLM, and agentic baselines
- [ ] Explicit model-selection decision
- [ ] Calibration, abstention, and slice analysis
- [ ] Deployed service with tests and latency measurements
- [ ] Drift simulation, rollback plan, and feedback loop
- [ ] Clear connection between model metrics and security outcomes
