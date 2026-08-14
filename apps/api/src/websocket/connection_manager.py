"""Gerencia conexões WebSocket ativas por conversa (instância única — POC)."""

from __future__ import annotations

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, conversation_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self._connections.setdefault(conversation_id, []).append(ws)

    def disconnect(self, conversation_id: str, ws: WebSocket) -> None:
        conns = self._connections.get(conversation_id, [])
        if ws in conns:
            conns.remove(ws)
        if not conns:
            self._connections.pop(conversation_id, None)

    async def send_json(self, conversation_id: str, payload: dict) -> None:
        for ws in self._connections.get(conversation_id, []):
            await ws.send_json(payload)
