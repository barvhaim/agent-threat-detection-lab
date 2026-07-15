# Model Selection Memo

## Decision

Use deterministic rules for high-confidence blocking. Keep the hybrid logistic model in shadow or analyst-review mode. Do not promote it to automatic blocking.

## Evidence

- rules precision / recall / F1: `1.0` / `0.25` / `0.4`
- hybrid precision / recall / F1: `0.821192` / `0.861111` / `0.840678`
- required blocking precision: `0.9`
- hybrid blocking gate: **FAIL**
- validation-to-test precision: `0.902778` to `0.821192`

## Interpretation

The hybrid materially improves coverage, but its selected threshold does not transfer at the required precision. This gap matters more than aggregate F1.

## Deployment posture

1. Rules may block only explicit high-severity conditions.
2. Hybrid scores create shadow telemetry and analyst-review candidates.
3. Evaluate authorized labels per tool, tenant, language, and attack family.
4. Recalibrate and freeze thresholds before a prospective shadow period.
5. Promote only after precision, recall, volume, latency, and rollback gates pass.

## Rejected alternatives

- Majority: no useful detection capability.
- Rules only: excellent precision but insufficient recall.
- TF-IDF only: slightly weaker than the hybrid without operational advantage.
- LLM judge or investigator: deferred until compared for injection, cost, latency, and stability on the same benchmark.
