# Tasks: Phase 3 Deployment Fix

**Input**: Design documents from `/specs/002-deployment-fix/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, contracts/

**Tests**: Manual verification via browser DevTools (no automated tests required per spec)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/`, `backend/` at repository root
- Frontend: TypeScript/Next.js
- Backend: Python/FastAPI

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify prerequisites and create missing infrastructure file

- [ ] T001 Verify current git branch is `002-deployment-fix` using `git branch --show-current`
- [ ] T002 Verify no uncommitted changes that might conflict using `git status`
- [ ] T003 Verify backend main.py has `os` module available by checking imports at `backend/app/main.py` line 1-10

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the missing apiBase.ts module that all user stories depend on

**⚠️ CRITICAL**: This module is imported by 5 frontend files but doesn't exist. Must be created before ANY other changes.

- [ ] T004 [US1] Create new file `frontend/lib/apiBase.ts` with getApiBase() function implementation per contracts/api-base-contract.md
  - Export function: `export function getApiBase(): string`
  - Environment detection: Use `process.env.NODE_ENV === 'production'`
  - Production behavior: Read `process.env.NEXT_PUBLIC_API_BASE_URL` or `process.env.NEXT_PUBLIC_API_URL`, throw error if both missing
  - Development behavior: Fallback to `'http://127.0.0.1:8000'` if no env vars set, log warning to console
  - Normalization: Strip trailing slash if present using `.endsWith('/') ? url.slice(0, -1) : url`
  - Error message for production: `"Error: API base URL not configured for production. Please set NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL environment variable. Current NODE_ENV: production"`
  - Warning for development: `"Warning: API base URL not configured, using development default: http://127.0.0.1:8000. Set NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL to override."`

**Checkpoint**: apiBase.ts module created - frontend imports will now resolve correctly

---

## Phase 3: User Story 1 - Production API Connectivity (Priority: P1) 🎯 MVP

**Goal**: Fix production deployment so API calls go to Hugging Face backend instead of localhost, eliminating CORS errors and login redirects

**Independent Test**: Deploy to Vercel, login, click "Chat with AI", verify stays on /chat page with no CORS errors in DevTools

### Implementation for User Story 1

**Frontend Changes** (Update imports to use new getApiBase function):

- [ ] T005 [P] [US1] Update `frontend/lib/api.ts` line 2 to import from new module
  - Change: `import { getApiBaseUrl } from './apiBase';` → `import { getApiBase } from './apiBase';`
  - Change: Line 8 constructor usage: `this.baseUrl = getApiBaseUrl()...` → `this.baseUrl = getApiBase()...`
  - Remove duplicate getApiBase() calls in same expression (call once, store result)

- [ ] T006 [P] [US1] Update `frontend/app/chat/ChatClient.tsx` line 15 to import from new module
  - Change: `import { getApiBaseUrl } from '@/lib/apiBase';` → `import { getApiBase } from '@/lib/apiBase';`
  - Find line ~80 where API_BASE is set: Change `const API_BASE = getApiBaseUrl();` → `const API_BASE = getApiBase();`

- [ ] T007 [P] [US1] Update `frontend/app/chat/page.tsx` line 7 to import from new module
  - Change: `import { getApiBaseUrl } from '@/lib/apiBase';` → `import { getApiBase } from '@/lib/apiBase';`
  - Find line ~32 where API_BASE is set: Change `const API_BASE = getApiBaseUrl();` → `const API_BASE = getApiBase();`

- [ ] T008 [P] [US1] Update `frontend/app/login/page.tsx` line 9 to import from new module
  - Change: `import { getApiBaseUrl } from '@/lib/apiBase';` → `import { getApiBase } from '@/lib/apiBase';`
  - Find line ~21 where API_BASE is set: Change `const API_BASE = getApiBaseUrl();` → `const API_BASE = getApiBase();`

- [ ] T009 [P] [US1] Update `frontend/app/signup/page.tsx` line 9 to import from new module
  - Change: `import { getApiBaseUrl } from '@/lib/apiBase';` → `import { getApiBase } from '@/lib/apiBase';`
  - Find line ~34 where getApiBaseUrl() is called: Change `${getApiBaseUrl()}/auth/signup` → `${getApiBase()}/auth/signup`

**Backend Changes** (Update CORS for Vercel deployments):

- [ ] T010 [US1] Update `backend/app/main.py` CORS configuration for dynamic Vercel support
  - Verify `import os` exists at top of file (add if missing after line 1)
  - Locate `create_app()` function around line 10
  - Find `allowed_origins` list around line 15
  - Add to list if missing: `"http://localhost:3001"`, `"http://127.0.0.1:3000"`
  - After the list initialization (before add_middleware call), add Vercel URL detection:
    ```python
    # Vercel deployments (production + previews)
    vercel_url = os.getenv("VERCEL_URL")
    if vercel_url:
        # VERCEL_URL doesn't include protocol, add https://
        allowed_origins.append(f"https://{vercel_url}")
    ```
  - Verify middleware has: `allow_credentials=True`, `allow_methods=["*"]`, `allow_headers=["*"]`

