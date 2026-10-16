import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

local_config_path = Path.cwd() / "config" / "settings.yaml"
package_config_path = Path(__file__).parent / "settings.yaml"


def load_yaml_config() -> dict:
    target_path = local_config_path if local_config_path.exists() else package_config_path
    if target_path.exists():
        with open(target_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


yaml_config = load_yaml_config()

DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", yaml_config.get("default_provider", "openai"))
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", yaml_config.get("default_model", "gpt-4o"))
DEFAULT_TEMPERATURE = float(
    os.getenv("DEFAULT_TEMPERATURE", yaml_config.get("default_temperature", 0.7))
)
PROVIDERS_CATALOG = yaml_config.get("providers", {})


def get_provider_default_model(provider: str) -> str:
    """Returns the default model configured for a specific provider."""
    prov_data = PROVIDERS_CATALOG.get(provider.lower(), {})
    return prov_data.get("default_model", DEFAULT_MODEL)


def get_model_config(provider: str, model: str) -> dict:
    """Retrieves specific settings for a given provider and model."""
    prov_data = PROVIDERS_CATALOG.get(provider.lower(), {})
    models = prov_data.get("models", {})
    return models.get(model, {})
