# Getting Started with n8n + Posit Connect Demo

**Quick 10-minute setup to replace Domino APIs with Posit Connect**

## Prerequisites

- Python 3.9+ installed
- Access to Posit Connect server (or test locally first)
- n8n workflow access (if integrating)

## Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone https://github.com/your-org/n8n-posit-connect-demo.git
cd n8n-posit-connect-demo

# Install dependencies with uv (recommended)
pip install uv
uv sync

# OR with pip
pip install -r requirements.txt
```

## Step 2: Test Locally (3 minutes)

### Start the Simple API

```bash
# Terminal 1: Start random number API
python n8n_demo_api.py

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test with curl

```bash
# Terminal 2: Test the API
curl -X POST http://localhost:8000/model \
  -H "Content-Type: application/json" \
  -d '{"data": {"min": 1, "max": 100}}'

# Expected response:
# {
#   "release": {"harness_version": "Posit Connect", ...},
#   "result": {"number": 42.13},
#   "timing": {"model_time_ms": 1.73}
# }
```

### Test Health Endpoint

```bash
curl http://localhost:8000/health

# Expected: {"status": "healthy", ...}
```

✅ **If you see the JSON response, the API is working!**

## Step 3: Deploy to Posit Connect (5 minutes)

### Install Deployment Tool

```bash
pip install rsconnect-python
```

### Configure Connect Server

```bash
rsconnect add \
  --account myaccount \
  --name myserver \
  --server https://connect.example.com \
  --api-key YOUR_CONNECT_API_KEY
```

**Where to get API key**: Posit Connect dashboard → Settings → API Keys

### Deploy the API

```bash
rsconnect deploy fastapi \
  --entrypoint n8n_demo_api:app \
  --name random-number-api \
  .
```

### Get the Deployment URL

After deployment completes, you'll see:
```
Deployment completed successfully.
Dashboard URL: https://connect.example.com/content/abc123
```

**API Endpoint URL**: `https://connect.example.com/content/abc123/model`

### Create API Key for n8n

1. Open the deployment URL in your browser
2. Go to **Access** tab
3. Click **Create API Key**
4. Name it "n8n Integration"
5. **Copy the key** (shown only once!)

## Step 4: Update n8n Workflow (3 minutes)

### Configure HTTP Request Node

Open your n8n workflow and update the HTTP Request node:

**Settings:**
- **Method**: `POST`
- **URL**: `https://connect.example.com/content/abc123/model`

**Headers:** (click "+ Add Header" twice)
- Name: `Authorization`
  Value: `Key YOUR_API_KEY_FROM_STEP_3`

- Name: `Content-Type`
  Value: `application/json`

**Body:**
```json
{
  "data": {
    "min": {{ $json.min }},
    "max": {{ $json.max }}
  }
}
```

**Note**: Change `Authorization: Basic` → `Authorization: Key`

### Test the Workflow

Click **Test Workflow** in n8n.

Expected result in n8n:
```json
{
  "result": {
    "number": 42.13
  },
  "timing": {
    "model_time_ms": 1.73
  }
}
```

✅ **You've successfully migrated from Domino to Posit Connect!**

## Next Steps

### Deploy the ML-Powered API

```bash
# Start locally first to test
python n8n_enrollment_api.py

# Test with curl
curl -X POST http://localhost:8001/model \
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

# Deploy to Connect
rsconnect deploy fastapi \
  --entrypoint n8n_enrollment_api:app \
  --name enrollment-api \
  .
```

### Monitor Your APIs

Visit Posit Connect dashboard:
- **Metrics** tab → View request counts, response times
- **Logs** tab → See real-time API logs
- **Versions** tab → Manage deployments and rollback if needed

### Learn More

- **Quick Reference**: [docs/QUICK-START.md](docs/QUICK-START.md)
- **Complete Guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Demo Script**: [docs/DEMO-SCRIPT.md](docs/DEMO-SCRIPT.md)

## Troubleshooting

### API won't start

**Problem**: `ModuleNotFoundError` or similar errors

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# OR with uv
uv sync
```

### 401 Unauthorized in n8n

**Problem**: n8n returns authorization error

**Solution**: Check auth header format
- ✅ `Authorization: Key YOUR_API_KEY`
- ❌ `Authorization: Basic YOUR_API_KEY`

### Deployment fails

**Problem**: `rsconnect deploy` returns error

**Solution**:
```bash
# Verify Connect configuration
rsconnect list

# Re-add server if needed
rsconnect add --account ... --server ... --api-key ...
```

### Can't access deployed API

**Problem**: 404 Not Found

**Solution**: Verify URL includes `/model`
- ✅ `https://connect.example.com/content/abc123/model`
- ❌ `https://connect.example.com/content/abc123`

## Questions?

- **Posit Support**: https://support.posit.co
- **Documentation**: [README.md](README.md)
- **Connect Docs**: https://docs.posit.co/connect/

---

**Ready to go?** Start with Step 1 above! 🚀
