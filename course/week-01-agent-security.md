# Week 1: Agent Security and Threat Modeling

## Goal

Model the complete system around an agent and identify where an attack becomes observable.

## Required reading

- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
- [MITRE ATLAS matrix: LLM Prompt Injection, AML.T0051](https://atlas.mitre.org)
- [MITRE ATLAS data: AI Agent Tool Invocation, AML.T0053](https://github.com/mitre-atlas/atlas-data)
- [NIST adversarial ML taxonomy](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)

## Mental model

An agent is not only an LLM. It is a model plus instructions, retrieved data, tools, permissions, identity, memory, workflow state, and output channels. A detector can operate at several boundaries:

1. content enters context
2. the model chooses a tool
3. arguments cross a policy boundary
4. a tool changes external state
5. data leaves the organization
6. memory persists an instruction

## Exercise

Complete [Lab 1](../labs/01-threat-model.md). Write six attack chains using the template in `templates/attack-chain.md`.

## Deliverable

Update `reports/threat-model.md` with a system diagram, trust boundaries, attacker assumptions, telemetry, and the earliest useful detection point.

## Self-check

- Can you distinguish direct injection, indirect injection, jailbreak, and tool misuse?
- Can you explain why malicious text and malicious impact are different labels?
- Can you name one control that must operate outside the model?
