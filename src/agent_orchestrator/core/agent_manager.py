import asyncio
from typing import Dict, Any, Optional

class AgentManager:
    def __init__(self, db_ops=None):
        # In-memory (default): agent_id: {"status": "healthy"/"unreachable", "load": int}
        self.registry: Dict[str, Dict[str, Any]] = {}
        self.lock = asyncio.Lock()
        self.db_ops = db_ops

    # In-memory agent registration/status for backward compatibility
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

    async def get_least_loaded_agent(self) -> Optional[str]:
        async with self.lock:
            healthy = [
                (aid, self.registry[aid]["load"])
                for aid, entry in self.registry.items()
                if entry["status"] == "healthy"
            ]
            if not healthy:
                return None
            return min(healthy, key=lambda x: x[1])[0]

    # Shared public interface for load operations (works for both modes)
    async def increment_load(self, agent_id: str):
        if self.db_ops:
            await self.db_ops.increment_agent_load(agent_id)
        else:
            async with self.lock:
                if agent_id in self.registry:
                    self.registry[agent_id]["load"] += 1

    async def decrement_load(self, agent_id: str):
        if self.db_ops:
            await self.db_ops.decrement_agent_load(agent_id)
        else:
            async with self.lock:
                if agent_id in self.registry and self.registry[agent_id]["load"] > 0:
                    self.registry[agent_id]["load"] -= 1

    async def get_load(self, agent_id: str) -> int:
        if self.db_ops:
            return await self.db_ops.get_agent_load(agent_id)
        else:
            async with self.lock:
                if agent_id in self.registry:
                    return self.registry[agent_id]["load"]
                return 0
