import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "こんにちは、あなたは誰？"}
    ]
)

print(response.choices[0].message.content)


