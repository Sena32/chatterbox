---
name: fastapi-layered-tdd
description: Use esta skill sempre que for criar ou alterar um endpoint da API do ChatterBox (apps/api), especialmente ao adicionar uma nova entidade, endpoint REST ou regra de negócio que envolva as camadas model/repository/service/controller. Garante que o fluxo TDD (red-green-refactor) seja seguido e que as camadas não sejam misturadas.
---

# FastAPI em Camadas com TDD

## Quando usar

Sempre que a tarefa envolver: criar um novo endpoint, adicionar um campo a um
model existente, criar uma nova regra de negócio em um service, ou criar
acesso a uma nova coleção do MongoDB.

## Passo a passo

1. **Confirme a spec.** Verifique em `specs/` se existe uma spec cobrindo a
   mudança. Se não houver, pare e sugira criá-la primeiro.

2. **Model primeiro (se necessário).**
   - Se a mudança envolve um novo dado, crie/atualize o Pydantic model em
     `src/models/`.
   - Escreva um teste simples de validação em
     `tests/unit/models/test_<entidade>.py` (ex: campos obrigatórios, tipos).

3. **Repository — TDD.**
   - Escreva o teste em `tests/unit/repositories/test_<entidade>_repository.py`
     usando um Mongo mockado (ex: `mongomock`/`mongomock-motor`) ou fixture de
     banco de teste.
   - Rode o teste e confirme que falha (o repository/método ainda não
     existe ou não tem esse comportamento).
   - Implemente o método mínimo em `src/repositories/<entidade>_repository.py`
     para o teste passar.
   - Repository só conversa com Mongo. Não deve conter regra de negócio.

4. **Service — TDD.**
   - Escreva o teste em `tests/unit/services/test_<entidade>_service.py`,
     **mockando o repository** (não usar Mongo real aqui).
   - Confirme que falha, implemente o mínimo, confirme que passa.
   - Toda decisão de negócio (validações, orquestração, chamadas a outros
     services como `AIService`) vive aqui.

5. **Controller.**
   - Crie/atualize `src/controllers/<entidade>_controller.py` com um
     `APIRouter`.
   - O controller recebe o `service` via `Depends(...)`, traduz exceções de
     domínio em `HTTPException` com status code apropriado, e retorna
     modelos Pydantic (FastAPI serializa automaticamente).
   - Registre o router em `src/main.py` se ainda não estiver.

6. **Teste de integração.**
   - Em `tests/integration/`, escreva um teste que sobe a app (via
     `httpx.AsyncClient` + `ASGITransport`, ou `TestClient`) contra um banco
     de teste, exercitando o endpoint HTTP de ponta a ponta.

7. **Atualize `specs/NNN/tasks.md`**, marcando as tasks concluídas.

## Checklist de qualidade (antes de considerar concluído)

- [ ] Nenhum `import motor`/`pymongo` fora de `repositories/`.
- [ ] Nenhuma regra de negócio dentro de `controllers/` ou `repositories/`.
- [ ] Todo método público de `service`/`repository` tem teste unitário
      correspondente escrito **antes** da implementação.
- [ ] Erros de domínio são exceções específicas, tratadas no controller.
- [ ] Config lida de `core/config.py`, nunca `os.environ` espalhado.

## Exemplo de esqueleto de teste (repository)

```python
# tests/unit/repositories/test_conversation_repository.py
import pytest

@pytest.mark.asyncio
async def test_create_returns_conversation_with_id(conversation_repository):
    conversation = await conversation_repository.create()
    assert conversation.id is not None
    assert conversation.messages == []
```

## Exemplo de esqueleto de teste (service, com repository mockado)

```python
# tests/unit/services/test_conversation_service.py
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_post_user_message_persists_message():
    repo = AsyncMock()
    service = ConversationService(repository=repo, ai_service=AsyncMock())

    await service.post_user_message(conversation_id="abc", content="oi")

    repo.add_message.assert_awaited()
```
