# Deploying APIs to Posit Connect for n8n Workflows

This guide shows how to deploy FastAPI applications to Posit Connect as API endpoints that can be invoked from n8n agentic workflows, replacing Domino as the compute backend.

## Overview

Posit Connect provides:
- ✅ **API Hosting**: Deploy FastAPI endpoints with automatic scaling
- ✅ **Authentication**: API keys for secure access (similar to Domino)
- ✅ **Monitoring**: Usage metrics, performance tracking, logs
- ✅ **Version Control**: Multiple versions, rollback capability
- ✅ **n8n Integration**: Direct HTTP POST requests with API keys

## Available Demo APIs

### 1. Random Number Generator (`n8n_demo_api.py`)
Simple "Hello World" example matching your Domino pattern.

**Purpose**: Demonstrates basic API deployment and n8n integration

**Endpoint**: `/model`

**Request**:
```json
{
  "data": {
    "min": 1,
    "max": 100
  }
}
```

**Response** (Domino-compatible format):
```json
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
```

### 2. Clinical Trial Enrollment Prediction (`n8n_enrollment_api.py`)
Real-world ML model serving enrollment predictions.

**Purpose**: Demonstrates production ML model deployment

**Endpoint**: `/model`

**Request**:
```json
{
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
}
```

**Response** (Domino-compatible format):
```json
{
  "release": {
    "harness_version": "Posit Connect",
    "model_version": "1.0",
    "model_version_number": 1
  },
  "request_id": "connect-request",
  "result": {
    "success_probability": 0.9388,
    "prediction": "Success",
    "risk_level": "Low",
    "recommendation": "Site has excellent characteristics..."
  },
  "timing": {
    "model_time_ms": 5.23
  }
}
```

## Deployment Steps

### Prerequisites

1. **Posit Connect Server**: Access to Posit Connect instance
2. **rsconnect-python**: Deployment CLI tool
3. **API Key**: Connect API key for deployment

Install rsconnect-python:
```bash
uv add rsconnect-python
# or
pip install rsconnect-python
```

### Step 1: Configure Connect Server

Add your Posit Connect server credentials:

```bash
rsconnect add \
  --account myaccount \
  --name myserver \
  --server https://connect.example.com \
  --api-key YOUR_CONNECT_API_KEY
```

Verify configuration:
```bash
rsconnect list
```

### Step 2: Deploy Random Number API

Navigate to the project directory:
```bash
cd VitalGen_Pharmaceuticals
```

Deploy the simple demo API:
```bash
rsconnect deploy fastapi \
  --entrypoint n8n_demo_api:app \
  --name random-number-api \
  --title "Random Number Generator for n8n" \
  .
```

**Note**: The `.` at the end tells rsconnect to deploy the current directory.

### Step 3: Deploy Enrollment Prediction API

Deploy the ML-powered API:
```bash
rsconnect deploy fastapi \
  --entrypoint n8n_enrollment_api:app \
  --name enrollment-api \
  --title "Clinical Trial Enrollment Prediction for n8n" \
  .
```

This deploys:
- The API code
- All dependencies (from `pyproject.toml`)
- ML model artifacts (from `ml/` directory)

### Step 4: Configure API Access in Posit Connect

After deployment:

1. **Open Connect Dashboard**: Navigate to your deployed API
2. **Access Tab**: Configure who can access the API
3. **API Keys**:
   - Click "Create API Key"
   - Give it a descriptive name (e.g., "n8n Integration Key")
   - **Copy the key immediately** (shown only once)
   - Store securely (this replaces your Domino API key)

### Step 5: Get the API Endpoint URL

In Posit Connect:
1. Open your deployed API
2. Copy the **Content URL** (e.g., `https://connect.example.com/content/abc123/`)
3. The model endpoint will be: `https://connect.example.com/content/abc123/model`

## Testing the Deployed API

### Using curl

Test the random number API:
```bash
curl -X POST https://connect.example.com/content/abc123/model \
  -H "Authorization: Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"min": 1, "max": 100}}'
```

Test the enrollment API:
```bash
curl -X POST https://connect.example.com/content/xyz789/model \
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
```

### Using Python

```python
import requests

url = "https://connect.example.com/content/abc123/model"
headers = {
    "Authorization": "Key YOUR_API_KEY",
    "Content-Type": "application/json"
}
payload = {
    "data": {
        "min": 1,
        "max": 100
    }
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## n8n Integration

### Configuring HTTP Request Node in n8n

1. **Add HTTP Request Node**
2. **Configure**:

   - **Method**: `POST`
   - **URL**: `https://connect.example.com/content/abc123/model`

   **Headers**:
   - `Authorization`: `Key YOUR_API_KEY`
   - `Content-Type`: `application/json`

   **Body**:
   ```json
   {
     "data": {
       "min": {{ $json.min }},
       "max": {{ $json.max }}
     }
   }
   ```

3. **Test Execution**: Run the workflow to verify connectivity

### Example n8n Workflow

