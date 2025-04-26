import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any
from agents import Agent, Runner, FileSearchTool, trace
from prompts import supervisor_prompt, emotional_prompt, summary_prompt, emotional_analyst_prompt
from typing import Literal
from states import SupervisorState, EmotionalState
from pydantic import BaseModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import AnyMessage
from db import vectorstore
# from openai import OpenAI

def log(message: str):
    """Funkcja do logowania z timestampem"""
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}")
    
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

class SummaryOutput(BaseModel):
    summary: str

agent_supervisor = Agent(
    name = "Supervisor",
    model = "gpt-4.1-mini",
    instructions = supervisor_prompt,
    output_type = SupervisorAgentOutput
)

agent_emotional = Agent(
    name = "EmotionalAgent",
    model = "gpt-4.1",
    instructions = emotional_analyst_prompt,
    output_type = EmotionalStateOutput,
    tools = [
        FileSearchTool(
            max_num_results=5,
            vector_store_ids=["vs_680c96022a7081919f0115cec214ea83"],
        )
    ]
)

agent_summarty = Agent(
    name = "SummaryAgent",
    model = "gpt-4.1-mini",
    instructions = summary_prompt,
    output_type = SummaryOutput
)

def history_to_text(messages: list[AnyMessage]) -> str:
    history_as_text = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            history_as_text += f"Human: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history_as_text += f"AI: {msg.content}\n"
    return history_as_text.strip()

async def supervisor_step(state:SupervisorState):
    try:
        if not state["messages"]:
            raise ValueError("State messages are empty or invalid.")
        
        history_as_text = history_to_text(state["messages"])

        with trace("OpenAI Hackathon"):
            result = await Runner.run(agent_supervisor, history_as_text)
        if not result:
            raise ValueError("Runner.run returned None.")

        print(result)
        return {
            "messages": AIMessage(result.final_output.message),
            "thread_id": state.get("thread_id", ""),
            "action": result.final_output.action,
            "agent": "supervisor_agent",
        }
    except Exception as e:
        logger.error(f"Error in supervisor_step: {e}")
        raise

async def emotional_step(state: SupervisorState):
    context = state["summary"].content
    # user_input = state["messages"][-1].content

    # Połączenie kontekstu z wiadomością użytkownika (jeśli Runner nie ma dedykowanego parametru na kontekst)
    enriched_input = f"Summary of interview with user:\n{context}"

    with trace("OpenAI Hackathon"):
        result = await Runner.run(agent_emotional, enriched_input)
    print(f"Emotional result: {result.new_items}")

    return {
        "messages": [AIMessage(result.final_output.message)],
        "thread_id": state.get("thread_id", ""),
        "agent": "emotional_agent",
        # "psychological_context": context,  # zachowujemy kontekst, jeśli potrzebny dalej
    }


async def summary_step(state:SupervisorState):
    history_as_text = history_to_text(state["messages"])

    with trace("OpenAI Hackathon"):
        result = await Runner.run(agent_summarty, history_as_text)

    return {
            "summary": AIMessage(result.final_output.summary),
            "thread_id": state.get("thread_id", ""),
            "agent": "summary_agent"
        
        }