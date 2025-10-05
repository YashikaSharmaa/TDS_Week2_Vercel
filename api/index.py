from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import json
import os

# Path to telemetry data
DATA_PATH = os.path.join(os.path.dirname(__file__), "telemetry.json")
with open(DATA_PATH) as f:
    telemetry = json.load(f)

app = FastAPI()

# Enable CORS for all origins
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
def compute_metrics(req: TelemetryRequest):
    result = {}

    for region in req.regions:
        # Filter telemetry records by region
        region_data = [r for r in telemetry if r["region"] == region]

        if not region_data:
            result[region] = None
            continue

        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime_pct"] for r in region_data]

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(np.mean(uptimes))
        breaches = sum(1 for l in latencies if l > req.threshold_ms)

        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 3),
            "breaches": breaches
        }

    return result
