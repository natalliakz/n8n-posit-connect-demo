# Swagger/OpenAPI Documentation Guide

## Viewing Swagger Docs

### Locally

When running the API locally:

```bash
# Start the API
python3 n8n_demo_api.py

# Open in browser:
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### In Posit Workbench

When running in Workbench, the URL will be shown when you start the server:

```bash
python3 n8n_demo_api.py
# Output shows: Workbench root path: /p/abc123/
```

Access Swagger at:
```
https://workbench.example.com/p/abc123/docs
```

### In Posit Connect (After Deployment)

After deploying to Connect:

```
https://connect.example.com/content/YOUR_CONTENT_ID/docs
```

**OR** click the "API Documentation" link in the Connect dashboard for your deployed API.

---

## What You'll See

### 📋 API Description
- Full markdown-formatted description
- Features and authentication info
- Example curl commands

### 🏷️ Tags for Organization
- **General**: Root and health endpoints
- **Model**: Prediction/generation endpoints

### 📝 Detailed Endpoint Documentation
Each endpoint shows:
- Description and purpose
- Request body schema with examples
- Response model with examples
- HTTP status codes
- Authentication requirements

### 🧪 Interactive Testing
- Click "Try it out" button
- Fill in parameters
- Click "Execute"
- See real response from API

---

## Swagger UI Features

### 1. Try It Out

Click **"Try it out"** on any endpoint to test it directly:

```
POST /model
▼ Try it out

Request body:
{
  "data": {
    "min": 1,
    "max": 100
  }
}

[Execute]
```

### 2. Model Schemas

Scroll down to see **Schemas** section:
- `RequestPayload` - Input format
- `ModelResponse` - Output format
- `DataPayload` - Nested models

### 3. Example Responses

Each endpoint shows example responses with:
- Status codes (200, 400, 500, etc.)
- Response body structure
- Expected data types

### 4. Authentication

For endpoints requiring API keys:

```
🔒 Authorize

Available authorizations:

APIKeyHeader (apiKey)
Value: Key YOUR_API_KEY

[Authorize] [Close]
```

---

## Customization Options

### Adding More Detail

Edit the FastAPI app configuration:

```python
app = FastAPI(
    title="Your API Title",
    description="""
    # Markdown formatted description

    ## Features
    - Feature 1
    - Feature 2

    ## Authentication
    Use API keys...
    """,
    version="1.0.0",
    contact={
        "name": "Your Team",
        "email": "team@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)
```

### Adding Response Examples

Add to Pydantic models:

```python
class MyModel(BaseModel):
    field: str

    class Config:
        json_schema_extra = {
            "example": {
                "field": "example value"
            }
        }
```

### Adding Tags

Organize endpoints into sections:

```python
@app.post("/endpoint", tags=["Category Name"])
async def my_endpoint():
    """Endpoint description"""
    pass
```

### Rich Docstrings

Use markdown in docstrings:

```python
@app.post("/endpoint")
async def my_endpoint():
    """
    **Endpoint Title**

    Description paragraph.

    ### Parameters
    - param1: Description
    - param2: Description

    ### Example
    ```json
    {"key": "value"}
    ```
    """
    pass
```

---

## Best Practices for Posit Connect

### 1. Clear Descriptions
- Explain the business purpose
- Include use cases
- Document expected inputs/outputs

### 2. Examples Everywhere
- Request body examples
- Response examples
- Error examples

### 3. Authentication Documentation
- Explain how to get API keys
- Show header format
- Link to Connect documentation

### 4. Status Codes
- Document all possible responses
- 200: Success
- 400: Bad request
- 401: Unauthorized
- 500: Server error

### 5. Version Information
- Keep version number updated
- Document breaking changes
- Link to changelog

---

## Troubleshooting

### Swagger UI Not Showing

**Problem**: `/docs` returns 404

**Solution**: Check FastAPI configuration
```python
app = FastAPI(
    docs_url="/docs",  # Enable Swagger UI
    redoc_url="/redoc"  # Enable ReDoc
)
```

### Examples Not Appearing

**Problem**: Request/response examples missing

**Solution**: Add to Pydantic model Config
```python
class Config:
    json_schema_extra = {
        "example": {...}
    }
```

### Descriptions Too Plain

**Problem**: Docs look basic

**Solution**: Use markdown formatting
```python
description="""
# Title
**Bold text**
- Bullet points
```code blocks```
"""
```

### Root Path Issues in Workbench

**Problem**: API works but docs show wrong URLs

**Solution**: Ensure root_path is set (already configured in our APIs)
```python
uvicorn.run(app, root_path=path)
```

---

## Demo API Documentation

### Random Number API

**Local**: http://localhost:8000/docs

**Features**:
- ✅ Domino-compatible format
- ✅ Request/response examples
- ✅ Interactive testing
- ✅ Organized with tags
- ✅ Markdown descriptions

### Enrollment Prediction API

**Local**: http://localhost:8001/docs

**Features**:
- ✅ ML model documentation
- ✅ Detailed input parameters
- ✅ Risk level explanations
- ✅ Real predictions in browser

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/tutorial/metadata/
- **OpenAPI Spec**: https://swagger.io/specification/
- **Posit Connect**: https://docs.posit.co/connect/user/fastapi/

---

**Pro Tip**: Good API documentation in Swagger = Faster user adoption!
Users can understand and test your API without reading separate documentation.
