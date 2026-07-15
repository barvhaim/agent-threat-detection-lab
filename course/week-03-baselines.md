# Week 3: Rules and Classical ML Baselines

## Goal

Establish interpretable performance and latency floors before adding complex models.

## Required reading

- [scikit-learn text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
- [scikit-learn logistic regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
- [scikit-learn inspection tools](https://scikit-learn.org/stable/inspection.html)

## Build

1. Extend the rules detector with explicit policy inputs.
2. Build TF-IDF plus logistic regression for content classification.
3. Add structured features such as tool, destination class, permission scope, memory write, and trace length.
4. Save configuration, dataset hash, split version, seed, and runtime.

## Comparison questions

- Does the model improve an important attack family or only aggregate F1?
- Which errors can a deterministic policy prevent more safely?
- Which features might encode environment-specific leakage?
- Can an analyst understand why the system alerted?

## Deliverable

`reports/baseline-benchmark.md` with rules, majority baseline, text model, and structured-feature model.
