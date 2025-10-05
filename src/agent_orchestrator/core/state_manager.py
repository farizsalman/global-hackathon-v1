import asyncio
from typing import Dict

class StateManager:
    def __init__(self):
        self.status: Dict[str, str] = {}
        self.lock = asyncio.Lock()

    def set_status(self, task_id: str, status: str):
        self.status[task_id] = status

    def get_status(self, task_id: str) -> str:
        return self.status.get(task_id, "unknown")
