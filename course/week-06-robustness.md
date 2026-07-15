# Week 6: Long Traces and Adversarial Robustness

## Goal

Determine whether the detector recognizes the behavior rather than memorizing attack phrasing.

## Read

- [AgentDojo](https://arxiv.org/abs/2406.13352) for stateful utility and security evaluation
- [Agent Security Bench](https://arxiv.org/abs/2410.02644) for a broader preprint benchmark
- [Google layered prompt-injection defense](https://blog.google/security/mitigating-prompt-injection-attacks)

## Robustness matrix

Test each important attack under:

- paraphrase and translation
- typographic and encoding changes
- long benign context before the payload
- nested quoted content
- delayed or triggered instructions
- conflicting tool outputs
- benign documents containing security vocabulary
- unseen tools with known capability types

## Build

Add chunking or event-level encoding, aggregation, evidence-event attribution, and robustness slices. Separate model failure from missing context and missing policy.

## Deliverable

`reports/robustness-and-error-analysis.md` with controlled transformations and before/after results.
