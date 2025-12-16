"""
Chat API endpoints
Handles message sending and RAG-powered responses
"""
import json
import logging
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, AsyncGenerator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
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


async def _sse_stream_generator(
    session_id: UUID,
    message: str,
    selected_text: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """
    Generate Server-Sent Events for streaming chat response.

    SSE Event Types:
    - token: Individual tokens as they're generated
    - done: Stream completed successfully with final message_id
    - error: An error occurred during streaming
    """
    full_response = ""
    start_time = datetime.now(timezone.utc)

    try:
        # Save user message first
        user_message = await session_service.save_message(
            session_id=session_id,
            role=MessageRole.USER,
            content=message,
            selected_text=selected_text
        )

        # Stream tokens from the agent
        async for token in agent_service.run_agent_streamed(
            query=message,
            selected_text=selected_text,
            session_id=str(session_id)
        ):
            full_response += token
            # Send token event
            event_data = json.dumps({"type": "token", "content": token})
            yield f"data: {event_data}\n\n"

        # Calculate latency
        end_time = datetime.now(timezone.utc)
        latency_ms = int((end_time - start_time).total_seconds() * 1000)

        # Save complete response to database
        assistant_message = await session_service.save_message(
            session_id=session_id,
            role=MessageRole.ASSISTANT,
            content=full_response,
            metadata={"latency_ms": latency_ms, "streaming": True}
        )

        # Send done event with message_id
        done_data = json.dumps({
            "type": "done",
            "message_id": str(assistant_message.id),
            "latency_ms": latency_ms
        })
        yield f"data: {done_data}\n\n"

        logger.info(f"Stream completed in {latency_ms}ms for session {session_id}")

    except Exception as e:
        logger.error(f"Stream error: {e}")
        error_data = json.dumps({
            "type": "error",
            "error": "An error occurred during streaming. Please try again."
        })
        yield f"data: {error_data}\n\n"


@router.post("/chat/stream")
@limiter.limit("20/minute")
async def stream_message(request: Request, body: ChatRequest):
    """
    Stream a chat response using Server-Sent Events (SSE).

    The response streams tokens as they're generated by the AI.
    Each event has a 'type' field: 'token', 'done', or 'error'.

    Example usage with curl:
    ```
    curl -N -X POST http://localhost:8000/api/chat/stream \
      -H "Content-Type: application/json" \
      -d '{"session_id": "...", "message": "What is Physical AI?"}'
    ```

    Example usage with JavaScript EventSource:
    ```javascript
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id, message })
    });
    const reader = response.body.getReader();
    // Process stream...
    ```
    """
    # Validate message length
    if len(body.message) < 1:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    if len(body.message) > 10000:
        raise HTTPException(status_code=400, detail="Message too long (max 10000 characters)")

    # Validate selected_text if provided
    if body.selected_text and len(body.selected_text) > 5000:
        raise HTTPException(status_code=400, detail="Selected text too long (max 5000 characters)")

    # Verify session exists
    session = await session_service.get_session(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    logger.info(f"Starting stream for session {body.session_id}")

    return StreamingResponse(
        _sse_stream_generator(
            session_id=body.session_id,
            message=body.message,
            selected_text=body.selected_text
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )
