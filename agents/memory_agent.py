# memory_agent.py — Redis session store + pgvector semantic long-term memory

import os

from memory.redis_store import RedisStore

from dotenv import load_dotenv

load_dotenv()


class MemoryAgent:

    def __init__(self):
        self._redis = RedisStore()

    def read(self, session_id: str, key: str):
        # Reads a session key from Redis
        return self._redis.read(session_id, key)

    def write(self, session_id: str, key: str, value) -> bool:
        # Writes a session key to Redis with TTL
        return self._redis.write(session_id, key, value)

    def delete(self, session_id: str, key: str) -> bool:
        # Deletes a session key from Redis
        return self._redis.delete(session_id, key)

    def get_all_keys(self, session_id: str) -> list[str]:
        # Returns all keys for dashboard memory panel
        return self._redis.get_all_keys(session_id)

    def semantic_search(self, query: str, top_k: int = 3) -> list[dict]:
        # Stub — wired to pgvector in F5
        return []

    def run(self, action: str, context: dict) -> dict:
        # Dispatches read / write / delete / search
        if action == "read":
            return {"value": self.read(context["session_id"], context["key"])}

        if action == "write":
            return {"ok": self.write(context["session_id"], context["key"], context["value"])}

        if action == "delete":
            return {"ok": self.delete(context["session_id"], context["key"])}

        if action == "search":
            return {"results": self.semantic_search(context.get("query", ""))}

        return {"error": "unknown action"}
