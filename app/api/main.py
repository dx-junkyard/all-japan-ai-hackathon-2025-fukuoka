import requests
from fastapi import FastAPI, Request, HTTPException, Query
from typing import Dict, List
import logging

# config.pyからトークンやAPIエンドポイントをインポート
from app.api.ai import AIClient
from app.api.db import DBClient

app = FastAPI()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINEのWebhookエンドポイント
@app.post("/api/v1/user-message")
async def post_usermessage(request: Request) -> str:
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
   
    ai_generator = AIClient()
    message = body.get("message", "")
    ai_response = ai_generator.create_response(message)
    logger.info(f"AI response: {ai_response}")
    repo = DBClient()
    repo.insert_message("me",message)
    repo.insert_message("ai",ai_response)
    return ai_response

@app.get("/api/v1/user-messages")
async def get_user_messages(user_id: str = Query(..., description="ユーザーID"), limit: int = Query(10, ge=1, le=100, description="取得件数")) -> List[Dict]:
    repo = DBClient()
    messages = repo.get_user_messages(user_id=user_id, limit=limit)
    return messages

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

