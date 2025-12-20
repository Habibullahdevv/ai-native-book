"""
FastAPI backend for AI Native Book Chat - Hugging Face Spaces version
Simple request-response chat without database dependency
"""
import os
import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

import cohere
from qdrant_client import QdrantClient
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Native Book Chat API",
    description="RAG-powered chatbot for the Physical AI & Humanoid Robotics textbook",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize clients
_cohere_api_key = os.getenv("COHERE_API_KEY")
_qdrant_url = os.getenv("QDRANT_URL")
_qdrant_api_key = os.getenv("QDRANT_API_KEY")
_qdrant_collection = os.getenv("QDRANT_COLLECTION", "Ai_Native_Book")
_gemini_api_key = os.getenv("GEMINI_API_KEY")

# Cohere client for embeddings
_cohere_client = None
if _cohere_api_key:
    _cohere_client = cohere.Client(_cohere_api_key)
    logger.info("Cohere client initialized")
else:
    logger.warning("COHERE_API_KEY not set")

# Qdrant client for vector search
_qdrant = None
if _qdrant_url and _qdrant_api_key:
    _qdrant = QdrantClient(url=_qdrant_url, api_key=_qdrant_api_key)
    logger.info("Qdrant client initialized")
else:
    logger.warning("QDRANT_URL or QDRANT_API_KEY not set")

# Gemini client for chat
_gemini_model = None
if _gemini_api_key:
    genai.configure(api_key=_gemini_api_key)
    _gemini_model = genai.GenerativeModel("gemini-2.0-flash")
    logger.info("Gemini client initialized")
else:
    logger.warning("GEMINI_API_KEY not set")


# Pydantic models
class SimpleChatRequest(BaseModel):
    """Simple chat request without session management"""
    message: str = Field(..., min_length=1, max_length=10000, description="The user's message")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Optional selected text context")


class SimpleChatResponse(BaseModel):
    """Simple chat response"""
    id: str
    response: str
    sources: list[str] = []
    timestamp: datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    services: dict


def get_embedding(text: str) -> list[float]:
    """Get embedding vector from Cohere"""
    if not _cohere_client:
        raise RuntimeError("Cohere client not initialized")
    response = _cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]


def retrieve_context(query: str, limit: int = 5) -> list[dict]:
    """Retrieve relevant content from Qdrant"""
    if not _qdrant:
        raise RuntimeError("Qdrant client not initialized")

    embedding = get_embedding(query)
    result = _qdrant.query_points(
        collection_name=_qdrant_collection,
        query=embedding,
        limit=limit
    )

    contexts = []
    for point in result.points:
        contexts.append({
            "text": point.payload.get("text", ""),
            "url": point.payload.get("url", "")
        })
    return contexts


def generate_response(query: str, contexts: list[dict], selected_text: Optional[str] = None) -> str:
    """Generate response using Google Gemini"""
    if not _gemini_model:
        raise RuntimeError("Gemini client not initialized")

    # Build context string
    context_text = "\n\n".join([f"Source: {c['url']}\n{c['text']}" for c in contexts])

    # Build prompt
    system_instruction = "You are an AI tutor for the Physical AI & Humanoid Robotics textbook. Be concise and accurate."

    if selected_text:
        prompt = f"""{system_instruction}

The user has selected this text for context:
---
{selected_text}
---

Additional relevant content from the textbook:
---
{context_text}
---

User question: {query}

Answer based on the selected text and retrieved content. Be concise and accurate. If the answer is not in the provided content, say "I don't know based on the textbook content."
"""
    else:
        prompt = f"""{system_instruction}

Relevant content from the textbook:
---
{context_text}
---

User question: {query}

Answer based ONLY on the retrieved content above. Be concise and accurate. If the answer is not in the provided content, say "I don't know based on the textbook content."
"""

    # Generate with Gemini
    try:
        response = _gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini generation error: {e}")
        raise RuntimeError(f"Failed to generate response: {str(e)}")


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Native Book Chat API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        services={
            "cohere": "connected" if _cohere_client else "not_configured",
            "qdrant": "connected" if _qdrant else "not_configured",
            "gemini": "connected" if _gemini_model else "not_configured"
        }
    )


@app.post("/api/chat", response_model=SimpleChatResponse)
async def chat(request: SimpleChatRequest):
    """
    Send a message and get a RAG-powered response.

    The AI will search the Physical AI & Humanoid Robotics textbook
    and respond based on the relevant content found.
    """
    # Validate services are initialized
    if not _cohere_client:
        raise HTTPException(status_code=503, detail="Cohere service not configured")
    if not _qdrant:
        raise HTTPException(status_code=503, detail="Qdrant service not configured")
    if not _gemini_model:
        raise HTTPException(status_code=503, detail="Gemini service not configured")

    try:
        logger.info(f"Processing chat: {request.message[:50]}...")

        # Retrieve relevant context
        contexts = retrieve_context(request.message)
        sources = list(set([c["url"] for c in contexts if c["url"]]))

        # Generate response
        response_text = generate_response(
            query=request.message,
            contexts=contexts,
            selected_text=request.selected_text
        )

        logger.info("Chat response generated successfully")

        return SimpleChatResponse(
            id=str(uuid4()),
            response=response_text,
            sources=sources,
            timestamp=datetime.now(timezone.utc)
        )

    except RuntimeError as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


# For Hugging Face Spaces - run with: python app.py
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

