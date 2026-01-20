from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.models import Task, TaskCreate, TaskUpdate, TaskResponse
from database.connection import get_session
from auth.jwt_handler import get_current_user, TokenData

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve all tasks for the authenticated user
    """
    statement = select(Task).where(Task.user_id == current_user.user_id)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Create a new task for the authenticated user
    """
    db_task = Task(**task.model_dump())
    db_task.user_id = current_user.user_id  # Assign the authenticated user's ID

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve a specific task by ID for the authenticated user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update a specific task by ID for the authenticated user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )

    # Update task fields
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    # Update the timestamp
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Delete a specific task by ID for the authenticated user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )

    session.delete(db_task)
    session.commit()
    # For HTTP 204, no response body should be returned


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    task_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Toggle the completion status of a specific task
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )

    # Toggle the completion status
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task