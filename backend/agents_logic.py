import os
import asyncio
import logging
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from agents import Agent, Runner


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

agent = Agent(
    name="Math Tutor",
    model = "gpt-4o-mini",
    instructions="Co drugie słowo w odpowiedzi powinno być pogrubione.",
)

async def openai_agent_step(state: Dict[str, Any]) -> Dict[str, Any]:
    result = await Runner.run(agent, state["message"])

    return {
            "message": result.final_output,
            "thread_id": state.get("thread_id", "")
        }
