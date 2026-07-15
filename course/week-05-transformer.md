# Week 5: Fine-Tune a Small Transformer

## Goal

Test whether a compact encoder adds robust signal beyond classical baselines.

## Required reading

- [Hugging Face text classification](https://huggingface.co/docs/transformers/en/tasks/sequence_classification)
- [Hugging Face Trainer guide](https://huggingface.co/docs/transformers/en/training)
- [Hugging Face model cards](https://huggingface.co/docs/hub/en/model-cards)

## Build

- choose a compact encoder such as DistilBERT or a small DeBERTa variant
- define a trace-to-text representation explicitly
- preserve a grouped out-of-distribution split
- record seed, tokenizer, checkpoint, package versions, and dataset version
- compare class weighting, hard-negative mining, and threshold tuning

## Acceptance criteria

The transformer must beat the strongest simpler baseline on a predeclared important slice or operational objective. Aggregate accuracy is not enough.

## Deliverable

A reproducible command, saved configuration, model card, latency measurement, and error comparison.
