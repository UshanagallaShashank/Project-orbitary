# lambda_handler.py — AWS Lambda entry point for all Orbit requests

import json

from agents.orchestrator import OrchestratorAgent

from memory.redis_store import RedisStore

orchestrator = OrchestratorAgent()

redis = RedisStore()


def handler(event, context):
    # Parse the incoming API Gateway request body
    body = json.loads(event.get("body", "{}"))

    session_id = body.get("session_id", "default")

    text = body.get("text", "")

    if not text:
        return _response(400, {"error": "text is required"})

    session_context = {"session_id": session_id}

    result = orchestrator.run(text, session_context)

    return _response(200, result)


def _response(status: int, body: dict) -> dict:
    # Wraps result in API Gateway-compatible format
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
