# Week 4: Operational Evaluation

## Goal

Turn offline scores into explicit allow, alert, review, and block decisions.

## Required reading

- [scikit-learn precision-recall example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html)
- [scikit-learn probability calibration](https://scikit-learn.org/stable/modules/calibration.html)
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Evaluation playbook](../docs/concepts/evaluation-playbook.md)

## Build

- precision-recall and calibration curves
- Brier score and expected calibration error
- bootstrap confidence intervals
- cost matrix for misses, alerts, review, and execution
- threshold selection using validation data only
- abstention and human-review routing
- slices by threat, tool, source, language, severity, and trace length

## Deliverable

A threshold memo that answers: which cases are blocked, reviewed, alerted, or allowed, and why?

## Self-check

- Why may ROC-AUC hide poor rare-event performance?
- What does a calibrated score of 0.8 mean?
- Why is one global F1 threshold often inappropriate?
