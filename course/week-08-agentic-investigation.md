# Week 8: Bounded Agentic Investigation

## Goal

Use an investigator only when additional context can resolve a defined uncertainty.

## Required reading

- [Inspect agents](https://inspect.aisi.org.uk/agents.html)
- [Inspect tool approval](https://inspect.aisi.org.uk/approval.html)
- [Inspect sandboxing](https://inspect.aisi.org.uk/sandboxing.html)
- [MITRE ATLAS data: AI Agent Tool Invocation, AML.T0053](https://github.com/mitre-atlas/atlas-data)

## Design constraints

- read-only tools by default
- allowlisted policy, identity, capability, and trace lookups
- explicit step, token, time, and cost limits
- no secrets in model-visible context unless necessary and authorized
- deterministic policy enforcement after investigation
- complete trace of evidence retrieval

## Experiment

Compare a non-agentic LLM judge with the investigator on cases whose answer requires policy or identity lookup. Run an ablation for each tool.

## Deliverable

`reports/cascade-ablation.md`. Remove the investigator if it does not improve a predeclared hard slice enough to justify complexity.
