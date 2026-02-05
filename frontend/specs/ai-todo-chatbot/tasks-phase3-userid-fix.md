# AI Todo Chatbot Phase 3 - User ID Retrieval Fix

## Issue
Phase 3 chat route uses /api/{user_id}/chat. Frontend is incorrectly calling /api/2/chat, causing "not authorized for user 2".
Current implementation decodes JWT token directly to extract user_id, but should use the new /auth/me endpoint.

## Solution
Update app/chat/page.tsx (or the chat client flow) to:
1. Read token from existing getToken()
2. Call GET `${NEXT_PUBLIC_API_URL || http://127.0.0.1:8000}/auth/me` with Authorization Bearer token
3. Extract user_id from response
4. Use that user_id when calling POST /api/{user_id}/chat
5. Remove hardcoded user id logic
6. Redirect to /login if /auth/me fails (401)

## Phase 1: Setup and Configuration
- [ ] T001 Update app/chat/page.tsx to import necessary modules for API calls
- [ ] T002 Define API_BASE constant with fallback to NEXT_PUBLIC_API_URL or http://127.0.0.1:8000

## Phase 2: Authentication Flow Update
- [ ] T003 Replace JWT token decoding logic with /auth/me API call in useEffect
- [ ] T004 Implement error handling for /auth/me API call (redirect to /login on 401)
- [ ] T005 Extract user_id from /auth/me response and store in state

## Phase 3: Integration and Validation
- [ ] T006 Verify that clicking "Chat with AI" keeps user logged in
- [ ] T007 Confirm chat requests go to /api/<real_user_id>/chat instead of /api/2/chat
- [ ] T008 Test that "mark task 1 as completed" no longer returns authorization error
- [ ] T009 Ensure existing Phase 2 tasks UI remains unchanged

## Acceptance Criteria
- [ ] Clicking "Chat with AI" keeps user logged in
- [ ] Chat requests go to /api/<real_user_id>/chat not /api/2/chat
- [ ] "mark task 1 as completed" no longer returns authorization error
- [ ] If /auth/me fails (401), redirect to /login (existing behavior)
- [ ] Existing Phase 2 tasks UI remains unchanged