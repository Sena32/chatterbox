"""
ConversationService — regras de negócio e orquestração.

Estado: PLACEHOLDER (boilerplate)
Spec de referência:
  - specs/001-iniciar-conversa/plan.md  (start_conversation, get_conversation, post_user_message)
  - specs/002-ia-responde-com-objetivo/plan.md (integração com AIService)
Skill de referência: .cursor/skills/fastapi-layered-tdd/SKILL.md

TODO (tasks T5, T6, T7 da spec 001 e tasks T5, T6 da spec 002 — TDD):
  1. Escrever testes em tests/unit/services/test_conversation_service.py (RED)
  2. Implementar start_conversation(), get_conversation(), post_user_message() (GREEN)
  3. Integrar AIService após spec 002 (estender testes existentes)

Este service recebe ConversationRepository e AIService via __init__ (injeção de dependência).
Nunca importar motor ou requests aqui diretamente.
"""

# TODO: implementar — aguardando spec 001 tasks T5–T7 e spec 002 tasks T5–T6
