"""
Session Token Creation Endpoint

This module provides a minimal endpoint for creating ChatKit session tokens
without changing existing auth mechanisms.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uuid
import time
from auth.jwt_handler import get_current_user, TokenData
from ..user_models import User


router = APIRouter(prefix="/session", tags=["session"])


class SessionTokenResponse(BaseModel):
    session_token: str
    user_id: int
    expires_at: int


@router.post("/token", response_model=SessionTokenResponse)
async def create_session_token(current_user: User = Depends(get_current_user)):
    """
    Create a session token for ChatKit integration.
    This is a minimal implementation that doesn't interfere with existing auth.
    """
    # Generate a unique session token
    session_token = str(uuid.uuid4())

    # Set expiration time (e.g., 1 hour from now)
    expires_at = int(time.time() + 3600)  # 1 hour

    return SessionTokenResponse(
        session_token=session_token,
        user_id=current_user.id,
        expires_at=expires_at
    )


@router.get("/health")
async def session_health():
    """Health check for the session endpoint."""
    return {"status": "healthy", "message": "Session service is running"}