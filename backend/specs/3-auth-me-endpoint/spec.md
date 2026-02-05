# Spec: Auth Me Endpoint

## Feature: Auth Me Endpoint to Retrieve Current User Info

### Overview
Currently, the chat endpoint requires `/api/{user_id}/chat` but the frontend is hardcoded to call `/api/2/chat`. We need a minimal endpoint that allows the frontend to learn the current user ID from the JWT token without exposing sensitive information.

### User Stories

#### Story 1: Frontend Needs Access to Current User ID (P1)
**As a** frontend application
**I want** to retrieve my current user ID from the JWT token
**So that** I can construct the correct chat endpoint URL with the dynamic user ID

**Acceptance Criteria:**
- GET /auth/me with valid Authorization: Bearer <token> returns 200
- Response includes "user_id" field from the token
- Response may include username/email if available from User model
- Without valid token returns 401 Unauthorized
- Endpoint uses existing get_current_user dependency
- No changes to existing login/signup flows

### Technical Requirements
- Use existing get_current_user dependency from auth/jwt_handler.py
- Return JSON response with at least { "user_id": <token_user_id> }
- Optionally include username/email if available, but don't break if not available
- Register route in main app like other auth routes
- Maintain existing auth security patterns
- Do not modify login/signup behavior

### Out of Scope
- Changing login/signup endpoints or behavior
- Modifying JWT token creation process
- Adding new authentication methods
- Changing existing user model structure