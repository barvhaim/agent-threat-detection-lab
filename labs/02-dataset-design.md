# Lab 2: Dataset Design Without Leakage

## Goal

Create a small benchmark that tests generalization beyond memorized attack wording.

## Schema

Each trace should include trace ID, ordered events, source, environment, attack family, template or campaign ID, label, severity, evidence event IDs, and adjudication status.

## Steps

1. Create 20 benign and 20 adversarial traces.
2. Include hard benign cases containing terms such as password, injection, secret, and exfiltration.
3. Generate at least four attack families with multiple paraphrases.
4. Group splits by family or template, not by row.
5. Reserve one attack construction for out-of-distribution testing.
6. Check exact and normalized duplicates across splits.
7. Manually relabel a sample after a delay and record disagreements.

## Failure checks

- label names or attack IDs accidentally appear in model input
- test paraphrases share the same generation template as training
- all benign examples are shorter or cleaner than attacks
- tool names reveal the answer
- synthetic attacks are much less natural than benign traces

## Artifact

Dataset card, schema, split script, duplicate report, and annotation-decision log.
