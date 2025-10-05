from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import os

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
database = Database()

async def get_database_client() -> AsyncIOMotorClient:
    return database.client

async def connect_to_mongo():
    """Create database connection"""
    database.client = AsyncIOMotorClient(
        os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    )
    
async def close_mongo_connection():
    """Close database connection"""
    if database.client:
        database.client.close()

async def init_database():
    """Initialize Beanie with document models"""
    from src.agent_orchestrator.db.models import (
        AgentTaskDocument, 
        AgentResultDocument, 
        WorkflowExecutionDocument,
        AgentStatusDocument
    )
    
    await init_beanie(
        database=database.client.agent_orchestrator,
        document_models=[
            AgentTaskDocument,
            AgentResultDocument, 
            WorkflowExecutionDocument,
            AgentStatusDocument
        ]
    )
