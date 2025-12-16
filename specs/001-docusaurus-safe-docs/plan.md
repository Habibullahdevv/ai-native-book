# Implementation Plan: Integrated RAG Chatbot for Docusaurus Book

**Branch**: `001-docusaurus-safe-docs` | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)
**Input**: User feature request for RAG chatbot integration

**Note**: This plan extends the existing safe documentation editing spec to add an AI-powered chatbot.

## Summary

Integrate an AI-powered RAG chatbot into the existing Docusaurus textbook website. The chatbot will:
1. Answer general questions about the Physical AI & Humanoid Robotics book content
2. Support context-aware Q&A based on user-selected text passages
3. Persist chat sessions using Neon Serverless Postgres
4. Leverage the existing Qdrant-backed RAG agent without rewriting core logic

## Technical Context

**Language/Version**:
- Backend: Python 3.13+ (existing)
- Frontend: JavaScript/React 18 (Docusaurus 3.9.2)

**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK (`agents>=1.4.0`), Cohere (`cohere>=5.20.0`), Qdrant Client (`qdrant-client>=1.16.1`), psycopg2/asyncpg (Neon)
- Frontend: React 18, clsx, @docusaurus/core

**Storage**:
- Vector DB: Qdrant Cloud (existing, collection: `Ai_Native_Book`)
- Sessions: Neon Serverless Postgres (new)

**Testing**: pytest (backend), Jest (optional frontend)

**Target Platform**:
- Backend: Linux server / Docker / Cloud Run
- Frontend: GitHub Pages (static hosting)

**Project Type**: Web application (backend + frontend)

**Performance Goals**:
- Chat response latency: <3s p95 for first token
- Embedding lookup: <500ms p95
- Concurrent users: 50+ (free tier constraints)

**Constraints**:
- Qdrant Cloud Free Tier limits
- Neon Free Tier: 0.5GB storage, 100 hours compute
- GitHub Pages: static only (no SSR)
- Gemini API rate limits

**Scale/Scope**:
- Single textbook (~50 pages)
- Estimated 100-500 daily active users
- Chat history retention: 30 days

## Constitution Check

*GATE: Verified against `.specify/memory/constitution.md`*

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Scientifically Accurate | ✅ Pass | RAG grounds responses in textbook content |
| Clarity for Engineers | ✅ Pass | API contracts and clean architecture |
| Reproducibility | ✅ Pass | Docker deployment, env configuration |
| Ethical AI Integration | ✅ Pass | User consent, no PII collection, transparent AI |

**Key Standards Compliance**:
- ✅ Reuses existing verified RAG pipeline
- ✅ No new unverified AI claims
- ✅ Text-selection grounding ensures accurate context

## Project Structure

### Documentation (this feature)

```text
specs/001-docusaurus-safe-docs/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions
├── data-model.md        # Phase 1: Database schema
├── contracts/           # Phase 1: OpenAPI specs
│   └── chat-api.yaml
├── quickstart.md        # Phase 1: Local setup guide
└── tasks.md             # Phase 2: Implementation tasks (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── main.py                    # Data ingestion (existing)
├── agent.py                   # RAG agent core (existing)
├── retrieving.py              # Retrieval utility (existing)
├── api/                       # NEW: FastAPI application
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py           # Chat endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py  # Wraps existing agent
│   │   └── session_service.py# Neon session management
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic models
│   └── db/
│       ├── __init__.py
│       └── connection.py     # Neon connection pool
├── requirements.txt          # NEW: Production dependencies
├── Dockerfile               # NEW: Container deployment
└── .env.example             # NEW: Environment template

src/
├── components/              # NEW: React components
│   └── ChatWidget/
│       ├── index.js
│       ├── ChatWidget.js
│       ├── ChatWidget.module.css
│       ├── ChatMessage.js
│       └── TextSelectionHandler.js
├── css/
│   └── custom.css           # Existing (extend for chatbot)
└── pages/
    └── index.js             # Existing (no changes needed)

# Root-level additions
.env.example                 # Environment variables template
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docusaurus Frontend                          │
│  ┌──────────────┐  ┌─────────────────────────────────────────┐ │
│  │  Book Pages  │  │          ChatWidget Component           │ │
│  │  (docs/**)   │  │  ┌─────────────┐ ┌──────────────────┐  │ │
│  │              │◄─┼──│ Text Select │ │  Chat Interface  │  │ │
│  │              │  │  │   Handler   │ │  - Messages      │  │ │
│  │              │  │  └─────────────┘ │  - Input         │  │ │
│  │              │  │                  │  - Streaming     │  │ │
│  └──────────────┘  │                  └────────┬─────────┘  │ │
│                    └──────────────────────────│─────────────┘ │
└───────────────────────────────────────────────│───────────────┘
                                                │ HTTPS/SSE
                                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Routes                             │  │
│  │  POST /api/chat        - Send message                    │  │
│  │  GET  /api/chat/stream - SSE stream                      │  │
│  │  POST /api/sessions    - Create session                  │  │
│  │  GET  /api/sessions/:id - Get session history           │  │
│  └────────────────────────────┬─────────────────────────────┘  │
│                               │                                 │
│  ┌────────────────┐  ┌───────┴───────┐  ┌──────────────────┐  │
│  │ Agent Service  │  │Session Service│  │  Neon Postgres   │  │
│  │                │  │               │  │                  │  │
│  │ - Wraps agent  │  │ - CRUD ops    │  │ - chat_sessions  │  │
│  │ - Injects ctx  │  │ - History     │  │ - chat_messages  │  │
│  └───────┬────────┘  └───────────────┘  └──────────────────┘  │
│          │                                                      │
└──────────│──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│               Existing RAG Infrastructure                       │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │  OpenAI Agent  │  │  Cohere API    │  │  Qdrant Cloud   │  │
│  │  (Gemini 2.0)  │  │  Embeddings    │  │  Vector Store   │  │
│  │                │  │                │  │                 │  │
│  │  agent.py      │  │  embed-v3.0    │  │ Ai_Native_Book  │  │
│  └────────────────┘  └────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. FastAPI over Flask
- **Decision**: Use FastAPI for the API layer
- **Rationale**: Native async support, automatic OpenAPI docs, Pydantic validation, SSE streaming support
- **Alternatives Rejected**: Flask (no native async), Django (too heavy)

### 2. Streaming via Server-Sent Events (SSE)
- **Decision**: Use SSE for streaming chat responses
- **Rationale**: Simple implementation, works with static hosting, no WebSocket complexity
- **Alternatives Rejected**: WebSockets (requires stateful server), Long polling (inefficient)

### 3. Neon Serverless Postgres
- **Decision**: Use Neon for session/message persistence
- **Rationale**: Serverless scale-to-zero, generous free tier, SQL compatibility
- **Alternatives Rejected**: Supabase (heavier), SQLite (no cloud persistence), Redis (not relational)

### 4. Docusaurus Theme Component (Swizzle)
- **Decision**: Create a custom ChatWidget using Docusaurus component swizzling
- **Rationale**: Integrates natively with theme, survives upgrades, follows Docusaurus patterns
- **Alternatives Rejected**: External widget iframe (poor UX), Direct DOM injection (fragile)

### 5. Text Selection Context
- **Decision**: Capture selected text and pass as additional context to RAG query
- **Rationale**: Enables "Ask about this passage" feature, improves answer relevance
- **Implementation**: Browser Selection API → context parameter → agent instruction modification

## API Endpoints Overview

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/sessions` | Create new chat session |
| GET | `/api/sessions/{id}` | Retrieve session with messages |
| POST | `/api/chat` | Send message (non-streaming) |
| GET | `/api/chat/stream` | Stream response via SSE |
| GET | `/api/health` | Health check endpoint |

