# CORS Configuration Contract

**File**: `backend/app/main.py`
**Version**: 1.0.0
**Date**: 2026-02-08

## Overview

Backend CORS configuration must allow requests from:
1. Local development environments (localhost)
2. Production Hugging Face Space domain
3. Vercel production and preview deployments (dynamic)

## Configuration Specification

### Allowed Origins

**Static Origins** (always allowed):
```python
allowed_origins = [
    "http://localhost:3000",       # Next.js default dev port
    "http://localhost:3001",       # Alternate dev port
    "http://127.0.0.1:3000",       # Explicit localhost IP
    "https://alisaboor3-todo-app.hf.space"  # HF Space (if frontend hosted there)
]
```

**Dynamic Origins** (conditional):
```python
# Vercel deployments (production + previews)
vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    # VERCEL_URL format: "my-app-abc123.vercel.app" (no protocol)
    allowed_origins.append(f"https://{vercel_url}")
```

### CORS Middleware Configuration

```python
from fastapi.middleware.cors import CORSMiddleware
import os

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,     # List above (NO wildcards)
    allow_credentials=True,            # Required for auth tokens/cookies
    allow_methods=["*"],               # Allow all HTTP methods
    allow_headers=["*"],               # Allow all request headers
)
```

## Behavior Specification

### Development Environment

**Scenario**: Running backend and frontend locally

| Frontend Origin | Backend Allows | Notes |
|----------------|----------------|-------|
| `http://localhost:3000` | ✅ Yes | Standard Next.js dev port |
| `http://localhost:3001` | ✅ Yes | Alternate port |
| `http://127.0.0.1:3000` | ✅ Yes | Explicit localhost IP |

**Verification**: Browser DevTools shows no CORS errors

### Production Environment

**Scenario**: Frontend on Vercel, Backend on HF Spaces

| Frontend Origin | VERCEL_URL Value | Backend Allows | Notes |
|----------------|------------------|----------------|-------|
| `https://my-app.vercel.app` | `my-app.vercel.app` | ✅ Yes | Production domain |
| `https://my-app-git-feat-user.vercel.app` | `my-app-git-feat-user.vercel.app` | ✅ Yes | Preview deployment |
| `https://my-app-abc123.vercel.app` | `my-app-abc123.vercel.app` | ✅ Yes | Preview deployment |
| `https://other-app.vercel.app` | (not set or different) | ❌ No | Different deployment |

**VERCEL_URL Behavior**:
- Automatically set by Vercel for all deployments
- Changes for each preview deployment
- Format: domain without protocol (e.g., `my-app-abc123.vercel.app`)
- Backend must prepend `https://` when adding to allowed origins

### Security Rules

**Prohibited Patterns**:
- ❌ `allow_origins=["*"]` with `allow_credentials=True` (browsers reject)
- ❌ `allow_origins=["*.vercel.app"]` (too broad, security risk)
- ❌ Regular expression patterns (complexity, hard to audit)

**Required**:
- ✅ Explicit origin list
- ✅ HTTPS for all production origins
- ✅ HTTP only for localhost development origins
- ✅ `allow_credentials=True` for authentication

## Environment Variables

### Backend Environment Variables

**Required**: None (works with defaults)

**Optional**:
- `VERCEL_URL` - Set automatically by Vercel
  - Format: `my-app-abc123.vercel.app` (no protocol)
  - Used to dynamically allow Vercel deployments
  - If not set, Vercel deployments won't work (frontend will see CORS errors)

**Example** (Hugging Face Spaces environment):
```bash
# No VERCEL_URL (backend running on HF Spaces)
# Vercel will set VERCEL_URL on the frontend deployment
```

**Example** (if backend needs to know frontend URL):
```bash
VERCEL_URL=my-todo-app.vercel.app
```

## Testing

### Manual Testing

**Development**:
1. Start backend: `uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Open browser DevTools > Console
4. Navigate to app, make API calls
5. **Verify**: No CORS errors

**Production**:
1. Deploy backend to HF Spaces
2. Deploy frontend to Vercel
3. Open production site in incognito
4. Open DevTools > Console and Network tabs
5. Log in and navigate to chat
6. **Verify**: No CORS errors, all requests succeed

### Automated Testing

**CORS Preflight Test**:
```bash
curl -X OPTIONS https://alisaboor3-todo-app.hf.space/auth/login \
  -H "Origin: https://my-app.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type, Authorization" \
  -v
```

**Expected Response Headers**:
```
Access-Control-Allow-Origin: https://my-app.vercel.app
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

## Migration

### Before (Hardcoded Origins)

```python
allowed_origins = [
    "http://localhost:3000",
    "https://alisaboor3-todo-app.hf.space"
]
```

**Issues**:
- ❌ Vercel preview deployments fail (CORS errors)
- ❌ Manual update required for each preview URL

### After (Dynamic Origins)

```python
import os

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "https://alisaboor3-todo-app.hf.space"
]

vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    allowed_origins.append(f"https://{vercel_url}")
```

**Benefits**:
- ✅ Vercel preview deployments work automatically
- ✅ No manual configuration needed
- ✅ Secure (explicit list, no wildcards)

## Troubleshooting

### CORS Error: "No 'Access-Control-Allow-Origin' header"

**Cause**: Frontend origin not in allowed_origins list

**Solutions**:
1. **Local Dev**: Check frontend is running on localhost:3000/3001
2. **Production**: Check VERCEL_URL is set in backend environment
3. **Preview**: Verify Vercel sets VERCEL_URL for preview deployments

### CORS Error: "Credentials flag is true, but origin is '*'"

**Cause**: Wildcard origin with credentials enabled

**Solution**: Use explicit origin list (never use `"*"` with `allow_credentials=True`)

### Browser Blocks Request: "Private Network Access"

**Cause**: Public website (Vercel) calling local network (localhost:8000)

**Solution**: This is correct behavior - production should never call localhost. Check frontend is using correct API base URL from environment variables.

## Security Considerations

### Attack Vectors Prevented

1. **Cross-Site Request Forgery (CSRF)**:
   - Credentials required (`allow_credentials=True`)
   - Origin validation prevents unauthorized sites

2. **Subdomain Takeover**:
   - No wildcard patterns (e.g., `*.vercel.app`)
   - Each deployment explicitly allowed via VERCEL_URL

3. **Origin Spoofing**:
   - Browser enforces Origin header integrity
   - Backend validates against whitelist

### Best Practices

- ✅ Use HTTPS for all production origins
- ✅ Explicit origin list (no wildcards)
- ✅ Regular audit of allowed_origins
- ✅ Log blocked CORS requests for monitoring
- ⚠️ VERCEL_URL trusted (set by Vercel platform)

## Versioning

**Version 1.0.0** (2026-02-08)
- Initial implementation with dynamic Vercel support
- Supports localhost development
- Supports Vercel production and preview deployments

**Future Considerations**:
- May add origin pattern validation/sanitization
- May add CORS monitoring/logging
- May add support for custom deployment platforms
