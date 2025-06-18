from django.conf import settings
from langchain_openai import ChatOpenAI


AI_API_KEYS = {
    "openai": settings.OPENAI_API_KEY,
    "anthropic": settings.ANTHROPIC_API_KEY,
    "google": settings.GOOGLE_API_KEY,
    "azure": settings.AZURE_OPENAI_API_KEY,
}

AI_MODELS = {
    "openai": "gpt-4o",
    "anthropic": "claude-2",
    "google": "gemini-2.0-flash",
    "azure": "gpt-4",
    "gpt-4-mini": "gpt-4-mini"
}


def get_openai_model(model=None):
    if model is None:
        model = AI_MODELS["openai"]

    return ChatOpenAI(
        model=model,
        temperature=0,
        max_tokens=None,
        max_retries=2,
        api_key=AI_API_KEYS["openai"],
    )
