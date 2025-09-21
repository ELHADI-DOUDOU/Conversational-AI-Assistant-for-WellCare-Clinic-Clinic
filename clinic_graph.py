import os
from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.base import BaseStore

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig

from langgraph.store.memory import InMemoryStore


# Create model
model = ChatOpenAI(temperature=0)
CLINIC_NAME = "WellCare Clinic"

MODEL_SYSTEM_MESSAGE = """You are a helpful medical assistant for {clinic_name}.
Use the patient's history to provide relevant, personalized appointment scheduling or advice.
Patient profile: {history}"""

UPDATE_PATIENT_PROFILE_INSTRUCTION = """Update the patient's medical/appointment profile with new information.

CURRENT PROFILE:
{history}

Update the profile based on this conversation:
"""

def check_condition(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_msg = state["messages"][-1].content.lower()
    if "emergency" in user_msg:
        return {'decision': 'emergency_route'}
    else:
        return {'decision': 'regular_route'}

def handle_emergency(state: MessagesState, config: RunnableConfig, store: BaseStore):
    return {
        "messages": [
            SystemMessage(
                content="🚨 Emergency detected! Please call 911 or our urgent line: +43 00 00 00."
            )
        ]
    }

def call_model(state: MessagesState, config: RunnableConfig, store: BaseStore):
    patient_id = config["configurable"]["patient_id"]
    namespace = ("patient_interactions", patient_id)
    key = "patient_data_memory"
    memory = store.get(namespace, key)
    history = memory.value.get('patient_data_memory') if memory else "No existing patient profile found."
    system_msg = MODEL_SYSTEM_MESSAGE.format(history=history, clinic_name=CLINIC_NAME)
    response = model.invoke([SystemMessage(content=system_msg)] + state["messages"])
    return {"messages": response}

def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):
    patient_id = config["configurable"]["patient_id"]
    namespace = ("patient_interactions", patient_id)
    key = "patient_data_memory"
    memory = store.get(namespace=namespace, key=key)
    history = memory.value.get(key) if memory else "No existing history."
    system_msg = UPDATE_PATIENT_PROFILE_INSTRUCTION.format(history=history)
    new_insights = model.invoke([SystemMessage(content=system_msg)] + state['messages'])
    store.put(namespace, key, {"patient_data_memory": new_insights.content})

# ---- Build the Graph ----
builder = StateGraph(MessagesState)
builder.add_node("check_condition", check_condition)
builder.add_node("call_model", call_model)
builder.add_node("handle_emergency", handle_emergency)
builder.add_node("write_memory", write_memory)

builder.add_edge(START, "check_condition")
builder.add_conditional_edges(
    "check_condition",
    lambda state: state["decision"],
    {"emergency_route": "handle_emergency", "regular_route": "call_model"}
)
builder.add_edge("handle_emergency", "write_memory")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)

# ✅ Memory
across_thread_memory = InMemoryStore()
within_thread_memory = MemorySaver()

# ✅ Compile the graph (this is what main.py needs!)
graph = builder.compile(
    checkpointer=within_thread_memory,
    store=across_thread_memory
)

# ✅ Default config template (also needed in main.py)
default_config = {
    "configurable": {"thread_id": "1", "patient_id": "1"}
}