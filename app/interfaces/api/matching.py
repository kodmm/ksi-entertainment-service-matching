"""マッチング関連のAPIルーター。

エンドポイントは application 層のコマンド/クエリハンドラーを呼ぶだけにする。
"""

from __future__ import annotations

from fastapi import APIRouter

from app.application.commands.request_match import RequestMatchCommand, request_match
from app.application.queries.get_candidates import get_candidates
from app.infrastructure.event_store import event_store

router = APIRouter(prefix="/matching")


@router.get("/candidates")
async def candidates() -> list[dict[str, str]]:
    """マッチング候補取得APIの入り口(プレースホルダー)。"""
    return get_candidates()


@router.post("/request")
async def request(command: RequestMatchCommand) -> dict[str, str]:
    """マッチングリクエストを受け付け、MatchRequestedイベントを1件追加する。"""
    event = request_match(command, event_store)
    return {"match_id": event.match_id, "event_id": event.event_id}


@router.get("/_debug/events")
async def debug_events() -> list[dict[str, object]]:
    """デバッグ用: event store の内容をそのまま返す。

    TODO(TASK-未定): 動作確認用の一時エンドポイント。
    本実装時に、恒久的に残すか認証付きの管理APIに置き換えるか判断する。
    """
    return [
        {
            "type": type(event).__name__,
            "match_id": event.match_id,
            "event_id": event.event_id,
            "occurred_at": event.occurred_at.isoformat(),
            **{
                key: value
                for key, value in vars(event).items()
                if key not in {"match_id", "event_id", "occurred_at"}
            },
        }
        for event in event_store.all()
    ]
