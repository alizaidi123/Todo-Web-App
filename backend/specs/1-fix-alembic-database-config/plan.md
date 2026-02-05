# Implementation Plan: Fix Alembic Database Configuration and Task Priority Field

## Technical Context

- **Current State**: Alembic uses hardcoded localhost:5432 in alembic.ini, Task model has optional priority field
- **Target State**: Alembic reads DATABASE_URL from environment, Task model has required priority field with default
- **Scope**: Backend database layer changes only (models, alembic config, migrations)
- **Affected Components**:
  - `alembic/env.py` - Alembic configuration
  - `app/models.py` - Task model definition
  - Alembic migration files
- **Non-Affected Components**: Routes, JWT handler, frontend, API contracts

## Constitution Check

Based on project constitution principles:
- ✅ Minimal change: Only modify DB layer as constrained
- ✅ Safe migrations: Proper default values and backward compatibility
- ✅ Environment-first: Use environment variables over hardcoded values
- ✅ Type safety: Use SQLModel-friendly types
- ✅ Testability: Include verification steps

## Gates

- ✅ Scope: Changes limited to DB layer (models, alembic config)
- ✅ Safety: Migration includes proper defaults and indexes
- ✅ Compliance: Respects all stated constraints
- ✅ Dependencies: Uses existing libraries (SQLAlchemy, Alembic, SQLModel)

## Phase 0: Research

### 0.1 Current Alembic Configuration Analysis
- **Status**: RESOLVED
- **Details**: alembic.ini has hardcoded `sqlalchemy.url = postgresql://username:password@localhost/dbname`
- **Solution**: Update alembic/env.py to read DATABASE_URL from environment variables

### 0.2 Current Task Model Analysis
- **Status**: RESOLVED
- **Details**: Task model has `priority: int = Field(default=1, index=True)` (already updated)
- **Solution**: Verify field is properly configured for AI agent/tooling

### 0.3 Alembic Migration Process
- **Status**: RESOLVED
- **Process**: Use `alembic revision --autogenerate` to detect model changes
- **Verification**: Use `alembic current` and `alembic head` to verify migration state

## Phase 1: Design & Contracts

### 1.1 Data Model Changes

#### Task Entity Enhancement
- **Entity**: Task
- **Field**: priority
- **Type**: int (non-nullable)
- **Default**: 1
- **Index**: True (for performance)
- **Validation**: Integer range validation if needed

### 1.2 Implementation Steps

#### Step 1: Update Alembic Environment Configuration
- **File**: `alembic/env.py`
- **Change**: Add code to read DATABASE_URL from environment variables
- **Error Handling**: Fail with clear message if DATABASE_URL not set

#### Step 2: Verify Task Model Configuration
- **File**: `app/models.py`
- **Check**: Ensure priority field is `int = Field(default=1, index=True)`
- **Update**: Ensure TaskUpdate includes priority field

#### Step 3: Generate Migration
- **Command**: `alembic revision --autogenerate -m "add priority field to task table"`
- **Output**: New migration file in `alembic/versions/`

#### Step 4: Apply Migration
- **Command**: `alembic upgrade head`
- **Verification**: Check database schema

#### Step 5: Verification
- **Command**: `alembic current` (should match head)
- **Query**: Direct DB inspection of task table structure
- **Test**: Verify AI agent can access priority field

### 1.3 Risk Mitigation

#### Migration Safety
- Use proper defaults to avoid breaking existing data
- Include index for performance
- Test with real database connection

#### Environment Variable Safety
- Fail fast with clear error message if DATABASE_URL missing
- Log which database URL is being used

## Phase 2: Implementation Tasks

### Task 1: Update Alembic Environment
- **Objective**: Make alembic/env.py read DATABASE_URL from environment
- **Steps**:
  1. Import os module
  2. Read DATABASE_URL from environment
  3. Set as sqlalchemy.url in config
  4. Add error handling for missing variable
- **Verification**: Alembic can connect using environment URL

### Task 2: Verify Task Model
- **Objective**: Ensure Task model has proper priority field
- **Steps**:
  1. Check Task model priority field definition
  2. Verify TaskUpdate includes priority field
  3. Confirm default value is appropriate for AI agent
- **Verification**: Model matches requirements

### Task 3: Generate and Apply Migration
- **Objective**: Create and apply the database migration
- **Steps**:
  1. Run alembic revision --autogenerate
  2. Review generated migration
  3. Apply with alembic upgrade head
- **Verification**: Database schema updated correctly

### Task 4: Verification
- **Objective**: Confirm all changes work correctly
- **Steps**:
  1. Run `alembic current` to verify migration state
  2. Query database directly to verify priority column
  3. Test AI agent access to priority field
- **Verification**: All checks pass successfully

## Quickstart for Implementation

1. **Environment Setup**:
   ```bash
   export $(grep -v '^#' .env | xargs)
   ```

2. **Update Alembic Config**:
   ```bash
   # Modify alembic/env.py to read DATABASE_URL from environment
   ```

3. **Generate Migration**:
   ```bash
   python -m alembic revision --autogenerate -m "add priority field to task table"
   ```

4. **Apply Migration**:
   ```bash
   python -m alembic upgrade head
   ```

5. **Verify**:
   ```bash
   python -m alembic current  # Should match head revision
   ```

## Success Criteria

- [ ] Alembic reads DATABASE_URL from environment variables
- [ ] Task model has priority field with integer type and default value
- [ ] Migration generated and applied successfully
- [ ] `alembic current` shows head revision
- [ ] Database contains priority column in task table
- [ ] AI agent/tooling can access Task priority field
- [ ] No breaking changes to existing functionality