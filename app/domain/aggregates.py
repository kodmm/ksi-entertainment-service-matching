"""集約(Aggregate)の定義。

CQRS+ES では、DBに現在の状態を直接保存するのではなく、
event store に積まれたイベント列を `apply()` で再生(replay)して
その都度状態を再構築する。これが CRUD との一番の違い。
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.events import DomainEvent, MatchAccepted, MatchRequested


@dataclass
class MatchAggregate:
    """マッチング1件分の状態を、イベント列から再構築する集約。"""

    match_id: str
    status: str = "unknown"  # pending / accepted など

    def apply(self, event: DomainEvent) -> None:
        """イベント1件を適用し、状態を更新する。"""
        if isinstance(event, MatchRequested):
            self.status = "pending"
        elif isinstance(event, MatchAccepted):
            self.status = "accepted"

    @classmethod
    def from_events(cls, match_id: str, events: list[DomainEvent]) -> MatchAggregate:
        """イベント列を先頭から再生し、集約を再構築する。"""
        aggregate = cls(match_id=match_id)
        for event in events:
            aggregate.apply(event)
        return aggregate
