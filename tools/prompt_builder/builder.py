from tools.prompt_builder.registry import PromptRegistry


class PromptBuilder:
    def __init__(self, registry: PromptRegistry | None = None):
        self.registry = registry or PromptRegistry()

    def build(self, prompt_name: str, version: str = "latest", **kwargs) -> str:
        """Loads the template and populates its variables safely via string formatting."""
        prompt_data = self.registry.get_prompt(prompt_name, version=version)
        template_text = prompt_data.get("template", "")

        try:
            return template_text.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable for prompt '{prompt_name}': {e}")
