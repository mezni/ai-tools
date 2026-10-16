# examples/test_prompt_builder_app.py
from tools.prompt_builder.builder import PromptBuilder
from tools.prompt_builder.optimizer import PromptOptimizer


def main():
    print("=== Testing Prompt Builder ===")
    builder = PromptBuilder()
    rendered_prompt = builder.build(
        prompt_name="code_refactor",
        version="v1",
        language="python",
        code="def add(a, b): return a + b",
    )
    print(rendered_prompt)
    print("\n" + "=" * 40 + "\n")

    print("=== Testing Prompt Optimizer (Meta-Prompting) ===")
    print("(Note: Requires active API key configured in .env)")
    optimizer = PromptOptimizer()
    try:
        result = optimizer.optimize(
            raw_prompt="write a script to scrape product prices from an e-commerce site"
        )
        print("Optimized Prompt:\n", result.get("optimized_prompt"))
        print("\nStrategies Applied:", result.get("strategies_applied"))
        print("Explanation:", result.get("explanation"))
    except Exception as e:  # noqa: BLE001
        print(f"Skipped live optimization call due to missing API key / connection: {e}")


if __name__ == "__main__":
    main()
