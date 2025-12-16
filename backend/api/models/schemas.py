"""
Pydantic schemas for the RAG Chatbot API
Based on data-model.md specification
"""
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum


class MessageRole(str, Enum):
    """Message sender role"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# Request Schemas

class CreateSessionRequest(BaseModel):
    """Request model for creating a new session"""
    metadata: dict = Field(default_factory=dict, description="Optional session metadata")


class ChatRequest(BaseModel):
    """Request model for sending a chat message"""
    session_id: UUID = Field(..., description="The session ID to add the message to")
    message: str = Field(..., min_length=1, max_length=10000, description="The user's message")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Optional selected text context")


# Response Schemas

class SessionResponse(BaseModel):
    """Response model for session data"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    metadata: dict


class MessageResponse(BaseModel):
    """Response model for message data"""
    id: UUID
    session_id: UUID
    role: MessageRole
    content: str
    selected_text: Optional[str] = None
    metadata: dict
    created_at: datetime


class SessionWithMessages(BaseModel):
    """Combined session with full message history"""
    session: SessionResponse
    messages: list[MessageResponse]


class ChatResponse(BaseModel):
    """Response model for chat completion"""
    message_id: UUID
    response: str
    metadata: dict = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    timestamp: datetime
    dependencies: dict = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str
    detail: Optional[str] = None
    retry: bool = False
