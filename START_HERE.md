# Start Here

This repository teaches one practical skill: turning an AI-agent threat into a detector that can be evaluated and operated responsibly.

## Choose your route

### I am new to agent security

1. Complete [Lab 0](labs/00-first-15-minutes.md).
2. Read [Agent security as system security](docs/concepts/detection-architecture.md).
3. Complete weeks 1 through 4 in the [course syllabus](course/syllabus.md).
4. Record evidence in the [progress log](templates/progress-log.md).

### I know security but need applied ML practice

Start at [Week 2](course/week-02-data-and-labels.md), then focus on weeks 3 through 6 and the [evaluation playbook](docs/concepts/evaluation-playbook.md).

### I know ML but need agent-security depth

Start at [Week 1](course/week-01-agent-security.md), use the [benchmark guide](resources/benchmarks-and-datasets.md), then complete weeks 7, 8, and 11.

### I want a portfolio project

Read the [capstone brief](capstone/brief.md), run Lab 0, and work through the weekly acceptance criteria. Do not claim benchmark or production readiness until the relevant checklists are complete.

## First 15 minutes

Requirements:

- Python 3.10 or newer
- CPU only
- no API key
- no model download
- expected cost: zero

Run:

```bash
PYTHONPATH=src python examples/run_baseline.py
PYTHONPATH=src python scripts/score_predictions.py   --expected data/sample_labels.jsonl   --predicted data/sample_predictions.jsonl
```

Expected behavior:

- the benign trace is allowed
- the two attack traces are blocked
- the toy scorer reports 2 true positives, 1 true negative, and no errors

The fixture is intentionally tiny. A perfect score proves that the teaching pipeline is wired correctly, not that the detector is good.

## What not to do first

- Do not fine-tune a large model before defining the threat and labels.
- Do not use random train/test splits when attack templates repeat.
- Do not use accuracy as the primary metric for rare attacks.
- Do not use an LLM judge without testing stability and injection resistance.
- Do not treat a benchmark score as a production-readiness claim.
- Do not run security tests against systems you do not own or have permission to test.
