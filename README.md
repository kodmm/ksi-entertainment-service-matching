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

## Docker

```bash
docker build -t ksi-matching .
docker run -p 8000:8000 ksi-matching
```

`http://127.0.0.1:8000/health` で `{"status": "ok"}` が返れば起動確認できる。

## エンドポイント

現時点ではスキャフォールディングのみで、いずれも実装は最小限のプレースホルダー。

| メソッド/パス | 内容 |
| --- | --- |
| `GET /health` | ヘルスチェック |
| `GET /matching/candidates` | マッチング候補取得APIの入り口（ダミーの固定配列を返すだけ） |
| `POST /matching/request` | マッチングリクエストを受け付け、`MatchRequested` イベントを1件追加する |
| `GET /matching/_debug/events` | デバッグ用。event store の内容をそのまま返す（動作確認用の一時エンドポイント） |
| `WS /ws/signaling/{session_id}` | WebRTCシグナリング中継の土台（受信メッセージをそのままエコーバックするだけ） |

マッチングアルゴリズムやWebRTCのSDP/ICEのやり取りロジックは未実装。

## アーキテクチャ

このサービスはClean Architectureを採用する。5つあるサービスのうちマッチングの状態遷移
（候補提示 → リクエスト送信 → マッチ成立 → 通話開始 → 通話終了）をイベント履歴として
モデリングできるため、このサービスに限り CQRS（コマンドとクエリの分離） + Event Sourcing（ES） を採用している
（他のサービスは通常のCQRSまたは素のCRUD）。

```
app/
├── domain/            # ドメイン層: ビジネスルールの核
│   ├── events.py      # DomainEvent（イベントの基底クラス）と具体イベント（MatchRequested等）
│   └── aggregates.py  # MatchAggregate。イベント列を再生(replay)して現在の状態を再構築する
├── application/        # アプリケーション層: ユースケース
│   ├── commands/      # 状態を変更するコマンドハンドラー（例: request_match.py）
│   └── queries/       # 状態を変更しないクエリハンドラー（例: get_candidates.py）
├── infrastructure/     # インフラ層: 技術的な実装詳細
│   ├── event_store.py # イベントストア（現時点はインメモリの最小実装）
│   └── signaling.py   # WebRTCシグナリング中継（現時点はエコーバックのみ）
└── interfaces/         # インターフェース層: 外部との接点
    ├── api/           # FastAPIのHTTPルーター。application層のハンドラーを呼ぶだけ
    └── ws/            # FastAPIのWebSocketルーター。infrastructure層を呼ぶだけ
```

CQRS+ESの考え方: 集約(`MatchAggregate`)の現在状態をDBに直接保存せず、
「何が起きたか」を表すイベント列（`event_store`）を正とする。状態が必要になった時点で
イベントを先頭から再生(replay)して都度再構築する。これにより、状態遷移の履歴がそのまま残る。

現時点ではイベントストアはインメモリ実装（プロセス再起動で消える）で、
イベントも `MatchRequested` / `MatchAccepted` の最小限のみ。実際のマッチングアルゴリズムや
永続化層は未実装（スコープ外）。
