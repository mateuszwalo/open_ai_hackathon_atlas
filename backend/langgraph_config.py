from langgraph.graph import StateGraph
from agents_logic import openai_agent_step

def build_graph():
    builder = StateGraph(dict)  # Używamy prostego dict zamiast AgentState
    builder.add_node("openai_agent", openai_agent_step)
    builder.set_entry_point("openai_agent")
    builder.set_finish_point("openai_agent")
    return builder.compile()

graph = build_graph()