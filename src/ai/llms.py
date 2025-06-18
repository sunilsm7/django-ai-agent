from django.conf import settings
from langchain_openai import ChatOpenAI


def get_openai_api_key():
    return settings.OPENAI_API_KEY


def get_openai_model(model="gpt-4o-mini"):
    return ChatOpenAI(
        model=model,
        temperature=0,
        max_tokens=None,
        max_retries=2,
        api_key=get_openai_api_key()
    )
