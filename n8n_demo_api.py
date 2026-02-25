"""
Random Number Generator API for n8n Workflows

This API mimics the Domino API pattern for integration with n8n agentic workflows.
Demonstrates how Posit Connect can replace Domino as the compute backend.

Deploy to Posit Connect:
    rsconnect deploy fastapi --entrypoint n8n_demo_api:app .

Example curl request:
    curl -X POST https://connect.example.com/content/abc123/model \
      -H "Authorization: Key YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"data": {"min": 1, "max": 100}}'
"""

import time
import random
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Random Number Generator API",
    description="Demo API for n8n Agentic Workflows - Posit Connect Deployment",
    version="1.0"
)

# Define the expected input schema (matching Domino pattern)
class DataPayload(BaseModel):
    min: int
    max: int

class RequestPayload(BaseModel):
    data: DataPayload


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Random Number Generator API for n8n Workflows",
        "version": "1.0",
        "endpoints": {
            "model": "/model (POST)",
            "health": "/health (GET)"
        },
        "deployment": "Posit Connect"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "random-number-generator",
        "platform": "Posit Connect"
    }


@app.post("/model")
async def generate_number(
    payload: RequestPayload,
    authorization: Optional[str] = Header(None)
):
    """
    Generate a random number within the specified range.

    Mimics Domino API response format for n8n compatibility.

    Request body:
        {
            "data": {
                "min": 1,
                "max": 100
            }
        }

    Response format (Domino-compatible):
        {
            "release": {
                "harness_version": "Posit Connect",
                "model_version": "1.0",
                "model_version_number": 1
            },
            "request_id": "connect-request",
            "result": {
                "number": 42.13
            },
            "timing": {
                "model_time_ms": 1.73
            }
        }
    """
    start_time = time.time()

    # Validate input range
    if payload.data.min >= payload.data.max:
        raise HTTPException(
            status_code=400,
            detail="min must be less than max"
        )

    # Generate random number based on n8n input parameters
    val = random.uniform(payload.data.min, payload.data.max)

    calc_time_ms = (time.time() - start_time) * 1000

    # Return the exact JSON structure Domino previously provided
    # This ensures n8n workflows remain compatible
    return {
        "release": {
            "harness_version": "Posit Connect",
            "model_version": "1.0",
            "model_version_number": 1
        },
        "request_id": "connect-request",
        "result": {
            "number": round(val, 2)
        },
        "timing": {
            "model_time_ms": round(calc_time_ms, 2)
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
