# Week 10: Monitoring and Feedback

## Goal

Detect when model, data, upstream systems, or attackers change.

## Required reading

- [Production monitoring guide](../docs/concepts/production-monitoring.md)
- [Evidently monitoring overview](https://www.evidentlyai.com/ml-in-production/model-monitoring)
- [OpenTelemetry GenAI conventions repository](https://github.com/open-telemetry/semantic-conventions-genai)

## Monitor four layers

1. system health: errors, timeouts, latency, saturation
2. data health: schema, missingness, volume, source and feature drift
3. model behavior: score distribution, abstention, threshold crossings, slice drift
4. security outcome: analyst overrides, confirmed incidents, miss rate, detection delay, blast radius

## Exercise

Simulate one upstream schema change, one benign distribution shift, and one adaptive attack shift. Define alerts, fallback, rollback, and labeling actions.

## Deliverable

`reports/production-readiness.md` with an owner and action for every alert.
