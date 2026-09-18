# ksi-entertainment-service-matching

「ksi-entertainment」のマッチング用バックエンドサービス。

## このサービスの役割

音楽ライブの参戦記録を残してシェアし、趣味の合う人とマッチングするサービス「ksi-entertainment」のうち、以下を担当する。

- 趣味の合うユーザーのマッチング/レコメンド計算
- WebRTC通話のためのシグナリング(WebSocket)

Go実装の misc-service とは別プロセス・別リポジトリの独立したマイクロサービスとして稼働する。

## 技術スタック

- Python (FastAPI + Uvicorn)
- 依存管理: [uv](https://docs.astral.sh/uv/)

## セットアップ

```bash
uv sync
```

## 起動

```bash
uv run uvicorn app.main:app --reload
```

`http://127.0.0.1:8000` で起動する。`GET /health` にアクセスして `{"status": "ok"}` が返れば起動確認できる。

## エンドポイント

現時点ではスキャフォールディングのみで、いずれも実装は最小限のプレースホルダー。

| メソッド/パス | 内容 |
| --- | --- |
| `GET /health` | ヘルスチェック |
| `GET /matching/candidates` | マッチング候補取得APIの入り口（ダミーの固定配列を返すだけ） |
| `WS /ws/signaling/{session_id}` | WebRTCシグナリング中継の土台（受信メッセージをそのままエコーバックするだけ） |

マッチングアルゴリズムやWebRTCのSDP/ICEのやり取りロジックは未実装。
