# Tasks: Fix Alembic Migration for Priority Column Conversion

## Feature Overview
Fix the Alembic migration that fails when converting priority column from INTEGER to TEXT on PostgreSQL/Neon databases. The current migration tries to update values before changing the type, causing DatatypeMismatch error.

## Dependencies
- Phase 1: Existing migration files exist
- Phase 2: Database schema is accessible

## Implementation Strategy
1. Update the migration to use a single ALTER statement with USING clause for atomic type conversion
2. Ensure the migration works correctly on PostgreSQL/Neon databases
3. Maintain data integrity during the conversion

---

## Phase 1: Setup Tasks

- [ ] T001 Prepare environment for migration fix

## Phase 2: Foundation Tasks

- [ ] T002 Analyze current broken migration behavior

## Phase 3: [US1] Fix Migration for PostgreSQL Compatibility

### Story Goal
Convert the current migration to use PostgreSQL-compatible ALTER COLUMN TYPE with USING clause to safely convert INTEGER to TEXT while mapping values.

### Independent Test Criteria
- Migration runs successfully on PostgreSQL/Neon without DatatypeMismatch error
- Values are correctly mapped: 1→'low', 2→'medium', 3→'high'
- Downgrade works correctly: 'low'→1, 'medium'→2, 'high'→3

### Implementation Tasks

- [X] T003 [US1] Update migration file to use USING clause for atomic conversion
- [X] T004 [US1] Test migration works with PostgreSQL-compatible syntax
- [X] T005 [US1] Verify downgrade functionality works correctly
- [X] T006 [US1] Validate data integrity after migration
- [X] T007 [US1] Document the fix for future reference

## Phase 4: Polish & Cross-Cutting Concerns

- [ ] T008 Update any related documentation about the migration fix
- [ ] T009 Run integration tests to ensure functionality remains intact

---

## Dependencies Section
- T003 must complete before T004, T005, T006
- T004, T005, T006 can run in parallel after T003

## Parallel Execution Examples
- T004, T005, T006 can be tested in parallel after migration fix