## Data Flow

### Chat Message Flow

```
1. User types question in ChatWidget
2. Frontend calls POST /api/chat or GET /api/chat/stream
3. FastAPI receives request with:
   - session_id (UUID)
   - message (string)
   - selected_text (optional string)
4. Agent Service:
   a. If selected_text provided, prepend to agent instructions
   b. Call retrieve() tool with query
   c. Generate response using Gemini
5. Session Service:
   a. Store user message in Neon
   b. Store assistant response in Neon
6. Return response (or stream tokens via SSE)
7. Frontend renders response in chat UI
```

### Text Selection Flow

```
1. User selects text on any docs/** page
2. TextSelectionHandler captures selection
3. Floating "Ask AI" button appears
4. User clicks → opens ChatWidget with context
5. selected_text sent with first message
```

## Environment Variables

```env
# Backend (.env)
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=https://your-qdrant-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=postgres://user:pass@host/db?sslmode=require
CORS_ORIGINS=https://habibullahdevv.github.io

# Frontend (build-time)
REACT_APP_API_URL=https://your-backend-url.com
```

## Security Considerations

1. **CORS Configuration**: Strict origin whitelist for production
2. **Rate Limiting**: Implement per-session rate limits (e.g., 20 req/min)
3. **Input Sanitization**: Validate message length and content
4. **No PII Storage**: Session IDs are anonymous UUIDs
5. **API Key Rotation**: Move all hardcoded keys to environment variables (CRITICAL)
6. **HTTPS Only**: Enforce TLS in production

## Complexity Tracking

> No constitution violations requiring justification

## Next Steps

1. **Phase 0**: Create `research.md` with technology decisions
2. **Phase 1**: Create `data-model.md`, `contracts/chat-api.yaml`, `quickstart.md`
3. **Phase 2**: Run `/sp.tasks` to generate implementation tasks

---

## Appendix: Existing Code Analysis

### Backend State

| File | Status | Notes |
|------|--------|-------|
| `main.py` | ✅ Working | Ingestion pipeline, uses Qdrant Cloud |
| `agent.py` | ⚠️ Needs fixes | Placeholder credentials, collection mismatch |
| `retrieving.py` | ⚠️ Needs fixes | Hardcoded credentials (security issue) |

### Critical Issues to Address

1. **Credential Exposure**: Move all API keys to `.env`
2. **Collection Name Mismatch**: `agent.py` uses `humanoid_ai_book`, should be `Ai_Native_Book`
3. **Missing Error Handling**: Add try/except for API failures
4. **No API Server**: Need to wrap agent in FastAPI

### Frontend State

| Component | Status | Notes |
|-----------|--------|-------|
| `src/pages/index.js` | ✅ Working | Homepage with module links |
| `src/css/custom.css` | ✅ Working | Theme customization |
| ChatWidget | 🆕 New | To be created |
