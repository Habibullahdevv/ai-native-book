"""
Session service for managing chat sessions and messages
Uses Neon Serverless Postgres for persistence
"""
import logging
from uuid import UUID
from typing import Optional
from datetime import datetime, timezone

from ..db.connection import execute_one, execute_query, execute
from ..models.schemas import (
    SessionResponse,
    MessageResponse,
    SessionWithMessages,
    MessageRole
)

logger = logging.getLogger(__name__)


async def create_session(metadata: dict = None) -> SessionResponse:
    """
    Create a new chat session.

    Args:
        metadata: Optional metadata dict for the session

    Returns:
        SessionResponse with the created session data
    """
    metadata = metadata or {}

    query = """
        INSERT INTO chat_sessions (metadata)
        VALUES ($1::jsonb)
        RETURNING id, created_at, updated_at, metadata
    """

    import json
    row = await execute_one(query, json.dumps(metadata))

    if not row:
        raise RuntimeError("Failed to create session")

    logger.info(f"Created session: {row['id']}")

    return SessionResponse(
        id=row["id"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        metadata=row["metadata"] or {}
    )


async def get_session(session_id: UUID) -> Optional[SessionResponse]:
    """
    Get a session by ID.

    Args:
        session_id: The session UUID

    Returns:
        SessionResponse if found, None otherwise
    """
    query = """
        SELECT id, created_at, updated_at, metadata
        FROM chat_sessions
        WHERE id = $1
    """

    row = await execute_one(query, session_id)

    if not row:
        return None

    return SessionResponse(
        id=row["id"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        metadata=row["metadata"] or {}
    )


async def get_session_with_messages(session_id: UUID) -> Optional[SessionWithMessages]:
    """
    Get a session with all its messages.

    Args:
        session_id: The session UUID

    Returns:
        SessionWithMessages if found, None otherwise
    """
    # Get session
    session = await get_session(session_id)
    if not session:
        return None

    # Get messages
    messages_query = """
        SELECT id, session_id, role, content, selected_text, metadata, created_at
        FROM chat_messages
        WHERE session_id = $1
        ORDER BY created_at ASC
    """

    rows = await execute_query(messages_query, session_id)

    messages = [
        MessageResponse(
            id=row["id"],
            session_id=row["session_id"],
            role=MessageRole(row["role"]),
            content=row["content"],
            selected_text=row["selected_text"],
            metadata=row["metadata"] or {},
            created_at=row["created_at"]
        )
        for row in rows
    ]

    return SessionWithMessages(
        session=session,
        messages=messages
    )


async def save_message(
    session_id: UUID,
    role: MessageRole,
    content: str,
    selected_text: Optional[str] = None,
    metadata: dict = None
) -> MessageResponse:
    """
    Save a message to a session.

    Args:
        session_id: The session UUID
        role: Message role (user, assistant, system)
        content: Message content
        selected_text: Optional selected text context
        metadata: Optional metadata dict

    Returns:
        MessageResponse with the created message data
    """
    metadata = metadata or {}

    query = """
        INSERT INTO chat_messages (session_id, role, content, selected_text, metadata)
        VALUES ($1, $2, $3, $4, $5::jsonb)
        RETURNING id, session_id, role, content, selected_text, metadata, created_at
    """

    import json
    row = await execute_one(
        query,
        session_id,
        role.value,
        content,
        selected_text,
        json.dumps(metadata)
    )

    if not row:
        raise RuntimeError("Failed to save message")

    logger.debug(f"Saved {role.value} message to session {session_id}")

    return MessageResponse(
        id=row["id"],
        session_id=row["session_id"],
        role=MessageRole(row["role"]),
        content=row["content"],
        selected_text=row["selected_text"],
        metadata=row["metadata"] or {},
        created_at=row["created_at"]
    )


async def get_session_messages(
    session_id: UUID,
    limit: int = 100
) -> list[MessageResponse]:
    """
    Get messages for a session.

    Args:
        session_id: The session UUID
        limit: Maximum number of messages to return

    Returns:
        List of MessageResponse objects
    """
    query = """
        SELECT id, session_id, role, content, selected_text, metadata, created_at
        FROM chat_messages
        WHERE session_id = $1
        ORDER BY created_at ASC
        LIMIT $2
    """

    rows = await execute_query(query, session_id, limit)

    return [
        MessageResponse(
            id=row["id"],
            session_id=row["session_id"],
            role=MessageRole(row["role"]),
            content=row["content"],
            selected_text=row["selected_text"],
            metadata=row["metadata"] or {},
            created_at=row["created_at"]
        )
        for row in rows
    ]


async def delete_session(session_id: UUID) -> bool:
    """
    Delete a session and all its messages.

    Args:
        session_id: The session UUID

    Returns:
        True if deleted, False if not found
    """
    query = "DELETE FROM chat_sessions WHERE id = $1"
    result = await execute(query, session_id)

    # Result format is "DELETE N" where N is row count
    deleted = result and "DELETE 1" in result

    if deleted:
        logger.info(f"Deleted session: {session_id}")

    return deleted
