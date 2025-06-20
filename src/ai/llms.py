from django.conf import settings
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI


class AIModelProvider:
    """Centralized provider for AI model configurations and instantiation."""

    API_KEYS = {
        "openai": settings.OPENAI_API_KEY,
        "anthropic": settings.ANTHROPIC_API_KEY,
        "google": settings.GOOGLE_API_KEY,
        "azure": settings.AZURE_OPENAI_API_KEY,
        "ollama": "",
        "deepseek": settings.DEEPSEEK_API_KEY,
    }

    MODEL_NAMES = {
        "openai": "gpt-4o",
        "anthropic": "claude-2",
        "google": "gemini-2.0-flash",
        "azure": "gpt-4",
        "gpt-4-mini": "gpt-4-mini",
        "ollama": "llama3.1",
        "deepseek": "deepseek-chat"
    }

    DEFAULT_PROVIDER = "google"

    @classmethod
    def get_model(cls, provider=None, model_name=None, **kwargs):
        """
        Get an AI model instance for the specified provider.

        Args:
            provider: The AI provider (e.g., 'openai', 'deepseek')
            model_name: Specific model name to override default
            **kwargs: Additional arguments to pass to the model constructor

        Returns:
            Initialized AI model instance
        """
        provider = provider or cls.DEFAULT_PROVIDER
        api_key = cls.API_KEYS.get(provider)
        model = model_name or cls.MODEL_NAMES.get(provider)

        if not api_key:
            raise ValueError(f"No API key configured for provider: {provider}")

        model_params = {
            "model": model,
            "temperature": 0,
            "max_tokens": None,
            "max_retries": 2,
            "api_key": api_key,
            **kwargs
        }

        if provider == "deepseek":
            return ChatDeepSeek(**model_params)
        elif provider == "google":
            return ChatGoogleGenerativeAI(**model_params)
        else:
            return ChatOpenAI(**model_params)


def get_openai_model(model=None):
    return AIModelProvider.get_model(model_name=model)
