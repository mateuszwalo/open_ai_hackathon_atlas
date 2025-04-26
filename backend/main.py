from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph_config import graph

app = FastAPI()

# In-memory store for paused states
paused_states = {}

# Pydantic Model do odbierania danych
class AgentInput(BaseModel):
    message: str
    thread_id: Optional[str] = ""

class HumanInput(BaseModel):
    thread_id: str
    input_message: str

@app.post("/agent")
async def run_openai_agent(input_data: AgentInput):
    print(f"🔍 Odebrano dane: {input_data.model_dump()}")

    try:
        state = {
            "messages": [input_data.message],
            "thread_id": input_data.thread_id or "",
            'action': ""  # lub inna akcja, jeśli jest potrzebna
        }

        config = {"configurable": {"thread_id": input_data.thread_id}}

        result = await graph.ainvoke(state, config)

        if not result:
            raise ValueError("Graph invocation returned None.")
        
        print(f"🔍 Wynik: {result}")

        return {
            "response": result["messages"][-1].content,
            "thread_id": result.get("thread_id", "")
        }
    except Exception as e:
        print(f"💥 Błąd podczas przetwarzania: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
