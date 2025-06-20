# 顧客は悟る

全日本AIハッカソン 2025 福岡大会(6月7日開催)の出展作品です。お題は「悟」。本アプリケーションは、架空の製品「ロボポン」が皿を割ってしまい怒鳴り込んでくる顧客を、穏やかに“悟らせる”カスタマーサポート AI エージェントです。FastAPI を使ったバックエンドと Streamlit によるフロントエンドで構成され、Whisperによる音声入力とVOICEVOXによる音声出力が行えます。

## 主な機能

- Streamlit フロントエンドでのチャット UI
- FastAPI バックエンドによる API 提供
- OpenAI Whisper を利用した音声認識
- VOICEVOX を利用した音声合成
- MySQL への会話履歴保存
- Ollama 経由で LLM から返答を生成

## プロジェクト構成

```
.
├── app/
│   ├── api/                    # FastAPIバックエンド
│   │   ├── main.py            # メインAPIエンドポイント
│   │   ├── ai.py              # AI応答生成ロジック
│   │   └── db.py              # メッセージ保存ロジック
│   └── ui/                    # Streamlitフロントエンド
│       ├── ui.py              # UIアプリケーション
│       ├── voice_input.py     # 音声入力機能
│       └── audio_output.py    # 音声出力機能
├── mysql/                     # MySQLデータベース関連
│   └── db/user_messages.sql   # テーブル定義(DDL)
├── static/                    # プロンプトや画像ファイル
│   ├── prompt.txt
│   └── robopon.png
├── config.py                  # 設定ファイル
├── requirements.api.txt       # API依存関係
├── requirements.ui.txt        # UI依存関係
├── Dockerfile.api             # API用Dockerfile
├── Dockerfile.ui              # UI用Dockerfile
├── docker-compose.yaml        # Docker Compose設定
├── api_test.sh                # APIテスト用スクリプト
├── ollama_test.sh             # LLM 疎通確認用
└── db_connect.sh              # DB接続確認用スクリプト
```

## 主要なコンポーネント

- FastAPIバックエンド: ユーザーメッセージの処理とAI応答の生成
- Streamlitフロントエンド: ユーザーインターフェースの提供
- データベース連携: 会話履歴の保存と取得
- 音声入出力: マイク録音と VOICEVOX による音声生成

## 実装のポイント

### バックエンド（FastAPI）
- APIエンドポイントの定義
- データベース操作の実装
- AI応答生成ロジックの実装

### フロントエンド（Streamlit）
- ユーザーインターフェースの実装
- APIとの通信処理
- セッション状態を使用した会話履歴の管理
 - OpenAI Whisper API を利用した音声認識
- 音声認識結果とLLMへ送信するプロンプトをログ出力
 - AI応答を VOICEVOX で音声生成して再生

## セットアップ

### 前提条件

- Python 3.9以上
- 必要なパッケージ（requirements.txtに記載）

### セットアップ手順

1. **リポジトリのクローン**
    ```bash
    git clone https://github.com/dx-junkyard/all-japan-ai-hackathon-2025-fukuoka.git
    cd all-japan-ai-hackathon-2025-fukuoka
    ```

2. **環境構築**
    - 必要な環境変数を設定
    - 依存パッケージのインストール

3. **アプリケーションの起動**
    ```bash
    # Linux/Mac環境
    docker compose up
    ```

4. **アプリケーションにアクセス**
    - UI: http://localhost:8080
    - API: http://localhost:8086
    - VOICEVOX: http://localhost:50021

## 使い方

### Webインターフェース

1. ブラウザで http://localhost:8080 にアクセス
2. 🎤 ボタンを押して録音開始、もう一度押すと送信できます
3. AIの応答は自動で音声再生されます
4. 会話履歴は画面上に表示されます
5. ロゴ画像を表示する場合は `static/robopon.png` に任意の画像を配置してください

#### 音声入力を利用するには

1. `.env.example` をコピーして `.env` を作成し、`OPENAI_API_KEY` を設定します
2. ブラウザがマイクへのアクセスを求めたら許可してください。録音はブラウザ側で行われるため、Dockerコンテナからホストのマイクを参照する必要はありません
3. 音声の変換には `ffmpeg` が必要です。Docker イメージでは自動でインストールされます。ローカル環境で実行する場合は `ffmpeg` をインストールしてください
4. 音声認識で得られたテキストはログに出力されます

#### 音声出力について
VOICEVOX コンテナを利用して音声を生成し、ブラウザ上で再生します。
`docker compose up` を実行すると自動で起動します。
再生速度は `VOICEVOX_SPEED` 環境変数で変更でき、デフォルトは `1.5` です。
プロンプトは `static/prompt.txt` を編集することでカスタマイズできます。

#### LLM について
Ollama を使用して LLM をローカルで実行します。モデル `schroneko/llama-3.1-swallow-8b-instruct-v0.1` を `ollama run` しておくか、`ollama serve` を起動してから Docker を立ち上げてください。

### APIの直接利用

#### メッセージの送信

```bash
curl http://localhost:8086/api/v1/user-message \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "message": "こんにちは！"
  }'
```

#### 履歴の取得

```bash
curl 'http://localhost:8086/api/v1/user-messages?user_id=me&limit=10'
```

## 開発

### バックエンド（FastAPI）

バックエンドはFastAPIを使用して実装されており、以下のエンドポイントを提供します：

- `POST /api/v1/user-message`: ユーザーメッセージを処理し、AI応答を返す
- `GET /api/v1/user-messages`: 過去のメッセージ履歴を取得
- 送信するプロンプトをログに記録してデバッグ可能

### フロントエンド（Streamlit）

フロントエンドはStreamlitを使用して実装されており、以下の機能を提供します：

- ユーザーメッセージの入力
- AI応答の表示
- メッセージ履歴の表示
- マイク入力と音声読み上げ

このUIは、以前HTMLサンプルとして示したチャット画面のレイアウトをStreamlit上で再現しています。

## 拡張アイデア

- ユーザー認証の追加
- 複数のAIモデル切り替え機能
- メッセージの検索機能
- 会話履歴のエクスポート機能

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
