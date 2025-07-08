import logging
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
import json

load_dotenv()

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://10.40.4.14:3000"],  # 只允许你的前端服务器跨域访问
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": req.message}],
        "temperature": 0.7,
    }
    async with httpx.AsyncClient() as client:
        logger.debug(f"Sending request to DeepSeek API: {payload}")
        try:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            logger.debug(f"DeepSeek API response status: {response.status_code}")
            response_text = await response.text()
            logger.debug(f"DeepSeek API response content: {response_text}")
            response.raise_for_status()
            data = json.loads(response_text)
            if "error" in data:
                raise Exception(f"DeepSeek API错误: {data['error']}")
            reply = data["choices"][0]["message"]["content"]
            return {"reply": reply}
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP错误 {e.response.status_code}: {await e.response.text()}"
        except KeyError as e:
            error_msg = f"API响应格式错误，缺少字段: {str(e)}, 响应内容: {response_text}"
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
        logger.error(error_msg)
        return {"reply": error_msg}
