---
title: AI Native Book Chat API
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# AI Native Book Chat API

RAG-powered chatbot API for the Physical AI & Humanoid Robotics textbook.

## API Endpoints

- `GET /` - API info
- `GET /api/health` - Health check
- `POST /api/chat` - Send a message and get a response

## Chat Request

```json
{
  "message": "What is Physical AI?",
  "selected_text": "optional context from the book"
}
```

## Chat Response

```json
{
  "id": "uuid",
  "response": "Physical AI refers to...",
  "sources": ["https://..."],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Environment Variables

- `COHERE_API_KEY` - Cohere API key for embeddings
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `QDRANT_COLLECTION` - Collection name (default: Ai_Native_Book)
- `GEMINI_API_KEY` - Google Gemini API key
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)
