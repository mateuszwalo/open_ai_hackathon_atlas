import os
import asyncio
import logging
from dotenv import load_dotenv
from typing import Dict, Any
from agents import Agent, Runner
from prompts import supervisor_prompt, emotional_prompt
from typing import Literal
from langgraph_config import SupervisorState, EmotionalState

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ładowanie zmiennych środowiskowych
load_dotenv(".env")

class SupervisorAgentOutput(BaseModel):
    message: str  
    action: Literal["ask_question", "forward_info"]

class EmotionalStateOutput(BaseModel):
    message: str

agent_supervisor = Agent(
    name = "Supervisor",
    model = "gpt-4o-mini",
    instructions = supervisor_prompt,
    output_type = SupervisorAgentOutput

)

agent_emotional = Agent(
    name = "EmotionalAgent",
    model = "gpt-4o-mini",
    instructions = emotional_prompt,
    output_type = EmotionalStateOutput
)


async def supervisor_step(state:SupervisorState) -> Dict[str, Any]:
    result = await Runner.run(agent_supervisor, state["messages"][-1])

    return {
            "messages": result.message,
            "thread_id": state.get("thread_id", ""),
            "action": result.action
        }

async def emotional_step(state:EmotionalState) -> Dict[str, Any]:
    result = await Runner.run(agent_emotional, state["messages"][-1])

    return {
            "messages": result.message,
            "thread_id": state.get("thread_id", "")
        }
