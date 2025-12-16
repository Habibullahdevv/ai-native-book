"""
RAG Agent for Physical AI & Humanoid Robotics Textbook
Uses OpenAI Agents SDK with Gemini 2.0 Flash and Qdrant vector search
"""
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled, function_tool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable tracing for cleaner output
set_tracing_disabled(disabled=True)

# Initialize Gemini provider via OpenAI-compatible API
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

# Initialize Cohere and Qdrant clients with environment variables
import cohere
from qdrant_client import QdrantClient

cohere_api_key = os.getenv("COHERE_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_collection = os.getenv("QDRANT_COLLECTION", "Ai_Native_Book")

if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")
if not qdrant_url:
    raise ValueError("QDRANT_URL environment variable is required")
if not qdrant_api_key:
    raise ValueError("QDRANT_API_KEY environment variable is required")

cohere_client = cohere.Client(cohere_api_key)
qdrant = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)


def get_embedding(text: str) -> list[float]:
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]


@function_tool
def retrieve(query: str) -> list[str]:
    """Retrieve relevant content from the textbook using semantic search"""
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name=qdrant_collection,
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in result.points]


# Default agent instructions
DEFAULT_INSTRUCTIONS = """
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
To answer the user question, first call the tool `retrieve` with the user query.
Use ONLY the returned content from `retrieve` to answer.
If the answer is not in the retrieved content, say "I don't know based on the textbook content."
Be concise and accurate.
"""

# Create the default agent
agent = Agent(
    name="BookAssistant",
    instructions=DEFAULT_INSTRUCTIONS,
    model=model,
    tools=[retrieve]
)


def create_agent_with_context(selected_text: str = None) -> Agent:
    """
    Create an agent with optional selected text context.
    If selected_text is provided, the agent will focus on that specific content.
    """
    if selected_text:
        instructions = f"""
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
    else:
        instructions = DEFAULT_INSTRUCTIONS

    return Agent(
        name="BookAssistant",
        instructions=instructions,
        model=model,
        tools=[retrieve]
    )


# Only run test when executed directly
if __name__ == "__main__":
    from agents import enable_verbose_stdout_logging
    enable_verbose_stdout_logging()

    result = Runner.run_sync(
        agent,
        input="what is physical ai?",
    )
    print(result.final_output)
