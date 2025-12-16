# Tasks: Integrated RAG Chatbot for Docusaurus Book

**Input**: Design documents from `/specs/001-docusaurus-safe-docs/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/chat-api.yaml ✅

**Tests**: Not explicitly requested - test tasks omitted (add with `/sp.tasks --with-tests` if needed)

**Organization**: Tasks grouped by user story for independent implementation and testing.

**Constitution Alignment**: All tasks adhere to scientific accuracy, reproducibility, and verification standards per `.specify/memory/constitution.md`.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1=General Book Q&A, US2=Selected-Text Q&A, US3=Chat History

## Path Conventions (from plan.md)

- **Backend**: `backend/api/` (FastAPI)
- **Frontend**: `src/components/`, `src/clientModules/`
- **Database**: `backend/api/db/`

---

## Phase 1: Setup (Backend Infrastructure)

**Purpose**: Create FastAPI project structure and fix existing code issues

- [x] T001 Create backend/api/ directory structure per plan.md: `api/__init__.py`, `api/routes/`, `api/services/`, `api/models/`, `api/db/`
- [x] T002 Create requirements.txt with dependencies: fastapi, uvicorn, asyncpg, python-dotenv, slowapi in `backend/requirements.txt`
- [x] T003 [P] Create .env.example with all required environment variables in `backend/.env.example`
- [x] T004 [P] Fix agent.py: Move hardcoded credentials to environment variables in `backend/agent.py`
- [x] T005 [P] Fix agent.py: Update collection name from "humanoid_ai_book" to "Ai_Native_Book" in `backend/agent.py`
- [x] T006 [P] Fix retrieving.py: Move hardcoded Cohere/Qdrant credentials to environment variables in `backend/retrieving.py`

---

## Phase 2: Foundational (Backend Core)

**Purpose**: Database connection, Pydantic schemas, and FastAPI app entry point

**⚠️ CRITICAL**: No API endpoints can be implemented until this phase is complete

- [x] T007 Create Pydantic schemas from data-model.md in `backend/api/models/schemas.py`
- [x] T008 Create database connection pool with asyncpg in `backend/api/db/connection.py`
- [x] T009 Create SQL schema file for Neon migration in `backend/api/db/schema.sql`
- [x] T010 Create FastAPI app entry point with CORS middleware in `backend/api/main.py`
- [x] T011 [P] Create custom exception handlers and error responses in `backend/api/main.py`
- [x] T012 [P] Add rate limiting middleware using slowapi in `backend/api/main.py`
- [x] T013 Implement health check endpoint GET /api/health in `backend/api/routes/health.py`

**Checkpoint**: FastAPI app runs, health check returns status, database connects

---

## Phase 3: User Story 1 - General Book Q&A (Priority: P1) 🎯 MVP

**Goal**: Users can ask general questions about the Physical AI book and receive RAG-powered answers

**Independent Test**: Start backend, POST to /api/chat with a question like "What is Physical AI?", receive answer grounded in book content

### Implementation for User Story 1

- [x] T014 [US1] Create agent_service.py wrapping existing agent.py with async support in `backend/api/services/agent_service.py`
- [x] T015 [US1] Refactor retrieve() function for async usage in `backend/api/services/agent_service.py`
- [x] T016 [US1] Create session_service.py with create_session() function in `backend/api/services/session_service.py`
- [x] T017 [US1] Add get_session() function to retrieve session with messages in `backend/api/services/session_service.py`
- [x] T018 [US1] Add save_message() function for storing user and assistant messages in `backend/api/services/session_service.py`
- [x] T019 [US1] Create sessions router with POST /api/sessions endpoint in `backend/api/routes/sessions.py`
- [x] T020 [US1] Add GET /api/sessions/{session_id} endpoint in `backend/api/routes/sessions.py`
- [x] T021 [US1] Create chat router with POST /api/chat endpoint (non-streaming) in `backend/api/routes/chat.py`
- [x] T022 [US1] Register routes in FastAPI app in `backend/api/main.py`
- [x] T023 [US1] Add error handling: "I don't know" when answer not in retrieved context in `backend/api/services/agent_service.py`
- [x] T024 [US1] Add input validation: message length (1-10000 chars) in `backend/api/routes/chat.py`

**Checkpoint**: POST /api/chat returns RAG-grounded answers, sessions persist in Neon

---

## Phase 4: User Story 2 - Selected-Text Q&A (Priority: P1) 🎯 MVP

**Goal**: Users can select text on any docs page and ask questions specifically about that passage

**Independent Test**: POST to /api/chat with `selected_text` parameter, verify response focuses on selected content

### Implementation for User Story 2

- [x] T025 [US2] Extend agent_service.py to inject selected_text into agent instructions in `backend/api/services/agent_service.py`
- [x] T026 [US2] Update POST /api/chat to accept optional selected_text parameter in `backend/api/routes/chat.py`
- [x] T027 [US2] Store selected_text in chat_messages table when provided in `backend/api/services/session_service.py`
- [x] T028 [US2] Add validation: selected_text max 5000 chars in `backend/api/routes/chat.py`

**Checkpoint**: Selected-text queries return context-specific answers

---

## Phase 5: User Story 3 - Streaming Responses (Priority: P2)

**Goal**: Chat responses stream in real-time via SSE for better UX

**Independent Test**: GET /api/chat/stream returns SSE events with tokens, test with curl or EventSource

### Implementation for User Story 3

- [x] T029 [US3] Add run_streamed() wrapper in agent_service.py using Runner.run_streamed() in `backend/api/services/agent_service.py`
- [x] T030 [US3] Create SSE stream generator function in `backend/api/routes/chat.py`
- [x] T031 [US3] Implement POST /api/chat/stream endpoint with StreamingResponse in `backend/api/routes/chat.py`
- [x] T032 [US3] Add SSE event types: token, done, error in `backend/api/routes/chat.py`
- [x] T033 [US3] Store complete streamed response to database after stream ends in `backend/api/routes/chat.py`

**Checkpoint**: SSE streaming works end-to-end, tokens appear progressively

---

## Phase 6: User Story 4 - Frontend ChatWidget (Priority: P1) 🎯 MVP

**Goal**: Docusaurus site has a floating chat widget on all pages

**Independent Test**: Run `npm start`, navigate to any page, click chat button, send message, see response

### Implementation for User Story 4

- [x] T034 [P] [US4] Create ChatWidget component structure in `src/components/ChatWidget/index.js`
- [x] T035 [P] [US4] Create ChatWidget.module.css with floating button and panel styles in `src/components/ChatWidget/ChatWidget.module.css`
- [x] T036 [US4] Implement ChatWidget.js with state management (open/closed, messages, loading) in `src/components/ChatWidget/ChatWidget.js`
- [x] T037 [US4] Create ChatMessage.js component for rendering individual messages in `src/components/ChatWidget/ChatMessage.js`
- [x] T038 [US4] Implement API client functions: createSession, sendMessage in `src/components/ChatWidget/api.js`
- [x] T039 [US4] Add loading spinner and error state handling in `src/components/ChatWidget/ChatWidget.js`
- [x] T040 [US4] Create Docusaurus client module to inject ChatWidget globally in `src/clientModules/chatWidget.js`
- [x] T041 [US4] Register clientModule in docusaurus.config.js in `docusaurus.config.js`
- [x] T042 [US4] Add environment variable for API URL in `.env.local` (build-time)

**Checkpoint**: Chat widget appears on all pages, can send/receive messages

---

## Phase 7: User Story 5 - Text Selection Integration (Priority: P2)

**Goal**: Users can select text on docs pages and click "Ask AI" to query about the selection

**Independent Test**: Select text on any docs page, see floating "Ask AI" button, click to open chat with context

### Implementation for User Story 5

- [x] T043 [US5] Create TextSelectionHandler.js using window.getSelection() API in `src/components/ChatWidget/TextSelectionHandler.js`
- [x] T044 [US5] Create floating "Ask AI" button that appears on text selection in `src/components/ChatWidget/TextSelectionHandler.js`
- [x] T045 [US5] Integrate TextSelectionHandler with ChatWidget state in `src/components/ChatWidget/ChatWidget.js`
- [x] T046 [US5] Pass selected_text to API when sending messages in `src/components/ChatWidget/api.js`
- [x] T047 [US5] Display selected text context in chat UI (quoted) in `src/components/ChatWidget/ChatMessage.js`
- [x] T048 [US5] Add debounce to prevent performance issues on selection in `src/components/ChatWidget/TextSelectionHandler.js`

**Checkpoint**: Text selection → Ask AI → context-aware response flow works

---

## Phase 8: User Story 6 - SSE Streaming in Frontend (Priority: P2)

**Goal**: Frontend uses SSE to display streaming responses token-by-token

**Independent Test**: Send message, see response appear progressively (not all at once)

### Implementation for User Story 6

- [x] T049 [US6] Implement EventSource client for /api/chat/stream in `src/components/ChatWidget/api.js`
- [x] T050 [US6] Update ChatWidget to render streaming tokens progressively in `src/components/ChatWidget/ChatWidget.js`
- [x] T051 [US6] Handle SSE error events gracefully in `src/components/ChatWidget/api.js`
- [x] T052 [US6] Add streaming indicator (typing dots) during response in `src/components/ChatWidget/ChatMessage.js`

**Checkpoint**: Streaming responses render progressively with good UX

---

## Phase 9: Polish & Deployment

**Purpose**: Production readiness, documentation, deployment

- [x] T053 [P] Create Dockerfile for backend deployment in `backend/Dockerfile`
- [x] T054 [P] Create docker-compose.yml for local full-stack testing in `docker-compose.yml`
- [x] T055 [P] Update .gitignore to exclude .env files but include .env.example
- [x] T056 [P] Add CORS production origin (habibullahdevv.github.io) in `backend/api/main.py`
- [ ] T057 Run quickstart.md validation: test local setup steps in `specs/001-docusaurus-safe-docs/quickstart.md`
- [ ] T058 Verify GitHub Pages compatibility: build frontend with production API URL
- [x] T059 Add logging for debugging (structured JSON logs) in `backend/api/main.py`
- [x] T060 Security review: verify no hardcoded credentials in any file

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phases 3-8 (User Stories) → Phase 9 (Polish)
                                     ↓
                        ┌────────────┼────────────┐
                        ↓            ↓            ↓
                   Phase 3      Phase 4      Phase 6
                   (US1: Q&A)   (US2: Select) (US4: Widget)
                        ↓            ↓            ↓
                   Phase 5      (merge)      Phase 7
                   (US3: SSE)                (US5: Text)
                                             ↓
                                        Phase 8
                                        (US6: Stream UI)
```

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 (General Q&A) | Phase 2 | US4 (Widget) |
| US2 (Selected Text) | US1 | US4 |
| US3 (SSE Backend) | US1 | US4, US5 |
| US4 (ChatWidget) | Phase 2 | US1, US2, US3 |
| US5 (Text Selection) | US4 | US2, US3 |
| US6 (SSE Frontend) | US3, US4 | - |

