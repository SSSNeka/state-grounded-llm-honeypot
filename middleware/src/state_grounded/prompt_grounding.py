"""Prompt grounding: inject the live state snapshot into the LLM context.

WEEK 1 SCAFFOLD: builds the grounded prompt string. The actual Ollama call and
response normalization are wired in Week 4 (TODO markers below).
"""

from __future__ import annotations

from .config import Config
from .state_engine import StateSnapshot

BASE_SYSTEM_PROMPT = (
    "You are a Linux shell. Respond ONLY with the exact terminal output of the "
    "user's command — no explanations, no markdown. Stay in character at all times."
)


def build_grounded_prompt(snapshot: StateSnapshot, config: Config) -> str:
    """Compose the system prompt fed to the LLM before each generation."""
    if not config.prompt_grounding:
        return BASE_SYSTEM_PROMPT
    return f"{BASE_SYSTEM_PROMPT}\n\n{snapshot.to_prompt_block()}"


def generate(command: str, snapshot: StateSnapshot, config: Config) -> str:
    """Generate a response for a non-deterministic command.

    TODO(week4): POST to {config.ollama_host}/api/generate with the grounded
    prompt and {config.ollama_model}; then run response normalization (light
    check for gross contradictions with the snapshot).
    """
    raise NotImplementedError(
        "LLM generation lands in Week 4 (prompt grounding). "
        "Week 1 ships the prompt builder only."
    )
