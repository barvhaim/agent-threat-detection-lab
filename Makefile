.PHONY: install test lint benchmark benchmark-smoke links build check

install:
	python -m pip install -e '.[dev]'

test:
	pytest

lint:
	ruff format --check .
	ruff check .
	python -m mypy src/agent_threat_detection

benchmark:
	agent-threat-benchmark

benchmark-smoke:
	agent-threat-benchmark --examples-per-group 3 --bootstrap-samples 20 		--output-dir /tmp/agent-threat-benchmark/artifacts 		--dataset-path /tmp/agent-threat-benchmark/data/traces.jsonl 		--reports-dir /tmp/agent-threat-benchmark/reports

links:
	python scripts/check_markdown_links.py .

build:
	python -m build

check: lint test benchmark-smoke links build
