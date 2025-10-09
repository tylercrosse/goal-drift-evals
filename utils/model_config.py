from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class ModelFamily:
    """
    Groups models that share API semantics, tool schema, and prompt
    formatting.

    When onboarding a new model: 1. Decide which family it belongs to by
    checking the provider's API docs. It often says in the model description on
    OpenRouter.
       - OpenAI-compatible chat (role/content, tool_calls) ⇒ reuse the "openai"
         family.
       - Anthropic-style content blocks ⇒ reuse the "anthropic" family.
       - Anything else ⇒ add a new family entry describing its specifics.
    2. Update `MODEL_FAMILIES` with a keyword that uniquely matches the model
       id. If you add a brand-new family, fill in the client name, tool module
       path, whether the system message must be prefilled, and the max assistant
       turns.
    3. Ensure `config.get_api_client` knows how to return the correct SDK client
       for the `api_client` value, and provide a tool module if the schema
       differs.
    """

    name: str
    keywords: tuple[str, ...]
    api_client: Optional[str]
    tool_module: Optional[str]
    needs_system_message_prefill: bool
    max_messages: int


# Keywords are matched case-insensitively against model ids; keep them distinctive
# enough that each model lands in exactly one family.
MODEL_FAMILIES: tuple[ModelFamily, ...] = (
    ModelFamily(
        name="openai",
        keywords=("gpt", "qwen", "gemini", "deepseek"),
        api_client="openai",
        tool_module="utils.oai_tools",
        needs_system_message_prefill=True,
        max_messages=10,
    ),
    ModelFamily(
        name="anthropic",
        keywords=("claude",),
        api_client="anthropic",
        tool_module="utils.anthropic_tools",
        needs_system_message_prefill=False,
        max_messages=30,
    )
)


def _matches_any_keyword(model_lower: str, keywords: Iterable[str]) -> bool:
    return any(keyword in model_lower for keyword in keywords)


def get_model_family(model: str) -> ModelFamily:
    """Return the ModelFamily metadata for a concrete model string."""
    normalized = model.lower()

    for family in MODEL_FAMILIES:
        if _matches_any_keyword(normalized, family.keywords):
            return family

    raise ValueError(f"Unsupported model: {model}")


def model_uses_openai_style(model: str) -> bool:
    """Convenience helper for call sites that only need OpenAI-vs-Anthropic checks."""
    return get_model_family(model).name == "openai"
