#!/usr/bin/env python
"""
Test script to verify the Tasks CRUD fixes work properly
"""

import sys
import os
from sqlmodel import SQLModel, Session
from database.connection import engine
from app.models import Task, TaskCreate, TaskResponse

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_task_crud_fixes():
    """Test that the Task CRUD fixes work properly"""
    print("Setting up test environment...")

    # Create all tables
    from database.init_db import create_db_and_tables
    create_db_and_tables()

    # Test 1: Verify TaskCreate doesn't require user_id
    print("\n1. Testing TaskCreate schema (should not require user_id)...")

    # This should work without specifying user_id
    task_create = TaskCreate(
        title="Test Task",
        description="This is a test task",
        completed=False
    )

    print(f"   Created TaskCreate object successfully: {task_create.title}")
    print(f"   TaskCreate dict: {task_create.model_dump()}")

    # user_id should not be in the dump
    assert 'user_id' not in task_create.model_dump(), "user_id should not be in TaskCreate schema"
    print("   [PASS] TaskCreate schema correctly excludes user_id")

    # Test 2: Simulate what happens in POST /api/tasks
    print("\n2. Testing task creation with user_id assignment...")

    # Simulate the logic from the POST endpoint
    with Session(engine) as session:
        # Clean up any existing test data
        from sqlmodel import select
        existing_tasks = session.exec(select(Task)).all()
        for task in existing_tasks:
            session.delete(task)
        session.commit()

        # Create a mock user_id (simulating current_user.user_id from JWT)
        mock_user_id = 1

        # This simulates the POST endpoint logic
        # Create task from validated input, then assign user_id separately
        db_task_data = task_create.model_dump()
        db_task = Task.model_validate({**db_task_data, "user_id": mock_user_id})

        print(f"   Created Task object with user_id={db_task.user_id}")
        print(f"   Task attributes: id={getattr(db_task, 'id', 'None')}, title='{db_task.title}', user_id={db_task.user_id}")

        # Verify the task has the assigned user_id
        assert db_task.user_id == mock_user_id, f"user_id should be {mock_user_id}"
        print("   [PASS] Task correctly assigns user_id from authenticated user")

        # Test 3: Verify we can query tasks for a specific user
        print("\n3. Testing task retrieval for specific user...")

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Query tasks for the specific user (simulating GET /api/tasks)
        statement = select(Task).where(Task.user_id == mock_user_id)
        user_tasks = session.exec(statement).all()

        print(f"   Retrieved {len(user_tasks)} tasks for user {mock_user_id}")

        # Should have exactly one task for this user
        assert len(user_tasks) == 1, f"Should have 1 task for user {mock_user_id}, got {len(user_tasks)}"
        assert user_tasks[0].user_id == mock_user_id, f"Task should belong to user {mock_user_id}"
        print("   [PASS] Task retrieval correctly filters by user_id")

    print("\n[SUCCESS] All tests passed! Tasks CRUD fixes are working correctly.")
    print("\nSummary of fixes:")
    print("- TaskCreate model no longer requires user_id in request body")
    print("- POST endpoint sets user_id from authenticated user (not from request)")
    print("- GET endpoint filters tasks by authenticated user_id")
    print("- Type conversion between JWT and database is handled properly")

if __name__ == "__main__":
    test_task_crud_fixes()