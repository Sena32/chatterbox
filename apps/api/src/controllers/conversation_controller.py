"""
ConversationController — rotas REST para conversas.

Estado: PLACEHOLDER (boilerplate)
Spec de referência: specs/001-iniciar-conversa/plan.md (seção "Camadas — API")

TODO (task T8 da spec 001):
  Implementar as 3 rotas após services e repositories estarem prontos e testados:
    POST   /conversations               → ConversationService.start_conversation()
    GET    /conversations/{id}          → ConversationService.get_conversation()
    POST   /conversations/{id}/messages → ConversationService.post_user_message()

  Registrar este router em src/main.py:
    app.include_router(router, prefix="/conversations", tags=["conversations"])

Regra: este módulo só pode importar services (via Depends), modelos Pydantic e FastAPI.
Nunca importar repositories ou motor diretamente aqui.
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: implementar rotas — aguardando spec 001 task T8
