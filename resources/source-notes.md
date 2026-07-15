# Research Source Notes

Research date: 2026-07-15

This guide favors primary standards, official documentation, original papers, and project repositories. Vendor material is labeled as practical guidance rather than neutral consensus.

## Security frameworks

### OWASP Top 10 for Agentic Applications 2026

Source: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026

Use it as a risk checklist. Its categories include goal hijacking, tool misuse, identity and privilege abuse, supply-chain issues, code execution, memory and context poisoning, inter-agent communication, cascading failure, human-agent trust, and rogue agents. A top-ten list is not a detector specification; translate each relevant risk into attacker assumptions, telemetry, labels, and controls.

### MITRE ATLAS

Sources:

- https://atlas.mitre.org
- https://github.com/mitre-atlas/atlas-data

ATLAS provides adversary techniques and case studies. The most directly useful entries for this course are LLM Prompt Injection (`AML.T0051`), AI Agent Tool Invocation (`AML.T0053`), and AI Agent Context Poisoning (`AML.T0080`). ATLAS explicitly connects tool invocation to execution and privilege escalation and lists mitigations such as telemetry, permission configuration, human approval, restricting tools on untrusted data, segmentation, and validation. The website's individual technique routes returned 404 to the repository link checker on the research date, so this material links the official matrix and official data repository. Pin an ATLAS data release when freezing a report because the matrix is a living source.

### NIST AI 100-2 E2025

Source: https://csrc.nist.gov/pubs/ai/100/2/e2025/final

NIST provides shared adversarial-ML terminology organized around lifecycle, attacker goals, capabilities, and knowledge. It is useful for disciplined threat descriptions and includes generative-AI concepts such as direct and indirect prompt injection. It is broader than agent runtime detection.

## Benchmarks

### AgentDojo

Sources:

- https://arxiv.org/abs/2406.13352
- https://github.com/ethz-spylab/agentdojo

The paper introduces a stateful environment with 97 realistic tasks and 629 security test cases. Its key methodological contribution is joint utility and security evaluation using environment-state checks. The authors warn that evaluating only default attacks is not enough; adaptive attacks matter. Use it to learn dynamic task design, not as a universal production score.

### InjecAgent

Source: https://github.com/uiuc-kang-lab/InjecAgent

InjecAgent contains 1,054 test cases spanning 17 user tools and 62 attacker tools. It covers direct harm and multi-stage data stealing and reports attack success on valid and all cases. Its scenarios are useful for taxonomy and tool-pair ideas, but its simulated, mostly single-turn construction differs from a stateful production agent.

### BIPIA

Source: https://github.com/microsoft/BIPIA

BIPIA covers indirect injection across email QA, web QA, summarization, table QA, and code QA. It composes clean context with attack content and includes prompt and fine-tuning defenses. Some source datasets require separate download because of licensing; inspect each underlying dataset before redistribution.

### Agent Security Bench

Source: https://arxiv.org/abs/2410.02644

ASB broadens coverage across scenarios, tools, attacks, defenses, and model backbones. Treat its quantitative results as paper-specific and check the current version before reproducing because it is a preprint with evolving versions.

## Defense and evaluation guidance

### Google layered prompt-injection defense

Source: https://blog.google/security/mitigating-prompt-injection-attacks

This is vendor engineering guidance emphasizing defense in depth, including model hardening, input and output classifiers, security policies, system-level safeguards, red teaming, and monitoring. Use it to avoid single-control thinking, not as proof that any layer is sufficient.

### MCP security best practices

Source: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices

The official guide complements MCP authorization and OAuth security guidance. It covers protocol-specific risks including confused-deputy behavior and token handling. Use it when traces involve MCP clients, servers, proxies, authorization, or tool exposure.

### scikit-learn evaluation and calibration

Sources:

- https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html
- https://scikit-learn.org/stable/modules/calibration.html

The official documentation explains precision-recall trade-offs for imbalanced tasks and the interpretation of calibrated probabilities. It also notes that Brier and log loss reflect both calibration and discrimination, so use reliability diagrams and task metrics together.

### OpenAI evaluation best practices

Source: https://developers.openai.com/api/docs/guides/evaluation-best-practices

The guidance recommends task-specific, continuous evaluations and concrete grading criteria. It is useful for LLM detector and structured-output tests. Keep provider-specific tools optional so the core course remains reproducible without credentials.

### Inspect AI

Source: https://inspect.aisi.org.uk

Inspect is an open evaluation framework from the UK AI Security Institute ecosystem. It supports datasets, solvers, scorers, agents, sandboxes, approvals, limits, tracing, and log analysis. Use it in the advanced agent-evaluation phase, not in the first dependency-free lab.

## Modeling and operations

### Hugging Face

Sources:

- https://huggingface.co/docs/datasets/en/about_dataset_features
- https://huggingface.co/docs/transformers/en/tasks/sequence_classification
- https://huggingface.co/docs/evaluate/index

The official documentation covers typed dataset features, text-classification fine-tuning, and evaluation tooling. The generic classification tutorial uses accuracy; this course replaces accuracy-only evaluation with rare-event security metrics and grouped splits.

### Production monitoring

Source: https://www.evidentlyai.com/ml-in-production/model-monitoring

This vendor guide gives a useful distinction among data drift, concept drift, data-quality failure, pipeline bugs, adversarial adaptation, and upstream-model failure. Drift is not automatically a quality failure; pair it with labels or targeted review.

### OpenTelemetry GenAI conventions

Sources:

- https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai
- https://github.com/open-telemetry/semantic-conventions-genai

The main OpenTelemetry registry marks older GenAI attributes as moved or deprecated in favor of the dedicated repository. Version the convention used by your service and review privacy before recording prompts, outputs, or tool arguments.
