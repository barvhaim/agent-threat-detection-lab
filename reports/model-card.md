# Model Card: Hybrid Logistic Baseline

## Intended use

Research baseline for binary attack detection in structured AI-agent traces. It combines word and character TF-IDF with event, trust, tool, and destination features.

## Not intended for

Production blocking, autonomous incident response, attribution, malware detection, or claims about real-world attack prevalence.

## Training and evaluation data

- synthetic records: 960
- isolated template groups: 80
- split policy: language template groups are isolated across train/calibration/validation/test
- calibration: Platt scaling on held-out calibration split

## Untouched test result

- precision: 0.821192
- recall: 0.861111
- F1: 0.840678
- false-positive rate: 0.28125
- average precision: 0.950428
- Brier score: 0.107867
- selected threshold: 0.292793

## Explainability

`artifacts/benchmark/results.json` records largest signed logistic coefficients. Association in generated data is not causal security importance.

## Known risks

Generator artifacts, stable schemas, adversarial paraphrase, multilingual input, malformed events, policy drift, and confidence shift outside this distribution.

## Release gate

Do not enable blocking until representative traces meet precision, critical-family recall, latency, review-budget, privacy, and rollback gates.
