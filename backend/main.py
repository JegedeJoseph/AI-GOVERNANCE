from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="Couch Tracker API")

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "mock_data", "projects.json")

@app.get("/projects")
def get_projects():
    """Returns the list of mock projects."""
    with open(MOCK_DATA_PATH, "r") as f:
        return json.load(f)

@app.post("/webhook")
async def twilio_webhook(request: Request):
    """
    Dummy webhook to simulate receiving a WhatsApp message from Twilio.
    """
    form_data = await request.form()
    message_body = form_data.get("Body", "")
    from_number = form_data.get("From", "")
    
    print(f"Received WhatsApp message from {from_number}: {message_body}")
    
    return {"status": "success", "message": "Webhook received"}
