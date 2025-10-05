from fastapi import APIRouter, Depends
from src.agent_orchestrator.api.models import OrchestrationRequest, OrchestrationResponse, AgentResult
from src.agent_orchestrator.services.huggingface_service import HuggingFaceService
import time

orchestrate_router = APIRouter()

async def get_hf_service():
    return HuggingFaceService()

@orchestrate_router.post("/", response_model=OrchestrationResponse)
async def orchestrate(
    req: OrchestrationRequest,
    hf_service: HuggingFaceService = Depends(get_hf_service)
):
    start = time.time()
    results = []
    for task in req.tasks:
        try:
            inference = await hf_service.query_model("bert-base-uncased", task.query)
            results.append(AgentResult(agent_id=task.agent_id, success=True, result=inference))
        except Exception as e:
            results.append(AgentResult(agent_id=task.agent_id, success=False, result=None, error=str(e)))
    elapsed = time.time() - start
    return OrchestrationResponse(
        workflow_id=req.workflow_id or "default_workflow",
        results=results,
        elapsed=elapsed
    )



# 

from fastapi import APIRouter, Depends
from src.agent_orchestrator.api.models import OrchestrationRequest, OrchestrationResponse
from src.agent_orchestrator.core.workflow_engine import WorkflowEngine

orchestrate_router = APIRouter()

@orchestrate_router.post("/", response_model=OrchestrationResponse)
async def orchestrate(
    req: OrchestrationRequest,
    engine: WorkflowEngine = Depends(get_workflow_engine)  # DI here!
):
    return await engine.run_workflow(req)



# Inject into route handlers using FastAPI

from fastapi import APIRouter, Depends
from src.agent_orchestrator.api.models import OrchestrationRequest, OrchestrationResponse
from src.agent_orchestrator.core.workflow_engine import WorkflowEngine

orchestrate_router = APIRouter()

@orchestrate_router.post("/", response_model=OrchestrationResponse)
async def orchestrate(
    req: OrchestrationRequest,
    engine: WorkflowEngine = Depends(get_workflow_engine)  # <-- Dependency injection!
):
    return await engine.run_workflow(req)
