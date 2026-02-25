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
    description="""
## n8n + Posit Connect Integration Demo

This API demonstrates how Posit Connect can replace Domino for n8n agentic workflows.

### Features
* **Domino-Compatible Format**: Maintains exact response structure from Domino
* **n8n Integration**: Drop-in replacement for existing workflows
* **Simple Demo**: Random number generation for testing

### Authentication
Use API keys created in Posit Connect:
```
Authorization: Key YOUR_API_KEY
```

### Example Usage
```bash
curl -X POST /model \\
  -H "Authorization: Key YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"data": {"min": 1, "max": 100}}'
```
    """,
    version="1.0.0",
    contact={
        "name": "Posit Demo Team",
        "email": "demo@posit.co"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# Define the expected input schema (matching Domino pattern)
class DataPayload(BaseModel):
    """Input parameters for random number generation."""
    min: int = 1
    max: int = 100

    class Config:
        json_schema_extra = {
            "example": {
                "min": 1,
                "max": 100
            }
        }

class RequestPayload(BaseModel):
    """Domino-compatible request wrapper."""
    data: DataPayload

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "min": 1,
                    "max": 100
                }
            }
        }

# Response models for Swagger documentation
class ReleaseInfo(BaseModel):
    """Release and version information."""
    harness_version: str = "Posit Connect"
    model_version: str = "1.0"
    model_version_number: int = 1

class ResultData(BaseModel):
    """Generated random number result."""
    number: float

class TimingInfo(BaseModel):
    """Performance timing information."""
    model_time_ms: float

class ModelResponse(BaseModel):
    """Complete API response matching Domino format."""
    release: ReleaseInfo
    request_id: str = "connect-request"
    result: ResultData
    timing: TimingInfo

    class Config:
        json_schema_extra = {
            "example": {
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
        }


@app.get("/", tags=["General"])
async def root():
    """
    **API Information**

    Returns basic information about the API including available endpoints.
    """
    return {
        "message": "Random Number Generator API for n8n Workflows",
        "version": "1.0",
        "endpoints": {
            "model": "/model (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        },
        "deployment": "Posit Connect"
    }


@app.get("/health", tags=["General"])
async def health():
    """
    **Health Check**

    Verify the API is running and responsive.

    Returns service status and platform information.
    """
    return {
        "status": "healthy",
        "service": "random-number-generator",
        "platform": "Posit Connect"
    }


@app.post("/model", response_model=ModelResponse, tags=["Model"])
async def generate_number(
    payload: RequestPayload,
    authorization: Optional[str] = Header(None)
):
    """
    **Generate Random Number**

    Generate a random number within the specified range using uniform distribution.

    ### Domino Compatibility
    This endpoint maintains the exact response format used by Domino APIs,
    ensuring seamless migration of existing n8n workflows.

    ### Parameters
    - **min** (int): Minimum value for random number generation
    - **max** (int): Maximum value for random number generation

    ### Authentication
    Optional API key in header:
    ```
    Authorization: Key YOUR_API_KEY
    ```

    ### Example Request
    ```json
    {
        "data": {
            "min": 1,
            "max": 100
        }
    }
    ```

    ### Example Response
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
    import os

    # Posit Workbench configuration
    # This sets the correct root path for FastAPI in Workbench
    path, port = '', 8000
    if 'RS_SERVER_URL' in os.environ and os.environ['RS_SERVER_URL']:
        import subprocess
        path = subprocess.run(
            f'echo $(/usr/lib/rstudio-server/bin/rserver-url -l {port})',
            stdout=subprocess.PIPE,
            shell=True
        ).stdout.decode().strip()

    print(f"Starting API server on port {port}")
    if path:
        print(f"Workbench root path: {path}")

    uvicorn.run(app, host="0.0.0.0", root_path=path, port=port)
