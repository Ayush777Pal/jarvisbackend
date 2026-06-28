import json

import requests
import os
import re
from dotenv import load_dotenv
from memory.services import get_memory_context

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTE_URL = "https://openrouter.ai/api/v1/chat/completions"


def clean_for_speech(text):
    """Strip markdown and special characters so TTS reads cleanly."""
    # Remove code blocks entirely (``` ... ```)
    text = re.sub(r"```[\s\S]*?```", "code block omitted", text)
    # Remove inline code
    text = re.sub(r"`[^`]+`", lambda m: m.group().strip("`"), text)
    # Remove bold/italic markers
    text = re.sub(r"\*{1,3}(.*?)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}(.*?)_{1,3}", r"\1", text)
    # Remove markdown headers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove bullet/numbered list markers
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    # Remove links, keep label
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove leftover special characters (>, |, ~, ^, etc.)
    text = re.sub(r"[>|~^\\]", "", text)
    # Collapse multiple blank lines
    text = re.sub(r"\n{2,}", " ", text)
    # Collapse whitespace
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def generate_ai_response(message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    memory_context = get_memory_context()
    print(memory_context)

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Jarvis.\n\n"
                    "Known facts about the user\n\n"
                    f"{memory_context}\n\n"
                    "Use these memories naturally.\n"
                    "Do not say "
                    "'according to my memory'.\n"
                    "Do not mention the database.\n"
                    "Speak as if you already know the user.\n\n"
                    "Respond in plain spoken English.\n"
                    "No markdown.\n"
                    "No bullet points.\n"
                    "Maximum three sentences."
                ),
            },
            {"role": "user", "content": message},
        ],
        "max_tokens": 120,  # hard cap — roughly 2-3 sentences
    }

    try:
        response = requests.post(OPENROUTE_URL, headers=headers, json=payload)
        data = response.json()

        if "choices" in data:
            raw = data["choices"][0]["message"]["content"]
            return clean_for_speech(raw)

        return "No response received from AI."

    except Exception as e:
        return f"Systems error: {str(e)}"
    
## app launcher for jarvis 

def extract_app(text):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":"application/json"
    }

    payload = {
        "model":"deepseek/deepseek-chat",
        "messages":[
            {
                "role":"system",
                "content":(
                    "You are Jarvis's application launcher parser.\n\n"

                    "Your job is to identify the application, website, or service "
                    "the user wants to open.\n\n"

                    "Return ONLY valid JSON.\n\n"

                    "Format:\n"
                    "{\n"
                    '    "app":"<application_name>"\n'
                    "}\n\n"

                    "Rules:\n"
                    "- Extract only the application's name.\n"
                    "- Convert it to lowercase.\n"
                    "- Remove unnecessary words like 'open', 'launch', 'start', "
                    "'please', 'could you', etc.\n"
                    "- Do not explain your answer.\n"
                    "- Do not use markdown.\n"
                    "- Always return valid JSON."
                )
            },
            {
                "role":"user",
                "content":text
            }
        ]
    }

    response = requests.post(
        OPENROUTE_URL,
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