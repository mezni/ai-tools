import pytest

from tools.prompt_builder.builder import PromptBuilder
from tools.prompt_builder.registry import PromptRegistry


def test_registry_loading():
    registry = PromptRegistry()
    prompt_data = registry.get_prompt("code_refactor", version="v1")
    assert prompt_data["name"] == "code_refactor"
    assert "template" in prompt_data


def test_registry_not_found():
    registry = PromptRegistry()
    with pytest.raises(FileNotFoundError):
        registry.get_prompt("non_existent_prompt", version="v1")


def test_prompt_builder_rendering():
    builder = PromptBuilder()
    rendered = builder.build("code_refactor", version="v1", language="python", code="x = 1")
    assert "expert python software engineer" in rendered
    assert "x = 1" in rendered


def test_prompt_builder_missing_variable():
    builder = PromptBuilder()
    with pytest.raises(ValueError):
        builder.build("code_refactor", version="v1", language="python")  # Missing 'code'
