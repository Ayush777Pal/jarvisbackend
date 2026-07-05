import json 
import requests

from decouple import config
from datetime import date
from .models import Todo
import json
import os

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

def extract_tasks(text):
    headers={
        "Authorization":f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":"application/json"
    }

    payload={
        "model":"deepseek/deepseek-chat",
        "messages":[
            {
                "role":"system",
                "content":(
                    "You are Jarvis's Todo extraction assistant.\n\n"

                    "Extract every todo task from the user's sentence.\n\n"

                    "Return ONLY valid JSON.\n\n"

                    "Format:\n"

                    "{\n"

                    '   "tasks":[\n'

                    '      "task1",\n'

                    '      "task2"\n'

                    "   ]\n"

                    "}\n\n"

                    "Do not explain anything."

                ),
            },
            {
                "role":"user",
                "content":text
            }
        ],
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
    )

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    content = (
        content.replace("```json","")
        .replace("```","")
        .strip()
    )

    return json.loads(content)

# for saving the tasks
def save_tasks(tasks):
    today = date.today()

    added = 0
    skipped = 0

    for task in tasks:

        exists = Todo.objects.filter(
            task__iexact=task,
            date=today
        ).exists()

        if exists:
            skipped += 1
            continue

        Todo.objects.create(
            task=task,
            date=today
        )

        added += 1

    total_today = Todo.objects.filter(date=today).count()

    return {
        "added": added,
        "skipped": skipped,
        "total_today": total_today
    }