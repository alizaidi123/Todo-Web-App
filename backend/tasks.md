# Tasks: Fix Priority Column Type Issue

## Feature Overview
Fix the priority column type mismatch where the database expects integers but the system sends string values ("low", "medium", "high").

## Dependencies
- Phase 1: Database setup completed
- Phase 2: Basic task CRUD operations functional

## Implementation Strategy
1. Update Task model to accept string priorities
2. Create safe migration to convert integer values to string equivalents
3. Update all related schemas and tools to handle string priorities
4. Maintain backward compatibility with existing functionality

---

## Phase 1: Setup Tasks

- [ ] T001 Create project structure per implementation plan

## Phase 2: Foundation Tasks

- [ ] T002 Ensure existing task functionality remains intact

## Phase 3: [US1] Priority Column Type Fix

### Story Goal
Convert the Task.priority column from INTEGER to TEXT type to accept string values ("low", "medium", "high") while maintaining data integrity.

### Independent Test Criteria
- Adding a task via AI with priority "medium" succeeds (no DB error)
- Existing tasks with integer priorities are properly mapped to string equivalents
- All priority operations work correctly with string values

### Implementation Tasks

- [X] T003 [P] [US1] Update Task model in app/models.py to change priority from int to str with allowed values
- [X] T004 [P] [US1] Update TaskCreate, TaskUpdate, and TaskResponse schemas to handle string priority
- [X] T005 [P] [US1] Update task routes in app/routes/tasks.py to work with string priorities
- [X] T006 [P] [US1] Create Alembic migration to safely convert priority column from INTEGER to TEXT
- [X] T007 [P] [US1] Update task tools in app/tools/task_tools.py to validate string priorities
- [X] T008 [P] [US1] Update MCP tools in app/mcp/tools.py to work with string priorities
- [X] T009 [US1] Test priority conversion: 1 -> "low", 2 -> "medium", 3 -> "high"
- [X] T010 [US1] Test default priority is "medium" when not specified
- [X] T011 [US1] Test all allowed priority values ("low", "medium", "high") work correctly
- [X] T012 [US1] Verify existing task API still works after priority type change
- [X] T013 [US1] Test AI chatbot can add tasks with string priorities successfully

## Phase 4: Polish & Cross-Cutting Concerns

- [X] T014 Update documentation to reflect priority type changes
- [X] T015 Add validation to prevent invalid priority values
- [X] T016 Run integration tests to ensure all functionality works correctly

---

## Dependencies Section
- T003 must complete before T004, T005, T006, T007, T008
- T006 (migration) must run before T010, T011, T012, T013
- T009, T010, T011, T012, T013 can run in parallel after migration

## Parallel Execution Examples
- T003, T004, T005, T006, T007, T008 can be worked on in parallel by different developers
- T009-T013 can be tested in parallel after migration is applied