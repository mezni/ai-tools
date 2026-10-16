# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-10-16

### Fixed

- Tenacity retry decorator binding bug in `LLMClient` that caused `wrap() takes 1 positional argument but 2 were given`.
- Missing API key `ValueError`s are no longer retried with exponential backoff (config errors fail fast).
- Wrong `ai_tools.*` imports in `examples/test_app.py`.
- Ruff lint issues (import sorting, deprecated `typing.List`/`Dict`/`Optional`).

### Added

- `Makefile` with `test`, `lint`, and `format` targets.

## [0.1.0] - 2026-10-16

### Added

- Universal LLM wrapper (`core/llm_client.py`) with multi-provider routing for OpenAI, Anthropic, and Google Gemini.
- Automatic retry and exponential backoff via `tenacity`.
- Versioned prompt builder and optimizer (`tools/prompt_builder/`) with registry, builder, and meta-prompting optimizer.
- Versioned JSON prompt templates (`code_refactor`, `meta_optimizer`).
- YAML-based configuration management (`config/settings.py`) with local consumer override support.
- uv-based packaging and consumer source overrides (editable local and GitHub remote).
- Unit tests for LLM calls, backoff retries, prompt versioning, and optimization.
- README with setup and consumer usage instructions.

[Unreleased]: https://github.com/your-username/ai-tools/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/your-username/ai-tools/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/your-username/ai-tools/releases/tag/v0.1.0
