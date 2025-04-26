from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from typing import Literal

class SupervisorState(TypedDict):
    # big_five: str
    summary: str
    thread_id: str
    action: str
    agent: str
    messages: Annotated[list[AnyMessage], add_messages]

class EmotionalState(TypedDict):
    psychological_context: str
    docs_context: str
    thread_id: str
    messages: Annotated[list[AnyMessage], add_messages]