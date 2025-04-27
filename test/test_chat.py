# test/test_chat.py

import asyncio
import json
from httpx import AsyncClient
import requests
import uuid

# Example conversation data matching the formatter's expected structure
SAMPLE_CONVERSATION = {
    "messages": [
        {
            "role": "user",
            "message": "Hello! I'm interested in upgrading my current plan. I've been having issues with my service lately."
        },
        {
            "role": "agent",
            "message": "I understand your concern. Let me help you with the upgrade options. What specific issues are you experiencing?"
        }
    ],
    "session_identifier": str(uuid.uuid4())  # Generate a random UUID
}



if __name__ == "__main__":
    # Simple script to send a request to the endpoint
    response = requests.post(
        "http://localhost:7000/api/v1/chat/analyze",
        json=SAMPLE_CONVERSATION,
        headers={
            "x-api-key": "temp_secret123",
            "Content-Type": "application/json"
        }
    )

    print(response.status_code)
    print(response.json())
