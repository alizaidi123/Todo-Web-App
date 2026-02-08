# Implementation Plan: Phase 3 Deployment Fix

**Branch**: `002-deployment-fix` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-deployment-fix/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Fix production deployment issue where Next.js frontend falls back to localhost instead of using Hugging Face backend URL. The root cause is a missing `apiBase.ts` module that all frontend files import but doesn't exist in the repository. This causes build failures or runtime errors leading to auth failures and redirects to login.

**Solution**: Create a canonical `getApiBase()` function that enforces environment-specific behavior:
- **Production**: Require NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL, throw error if missing (no localhost fallback)
- **Development**: Allow fallback to http://127.0.0.1:8000 if env vars not set
- Update backend CORS to dynamically allow Vercel preview URLs using VERCEL_URL environment variable

## Technical Context

**Language/Version**: TypeScript (Next.js frontend), Python 3.11 (FastAPI backend)
**Primary Dependencies**: Next.js 14+, FastAPI, axios (frontend HTTP client)
**Storage**: N/A (configuration change only)
**Testing**: Manual verification via browser DevTools, deployment testing
**Target Platform**: Vercel (frontend), Hugging Face Spaces Docker (backend)
**Project Type**: Web application (separate frontend/backend)
**Performance Goals**: No performance impact - configuration change only
**Constraints**: Must not break local development workflow, must work with Vercel preview deployments
**Scale/Scope**: 1 new file, 6 file modifications (5 frontend, 1 backend)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: Constitution file contains only template placeholders. Applying standard web application best practices:

- ✅ **No New Dependencies**: Solution uses existing packages only
- ✅ **Minimal Changes**: Focused only on API URL resolution and CORS configuration
- ✅ **Testable**: Can be verified through browser DevTools and deployment testing
- ✅ **Environment Separation**: Clear distinction between development and production behavior
- ✅ **Fail Fast**: Production mode throws explicit errors for missing configuration

## Project Structure

### Documentation (this feature)

```text
specs/002-deployment-fix/
├── spec.md              # Feature specification
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - environment variable best practices
├── contracts/           # Phase 1 output - API contract (minimal, just env var contract)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── lib/
│   ├── apiBase.ts       # NEW: Canonical API base URL resolver
│   ├── api.ts           # MODIFIED: Use new getApiBase() function
│   └── auth-utils.ts    # No changes needed
├── app/
│   ├── chat/
│   │   ├── ChatClient.tsx   # MODIFIED: Use new getApiBase() function
│   │   └── page.tsx         # MODIFIED: Use new getApiBase() function
│   ├── login/
│   │   └── page.tsx         # MODIFIED: Use new getApiBase() function
│   └── signup/
│       └── page.tsx         # MODIFIED: Use new getApiBase() function

backend/
└── app/
    └── main.py          # MODIFIED: Dynamic CORS with VERCEL_URL support
```

**Structure Decision**: Existing web application structure with separate frontend/backend. All changes are in-place modifications to existing files plus one new utility module.

## Complexity Tracking

No constitution violations - all changes follow standard patterns for environment configuration.

## Phase 0: Research

### Environment Variable Best Practices in Next.js

**Decision**: Use `process.env.NODE_ENV` to distinguish development from production

**Rationale**:
- Next.js automatically sets `NODE_ENV` to 'development' for `next dev` and 'production' for `next build`
- This is more reliable than custom environment variables
- Prevents accidental localhost usage in production builds

**Alternatives considered**:
- Custom environment variable like `APP_ENV` - Rejected because it requires additional configuration and can get out of sync
- Runtime detection via `window.location` - Rejected because it fails at build time and doesn't catch configuration errors early

### API Base URL Resolution Strategy

**Decision**: Single canonical function with explicit production requirements

**Rationale**:
- Centralized logic prevents inconsistent behavior across files
- Explicit error in production mode catches misconfiguration during deployment
- Fallback only in development preserves local workflow

**Alternatives considered**:
- Silent fallback in all environments - Rejected because it hides production configuration errors
- Separate functions for dev/prod - Rejected because it requires caller to choose correctly
- Environment-specific build outputs - Rejected as over-engineered for this use case

### CORS Configuration for Vercel Preview Deployments

**Decision**: Use `VERCEL_URL` environment variable for dynamic origin allowance

**Rationale**:
- Vercel automatically sets `VERCEL_URL` for all deployments (production and preview)
- Allows preview deployments to work without hardcoding URLs
- More secure than wildcard patterns like `*.vercel.app`

**Alternatives considered**:
- Wildcard CORS origins - Rejected due to security concerns (allows any subdomain)
- Hardcode production URL only - Rejected because it breaks preview deployments
- Regular expression patterns - Rejected as unnecessarily complex

### Trailing Slash Handling

**Decision**: Strip trailing slashes from base URL in canonical function

**Rationale**:
- Prevents double-slash issues when joining with endpoint paths
- Single normalization point is more maintainable
- Consistent behavior across all API calls

