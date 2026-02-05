from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(description="Foreign key to user", foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    priority: str = Field(default="medium", index=True, max_length=10)


class TaskCreate(TaskBase):
    # Don't include user_id in TaskCreate - it will be set from authenticated user
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = Field(default=None)
    priority: Optional[str] = Field(default=None, max_length=10)


class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    priority: str


# Conversation and Message models for Phase III AI Chatbot
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .user_models import User  # Import User if needed for relationships


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class ConversationBase(SQLModel):
    user_id: int = Field(description="Foreign key to user", index=True)
    title: str = Field(default="New Conversation", max_length=200)


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    pass


class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime


class MessageBase(SQLModel):
    conversation_id: int = Field(description="Foreign key to conversation", foreign_key="conversation.id", index=True)
    role: MessageRole = Field(description="Role of the message sender (user/assistant/system)")
    content: str = Field(description="Content of the message")
    tool_calls: Optional[str] = Field(default=None, description="Tool calls made by the assistant (JSON string)")
    tool_responses: Optional[str] = Field(default=None, description="Responses from tools (JSON string)")


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    timestamp: datetime