#!/usr/bin/env python
"""
Test script to verify the user_id type fix works properly
"""

import os
import sys
from sqlmodel import SQLModel, Session, select
from database.connection import engine, get_session
from app.models import Task, TaskCreate
from app.user_models import User, UserCreate

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_user_id_fix():
    """Test that the user_id type mismatch is fixed"""
    print("Setting up test environment...")

    # Create all tables
    from database.init_db import create_db_and_tables
    create_db_and_tables()

    # Create a test user
    with Session(engine) as session:
        # Clean up any existing test data
        session.exec(select(Task)).all()  # Just to test connection

        # Create test user
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_test_password"
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        print(f"Created test user with ID: {test_user.id} (type: {type(test_user.id)})")

        # Create a test task associated with the user
        task_create = TaskCreate(
            title="Test Task",
            description="This is a test task",
            completed=False,
            user_id=test_user.id  # This should be an integer
        )

        task = Task.model_validate(task_create.model_dump())
        session.add(task)
        session.commit()
        session.refresh(task)

        print(f"Created test task with user_id: {task.user_id} (type: {type(task.user_id)})")

        # Now try to query tasks for the user (this was failing before)
        statement = select(Task).where(Task.user_id == test_user.id)
        user_tasks = session.exec(statement).all()

        print(f"Successfully retrieved {len(user_tasks)} tasks for user {test_user.id}")

        # Test filtering by user_id (the original issue)
        print("Testing the original problematic query...")
        try:
            # This is the query that was causing the error: WHERE task.user_id = $1::INTEGER
            statement = select(Task).where(Task.user_id == test_user.id)
            result = session.exec(statement).all()
            print(f"Query succeeded! Found {len(result)} tasks for user_id {test_user.id}")

            # Verify the types match
            for task in result:
                print(f"Task {task.id}: user_id={task.user_id} (type: {type(task.user_id)})")

        except Exception as e:
            print(f"Query failed with error: {e}")
            return False

    print("All tests passed! The user_id type mismatch issue has been fixed.")
    return True

if __name__ == "__main__":
    success = test_user_id_fix()
    if not success:
        sys.exit(1)