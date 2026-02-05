# AI Todo Chatbot Implementation Tasks

## Phase 1: Setup and Configuration
- [X] Configure API base URL in ChatClient component
- [X] Implement environment variable fallback mechanism
- [X] Update API call to use absolute URL with user ID

## Phase 2: Core Implementation
- [X] Modify axios.post() call to use ${API_BASE}/api/${userId}/chat
- [X] Ensure Authorization header reuses existing token system
- [X] Test API connection with backend endpoint

## Phase 3: User ID Retrieval Fix
- [X] T001 Update app/chat/page.tsx to import axios for API calls
- [X] T002 Replace JWT token decoding logic with /auth/me API call in useEffect
- [X] T003 Define API_BASE constant with fallback to NEXT_PUBLIC_API_URL or http://127.0.0.1:8000
- [X] T004 Call GET /auth/me endpoint with Authorization Bearer token
- [X] T005 Extract user_id from /auth/me response and store in state
- [X] T006 Implement error handling for /auth/me API call (redirect to /login on 401)
- [X] T007 Remove hardcoded user ID logic from JWT token decoding
- [X] T008 Update ChatClient component to receive dynamic user ID

## Phase 4: Integration and Testing
- [X] T009 Verify chat functionality connects to FastAPI backend with correct user ID
- [X] T010 Test that clicking "Chat with AI" keeps user logged in
- [X] T011 Confirm chat requests go to /api/<real_user_id>/chat instead of /api/2/chat
- [X] T012 Test that "mark task 1 as completed" no longer returns authorization error
- [X] T013 Verify existing Phase 2 tasks UI remains unchanged

## Phase 5: Validation
- [X] T014 Test end-to-end chat functionality with dynamic user ID
- [X] T015 Verify error handling for network issues and 401 responses
- [X] T016 Confirm proper user ID derivation from /auth/me endpoint
- [X] T017 Validate JWT token reuse in authorization header for both /auth/me and chat calls

## Dependencies
- Backend /auth/me endpoint must be available and functional
- Existing authentication system must remain unchanged

## Parallel Execution Examples
- T001, T002, T003 can be executed in parallel (setup tasks)
- T004, T005, T006 can be executed in parallel (API integration tasks)

## Implementation Strategy
1. MVP: Basic /auth/me integration with user ID retrieval
2. Enhancement: Error handling and proper redirects
3. Validation: Complete testing with various scenarios