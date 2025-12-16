# Research: Integrated RAG Chatbot for Docusaurus Book

**Feature**: `001-docusaurus-safe-docs` | **Date**: 2025-12-16 | **Phase**: 0

## Overview

This document consolidates research findings for technology decisions and unknowns identified during planning.

---

## 1. FastAPI + OpenAI Agents SDK Integration

### Research Question
How to wrap the existing OpenAI Agents SDK `Runner.run_sync()` pattern into FastAPI async endpoints?

### Decision
Use `Runner.run()` (async) instead of `Runner.run_sync()` within FastAPI async endpoints.

### Rationale
- FastAPI is built on Starlette and fully async-native
- OpenAI Agents SDK provides both sync (`run_sync`) and async (`run`) methods
- Async execution allows non-blocking request handling
- Better performance under concurrent load

### Implementation Pattern
```python
from fastapi import FastAPI
from agents import Agent, Runner

app = FastAPI()

@app.post("/api/chat")
async def chat(request: ChatRequest):
    result = await Runner.run(agent, input=request.message)
    return {"response": result.final_output}
```

### Alternatives Considered
1. **Thread pool for sync calls**: Added complexity, defeats async purpose
2. **Background tasks**: Not suitable for request-response pattern
3. **Celery workers**: Overkill for this use case

---

## 2. SSE Streaming with OpenAI Agents SDK

### Research Question
How to stream responses from the agent to the frontend via SSE?

### Decision
Use `Runner.run_streamed()` with FastAPI's `StreamingResponse`.

### Rationale
- OpenAI Agents SDK supports streaming via `run_streamed()` method
- Returns async generator of stream events
- Native integration with FastAPI's streaming capabilities
- Browser EventSource API consumes SSE natively

### Implementation Pattern
```python
from fastapi.responses import StreamingResponse
from agents import Runner

async def stream_generator(agent, message):
    async with Runner.run_streamed(agent, input=message) as stream:
        async for event in stream.stream_events():
            if event.type == "raw_response_event":
                yield f"data: {event.data}\n\n"
    yield "data: [DONE]\n\n"

@app.get("/api/chat/stream")
async def chat_stream(session_id: str, message: str):
    return StreamingResponse(
        stream_generator(agent, message),
        media_type="text/event-stream"
    )
```

### Alternatives Considered
1. **WebSockets**: Requires connection state management, CORS complications
2. **Long Polling**: Higher latency, more HTTP overhead
3. **Non-streaming POST**: Poor UX for longer responses

---

## 3. Neon Serverless Postgres Integration

### Research Question
Best practices for connecting to Neon from FastAPI in a serverless-friendly way?

### Decision
Use `asyncpg` with connection pooling via Neon's pooled connection string.

### Rationale
- Neon provides pooled endpoints by default (`-pooler` suffix)
- `asyncpg` is the fastest async Postgres driver for Python
- Connection pooling handles serverless cold starts gracefully
- Compatible with SQLAlchemy async if needed later

### Implementation Pattern
```python
import asyncpg
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("NEON_DATABASE_URL")

@asynccontextmanager
async def get_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()
```

### Connection String Format
```
postgres://user:password@ep-xyz-pooler.region.aws.neon.tech/dbname?sslmode=require
```

### Alternatives Considered
1. **psycopg2**: Sync only, blocks event loop
2. **SQLAlchemy**: Added complexity for simple CRUD
3. **Prisma**: Python support is experimental

---

## 4. Docusaurus Chat Widget Integration

### Research Question
Best approach to add a floating chat widget to all Docusaurus pages?

### Decision
Use Docusaurus client module pattern (not swizzling).

### Rationale
- Client modules run on every page load
- No need to modify theme internals
- Survives Docusaurus upgrades cleanly
- Can inject React components into DOM

### Implementation Pattern

1. Create component at `src/components/ChatWidget/index.js`
2. Create client module at `src/clientModules/chatWidget.js`:
```javascript
import React from 'react';
import { createRoot } from 'react-dom/client';
import ChatWidget from '@site/src/components/ChatWidget';

export function onRouteDidUpdate() {
  const container = document.getElementById('chat-widget-root');
  if (!container) {
    const root = document.createElement('div');
    root.id = 'chat-widget-root';
    document.body.appendChild(root);
    createRoot(root).render(<ChatWidget />);
  }
}
```
3. Register in `docusaurus.config.js`:
```javascript
clientModules: [
  require.resolve('./src/clientModules/chatWidget.js'),
],
```

### Alternatives Considered
1. **Theme swizzling**: Couples to specific theme version, harder to maintain
2. **External script injection**: No React integration, janky
3. **Plugin**: Overkill for single component

---

## 5. Text Selection Context Capture

### Research Question
How to capture user-selected text and associate it with chat questions?

### Decision
Use `window.getSelection()` API with a floating action button.

### Rationale
- Native browser API, no dependencies
- Works on all modern browsers
- Can capture selection from any text element
- Debounce prevents performance issues

### Implementation Pattern
```javascript
// TextSelectionHandler.js
import { useEffect, useState } from 'react';

export function useTextSelection() {
  const [selection, setSelection] = useState(null);

  useEffect(() => {
    const handleSelection = () => {
      const sel = window.getSelection();
      const text = sel?.toString().trim();
      if (text && text.length > 10) {
        const range = sel.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        setSelection({ text, position: rect });
      } else {
        setSelection(null);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  return selection;
}
```