**Checkpoint**: All code changes complete for User Story 1

### Local Verification for User Story 1

- [ ] T011 [US1] Test local development build (verify dev fallback works)
  - Command: `cd frontend && npm run dev`
  - Open browser DevTools > Console
  - Expected: Warning message about using development default appears
  - Expected: No errors about missing apiBase module
  - Command to stop: `Ctrl+C`

- [ ] T012 [US1] Test production build locally with env vars (verify production mode works)
  - Set env var: `$env:NEXT_PUBLIC_API_BASE_URL="https://alisaboor3-todo-app.hf.space"` (PowerShell)
  - Command: `cd frontend && npm run build`
  - Expected: Build succeeds without errors
  - Expected: No warnings about missing API base URL
  - Command: `npm run start` to test built app
  - Open browser, check console - should use HF Space URL
  - Command to stop: `Ctrl+C`

- [ ] T013 [US1] Test production build locally WITHOUT env vars (verify error thrown)
  - Remove env var: `Remove-Item Env:\NEXT_PUBLIC_API_BASE_URL` (PowerShell)
  - Command: `cd frontend && npm run build`
  - Expected: Build succeeds but app throws error at runtime when getApiBase() is called
  - Open browser, check console - should show "API base URL not configured for production" error
  - This is correct behavior - production requires explicit configuration

**Checkpoint**: Local testing complete, ready for deployment

### Deployment for User Story 1

- [ ] T014 [US1] Deploy backend changes to Hugging Face Spaces
  - Command: `git add backend/app/main.py`
  - Command: `git commit -m "Add dynamic CORS for Vercel deployments"`
  - Command: `git push hf 002-deployment-fix:main` (pushes to HF Space)
  - Alternative: Use HF Spaces UI to trigger rebuild from GitHub branch
  - Wait for Docker build to complete (check HF Spaces logs)
  - Verify backend is running: Open https://alisaboor3-todo-app.hf.space in browser
  - Expected: {"message": "Todo API is running!"}

- [ ] T015 [US1] Deploy frontend changes to Vercel
  - Verify Vercel environment variables are set in dashboard:
    - Navigate to Vercel dashboard > Project > Settings > Environment Variables
    - Confirm `NEXT_PUBLIC_API_BASE_URL=https://alisaboor3-todo-app.hf.space` for all environments (Production, Preview, Development)
    - Alternative variable: `NEXT_PUBLIC_API_URL=https://alisaboor3-todo-app.hf.space`
  - Command: `git add frontend/lib/apiBase.ts frontend/lib/api.ts frontend/app/`
  - Command: `git commit -m "Create apiBase module and update all import sites"`
  - Command: `git push origin 002-deployment-fix`
  - Vercel will auto-deploy preview from branch
  - In Vercel dashboard, find the preview deployment
  - **CRITICAL**: Redeploy without build cache:
    - Click preview deployment > three dots menu > "Redeploy"
    - **Uncheck** "Use existing Build Cache"
    - Click "Redeploy"
  - Wait for deployment to complete

**Checkpoint**: Both backend and frontend deployed

### Production Verification for User Story 1

- [ ] T016 [US1] Browser DevTools verification on production deployment
  - Open Vercel preview URL in **incognito/private window**
  - Open DevTools (F12) > Network tab
  - Navigate to signup page, create test account
  - Navigate to login page, log in with test account
  - Click "Chat with AI" button
  - **Verify**: Browser stays on /chat page (no redirect to /login) ✅ SC-001
  - **Verify**: Network tab shows all API calls to `https://alisaboor3-todo-app.hf.space` (not localhost) ✅ SC-002
  - **Verify**: /auth/me request shows Status 200 with user data ✅ SC-003
  - Open DevTools > Console tab
  - **Verify**: Zero CORS errors (no red errors about Access-Control-Allow-Origin) ✅ SC-004
  - **Verify**: Zero PNA (Private Network Access) errors ✅ SC-004
  - Try sending a chat message, verify AI responds
  - **Verify**: Authentication persists across page navigation

- [ ] T017 [US1] Document any issues found during verification
  - If CORS errors appear: Check backend logs for allowed origins
  - If localhost appears in Network tab: Check Vercel env vars are set and build cache was disabled
  - If redirected to login: Check /auth/me response in Network tab for error details
  - Create note in specs/002-deployment-fix/verification-results.md with screenshots if needed

**Checkpoint**: User Story 1 complete and verified - production deployment working

---

## Phase 4: User Story 2 - Local Development Preservation (Priority: P2)

