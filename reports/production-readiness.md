# Production Readiness

Current verdict: **NOT READY FOR PRODUCTION BLOCKING**

| Gate | Status | Evidence |
|---|---|---|
| Reproducible evaluation | PASS | deterministic generator, seed, and CLI |
| Split leakage checks | PASS | template and normalized-content isolation |
| Held-out calibration | PASS | dedicated calibration split |
| Frozen-threshold test | PASS | untouched test split |
| Blocking precision | FAIL | test precision 0.821192 |
| Representative authorized data | FAIL | synthetic data only |
| Prospective shadow evaluation | FAIL | not run |
| Service load and failure testing | FAIL | model-only latency measured |
| Monitoring and rollback drill | FAIL | design only |
| Privacy and retention review | FAIL | required before real telemetry |

## Promotion criteria

Pass numerical gates for representative precision, critical-family recall, analyst volume, latency, availability, privacy, and rollback. Synthetic F1 is not a gate.
