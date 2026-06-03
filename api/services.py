import requests
import os
import re
from dotenv import load_dotenv

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

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a futuristic AI assistant. "
                    "You are intelligent, concise, helpful, and slightly futuristic in tone. "
                    "IMPORTANT: Respond in plain spoken English only — no markdown, no bullet points, "
                    "no asterisks, no code blocks, no special characters. "
                    "Keep every response to 2-3 sentences maximum. "
                    "If a topic needs more detail, summarise the key point and offer to elaborate."
                ),
            },
            {"role": "user", "content": message},
        ],
        "max_tokens": 120,  # hard cap — roughly 2-3 sentences
    }

    try:
        response = requests.post(OPENROUTE_URL, headers=headers, json=payload)
        print("STATUS:", response.status_code)
        print("RAW:", response.text)
        data = response.json()

        if "choices" in data:
            raw = data["choices"][0]["message"]["content"]
            return clean_for_speech(raw)

        return "No response received from AI."

    except Exception as e:
        return f"Systems error: {str(e)}"