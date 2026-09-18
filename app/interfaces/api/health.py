"""ヘルスチェック用ルーター。"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """ヘルスチェック用エンドポイント。"""
    return {"status": "ok"}
