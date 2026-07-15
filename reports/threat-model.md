# Threat Model

## System boundary

The modeled system receives a user goal, retrieves content from an external or semi-trusted source, gives ordered events to an agent, and allows the agent to select a tool with arguments. The detector observes the trace before or around tool execution. It does not control the model provider, source content, identity provider, tool implementation, or destination system.

## Assets

- credentials and private data accessible through tools
- authorization scope attached to the user or service identity
- durable memory and policy state
- integrity of external actions
- analyst attention and benign-workflow availability

## Attacker capabilities

The attacker may place instructions in retrieved content, influence tool arguments, request an external destination, exploit over-privileged identity, or attempt a persistent memory change. The benchmark does not assume model-weight access, host compromise, or control of the deterministic enforcement layer.

## Attack chains

| Family | Entry | Privileged transition | Intended impact | Observable evidence |
|---|---|---|---|---|
| Prompt injection | untrusted document or message | model adopts external objective | task or policy hijack | source trust, instruction language, goal mismatch |
| Data exfiltration | malicious retrieved content | send/upload tool crosses boundary | private data leaves system | data class, destination, tool, arguments |
| Privilege abuse | external request | role or shell capability exceeds scope | unauthorized control | identity, approval, capability, arguments |
| Memory poisoning | untrusted instruction | durable write affects future runs | persistent behavior change | memory-write tool, source, key/value, later activation |

## Trust boundaries

1. external source to retrieved context
2. model plan to tool-selection request
3. tool request to authorization and policy gate
4. tool result to external state or destination
5. current trace to durable memory

## Control allocation

- Deterministic policy should enforce identity, scope, destination, approval, and high-impact actions.
- Statistical models may rank ambiguous traces for review and identify unfamiliar language patterns.
- LLM judges are untrusted components and require schema validation, injection tests, cost and latency limits, and deterministic post-policy.
- Impact telemetry confirms state change and supplies delayed labels.

## Research question

Which combination of content, behavior, and policy signals yields useful recall under a strict false-positive budget when language templates, tool names, and telemetry completeness shift?

## Out of scope

Malware execution, model theft, training-time poisoning, cryptographic compromise, network intrusion, and production incident-rate estimation.
