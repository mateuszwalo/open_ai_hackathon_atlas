from langgraph.graph import StateGraph
from agents_logic import supervisor_step, emotional_step
# from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver
from states import SupervisorState, EmotionalState

def supervisor_edge(state: SupervisorState):
    if state["action"] == "ask_question":
        # Logika zadawania pytania
        return "human"
    elif state["action"] == "forward_info":
        # Logika przekazywania informacji
        return "emotional_agent"
    
def human_node(state: SupervisorState):
    # Pause the graph and wait for human input
    pass

checkpointer = MemorySaver()

def build_graph():
    builder = StateGraph(SupervisorState)  # Używamy prostego dict zamiast AgentState
    builder.add_node("supervisor", supervisor_step)
    builder.add_node("emotional_agent", emotional_step)
    builder.add_node("human", human_node)
    builder.add_conditional_edges("supervisor", supervisor_edge, ["human","emotional_agent"])
    builder.add_edge("human", "supervisor")
    builder.set_entry_point("supervisor")
    builder.set_finish_point("emotional_agent")
    return builder.compile(interrupt_before=["human"], checkpointer=checkpointer)

graph = build_graph()