# Week 2: Data, Labels, and Leakage

## Goal

Build a dataset whose score means something outside the exact prompts used to create it.

## Required reading

- [Hugging Face dataset features](https://huggingface.co/docs/datasets/en/about_dataset_features)
- [AgentDojo paper](https://arxiv.org/abs/2406.13352)
- [InjecAgent repository](https://github.com/uiuc-kang-lab/InjecAgent)
- [BIPIA repository](https://github.com/microsoft/BIPIA)

## Key concepts

- **Unit of analysis:** message, event, tool call, trace, session, or incident.
- **Label target:** malicious content, unsafe intent, policy violation, or realized impact.
- **Provenance:** where the trace and attack pattern came from.
- **Group identifier:** source, attack family, template, actor, campaign, or environment.
- **Adjudication:** how ambiguous labels are resolved.
- **Leakage:** train and test share wording or structure that makes generalization look better than it is.

## Exercise

Complete [Lab 2](../labs/02-dataset-design.md). Create at least 40 traces across benign and adversarial families, then split by attack template or source rather than by row.

## Deliverable

A dataset card, annotation guide, schema validation, duplicate report, and grouped split script.

## Self-check

- What is the difference between a hard negative and an unlabeled attack?
- Why can a cross-product benchmark overstate dataset size?
- Which fields must never be fed to the model because they leak the answer?
