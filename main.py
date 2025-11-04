from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b:free")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/v1/chat/completions")
async def generate_text(request: PromptRequest):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": request.prompt}],
        "response_format": {"type": "json_object"}
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    message = data["choices"][0]["message"]["content"]
    return {"response": message}
