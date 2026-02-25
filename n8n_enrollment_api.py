"""
Clinical Trial Enrollment Prediction API for n8n Workflows

Real-world example using ML model with Domino-compatible API format.
Demonstrates how Posit Connect can serve ML models for n8n workflows.

Deploy to Posit Connect:
    rsconnect deploy fastapi --entrypoint n8n_enrollment_api:app .

Example curl request:
    curl -X POST https://connect.example.com/content/abc123/model \
      -H "Authorization: Key YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "data": {
            "phase": "Phase II",
            "therapeutic_area": "Oncology",
            "country": "USA",
            "site_type": "Academic Medical Center",
            "investigator_experience_years": 15,
            "site_staff_count": 20,
            "prior_trials_completed": 25,
            "patient_database_size": 15000,
            "target_per_site": 75
        }
      }'
"""

import time
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path

app = FastAPI(
    title="Clinical Trial Enrollment Prediction API",
    description="An ML-powered API to predict clinical trial site enrollment success. Provides risk assessment and recommendations for trial site selection.",
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
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "default",
            "description": "ML prediction endpoints and service monitoring"
        }
    ]
)

# Load model artifacts
try:
    model = joblib.load("ml/enrollment_model.joblib")
    scaler = joblib.load("ml/scaler.joblib")
    encoders = joblib.load("ml/encoders.joblib")
    model_loaded = True
except Exception as e:
    print(f"Warning: Could not load model artifacts: {e}")
    model = None
    scaler = None
    encoders = None
    model_loaded = False


# Define input schema (simplified for n8n)
class SitePredictionData(BaseModel):
    """Site characteristics for enrollment prediction."""
    phase: str = Field(..., description="Trial phase (Phase I, Phase II, Phase III)")
    therapeutic_area: str = Field(..., description="Therapeutic area")
    country: str = Field(..., description="Country")
    site_type: str = Field(..., description="Site type")
    investigator_experience_years: int = Field(..., description="Investigator experience")
    site_staff_count: int = Field(..., description="Site staff count")
    prior_trials_completed: int = Field(..., description="Prior trials")
    patient_database_size: int = Field(..., description="Patient database size")
    target_per_site: int = Field(..., description="Target enrollment")

    # Optional parameters with defaults
    population_density: str = Field(default="Urban", description="Population density")
    distance_to_metro_km: int = Field(default=20, description="Distance to metro")
    inclusion_criteria_count: int = Field(default=10, description="Inclusion criteria")
    exclusion_criteria_count: int = Field(default=8, description="Exclusion criteria")
    protocol_amendments: int = Field(default=1, description="Protocol amendments")


class RequestPayload(BaseModel):
    """Domino-style request wrapper."""
    data: SitePredictionData


@app.get("/", include_in_schema=False)
async def root(request: Request):
    """Redirect to API documentation."""
    # Use request.url to get the correct URL with root_path
    docs_url = str(request.url).rstrip('/') + '/docs'
    return RedirectResponse(url=docs_url)


@app.get("/health", tags=["default"], summary="Health Check")
async def health():
    """Verify the API and ML model are loaded and responsive."""
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "service": "enrollment-prediction",
        "platform": "Posit Connect"
    }


@app.post("/model", tags=["default"], summary="Predict Enrollment Success")
async def predict_enrollment(
    payload: RequestPayload,
    authorization: Optional[str] = Header(None)
):
    """
    Predict the probability of successful patient enrollment for a clinical trial site based on site characteristics and trial parameters. Returns risk level and actionable recommendations.
    """
    start_time = time.time()

    if not model_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Ensure model artifacts are available."
        )

    try:
        site_data = payload.data

        # Validate categorical values
        valid_phases = list(encoders["phase"].classes_)
        valid_tas = list(encoders["therapeutic_area"].classes_)
        valid_countries = list(encoders["country"].classes_)
        valid_site_types = list(encoders["site_type"].classes_)
        valid_densities = list(encoders["population_density"].classes_)

        if site_data.phase not in valid_phases:
            raise HTTPException(status_code=400, detail=f"Invalid phase. Must be one of: {valid_phases}")
        if site_data.therapeutic_area not in valid_tas:
            raise HTTPException(status_code=400, detail=f"Invalid therapeutic area. Must be one of: {valid_tas}")
        if site_data.country not in valid_countries:
            raise HTTPException(status_code=400, detail=f"Invalid country. Must be one of: {valid_countries}")
        if site_data.site_type not in valid_site_types:
            raise HTTPException(status_code=400, detail=f"Invalid site type. Must be one of: {valid_site_types}")
        if site_data.population_density not in valid_densities:
            raise HTTPException(status_code=400, detail=f"Invalid population density. Must be one of: {valid_densities}")

        # Prepare features
        features = [
            encoders["phase"].transform([site_data.phase])[0],
            encoders["therapeutic_area"].transform([site_data.therapeutic_area])[0],
            encoders["country"].transform([site_data.country])[0],
            encoders["site_type"].transform([site_data.site_type])[0],
            encoders["population_density"].transform([site_data.population_density])[0],
            site_data.investigator_experience_years,
            site_data.site_staff_count,
            site_data.prior_trials_completed,
            site_data.patient_database_size,
            site_data.distance_to_metro_km,
            site_data.inclusion_criteria_count,
            site_data.exclusion_criteria_count,
            site_data.protocol_amendments,
            site_data.target_per_site
        ]

        X = np.array(features).reshape(1, -1)
        X_scaled = scaler.transform(X)

        # Make prediction
        probability = float(model.predict_proba(X_scaled)[0, 1])
        prediction = "Success" if probability >= 0.5 else "At Risk"

        # Determine risk level
        if probability >= 0.7:
            risk_level = "Low"
            recommendation = "Site has excellent characteristics for meeting enrollment targets."
        elif probability >= 0.4:
            risk_level = "Moderate"
            recommendation = "Site may benefit from additional support or optimization strategies."
        else:
            risk_level = "High"
            recommendation = "Site faces significant challenges. Consider additional sites or protocol modifications."

        calc_time_ms = (time.time() - start_time) * 1000

        # Return Domino-compatible format
        return {
            "release": {
                "harness_version": "Posit Connect",
                "model_version": "1.0",
                "model_version_number": 1
            },
            "request_id": "connect-request",
            "result": {
                "success_probability": round(probability, 4),
                "prediction": prediction,
                "risk_level": risk_level,
                "recommendation": recommendation
            },
            "timing": {
                "model_time_ms": round(calc_time_ms, 2)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import os

    # Posit Workbench configuration
    # This sets the correct root path for FastAPI in Workbench
    path, port = '', 8001
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
