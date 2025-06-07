import requests
import logging
from config import AI_MODEL, AI_URL

# ログ設定（必要に応じてレベルを DEBUG に変更可能）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)
class AIClient:
    """
    ユーザーの発言に対して、会話を盛り上げる返答を生成するクラス。
    """

    def __init__(self, model: str = AI_MODEL, base_url: str = AI_URL):
        self.model = model
        self.api_url = f"{base_url}/api/generate"
        logging.info(f"AIClient initialized with model: {model} and endpoint: {self.api_url}")

    def create_response(self, user_message: str) -> str:
        """
        ユーザー全体の発言ログを要約する（興味・知識・スキルの傾向など）。
        """

        prompt = f"""以下はカスタマーサポート担当者とユーザーの会話です。丁寧な敬語でユーザーの問題解決をサポートする返答をしてください。
    【ユーザー発言】:
    {user_message}
    """
        logger.info(f"Prompt sent to LLM: {prompt}")

        try:
            response = requests.post(self.api_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            logging.error(f"[✗] 返答生成失敗: {e}")
            return "すみません、AIが回答できませんでした。"
