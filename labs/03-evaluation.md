# Lab 3: From Score to Decision

## Goal

Select thresholds based on security and operational costs rather than a default of 0.5.

## Steps

1. Produce a validation file with trace ID, label, score, threat slice, and severity.
2. Plot or tabulate precision, recall, false-positive rate, and review volume across thresholds.
3. Define separate thresholds for alert and block.
4. Add an abstention range for analyst review.
5. Calculate results by important slice.
6. Check calibration using a reliability diagram and Brier score.
7. Bootstrap the primary metric to show uncertainty.
8. Freeze thresholds before opening the final test set.

## Decision memo

Document traffic assumptions, incident cost, alert-review cost, miss cost, latency budget, chosen thresholds, expected volume, rollback trigger, and known blind spots.

## Warning

The sample scorer in this repository accepts binary predictions and teaches record alignment. It does not replace threshold curves, probability calibration, or representative evaluation.
