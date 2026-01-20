# Speckit Plan - Phase II Hackathon Todo

## Architecture Overview

The application follows a monorepo structure with separate frontend and backend services, connected via a RESTful API. The frontend handles user interaction and authentication, while the backend manages data persistence and business logic.

## Monorepo Structure

```
todo-app/
├── frontend/           # Next.js application
│   ├── app/            # App Router pages
│   ├── components/     # Reusable UI components
│   ├── lib/            # Utility functions and API clients
│   └── public/         # Static assets
├── backend/            # FastAPI application
│   ├── app/            # API routes and models
│   ├── auth/           # JWT verification utilities
│   ├── database/       # SQLModel definitions and connections
│   └── main.py         # Application entry point
└── shared/             # Shared types and constants (optional)
```

## Next.js Frontend Responsibilities

- Handle user authentication via Better Auth
- Issue JWT tokens to the backend on user login
- Manage user interface for todo operations
- Interact with backend API using JWT-authenticated requests
- Store JWT securely in browser (localStorage or httpOnly cookie)
- Display user-specific tasks only
- Handle form submissions for task CRUD operations

## FastAPI Backend Responsibilities

- Verify JWT tokens for all incoming requests
- Extract user identity from JWT claims
- Perform database operations for tasks
- Ensure user data isolation (users only access their own tasks)
- Return appropriate HTTP status codes
- Handle error responses consistently
- Maintain stateless operation (no server-side sessions)

## JWT Authentication Flow

1. **Better Auth issues JWT on frontend**
   - User authenticates through Better Auth
   - Frontend receives user information and generates JWT using shared secret
   - JWT contains user ID and expiration time

2. **Frontend attaches JWT to API requests**
   - All API calls include `Authorization: Bearer <token>` header
   - Token validity maintained across user session

3. **FastAPI verifies JWT using shared secret**
   - Middleware intercepts requests to protected endpoints
   - JWT signature verified against shared secret
   - Expired or invalid tokens rejected with 401 status

4. **User identity extracted from token**
   - Valid JWT payload parsed to extract user ID
   - User ID used to scope database queries
   - Requests proceed with authenticated user context

## SQLModel Schema for Tasks

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: int  # Foreign key to user

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

## Neon PostgreSQL Integration

- Connection managed through SQLModel and SQLAlchemy
- Environment variables for database connection string
- Connection pooling for optimal performance
- SSL encryption enabled by default with Neon
- Database migrations handled separately

## REST API Endpoint Structure

```
POST   /api/auth/login     # Login (handled by Better Auth frontend)
GET    /api/tasks          # Retrieve user's tasks
POST   /api/tasks          # Create new task
GET    /api/tasks/{id}     # Retrieve specific task
PUT    /api/tasks/{id}     # Update specific task
DELETE /api/tasks/{id}     # Delete specific task
PATCH  /api/tasks/{id}/complete  # Toggle task completion status
```

### Request/Response Examples:

**Get all tasks:**
- Request: `GET /api/tasks` with `Authorization: Bearer <token>`
- Response: `200 OK` with array of user's tasks

**Create task:**
- Request: `POST /api/tasks` with `Authorization: Bearer <token>` and `{ "title": "Task title", "description": "Description" }`
- Response: `201 Created` with created task object

## Error Handling and Security Boundaries

### Error Responses:
- `401 Unauthorized`: Invalid or missing JWT
- `403 Forbidden`: User attempting to access another user's data
- `404 Not Found`: Requested resource doesn't exist
- `422 Unprocessable Entity`: Invalid request data
- `500 Internal Server Error`: Unexpected server errors

### Security Measures:
- All API endpoints require JWT authentication
- Database queries always filtered by user ID from JWT
- Input validation on all endpoints
- SQL injection prevention through SQLModel/SQLAlchemy
- Rate limiting considerations (implementation TBD)
- JWT expiration and refresh mechanisms
- Secure secret management for JWT signing