**Goal**: Ensure local development workflow remains unchanged with proper fallback to localhost

**Independent Test**: Run `npm run dev` locally without env vars, verify API calls go to http://localhost:8000 or http://127.0.0.1:8000

### Implementation for User Story 2

**Note**: Implementation already complete in Phase 3 - the getApiBase() function includes development fallback

### Local Verification for User Story 2

- [ ] T018 [US2] Test local dev without environment variables (verify localhost fallback)
  - Remove any NEXT_PUBLIC env vars: `Remove-Item Env:\NEXT_PUBLIC_API_BASE_URL -ErrorAction SilentlyContinue` (PowerShell)
  - Start backend: `cd backend && uvicorn app.main:app --reload --port 8000`
  - In new terminal, start frontend: `cd frontend && npm run dev`
  - Open http://localhost:3000 in browser
  - Open DevTools > Console
  - **Verify**: Warning message appears: "Warning: API base URL not configured, using development default: http://127.0.0.1:8000" ✅
  - **Verify**: No errors about missing configuration
  - Open DevTools > Network tab
  - Navigate app (login, signup, chat)
  - **Verify**: All API calls go to `http://127.0.0.1:8000` ✅ SC-005
  - **Verify**: All features work normally (signup, login, chat) ✅ SC-005
  - Commands to stop: `Ctrl+C` in both terminals

- [ ] T019 [US2] Test local dev WITH environment variable override (verify env var takes precedence)
  - Set custom backend URL: `$env:NEXT_PUBLIC_API_BASE_URL="http://localhost:5000"` (PowerShell)
  - Start backend on port 5000: `cd backend && uvicorn app.main:app --reload --port 5000`
  - In new terminal, start frontend: `cd frontend && npm run dev`
  - Open http://localhost:3000 in browser
  - Open DevTools > Network tab
  - Navigate app
  - **Verify**: All API calls go to `http://localhost:5000` (env var respected)
  - **Verify**: No warning message in console (env var is set)
  - Commands to stop: `Ctrl+C` in both terminals

- [ ] T020 [US2] Test with alternate dev port (verify localhost:3001 CORS works)
  - Keep backend running on port 8000
  - Remove env var: `Remove-Item Env:\NEXT_PUBLIC_API_BASE_URL -ErrorAction SilentlyContinue`
  - Start frontend on port 3001: `cd frontend && npm run dev -- -p 3001`
  - Open http://localhost:3001 in browser
  - Navigate app
  - **Verify**: No CORS errors (backend allows localhost:3001) ✅
  - Command to stop: `Ctrl+C`

**Checkpoint**: User Story 2 complete and verified - local development workflow preserved

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, cleanup, and final validation

- [ ] T021 [P] Update project README.md with deployment fix notes
  - Add section: "## Deployment Configuration"
  - Document required environment variables for Vercel
  - Document VERCEL_URL usage for backend CORS
  - Note: Development fallback to localhost:8000

- [ ] T022 [P] Create deployment runbook at `specs/002-deployment-fix/DEPLOYMENT.md`
  - Copy deployment steps from plan.md
  - Add verification checklist
  - Add troubleshooting section for common issues
  - Add rollback procedure

- [ ] T023 Validate all acceptance criteria from spec.md are met
  - Review spec.md User Story 1 acceptance scenarios (lines 18-22)
  - Review spec.md User Story 2 acceptance scenarios (lines 35-38)
  - Confirm all edge cases addressed (spec.md lines 42-47)
  - Confirm all success criteria met (SC-001 through SC-006)

- [ ] T024 Prepare PR description with before/after comparison
  - Title: "Fix: Production deployment API URL configuration"
  - Include: Root cause (missing apiBase.ts)
  - Include: Solution summary (canonical getApiBase function)
  - Include: Files changed (1 new, 6 modified)
  - Include: Deployment verification checklist
  - Include: Screenshots from DevTools showing working production deployment

**Checkpoint**: All tasks complete, ready for PR and merge to main

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T003) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (T004) completion
- **User Story 2 (Phase 4)**: Implementation complete in Phase 3, only verification needed
- **Polish (Phase 5)**: Depends on User Stories 1 & 2 being complete and verified

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational T004 (apiBase.ts must exist)
- **User Story 2 (P2)**: No additional implementation - shares implementation with US1

### Within Each User Story

**User Story 1**:
- T004 (create apiBase.ts) must complete before T005-T009 (frontend updates)
- T005-T009 (frontend) can run in parallel (different files)
- T010 (backend) can run in parallel with T005-T009
- T011-T013 (local verification) must run after T005-T010
- T014 (backend deploy) should complete before T015 (frontend deploy)
- T015 (frontend deploy) must complete before T016-T017 (production verification)

**User Story 2**:
- T018-T020 (verification) can only run after User Story 1 implementation complete

### Parallel Opportunities