**Alternatives considered**:
- Handle in each caller - Rejected due to duplication and inconsistency risk
- Require callers to normalize - Rejected because it's error-prone

## Phase 1: Design & Contracts

### API Base URL Module Contract

**Module**: `frontend/lib/apiBase.ts`

**Exports**:
```typescript
/**
 * Get the API base URL based on environment
 * @returns Base URL without trailing slash
 * @throws Error in production if NEXT_PUBLIC_API_BASE_URL and NEXT_PUBLIC_API_URL are both missing
 */
export function getApiBase(): string
```

**Behavior Contract**:

| Environment | Env Vars Set | Returns | Error |
|-------------|-------------|---------|-------|
| Production | NEXT_PUBLIC_API_BASE_URL=https://api.example.com | https://api.example.com | No |
| Production | NEXT_PUBLIC_API_URL=https://api.example.com/ | https://api.example.com | No |
| Production | Neither set | N/A | Yes: "API base URL not configured..." |
| Production | Both set | Uses NEXT_PUBLIC_API_BASE_URL (priority) | No |
| Development | NEXT_PUBLIC_API_BASE_URL=https://api.example.com | https://api.example.com | No |
| Development | Neither set | http://127.0.0.1:8000 | No |

**Environment Detection**:
- Production: `process.env.NODE_ENV === 'production'`
- Development: `process.env.NODE_ENV === 'development'` or undefined

**Normalization**:
- Strip trailing slash if present: `url.endsWith('/') ? url.slice(0, -1) : url`

### Backend CORS Configuration Contract

**File**: `backend/app/main.py`

**Allowed Origins Logic**:

```python
allowed_origins = [
    "http://localhost:3000",      # Local development (Next.js default)
    "http://localhost:3001",       # Local development (alternate port)
    "http://127.0.0.1:3000",      # Local development (explicit localhost)
]

# Production Hugging Face Space domain
allowed_origins.append("https://alisaboor3-todo-app.hf.space")

# Vercel deployments (production + previews)
vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    # VERCEL_URL doesn't include protocol, add https://
    allowed_origins.append(f"https://{vercel_url}")
```

**CORS Middleware Configuration**:
```python
CORSMiddleware(
    allow_origins=allowed_origins,    # List above, NO wildcards
    allow_credentials=True,            # Required for auth cookies/tokens
    allow_methods=["*"],               # Allow all HTTP methods
    allow_headers=["*"],               # Allow all headers
)
```

**Security Notes**:
- No wildcard origins (`*` or `*.vercel.app`)
- Explicit protocol (https) for production origins
- Localhost allowed for development only

### Frontend Migration Pattern

**Current Pattern** (broken):
```typescript
import { getApiBaseUrl } from '@/lib/apiBase';  // Module doesn't exist!
const API_BASE = getApiBaseUrl();
```

**New Pattern**:
```typescript
import { getApiBase } from '@/lib/apiBase';     // New module
const API_BASE = getApiBase();
```

**Files to Update**:
1. `frontend/lib/api.ts` - Update ApiClient constructor
2. `frontend/app/chat/ChatClient.tsx` - Update axios calls
3. `frontend/app/chat/page.tsx` - Update /auth/me call
4. `frontend/app/login/page.tsx` - Update /auth/login call
5. `frontend/app/signup/page.tsx` - Update /auth/signup call

### Error Messages

**Production Missing Config Error**:
```
Error: API base URL not configured for production.
Please set NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL environment variable.
Current NODE_ENV: production
```

**Development Fallback Warning** (console.warn):
```
Warning: API base URL not configured, using development default: http://127.0.0.1:8000
Set NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL to override.
```

## Phase 2: Implementation Tasks Overview

**Task Groups** (detailed breakdown in `/sp.tasks`):

1. **Create API Base Module** (frontend/lib/apiBase.ts)
   - Implement getApiBase() function
   - Add environment detection logic
   - Add error handling for production
   - Add development fallback with warning
   - Add trailing slash normalization

2. **Update Frontend API Calls** (5 files)
   - frontend/lib/api.ts
   - frontend/app/chat/ChatClient.tsx
   - frontend/app/chat/page.tsx
   - frontend/app/login/page.tsx
   - frontend/app/signup/page.tsx

3. **Update Backend CORS** (backend/app/main.py)
   - Add os import if missing
   - Add VERCEL_URL detection
   - Update allowed_origins list
   - Verify middleware configuration

4. **Deployment & Verification**
   - Deploy to Vercel (disable build cache)
   - Verify environment variables set
   - Restart Hugging Face backend
   - Test with browser DevTools

## Deployment Strategy

### Pre-Deployment Checklist

- [ ] All code changes committed to `002-deployment-fix` branch
- [ ] Local testing completed (verify dev mode still works)
- [ ] Production build test locally with env vars set
- [ ] Backend changes deployed to Hugging Face Spaces
- [ ] Vercel environment variables confirmed in dashboard

### Deployment Steps

