"""
Chat endpoint skeleton (no AI).

This module implements the basic chat endpoint that stores user messages
and returns placeholder assistant responses.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlmodel import Session, select
from auth.jwt_handler import get_current_user
from ..user_models import User
from ..models import Conversation, Message
from database.connection import engine
from ..services.agent_runner import run_agent_for_user
import json

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    success: bool
    conversation_id: int
    messages: List[Dict[str, Any]]


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: int,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Chat endpoint that loads conversation history, runs agent, executes tool calls,
    stores user and assistant messages with tool trace, and returns response.
    """

    # jwt_handler returns TokenData (usually has `user_id`), not a full User model
    token_user_id = getattr(current_user, "user_id", None)

    if token_user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    if token_user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this user's chat"
        )

    with Session(engine) as session:
        # Find or create a conversation for this user
        conversation = None

        if chat_request.conversation_id:
            # Try to find the specific conversation
            conversation = session.get(Conversation, chat_request.conversation_id)
            # Verify it belongs to the user
            if conversation and conversation.user_id != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to access this conversation",
                )

        if not conversation:
            # Find most recent conversation for this user, or create new one
            conversation_query = (
                select(Conversation)
                .where(Conversation.user_id == user_id)
                .order_by(Conversation.updated_at.desc())
                .limit(1)
            )
            conversation = session.exec(conversation_query).first()

            if not conversation:
                # TokenData usually won't have username, so don't depend on it
                conversation = Conversation(
                    user_id=user_id,
                    title=f"Conversation with user {user_id}",
                )
                session.add(conversation)
                session.commit()
                session.refresh(conversation)

        # Store user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=chat_request.message,
        )
        session.add(user_message)
        session.commit()
        session.refresh(user_message)

        # Load conversation history for the agent
        history_query = (
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.timestamp.asc())
        )
        history_messages = session.exec(history_query).all()

        # Convert history to the format expected by the agent
        chat_history = []
        for msg in history_messages[:-1]:  # Exclude the current user message
            chat_history.append({"role": msg.role, "content": msg.content})

        # Run the agent to process the user input
        agent_result = run_agent_for_user(
            user_input=chat_request.message,
            user_id=user_id,
            chat_history=chat_history,
        )

        # Extract the response and tool information
        assistant_response = agent_result.get("response", "I processed your request.")
        tool_calls = agent_result.get("tool_calls", [])
        tool_results = agent_result.get("tool_results", [])

        # Store assistant response with tool trace
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_response,
            tool_calls=json.dumps(tool_calls) if tool_calls else None,
            tool_responses=json.dumps(tool_results) if tool_results else None,
        )
        session.add(assistant_message)
        session.commit()
        session.refresh(assistant_message)

        # Get all messages for this conversation to return
        messages_query = (
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.timestamp.asc())
        )
        messages = session.exec(messages_query).all()

        response_messages = []
        for msg in messages:
            response_messages.append(
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "tool_calls": json.loads(msg.tool_calls) if msg.tool_calls else [],
                    "tool_responses": json.loads(msg.tool_responses)
                    if msg.tool_responses
                    else [],
                }
            )

        return ChatResponse(
            response=assistant_response,
            success=agent_result.get("success", True),
            conversation_id=conversation.id,
            messages=response_messages,
        )


@router.get("/health")
async def chat_health():
    """Health check for the chat endpoint."""
    return {"status": "healthy", "message": "Chat service is running"}
