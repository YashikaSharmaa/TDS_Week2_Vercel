from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import json
import os

# Load telemetry data
with open(os.path.join(os.path.dirname(__file__), "../telemetry.json")) as f:
    telemetry = json.load(f)

app = FastAPI()

# Enable CORS for POST from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class TelemetryRequest(BaseModel):
    regions: list
    threshold_ms: float

@app.post("/")
def metrics(req: TelemetryRequest):
    result = {}
    for region in req.regions:
        region_data = [r for r in telemetry if r["region"] == region]
        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime"] for r in region_data]

        avg_latency = float(np.mean(latencies)) if latencies else None
        p95_latency = float(np.percentile(latencies, 95)) if latencies else None
        avg_uptime = float(np.mean(uptimes)) if uptimes else None
        breaches = sum(1 for l in latencies if l > req.threshold_ms)

        result[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }

    return result