### Within Each User Story

1. Services before routes
2. Routes before integration
3. Backend before frontend (for full integration)

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T004, T005, T006 can run in parallel
**Phase 2 (Foundational)**: T011, T012 can run in parallel after T010
**Phase 6 (Widget)**: T034, T035 can run in parallel
**Phase 9 (Polish)**: T053, T054, T055, T056 can run in parallel

---

## Parallel Example: Backend MVP

```bash
# After Phase 2, launch backend user stories together:
# Developer A: US1 (General Q&A) - T014-T024
# Developer B: US2 (Selected Text) - T025-T028 (waits for T014)

# Frontend can start in parallel with backend:
# Developer C: US4 (ChatWidget) - T034-T042
```

---

## Implementation Strategy

### MVP First (Recommended)

1. **Phase 1**: Setup (T001-T006)
2. **Phase 2**: Foundational (T007-T013)
3. **Phase 3**: US1 General Q&A (T014-T024)
4. **Phase 4**: US2 Selected Text (T025-T028)
5. **Phase 6**: US4 ChatWidget (T034-T042)
6. **STOP and VALIDATE**: Full MVP works end-to-end
7. Deploy backend to Railway, frontend to GitHub Pages

### Full Feature Set

After MVP validation:
1. **Phase 5**: US3 SSE Backend (T029-T033)
2. **Phase 7**: US5 Text Selection (T043-T048)
3. **Phase 8**: US6 SSE Frontend (T049-T052)
4. **Phase 9**: Polish & Deploy (T053-T060)

