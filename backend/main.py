from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import agent, events, projects, schema, tasks
from src.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown events."""
    await init_db()
    yield


app = FastAPI(
    title="Kanban Orchestrator API",
    version="0.1.0",
    lifespan=lifespan,
)

# TODO: Production - Use Vite proxy instead of CORS regex
# Configure vite.config.ts: server.proxy = { '/api': 'http://backend:8000' }
# Then set allow_origins to specific production domains only
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:\d+",  # DEV ONLY: allows all localhost ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(agent.router)
app.include_router(events.router)
app.include_router(schema.router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
