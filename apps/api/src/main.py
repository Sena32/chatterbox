"""ChatterBox API — Ponto de entrada da aplicação FastAPI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from src.controllers.conversation_controller import router as conversation_router
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(settings.mongo_uri)
    app.state.mongo_client = client
    app.state.db = client[settings.mongo_db_name]
    yield
    client.close()


app = FastAPI(
    title="ChatterBox 2.0 API",
    description="POC — Conversas com IA (objetivo: convencer que a Terra é plana).",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(
    conversation_router,
    prefix="/conversations",
    tags=["conversations"],
)


@app.get("/health", tags=["infra"])
async def health() -> dict:
    """Health check — confirma que a API está no ar."""
    return {"status": "ok"}
