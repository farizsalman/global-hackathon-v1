from fastapi import APIRouter, Depends, HTTPException
from src.agent_orchestrator.api.models import AgentTask, AgentResult
from src.agent_orchestrator.services.huggingface_service import HuggingFaceService

agent_router = APIRouter()

async def get_hf_service():
    return HuggingFaceService()

@agent_router.post("/", response_model=AgentResult)
async def run_agent(
    task: AgentTask,
    hf_service: HuggingFaceService = Depends(get_hf_service)
):
    try:
        inference = await hf_service.query_model("bert-base-uncased", task.query)
        return AgentResult(agent_id=task.agent_id, success=True, result=inference)
    except Exception as e:
        return AgentResult(agent_id=task.agent_id, success=False, result=None, error=str(e))
