# Speckit Specification - Phase II Hackathon Todo

## User Journeys

1. **User signs up and signs in using Better Auth**
   - User accesses the signup/login page
   - User provides credentials through Better Auth
   - User receives JWT token upon successful authentication

2. **User creates a todo task**
   - Authenticated user submits a new task via the UI
   - Task is associated with the authenticated user's ID
   - Task is stored in the database

3. **User views only their own tasks**
   - Authenticated user navigates to the tasks page
   - Backend verifies user's JWT token
   - Backend returns only tasks belonging to the authenticated user

4. **User updates a task**
   - Authenticated user selects a task to update
   - User modifies task details and saves changes
   - Backend verifies user owns the task before allowing update

5. **User deletes a task**
   - Authenticated user selects a task to delete
   - Backend verifies user owns the task before deletion
   - Task is removed from the database

6. **User marks a task as complete**
   - Authenticated user toggles completion status of a task
   - Backend verifies user owns the task before updating
   - Task completion status is updated in the database

## Functional Requirements

- **Multi-user support**: System supports multiple users with individual accounts
- **Persistent storage in Neon PostgreSQL**: All data is stored durably in Neon Serverless PostgreSQL
- **RESTful API**: Backend exposes RESTful endpoints for all operations
- **JWT required for all backend requests**: Every API call must include a valid JWT token
- **Unauthorized requests return 401**: Requests without valid JWT return HTTP 401 status
- **Tasks are always user-isolated**: Users can only access their own tasks, never others'

## Non-Functional Requirements

- **Backend is stateless**: Backend service maintains no session state between requests
- **No sessions or cookies on backend**: Authentication relies solely on JWT tokens passed in headers
- **Simple and readable architecture**: Codebase remains simple and easy to understand, favoring clarity over complex abstractions