"""
MCP (Model Context Protocol) Tools for Todo Operations.

This module exposes the 5 required todo tools that interact with the existing
Phase II service layer without modifying the tasks routes.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, field_validator
from sqlmodel import Session, select
from database.connection import engine
from ..models import Task, PriorityEnum


class AddTaskInput(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    user_id: int  # Required to associate with user

    @field_validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError(f'Priority must be one of: low, medium, high. Got: {v}')
        return v


def add_task(input_data: AddTaskInput) -> Dict[str, Any]:
    """
    Add a new task to the database using existing service layer logic.
    """
    with Session(engine) as session:
        # Create task using the same logic as the existing Phase II service
        task = Task(
            title=input_data.title,
            description=input_data.description,
            priority=input_data.priority,
            completed=False,
            user_id=input_data.user_id  # Associate with user
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task_id": task.id,
            "message": f"Task '{task.title}' added successfully",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed,
                "user_id": task.user_id
            }
        }


class ListTasksInput(BaseModel):
    user_id: int
    completed: Optional[bool] = None
    priority: Optional[str] = None

    @field_validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError(f'Priority must be one of: low, medium, high. Got: {v}')
        return v


def list_tasks(input_data: ListTasksInput) -> Dict[str, Any]:
    """
    List tasks for a specific user with optional filters, using existing service logic.
    """
    with Session(engine) as session:
        # Query tasks for the specific user
        query = select(Task).where(Task.user_id == input_data.user_id)

        if input_data.completed is not None:
            query = query.where(Task.completed == input_data.completed)
        if input_data.priority is not None:
            query = query.where(Task.priority == input_data.priority)

        tasks = session.exec(query).all()

        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed,
                "user_id": task.user_id
            })

        return {
            "success": True,
            "count": len(task_list),
            "tasks": task_list
        }


class UpdateTaskInput(BaseModel):
    task_id: int
    user_id: int  # Verify ownership
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError(f'Priority must be one of: low, medium, high. Got: {v}')
        return v


def update_task(input_data: UpdateTaskInput) -> Dict[str, Any]:
    """
    Update an existing task using existing service layer logic.
    """
    with Session(engine) as session:
        # First verify the task belongs to the user
        task = session.get(Task, input_data.task_id)
        if not task:
            return {
                "success": False,
                "error": f"Task with id {input_data.task_id} not found"
            }

        if task.user_id != input_data.user_id:
            return {
                "success": False,
                "error": "Not authorized to update this task"
            }

        # Update fields if provided (similar to existing service logic)
        if input_data.title is not None:
            task.title = input_data.title
        if input_data.description is not None:
            task.description = input_data.description
        if input_data.priority is not None:
            task.priority = input_data.priority
        if input_data.completed is not None:
            task.completed = input_data.completed

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "message": f"Task {task.id} updated successfully",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed,
                "user_id": task.user_id
            }
        }


class DeleteTaskInput(BaseModel):
    task_id: int
    user_id: int  # Verify ownership


def delete_task(input_data: DeleteTaskInput) -> Dict[str, Any]:
    """
    Delete a task using existing service layer logic.
    """
    with Session(engine) as session:
        # First verify the task belongs to the user
        task = session.get(Task, input_data.task_id)
        if not task:
            return {
                "success": False,
                "error": f"Task with id {input_data.task_id} not found"
            }

        if task.user_id != input_data.user_id:
            return {
                "success": False,
                "error": "Not authorized to delete this task"
            }

        session.delete(task)
        session.commit()

        return {
            "success": True,
            "message": f"Task {input_data.task_id} deleted successfully"
        }


class CompleteTaskInput(BaseModel):
    task_id: int
    user_id: int  # Verify ownership
    completed: bool = True


def complete_task(input_data: CompleteTaskInput) -> Dict[str, Any]:
    """
    Mark a task as complete/incomplete using existing service layer logic.
    """
    with Session(engine) as session:
        # First verify the task belongs to the user
        task = session.get(Task, input_data.task_id)
        if not task:
            return {
                "success": False,
                "error": f"Task with id {input_data.task_id} not found"
            }

        if task.user_id != input_data.user_id:
            return {
                "success": False,
                "error": "Not authorized to modify this task"
            }

        task.completed = input_data.completed
        session.add(task)
        session.commit()
        session.refresh(task)

        status = "completed" if input_data.completed else "marked incomplete"
        return {
            "success": True,
            "message": f"Task {task.id} {status} successfully",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed,
                "user_id": task.user_id
            }
        }


# MCP Tools Registry
MCP_TOOLS = {
    "add_task": {
        "function": add_task,
        "description": "Add a new task with title, description, and priority",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title of the task"},
                "description": {"type": "string", "description": "Description of the task"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"},
                "user_id": {"type": "integer", "description": "ID of the user who owns the task"}
            },
            "required": ["title", "user_id"]
        }
    },
    "list_tasks": {
        "function": list_tasks,
        "description": "List tasks for a user with optional filters",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer", "description": "ID of the user whose tasks to list"},
                "completed": {"type": "boolean", "description": "Filter by completion status"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Filter by priority"}
            },
            "required": ["user_id"]
        }
    },
    "update_task": {
        "function": update_task,
        "description": "Update an existing task",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "ID of the task to update"},
                "user_id": {"type": "integer", "description": "ID of the user who owns the task"},
                "title": {"type": "string", "description": "New title"},
                "description": {"type": "string", "description": "New description"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "New priority"},
                "completed": {"type": "boolean", "description": "New completion status"}
            },
            "required": ["task_id", "user_id"]
        }
    },
    "delete_task": {
        "function": delete_task,
        "description": "Delete a task by its ID",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "ID of the task to delete"},
                "user_id": {"type": "integer", "description": "ID of the user who owns the task"}
            },
            "required": ["task_id", "user_id"]
        }
    },
    "complete_task": {
        "function": complete_task,
        "description": "Mark a task as complete or incomplete",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "ID of the task to update"},
                "user_id": {"type": "integer", "description": "ID of the user who owns the task"},
                "completed": {"type": "boolean", "default": True, "description": "Whether to mark as complete (true) or incomplete (false)"}
            },
            "required": ["task_id", "user_id"]
        }
    }
}