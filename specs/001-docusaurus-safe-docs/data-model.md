# Data Model: Integrated RAG Chatbot

**Feature**: `001-docusaurus-safe-docs` | **Date**: 2025-12-16 | **Phase**: 1

## Overview

This document defines the database schema for chat session persistence using Neon Serverless Postgres.

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│           chat_sessions             │
├─────────────────────────────────────┤
│ id (PK)          UUID               │
│ created_at       TIMESTAMPTZ        │
│ updated_at       TIMESTAMPTZ        │
│ metadata         JSONB              │
└─────────────────┬───────────────────┘
                  │ 1:N
                  ▼
┌─────────────────────────────────────┐
│           chat_messages             │
├─────────────────────────────────────┤
│ id (PK)          UUID               │
│ session_id (FK)  UUID               │
│ role             VARCHAR(20)        │
│ content          TEXT               │
│ selected_text    TEXT (nullable)    │
│ metadata         JSONB              │
│ created_at       TIMESTAMPTZ        │
└─────────────────────────────────────┘
```

---

## Entities

### 1. chat_sessions

Represents a single chat conversation instance.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique session identifier |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Session creation timestamp |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Last activity timestamp |
| `metadata` | JSONB | DEFAULT '{}' | Extensible metadata (user-agent, source page, etc.) |

**Indexes**:
- `idx_sessions_created_at`: B-tree on `created_at` for time-based queries
- `idx_sessions_updated_at`: B-tree on `updated_at` for activity sorting

### 2. chat_messages

Stores individual messages within a session.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique message identifier |
| `session_id` | UUID | NOT NULL, FK → chat_sessions(id) ON DELETE CASCADE | Parent session reference |
| `role` | VARCHAR(20) | NOT NULL, CHECK (role IN ('user', 'assistant', 'system')) | Message sender role |
| `content` | TEXT | NOT NULL | Message text content |
| `selected_text` | TEXT | NULLABLE | User-selected context text (for user messages) |
| `metadata` | JSONB | DEFAULT '{}' | Extensible metadata (tokens used, latency, etc.) |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Message creation timestamp |

**Indexes**:
- `idx_messages_session_id`: B-tree on `session_id` for session message retrieval
- `idx_messages_created_at`: B-tree on `created_at` for chronological ordering

---

## SQL Schema

```sql
-- Enable UUID extension (Neon has this by default)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- Messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    selected_text TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON chat_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_sessions_updated_at ON chat_sessions(updated_at);
CREATE INDEX IF NOT EXISTS idx_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON chat_messages(created_at);

-- Function to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for sessions updated_at
CREATE TRIGGER update_sessions_updated_at
    BEFORE UPDATE ON chat_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Validation Rules

### chat_sessions

| Field | Rule | Error Message |
|-------|------|---------------|
| `id` | Valid UUID v4 | "Invalid session ID format" |
| `metadata` | Valid JSON object | "Metadata must be a JSON object" |

### chat_messages

| Field | Rule | Error Message |
|-------|------|---------------|
| `id` | Valid UUID v4 | "Invalid message ID format" |
| `session_id` | Must exist in chat_sessions | "Session not found" |
| `role` | One of: 'user', 'assistant', 'system' | "Invalid message role" |
| `content` | Non-empty string, max 10,000 chars | "Message content required" / "Message too long" |
| `selected_text` | Max 5,000 chars if provided | "Selected text too long" |

---

## State Transitions

### Session Lifecycle

```
[Created] → [Active] → [Expired]
    │           │
    │           └─ Messages added (updates updated_at)
    │
    └─ Initial creation via POST /api/sessions
```

### Message Roles Flow

```
User sends message:
  [user] → stored

Agent processes:
  [assistant] → stored

(Optional) System context:
  [system] → stored (not exposed to frontend)
```

---

## Pydantic Models (Python)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, Literal
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatSessionCreate(BaseModel):
    """Request model for creating a new session"""
    metadata: dict = Field(default_factory=dict)

class ChatSessionResponse(BaseModel):
    """Response model for session data"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    metadata: dict

class ChatMessageCreate(BaseModel):
    """Request model for creating a new message"""
    session_id: UUID
    content: str = Field(..., min_length=1, max_length=10000)
    selected_text: Optional[str] = Field(None, max_length=5000)

class ChatMessageResponse(BaseModel):
    """Response model for message data"""
    id: UUID
    session_id: UUID
    role: MessageRole
    content: str
    selected_text: Optional[str]
    metadata: dict
    created_at: datetime

class SessionWithMessages(BaseModel):
    """Combined session with full message history"""
    session: ChatSessionResponse
    messages: list[ChatMessageResponse]
```

---

## Sample Queries

### Create Session
```sql
INSERT INTO chat_sessions (metadata)
VALUES ('{"source": "docs/module1", "user_agent": "Mozilla/5.0..."}'::jsonb)
RETURNING id, created_at, updated_at, metadata;
```

### Add Message
```sql
INSERT INTO chat_messages (session_id, role, content, selected_text, metadata)
VALUES (
    'a1b2c3d4-...',
    'user',
    'What is Physical AI?',
    'Physical AI represents the convergence of artificial intelligence with robotics...',
    '{"tokens": 5}'::jsonb
)
RETURNING id, session_id, role, content, selected_text, metadata, created_at;
```

### Get Session with Messages
```sql
SELECT
    s.id as session_id,
    s.created_at as session_created,
    s.updated_at as session_updated,
    s.metadata as session_metadata,
    m.id as message_id,
    m.role,
    m.content,
    m.selected_text,
    m.metadata as message_metadata,
    m.created_at as message_created
FROM chat_sessions s
LEFT JOIN chat_messages m ON m.session_id = s.id
WHERE s.id = 'a1b2c3d4-...'
ORDER BY m.created_at ASC;
```

### Cleanup Old Sessions (30-day retention)
```sql
DELETE FROM chat_sessions
WHERE updated_at < now() - INTERVAL '30 days';
```

---

## Data Retention Policy

| Data Type | Retention | Cleanup Method |
|-----------|-----------|----------------|
| Sessions | 30 days from last activity | Scheduled job (daily) |
| Messages | Cascade delete with session | FK constraint |
| Metadata | Same as parent entity | Cascade |

---

## Extensibility

The `metadata` JSONB columns allow for future extensions without schema changes:

**Potential future metadata fields**:

For `chat_sessions`:
```json
{
  "source_page": "/docs/module1/intro",
  "user_agent": "Mozilla/5.0...",
  "referrer": "google.com",
  "locale": "en-US"
}
```

For `chat_messages`:
```json
{
  "tokens_used": 150,
  "latency_ms": 1234,
  "model_version": "gemini-2.0-flash",
  "retrieval_count": 5,
  "feedback": "helpful"
}
```

---

## Migration Notes

### Initial Setup
Run the SQL schema above against Neon database to create tables.

### Version Control
Schema changes should be managed via migration files in `backend/migrations/`.

### Rollback
```sql
DROP TABLE IF EXISTS chat_messages;
DROP TABLE IF EXISTS chat_sessions;
DROP FUNCTION IF EXISTS update_updated_at_column;
```
