# pgvector_store.py — embed text via Gemini, store + search via pgvector

import os
import json

import psycopg2

from dotenv import load_dotenv

load_dotenv()

CREATE_TABLE_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS orbit_memory (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(768),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""


class PgVectorStore:

    def __init__(self):
        self._dsn = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
            "dbname": os.getenv("POSTGRES_DB", "orbit"),
            "user": os.getenv("POSTGRES_USER", "orbit_user"),
            "password": os.getenv("POSTGRES_PASSWORD", ""),
        }

        self._gemini_client = self._build_gemini()

    def _build_gemini(self):
        # Returns Gemini client if key present, else None
        api_key = os.getenv("GEMINI_API_KEY", "")

        if not api_key:
            return None

        from google import genai

        return genai.Client(api_key=api_key)

    def _connect(self):
        # Opens a fresh psycopg2 connection
        return psycopg2.connect(**self._dsn)

    def embed(self, text: str) -> list[float]:
        # Calls Gemini embedding model, returns 768-dim vector
        if not self._gemini_client:
            return [0.0] * 768

        result = self._gemini_client.models.embed_content(
            model="models/text-embedding-004",
            contents=text,
        )

        return result.embeddings[0].values

    def ensure_table(self):
        # Creates table and vector extension if they don't exist
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_SQL)

            conn.commit()

    def store(self, text: str, metadata: dict) -> bool:
        # Embeds text and inserts into pgvector table
        vector = self.embed(text)

        sql = "INSERT INTO orbit_memory (content, embedding, metadata) VALUES (%s, %s, %s)"

        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (text, vector, json.dumps(metadata)))

                conn.commit()

            return True

        except Exception:
            return False

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        # Embeds query, runs cosine similarity search, returns top_k results
        vector = self.embed(query)

        sql = """
            SELECT content, metadata, 1 - (embedding <=> %s::vector) AS score
            FROM orbit_memory
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """

        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (vector, vector, top_k))

                    rows = cur.fetchall()

            return [{"content": r[0], "metadata": r[1], "score": float(r[2])} for r in rows]

        except Exception:
            return []
