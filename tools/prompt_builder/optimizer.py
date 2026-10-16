import json
from typing import Any

from core.llm_client import LLMClient
from tools.prompt_builder.registry import PromptRegistry


class PromptOptimizer:
    def __init__(self, llm_client: LLMClient | None = None, registry: PromptRegistry | None = None):
        self.client = llm_client or LLMClient()
        self.registry = registry or PromptRegistry()

    def optimize(self, raw_prompt: str, version: str = "latest") -> dict[str, Any]:
        """Takes a raw user prompt draft and uses meta-prompting to refactor it."""
        meta_data = self.registry.get_prompt("meta_optimizer", version=version)
        system_prompt = meta_data.get("template", "You are an expert prompt engineer.")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Optimize this prompt draft:\n\n{raw_prompt}"},
        ]

        response_text = self.client.generate(messages=messages, temperature=0.2)

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "optimized_prompt": response_text,
                "strategies_applied": ["Automatic Refactoring"],
                "explanation": "Response could not be parsed as pure JSON.",
            }
