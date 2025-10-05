from typing import List
from src.agent_orchestrator.core.task_router import TaskRouter
from src.agent_orchestrator.core.agent_manager import AgentManager
from src.agent_orchestrator.api.models import OrchestrationRequest, OrchestrationResponse, AgentResult
from src.agent_orchestrator.core.state_manager import StateManager

class WorkflowEngine:
    def __init__(self, task_router: TaskRouter, agent_manager: AgentManager, state_manager: StateManager):
        self.task_router = task_router
        self.agent_manager = agent_manager
        self.state_manager = state_manager

    async def run_workflow(self, req: OrchestrationRequest) -> OrchestrationResponse:
        results: List[AgentResult] = []
        for task in req.tasks:
            agent_id = await self.task_router.route_task(task)
            await self.agent_manager.increment_load(agent_id)
            self.state_manager.set_status(task.agent_id, "started")
            try:
                # Assuming async agent execution (replace with real Hugging Face call/agent logic)
                # Example: result = await agents[agent_id].run(task)
                result_data = {"mock_output": "result"}  # Replace with real result!
                result = AgentResult(agent_id=agent_id, success=True, result=result_data)
                self.state_manager.set_status(task.agent_id, "finished")
            except Exception as e:
                result = AgentResult(agent_id=agent_id, success=False, result=None, error=str(e))
                self.state_manager.set_status(task.agent_id, "error")
            await self.agent_manager.decrement_load(agent_id)
            results.append(result)
        return OrchestrationResponse(
            workflow_id=req.workflow_id or "default_workflow",
            results=results,
            elapsed=0.0  # Set accurate timing in real usage
        )
