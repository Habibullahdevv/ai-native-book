"""
Database connection pool for Neon Serverless Postgres
Uses asyncpg for async database operations
"""
import os
import asyncpg
from contextlib import asynccontextmanager
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def init_db_pool() -> Optional[asyncpg.Pool]:
    """Initialize the database connection pool"""
    global _pool

    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        logger.warning("NEON_DATABASE_URL not set - database features disabled")
        return None

    if _pool is None:
        logger.info("Creating database connection pool...")
        _pool = await asyncpg.create_pool(
            database_url,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        logger.info("Database connection pool created")

    return _pool


async def close_db_pool():
    """Close the database connection pool"""
    global _pool
    if _pool:
        logger.info("Closing database connection pool...")
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


async def get_pool() -> Optional[asyncpg.Pool]:
    """Get the current connection pool, initializing if needed"""
    global _pool
    if _pool is None:
        _pool = await init_db_pool()
    return _pool


@asynccontextmanager
async def get_connection():
    """Context manager for getting a database connection from the pool"""
    pool = await get_pool()
    if pool is None:
        raise RuntimeError("Database not configured - NEON_DATABASE_URL not set")
    async with pool.acquire() as conn:
        yield conn


async def execute_query(query: str, *args):
    """Execute a query and return the result"""
    async with get_connection() as conn:
        return await conn.fetch(query, *args)


async def execute_one(query: str, *args):
    """Execute a query and return a single row"""
    async with get_connection() as conn:
        return await conn.fetchrow(query, *args)


async def execute(query: str, *args):
    """Execute a query without returning results"""
    async with get_connection() as conn:
        return await conn.execute(query, *args)


async def check_connection() -> bool:
    """Check if database connection is healthy"""
    pool = await get_pool()
    if pool is None:
        return False  # DB not configured
    try:
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
