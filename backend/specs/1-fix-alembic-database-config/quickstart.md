# Quickstart Guide: Alembic and Task Priority Implementation

## Overview
This guide provides step-by-step instructions to implement the Alembic database configuration fix and Task priority field enhancement.

## Prerequisites
- Python environment with dependencies installed
- Access to .env file with DATABASE_URL configured
- Database access permissions

## Step-by-Step Implementation

### Step 1: Prepare Environment
```bash
# Navigate to backend directory
cd D:\todo-app\backend

# Load environment variables
export $(grep -v '^#' .env | xargs)
```

### Step 2: Update Alembic Configuration
Edit `alembic/env.py` to read DATABASE_URL from environment:

```python
# Add these lines after the imports
import os

# Load DATABASE_URL from environment variables
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL environment variable is required but not set")

# Override the sqlalchemy.url in config with the environment variable
config.set_main_option('sqlalchemy.url', database_url)
```

### Step 3: Verify Task Model Configuration
Ensure `app/models.py` has the correct priority field:

```python
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(description="Foreign key to user", foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    priority: int = Field(default=1, index=True)  # Changed from Optional[int]
```

Also update TaskUpdate:

```python
class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = Field(default=None)
    priority: Optional[int] = Field(default=None)  # Allow priority updates
```

### Step 4: Generate Migration
```bash
python -m alembic revision --autogenerate -m "add priority field to task table"
```

### Step 5: Apply Migration
```bash
python -m alembic upgrade head
```

### Step 6: Verify Implementation
```bash
# Check current migration state
python -m alembic current

# Verify database structure (should show head revision)
python -m alembic heads

# Run verification script
python verify_migration_fix.py
```

## Expected Results
- Alembic now reads DATABASE_URL from environment variables
- Task table has priority column with default value of 1
- All existing and new tasks have priority field populated
- AI agent can access Task priority field reliably

## Troubleshooting

### If DATABASE_URL is not found:
- Verify .env file exists and contains DATABASE_URL
- Ensure environment variables are loaded before running Alembic commands

### If migration fails:
- Check that database is accessible
- Verify existing migration state with `alembic current`
- If needed, reset migration state with `alembic stamp head`

### If priority field is not accessible:
- Verify the migration was applied successfully
- Check that the model definition matches the database schema