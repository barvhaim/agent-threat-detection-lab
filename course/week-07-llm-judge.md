# Week 7: Structured LLM Detection

## Goal

Evaluate an LLM detector as an untrusted, variable component rather than an oracle.

## Required reading

- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Structured-output evaluation example](https://developers.openai.com/cookbook/examples/evaluation/use-cases/structured-outputs-evaluation)
- [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)

## Output contract

Require a validated schema containing label, severity, confidence, evidence event IDs, applicable policy, and abstention reason. Do not accept free-form prose as the only result.

## Threat model the judge

- untrusted tool output attempts to instruct the judge
- malformed or excessively long traces
- model or provider version changes
- nondeterministic labels across repeated calls
- rationale that cites nonexistent evidence
- sensitive content copied into logs

## Deliverable

A benchmark against the best small model covering quality, repeated-call stability, injection resistance, schema-validity rate, latency, and cost.
