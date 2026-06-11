import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

VALID_CATEGORIES = {
    "работа",
    "личное",
    "здоровье",
    "обучение",
    "другое",
}


def parse_category(raw: str) -> str:
    category = raw.strip().lower()
    return category if category in VALID_CATEGORIES else "другое"


def parse_minutes(raw: str) -> int:
    try:
        minutes = int("".join(ch for ch in raw if ch.isdigit()))
        return max(5, min(minutes, 480))
    except ValueError:
        return 30


async def ask_openai(prompt: str) -> str:
    if not OPENAI_API_KEY:
        return ""

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except Exception:
        return ""


async def categorize_task(description: str) -> str:
    prompt = (
        "Отнеси эту задачу к одной из категорий: "
        "`работа`, `личное`, `здоровье`, `обучение`, `другое`. "
        "Верни только название категории.\n\n"
        f"Задача: {description}"
    )

    result = await ask_openai(prompt)
    return parse_category(result)


async def estimate_task_time(description: str) -> int:
    prompt = (
        f"Оцени, сколько минут займет выполнение этой задачи: '{description}'. "
        "Учти, что это ежедневная задача в планировщике. "
        "Верни только число."
    )

    result = await ask_openai(prompt)
    return parse_minutes(result)
