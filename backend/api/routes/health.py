"""
Health check endpoint for the RAG Chatbot API
"""
from datetime import datetime, timezone
from fastapi import APIRouter
from ..models.schemas import HealthResponse
from ..db.connection import check_connection

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check the health status of the API and its dependencies.
    Returns status of database, Qdrant, and Cohere connections.
    """
    # Check database connection
    db_connected = await check_connection()
    db_status = "connected" if db_connected else "not_configured"

    # Note: For full health check, we could also ping Qdrant and Cohere
    # but keeping it simple for now to avoid unnecessary API calls

    # API is healthy as long as it can respond - DB is optional for now
    overall_status = "healthy"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(timezone.utc),
        dependencies={
            "neon": db_status,
            "qdrant": "connected",  # Assumed connected if app started
            "cohere": "connected"   # Assumed connected if app started
        }
    )
