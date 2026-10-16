# AI Tools Package (`ai-tools`)

A modular, reusable Python package designed to power AI-driven applications with a robust core and structured tool suites.

## Core Features

1. **Universal LLM Wrapper (`core/llm_client.py`)**:
   - Supports multi-provider routing (**OpenAI**, **Anthropic**, and **Google Gemini**).
   - Supports multiple models per provider configured via YAML settings.
   - Built-in automatic retry and exponential backoff error handling using **`tenacity`**.
2. **Versioned Prompt Builder & Optimizer (`tools/prompt_builder/`)**:
   - **Registry**: Loads versioned prompt JSON templates (`v1.json`, `latest.json`).
   - **Builder**: Safe string interpolation for dynamic runtime variables.
   - **Optimizer**: Meta-prompting engine that rewrites raw user drafts into production-grade prompts.
3. **Flexible Configuration Management (`config/settings.py`)**:
   - Parses multi-model catalogs from `settings.yaml`.
   - Supports local project overrides so consumer projects can customize defaults seamlessly without modifying the package source.

## Installation & Setup (Using uv)

1. Clone or place this repository locally.

2. Initialize and sync the virtual environment using uv:

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

3. Create a `.env` file in your root directory with your provider API keys:

   ```dotenv
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GEMINI_API_KEY=AIza...
   ```

## Usage in Consumer Projects

You can consume `ai-tools` in your downstream applications using one of two methods via uv's source overrides (`[tool.uv.sources]`):

### Method 1: Local Development (Editable Mode)

Use this when `ai-tools` and your consumer app live side-by-side on your machine. Code changes in `ai-tools` will instantly reflect in your app.

In your consumer app's `pyproject.toml`:

```toml
[project]
name = "my-cool-app"
version = "0.1.0"
dependencies = [
    "ai-tools",
]

[tool.uv.sources]
ai-tools = { path = "../ai-tools", editable = true }
```

Run `uv sync` inside your consumer project directory.

### Method 2: Remote Production (From GitHub)

Use this when deploying or sharing code across teams, pulling directly from a remote GitHub repository.

In your consumer app's `pyproject.toml`:

```toml
[project]
name = "my-cool-app"
version = "0.1.0"
dependencies = [
    "ai-tools",
]

[tool.uv.sources]
ai-tools = { git = "https://github.com/your-username/ai-tools.git", branch = "main" }
```

Run `uv sync` inside your consumer project directory.
