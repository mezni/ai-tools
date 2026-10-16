import json
from pathlib import Path
from typing import Any

TEMPLATES_DIR = Path(__file__).parent / "templates"


class PromptRegistry:
    def __init__(self, templates_base_dir: Path = TEMPLATES_DIR):
        self.base_dir = templates_base_dir

    def get_prompt(self, prompt_name: str, version: str = "latest") -> dict[str, Any]:
        """Loads a prompt template JSON object by name and version tag."""
        prompt_dir = self.base_dir / prompt_name

        if not prompt_dir.exists():
            raise FileNotFoundError(
                f"Prompt template directory '{prompt_name}' not found at {prompt_dir}."
            )

        version_filename = f"{version}.json" if not version.endswith(".json") else version
        target_path = prompt_dir / version_filename

        if not target_path.exists():
            raise FileNotFoundError(
                f"Version '{version}' for prompt '{prompt_name}' not found at {target_path}."
            )

        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
