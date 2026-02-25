# n8n + Posit Connect Integration Demo

**Replace Domino APIs with Posit Connect for n8n Agentic Workflows**

This demo shows how to deploy FastAPI endpoints to Posit Connect that maintain Domino-compatible response formats, enabling seamless integration with n8n workflows.

[![Posit Connect](https://img.shields.io/badge/Posit-Connect-blue)](https://posit.co/products/enterprise/connect/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-green)](https://fastapi.tiangolo.com/)
[![n8n](https://img.shields.io/badge/n8n-Compatible-orange)](https://n8n.io/)

## 🎯 Problem Statement

**Current State**: Teams use Domino API endpoints for n8n workflows:
```bash
curl 'https://guardanthealth.domino.tech/models/1234/latest/model' \
  -H 'Authorization: Basic <API_key>' \
  -H 'Content-Type: application/json' \
  -d '{"data": {"min": 1, "max": 100}}'
```

**Goal**: Migrate to Posit Connect while maintaining:
- ✅ Same request/response format
- ✅ API authentication pattern
- ✅ n8n workflow compatibility
- ✅ Minimal migration effort

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv init
uv add fastapi uvicorn pydantic joblib numpy scikit-learn

# OR using pip
pip install fastapi uvicorn pydantic joblib numpy scikit-learn
```

### 2. Test Locally

```bash
# Terminal 1: Start simple demo API
python n8n_demo_api.py

# Terminal 2: Test it
curl -X POST http://localhost:8000/model \
  -H "Content-Type: application/json" \
  -d '{"data": {"min": 1, "max": 100}}'

# Expected response (Domino-compatible format):
# {
#   "release": {"harness_version": "Posit Connect", ...},
#   "result": {"number": 42.13},
#   "timing": {"model_time_ms": 1.73}
# }
```

### 3. Deploy to Posit Connect

```bash
# Install rsconnect-python
pip install rsconnect-python

# Configure Connect server
rsconnect add \
  --account myaccount \
  --name myserver \
  --server https://connect.example.com \
  --api-key YOUR_CONNECT_API_KEY

# Deploy
rsconnect deploy fastapi \
  --entrypoint n8n_demo_api:app \
  --name random-number-api \
  .
```

### 4. Update n8n Workflow

In n8n HTTP Request node:
- **Method**: `POST`
- **URL**: `https://connect.example.com/content/abc123/model`
- **Headers**:
  - `Authorization: Key YOUR_API_KEY` ← **Changed from "Basic"**
  - `Content-Type: application/json`
- **Body**: `{"data": {"min": 1, "max": 100}}`

**That's it!** Your n8n workflow now uses Posit Connect instead of Domino.

## 📦 What's Included

### 1. Simple Demo API (`n8n_demo_api.py`)

Random number generator - perfect for testing n8n integration.

**Request**:
```json
{
  "data": {
    "min": 1,
    "max": 100
  }
}
```

**Response** (Domino-compatible):
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

### 2. ML-Powered API (`n8n_enrollment_api.py`)

Real-world example: Clinical trial enrollment prediction using scikit-learn.

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

**Response**:
```json
{
  "release": {
    "harness_version": "Posit Connect",
    "model_version": "1.0",
    "model_version_number": 1
  },
  "request_id": "connect-request",
  "result": {
    "success_probability": 0.9412,
    "prediction": "Success",
    "risk_level": "Low",
    "recommendation": "Site has excellent characteristics..."
  },
  "timing": {
    "model_time_ms": 21.23
  }
}
```

### 3. Testing Script (`test_n8n_apis.py`)

Automated tests to verify both APIs work before deployment:

```bash
# Run all tests
python test_n8n_apis.py
```

## 🔄 Migration from Domino

### What Changes?

| Component | Domino | Posit Connect |
|-----------|--------|---------------|
| **URL** | `guardanthealth.domino.tech/models/1234/latest/model` | `connect.example.com/content/abc123/model` |
| **Auth Header** | `Authorization: Basic <key>` | `Authorization: Key <key>` |
| **Response Format** | ✅ Maintained | ✅ Exactly the same |
| **Request Body** | ✅ Maintained | ✅ No changes needed |

### Migration Checklist

- [ ] Deploy API to Posit Connect
- [ ] Generate API key in Connect dashboard
- [ ] Update n8n HTTP Request node URL
- [ ] Change auth header from `Basic` to `Key`
- [ ] Test workflow
- [ ] Monitor in Connect dashboard

**Estimated Time**: ~15 minutes for first API, ~3 minutes per n8n workflow

## 📊 Monitoring & Management

### In Posit Connect Dashboard

1. **Metrics Tab**:
   - Request count (daily/weekly/monthly)
   - Response times (p50, p95, p99)
   - Error rates
   - Active users

2. **Logs Tab**:
   - Real-time request logs
   - Error messages
   - Debug output

3. **Versions Tab**:
   - Version history
   - Instant rollback
   - A/B testing

### Health Endpoints

Both APIs include health checks:

```bash
curl http://localhost:8000/health
# {"status": "healthy", "service": "random-number-generator"}

curl http://localhost:8001/health
# {"status": "healthy", "model_loaded": true}
```

## 🧪 Testing Before Deployment

### Automated Testing

```bash
# Start both APIs in separate terminals
python n8n_demo_api.py      # Terminal 1
python n8n_enrollment_api.py  # Terminal 2

# Run tests
python test_n8n_apis.py      # Terminal 3
```

### Manual Testing with curl

```bash
# Test random number API
curl -X POST http://localhost:8000/model \
  -H "Content-Type: application/json" \
  -d '{"data": {"min": 1, "max": 100}}'

# Test enrollment API
curl -X POST http://localhost:8001/model \
  -H "Content-Type: application/json" \
  -d '{"data": {
    "phase": "Phase II",
    "therapeutic_area": "Oncology",
    "country": "USA",
    "site_type": "Academic Medical Center",
    "investigator_experience_years": 15,
    "site_staff_count": 20,
    "prior_trials_completed": 25,
    "patient_database_size": 15000,
    "target_per_site": 75
  }}'
```

## 🔐 Security

### API Key Management

**In Posit Connect**:
1. Open deployed API
2. Go to **Access** tab
3. Click **Create API Key**
4. Name it (e.g., "n8n Production")
5. Copy and store securely

**Best Practices**:
- ✅ Create separate keys for dev/prod
- ✅ Use descriptive names
- ✅ Rotate keys quarterly
- ✅ Store in credential manager
- ❌ Don't share keys across teams
- ❌ Don't commit keys to version control

### Access Control

Configure in Posit Connect:
- **Anyone with API Key** (recommended for n8n)
- **Logged in users**
- **Specific users/groups**

## 🎓 Example n8n Workflows

### Workflow 1: Random Number Generation

```
[Manual Trigger]
    ↓
[Set Parameters: min=1, max=100]
    ↓
[HTTP Request: POST to /model]
    ↓
[Extract Result: $json.result.number]
    ↓
[Send Notification]
```

### Workflow 2: Risk Assessment

```
[Webhook: New trial site]
    ↓
[Format Site Data]
    ↓
[HTTP Request: Enrollment API]
    ↓
[Branch by Risk Level]
    ├─ Low → [Auto-Approve]
    ├─ Moderate → [Request Review]
    └─ High → [Send Alert]
```

### Workflow 3: Batch Processing

```
[Schedule: Daily]
    ↓
[Get Sites from Database]
    ↓
[Loop Through Sites]
    ├─ [Call API for each]
    └─ [Collect Results]
    ↓
[Generate Report]
```

## 📁 Repository Structure

```
n8n-posit-connect-demo/
├── n8n_demo_api.py           # Simple random number API
├── n8n_enrollment_api.py     # ML-powered prediction API
├── test_n8n_apis.py          # Automated testing script
├── ml/
│   ├── enrollment_model.joblib  # Trained ML model
│   ├── scaler.joblib           # Feature scaler
│   ├── encoders.joblib         # Categorical encoders
│   └── model_utils.py          # Model utility functions
├── docs/
│   ├── QUICK-START.md          # 5-minute setup guide
│   ├── DEPLOYMENT.md           # Detailed deployment guide
│   └── DEMO-SCRIPT.md          # 15-minute demo flow
├── pyproject.toml              # Python dependencies (uv)
├── requirements.txt            # Python dependencies (pip)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🛠️ Troubleshooting

### Issue: 401 Unauthorized

**Problem**: n8n returns 401 error

**Solution**: Check auth header format
```
✅ Authorization: Key YOUR_API_KEY
❌ Authorization: Basic YOUR_API_KEY
```

### Issue: 404 Not Found

**Problem**: Endpoint not found

**Solution**: Verify URL includes `/model`
```
✅ https://connect.example.com/content/abc123/model
❌ https://connect.example.com/content/abc123
```

### Issue: Model Not Loaded (enrollment API)

**Problem**: API returns "model not loaded" error

**Solution**: Ensure ML artifacts are deployed
```bash
# Check files exist
ls ml/*.joblib

# Should show: enrollment_model.joblib, scaler.joblib, encoders.joblib

# Redeploy if needed
rsconnect deploy fastapi --entrypoint n8n_enrollment_api:app .
```

### Issue: Slow Response Times

**Check**:
1. Connect server status
2. API logs for bottlenecks
3. Model load time (first request is slower)

**Optimize**:
- Cache predictions for repeated requests
- Increase Connect process count
- Use async where possible

## 📚 Documentation

- **[QUICK-START.md](docs/QUICK-START.md)** - 5-minute deployment guide
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Complete deployment instructions
- **[DEMO-SCRIPT.md](docs/DEMO-SCRIPT.md)** - 15-minute demo flow

## 🤝 Support

- **Posit Connect Docs**: https://docs.posit.co/connect/
- **FastAPI Deployment**: https://docs.posit.co/connect/user/fastapi/
- **Posit Support**: https://support.posit.co

## 📄 License

This demo is provided for evaluation purposes. Synthetic data and ML models included are for demonstration only.

## 🙋 FAQ

**Q: Does this work with my existing n8n workflows?**
A: Yes! Only the URL and auth header need to change.

**Q: How long does migration take?**
A: ~15 minutes for first API deployment, ~3 minutes per n8n workflow.

**Q: Can I test before migrating production?**
A: Yes! Test locally, then deploy to dev Connect first.

**Q: What about rate limiting?**
A: Configure in Posit Connect settings per API.

**Q: Can I version my APIs?**
A: Yes, Connect maintains version history with instant rollback.

**Q: Do I need to change my data format?**
A: No, request/response formats are maintained exactly.

---

## 🚦 Next Steps

1. ✅ **Test locally** - Run both APIs and test with curl
2. ✅ **Deploy to dev** - Deploy simple API to test Connect
3. ✅ **Update n8n** - Configure one workflow with new endpoint
4. ✅ **Monitor** - Check metrics in Connect dashboard
5. ✅ **Scale** - Deploy ML API and migrate more workflows

**Ready to start?** Run `python n8n_demo_api.py` and test your first API!

---

*Created for Merck - Internal Analytics Platform Group*
*Demonstrates n8n workflow integration with Posit Connect*
