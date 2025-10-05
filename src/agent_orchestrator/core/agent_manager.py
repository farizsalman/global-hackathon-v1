import asyncio
from typing import Dict, Optional

class AgentManager:
    def __init__(self):
        # agent_id: {"status": "healthy"/"unreachable", "load": int}
        self.registry: Dict[str, Dict[str, Any]] = {}
        self.lock = asyncio.Lock()

    async def register_agent(self, agent_id: str):
        async with self.lock:
            self.registry[agent_id] = {"status": "healthy", "load": 0}

    async def update_status(self, agent_id: str, status: str):
        async with self.lock:
            if agent_id in self.registry:
                self.registry[agent_id]["status"] = status

    async def get_healthy_agents(self):
        async with self.lock:
            return [aid for aid, entry in self.registry.items() if entry["status"] == "healthy"]

    async def increment_load(self, agent_id: str):
        async with self.lock:
            if agent_id in self.registry:
                self.registry[agent_id]["load"] += 1

    async def decrement_load(self, agent_id: str):
        async with self.lock:
            if agent_id in self.registry and self.registry[agent_id]["load"] > 0:
                self.registry[agent_id]["load"] -= 1

    async def get_least_loaded_agent(self) -> Optional[str]:
        async with self.lock:
            healthy = [(aid, self.registry[aid]["load"]) for aid, entry in self.registry.items() if entry["status"] == "healthy"]
            if not healthy:
                return None
            return min(healthy, key=lambda x: x[1])[0]
