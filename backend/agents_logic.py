import os
import asyncio
import logging
from dotenv import load_dotenv
from typing import Dict, Any
from agents import Agent, Runner
from prompts import supervisor_prompt, emotional_prompt
from typing import Literal
from states import SupervisorState, EmotionalState
from pydantic import BaseModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

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


async def supervisor_step(state:SupervisorState):
    try:
        print(f"State: {state}")
        if not state["messages"]:
            raise ValueError("State messages are empty or invalid.")
        
        history_as_text = ""
        for msg in state["messages"]:
            if isinstance(msg, HumanMessage):
                history_as_text += f"Human: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                history_as_text += f"AI: {msg.content}\n"

        result = await Runner.run(agent_supervisor, history_as_text)
        if not result:
            raise ValueError("Runner.run returned None.")

        print(result)
        return {
            "messages": AIMessage(result.final_output.message),
            "thread_id": state.get("thread_id", ""),
            "action": result.final_output.action
        }
    except Exception as e:
        logger.error(f"Error in supervisor_step: {e}")
        raise

async def emotional_step(state:EmotionalState) -> Dict[str, Any]:
    result = await Runner.run(agent_emotional, state["messages"][-1].content)

    return {
            "messages": AIMessage(result.final_output.message),
            "thread_id": state.get("thread_id", "")
        }
