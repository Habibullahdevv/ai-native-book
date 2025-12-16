"""
Chat API endpoints
Handles message sending and RAG-powered responses
"""
import logging
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..models.schemas import (
    ChatRequest,
    ChatResponse,
    MessageRole
)
from ..services import session_service, agent_service

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
async def send_message(request: Request, body: ChatRequest):
    """
    Send a chat message and receive a RAG-powered response.

    The AI will search the Physical AI & Humanoid Robotics textbook
    and respond based on the relevant content found.

    If `selected_text` is provided, the AI will focus its response
    on that specific passage.
    """
    # Validate message length
    if len(body.message) < 1:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    if len(body.message) > 10000:
        raise HTTPException(status_code=400, detail="Message too long (max 10000 characters)")

    # Validate selected_text if provided
    if body.selected_text and len(body.selected_text) > 5000:
        raise HTTPException(status_code=400, detail="Selected text too long (max 5000 characters)")

    try:
        # Verify session exists
        session = await session_service.get_session(body.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Save user message
        start_time = datetime.now(timezone.utc)
        user_message = await session_service.save_message(
            session_id=body.session_id,
            role=MessageRole.USER,
            content=body.message,
            selected_text=body.selected_text
        )

        # Run agent to generate response
        logger.info(f"Processing chat message for session {body.session_id}")
        response_text = await agent_service.run_agent(
            query=body.message,
            selected_text=body.selected_text,
            session_id=str(body.session_id)
        )

        # Calculate latency
        end_time = datetime.now(timezone.utc)
        latency_ms = int((end_time - start_time).total_seconds() * 1000)

        # Save assistant response
        assistant_message = await session_service.save_message(
            session_id=body.session_id,
            role=MessageRole.ASSISTANT,
            content=response_text,
            metadata={"latency_ms": latency_ms}
        )

        logger.info(f"Chat response generated in {latency_ms}ms for session {body.session_id}")

        return ChatResponse(
            message_id=assistant_message.id,
            response=response_text,
            metadata={
                "latency_ms": latency_ms,
                "selected_text_used": body.selected_text is not None
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=503,
            detail="I'm having trouble processing your request. Please try again."
        )


@router.post("/chat/selection", response_model=ChatResponse)
@limiter.limit("20/minute")
async def send_message_with_selection(request: Request, body: ChatRequest):
    """
    Send a chat message with selected text context.

    This is an alias for POST /chat with required selected_text.
    The AI will focus its response specifically on the selected passage.
    """
    if not body.selected_text:
        raise HTTPException(
            status_code=400,
            detail="selected_text is required for this endpoint"
        )

    # Delegate to main chat endpoint
    return await send_message(request, body)
