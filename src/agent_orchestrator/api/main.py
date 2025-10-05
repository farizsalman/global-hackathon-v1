from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.agent_orchestrator.api.routers import agent_router, orchestrate_router, health_router
from src.agent_orchestrator.agents.research_agent import ResearchAgent
from src.agent_orchestrator.agents.analysis_agent import AnalysisAgent
from src.agent_orchestrator.agents.decision_agent import DecisionAgent

def create_app() -> FastAPI:
    app = FastAPI(title="Agent Orchestration API")

    # CORS config
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],           # For dev, restrict on prod!
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Error handling
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)}
        )

    # Include routers
    app.include_router(agent_router, prefix="/api/agents")
    app.include_router(orchestrate_router, prefix="/api/orchestrate")
    app.include_router(health_router, prefix="/api/health")

    return app

app = create_app()


# Dependency functions for FastAPI

from fastapi import Depends



#Instantiate orchestration classes globally

from src.agent_orchestrator.core.task_router import TaskRouter
from src.agent_orchestrator.core.agent_manager import AgentManager
from src.agent_orchestrator.core.workflow_engine import WorkflowEngine
from src.agent_orchestrator.core.state_manager import StateManager


# AGENTS mapping with proper keys for agents
AGENTS = {
    "research": ["research", "web", "search", "information"],
    "analysis": ["analysis", "data", "statistics", "insights"],
    "decision": ["decision", "recommendation", "synthesis"],
}

task_router = TaskRouter(agent_capabilities=AGENTS)
agent_manager = AgentManager()
agent_manager.registry["research"] = ResearchAgent()
agent_manager.registry["analysis"] = AnalysisAgent()
agent_manager.registry["decision"] = DecisionAgent()
state_manager = StateManager()
workflow_engine = WorkflowEngine(
    task_router=task_router,
    agent_manager=agent_manager,
    state_manager=state_manager
)


# Create FastAPI dependency functions

def get_task_router():
    return task_router

def get_agent_manager():
    return agent_manager

def get_state_manager():
    return state_manager

def get_workflow_engine():
    return workflow_engine
