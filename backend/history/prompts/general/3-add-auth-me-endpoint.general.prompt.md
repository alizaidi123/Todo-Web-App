---
id: 3
title: Add Auth Me Endpoint
stage: general
date_iso: 2026-01-28
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 1-ai-todo-chatbot
user: user
command: sp.tasks
labels: ["auth", "endpoint", "user-id", "jwt"]
links:
  spec: null
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
  - "test_auth_me_endpoint.py"
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

Successfully implemented the /auth/me endpoint as requested. Here's what was done:

1. Added UserMeResponse Pydantic model to app/user_models.py to define the response structure
2. Updated app/routes/auth.py to include:
   - Import of TokenData and get_current_user dependency
   - Helper function get_user_by_id to fetch user details from database
   - New GET /auth/me endpoint that:
     * Uses the existing get_current_user dependency for authentication
     * Looks up user details in the database using the user_id from the token
     * Returns user_id from token plus username/email from database
     * Handles cases where user might not be found in the database
3. Created spec, plan, and tasks documents in specs/3-auth-me-endpoint/

The endpoint follows the exact requirements:
- Depends on existing get_current_user for authentication
- Returns JSON with user_id from the token
- Includes username/email if available from the database
- Maintains existing security patterns (returns 401 without valid token)
- Does not modify login/signup behavior
- Is automatically registered through the existing auth router inclusion in main.py

## OUTCOME

The /auth/me endpoint is now available and ready for the frontend to use to dynamically determine the user ID for constructing the correct chat endpoint URL. The implementation is minimal, secure, and consistent with existing auth patterns.