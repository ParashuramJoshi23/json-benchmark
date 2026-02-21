# JSON vs ujson Benchmark Web Tool

*2026-02-19T08:29:59Z by Showboat 0.6.0*
<!-- showboat-id: 1131d221-76d5-441e-a689-df800f3508cc -->

The benchmark tool has been rewritten as a web application using FastAPI and a Vanilla CSS/JS frontend. This document demonstrates the API and the verification process.

### 1. API Benchmark\nTesting the `/benchmark` endpoint with a sample payload via curl (Port 8005).

```bash
curl -s -X POST http://localhost:8005/benchmark -H 'Content-Type: application/json' -d '{"payload": {"key": "value", "list": [1,2,3]}, "iterations": 1000}'
```

```output
{"iterations":1000,"results":{"dumps":{"json":0.001167,"ujson":0.000399,"speedup":2.92},"loads":{"json":0.000889,"ujson":0.000439,"speedup":2.02}}}```
```

### 2. Verification\nRunning the project tests to ensure logic consistency.

```bash
./.venv/bin/python3 -m pytest tests/
```

```output
============================= test session starts ==============================
platform darwin -- Python 3.14.2, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/parashuram/projects/json-benchmark
plugins: anyio-4.12.1
collected 11 items

tests/test_benchmark.py ...........                                      [100%]

============================== 11 passed in 0.06s ==============================
```
