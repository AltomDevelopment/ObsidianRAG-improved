import os
import uuid
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from qdrant_client.http import models as rest
from typing import List

# Load environment
load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "http://localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "documents"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def init_collection():
    if COLLECTION_NAME not in [col.name for col in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def embed_and_store(text: str, metadata: dict):
    embedding = model.encode(text).tolist()
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload=metadata
    )
    client.upsert(COLLECTION_NAME, [point])

def semantic_search(query: str, top_k: int = 5) -> List[dict]:
    query_vector = model.encode(query).tolist()
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    return [hit.payload for hit in search_result]