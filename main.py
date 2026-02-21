import json
import timeit
import ujson
from typing import Any, Dict, Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator

app = FastAPI(title="JSON vs ujson Benchmark Tool")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BenchmarkRequest(BaseModel):
    payload: Union[Dict[str, Any], list]
    iterations: int = Field(default=1000, ge=1, le=10000)

    @validator("payload")
    def validate_payload_size(cls, v):
        # Rough check: serialize to see size
        size = len(json.dumps(v))
        if size > 1_000_000:  # 1MB limit
            raise ValueError("Payload too large (max 1MB)")
        return v

def run_benchmark(lib, data, iterations):
    serialized = lib.dumps(data)
    
    # Warm up
    lib.dumps(data)
    lib.loads(serialized)
    
    dumps_time = timeit.timeit(lambda: lib.dumps(data), number=iterations)
    loads_time = timeit.timeit(lambda: lib.loads(serialized), number=iterations)
    
    return dumps_time, loads_time

@app.post("/benchmark")
async def benchmark_endpoint(request: BenchmarkRequest):
    try:
        json_dumps, json_loads = run_benchmark(json, request.payload, request.iterations)
        ujson_dumps, ujson_loads = run_benchmark(ujson, request.payload, request.iterations)
        
        return {
            "iterations": request.iterations,
            "results": {
                "dumps": {
                    "json": round(json_dumps, 6),
                    "ujson": round(ujson_dumps, 6),
                    "speedup": round(json_dumps / ujson_dumps, 2)
                },
                "loads": {
                    "json": round(json_loads, 6),
                    "ujson": round(ujson_loads, 6),
                    "speedup": round(json_loads / ujson_loads, 2)
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
