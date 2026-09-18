"""WebRTCシグナリング用WebSocketルーター。"""

from __future__ import annotations

from fastapi import APIRouter, WebSocket

from app.infrastructure.signaling import handle_signaling_connection

router = APIRouter()


@router.websocket("/ws/signaling/{session_id}")
async def signaling(websocket: WebSocket, session_id: str) -> None:
    await handle_signaling_connection(websocket, session_id)
