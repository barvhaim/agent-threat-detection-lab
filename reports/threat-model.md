# Threat Model

Status: initial scaffold

## System boundary

Document the agent's inputs, retrieved content, model context, tools, permissions, identity, memory, external actions, and audit channels.

## Attack-chain template

1. Attacker and preconditions
2. Entry point
3. Untrusted content or action
4. Trust-boundary crossing
5. Privileged capability used
6. Intended and realized impact
7. Observable telemetry
8. Earliest useful detection point
9. Preventive and detective controls

## Initial research question

Which event or event sequence provides the earliest reliable signal of unsafe tool use without creating unacceptable alert volume?
