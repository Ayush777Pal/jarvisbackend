from .models import Memory
import requests
import json
import os

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)


def save_memory(key,value):
    memory, created = Memory.objects.update_or_create(
        key=key,
        defaults={
            "value":value
        }
    )
    return memory

def get_memory(key):
    try:
        return Memory.objects.get(
            key=key
        )
    except Memory.DoesNotExist:
        return None

def delete_memory(key):
    Memory.objects.filter(
        key=key,
    ).delete()

def list_memories():
    return Memory.objects.all()


def extract_memory(text):

    headers = {
        "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":
            "application/json"
    }

    payload = {
        "model":
            "deepseek/deepseek-chat",

        "messages":[
            {
                "role":"system",

                "content":(
                    "You extract personal memories. "
                    "Return ONLY valid JSON.\n\n"
                    "Format:\n"
                    "{\n"
                    '  "key":"...",\n'
                    '  "value":"..."\n'
                    "}\n\n"
                    "No markdown. "
                    "No explanation."
                )
            },
            {
                "role":"user",
                "content":text
            }
        ]
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload
    )

    data = response.json()

    content = (
        data["choices"][0]
        ["message"]
        ["content"]
    )
    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()
    
    return json.loads(content)