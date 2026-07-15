# Production Monitoring for Agent Threat Detectors

## Why offline evaluation is insufficient

Attackers adapt, agent tools change, permissions drift, model providers update behavior, and labels arrive late. Monitoring must cover software, data, models, and security outcomes.

## Minimum event record

Capture a privacy-reviewed subset of:

- trace and event identifiers
- timestamp and environment
- detector and policy versions
- tool and capability category
- identity and permission class
- score, threshold, decision, and abstention
- evidence event identifiers
- latency and cost
- reviewer outcome and incident disposition when available

Avoid logging raw secrets, full private prompts, or unnecessary personal data.

## Drift is a symptom

A changed score or feature distribution does not prove quality degradation. It triggers investigation. Confirm with delayed labels, controlled replay, or targeted annotation.

## Response matrix

| Signal | Possible cause | Response |
|---|---|---|
| schema errors | upstream change | reject safely, alert owner, update contract |
| alert-rate jump | attack, drift, or bug | sample traces, compare slices, enable fallback |
| confidence collapse | unseen patterns | abstain more, label sample, challenge model |
| false-positive increase | benign workflow change | review policy and thresholds, do not blindly retrain |
| miss or incident | coverage failure | preserve trace, add regression case, reassess control layer |
| latency increase | provider or load issue | degrade to cheaper baseline, enforce timeout |

## Rollback criteria

Define a previous known-good model, policy, and schema. Roll back when safety, correctness, latency, or operational-review budgets cross predeclared boundaries.

## Standards note

OpenTelemetry's older GenAI attributes have moved to the dedicated GenAI semantic-conventions repository. Treat current conventions as evolving and version the telemetry contract you actually implement.
