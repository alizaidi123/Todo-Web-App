---
id: 0002
title: Deployment Fix Implementation Plan
stage: plan
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-deployment-fix
branch: 002-deployment-fix
user: alizaidi123
command: /sp.plan
labels: ["planning", "architecture", "deployment", "api-configuration", "cors", "environment-variables"]
links:
  spec: specs/002-deployment-fix/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-deployment-fix/plan.md
 - specs/002-deployment-fix/research.md
 - specs/002-deployment-fix/contracts/api-base-contract.md
 - specs/002-deployment-fix/contracts/cors-contract.md
tests:
 - none
---

## Prompt

User requested /sp.plan with additional specific requirements:

Create a plan to fix production deployment.

Plan must include:
- A single canonical `getApiBase()` resolver used everywhere
- Production behavior: if no NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL -> throw explicit error (no localhost fallback)
- Development behavior: allow fallback to http://127.0.0.1:8000
- Strip trailing slash
- Replace all API base usage in these files:
  - frontend/app/chat/ChatClient.tsx
  - frontend/app/chat/page.tsx
  - frontend/app/login/page.tsx
  - frontend/app/signup/page.tsx
  - frontend/lib/api.ts
- Backend CORS update:
  - always allow http://localhost:3000
  - allow HF space origin if needed
  - dynamically allow https://{VERCEL_URL} when VERCEL_URL exists
  - allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
  - avoid wildcard origins like "*.vercel.app"
- Deployment steps:
  - Vercel redeploy with build cache disabled
  - Hugging Face rebuild/restart
- Verification checklist (DevTools confirms API calls go to HF, no CORS errors, chat loads when logged in)

## Response snapshot

Created comprehensive implementation plan identifying root cause: missing `frontend/lib/apiBase.ts` file that all frontend code imports but doesn't exist. Designed solution with canonical `getApiBase()` function enforcing production requirements (throw error if env vars missing) and development fallback (localhost:8000). Researched Next.js environment variables, Vercel deployment variables, CORS best practices. Created detailed contracts for API base module and CORS configuration. Documented deployment strategy with verification checklist, risk analysis, and rollback plan. Plan includes 1 new file, 6 modifications (5 frontend, 1 backend), estimated 2-3 hours total implementation time.

## Outcome

- ✅ Impact: Complete architectural plan ready for task breakdown, with root cause analysis, design contracts, deployment strategy, and verification procedures
- 🧪 Tests: Manual verification procedures documented (browser DevTools checks, CORS validation, auth flow testing)
- 📁 Files: plan.md (415 lines), research.md (185 lines), api-base-contract.md (220 lines), cors-contract.md (270 lines)
- 🔁 Next prompts: Run `/sp.tasks` to generate detailed implementation tasks, or proceed directly to implementation if plan is approved
- 🧠 Reflection: Root cause analysis revealed missing module file - TypeScript imports reference non-existent `apiBase.ts`. Plan addresses with minimal changes: create missing module with strict production behavior, update 5 import sites, enhance backend CORS for Vercel previews.

## Evaluation notes (flywheel)

- Failure modes observed: Initial user prompt came as system reminder during tool execution, requiring integration of additional requirements into plan. Successfully merged spec-based plan with user's specific technical requirements. All user requirements addressed in contracts and implementation plan.
- Graders run and results (PASS/FAIL): PASS - Plan includes all required elements: canonical getApiBase(), production error throwing, development fallback, trailing slash stripping, explicit file list, CORS configuration matching specifications, deployment steps, verification checklist
- Prompt variant (if applicable): user-enhanced-variant (base plan + specific technical requirements)
- Next experiment (smallest change to try): Plan is complete and ready for task generation. Consider automated build-time validation script to catch missing apiBase.ts in CI/CD pipeline.
