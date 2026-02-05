---
id: 3
title: Add Auth Me Endpoint
stage: tasks
date_iso: 2026-01-28
surface: agent
model: Claude Sonnet 4.5
feature: auth-me-endpoint
branch: 1-ai-todo-chatbot
user: user
command: sp.tasks
labels: ["auth", "endpoint", "user-id", "jwt"]
links:
  spec: specs/3-auth-me-endpoint/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "app/routes/auth.py"
  - "app/user_models.py"
  - "specs/3-auth-me-endpoint/spec.md"
  - "specs/3-auth-me-endpoint/plan.md"
  - "specs/3-auth-me-endpoint/tasks.md"
tests_yaml:
  -
outcome: Successfully implemented the /auth/me endpoint allowing frontend to retrieve current user ID from JWT token
---

# Add Auth Me Endpoint

## PROMPT_TEXT

We have a Phase 3 issue: chat endpoint requires /api/{user_id}/chat, but frontend is calling /api/2/chat (hardcoded/wrong).

Backend auth returns TokenData (has user_id) and should enforce user isolation.
We need a minimal endpoint to allow frontend to learn the current user id from the JWT.

TASKS:
1) Add a new route GET /auth/me that:
   - Depends on existing get_current_user
   - Returns JSON with at least: { "user_id": <token_user_id> }
   - If available, also include username/email, but do not break if TokenData does not have them.
2) Ensure /auth/me is registered in app.main router (like other auth routes).
3) Do NOT change login/signup behavior.
4) Keep it minimal, safe, and consistent with current auth structure.

Acceptance:
- GET /auth/me with Authorization: Bearer <token> returns 200 and includes user_id.
- Without token returns 401.

## RESPONSE_TEXT

Successfully generated and implemented the tasks for the auth/me endpoint. Created the complete spec, plan, and tasks documents in the specs/3-auth-me-endpoint/ directory, and implemented the actual endpoint in app/routes/auth.py with supporting changes to app/user_models.py.

The implementation includes:
- UserMeResponse model for the endpoint response
- GET /auth/me endpoint using existing get_current_user dependency
- Proper error handling and security
- Automatic registration through existing auth router

All requirements have been met and the endpoint is ready for the frontend to use.

## EVALUATION

All tasks have been completed successfully:
- [X] Created spec documentation outlining the user story and requirements
- [X] Created architectural plan with security considerations
- [X] Generated detailed task breakdown
- [X] Implemented the /auth/me endpoint with proper authentication
- [X] Ensured endpoint returns user_id and optionally username/email
- [X] Verified endpoint integrates with existing auth system
- [X] Confirmed no changes were made to login/signup behavior
- [X] Tested that application loads correctly with new endpoint