**Phase 2 (Foundational)**:
- Only 1 task (T004) - no parallelism

**Phase 3 (User Story 1 Implementation)**:
- T005, T006, T007, T008, T009 (all frontend updates) can run in parallel
- T010 (backend) can run in parallel with T005-T009

**Phase 3 (User Story 1 Verification)**:
- T011, T012, T013 (local tests) must run sequentially (use same dev server)
- T016, T017 (production verification) must run after deployment

**Phase 5 (Polish)**:
- T021, T022 (documentation) can run in parallel

---

## Parallel Example: User Story 1 Implementation

```bash
# After T004 (apiBase.ts) is complete, launch frontend updates in parallel:

# Terminal 1:
Task T005: "Update frontend/lib/api.ts imports"

# Terminal 2:
Task T006: "Update frontend/app/chat/ChatClient.tsx imports"

# Terminal 3:
Task T007: "Update frontend/app/chat/page.tsx imports"

# Terminal 4:
Task T008: "Update frontend/app/login/page.tsx imports"

# Terminal 5:
Task T009: "Update frontend/app/signup/page.tsx imports"

# Terminal 6 (parallel with above):
Task T010: "Update backend/app/main.py CORS configuration"
```

All 6 tasks (T005-T010) operate on different files and can complete simultaneously.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003) - 5 minutes
2. Complete Phase 2: Foundational (T004) - 15 minutes
3. Complete Phase 3: User Story 1 (T005-T017) - 1-2 hours including deployment
4. **STOP and VALIDATE**: Production deployment working
5. Deploy/demo if ready

**Result**: Production deployment fixed, application functional on Vercel

### Incremental Delivery

1. Complete Setup + Foundational → apiBase.ts created
2. Add User Story 1 implementation → Test locally → Deploy → Verify production (MVP!)
3. Add User Story 2 verification → Confirm local dev still works
4. Polish → Documentation and PR

### Sequential Execution (Single Developer)

1. T001-T003: Setup (verify prerequisites)
2. T004: Create apiBase.ts
3. T005-T010: Update all import sites (can batch commit)
4. T011-T013: Local verification
5. T014: Deploy backend
6. T015: Deploy frontend
7. T016-T017: Production verification
8. T018-T020: Local dev verification
9. T021-T024: Documentation and PR prep

**Estimated Time**: 2-3 hours total

---

## Critical Success Factors

### Must-Have Before Deployment

1. ✅ apiBase.ts file exists with correct getApiBase() implementation
2. ✅ All 5 frontend files updated to import from new module
3. ✅ Backend CORS includes VERCEL_URL support
4. ✅ Vercel environment variables confirmed in dashboard
5. ✅ Local tests pass (T011-T013)

### Deployment Requirements

1. ✅ Backend deployed and running on HF Spaces
2. ✅ Frontend redeployed with build cache disabled
3. ✅ Production verification checklist complete (T016)

### Verification Checklist

From spec.md Success Criteria:

- [ ] SC-001: Users can access /chat without redirect to /login
- [ ] SC-002: 100% API calls to HF backend (0% localhost)
- [ ] SC-003: /auth/me returns 200 with user data
- [ ] SC-004: Zero CORS errors in DevTools Console
- [ ] SC-004: Zero PNA errors in DevTools Console
- [ ] SC-005: Local dev works without env vars
- [ ] SC-006: Local prod build works with env vars

---

## Troubleshooting Guide

### Issue: Build fails with "Cannot find module './apiBase'"

**Cause**: Task T004 not completed (file doesn't exist yet)
**Solution**: Complete T004 first to create frontend/lib/apiBase.ts

### Issue: Production deployment still calls localhost

**Cause**: Build cache contains old broken code
**Solution**: Redeploy in Vercel with "Use existing Build Cache" unchecked

### Issue: CORS errors on production

**Cause 1**: Backend not deployed yet with VERCEL_URL support
**Solution**: Complete T014 to deploy backend changes

**Cause 2**: VERCEL_URL not being set by Vercel
**Solution**: Check Vercel deployment logs, VERCEL_URL should be automatic

### Issue: Local dev throws "API base URL not configured" error

**Cause**: Production build mode being used locally
**Solution**: Use `npm run dev` (not `npm run build`), development mode has localhost fallback

### Issue: Env vars not taking effect

**Cause**: Next.js inlines env vars at build time, not runtime
**Solution**: Must rebuild frontend after changing env vars (npm run build)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [US1] = User Story 1 task (Production API Connectivity)
- [US2] = User Story 2 task (Local Development Preservation)
- All file paths are from repository root
- Commit after each logical group of tasks
- Stop at any checkpoint to validate independently
- Backend deployment before frontend deployment (avoid CORS timing issues)
- Always disable build cache when deploying apiBase.ts changes
- Local verification before production deployment reduces risk
