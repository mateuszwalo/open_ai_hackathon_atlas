from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph_config import graph
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add this after creating the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for paused states
paused_states = {}

# Pydantic Model do odbierania danych
class AgentInput(BaseModel):
    message: str
    thread_id: Optional[str] = ""

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
            "thread_id": result.get("thread_id", ""),
            "agent": result.get("agent", "")  # Dodajemy agent do odpowiedzi
        }
    except Exception as e:
        print(f"💥 Błąd podczas przetwarzania: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
