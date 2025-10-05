from pydantic import BaseModel, Field, validator
from typing import Any, Dict, List, Optional

class AgentTask(BaseModel):
    agent_id: str = Field(..., min_length=3)
    query: str = Field(..., min_length=1)
    params: Optional[Dict[str, Any]] = None

class AgentResult(BaseModel):
    agent_id: str
    success: bool
    result: Any
    error: Optional[str] = None

class OrchestrationRequest(BaseModel):
    tasks: List[AgentTask]
    workflow_id: Optional[str] = None

class OrchestrationResponse(BaseModel):
    workflow_id: str
    results: List[AgentResult]
    elapsed: float
