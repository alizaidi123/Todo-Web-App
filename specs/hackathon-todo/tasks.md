# Speckit Tasks - Phase II Hackathon Todo

## Atomic Tasks

### T1: Initialize monorepo structure
**Objective**: Set up the foundational monorepo structure with separate frontend and backend directories
- Create `frontend/` directory with Next.js project structure
- Create `backend/` directory with FastAPI project structure
- Configure root-level configuration files
- Set up shared dependencies and environment management
- Establish proper build and run scripts

### T2: Configure Neon PostgreSQL connection
**Objective**: Establish secure connection between backend and Neon PostgreSQL database
- Install SQLModel and related dependencies
- Configure database connection string using environment variables
- Set up connection pooling and SSL settings
- Create database initialization utilities
- Test database connectivity

### T3: Define SQLModel Task schema
**Objective**: Create the Task model with proper relationships and constraints
- Define TaskBase class with essential fields (title, description, completed, user_id)
- Create Task class extending TaskBase with database-specific fields (id, timestamps)
- Implement TaskCreate, TaskUpdate, and TaskResponse Pydantic models
- Add proper validation rules and constraints
- Include foreign key relationship to user

### T4: Implement FastAPI CRUD endpoints
**Objective**: Build complete CRUD operations for tasks with proper HTTP methods
- Create GET /api/tasks endpoint to retrieve user's tasks
- Create POST /api/tasks endpoint to create new tasks
- Create GET /api/tasks/{id} endpoint to retrieve specific task
- Create PUT /api/tasks/{id} endpoint to update specific task
- Create DELETE /api/tasks/{id} endpoint to delete specific task
- Create PATCH /api/tasks/{id}/complete endpoint to toggle completion status
- Implement proper request/response validation
- Add appropriate status codes and error handling

### T5: Implement JWT verification middleware
**Objective**: Add authentication layer to protect all endpoints with JWT verification
- Create JWT utility functions for token verification
- Implement FastAPI dependency for JWT authentication
- Extract user ID from JWT claims
- Add middleware to attach user context to requests
- Return 401 Unauthorized for invalid/missing tokens
- Ensure all endpoints require valid JWT

### T6: Setup Next.js App Router frontend
**Objective**: Configure Next.js frontend with App Router structure for todo functionality
- Set up app directory structure with layout and page components
- Create dashboard/page.tsx for task listing and creation
- Implement task management components (list, form, item)
- Add routing for different application views
- Configure global styles and layout
- Set up necessary dependencies and configurations

### T7: Integrate Better Auth on frontend
**Objective**: Add Better Auth authentication system to the frontend
- Install and configure Better Auth client
- Set up authentication pages (login, register, profile)
- Implement authentication context/provider
- Add protected route handling
- Configure JWT token issuance upon successful authentication
- Implement logout functionality

### T8: Attach JWT to frontend API requests
**Objective**: Ensure all API calls from frontend include proper JWT authentication
- Create API client utility with JWT inclusion
- Implement token retrieval from authentication context
- Add Authorization header with Bearer token to all API requests
- Handle token expiration and refresh if needed
- Implement error handling for authentication failures
- Add request/response interceptors if necessary

### T9: Enforce user isolation on backend
**Objective**: Ensure users can only access and modify their own tasks
- Add user ID verification in all CRUD endpoints
- Filter database queries by authenticated user ID
- Prevent unauthorized access to other users' tasks
- Return 403 Forbidden for cross-user access attempts
- Implement proper authorization checks in update/delete operations
- Add tests to verify user isolation functionality

### T10: Validate end-to-end functionality
**Objective**: Test complete user journey and ensure all components work together
- Test user registration and login flow
- Verify task creation, reading, updating, and deletion
- Confirm JWT authentication works across all endpoints
- Validate user isolation by testing cross-user access attempts
- Test error conditions and proper error responses
- Perform integration testing of frontend-backend communication
- Verify Neon PostgreSQL persistence works correctly
- Document any issues and finalize implementation