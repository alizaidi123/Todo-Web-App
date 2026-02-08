# Feature Specification: Phase 3 Deployment Fix

**Feature Branch**: `002-deployment-fix`
**Created**: 2026-02-08
**Status**: Draft
**Input**: User description: "Phase 3 Deployment Fix (Vercel frontend + HF backend) - Fix production environment configuration to ensure frontend calls backend correctly with proper CORS handling"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Production API Connectivity (Priority: P1)

As a user accessing the deployed application on Vercel, when I click "Chat with AI" while logged in, I should be taken to the chat interface without being redirected to the login page, and all API calls should successfully reach the Hugging Face backend.

**Why this priority**: This is the core functionality issue preventing the production deployment from working. Without this fix, the application is non-functional in production.

**Independent Test**: Can be fully tested by deploying to Vercel, logging in, clicking "Chat with AI", and verifying that the user stays on the /chat page and can interact with the AI chatbot.

**Acceptance Scenarios**:

1. **Given** a user is logged into the Vercel-deployed application, **When** they click "Chat with AI", **Then** they should be taken to the /chat page without being redirected to /login
2. **Given** the user is on the /chat page, **When** the page loads, **Then** browser DevTools should show API calls going to https://alisaboor3-todo-app.hf.space (not localhost)
3. **Given** the user is on the /chat page, **When** an API request is made to /auth/me, **Then** it should return successfully with user data (no CORS or PNA errors)

---

### User Story 2 - Local Development Preservation (Priority: P2)

As a developer working on the application locally, I should be able to run the application on localhost with the frontend calling the local backend without any changes to my workflow.

**Why this priority**: Maintaining local development workflow is critical for continued development, but the production fix is the immediate blocker.

**Independent Test**: Can be fully tested by running the application locally (npm run dev for frontend, uvicorn for backend) and verifying that API calls go to http://localhost:8000.

**Acceptance Scenarios**:

1. **Given** the application is running locally, **When** the frontend makes API calls, **Then** they should go to http://localhost:8000 (or configured local backend URL)
2. **Given** environment variables are set for local development, **When** the frontend starts, **Then** it should use those local environment variables
3. **Given** no environment variables are explicitly set, **When** running locally, **Then** the application should default to localhost:8000

---

### Edge Cases

- What happens when NEXT_PUBLIC_API_BASE_URL is not set in production? System should fail fast with clear error message rather than falling back to localhost.
- What happens when the backend is temporarily unavailable? Frontend should show appropriate error messages without exposing internal URLs.
- What happens when a developer runs a production build locally? Should use the same environment variable resolution as production.
- How does the system handle requests from multiple origins during deployment preview? Backend CORS must allow both production Vercel URL and preview URLs.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Frontend MUST never fall back to localhost URLs when running in production build mode
- **FR-002**: Frontend MUST read backend URL exclusively from NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL environment variables in production
- **FR-003**: Frontend MUST use localhost backend URL when running in local development mode
- **FR-004**: Backend MUST accept CORS requests from the Vercel production domain
- **FR-005**: Backend MUST accept CORS requests from localhost for local development
- **FR-006**: Authentication flow MUST remain intact - logged-in users should stay logged in when navigating to /chat
- **FR-007**: /auth/me endpoint MUST return successful responses for authenticated users without CORS or PNA errors
- **FR-008**: Environment variable configuration MUST be validated at build time or startup to catch missing configurations early
- **FR-009**: API client configuration MUST distinguish between development and production environments correctly
- **FR-010**: No new dependencies should be introduced to fix this issue

### Key Entities

- **API Client Configuration**: Manages the base URL and request configuration for all API calls, must correctly resolve environment variables based on build mode
- **CORS Policy**: Defines allowed origins for cross-origin requests, must include both production Vercel domain and local development origins
- **Authentication State**: User authentication status maintained across page navigation, must work consistently across localhost and production environments

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access the /chat page on production Vercel deployment without being redirected to /login
- **SC-002**: 100% of API calls from production Vercel deployment go to https://alisaboor3-todo-app.hf.space (0% to localhost)
- **SC-003**: /auth/me endpoint returns successful 200 responses for authenticated users on production deployment
- **SC-004**: Browser DevTools shows zero CORS errors or Private Network Access (PNA) errors on production deployment
- **SC-005**: Local development environment continues to work without any configuration changes or workflow disruption
- **SC-006**: Production build can be tested locally by setting environment variables and produces same behavior as Vercel deployment

## Scope *(mandatory)*

### In Scope

- Fix frontend API client to correctly use environment variables in production
- Remove or correct any localhost fallback logic in frontend code
- Configure backend CORS to allow requests from Vercel production domain
- Ensure authentication flow works correctly with the corrected API URLs
- Validate that local development workflow remains intact

### Out of Scope

- Changes to authentication mechanism or flows beyond fixing the API URL issue
- Adding new features or functionality to the chat interface
- Performance optimizations for API calls
- Adding new environment variables beyond NEXT_PUBLIC_API_BASE_URL/NEXT_PUBLIC_API_URL
- Changes to deployment pipeline or CI/CD workflows
- Refactoring unrelated code

## Assumptions *(optional)*

- Vercel environment variables (NEXT_PUBLIC_API_BASE_URL, NEXT_PUBLIC_API_URL) are correctly set to https://alisaboor3-todo-app.hf.space in all environments
- The Hugging Face backend is deployed and accessible at https://alisaboor3-todo-app.hf.space
- The issue is caused by frontend fallback logic, not by incorrect Vercel configuration
- Authentication tokens/cookies are being correctly sent with API requests
- The local development setup uses http://localhost:8000 for the backend
- The Vercel production domain follows the pattern https://[project-name].vercel.app

## Dependencies *(optional)*

### External Dependencies

- Vercel platform for frontend hosting (deployment environment)
- Hugging Face Spaces for backend hosting (Docker environment)
- Vercel environment variable configuration (must be correctly set)

### Internal Dependencies

- Frontend API client code (likely in frontend/lib/api.ts)
- Backend CORS configuration (likely in backend/app/main.py)
- Authentication middleware on frontend pages (/chat, /login)
- Environment variable resolution in Next.js build process

## Constraints *(optional)*

- **Minimal Changes**: Only modify code directly related to the API URL configuration and CORS issue
- **No New Dependencies**: Cannot add new npm packages or Python libraries
- **Backward Compatibility**: Local development workflow must remain unchanged
- **No Auth Changes**: Authentication flows and logic should not be modified except for fixing the URL issue
- **Same Day Fix**: This is a blocking production issue that should be resolved quickly

## Non-Functional Requirements *(optional)*

### Security

- API URLs should not be hardcoded with sensitive information
- CORS configuration should be restrictive (only allow specific origins, not wildcards in production)
- Authentication tokens should continue to be transmitted securely
- Error messages should not expose internal system details or localhost references

### Performance

- Environment variable resolution should not add noticeable latency to API calls
- CORS preflight requests should be cached appropriately to minimize overhead

### Reliability

- Configuration errors should fail fast with clear error messages rather than silently falling back to incorrect defaults
- Missing environment variables should be detected at build/startup time, not runtime

### Maintainability

- Environment variable naming should be consistent and self-documenting
- CORS configuration should be centralized and easy to update
- Code changes should include comments explaining the production vs development environment handling
