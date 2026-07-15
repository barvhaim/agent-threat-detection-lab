# Capstone: Agent Threat Detection System

## Mission

Build and defend an end-to-end decision system for structured agent traces. Compare rules, classical ML, a compact transformer, a structured LLM judge, and an optional bounded investigator.

## Required threat coverage

- benign workflow
- direct or indirect prompt injection
- tool misuse
- sensitive-data exfiltration
- memory or context poisoning
- identity or privilege abuse

## Required evidence

1. system threat model and trust boundaries
2. dataset card, annotation guide, and grouped split
3. transparent baseline
4. model comparison with calibration and slices
5. robustness evaluation against unseen constructions
6. latency and cost comparison
7. versioned service contract and golden tests
8. monitoring, feedback, and rollback design
9. model-selection memo stating what was rejected and why

## Required demo

Show one legitimate workflow and one attack chain. Display content, behavior, policy, and impact signals. Explain which control blocks the action and which model outputs are advisory.

## Grading rubric

| Area | Strong evidence |
|---|---|
| threat model | explicit attacker, boundaries, capabilities, and impact |
| data | provenance, ambiguity, leakage checks, and OOD split |
| modeling | simple baselines and justified complexity |
| evaluation | operational thresholds, calibration, slices, and uncertainty |
| security | authorized tests, deterministic enforcement, minimized data exposure |
| production | tested service, monitoring actions, fallback, and rollback |
| communication | reproducible commands, honest limits, concise decisions |
