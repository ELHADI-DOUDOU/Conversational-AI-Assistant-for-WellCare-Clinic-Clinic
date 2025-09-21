from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from clinic_graph import graph, default_config

app = FastAPI(title="Good Health Clinic AI Assistant")

class ChatRequest(BaseModel):
    patient_id: str
    thread_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    config = {"configurable": {"patient_id": req.patient_id, "thread_id": req.thread_id}}
    input_msg = [HumanMessage(content=req.message)]

    output_messages = []
    for chunk in graph.stream({"messages": input_msg}, config, stream_mode="values"):
        output_messages.append(chunk["messages"][-1].content)

    return {"reply": output_messages[-1]}
