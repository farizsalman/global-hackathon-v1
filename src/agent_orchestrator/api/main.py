from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.agent_orchestrator.api.routers import agent_router, orchestrate_router, health_router

def create_app() -> FastAPI:
    app = FastAPI(title="Agent Orchestration API")

    # CORS config
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],           # For dev, restrict on prod!
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Error handling
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)}
        )

    # Include routers
    app.include_router(agent_router, prefix="/api/agents")
    app.include_router(orchestrate_router, prefix="/api/orchestrate")
    app.include_router(health_router, prefix="/api/health")

    return app

app = create_app()

