from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph_config import graph

app = FastAPI()

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
        # Przygotowanie stanu dla LangGraph
        state = {
            "message": input_data.message,
            "thread_id": input_data.thread_id or ""
        }

        # Wywołanie grafu (używając ainvoke dla async)
        result = await graph.ainvoke(state)
        
        return {
            "response": result.get("message", ""),
            "thread_id": result.get("thread_id", "")
        }
    except Exception as e:
        print(f"💥 Błąd podczas przetwarzania: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/human_input")
async def provide_human_input(input_data: HumanInput):
    print(f"🤝 Received human input: {input_data.model_dump()}")

    try:
        # Retrieve the paused state using thread_id (from a persistent store or in-memory store)
        paused_state = {
            "thread_id": input_data.thread_id,
            "message": input_data.input_message
        }

        # Resume the graph execution
        result = await graph.ainvoke(paused_state)

        return {
            "response": result.get("message", ""),
            "thread_id": result.get("thread_id", "")
        }
    except Exception as e:
        print(f"💥 Error while processing human input: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))