### Agent Context Injection
When `selected_text` is provided, modify agent instructions:
```python
base_instructions = agent.instructions
if selected_text:
    agent.instructions = f"""
{base_instructions}

The user has selected the following text passage for context:
---
{selected_text}
---
Focus your answer specifically on this selected content when relevant.
"""
```

### Alternatives Considered
1. **Highlight.js integration**: Overkill, doesn't help with selection
2. **Custom selection library**: Unnecessary dependency
3. **Context menu approach**: Poor mobile UX

---

## 6. CORS and Security Configuration

### Research Question
How to securely configure CORS for static frontend + separate backend?

### Decision
Strict origin whitelist with credentials support.

### Rationale
- GitHub Pages serves from `https://habibullahdevv.github.io`
- Backend will be on different origin (Cloud Run, Railway, etc.)
- Need to allow credentials for session cookies (optional future feature)

### Implementation Pattern
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://habibullahdevv.github.io",
        "http://localhost:3000",  # Local dev
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

### Alternatives Considered
1. **Wildcard origins**: Security risk in production
2. **Proxy through Docusaurus**: Would require SSR, not supported
3. **Same-origin deployment**: Not feasible with GitHub Pages

---

## 7. Rate Limiting Strategy

### Research Question
How to implement rate limiting without Redis/external state?

### Decision
Use `slowapi` (built on `limits`) with in-memory storage for MVP.

### Rationale
- Simple integration with FastAPI
- In-memory storage sufficient for single-instance deployment
- Can upgrade to Redis later if needed
- Session-based limiting prevents abuse

### Implementation Pattern
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat")
@limiter.limit("20/minute")
async def chat(request: Request, body: ChatRequest):
    ...
```

### Alternatives Considered
1. **Redis-based**: Added infrastructure complexity
2. **Token bucket custom**: Reinventing the wheel
3. **No rate limiting**: Risk of abuse/cost overrun

---

## 8. Backend Deployment Options

### Research Question
Where to deploy FastAPI backend with minimal cost and complexity?

### Decision
Primary: Railway. Fallback: Google Cloud Run.

### Rationale
- **Railway**:
  - Simple GitHub integration
  - $5/month free tier
  - Automatic SSL
  - Easy environment variable management
- **Cloud Run**:
  - Scale-to-zero
  - Pay-per-request
  - More complex setup

### Deployment Configuration (Railway)
```yaml
# railway.yaml
services:
  backend:
    source: backend/
    healthcheck: /api/health
    env:
      PORT: 8000
```

### Dockerfile
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Alternatives Considered
1. **Vercel**: Poor Python support, serverless cold starts
2. **Heroku**: Free tier removed
3. **AWS Lambda**: Complex setup for streaming

---

## 9. Error Handling Patterns

### Research Question
How to handle failures gracefully across the RAG pipeline?

### Decision
Implement layered error handling with user-friendly messages.

### Error Categories

| Category | Example | User Message | Log Level |
|----------|---------|--------------|-----------|
| Retrieval Failure | Qdrant timeout | "I'm having trouble searching. Please try again." | ERROR |
| LLM Failure | Gemini rate limit | "Our AI is busy. Please wait a moment." | WARNING |
| Embedding Failure | Cohere API down | "I can't process your question right now." | ERROR |
| Session Failure | Neon connection | "Chat history unavailable. Starting fresh." | WARNING |
| Validation Error | Empty message | "Please enter a question." | INFO |

### Implementation Pattern
```python
from fastapi import HTTPException

class RAGServiceError(Exception):
    def __init__(self, message: str, user_message: str):
        self.message = message
        self.user_message = user_message

@app.exception_handler(RAGServiceError)
async def rag_error_handler(request, exc):
    logger.error(f"RAG Error: {exc.message}")
    return JSONResponse(
        status_code=503,
        content={"error": exc.user_message, "retry": True}
    )
```

---

## 10. Collection Name Consistency

### Research Question
The agent.py uses `humanoid_ai_book` but ingestion creates `Ai_Native_Book`. Which is correct?

### Decision
Standardize on `Ai_Native_Book` (matches ingestion).

### Rationale
- Ingestion script (`main.py`) creates `Ai_Native_Book`
- This collection contains the actual embedded data
- `humanoid_ai_book` appears to be a leftover from development

### Migration Steps
1. Update `agent.py` line 50: change `humanoid_ai_book` → `Ai_Native_Book`
2. Update any environment variables referencing the collection
3. Verify retrieval works after update

---

## Summary of Decisions

| Area | Decision | Confidence |
|------|----------|------------|
| API Framework | FastAPI | High |
| Streaming | SSE via StreamingResponse | High |
| Database | Neon Postgres + asyncpg | High |
| Frontend Integration | Client module pattern | High |
| Text Selection | window.getSelection() | High |
| Rate Limiting | slowapi in-memory | Medium |
| Deployment | Railway (primary) | Medium |
| Error Handling | Layered with user messages | High |

All "NEEDS CLARIFICATION" items have been resolved. Ready for Phase 1.
