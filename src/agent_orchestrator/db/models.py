from beanie import Document, Indexed
from pydantic import Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentTaskDocument(Document):
    agent_id: Indexed(str)
    query: str
    params: Optional[Dict[str, Any]] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "agent_tasks"
        indexes = [
            [("agent_id", 1), ("status", 1)],
            [("created_at", -1)]
        ]

class AgentResultDocument(Document):
    task_id: Indexed(str)
    agent_id: Indexed(str)
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    confidence_score: Optional[float] = None
    execution_time: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "agent_results"
        indexes = [
            [("task_id", 1)],
            [("agent_id", 1), ("created_at", -1)]
        ]

class WorkflowExecutionDocument(Document):
    workflow_id: Indexed(str)
    status: TaskStatus = TaskStatus.PENDING
    agent_results: List[str] = []  # AgentResult IDs
    human_review_required: bool = False
    confidence_score: Optional[float] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    class Settings:
        name = "workflow_executions"
        indexes = [
            [("workflow_id", 1)],
            [("status", 1), ("started_at", -1)]
        ]

class AgentStatusDocument(Document):
    agent_id: Indexed(str)
    current_load: int = 0
    max_load: int = 10
    status: str = "active"
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "agent_status"
        indexes = [
            [("agent_id", 1)]
        ]
