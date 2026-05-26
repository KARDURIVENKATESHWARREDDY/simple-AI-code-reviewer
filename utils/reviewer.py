import os

from groq import Groq
from langsmith import traceable
from langsmith.wrappers import wrap_openai

from utils.prompts import build_review_prompt


def is_langsmith_enabled() -> bool:
    return os.getenv("LANGSMITH_TRACING", "false").lower() == "true"


def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")
    client = Groq(api_key=api_key)
    if is_langsmith_enabled():
        return wrap_openai(client)
    return client


@traceable(name="review_code")
def review_code(client: Groq, model: str, language: str, code: str) -> str:
    prompt = build_review_prompt(language, code)
    completion = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You produce high-quality software code reviews in markdown."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1800,
    )
    return completion.choices[0].message.content.strip()

