"""WebSocket — streaming de mensagens da IA por conversa."""

from __future__ import annotations

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.core.exceptions import AIUnavailableError, ConversationNotFoundError
from src.services.conversation_service import ConversationService
from src.core.dependencies import get_conversation_service
from src.websocket.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/conversations/{conversation_id}")
async def ws_conversation_endpoint(
    websocket: WebSocket,
    conversation_id:str,
    service: ConversationService = Depends(get_conversation_service),
) -> None:
    print(f"WS Connection: {conversation_id}")
    await manager.connect(conversation_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content", "")
            if not content:
                continue

            await service.add_user_message(conversation_id, content)

            full_response = ""
            try:
                async for chunk in service.stream_ai_reply(conversation_id):
                    full_response += chunk
                    await websocket.send_json(
                        {
                            "type": "ai_message_chunk",
                            "conversation_id": conversation_id,
                            "content": chunk,
                        }
                    )
            except AIUnavailableError as exc:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": f"IA indisponível: {exc.conversation_id}",
                    }
                )
                continue

            ai_message = await service.finalize_ai_message(
                conversation_id, full_response
            )
            await websocket.send_json(
                {
                    "type": "ai_message_done",
                    "conversation_id": conversation_id,
                    "message": ai_message.model_dump(mode="json"),
                }
            )
    except WebSocketDisconnect:
        manager.disconnect(conversation_id, websocket)
    except ConversationNotFoundError:
        await websocket.send_json(
            {"type": "error", "message": "Conversa não encontrada."}
        )
        manager.disconnect(conversation_id, websocket)
    except Exception as exc:
        print(f"Error WS Controller: {exc}")
        await websocket.send_json({"type": "error", "message": str(exc)})
        manager.disconnect(conversation_id, websocket)
