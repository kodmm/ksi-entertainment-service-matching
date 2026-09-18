"""service-matching サービスのコンポジションルート。

FastAPIアプリを作成し、interfaces層のルーターを登録するだけにする。
実際のロジックは domain / application / infrastructure 層に置く
（層構成の詳細はREADME参照）。
"""

from __future__ import annotations

from fastapi import FastAPI

from app.interfaces.api.health import router as health_router
from app.interfaces.api.matching import router as matching_router
from app.interfaces.ws.signaling import router as signaling_router

app = FastAPI(title="ksi-entertainment-service-matching")

app.include_router(health_router)
app.include_router(matching_router)
app.include_router(signaling_router)
