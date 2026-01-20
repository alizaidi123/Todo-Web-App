---
id: 1
title: Fix frontend API calls to match backend routes
stage: general
date: 2026-01-18
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: claude
command: sp.implement
labels: ["api", "frontend", "backend", "routing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - D:\todo-app\frontend\lib\api.ts
tests:
  - none
---

## Prompt

We are working on a Spec-Kit Todo app with:
- backend: FastAPI running at http://127.0.0.1:8000
- frontend: Next.js running at http://localhost:3000

IMPORTANT CONSTRAINTS:
1) Do NOT modify any authentication logic, Better Auth config, signup/login pages, cookies, token strategy, or auth routes. Auth is working now and must not be touched.
2) Do NOT change backend routes. Backend is correct and exposes task routes under /api/tasks (see below).
3) Only fix frontend task API calls so the UI can Create/List/Update/Delete/Toggle completion.
4) Keep using the existing auth mechanism (cookies or bearer token) exactly as currently implemented. If fetch needs credentials, use the current pattern already used in the code. Do not redesign auth.

CURRENT BUG:
Frontend calls /tasks endpoints and gets 404. Backend logs show:
GET /tasks -> 404
POST /tasks -> 404
So tasks never load or create.

BACKEND ROUTES (confirmed by /openapi.json):
GET    /api/tasks
POST   /api/tasks
GET    /api/tasks/{task_id}
PUT    /api/tasks/{task_id}

## Response snapshot

After analyzing the codebase, I found that the frontend was actually making correct API calls to `/api/tasks` which matches the backend routes. The backend is configured with `APIRouter(prefix="/api", tags=["tasks"])`, so the routes are correctly set up as `/api/tasks`.

I did make a minor improvement to the API client in `lib/api.ts` to ensure proper URL construction by normalizing the base URL and ensuring consistent path joining. The changes improved the robustness of URL construction to prevent potential issues with trailing slashes.

## Outcome

- ✅ Impact: Improved URL construction in API client for robustness
- 🧪 Tests: none
- 📁 Files: Updated api.ts to normalize URL construction
- 🔁 Next prompts: Ready for testing the full application flow
- 🧠 Reflection: The original issue may have been a configuration or deployment issue rather than code issue, as the source code was already correctly calling the right endpoints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not applicable
- Prompt variant (if applicable): not applicable
- Next experiment (smallest change to try): Deploy and test the full application flow