"""イベントストアのインメモリ実装。

プロセスを再起動するとイベントは消えるが、スキャフォールディング段階では
それで十分（将来的にDBや専用のイベントストアへの置き換えを想定）。
"""

from __future__ import annotations

from app.domain.events import DomainEvent


class EventStore:
    """イベントをメモリ上のリストに追加するだけの最小実装。"""

    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def append(self, event: DomainEvent) -> None:
        self._events.append(event)

    def all(self) -> list[DomainEvent]:
        return list(self._events)

    def for_match(self, match_id: str) -> list[DomainEvent]:
        return [event for event in self._events if event.match_id == match_id]


# モジュールレベルの単一インスタンス。DIコンテナを導入するほどの規模ではないため、
# コマンドハンドラーとデバッグ用エンドポイントはこのインスタンスを共有する。
event_store = EventStore()
