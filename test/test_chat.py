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
        "http://localhost:7002/api/v1/chat/analyze",
        json=SAMPLE_CONVERSATION,
        headers={
            "x-api-key": "temp_secret123",
            "Content-Type": "application/json"
        }
    )

    print(f"Status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Raw response text: {response.text}")
    
    # Add error handling for JSON parsing
    try:
        json_response = response.json()
        print("JSON Response:", json_response)
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        # The response is not valid JSON, which might indicate a server error
        if response.status_code != 200:
            print(f"Server returned error status: {response.status_code}")
