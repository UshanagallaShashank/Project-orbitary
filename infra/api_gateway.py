# api_gateway.py — FastAPI server that mirrors the Lambda handler locally

import os

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from agents.orchestrator import OrchestratorAgent

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Orbit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = OrchestratorAgent()


class OrbitRequest(BaseModel):
    session_id: str
    text: str


@app.get("/health")
def health():
    # Basic liveness check
    return {"status": "ok", "env": os.getenv("ORBIT_ENV", "development")}


@app.post("/intent")
def route_intent(req: OrbitRequest):
    # Main route — classifies intent and dispatches to agents
    result = orchestrator.run(req.text, {"session_id": req.session_id})

    return result
