# Tasks: Fix Alembic Database Configuration and Task Priority Field

## Feature Overview
Fix Alembic configuration to read DATABASE_URL from environment variables and ensure Task model has proper priority field configuration for Phase 3 AI agent/tooling requirements.

## Implementation Strategy
This feature will be implemented in phases, with foundational tasks first, followed by user story implementations. The approach ensures each user story is independently testable while maintaining proper dependencies.

## Dependencies
- User Story 1 (Alembic Configuration) must complete before User Story 2 (Task Model) to ensure proper migration generation
- Both foundational changes needed before migration can be generated and applied

## Parallel Execution Opportunities
- Within User Story 1: Environment configuration and model metadata setup can run in parallel
- Within User Story 2: Model changes and update model changes can run in parallel

## Phase 1: Setup
No specific setup tasks needed beyond existing project structure.

## Phase 2: Foundational Tasks
Tasks that must complete before user stories can begin.

- [X] T001 [P] Update alembic/env.py to use os.getenv("DATABASE_URL") for database connection
- [X] T002 [P] Configure target_metadata in alembic/env.py to use SQLModel.metadata

## Phase 3: [US1] Alembic Environment Configuration
Configure Alembic to read DATABASE_URL from environment variables instead of hardcoded values.

**Goal**: Alembic successfully connects to database using environment variables and follows proper error handling.

**Independent Test Criteria**:
- Running `alembic current` with DATABASE_URL in environment succeeds
- Running `alembic current` without DATABASE_URL throws clear error

- [X] T003 [US1] Add error handling for missing DATABASE_URL in alembic/env.py
- [X] T004 [US1] Verify alembic/env.py properly reads environment variables

## Phase 4: [US2] Task Model Enhancement
Enhance Task model to include priority field with proper default value and constraints.

**Goal**: Task model has priority field with integer type, default value, and proper indexing.

**Independent Test Criteria**:
- Task model definition includes priority field with int type and default value
- TaskUpdate model includes priority field for updates

- [X] T005 [US2] Locate Task SQLModel definition in app/models.py and add priority: int with default=1 and index=True
- [X] T006 [US2] Update TaskUpdate model to include priority field as Optional[int]

## Phase 5: [US3] Migration Generation and Application
Generate and apply database migration to add priority column to existing Task table.

**Goal**: Database schema updated with priority column matching model definition.

**Independent Test Criteria**:
- Alembic migration generated successfully reflecting model changes
- Migration applied successfully to database
- Database table contains priority column with proper constraints

- [X] T007 [US3] Run alembic autogenerate to create a revision adding the priority column
- [X] T008 [US3] Review and clean generated migration file to only include priority field changes
- [X] T009 [US3] Run alembic upgrade head to apply the migration
- [X] T010 [US3] Verify priority column exists in database with correct properties

## Phase 6: [US4] Verification and Validation
Complete verification of all changes and ensure system integrity.

**Goal**: All changes validated and system working properly.

**Independent Test Criteria**:
- All verification steps pass successfully
- Commands work as expected

- [X] T011 [US4] Provide verification steps to confirm column exists in database
- [X] T012 [US4] Create quick command to confirm column exists and has correct properties
- [X] T013 [US4] Run comprehensive verification script to test all functionality

## Phase 7: Polish & Cross-Cutting Concerns
Final validation and documentation.

- [X] T014 Update any related documentation to reflect the new priority field
- [X] T015 Clean up temporary files or test data created during implementation