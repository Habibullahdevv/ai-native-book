---
id: 002
title: RAG Chatbot Integration Plan
stage: plan
date: 2025-12-16
surface: agent
model: claude-sonnet-4.5
feature: 001-docusaurus-safe-docs
branch: 001-docusaurus-safe-docs
user: Habibullahdevv
command: /sp.plan
labels: ["rag", "chatbot", "fastapi", "docusaurus", "architecture"]
links:
  spec: specs/001-docusaurus-safe-docs/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-docusaurus-safe-docs/plan.md
  - specs/001-docusaurus-safe-docs/research.md
  - specs/001-docusaurus-safe-docs/data-model.md
  - specs/001-docusaurus-safe-docs/contracts/chat-api.yaml
  - specs/001-docusaurus-safe-docs/quickstart.md
tests:
  - null
---

## Prompt

Integrated RAG Chatbot for Docusaurus Book

## Context
We already have a working backend RAG agent located in a folder named `backend/`.
The backend uses:
- Python
- OpenAI Agents SDK
- Cohere embeddings
- Qdrant Cloud (Free Tier)
- Pluggable OpenAI-compatible LLM providers

The frontend is a Docusaurus website hosting a published textbook.

## Goal
Plan a clean architecture to embed an AI-powered RAG chatbot into the Docusaurus website using:
- FastAPI as the backend API layer
- OpenAI Agents / ChatKit-compatible patterns
- Neon Serverless Postgres for chat history & sessions
- Qdrant for semantic retrieval
- Support for answering:
  1. General book questions
  2. Questions based ONLY on user-selected text

## High-Level Architecture
- FastAPI wraps the existing agent
- REST endpoints expose chat functionality
- Neon Postgres stores chat sessions & messages
- Docusaurus embeds a React-based chatbot widget
- Widget communicates with FastAPI via fetch/streaming
- Optional text-selection context is passed to backend

## Key Components
1. Backend API (`backend/api`)
2. Chat session persistence (Neon)
3. Agent enhancement for selected-text grounding
4. Frontend chatbot UI (React)
5. Secure CORS & env configuration

## Constraints
- Do NOT rewrite the RAG core logic
- Reuse existing agent, tools, and retrieval

## Response snapshot

Created comprehensive implementation plan for integrating RAG chatbot into Docusaurus textbook site.

**Key Artifacts Created:**

1. **plan.md** - Full implementation plan with:
   - Technical context (Python 3.13, FastAPI, React 18, Docusaurus 3.9)
   - Architecture diagram showing Frontend → FastAPI → RAG components
   - API endpoints: sessions, chat, streaming (SSE)
   - Environment variables and security considerations
   - Constitution compliance verification

2. **research.md** - Technology decisions including:
   - FastAPI + OpenAI Agents SDK async integration
   - SSE streaming with `Runner.run_streamed()`
   - Neon Postgres with asyncpg
   - Docusaurus client module pattern for ChatWidget
   - Text selection via `window.getSelection()` API
   - Rate limiting with slowapi
   - Deployment strategy (Railway primary)

3. **data-model.md** - Database schema:
   - `chat_sessions` table (UUID, timestamps, metadata)
   - `chat_messages` table (role, content, selected_text)
   - Pydantic models for API validation
   - SQL schema with indexes and triggers

4. **contracts/chat-api.yaml** - OpenAPI 3.1 specification:
   - POST /api/sessions - Create session
   - GET /api/sessions/{id} - Get session with messages
   - POST /api/chat - Send message (non-streaming)
   - GET /api/chat/stream - SSE streaming
   - GET /api/health - Health check

5. **quickstart.md** - Local development guide:
   - Prerequisites and setup steps
   - Environment configuration
   - Common troubleshooting

**Critical Issues Identified:**
- Hardcoded credentials in existing backend files (security risk)
- Collection name mismatch: `humanoid_ai_book` vs `Ai_Native_Book`
- No error handling in current agent code

## Outcome

- ✅ Impact: Complete architecture planned for RAG chatbot integration
- 🧪 Tests: None (planning phase)
- 📁 Files: 5 files created (plan.md, research.md, data-model.md, chat-api.yaml, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation task list
- 🧠 Reflection: Planning phase complete. Ready for implementation with clear contracts and data models.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement FastAPI wrapper for existing agent
