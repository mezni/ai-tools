import logging
import os

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from config.settings import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    DEFAULT_TEMPERATURE,
    get_model_config,
    get_provider_default_model,
)

logger = logging.getLogger(__name__)

_retry_decorator = retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_not_exception_type(ValueError),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)


class LLMClient:
    def __init__(self, default_provider: str | None = None, default_model: str | None = None):
        self.default_provider = (default_provider or DEFAULT_PROVIDER).lower()
        self.default_model = default_model or DEFAULT_MODEL
        self._init_clients()

    def _init_clients(self):
        if os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI

            self.openai_client = OpenAI()
        else:
            self.openai_client = None

        if os.getenv("ANTHROPIC_API_KEY"):
            import anthropic

            self.anthropic_client = anthropic.Anthropic()
        else:
            self.anthropic_client = None

        if os.getenv("GEMINI_API_KEY"):
            from google import genai

            self.gemini_client = genai.Client()
        else:
            self.gemini_client = None

    def generate(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        provider: str | None = None,
        temperature: float | None = None,
    ) -> str:
        prov = (provider or self.default_provider).lower()
        mod = model or get_provider_default_model(prov)
        temp = temperature if temperature is not None else DEFAULT_TEMPERATURE

        model_cfg = get_model_config(prov, mod)
        max_tokens = model_cfg.get("max_tokens", 4096)

        @_retry_decorator
        def _execute():
            if prov == "openai":
                if not self.openai_client:
                    raise ValueError("OpenAI API key missing. Set OPENAI_API_KEY in .env")
                res = self.openai_client.chat.completions.create(
                    model=mod, messages=messages, temperature=temp, max_tokens=max_tokens
                )
                return res.choices[0].message.content

            elif prov == "anthropic":
                if not self.anthropic_client:
                    raise ValueError("Anthropic API key missing. Set ANTHROPIC_API_KEY in .env")
                system_prompt = next(
                    (m["content"] for m in messages if m["role"] == "system"), None
                )
                chat_messages = [m for m in messages if m["role"] != "system"]

                kwargs = {
                    "model": mod,
                    "max_tokens": max_tokens,
                    "messages": chat_messages,
                    "temperature": temp,
                }
                if system_prompt:
                    kwargs["system"] = system_prompt

                res = self.anthropic_client.messages.create(**kwargs)
                return res.content[0].text

            elif prov == "gemini":
                if not self.gemini_client:
                    raise ValueError("Gemini API key missing. Set GEMINI_API_KEY in .env")
                system_instruction = next(
                    (m["content"] for m in messages if m["role"] == "system"), None
                )
                chat_messages = [
                    {
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [{"text": m["content"]}],
                    }
                    for m in messages
                    if m["role"] != "system"
                ]
                config = {"temperature": temp}
                if system_instruction:
                    config["system_instruction"] = system_instruction

                res = self.gemini_client.models.generate_content(
                    model=mod, contents=chat_messages, config=config
                )
                return res.text
            else:
                raise ValueError(f"Unsupported provider: '{prov}'")

        return _execute()
