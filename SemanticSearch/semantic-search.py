import openai
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Initialize OpenAI API key
openai.api_key = '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'

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url='https://bd06f3f0-fa1e-48d6-934d-7031533aa81d.europe-west3-0.gcp.cloud.qdrant.io:6333',
    api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.oqlgLBRsHnfZsMcae-dVttc1e0CuYmjymPRC37PukEg'  # replace if needed
)

# Define collection
collection_name = 'obsidian_notebook_notes'

# Function to query Qdrant
def query_qdrant(query_vector, top_k=5):
    response = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    return response

# Function to embed text and query Qdrant
def query_openai_with_qdrant(query, collection_name):
    # Generate embedding
    st_model = SentenceTransformer("all-mpnet-base-v2")
    embedding_vector = st_model.encode(query).tolist()

    # Query Qdrant
    results = query_qdrant(query_vector=embedding_vector)
    return results

# Example usage
query_text = "What are my views on life?"
response = query_openai_with_qdrant(query_text, collection_name)

# Print results
for hit in response:
    print(hit)

