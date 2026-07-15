# Lab 1: Threat to Trainable Signal

## Goal

Convert one threat into an attack chain, observable telemetry, candidate labels, and controls.

## Steps

1. Choose an authorized workflow involving untrusted content and at least one tool.
2. Draw inputs, context assembly, model, tools, identity, permissions, memory, outputs, and logs.
3. Mark trust boundaries.
4. Complete `templates/attack-chain.md`.
5. List signals at content, behavior, policy, and impact stages.
6. Decide which signal is a model feature, a deterministic control, or investigation context.
7. Write three benign lookalikes that should not alert.

## Acceptance criteria

- attacker and preconditions are explicit
- attack goal differs from user goal
- privileged action and impact are separate
- evidence exists before or at the decision point
- at least one mitigation operates outside the model
- the scenario uses synthetic or authorized data
