# Lab 0: First Detection Loop

Time: 10 to 15 minutes  
Cost: zero  
Hardware: any recent CPU  
Credentials: none

## Goal

See a full input, detector, evidence, prediction, and score loop before studying model training.

## Run the baseline

```bash
PYTHONPATH=src python examples/run_baseline.py
```

Inspect each JSON line. Identify the trace ID, decision, finding label, severity, rule, and evidence event IDs.

## Score the predictions

```bash
PYTHONPATH=src python scripts/score_predictions.py   --expected data/sample_labels.jsonl   --predicted data/sample_predictions.jsonl
```

Expected counts: `tp=2`, `tn=1`, `fp=0`, `fn=0`.

## Create a failure

Change the prediction for `attack-002` to `false` in a temporary copy and rerun the scorer. Recall should fall and one false negative should appear.

## Explain

- Why is the perfect original score not evidence of detector quality?
- Which rule produced the evidence for each attack?
- What realistic benign input might cause a false positive?

## Artifact

Add three bullets to your progress log: observed behavior, one failure mode, and one next experiment.
