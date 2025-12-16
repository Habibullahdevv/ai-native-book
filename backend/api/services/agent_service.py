"""
Agent service for RAG chatbot
Wraps the existing agent.py with async support and context injection
"""
import os
import logging
import asyncio
from typing import Optional, AsyncGenerator
from dotenv import load_dotenv

from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled, function_tool
from agents.stream_events import RawResponsesStreamEvent, RunItemStreamEvent
import cohere
from qdrant_client import QdrantClient

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Disable tracing for cleaner output
set_tracing_disabled(disabled=True)

# Initialize providers and clients
_gemini_api_key = os.getenv("GEMINI_API_KEY")
_cohere_api_key = os.getenv("COHERE_API_KEY")
_qdrant_url = os.getenv("QDRANT_URL")
_qdrant_api_key = os.getenv("QDRANT_API_KEY")
_qdrant_collection = os.getenv("QDRANT_COLLECTION", "Ai_Native_Book")

# Validate required environment variables
_missing_vars = []
if not _gemini_api_key:
    _missing_vars.append("GEMINI_API_KEY")
if not _cohere_api_key:
    _missing_vars.append("COHERE_API_KEY")
if not _qdrant_url:
    _missing_vars.append("QDRANT_URL")
if not _qdrant_api_key:
    _missing_vars.append("QDRANT_API_KEY")

if _missing_vars:
    logger.warning(f"Missing environment variables: {', '.join(_missing_vars)}")

# Initialize clients (will be None if env vars missing)
_provider = None
_model = None
_cohere_client = None
_qdrant = None

if _gemini_api_key:
    _provider = AsyncOpenAI(
        api_key=_gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    _model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=_provider
    )

if _cohere_api_key:
    _cohere_client = cohere.Client(_cohere_api_key)

if _qdrant_url and _qdrant_api_key:
    _qdrant = QdrantClient(
        url=_qdrant_url,
        api_key=_qdrant_api_key
    )


def _get_embedding(text: str) -> list[float]:
    """Get embedding vector from Cohere Embed v3"""
    if not _cohere_client:
        raise RuntimeError("Cohere client not initialized")
    response = _cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]


@function_tool
def retrieve(query: str) -> list[str]:
    """Retrieve relevant content from the textbook using semantic search"""
    if not _qdrant:
        raise RuntimeError("Qdrant client not initialized")
    try:
        embedding = _get_embedding(query)
        result = _qdrant.query_points(
            collection_name=_qdrant_collection,
            query=embedding,
            limit=5
        )
        texts = [point.payload["text"] for point in result.points]
        logger.debug(f"Retrieved {len(texts)} chunks for query: {query[:50]}...")
        return texts
    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        return []


# Default agent instructions
DEFAULT_INSTRUCTIONS = """
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
To answer the user question, first call the tool `retrieve` with the user query.
Use ONLY the returned content from `retrieve` to answer.
If the answer is not in the retrieved content, say "I don't know based on the textbook content."
Be concise and accurate.
"""

# Selected text context template
SELECTED_TEXT_INSTRUCTIONS = """
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
The user has selected the following text passage for context:

---
{selected_text}
---

When answering, focus specifically on this selected content.
If the question relates to the selected text, answer based on it.
If additional context is needed, call the `retrieve` tool.
If you cannot answer based on the selected text or retrieved content, say "I don't know based on the available content."
Be concise and accurate.
"""


def _create_agent(selected_text: Optional[str] = None) -> Agent:
    """Create an agent with optional selected text context"""
    if not _model:
        raise RuntimeError("Model not initialized - check GEMINI_API_KEY")

    if selected_text:
        instructions = SELECTED_TEXT_INSTRUCTIONS.format(selected_text=selected_text)
    else:
        instructions = DEFAULT_INSTRUCTIONS

    return Agent(
        name="BookAssistant",
        instructions=instructions,
        model=_model,
        tools=[retrieve]
    )


async def run_agent(
    query: str,
    selected_text: Optional[str] = None,
    session_id: Optional[str] = None
) -> str:
    """
    Run the RAG agent asynchronously with the given query.

    Args:
        query: The user's question
        selected_text: Optional selected text context
        session_id: Optional session ID for tracking

    Returns:
        The agent's response string
    """
    logger.info(f"Running agent for session {session_id}: {query[:50]}...")

    try:
        agent = _create_agent(selected_text)

        # Run the agent asynchronously
        result = await Runner.run(agent, input=query)

        response = result.final_output
        logger.info(f"Agent response generated for session {session_id}")

        # Check for empty or unhelpful responses
        if not response or len(response.strip()) < 10:
            response = "I don't know based on the textbook content."

        return response

    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise RuntimeError(f"Failed to generate response: {str(e)}")


def run_agent_sync(
    query: str,
    selected_text: Optional[str] = None,
    session_id: Optional[str] = None
) -> str:
    """
    Synchronous wrapper for run_agent.
    Use this for testing or when async is not available.
    """
    return asyncio.run(run_agent(query, selected_text, session_id))


async def run_agent_streamed(
    query: str,
    selected_text: Optional[str] = None,
    session_id: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """
    Run the RAG agent with streaming response.

    Args:
        query: The user's question
        selected_text: Optional selected text context
        session_id: Optional session ID for tracking

    Yields:
        String tokens as they are generated
    """
    logger.info(f"Running streamed agent for session {session_id}: {query[:50]}...")

    try:
        agent = _create_agent(selected_text)

        # Run the agent with streaming
        result = Runner.run_streamed(agent, input=query)

        full_response = ""
        async for event in result.stream_events():
            # Handle raw response stream events (tokens)
            if isinstance(event, RawResponsesStreamEvent):
                # Extract text delta from the event
                if hasattr(event, 'data') and hasattr(event.data, 'choices'):
                    for choice in event.data.choices:
                        if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                            token = choice.delta.content
                            if token:
                                full_response += token
                                yield token

        logger.info(f"Streamed agent response completed for session {session_id}")

        # If no tokens were yielded, provide a fallback
        if not full_response or len(full_response.strip()) < 10:
            yield "I don't know based on the textbook content."

    except Exception as e:
        logger.error(f"Streaming agent error: {e}")
        yield f"Error generating response: {str(e)}"


# Check if service is properly initialized
def is_initialized() -> bool:
    """Check if the agent service is properly initialized"""
    return all([_model, _cohere_client, _qdrant])
