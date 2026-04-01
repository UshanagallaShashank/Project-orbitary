# redis_store.py — session key-value store with TTL via Redis

import os
import json

import redis

from dotenv import load_dotenv

load_dotenv()


class RedisStore:

    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")

        self.port = int(os.getenv("REDIS_PORT", "6379"))

        self.ttl = int(os.getenv("REDIS_TTL_SECONDS", "3600"))

        self._client = redis.Redis(host=self.host, port=self.port, decode_responses=True)

    def _key(self, session_id: str, key: str) -> str:
        # Namespaces all keys under orbit:<session>:<key>
        return f"orbit:{session_id}:{key}"

    def read(self, session_id: str, key: str):
        # Returns parsed value or None if key missing
        raw = self._client.get(self._key(session_id, key))

        return json.loads(raw) if raw is not None else None

    def write(self, session_id: str, key: str, value) -> bool:
        # Writes value as JSON with TTL, returns True on success
        result = self._client.setex(self._key(session_id, key), self.ttl, json.dumps(value))

        return bool(result)

    def delete(self, session_id: str, key: str) -> bool:
        # Deletes key, returns True if it existed
        return bool(self._client.delete(self._key(session_id, key)))

    def get_all_keys(self, session_id: str) -> list[str]:
        # Returns all short key names for a session (strips namespace prefix)
        prefix = f"orbit:{session_id}:"

        full_keys = self._client.keys(f"{prefix}*")

        return [k.replace(prefix, "") for k in full_keys]
