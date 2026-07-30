"""ConversationRepository — acesso ao MongoDB (coleção 'conversations')."""

from __future__ import annotations

from datetime import datetime, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from src.models.conversation import Conversation, Message


def _doc_to_conversation(doc: dict) -> Conversation:
    mapped = dict(doc)
    mapped["id"] = str(mapped.pop("_id"))
    return Conversation(**mapped)


class ConversationRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._col = db["conversations"]

    async def create(self) -> Conversation:
        now = datetime.now(timezone.utc)
        result = await self._col.insert_one({"created_at": now, "messages": []})
        doc = await self._col.find_one({"_id": result.inserted_id})
        return _doc_to_conversation(doc)

    async def get_by_id(self, conversation_id: str) -> Conversation | None:
        if not ObjectId.is_valid(conversation_id):
            return None
        doc = await self._col.find_one({"_id": ObjectId(conversation_id)})
        if doc is None:
            return None
        return _doc_to_conversation(doc)

    async def add_message(self, conversation_id: str, message: Message) -> Conversation:
        doc = await self._col.find_one_and_update(
            {"_id": ObjectId(conversation_id)},
            {"$push": {"messages": message.model_dump()}},
            return_document=ReturnDocument.AFTER,
        )
        if doc is None:
            raise ValueError(f"Conversation not found: {conversation_id}")
        return _doc_to_conversation(doc)
