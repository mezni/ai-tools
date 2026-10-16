# examples/test_app.py
import logging

from config.settings import DEFAULT_MODEL, DEFAULT_PROVIDER
from core.llm_client import LLMClient

# Enable logging to watch tenacity retry warnings if any transient failures happen
logging.basicConfig(level=logging.INFO)


def main():
    print(f"--- Default Provider: {DEFAULT_PROVIDER} ---")
    print(f"--- Default Model: {DEFAULT_MODEL} ---\n")

    client = LLMClient()

    # Test payload
    messages = [
        {"role": "system", "content": "You are a concise AI assistant."},
        {"role": "user", "content": "Say hello and state your model name in 6 words or less."},
    ]

    # Test matrix: specify different providers and models configured in settings.yaml
    test_targets = [
        ("openai", "gpt-4o"),
        ("openai", "gpt-4o-mini"),
        ("anthropic", "claude-3-5-haiku-20241022"),
        ("gemini", "gemini-2.5-flash"),
    ]

    for provider, model in test_targets:
        print(f"[*] Testing Provider: {provider} | Model: {model}...")
        try:
            response = client.generate(messages=messages, provider=provider, model=model)
            print(f" -> Response: {response.strip()}\n")
        except Exception as e:  # noqa: BLE001
            print(f" -> Error (Check your API keys in .env): {e}\n")


if __name__ == "__main__":
    main()
