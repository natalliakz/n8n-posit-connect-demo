# n8n + Posit Connect Quick Start Guide

**Quick reference for integrating Posit Connect APIs with n8n workflows**

## 🎯 Goal

Replace Domino API endpoints with Posit Connect for n8n agentic workflows.

## 📋 What You Need

- ✅ Posit Connect server URL
- ✅ API key from Posit Connect
- ✅ Deployed API endpoint URL
- ✅ n8n workflow access

## 🚀 Quick Setup (5 minutes)

### 1. Deploy API to Posit Connect

```bash
# Install deployment tool
uv add rsconnect-python

# Configure Connect server
rsconnect add \
  --account myaccount \
  --name myserver \
  --server https://connect.example.com \
  --api-key YOUR_CONNECT_API_KEY

# Deploy API
rsconnect deploy fastapi \
  --entrypoint n8n_demo_api:app \
  --name random-number-api \
  .
```

### 2. Get API Key

1. Open deployed API in Posit Connect dashboard
2. Go to **Access** tab
3. Click **Create API Key**
4. Name it (e.g., "n8n Production")
5. **Copy and save the key** (shown only once!)

### 3. Configure n8n HTTP Request Node

**Settings:**
- **Method**: `POST`
- **URL**: `https://connect.example.com/content/[YOUR-CONTENT-ID]/model`

**Headers:**
```
Authorization: Key YOUR_API_KEY
Content-Type: application/json
```

**Body:**
```json
{
  "data": {
    "min": {{ $json.min }},
    "max": {{ $json.max }}
  }
}
```

### 4. Test It!

Click **Test Workflow** in n8n.

Expected response:
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

## 📊 Available Demo APIs

### API 1: Random Number Generator

**File**: `n8n_demo_api.py`

**Purpose**: Simple "Hello World" demo

**Request**:
```json
{
  "data": {
    "min": 1,
    "max": 100
  }
}
```

**Use Case**: Basic workflow testing, parameter passing

---

### API 2: Enrollment Prediction (ML Model)

**File**: `n8n_enrollment_api.py`

**Purpose**: Real-world ML prediction

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
  "result": {
    "success_probability": 0.9388,
    "prediction": "Success",
    "risk_level": "Low",
    "recommendation": "Site has excellent characteristics..."
  }
}
```

**Use Case**: Decision automation, risk assessment workflows

## 🔄 Migration from Domino

### What Changes?

| Component | Domino | Posit Connect |
|-----------|--------|---------------|
| **URL** | `guardanthealth.domino.tech/models/1234/latest/model` | `connect.example.com/content/abc123/model` |
| **Auth Header** | `Authorization: Basic <key>` | `Authorization: Key <key>` |
| **Response Format** | ✅ Same | ✅ Same (maintained compatibility) |

### Update Checklist

- [ ] Get new Posit Connect API endpoint URL
- [ ] Generate API key in Posit Connect
- [ ] Update n8n HTTP Request node URL
- [ ] Change `Authorization: Basic` → `Authorization: Key`
- [ ] Test workflow with new endpoint
- [ ] Update documentation for team
- [ ] Archive old Domino credentials

## 🧪 Testing Locally Before Deployment

```bash
# Start API locally
uv run python n8n_demo_api.py

# Test with curl
curl -X POST http://localhost:8000/model \
  -H "Content-Type: application/json" \
  -d '{"data": {"min": 1, "max": 100}}'

# Expected: {"result": {"number": 42.13}, ...}
```

## 📈 Monitoring in Posit Connect

### Check API Health

Navigate to your API in Connect dashboard:

**Metrics Tab:**
- Request count (daily, weekly, monthly)
- Response times (p50, p95, p99)
- Error rates
- Active users

**Logs Tab:**
- Real-time request logs
- Error messages
- Debug output

### Set Up Alerts

1. Go to API **Settings**
2. Configure email alerts for:
   - High error rates
   - Slow response times
   - API downtime

## 🛠️ Troubleshooting

### Issue: 401 Unauthorized

**Fix:**
```
Check API key format: "Authorization: Key YOUR_API_KEY"
NOT "Authorization: Basic YOUR_API_KEY"
```

### Issue: 404 Not Found

**Fix:**
```
Verify endpoint URL includes /model:
✅ https://connect.example.com/content/abc123/model
❌ https://connect.example.com/content/abc123
```

### Issue: Slow Response

**Check:**
1. Connect server status
2. API logs for bottlenecks
3. Model load time (first request is slower)

**Optimize:**
- Cache predictions for repeated requests
- Increase Connect process count

### Issue: Model Not Loaded (enrollment API)

**Fix:**
```bash
# Ensure ML artifacts are deployed
ls ml/  # Should show .joblib files

# Redeploy with artifacts
rsconnect deploy fastapi --entrypoint n8n_enrollment_api:app .
```

## 💡 Best Practices

### Security
- ✅ Create separate API keys for dev/prod
- ✅ Store keys in credential manager (not in n8n directly)
- ✅ Rotate keys quarterly
- ❌ Don't share keys across teams

### Performance
- ✅ Cache frequent predictions
- ✅ Use async workflows when possible
- ✅ Monitor response times
- ❌ Don't make synchronous calls in loops

### Deployment
- ✅ Test locally before deploying
- ✅ Deploy to dev environment first
- ✅ Use version control for rollback
- ❌ Don't deploy directly to production

## 📞 Getting Help

**Posit Support**: https://support.posit.co

**Documentation**:
- Connect Admin Guide: https://docs.posit.co/connect/admin/
- FastAPI Deployment: https://docs.posit.co/connect/user/fastapi/
- API Hosting: https://docs.posit.co/connect/user/content-settings/

**Internal Resources**:
- Full deployment guide: `POSIT-CONNECT-DEPLOYMENT.md`
- API source code: `n8n_demo_api.py`, `n8n_enrollment_api.py`

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
[Send Email: "Generated number: 42"]
```

### Workflow 2: Site Risk Assessment

```
[Webhook Trigger: New trial site]
    ↓
[Format Site Data]
    ↓
[HTTP Request: POST to enrollment API]
    ↓
[Check Risk Level]
    ├─ Low Risk → [Approve Site]
    ├─ Moderate → [Request Review]
    └─ High Risk → [Send Alert]
```

### Workflow 3: Batch Processing

```
[Schedule: Daily 9 AM]
    ↓
[Get Sites from Database]
    ↓
[Loop Through Sites]
    ├─ [Call Prediction API for each]
    └─ [Collect Results]
    ↓
[Generate Report]
    ↓
[Send to Team]
```

## 🚦 Next Steps

1. **Deploy Simple API**
   - Start with `n8n_demo_api.py`
   - Test in n8n workflow
   - Verify Domino-compatible format

2. **Deploy ML API**
   - Deploy `n8n_enrollment_api.py`
   - Test with real-world scenarios
   - Monitor performance

3. **Migrate Workflows**
   - Update n8n workflows one at a time
   - Test each before migrating next
   - Document changes

4. **Train Team**
   - Share deployment guide
   - Demo n8n integration
   - Set up monitoring alerts

---

**Ready to start?** Deploy the random number API first, test in n8n, then move to production ML models! 🚀
