"""マッチング候補取得クエリのハンドラー。

TODO: 実際のマッチング/レコメンドアルゴリズムに置き換える。
現時点ではダミーの固定配列を返すだけ。
"""

from __future__ import annotations


def get_candidates() -> list[dict[str, str]]:
    return [
        {"user_id": "dummy-user-1", "display_name": "Dummy User 1"},
        {"user_id": "dummy-user-2", "display_name": "Dummy User 2"},
    ]
