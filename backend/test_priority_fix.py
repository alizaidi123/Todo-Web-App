#!/usr/bin/env python3
"""
Test script to verify priority column fix implementation.
This tests the model definitions and validation without requiring a database.
"""

from app.models import Task, TaskUpdate, PriorityEnum
from app.tools.task_tools import AddTaskInput, ListTasksInput, UpdateTaskInput
from app.mcp.tools import AddTaskInput as MCPAddTaskInput, ListTasksInput as MCPListTasksInput, UpdateTaskInput as MCPUpdateTaskInput

def test_models():
    """Test that models accept string priorities"""
    print("Testing Task model...")

    # Test creating a Task with string priority
    task = Task(title="Test task", priority="medium")
    assert task.priority == "medium"
    print("[OK] Task model accepts string priority")

    # Test default priority
    task_default = Task(title="Default task")
    assert task_default.priority == "medium"
    print("[OK] Task model has correct default priority")

    # Test TaskUpdate with string priority
    task_update = TaskUpdate(priority="high")
    assert task_update.priority == "high"
    print("[OK] TaskUpdate accepts string priority")


def test_tool_validations():
    """Test that tool inputs validate priority values"""
    print("\nTesting tool input validations...")

    # Test valid priorities
    valid_priorities = ["low", "medium", "high"]
    for priority in valid_priorities:
        # Test AddTaskInput
        add_input = AddTaskInput(title="Test", priority=priority)
        assert add_input.priority == priority
        print(f"[OK] AddTaskInput accepts '{priority}'")

        # Test ListTasksInput
        list_input = ListTasksInput(priority=priority)
        assert list_input.priority == priority
        print(f"[OK] ListTasksInput accepts '{priority}'")

        # Test UpdateTaskInput
        update_input = UpdateTaskInput(task_id=1, priority=priority)
        assert update_input.priority == priority
        print(f"[OK] UpdateTaskInput accepts '{priority}'")

        # Test MCP tools
        mcp_add_input = MCPAddTaskInput(title="Test", priority=priority, user_id=1)
        assert mcp_add_input.priority == priority
        print(f"[OK] MCP AddTaskInput accepts '{priority}'")

        mcp_list_input = MCPListTasksInput(user_id=1, priority=priority)
        assert mcp_list_input.priority == priority
        print(f"[OK] MCP ListTasksInput accepts '{priority}'")

        mcp_update_input = MCPUpdateTaskInput(task_id=1, user_id=1, priority=priority)
        assert mcp_update_input.priority == priority
        print(f"[OK] MCP UpdateTaskInput accepts '{priority}'")

    # Test invalid priority raises error
    try:
        invalid_input = AddTaskInput(title="Test", priority="invalid")
        assert False, "Should have raised validation error"
    except ValueError:
        print("[OK] AddTaskInput rejects invalid priority")

    try:
        invalid_input = UpdateTaskInput(task_id=1, priority="invalid")
        assert False, "Should have raised validation error"
    except ValueError:
        print("[OK] UpdateTaskInput rejects invalid priority")


def test_default_values():
    """Test default priority values"""
    print("\nTesting default values...")

    # Test default priority in AddTaskInput
    add_input = AddTaskInput(title="Test")
    assert add_input.priority == "medium"
    print("[OK] AddTaskInput has correct default priority")

    # Test default priority in MCP AddTaskInput
    mcp_add_input = MCPAddTaskInput(title="Test", user_id=1)
    assert mcp_add_input.priority == "medium"
    print("[OK] MCP AddTaskInput has correct default priority")


if __name__ == "__main__":
    print("Running priority column fix verification tests...\n")

    test_models()
    test_tool_validations()
    test_default_values()

    print("\n*** All tests passed! Priority column fix implementation is correct. ***")
    print("\nSummary of changes:")
    print("- Task model updated to use string priority with default 'medium'")
    print("- TaskUpdate schema updated to use string priority")
    print("- TaskResponse schema updated to include priority field")
    print("- Tool inputs validated to accept only 'low', 'medium', 'high'")
    print("- MCP tools updated with same validation")
    print("- Alembic migration created to convert INTEGER to TEXT")