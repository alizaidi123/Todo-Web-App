# Research: Phase 3 Deployment Fix

**Feature**: 002-deployment-fix
**Date**: 2026-02-08
**Status**: Complete

## Problem Analysis

### Root Cause Identified

All frontend files import from `@/lib/apiBase` which resolves to `frontend/lib/apiBase.ts`, but this file **does not exist** in the repository. This causes:

1. Build failures or TypeScript errors (module not found)
2. Runtime errors if build somehow succeeds
3. Fallback to undefined behavior
4. Auth failures when API calls fail
5. Redirect to /login due to failed /auth/me checks

### Affected Files

**Importing non-existent module**:
- `frontend/lib/api.ts` (line 2)
- `frontend/app/chat/ChatClient.tsx` (line 15)
- `frontend/app/chat/page.tsx` (line 7)
- `frontend/app/login/page.tsx` (line 9)
- `frontend/app/signup/page.tsx` (line 9)

### Current State

**Frontend**: Expects `getApiBaseUrl()` function from missing module
**Backend**: Has basic CORS but missing VERCEL_URL support for preview deployments

## Research Findings

### 1. Next.js Environment Variables

**Documentation**: https://nextjs.org/docs/app/building-your-application/configuring/environment-variables

**Key Points**:
- Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- `process.env.NODE_ENV` is automatically set by Next.js:
  - `'development'` when running `next dev`
  - `'production'` when running `next build` or `next start`
- Environment variables are **inlined at build time**, not runtime
- Different behavior needed for server-side vs client-side code

**Best Practice**: Use `NODE_ENV` for environment detection, not custom variables

### 2. Vercel Environment Variables

**Documentation**: https://vercel.com/docs/projects/environment-variables

**Automatic Variables Vercel Sets**:
- `VERCEL=1` - Always set in Vercel environment
- `VERCEL_ENV` - Values: `production`, `preview`, or `development`
- `VERCEL_URL` - The deployment URL (e.g., `my-app-abc123.vercel.app`)
  - Does NOT include protocol (https://)
  - Changes for each preview deployment
  - Useful for dynamic CORS configuration

**NEXT_PUBLIC Variables**:
- Must be set in Vercel dashboard for each environment
- Applied during build time
- Cannot be changed without rebuild

**Best Practice**: Use VERCEL_URL on backend for dynamic preview support, require NEXT_PUBLIC_* on frontend

### 3. CORS Configuration

**Documentation**: https://fastapi.tiangolo.com/tutorial/cors/

**FastAPI CORSMiddleware Options**:
```python
allow_origins: List[str]      # Specific origins (recommended)
allow_origin_patterns: List[str]  # Regex patterns (use with caution)
allow_credentials: bool       # True for cookies/auth headers
allow_methods: List[str]      # HTTP methods
allow_headers: List[str]      # Request headers
```

**Security Considerations**:
- **Never use** `allow_origins=["*"]` with `allow_credentials=True` (browsers reject it)
- Wildcard subdomains (`*.vercel.app`) are risky - any subdomain matches
- Explicit origin list is most secure
- Dynamic origins (from env vars) are acceptable if controlled

**Best Practice**: Maintain explicit list, use VERCEL_URL for preview deployments

### 4. API Base URL Resolution Patterns

**Common Patterns Analyzed**:

**Pattern A: Runtime Detection** (Rejected)
```typescript
const API_BASE = typeof window !== 'undefined'
  ? window.location.origin.includes('localhost') ? 'http://localhost:8000' : process.env.NEXT_PUBLIC_API_BASE_URL
  : process.env.NEXT_PUBLIC_API_BASE_URL
```
- ❌ Fails at build time if env var missing
- ❌ Doesn't catch configuration errors early
- ❌ Complex logic in multiple places

**Pattern B: Build-Time with Fallback** (Selected)
```typescript
export function getApiBase(): string {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL;

  if (apiBaseUrl) {
    return apiBaseUrl.endsWith('/') ? apiBaseUrl.slice(0, -1) : apiBaseUrl;
  }

  if (process.env.NODE_ENV === 'production') {
    throw new Error('API base URL not configured for production');
  }

  return 'http://127.0.0.1:8000';
}
```
- ✅ Catches missing config during build
- ✅ Single source of truth
- ✅ Environment-specific behavior
- ✅ Clear error messages

**Best Practice**: Use Pattern B with explicit production requirements

### 5. Trailing Slash Handling

**Issue**: URL joining with trailing slashes
```typescript
// Bad: Double slash
baseUrl = "https://api.example.com/"
url = baseUrl + "/auth/login"  // "https://api.example.com//auth/login"

// Good: Normalized
baseUrl = "https://api.example.com"
url = `${baseUrl}/auth/login`  // "https://api.example.com/auth/login"
```

**Best Practice**: Normalize in single function, strip trailing slash from base URL

## Decision Summary

| Decision Point | Selected Approach | Rationale |
|----------------|-------------------|-----------|
| Environment detection | `process.env.NODE_ENV` | Next.js built-in, reliable |
| Production behavior | Throw error if no env var | Fail fast, catch config errors |
| Development behavior | Fallback to localhost:8000 | Preserve local workflow |
| CORS for previews | Use VERCEL_URL dynamically | Secure, supports all deployments |
| Trailing slash | Strip in getApiBase() | Single normalization point |
| Function name | `getApiBase()` | Shorter, matches new contract |

## Implementation Checklist

- [x] Identify root cause (missing apiBase.ts file)
- [x] Research Next.js environment variable handling
- [x] Research Vercel deployment environment variables
- [x] Research CORS best practices for FastAPI
- [x] Evaluate API base URL resolution patterns
- [x] Document selected approach with rationale
- [x] Create implementation contracts (see contracts/ directory)
- [ ] Implement getApiBase() function (see tasks.md)
- [ ] Update all frontend import sites (see tasks.md)
- [ ] Update backend CORS configuration (see tasks.md)
- [ ] Deploy and verify (see plan.md deployment section)

## References

- [Next.js Environment Variables](https://nextjs.org/docs/app/building-your-application/configuring/environment-variables)
- [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Vercel System Environment Variables](https://vercel.com/docs/projects/environment-variables/system-environment-variables)
