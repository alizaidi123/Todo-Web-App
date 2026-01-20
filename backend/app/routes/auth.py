from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import timedelta
from typing import Optional
import os
from pydantic import BaseModel

from app.user_models import User, UserCreate, Token, UserResponse
from database.connection import get_session
from auth.jwt_handler import create_access_token
from passlib.context import CryptContext

router = APIRouter(tags=["auth"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/auth/signup", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user with email already exists
    existing_user_by_email = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Check if user with username already exists
    existing_user_by_username = session.exec(
        select(User).where(User.username == user.username)
    ).first()

    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists"
        )

    # Create new user
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.post("/auth/login", response_model=Token)
def login_user(login_request: LoginRequest, session: Session = Depends(get_session)):
    """Login user and return access token. Username can be email or username."""
    # Find user by either email or username
    user = session.exec(
        select(User).where((User.email == login_request.username) | (User.username == login_request.username))
    ).first()

    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with 7-day expiry
    access_token_expires = timedelta(days=7)  # 7 days expiry
    access_token = create_access_token(
        data={"sub": str(user.id), "user_id": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}