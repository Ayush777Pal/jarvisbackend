import requests
import json
import os

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)


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

    return json.loads(content)