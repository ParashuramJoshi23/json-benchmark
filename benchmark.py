#!/usr/bin/env python3
"""Benchmark: stdlib json vs ujson for serialization and deserialization."""

import json
import sys
import timeit

try:
    import ujson
except ImportError:
    print("ujson not found. Install it with: pip install ujson")
    sys.exit(1)


def generate_datasets():
    small_dict = {f"key_{i}": f"value_{i}" for i in range(10)}
    small_dict.update({"count": 42, "active": True, "ratio": 3.14})

    large_dict = {f"field_{i}": i * 1.5 for i in range(1000)}

    def make_nested(depth):
        if depth == 0:
            return {"value": "leaf", "count": 0}
        return {"level": depth, "data": [1, 2, 3], "child": make_nested(depth - 1)}

    nested = make_nested(5)

    list_of_dicts = [
        {"id": i, "name": f"user_{i}", "score": i * 0.1, "active": i % 2 == 0}
        for i in range(1000)
    ]

    unicode_heavy = {
        "greeting": "こんにちは世界",
        "emoji": "Hello 🌍🎉🚀",
        "arabic": "مرحبا بالعالم",
        "mixed": [f"item_{i}_αβγ" for i in range(50)],
        "chinese": "中文字符测试",
    }

    return {
        "small_dict": small_dict,
        "large_dict": large_dict,
        "nested": nested,
        "list_of_dicts": list_of_dicts,
        "unicode_heavy": unicode_heavy,
    }


def benchmark(module, data, iterations=10_000):
    serialized = module.dumps(data)

    # Warm up
    module.dumps(data)
    module.loads(serialized)

    dumps_time = timeit.timeit(lambda: module.dumps(data), number=iterations)
    loads_time = timeit.timeit(lambda: module.loads(serialized), number=iterations)

    return dumps_time, loads_time


def main():
    iterations = 10_000
    datasets = generate_datasets()

    col_dataset = 18
    col_op = 12
    col_time = 11
    col_speedup = 9
    total_width = col_dataset + col_op + col_time * 2 + col_speedup

    print(f"\nJSON vs ujson Benchmark  ({iterations:,} iterations each)")
    print("=" * total_width)
    print(
        f"{'Dataset':<{col_dataset}}{'Operation':<{col_op}}"
        f"{'json (s)':>{col_time}}{'ujson (s)':>{col_time}}{'Speedup':>{col_speedup}}"
    )
    print("-" * total_width)

    for name, data in datasets.items():
        json_dumps, json_loads = benchmark(json, data, iterations)
        ujson_dumps, ujson_loads = benchmark(ujson, data, iterations)

        dumps_speedup = json_dumps / ujson_dumps
        loads_speedup = json_loads / ujson_loads

        print(
            f"{name:<{col_dataset}}{'dumps':<{col_op}}"
            f"{json_dumps:>{col_time}.4f}{ujson_dumps:>{col_time}.4f}"
            f"{dumps_speedup:>{col_speedup}.2f}x"
        )
        print(
            f"{'':<{col_dataset}}{'loads':<{col_op}}"
            f"{json_loads:>{col_time}.4f}{ujson_loads:>{col_time}.4f}"
            f"{loads_speedup:>{col_speedup}.2f}x"
        )
        print()


if __name__ == "__main__":
    main()
