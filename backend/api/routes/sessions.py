"""
Sessions API endpoints
Handles chat session creation and retrieval
"""
from uuid import UUID
from fastapi import APIRouter, HTTPException

from ..models.schemas import (
    CreateSessionRequest,
    SessionResponse,
    SessionWithMessages
)
from ..services import session_service

router = APIRouter()


@router.post("/sessions", response_model=SessionResponse, status_code=201)
async def create_session(request: CreateSessionRequest = None):
    """
    Create a new chat session.

    Sessions are used to group related messages and maintain conversation context.
    """
    try:
        metadata = request.metadata if request else {}
        session = await session_service.create_session(metadata)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/sessions/{session_id}", response_model=SessionWithMessages)
async def get_session(session_id: UUID):
    """
    Get a session with all its messages.

    Returns the session details and all messages in chronological order.
    """
    try:
        result = await session_service.get_session_with_messages(session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Session not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve session: {str(e)}")
