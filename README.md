# ObsidianAI - RAG-Enhanced Semantic Search

This project provides a Django-based document uploader and viewer with integrated semantic search powered by a local embedding model and Qdrant vector DB.

## Features
- Upload PDF or text documents
- Automatically extract content
- Generate vector embeddings using `all-MiniLM-L6-v2`
- Store vectors in Qdrant
- Query with semantic search using RAG

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

## Running

```bash
cd ObsidianDjangoApp/obsidian-django-app
python manage.py migrate
python manage.py runserver
```

Access the app at: `http://127.0.0.1:8000`

## Notes
- You must have Qdrant running (use Docker or cloud)
- You may optionally adapt this to HuggingFace API or OpenAI