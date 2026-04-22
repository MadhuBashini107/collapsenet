from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Optional
import uvicorn

from environment import CollapseNetEnv, TASK_IDS

app = FastAPI(
    title="CollapseNet v2 — Fleet AI Aligned Generational Degradation Watchdog",
    description=(
        "An RL environment aligned with the Fleet AI sub-theme. "
        "3 domain-specific model agents (science, medicine, legal) collapse simultaneously. "
        "A watchdog agent monitors all 3, detects hallucinations, tracks generational degradation, "
        "allocates limited retraining budget, and provides structured oversight explanations."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

env = CollapseNetEnv()


class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"


class StepRequest(BaseModel):
    action: dict[str, Any]


class MCPRequest(BaseModel):
    jsonrpc: Optional[str] = "2.0"
    id: Optional[Any] = 1
    method: Optional[str] = None
    params: Optional[Any] = None


@app.get("/")
def root():
    return {
        "name": "CollapseNet v2",
        "version": "2.0.0",
        "sub_theme": "Fleet AI — Scalable Oversight",
        "description": (
            "3 domain AI agents collapse simultaneously across generations. "
            "A Fleet AI Watchdog monitors all 3, detects hallucinations, "
            "tracks per-agent collapse trends, allocates retraining budget, "
            "and produces structured oversight explanations scored by Mercor reward scaling."
        ),
        "tasks": TASK_IDS,
        "model_agents": ["science_model", "medicine_model", "legal_model"],
        "endpoints": ["/reset", "/step", "/state", "/tasks", "/health", "/metadata", "/schema", "/mcp", "/docs"],
        "themes": [
            "Theme #1 — Fleet AI Sub-theme: Scalable Oversight across 3 simultaneous AI agents",
            "Theme #4 — Self-Improvement: Watchdog improves collapse detection across generations",
            "Mercor Bonus: Reward scaling based on explanation quality and depth",
        ],
        "grader_dimensions": {
            "hallucination_detection": "30% — 10% per agent",
            "severity_assessment":     "20% — 6.7% per agent",
            "collapse_trend_tracking": "15% — 5% per agent",
            "retraining_allocation":   "20% — F1 score of budget decisions",
            "explanation_quality":     "15% — Mercor reward scaling by depth and coverage",
        },
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/metadata")
def metadata():
    return {
        "name": "CollapseNet v2",
        "description": (
            "3 domain AI agents collapse simultaneously across generations. "
            "A Fleet AI Watchdog monitors all 3, detects hallucinations, "
            "tracks per-agent collapse trends, allocates retraining budget, "
            "and produces structured oversight explanations scored by Mercor reward scaling."
        ),
        "version": "2.0.0",
        "sub_theme": "Fleet AI — Scalable Oversight",
        "tasks": TASK_IDS,
        "model_agents": ["science_model", "medicine_model", "legal_model"],
    }


@app.get("/schema")
def schema():
    return {
        "action": {
            "watchdog_flags": {
                "type": "dict",
                "description": "Per-agent hallucination flags e.g. {science_model: true, medicine_model: false, legal_model: true}",
                "keys": ["science_model", "medicine_model", "legal_model"]
            },
            "severity_scores": {
                "type": "dict",
                "description": "Per-agent severity score 0.0-1.0 e.g. {science_model: 0.8}",
                "keys": ["science_model", "medicine_model", "legal_model"]
            },
            "collapse_trends": {
                "type": "dict",
                "description": "Per-agent trend: stable, declining, critical",
                "keys": ["science_model", "medicine_model", "legal_model"]
            },
            "retraining_budget": {
                "type": "dict",
                "description": "Budget allocation per agent e.g. {science_model: 1, medicine_model: 0, legal_model: 0}",
                "keys": ["science_model", "medicine_model", "legal_model"]
            },
            "explanation": {
                "type": "string",
                "description": "Structured oversight explanation covering all 3 agents, trends, and retraining rationale"
            }
        },
        "observation": {
            "generation": {"type": "int", "description": "Current generation number"},
            "agent_outputs": {"type": "dict", "description": "Output text from each agent this generation"},
            "collapse_indicators": {"type": "dict", "description": "Per-agent collapse signal strength 0.0-1.0"},
            "retraining_budget_remaining": {"type": "int", "description": "Retraining tokens left"},
            "task_id": {"type": "string", "description": "Current task difficulty"}
        },
        "state": {
            "generation": {"type": "int", "description": "Current generation"},
            "done": {"type": "bool", "description": "Whether episode is complete"},
            "agents": {"type": "list", "description": "List of active agent names"},
            "task_id": {"type": "string", "description": "Current task ID"},
            "retraining_budget_remaining": {"type": "int", "description": "Tokens remaining"}
        }
    }


@app.post("/mcp")
def mcp(req: MCPRequest):
    return {
        "jsonrpc": "2.0",
        "id": req.id,
        "result": {
            "status": "ok",
            "environment": "CollapseNet v2",
            "capabilities": ["reset", "step", "state", "grade"]
        }
    }


@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            {
                "id": "easy",
                "description": "3 generations, mild collapse, 1 retraining token",
                "generations": 3,
                "retraining_budget": 1,
            },
            {
                "id": "medium",
                "description": "4 generations, moderate collapse across agents, 1 retraining token",
                "generations": 4,
                "retraining_budget": 1,
            },
            {
                "id": "hard",
                "description": "5 generations, severe multi-agent collapse, 2 retraining tokens — not enough to save everyone",
                "generations": 5,
                "retraining_budget": 2,
            },
        ]
    }


@app.post("/reset")
def reset(req: ResetRequest):
    task_id = req.task_id if req.task_id in TASK_IDS else "easy"
    return env.reset(task_id=task_id)


@app.post("/step")
def step(req: StepRequest):
    if not req.action:
        raise HTTPException(status_code=400, detail="action must not be empty")
    return env.step(req.action)


@app.get("/state")
def state():
    return env.state()

from fastapi.responses import FileResponse

@app.get("/dashboard")
def dashboard():
    return FileResponse("dashboard.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=False)