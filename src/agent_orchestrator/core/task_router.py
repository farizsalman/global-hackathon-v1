from typing import List, Dict, Any
from src.agent_orchestrator.api.models import AgentTask

class TaskRouter:
    def __init__(self, agent_capabilities: Dict[str, List[str]]):
        """
        agent_capabilities: {agent_id: [list of capabilities/keywords]}
        """
        self.agent_capabilities = agent_capabilities

    async def route_task(self, task: AgentTask) -> str:
        """
        Analyze the task and return the best agent_id.
        """
        for agent_id, capabilities in self.agent_capabilities.items():
            if any(keyword in task.query.lower() for keyword in capabilities):
                return agent_id
        # Default: first agent if no match
        return next(iter(self.agent_capabilities.keys()))
