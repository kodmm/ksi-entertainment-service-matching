"""ドメインイベントの型定義。

Event Sourcing(ES) では、集約(Aggregate)の状態を直接保存せず、
「何が起きたか」を表すイベントの列を正とする。状態はイベントを
再生(replay)することでその都度再構築する（詳細は aggregates.py）。

現時点ではマッチングの状態遷移
（候補提示 → リクエスト送信 → マッチ成立 → 通話開始 → 通話終了）のうち
MatchRequested / MatchAccepted のみ最小実装する。
候補提示・通話開始・通話終了に対応するイベントは未実装(スコープ外)。
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class DomainEvent:
    """すべてのドメインイベントの基底クラス。"""

    match_id: str
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class MatchRequested(DomainEvent):
    """ユーザーがマッチングをリクエストしたことを表すイベント。"""

    requester_id: str = ""


@dataclass(frozen=True)
class MatchAccepted(DomainEvent):
    """マッチングリクエストが相手に受け入れられ、マッチが成立したことを表すイベント。"""

    acceptor_id: str = ""
