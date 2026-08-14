"""Testes unitários do ConnectionManager (spec 003 T1)."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.websocket.connection_manager import ConnectionManager


@pytest.fixture
def manager():
    return ConnectionManager()


@pytest.fixture
def mock_websocket():
    ws = AsyncMock()
    ws.accept = AsyncMock()
    ws.send_json = AsyncMock()
    return ws


@pytest.mark.asyncio
async def test_connect_accepts_and_registers_websocket(
    manager, mock_websocket
):
    await manager.connect("conv-1", mock_websocket)

    mock_websocket.accept.assert_awaited_once()
    assert mock_websocket in manager._connections["conv-1"]


@pytest.mark.asyncio
async def test_connect_appends_multiple_websockets_same_conversation(
    manager, mock_websocket
):
    ws2 = AsyncMock()
    ws2.accept = AsyncMock()

    await manager.connect("conv-1", mock_websocket)
    await manager.connect("conv-1", ws2)

    assert len(manager._connections["conv-1"]) == 2


def test_disconnect_removes_websocket(manager, mock_websocket):
    manager._connections["conv-1"] = [mock_websocket]

    manager.disconnect("conv-1", mock_websocket)

    assert mock_websocket not in manager._connections.get("conv-1", [])


@pytest.mark.asyncio
async def test_send_json_broadcasts_to_all_connections_in_conversation(manager):
    ws1 = AsyncMock()
    ws2 = AsyncMock()
    manager._connections["conv-1"] = [ws1, ws2]
    payload = {"type": "ai_message_chunk", "content": "hi"}

    await manager.send_json("conv-1", payload)

    ws1.send_json.assert_awaited_once_with(payload)
    ws2.send_json.assert_awaited_once_with(payload)


@pytest.mark.asyncio
async def test_send_json_no_op_when_no_connections(manager):
    await manager.send_json("missing", {"type": "error"})
