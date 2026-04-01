# pgvector_store.py — embed, store, and semantic search long-term memory

import os

from dotenv import load_dotenv

load_dotenv()

EMBED_DIM = 768


class PgVectorStore:

    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")

        self.port = int(os.getenv("POSTGRES_PORT", "5432"))

        self.db = os.getenv("POSTGRES_DB", "orbit")

        self.user = os.getenv("POSTGRES_USER", "orbit_user")

        self.password = os.getenv("POSTGRES_PASSWORD", "")

    def embed(self, text: str) -> list[float]:
        # Stub — replaced in F5 with real Gemini embedding call
        return [0.0] * EMBED_DIM

    def store(self, text: str, metadata: dict) -> bool:
        # Embeds and stores a fact with metadata
        return False

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        # Stub — replaced in F5 with real pgvector cosine search
        return []
