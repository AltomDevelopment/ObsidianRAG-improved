# rag_pipeline.py
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

# Initialize FAISS vector store once
EMBED_MODEL = OpenAIEmbeddings(
    model="text-embedding-ada-002", api_key=os.getenv("OPENAI_API_KEY")
)
splitter = CharacterTextSplitter(chunk_size=1000, overlap=200)
db = FAISS(embedding_function=EMBED_MODEL)

def embed_and_store(docs: list[tuple[str, str, dict]]):
    """
    docs: list of (id, text, metadata dict)
    Splits and indexes chunks into FAISS store.
    """
    lc_docs = []
    for _id, txt, meta in docs:
        chunks = splitter.split_text(txt)
        for chunk in chunks:
            lc_docs.append(Document(page_content=chunk, metadata={"id": _id, **meta}))
    db.add_documents(lc_docs)
    return {"indexed_chunks": len(lc_docs)}

def semantic_search(query: str, k: int = 5):
    """
    Returns top k similar chunks for a given query.
    """
    docs = db.similarity_search(query, k=k)
    return [{"id": doc.metadata.get("id"), "text": doc.page_content, "metadata": doc.metadata} for doc in docs]
