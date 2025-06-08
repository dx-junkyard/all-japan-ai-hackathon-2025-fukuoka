# config.py
# ここに設定を記載します

import os
from dotenv import load_dotenv

# .env ファイルが存在すれば読み込む
load_dotenv()

# LINEチャネルアクセストークン（LINE Developersで発行されたトークン）
LINE_CHANNEL_ACCESS_TOKEN = "basicコースでは使いません"

# OpenAI の Chat Completions API で使用するモデル名
# `.env` の OPENAI_MODEL があればそれを、無ければ `gpt-4o` を採用
AI_MODEL = "gpt-4o"

AI_URL = "http://host.docker.internal:11434"

DB_HOST = "db"

DB_USER = "me"

DB_PASSWORD = "me"

DB_NAME = "mydb"

DB_PORT = 3306

# VOICEBOXエンジンのURL
VOICEBOX_URL = "http://voicebox:50021"

VOICEBOX_SPEAKER=14
VOICEBOX_SPEED=2.0
