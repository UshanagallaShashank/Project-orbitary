# redis_store.py — session key-value store with TTL

import os

from dotenv import load_dotenv

load_dotenv()


class RedisStore:

    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")

        self.port = int(os.getenv("REDIS_PORT", "6379"))

        self.ttl = int(os.getenv("REDIS_TTL_SECONDS", "3600"))

        self._client = None

    def _key(self, session_id: str, key: str) -> str:
        # Namespaces keys by session
        return f"orbit:{session_id}:{key}"

    def read(self, session_id: str, key: str):
        # Stub — replaced in F4
        return None

    def write(self, session_id: str, key: str, value: str) -> bool:
        # Stub — replaced in F4
        return False

    def delete(self, session_id: str, key: str) -> bool:
        # Stub — replaced in F4
        return False

    def get_all_keys(self, session_id: str) -> list[str]:
        # Returns all keys for a session — used by dashboard memory panel
        return []
