import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from config import AI_MODEL

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

    PROMPT_FILE = Path(__file__).resolve().parents[2] / "static" / "prompt.txt"

    def __init__(self, model: str = AI_MODEL):
        load_dotenv()
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
        try:
            self.prompt_template = self.PROMPT_FILE.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.prompt_template = (
                "以下はカスタマーサポート担当者とユーザーの会話です。丁寧な敬語でユーザーの問題解決をサポートする返答をしてください。\n"
                "【ユーザー発言】:\n{user_message}"
            )
            logging.warning("Prompt file not found; using default template")
        logging.info(f"AIClient initialized with model: {model}")

    def create_response(self, user_message: str, history=None) -> str:
        """
        ユーザー全体の発言ログを要約する（興味・知識・スキルの傾向など）。
        """

        messages = []
        if history:
            for m in history:
                role = "user" if m.get("role") == "user" else "assistant"
                content = m.get("content", "")
                messages.append({"role": role, "content": content})

        prompt = self.prompt_template.format(user_message=user_message)
        messages.append({"role": "user", "content": prompt})
        logger.info(f"Prompt sent to LLM: {prompt}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"[✗] 返答生成失敗: {e}")
            return "すみません、AIが回答できませんでした。"
