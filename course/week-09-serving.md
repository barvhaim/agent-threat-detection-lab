# Week 9: Serving and Release Engineering

## Goal

Package the chosen detector behind a versioned, observable interface.

## Build

- prediction, health, and version endpoints
- explicit request and response schemas
- model loading and startup failure behavior
- timeouts, batching, concurrency, and rate limits
- golden-set regression tests
- container image and dependency scan
- shadow mode before blocking
- redaction and secure logging

## Security requirements

Treat the detector itself as a security-sensitive service. Validate size and shape, avoid arbitrary deserialization, minimize logged content, authenticate callers, and separate model confidence from policy decisions.

## Deliverable

A runnable service plus p50 and p95 latency, throughput, memory, startup time, and failure-mode results.
