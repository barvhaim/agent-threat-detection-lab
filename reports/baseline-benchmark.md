# Baseline Benchmark

> Reproducible synthetic benchmark. It validates methodology and code, not production performance.

## Experimental protocol

- Records: **960**
- Template groups: **80**
- Splits: `{'calibration': 240, 'test': 240, 'train': 240, 'validation': 240}`
- Language-template groups are disjoint across all four splits.
- Calibration and threshold selection occur before test evaluation.
- Threshold policy: maximize validation recall subject to precision floor.
- Confidence intervals resample template groups rather than rows.

## Test results

| Model | Precision | Recall | F1 | FPR | AP | Brier | ECE | ms/trace |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `majority` | 0.000 | 0.000 | 0.000 | 0.000 | 0.600 | 0.240 | 0.000 | 0.000 |
| `rules` | 1.000 | 0.250 | 0.400 | 0.000 | 0.700 | 0.407 | 0.415 | 0.009 |
| `tfidf_logreg` | 0.822 | 0.833 | 0.828 | 0.271 | 0.942 | 0.118 | 0.086 | 0.449 |
| `hybrid_logreg` | 0.821 | 0.861 | 0.841 | 0.281 | 0.950 | 0.108 | 0.041 | 0.482 |

## Operating points

### majority

- threshold: `1.0`
- validation precision / recall: `1.0` / `0.0`
- test F1 95% group-bootstrap interval: `0.0` to `0.0`
- confusion matrix: TP=0, FP=0, FN=144, TN=96

### rules

- threshold: `0.95`
- validation precision / recall: `1.0` / `0.25`
- test F1 95% group-bootstrap interval: `0.269231` to `0.5`
- confusion matrix: TP=36, FP=0, FN=108, TN=96

### tfidf_logreg

- threshold: `0.363395`
- validation precision / recall: `0.912409` / `0.868056`
- test F1 95% group-bootstrap interval: `0.623021` to `0.96`
- confusion matrix: TP=120, FP=26, FN=24, TN=70

### hybrid_logreg

- threshold: `0.292793`
- validation precision / recall: `0.902778` / `0.902778`
- test F1 95% group-bootstrap interval: `0.646731` to `0.960074`
- confusion matrix: TP=124, FP=27, FN=20, TN=69

## Stress tests

Thresholds are frozen and no model is refit on these transformations.

| Model | Shift | Precision | Recall | F1 | F1 delta |
|---|---|---:|---:|---:|---:|
| `majority` | `long_context` | 0.000 | 0.000 | 0.000 | +0.000 |
| `majority` | `missing_arguments` | 0.000 | 0.000 | 0.000 | +0.000 |
| `majority` | `unseen_tool_names` | 0.000 | 0.000 | 0.000 | +0.000 |
| `rules` | `long_context` | 1.000 | 0.250 | 0.400 | +0.000 |
| `rules` | `missing_arguments` | 1.000 | 0.167 | 0.286 | -0.114 |
| `rules` | `unseen_tool_names` | 0.000 | 0.000 | 0.000 | -0.400 |
| `tfidf_logreg` | `long_context` | 0.600 | 1.000 | 0.750 | -0.078 |
| `tfidf_logreg` | `missing_arguments` | 0.696 | 0.889 | 0.780 | -0.047 |
| `tfidf_logreg` | `unseen_tool_names` | 0.706 | 0.882 | 0.784 | -0.044 |
| `hybrid_logreg` | `long_context` | 0.600 | 1.000 | 0.750 | -0.091 |
| `hybrid_logreg` | `missing_arguments` | 0.783 | 0.903 | 0.839 | -0.002 |
| `hybrid_logreg` | `unseen_tool_names` | 0.600 | 1.000 | 0.750 | -0.091 |

## Model-selection decision

- Hybrid blocking precision gate: **FAIL**.
- Validation precision was `0.902778`, while test precision was `0.821192`.
- Keep deterministic high-confidence rules for blocking.
- Keep the hybrid in shadow or analyst-review mode until representative data passes.
- Compare any LLM judge against these frozen baselines before adoption.

## Limitations

- All traces are synthetic and share a controlled generator.
- Template isolation does not reproduce organic enterprise distributions.
- Stress transformations are controlled probes, not adaptive red-team attacks.
- Latency is local CPU inference, not service-level p95 latency.
- The binary target collapses impact and severity classes.
