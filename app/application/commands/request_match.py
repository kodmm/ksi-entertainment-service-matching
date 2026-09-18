"""「マッチングをリクエストする」コマンドのハンドラー。

コマンドハンドラーは、必要なら集約(MatchAggregate)の現在状態を確認したうえで
操作を行い、結果のイベントを event store に追加する。
現時点では MatchRequested イベントを1件追加するだけの最小実装。
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.domain.events import MatchRequested
from app.infrastructure.event_store import EventStore


@dataclass
class RequestMatchCommand:
    """マッチングリクエストのコマンド(入力)。"""

    requester_id: str


def request_match(command: RequestMatchCommand, event_store: EventStore) -> MatchRequested:
    """マッチングリクエストを処理し、MatchRequestedイベントを追加する。

    TODO: 実際のマッチングアルゴリズムでマッチ相手を決定するロジックは未実装。
    現時点では新規のmatch_idを発行するだけ。
    """
    match_id = str(uuid.uuid4())
    event = MatchRequested(match_id=match_id, requester_id=command.requester_id)
    event_store.append(event)
    return event
