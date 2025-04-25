import os
import asyncio
import logging
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from agents import Agent, Runner
from prompts import supervisor_prompt


# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ładowanie zmiennych środowiskowych
load_dotenv(".env")

agent_supervisor = Agent(
    name = "Supervisor",
    model = "gpt-4o-mini",
    instructions = supervisor_prompt,
)

async def supervisor_step(state: Dict[str, Any]) -> Dict[str, Any]:
    result = await Runner.run(agent_supervisor, state["message"])

    return {
            "message": result.final_output,
            "thread_id": state.get("thread_id", "")
        }
