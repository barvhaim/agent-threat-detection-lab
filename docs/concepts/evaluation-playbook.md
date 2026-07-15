# Evaluation Playbook for Rare Security Events

## Start from a decision

A detector is useful only in a workflow. Define whether a score triggers allow, log, alert, analyst review, user approval, or block.

## Core metrics

- **Precision:** among alerts, how many are attacks?
- **Recall:** among attacks, how many are detected?
- **False-positive rate:** among benign events, how many alert?
- **PR-AUC:** threshold-independent summary suited to rare positives, but still not an operating point.
- **Calibration:** whether predicted probabilities match observed frequencies.
- **Brier score:** proper score for probability quality, combining calibration and resolution.
- **MCC:** useful confusion-matrix summary under imbalance.
- **Attack success rate:** whether the attacker achieved its goal. Keep separate from detector classification accuracy.
- **Benign utility:** whether the agent still completes legitimate tasks.

## Split design

Never split near-duplicate templates randomly. Group by attack family, source, campaign, environment, tool family, or generation recipe. Keep a final out-of-distribution set containing unseen constructions.

## Threshold design

Choose thresholds on validation data. Report at least:

- precision at the alert threshold
- recall at the block threshold
- false-positive rate on representative benign traffic
- review volume per unit of production traffic
- cost-weighted utility using an explicit cost matrix

## Confidence intervals

Security datasets are often small in important slices. Use bootstrap intervals or exact binomial intervals and report counts beside percentages.

## LLM and agent evaluation

Measure repeated-call agreement, schema validity, cost, latency, evidence grounding, injection resistance, tool-use limits, and model-version sensitivity. Do not rely on another LLM as the only ground truth for security impact when environment-state checks are possible.

## Error-analysis loop

1. sample false positives and false negatives
2. assign a cause: data, label, representation, model, policy, threshold, or upstream telemetry
3. choose one controlled change
4. rerun the unchanged benchmark
5. inspect whether improvement is broad or slice-specific
6. update the decision memo
