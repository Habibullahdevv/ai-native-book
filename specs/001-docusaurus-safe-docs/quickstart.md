# Quickstart Guide: RAG Chatbot Development

**Feature**: `001-docusaurus-safe-docs` | **Date**: 2025-12-16 | **Phase**: 1

## Overview

This guide covers local development setup for both backend (FastAPI) and frontend (Docusaurus) components.

---

## Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| Python | 3.13+ | [python.org](https://python.org/) |
| Git | 2.x | [git-scm.com](https://git-scm.com/) |
| uv (optional) | 0.4+ | `pip install uv` |

### Required Accounts

| Service | Purpose | Signup |
|---------|---------|--------|
| Neon | Chat persistence | [neon.tech](https://neon.tech/) |
| Cohere | Embeddings | [cohere.com](https://cohere.com/) |
| Qdrant Cloud | Vector storage | [qdrant.tech](https://qdrant.tech/) |
| Google AI Studio | Gemini API | [aistudio.google.com](https://aistudio.google.com/) |

---

## 1. Clone Repository

```bash
git clone https://github.com/Habibullahdevv/ai-native-book.git
cd ai-native-book
git checkout 001-docusaurus-safe-docs
```

---

## 2. Backend Setup

### 2.1 Create Virtual Environment

```bash
cd backend

# Option A: Using uv (recommended)
uv venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Option B: Using standard venv
python -m venv .venv
source .venv/bin/activate
```

### 2.2 Install Dependencies

```bash
# Option A: Using uv
uv pip install -r requirements.txt

# Option B: Using pip
pip install -r requirements.txt
```

### 2.3 Configure Environment Variables

Create `.env` file in `backend/`:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# LLM Provider (Gemini via OpenAI-compatible API)
GEMINI_API_KEY=your_gemini_api_key_here

# Cohere Embeddings
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Cloud
QDRANT_URL=https://your-cluster-id.region.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION=Ai_Native_Book

# Neon Postgres
NEON_DATABASE_URL=postgres://user:password@ep-xyz-pooler.region.aws.neon.tech/dbname?sslmode=require

# CORS (for local development)
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Optional: Debug mode
DEBUG=true
```

### 2.4 Initialize Database

Run the schema migration against Neon:

```bash
# Using psql (if installed)
psql "$NEON_DATABASE_URL" -f api/db/schema.sql

# Or via Python script
python -c "
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    conn = await asyncpg.connect(os.getenv('NEON_DATABASE_URL'))
    with open('api/db/schema.sql', 'r') as f:
        await conn.execute(f.read())
    await conn.close()
    print('Database initialized!')

asyncio.run(init_db())
"
```

### 2.5 Start Backend Server

```bash
# Development mode with auto-reload
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2.6 Verify Backend

```bash
# Health check
curl http://localhost:8000/api/health

# Create session
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{}'

# Send message (replace SESSION_ID)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION_ID",
    "message": "What is Physical AI?"
  }'
```

---

## 3. Frontend Setup

### 3.1 Install Dependencies

```bash
# From repository root
npm install
```

### 3.2 Configure Frontend Environment

Create `.env.local` in repository root:

```env
# Backend API URL
REACT_APP_API_URL=http://localhost:8000
```

### 3.3 Start Development Server

```bash
npm run start
```

The site will be available at `http://localhost:3000`.

### 3.4 Build for Production

```bash
npm run build
npm run serve  # Preview production build
```

---

## 4. Development Workflow

### Backend Changes

```bash
# Run tests
cd backend
pytest

# Type checking (if using mypy)
mypy api/

# Format code
black api/
isort api/
```

### Frontend Changes

```bash
# Run linter
npm run lint

# Type checking (if using TypeScript)
npm run typecheck

# Build and test
npm run build
```

### Full Stack Testing

1. Start backend: `uvicorn api.main:app --reload`
2. Start frontend: `npm run start`
3. Open browser: `http://localhost:3000`
4. Navigate to any docs page
5. Select text → click "Ask AI" button
6. Test chat widget

---

## 5. Common Issues

### Issue: CORS errors in browser

**Solution**: Verify `CORS_ORIGINS` in `.env` includes `http://localhost:3000`

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Issue: Qdrant connection failed

**Solution**: Check Qdrant Cloud dashboard for correct URL and API key

```bash
# Test connection
curl -H "api-key: YOUR_KEY" \
  https://your-cluster.cloud.qdrant.io:6333/collections
```

### Issue: Neon connection timeout

**Solution**: Use the pooled connection string (includes `-pooler`)

```
# Correct
postgres://user:pass@ep-xyz-pooler.region.aws.neon.tech/db

# Incorrect (direct connection)
postgres://user:pass@ep-xyz.region.aws.neon.tech/db
```

### Issue: Module not found errors

**Solution**: Ensure virtual environment is activated

```bash
# Check Python path
which python  # Should show .venv/bin/python

# Reinstall if needed
pip install -e .
```

### Issue: Port already in use

**Solution**: Kill existing process or use different port

```bash
# Find process on port 8000
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 PID

# Or use different port
uvicorn api.main:app --port 8001
```

---

## 6. Project Structure Reference

```
ai-native-book/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI entry point
│   │   ├── routes/
│   │   │   └── chat.py       # Chat endpoints
│   │   ├── services/
│   │   │   ├── agent_service.py
│   │   │   └── session_service.py
│   │   ├── models/
│   │   │   └── schemas.py    # Pydantic models
│   │   └── db/
│   │       ├── connection.py
│   │       └── schema.sql
│   ├── agent.py              # RAG agent (existing)
│   ├── main.py               # Ingestion (existing)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── src/
│   ├── components/
│   │   └── ChatWidget/
│   │       ├── index.js
│   │       ├── ChatWidget.js
│   │       └── ChatWidget.module.css
│   ├── clientModules/
│   │   └── chatWidget.js
│   └── css/
│       └── custom.css
│
├── docs/                     # Book content
├── docusaurus.config.js
├── package.json
└── .env.local
```

---

## 7. API Documentation

Once the backend is running, access interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 8. Useful Commands

```bash
# Backend
uvicorn api.main:app --reload           # Dev server
pytest                                   # Run tests
python main.py                          # Re-ingest book content

# Frontend
npm run start                           # Dev server
npm run build                           # Production build
npm run serve                           # Preview build
npm run clear                           # Clear cache

# Git
git status
git diff
git add .
git commit -m "feat: add chat widget"
```

---

## Next Steps

After local setup is complete:

1. Run `/sp.tasks` to generate implementation task list
2. Follow tasks in order (dependencies are marked)
3. Test each component before moving to next
4. Deploy backend to Railway/Cloud Run
5. Update frontend with production API URL
6. Deploy frontend to GitHub Pages

---

## Support

- **GitHub Issues**: [Report bugs](https://github.com/Habibullahdevv/ai-native-book/issues)
- **Documentation**: See `specs/001-docusaurus-safe-docs/` for detailed plans
