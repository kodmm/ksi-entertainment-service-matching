"""WebRTCシグナリング中継の土台。

現時点では受信したメッセージをそのままエコーバックするだけの最小実装。
SDP/ICEのやり取りロジックは未実装(スコープ外)。
"""

from __future__ import annotations

from fastapi import WebSocket


async def handle_signaling_connection(websocket: WebSocket, session_id: str) -> None:
    """WebSocket接続を受け付け、受信メッセージをそのままエコーバックする。"""
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(message)
    except Exception:
        # 切断時に例外が飛んでくるため、ここでは無視して接続を終える。
        pass