1. **Backend Deployment (Hugging Face Spaces)**:
   ```bash
   # Changes auto-deploy via git push to HF Space
   git push hf 002-deployment-fix:main
   # Or trigger rebuild in HF Spaces UI
   ```
   - Wait for Docker build to complete
   - Verify app is running at https://alisaboor3-todo-app.hf.space

2. **Frontend Deployment (Vercel)**:
   - Push branch to GitHub: `git push origin 002-deployment-fix`
   - Vercel auto-deploys preview
   - **Important**: Disable build cache for this deployment (Vercel dashboard > Deployment > Redeploy > uncheck "Use existing build cache")
   - Verify environment variables in Vercel dashboard:
     - `NEXT_PUBLIC_API_BASE_URL=https://alisaboor3-todo-app.hf.space`
     - `NEXT_PUBLIC_API_URL=https://alisaboor3-todo-app.hf.space`

3. **Merge to Main** (after verification):
   - Create PR from `002-deployment-fix` to `main`
   - Verify production deployment succeeds
   - Monitor for any runtime errors

### Verification Checklist

**Browser DevTools Verification**:
- [ ] Open production site in incognito window
- [ ] Open DevTools > Network tab
- [ ] Log in to application
- [ ] Click "Chat with AI"
- [ ] Verify stays on /chat page (no redirect to /login)
- [ ] Verify all API calls in Network tab go to `https://alisaboor3-todo-app.hf.space`
- [ ] Verify zero CORS errors in Console tab
- [ ] Verify zero "Private Network Access" (PNA) errors
- [ ] Verify /auth/me returns 200 status

**Functional Verification**:
- [ ] Can sign up new user
- [ ] Can log in
- [ ] Can access chat interface
- [ ] Can send message to AI
- [ ] Can receive AI response
- [ ] Auth persists across page navigation

**Local Development Verification** (after merge):
- [ ] `npm run dev` works without env vars (uses localhost fallback)
- [ ] API calls go to http://127.0.0.1:8000
- [ ] Warning message appears in console about using dev default
- [ ] All features work locally

## Risk Analysis

### High Risk Items

1. **Vercel Build Cache**
   - **Risk**: Old build with broken imports persists
   - **Mitigation**: Explicitly disable build cache during redeploy
   - **Detection**: Check build logs for apiBase.ts compilation

2. **Environment Variable Precedence**
   - **Risk**: NEXT_PUBLIC_API_URL takes priority over NEXT_PUBLIC_API_BASE_URL
   - **Mitigation**: Clear documentation in code comments
   - **Detection**: Log actual resolved URL during build

3. **CORS Timing**
   - **Risk**: Frontend deploys before backend CORS update
   - **Mitigation**: Deploy backend first, then frontend
   - **Detection**: CORS errors in browser console

### Medium Risk Items

1. **Preview Deployments**
   - **Risk**: VERCEL_URL might not be set in all preview contexts
   - **Mitigation**: Test with preview deployment before merging
   - **Fallback**: Can manually add preview URL to CORS if needed

2. **Local Development Disruption**
   - **Risk**: Developers with custom env vars see unexpected behavior
   - **Mitigation**: Document expected behavior in PR description
   - **Detection**: Team testing before merge

### Rollback Plan

If production deployment fails:

1. **Immediate**: Revert Vercel deployment to last known good version
2. **Backend**: Revert HF Spaces to previous commit (git revert)
3. **Investigation**: Check build logs and browser console
4. **Fix Forward**: Address issues in branch and redeploy

## Success Criteria Mapping

| Success Criterion | Verification Method | Expected Result |
|-------------------|---------------------|-----------------|
| SC-001: Access /chat without redirect | Manual test on production | User stays on /chat after login |
| SC-002: 100% API calls to HF backend | DevTools Network tab | All requests to alisaboor3-todo-app.hf.space |
| SC-003: /auth/me returns 200 | DevTools Network tab | Status 200, user data returned |
| SC-004: Zero CORS/PNA errors | DevTools Console tab | No red CORS or PNA errors |
| SC-005: Local dev unchanged | `npm run dev` test | Works without env vars |
| SC-006: Local prod build works | `npm run build` with env vars | Behaves like Vercel deployment |

## Dependencies

**Blocked By**: None (ready to start)

**Blocks**: None (production fix is independent)

**External Dependencies**:
- Vercel platform operational
- Hugging Face Spaces operational
- GitHub Actions for auto-deployment

## Timeline Estimate

- **Phase 0 Research**: Complete (documented above)
- **Phase 1 Design**: Complete (documented above)
- **Phase 2 Implementation**: 1-2 hours (simple code changes)
- **Testing & Deployment**: 1 hour (includes verification)
- **Total**: 2-3 hours end-to-end

## Notes

- This is a critical production fix - prioritize over new features
- Changes are minimal and focused - reduces risk
- Backend CORS change is additive only (doesn't remove existing origins)
- Frontend change consolidates existing scattered logic into one function
- No database migrations or schema changes required
- No user data affected by this change
