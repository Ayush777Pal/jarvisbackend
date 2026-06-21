from .models import Memory,Contact
import requests
import json
import os
import re

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

def extract_forget_key(text):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You extract memory keys to forget.\n"
                    "Return ONLY JSON.\n"
                    "Format:\n"
                    "{\n"
                    '   "key":"..."\n'
                    "}\n"
                    "No markdown."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload
    )

    data = response.json()

    content = data["choices"][0]["message"]["content"]

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(content)

def get_memory_context():
    memories = list_memories()
    context = {}
    for memory in memories:
        context[memory.key] = memory.value

    return json.dumps(
        context,
        indent=2
    )

def save_contact(name,phone_number):
    contact, created = (
        Contact.objects.update_or_create(
            name = name.lower(),
            defaults={
                "phone_number":phone_number
            }
        )
    )

    return contact

def get_contact(name):
    try:
        return Contact.objects.get(
            name = name.lower()
        )
    except Contact.DoesNotExist:
        return None
    
def extract_contact(text):
    text = text.lower()
    phone_match = re.search(
        r"\b\d{10}\b",
        text
    )
    if not phone_match:
        return None
    
    phone_number = (
        phone_match.group()
    )
    
    text = text.replace(
        phone_number,
        ""
    )

    text = (
        text.replace("jarvis","").replace("save","").replace("contact","").replace("number","").strip()
    )
    name = (
        text.split()[0]
    )
    return {
        "name":name,
        "phone_number":phone_number
    }

def extract_contact_name(text):
    text = (
        text.lower()
    )
    text = (
        text.replace("jarvis","").replace("call","").strip()
    )
    return text