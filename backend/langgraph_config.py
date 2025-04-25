from langgraph.graph import StateGraph
from agents_logic import supervisor_step

def build_graph():
    builder = StateGraph(dict)  # Używamy prostego dict zamiast AgentState
    builder.add_node("supervisor", supervisor_step)
    builder.set_entry_point("supervisor")
    builder.set_finish_point("supervisor")
    return builder.compile()

graph = build_graph()