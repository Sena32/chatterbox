---
name: mongodb-repository-pattern
description: Use esta skill ao criar ou modificar qualquer arquivo em apps/api/src/repositories/. Garante que o acesso ao MongoDB via Motor siga o padrão correto do projeto: async, tipado com Pydantic, sem lógica de negócio, e testável com banco mockado.
---

# MongoDB Repository Pattern (Motor async)

## Responsabilidade da camada

O repository é o **único** ponto de contato com o MongoDB. Ele:

- Recebe e retorna **modelos Pydantic** (nunca dicts crus fora da camada).
- Não contém validação de regra de negócio.
- Usa `motor.motor_asyncio.AsyncIOMotorDatabase` injetado via `__init__`.

## Estrutura padrão

```python
# src/repositories/conversation_repository.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from src.models.conversation import Conversation, Message

class ConversationRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._col = db["conversations"]

    async def create(self) -> Conversation:
        ...

    async def get_by_id(self, conversation_id: str) -> Conversation | None:
        ...

    async def add_message(self, conversation_id: str, message: Message) -> Conversation:
        ...
```

## Mapeamento ObjectId ↔ str

- MongoDB usa `ObjectId` como `_id`. Pydantic usa `str` como `id`.
- Crie um helper de conversão (ex: `core/db.py`) para mapear documentos do
  Mongo para modelos. Nunca exponha `ObjectId` fora do repository.

```python
def doc_to_conversation(doc: dict) -> Conversation:
    doc["id"] = str(doc.pop("_id"))
    return Conversation(**doc)
```

## Testes com Mongo mockado

Use `mongomock-motor` (ou `motor` com `mongomock` backend) para testes
unitários que não precisam de um container Mongo real:

```python
# tests/unit/repositories/conftest.py
import pytest
from mongomock_motor import AsyncMongoMockClient

@pytest.fixture
async def db():
    client = AsyncMongoMockClient()
    return client["test_chatterbox"]

@pytest.fixture
async def conversation_repository(db):
    from src.repositories.conversation_repository import ConversationRepository
    return ConversationRepository(db)
```

## Checklist

- [ ] Nenhuma query Mongo fora de `repositories/`.
- [ ] Métodos são `async`.
- [ ] Retorna modelo Pydantic, não dict.
- [ ] `_id` do Mongo convertido para `id` str antes de sair da camada.
- [ ] `db` injetado no `__init__`, não importado globalmente.
