"""
ChatterBox API — Ponto de entrada da aplicação FastAPI.

Estado: PLACEHOLDER (boilerplate)
Spec de referência: specs/001-iniciar-conversa, specs/002-ia-responde-com-objetivo

TODO (seguir a ordem das tasks em specs/001/tasks.md e specs/002/tasks.md):
  - Implementar models, repositories e services (TDD)
  - Registrar routers de conversas (ConversationController)
  - Registrar endpoint WebSocket (spec 003, opcional)
  - Configurar lifespan para conexão com MongoDB
"""

from fastapi import FastAPI

# TODO: importar e registrar routers quando implementados
# from src.controllers.conversation_controller import router as conversation_router

app = FastAPI(
    title="ChatterBox 2.0 API",
    description="POC — Conversas com IA (objetivo: convencer que a Terra é plana).",
    version="0.1.0",
)

# TODO: app.include_router(conversation_router, prefix="/conversations", tags=["conversations"])
# TODO: registrar endpoint WS: app.add_api_websocket_route(...)
# TODO: lifespan com conexão Motor ao MongoDB


@app.get("/health", tags=["infra"])
async def health() -> dict:
    """Health check — confirma que a API está no ar."""
    return {"status": "ok"}
