# Tasks: Auth Me Endpoint

## Feature: Auth Me Endpoint to Retrieve Current User Info

### Phase 1: Setup
- [X] T001 Create spec directory structure for auth/me endpoint feature

### Phase 2: Foundational Tasks
- [X] T002 [P] Review existing auth implementation in app/routes/auth.py
- [X] T003 [P] Review JWT token structure and get_current_user dependency in auth/jwt_handler.py
- [X] T004 [P] Examine current User model in app/user_models.py to understand available fields

### Phase 3: Auth Me Endpoint Implementation [US1]
- [X] T005 [US1] Add GET /auth/me route that depends on existing get_current_user
- [X] T006 [US1] Return JSON with user_id from TokenData in /auth/me endpoint
- [X] T007 [US1] Include username/email in response if available from User model
- [X] T008 [US1] Handle cases where TokenData doesn't have username/email gracefully
- [X] T009 [US1] Ensure /auth/me route is properly registered in app.main router
- [X] T010 [US1] Test that endpoint returns 200 with valid JWT token
- [X] T011 [US1] Test that endpoint returns 401 without valid JWT token

### Acceptance Criteria
- GET /auth/me with Authorization: Bearer <token> returns 200 and includes user_id
- Without token returns 401
- Response includes username/email if available, but doesn't break if not available
- Endpoint follows same auth pattern as existing routes
- No changes made to login/signup behavior

### Dependencies
- User Story 1 (US1) depends on foundational tasks T002-T004 being completed

### Parallel Execution Examples
- T002, T003, T004 can be executed in parallel during foundational phase
- T005-T011 can be executed sequentially during US1 implementation

### Implementation Strategy
- MVP: Implement basic /auth/me endpoint returning only user_id
- Enhancement: Add username/email to response if available
- Testing: Verify both success and failure cases