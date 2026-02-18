# json-benchmark

Benchmarks Python's stdlib `json` module against `ujson` (UltraJSON) for serialization and deserialization across realistic data shapes.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run benchmark

```bash
python benchmark.py
```

## Run tests

```bash
python -m pytest tests/
```

## Project structure

- `benchmark.py` — main benchmark script (`generate_datasets`, `benchmark`, `main`)
- `requirements.txt` — `ujson` dependency
- `tests/test_benchmark.py` — unit tests for dataset generation and timing logic
