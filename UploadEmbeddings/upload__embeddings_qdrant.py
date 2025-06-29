import json
import time
import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Load model (outputs 768-dim vectors)
model = SentenceTransformer("all-mpnet-base-v2")
vector_size = model.get_sentence_embedding_dimension()

# Qdrant setup
qdrant_client = QdrantClient(
    url="https://bd06f3f0-fa1e-48d6-934d-7031533aa81d.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.oqlgLBRsHnfZsMcae-dVttc1e0CuYmjymPRC37PukEg"  # 🔐 Replace in production
)
collection_name = "obsidian_notebook_notes"

# Check if the collection exists
if qdrant_client.collection_exists(collection_name):
    qdrant_client.delete_collection(collection_name)

# Create collection fresh
qdrant_client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
)
# Load JSON data
json_file_path = "C:\\Users\\Administrator\\Desktop\\ObsidianAI\\UploadEmbeddings\\obsidian_notes_output.json"
with open(json_file_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Filter valid entries
valid_data = []
for i, item in enumerate(json_data):
    if isinstance(item, dict) and "text" in item and isinstance(item["text"], str):
        valid_data.append(item)
    else:
        print(f"⚠️ Skipping item at index {i}: {item}")

# Extract plain text list
texts = [item["text"] for item in valid_data]
print(f"Encoding {len(texts)} items...")

# Generate embeddings
embeddings = model.encode(texts, convert_to_numpy=True)

# Create Qdrant points
points = [
    PointStruct(
        id=item.get("id") or str(uuid.uuid4()),
        vector=vector.tolist(),
        payload={"text": item["text"]}
    )
    for item, vector in zip(valid_data, embeddings)
]

def batch(iterable, batch_size=25):
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]

# Upload to Qdrant
for i, batch_points in enumerate(batch(points, batch_size=25)):
    success = False
    for attempt in range(3):  # Try up to 3 times
        try:
            qdrant_client.upsert(collection_name=collection_name, points=batch_points)
            print(f"✅ Uploaded batch {i + 1}")
            success = True
            break
        except Exception as e:
            print(f"⚠️ Retry {attempt + 1} for batch {i + 1} due to: {e}")
            time.sleep(3)  # Wait a bit before retrying
    if not success:
        print(f"❌ Failed to upload batch {i + 1} after 3 attempts.")