### Quick Demo Path

For fastest working demo:
1. Complete T001-T024 (backend with basic chat)
2. Use curl/Postman to demo API
3. Add frontend later

---

## Summary

| Phase | User Story | Tasks | Parallel |
|-------|------------|-------|----------|
| 1 | Setup | T001-T006 | 4 |
| 2 | Foundational | T007-T013 | 2 |
| 3 | US1: General Q&A | T014-T024 | 0 |
| 4 | US2: Selected Text | T025-T028 | 0 |
| 5 | US3: SSE Backend | T029-T033 | 0 |
| 6 | US4: ChatWidget | T034-T042 | 2 |
| 7 | US5: Text Selection | T043-T048 | 0 |
| 8 | US6: SSE Frontend | T049-T052 | 0 |
| 9 | Polish | T053-T060 | 4 |
| **Total** | | **60 tasks** | **12 parallel** |

### MVP Scope (US1 + US2 + US4)

- Tasks: T001-T042 (42 tasks)
- Deliverable: Working chatbot with general Q&A, selected-text queries, and basic UI
- Deploy: Backend on Railway, Frontend on GitHub Pages

---

## Notes

- [P] = can run in parallel (different files, no dependencies)
- [USn] = belongs to User Story n for traceability
- Commit after each task or logical group
- Run `npm run build` to validate frontend changes
- Run `uvicorn api.main:app --reload` to test backend changes
- Quality constraint: AI must say "I don't know" if answer not in retrieved content
