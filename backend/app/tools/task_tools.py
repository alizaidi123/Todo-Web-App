from typing import List, Optional
from pydantic import BaseModel, field_validator
from sqlmodel import Session, select
from ..models import Task, PriorityEnum
from database.connection import engine


class AddTaskInput(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"

    @field_validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError(f'Priority must be one of: low, medium, high. Got: {v}')
        return v


def add_task(input_data: AddTaskInput) -> dict:
    """Add a new task to the database."""
    with Session(engine) as session:
        task = Task(
            title=input_data.title,
            description=input_data.description,
            priority=input_data.priority,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"success": True, "task_id": task.id, "message": f"Task '{task.title}' added successfully"}


class ListTasksInput(BaseModel):
    completed: Optional[bool] = None
    priority: Optional[str] = None

    @field_validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError(f'Priority must be one of: low, medium, high. Got: {v}')
        return v


def list_tasks(input_data: ListTasksInput) -> dict:
    """List tasks with optional filters."""
    with Session(engine) as session:
        query = select(Task)

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
                "created_at": task.created_at.isoformat() if task.created_at else None
            })

        return {"tasks": task_list}


class UpdateTaskInput(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError(f'Priority must be one of: low, medium, high. Got: {v}')
        return v


def update_task(input_data: UpdateTaskInput) -> dict:
    """Update an existing task in the database."""
    with Session(engine) as session:
        task = session.get(Task, input_data.task_id)
        if not task:
            return {"success": False, "error": f"Task with id {input_data.task_id} not found"}

        # Update fields if provided
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

        return {"success": True, "message": f"Task {task.id} updated successfully"}


class DeleteTaskInput(BaseModel):
    task_id: int


def delete_task(input_data: DeleteTaskInput) -> dict:
    """Delete a task from the database."""
    with Session(engine) as session:
        task = session.get(Task, input_data.task_id)
        if not task:
            return {"success": False, "error": f"Task with id {input_data.task_id} not found"}

        session.delete(task)
        session.commit()

        return {"success": True, "message": f"Task {input_data.task_id} deleted successfully"}


class CompleteTaskInput(BaseModel):
    task_id: int
    completed: bool = True


def complete_task(input_data: CompleteTaskInput) -> dict:
    """Mark a task as complete or incomplete."""
    with Session(engine) as session:
        task = session.get(Task, input_data.task_id)
        if not task:
            return {"success": False, "error": f"Task with id {input_data.task_id} not found"}

        task.completed = input_data.completed
        session.add(task)
        session.commit()
        session.refresh(task)

        status = "completed" if input_data.completed else "marked incomplete"
        return {"success": True, "message": f"Task {task.id} {status} successfully"}