```json
{
  "nodes": [
    {
      "name": "Set Parameters",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "values": {
          "number": [
            {
              "name": "min",
              "value": 1
            },
            {
              "name": "max",
              "value": 100
            }
          ]
        }
      }
    },
    {
      "name": "Call Posit Connect API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://connect.example.com/content/abc123/model",
        "authentication": "none",
        "options": {},
        "headerParametersUi": {
          "parameter": [
            {
              "name": "Authorization",
              "value": "Key YOUR_API_KEY"
            },
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "bodyParametersUi": {
          "parameter": [
            {
              "name": "data",
              "value": "={{ { min: $json.min, max: $json.max } }}"
            }
          ]
        }
      }
    },
    {
      "name": "Process Result",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "values": {
          "number": [
            {
              "name": "random_number",
              "value": "={{ $json.result.number }}"
            }
          ]
        }
      }
    }
  ]
}
```

## Monitoring and Management

### Usage Metrics in Posit Connect

1. **Open API in Connect Dashboard**
2. **Metrics Tab**:
   - Request count over time
   - Response times
   - Error rates
   - Active users

3. **Logs Tab**:
   - Real-time logs
   - Error messages
   - Debug output

### Performance Optimization

**Scaling**:
- Connect automatically scales based on load
- Configure min/max processes in Settings

**Caching**:
- Add caching for frequently requested predictions
- Use Redis or in-memory caching

**Resource Limits**:
- Set memory limits per process
- Configure timeout values

## API Versioning

### Deploying New Versions

Update code and redeploy:
```bash
rsconnect deploy fastapi \
  --entrypoint n8n_demo_api:app \
  --name random-number-api \
  .
```

Connect automatically creates a new version while keeping the old one accessible.

### Rolling Back

If issues occur:
1. Open API in Connect Dashboard
2. **Versions** tab
3. Select previous version
4. Click "Activate"

### Version-Specific Endpoints

Access specific versions:
- Latest: `https://connect.example.com/content/abc123/model`
- Version 2: `https://connect.example.com/content/abc123/v2/model`

## Security Best Practices

### API Key Management

✅ **Do**:
- Create separate API keys for each integration
- Use descriptive names (e.g., "n8n Production", "n8n Dev")
- Rotate keys periodically
- Store in secure credential managers (not in n8n directly)

❌ **Don't**:
- Share API keys across multiple services
- Commit API keys to version control
- Use personal API keys for production

### Access Control

In Posit Connect:
1. **Access Tab** → Configure permissions
2. Options:
   - **Anyone** - No authentication required (not recommended)
   - **Anyone with API Key** - Recommended for n8n
   - **Logged in users** - Requires Connect login
   - **Specific users/groups** - Granular control

### Network Security

- Use HTTPS only (Posit Connect enforces this)
- Configure IP allowlists if needed
- Enable audit logging

## Comparison: Domino vs. Posit Connect

| Feature | Domino | Posit Connect |
|---------|--------|---------------|
| **Authentication** | `Authorization: Basic <key>` | `Authorization: Key <key>` |
| **Deployment** | Domino UI/CLI | `rsconnect-python` CLI |
| **Monitoring** | Domino dashboard | Connect dashboard |
| **Scaling** | Manual configuration | Automatic |
| **Languages** | Python, R | Python, R, Quarto |
| **Version Control** | Model versions | Content versions |
| **Cost** | Per-user licensing | Server-based licensing |

### Migration Checklist

- [x] Replace `Authorization: Basic` with `Authorization: Key`
- [x] Update endpoint URLs from Domino to Connect
- [x] Test API response format (Domino-compatible maintained)
- [x] Update n8n workflows with new credentials
- [x] Configure monitoring and alerts in Connect
- [x] Document new deployment process for team

## Troubleshooting

### Common Issues

**1. "Model not loaded" error**

Ensure ML artifacts are included in deployment:
```bash
# Check that ml/ directory is present
ls ml/
# Should show: enrollment_model.joblib, scaler.joblib, encoders.joblib
```

**2. Import errors after deployment**

Verify all dependencies in `pyproject.toml`:
```bash
uv add missing-package
```

**3. 401 Unauthorized**

- Check API key is correct
- Verify header format: `Authorization: Key YOUR_API_KEY` (not `Basic`)
- Ensure API access settings allow API key authentication

**4. Slow response times**

- Check Connect server resources
- Review API logs for bottlenecks
- Consider caching for repeated requests

### Getting Help

- **Posit Support**: https://support.posit.co
- **Connect Admin Guide**: https://docs.posit.co/connect/admin/
- **API Hosting Guide**: https://docs.posit.co/connect/user/fastapi/

## Next Steps

1. **Test Locally**: Run APIs locally before deploying
   ```bash
   uv run python n8n_demo_api.py
   uv run python n8n_enrollment_api.py
   ```

2. **Deploy to Dev**: Deploy to development Connect server first

3. **Update n8n**: Configure n8n workflows with new endpoints

4. **Monitor Performance**: Track usage and optimize as needed

5. **Document for Team**: Share deployment process and API keys

---

**Ready to deploy?** Start with the simple random number API, test in n8n, then deploy the ML-powered enrollment API for production use cases.
