import os
import asyncio
import logging
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import Dict, Any
from fastapi import FastAPI, HTTPException


# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ładowanie zmiennych środowiskowych
load_dotenv(".env")

# Inicjalizacja klienta OpenAI
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

# ID asystenta (zmień na swoje)
ASSISTANT_ID = "asst_bwWNGVBIsQyZ4WHjUKGWiyg6"

async def openai_agent_step(state: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Weryfikacja przed wysłaniem żądania
        if not state.get("message"):
            raise ValueError("Empty message")

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": state["message"]}
            ],
            max_tokens=150
        )
        
        return {
            "message": response.choices[0].message.content,
            "thread_id": state.get("thread_id", "")
        }
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))