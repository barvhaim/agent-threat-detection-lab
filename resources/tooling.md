# Tooling Map

Use tools when they solve a current problem, not as a checklist.

## Core, low dependency

- Python standard library for fixtures, schemas, metrics, and CLI smoke tests
- pytest or unittest for behavior and golden cases
- Ruff for static checks
- Git and CI for versioned evidence

## Classical ML

- scikit-learn for TF-IDF, logistic regression, calibration, metrics, grouped splitting, and inspection
- imbalanced-learn only after understanding how resampling changes the training distribution

## Deep learning

- PyTorch for training control
- Hugging Face Datasets for typed schemas and processing
- Transformers for compact sequence classifiers
- Evaluate or direct scikit-learn metrics for reproducible scoring

## LLM and agent evaluation

- provider structured-output APIs for schema-constrained experiments
- Inspect AI for tasks, scorers, sandboxes, limits, approvals, and agent evaluations
- AgentDojo for stateful prompt-injection research

## Experiment and operations

- MLflow or Weights & Biases for experiment tracking
- FastAPI for a small versioned service
- Docker for packaging
- OpenTelemetry for traces and metrics, with a pinned semantic-convention version
- Evidently or custom reports for drift and data-quality checks

## Security controls

- policy engine or explicit code for deterministic authorization
- secret scanning and dependency scanning in CI
- data classification and redaction before model or telemetry exposure
- sandboxing and human approval for high-impact agent tools
