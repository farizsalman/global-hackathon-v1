from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId
from src.agent_orchestrator.db.models import (
    AgentTaskDocument, 
    AgentResultDocument, 
    WorkflowExecutionDocument,
    AgentStatusDocument,
    TaskStatus
)
from src.agent_orchestrator.api.models import AgentTask, AgentResult

class DatabaseOperations:
    
    async def create_task(self, task: AgentTask) -> AgentTaskDocument:
        """Create and store agent task"""
        task_doc = AgentTaskDocument(
            agent_id=task.agent_id,
            query=task.query,
            params=task.params
        )
        return await task_doc.insert()
    
    async def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status"""
        result = await AgentTaskDocument.find_one(
            AgentTaskDocument.id == PydanticObjectId(task_id)
        ).update({"$set": {"status": status, "updated_at": datetime.utcnow()}})
        return result.modified_count > 0
    
    async def store_agent_result(self, result: AgentResult, task_id: str) -> AgentResultDocument:
        """Store agent execution result"""
        result_doc = AgentResultDocument(
            task_id=task_id,
            agent_id=result.agent_id,
            success=result.success,
            result=result.result,
            error=result.error
        )
        return await result_doc.insert()
    
    async def create_workflow_execution(self, workflow_id: str) -> WorkflowExecutionDocument:
        """Create workflow execution record"""
        workflow_doc = WorkflowExecutionDocument(workflow_id=workflow_id)
        return await workflow_doc.insert()
    
    async def update_workflow_status(self, workflow_id: str, status: TaskStatus, 
                                   confidence_score: Optional[float] = None) -> bool:
        """Update workflow execution status"""
        update_data = {"status": status}
        if status == TaskStatus.COMPLETED:
            update_data["completed_at"] = datetime.utcnow()
        if confidence_score:
            update_data["confidence_score"] = confidence_score
            
        result = await WorkflowExecutionDocument.find_one(
            WorkflowExecutionDocument.workflow_id == workflow_id
        ).update({"$set": update_data})
        return result.modified_count > 0
    
    async def get_workflow_history(self, limit: int = 50) -> List[WorkflowExecutionDocument]:
        """Get recent workflow executions"""
        return await WorkflowExecutionDocument.find().sort(-WorkflowExecutionDocument.started_at).limit(limit).to_list()
    
    async def get_agent_load(self, agent_id: str) -> int:
        """Get current agent load"""
        status = await AgentStatusDocument.find_one(AgentStatusDocument.agent_id == agent_id)
        return status.current_load if status else 0
    
    async def increment_agent_load(self, agent_id: str) -> bool:
        """Increment agent load"""
        result = await AgentStatusDocument.find_one(
            AgentStatusDocument.agent_id == agent_id
        ).update({"$inc": {"current_load": 1}, "$set": {"last_updated": datetime.utcnow()}})
        return result.modified_count > 0
    
    async def decrement_agent_load(self, agent_id: str) -> bool:
        """Decrement agent load"""
        result = await AgentStatusDocument.find_one(
            AgentStatusDocument.agent_id == agent_id
        ).update({"$inc": {"current_load": -1}, "$set": {"last_updated": datetime.utcnow()}})
        return result.modified_count > 0

# Global database operations instance
db_ops = DatabaseOperations()
