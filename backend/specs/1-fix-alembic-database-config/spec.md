# Feature Specification: Fix Alembic Database Configuration and Task Priority Field

## Overview
Fix Alembic configuration to read DATABASE_URL from environment variables and ensure Task model has proper priority field configuration for Phase 3 AI agent/tooling requirements.

## Problem Statement
- Alembic uses hardcoded localhost:5432 and fails when the application uses Neon via DATABASE_URL in .env
- Running `python -m alembic revision --autogenerate` fails because Alembic isn't reading DATABASE_URL from environment
- Phase 3 requires Task to have a `priority` attribute but the current Task model has it as optional, causing runtime errors in the AI agent/tooling

## User Scenarios & Testing

### Primary Scenario
1. Developer runs `alembic revision --autogenerate -m "add priority to task"`
2. Alembic successfully connects to the database using DATABASE_URL from environment
3. Migration is generated correctly reflecting the Task model changes
4. Migration is applied successfully with `alembic upgrade head`
5. Application continues to work with Task priority field properly configured

### Testing Scenarios
- Verify Alembic can connect to database using environment variables
- Verify Task model accepts priority field during CRUD operations
- Verify existing data is not affected by the migration
- Verify AI agent/tooling can work with Task priority field

## Functional Requirements

### FR1: Alembic Environment Configuration
- Alembic must read DATABASE_URL from environment variables instead of hardcoded values
- If DATABASE_URL is not set in environment, Alembic must fail with a clear error message
- Alembic must work in both online and offline modes appropriately

### FR2: Task Model Priority Field
- Task model must have a priority field of type integer
- Priority field must have a default value (not optional/nullable initially)
- Priority field must be indexed for performance
- Existing Task records must handle the priority field gracefully

### FR3: Migration Generation and Execution
- Alembic autogenerate must successfully detect model changes
- Migration files must be properly generated and stored in versions/
- Migration execution must work without errors
- Database schema must match the SQLModel definitions

## Success Criteria
- Alembic revision autogenerate runs successfully using environment DATABASE_URL
- Task model has priority field with integer type and default value
- Migration can be applied successfully to the database
- No runtime errors occur when AI agent/tooling accesses Task priority field
- Existing functionality remains unaffected

## Key Entities
- **Task**: Enhanced with priority field (integer with default)
- **Alembic Configuration**: Updated to read DATABASE_URL from environment
- **Database Connection**: Uses environment variables instead of hardcoded values

## Constraints
- Do NOT edit task routes
- Do NOT edit jwt_handler
- Only modify DB layer code: SQLModel models and Alembic migrations and Alembic env configuration
- Use SQLModel-friendly types
- Maintain backward compatibility for existing data

## Assumptions
- DATABASE_URL format follows standard PostgreSQL URL format
- Environment variables are properly loaded before running Alembic commands
- Existing Task records will be handled appropriately during migration
- Application code is already designed to work with the priority field conceptually

## Dependencies
- SQLAlchemy and Alembic libraries
- Python-dotenv for environment variable loading
- SQLModel for model definitions
- Neon PostgreSQL database access