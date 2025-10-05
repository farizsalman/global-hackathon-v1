from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.agent_orchestrator.api.routers import agent_router, orchestrate_router, health_router

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


from src.agent_orchestrator.core.task_router import TaskRouter
from src.agent_orchestrator.core.agent_manager import AgentManager
from src.agent_orchestrator.core.workflow_engine import WorkflowEngine
from src.agent_orchestrator.core.state_manager import StateManager

# Example agent capability mapping (for TaskRouter)
AGENTS = {
    "agent1": ["text", "nlp", "classify"],
    "agent2": ["image", "vision", "detect"],
}

# Single instances (for simplicity); use for DI
task_router = TaskRouter(agent_capabilities=AGENTS)
agent_manager = AgentManager()
state_manager = StateManager()
workflow_engine = WorkflowEngine(
    task_router=task_router,
    agent_manager=agent_manager,
    state_manager=state_manager
)


# Dependency functions for FastAPI

from fastapi import Depends

def get_workflow_engine():
    return workflow_engine





#Instantiate orchestration classes globally

from src.agent_orchestrator.core.task_router import TaskRouter
from src.agent_orchestrator.core.agent_manager import AgentManager
from src.agent_orchestrator.core.workflow_engine import WorkflowEngine
from src.agent_orchestrator.core.state_manager import StateManager

# Example ability config
AGENTS = {
    "agent1": ["text", "nlp", "research"],
    "agent2": ["image", "vision"],
}

task_router = TaskRouter(agent_capabilities=AGENTS)
agent_manager = AgentManager()
state_manager = StateManager()
workflow_engine = WorkflowEngine(task_router, agent_manager, state_manager)

# Create FastAPI dependency functions

def get_task_router():
    return task_router

def get_agent_manager():
    return agent_manager

def get_state_manager():
    return state_manager

def get_workflow_engine():
    return workflow_engine
