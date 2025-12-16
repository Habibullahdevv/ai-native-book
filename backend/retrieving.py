"""
Retrieval utility for RAG chatbot
Uses Cohere embeddings and Qdrant vector search
"""
import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

# Initialize clients from environment variables
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


def retrieve(query: str, limit: int = 5) -> list[str]:
    """Retrieve relevant content from the textbook collection"""
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name=qdrant_collection,
        query=embedding,
        limit=limit
    )
    return [point.payload["text"] for point in result.points]


# Only run test when executed directly
if __name__ == "__main__":
    print(retrieve("What data do you have?"))
