"""
FastAPI application entry point for RAG Chatbot API
"""
import os
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .db.connection import init_db_pool, close_db_pool
from .models.schemas import ErrorResponse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown"""
    # Startup
    logger.info("Starting RAG Chatbot API...")
    try:
        await init_db_pool()
        logger.info("Database pool initialized")
    except Exception as e:
        logger.warning(f"Could not initialize database pool: {e}")
    yield
    # Shutdown
    logger.info("Shutting down RAG Chatbot API...")
    await close_db_pool()
    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="AI Native Book Chat API",
    description="RAG-powered chatbot for the Physical AI & Humanoid Robotics textbook",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# Custom exception handlers

class RAGServiceError(Exception):
    """Custom exception for RAG service errors"""
    def __init__(self, message: str, user_message: str, retry: bool = True):
        self.message = message
        self.user_message = user_message
        self.retry = retry
        super().__init__(self.message)


@app.exception_handler(RAGServiceError)
async def rag_error_handler(request: Request, exc: RAGServiceError):
    """Handle RAG service errors"""
    logger.error(f"RAG Error: {exc.message}")
    return JSONResponse(
        status_code=503,
        content={"error": exc.user_message, "retry": exc.retry}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "retry": False}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.exception(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred", "retry": True}
    )


# Import and register routes
from .routes import health

app.include_router(health.router, prefix="/api", tags=["Health"])

# Only register DB-dependent routes if database is configured
if os.getenv("NEON_DATABASE_URL"):
    from .routes import sessions, chat
    app.include_router(sessions.router, prefix="/api", tags=["Sessions"])
    app.include_router(chat.router, prefix="/api", tags=["Chat"])
    logger.info("Database routes enabled")
else:
    logger.warning("Database routes disabled - NEON_DATABASE_URL not set")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Native Book Chat API",
        "version": "1.0.0",
        "docs": "/docs"
    }
