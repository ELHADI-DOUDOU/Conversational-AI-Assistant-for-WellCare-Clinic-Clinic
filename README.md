Conversational AI Assistant for Good Health Clinic

An AI-powered assistant for Good Health Clinic that helps patients with appointment scheduling, medical profile tracking, and intelligent responses based on patient history.

This project uses LangGraph, LangChain, FastAPI, and OpenAI GPT models to simulate a real-world conversational medical assistant.

🚀 Features

🧑‍⚕️ Conversational AI Assistant – provides personalised responses based on patient history

📅 Appointment Scheduling – manages routine and follow-up visits

📝 Patient Profile Management – stores medical notes, allergies, treatments, and medications

⚠️ Emergency Handling – detects urgent cases and escalates with emergency contacts

💾 Memory – stores patient interactions and history for continuity

📂 Project Structure
good_health_assistant/
│── main.py              # FastAPI server entrypoint
│── clinic_graph.py       # LangGraph workflow for patient interactions
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation

🔧 Installation
1. Clone the repository
git clone https://github.com/your-username/good_health_assistant.git
cd good_health_assistant

2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3. Install dependencies
pip install -r requirements.txt

4. Set your OpenAI API key

Create a .env file in the project root and add:

OPENAI_API_KEY=your_api_key_here


Verify it’s loaded correctly:

import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

▶️ Running the Server

Start the FastAPI server:

uvicorn main:app --reload


Server will run at:

http://127.0.0.1:8000


Check interactive API docs:

http://127.0.0.1:8000/docs

💬 Example Usage

Send a POST request to /chat:

curl -X 'POST' \
  'http://127.0.0.1:8000/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "patient_id": "1",
  "thread_id": "conv1",
  "message": "Hello, I need to book an appointment for next week"
}'


Example Response:

{
  "response": "Sure! I can help you schedule an appointment. Could you tell me which day and time works best for you?"
}

🛠️ Tech Stack

LangGraph
 – Graph-based conversational workflows

LangChain
 – LLM orchestration

FastAPI
 – API framework

OpenAI GPT
 – LLM backend

Uvicorn
 – ASGI server

📌 Roadmap

 Add frontend UI for patient chat

 Store patient profiles in a database (PostgreSQL / MongoDB)

 Expand medical knowledge integration (guidelines, FAQs)

 Deploy on cloud (Render, AWS, Azure, etc.)

⚠️ Disclaimer

This project is a prototype for educational purposes.
It should not be used as a replacement for professional medical advice.
Always consult qualified healthcare professionals for medical concerns."# Conversational-AI-Assistant-for-WellCare-Clinic-Clinic" 
"# Conversational-AI-Assistant-for-WellCare-Clinic-Clinic" 
"# Conversational-AI-Assistant-for-WellCare-Clinic-Clinic" 
"# Conversational-AI-Assistant-for-WellCare-Clinic-Clinic" 
