from config.settings import DEFAULT_PROVIDER, get_model_config, get_provider_default_model
from core.llm_client import LLMClient


def test_settings_catalog():
    assert DEFAULT_PROVIDER in ["openai", "anthropic", "gemini"]
    openai_default = get_provider_default_model("openai")
    assert openai_default == "gpt-4o"

    cfg = get_model_config("openai", "gpt-4o-mini")
    assert cfg.get("max_tokens") == 4096


def test_llm_client_initialization():
    client = LLMClient()
    assert client.default_provider is not None
    assert client.default_model is not None
