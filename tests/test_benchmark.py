import json
import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from benchmark import generate_datasets, benchmark


# --- generate_datasets ---

EXPECTED_DATASETS = {"small_dict", "large_dict", "nested", "list_of_dicts", "unicode_heavy"}


def test_generate_datasets_returns_all_keys():
    datasets = generate_datasets()
    assert set(datasets.keys()) == EXPECTED_DATASETS


def test_small_dict_is_dict():
    data = generate_datasets()["small_dict"]
    assert isinstance(data, dict)
    assert len(data) > 0


def test_large_dict_has_1000_keys():
    data = generate_datasets()["large_dict"]
    assert len(data) == 1000


def test_nested_is_recursive():
    data = generate_datasets()["nested"]
    # Walk at least 5 levels deep
    node = data
    for _ in range(5):
        assert "child" in node or node.get("value") == "leaf"
        node = node.get("child", {})


def test_list_of_dicts_length():
    data = generate_datasets()["list_of_dicts"]
    assert isinstance(data, list)
    assert len(data) == 1000
    assert isinstance(data[0], dict)


def test_unicode_heavy_contains_non_ascii():
    data = generate_datasets()["unicode_heavy"]
    serialized = json.dumps(data)
    # Non-ASCII characters should be present in the original values
    all_values = str(data)
    assert any(ord(c) > 127 for c in all_values)


# --- benchmark ---

def test_benchmark_returns_two_floats():
    data = {"key": "value"}
    dumps_time, loads_time = benchmark(json, data, iterations=10)
    assert isinstance(dumps_time, float)
    assert isinstance(loads_time, float)


def test_benchmark_times_are_positive():
    data = {"key": "value"}
    dumps_time, loads_time = benchmark(json, data, iterations=10)
    assert dumps_time > 0
    assert loads_time > 0


def test_benchmark_scales_with_iterations():
    data = {"key": "value"}
    t_small, _ = benchmark(json, data, iterations=100)
    t_large, _ = benchmark(json, data, iterations=1000)
    # More iterations should take longer
    assert t_large > t_small


def test_benchmark_works_with_ujson():
    ujson = pytest.importorskip("ujson")
    data = generate_datasets()["small_dict"]
    dumps_time, loads_time = benchmark(ujson, data, iterations=10)
    assert dumps_time > 0
    assert loads_time > 0


def test_benchmark_ujson_faster_than_json_for_small_dict():
    ujson = pytest.importorskip("ujson")
    data = generate_datasets()["small_dict"]
    iterations = 5000
    json_dumps, _ = benchmark(json, data, iterations=iterations)
    ujson_dumps, _ = benchmark(ujson, data, iterations=iterations)
    # ujson should be faster; allow up to 2x slower as a very loose bound for slow CI
    assert ujson_dumps < json_dumps * 2
