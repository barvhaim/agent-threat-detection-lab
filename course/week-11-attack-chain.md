# Week 11: End-to-End Attack-Chain Detection

## Goal

Compare detection points across one complete indirect-injection chain.

## Scenario

A malicious instruction enters through an email, ticket, document, or tool output. The agent reads it during a legitimate task, invokes a privileged tool, and attempts an external action or memory write.

## Detect at four stages

1. content detector: suspicious instruction language
2. behavior detector: unexpected tool choice or sequence
3. policy detector: unauthorized identity, scope, destination, or action
4. impact detector: sensitive data or state actually changed

## Measure

- attack success and benign utility
- time to detect
- evidence quality
- false-positive burden
- prevention versus detection
- blast-radius reduction

## Deliverable

A five-minute demo and one-page decision explaining which signals are useful alone, which require correlation, and which controls must remain deterministic.
