"""service-matching サービスのエントリーポイント。

役割:
- 趣味の合うユーザーのマッチング/レコメンド計算
- WebRTC通話のためのシグナリング(WebSocket)

現時点ではスキャフォールディングのみで、実際のマッチングアルゴリズムや
WebRTC シグナリングのロジックは未実装。
"""

from fastapi import FastAPI, WebSocket

app = FastAPI(title="ksi-entertainment-service-matching")


@app.get("/health")
async def health() -> dict[str, str]:
    """ヘルスチェック用エンドポイント。"""
    return {"status": "ok"}


@app.get("/matching/candidates")
async def get_matching_candidates() -> list[dict[str, str]]:
    """マッチング候補取得APIのプレースホルダー。

    TODO: 実際のマッチング/レコメンドアルゴリズムに置き換える。
    現時点ではダミーの固定配列を返すだけ。
    """
    return [
        {"user_id": "dummy-user-1", "display_name": "Dummy User 1"},
        {"user_id": "dummy-user-2", "display_name": "Dummy User 2"},
    ]


@app.websocket("/ws/signaling/{session_id}")
async def signaling(websocket: WebSocket, session_id: str) -> None:
    """WebRTCシグナリング中継の土台となるWebSocketエンドポイント。

    現時点では受信したメッセージをそのままエコーバックするだけの最小実装。
    SDP/ICE のやり取りロジックは未実装。
    """
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(message)
    except Exception:
        # 切断時に例外が飛んでくるため、ここでは無視して接続を終える。
        pass
