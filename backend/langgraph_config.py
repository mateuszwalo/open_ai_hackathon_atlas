from langgraph.graph import StateGraph
from typing import Literal
from typing_extensions import TypedDict, Annotated
from agents_logic import supervisor_step, emotional_step
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.types import interrupt

class SupervisorState(TypedDict):
    big_five: str
    summary: str
    thread_id: int
    action: Literal["ask_question", "forward_info"]
    messages: Annotated[list[AnyMessage], add_messages]

class EmotionalState(TypedDict):
    pass

def supervisor_step(state: SupervisorState):
    if state["action"] == "ask_question":
        # Logika zadawania pytania
        return "ask_question"
    elif state["action"] == "forward_info":
        # Logika przekazywania informacji
        return "emotional_agent"
    
def human_node(state: SupervisorState):
    # Pause the graph and wait for human input
    print("⏸️ Graph paused, waiting for human input...")
    # Save the state to a persistent store (e.g., database or in-memory store)
    value = interrupt(state)
    # For simplicity, we'll just return the state here
    return {
        "messages": value
    }

def build_graph():
    builder = StateGraph(SupervisorState)  # Używamy prostego dict zamiast AgentState
    builder.add_node("supervisor", supervisor_step)
    builder.add_node("emotional_agent", emotional_step)
    builder.add_node("human", human_node)
    builder.add_conditional_edges("supervisor", supervisor_step, ["human","emotional_agent"])
    builder.set_entry_point("supervisor")
    builder.set_finish_point("supervisor")
    return builder.compile()

graph = build_graph()