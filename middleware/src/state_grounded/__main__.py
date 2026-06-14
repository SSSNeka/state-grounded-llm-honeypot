"""Runnable demo (the Week 1 "Hello World").

Replays a short scripted session through the state engine and prints, after
each command, the grounded system prompt the LLM *would* receive. This proves
the snapshot/grounding flow end-to-end on sample data, with no Cowrie or Ollama
required yet.

Run:  python -m state_grounded
"""

from __future__ import annotations

from .config import Config
from .prompt_grounding import build_grounded_prompt
from .state_engine import StateEngine

DEMO_SESSION = [
    "pwd",
    "mkdir /tmp/x",
    "cd /tmp",
    "ls",
    "cd /tmp/x",
    "pwd",
    "uname -a",  # non-deterministic → would defer to the LLM
]


def main() -> None:
    config = Config.from_env()
    engine = StateEngine()

    print("=" * 64)
    print(" State-Grounded LLM Honeypot — Week 1 demo")
    print(f" model={config.ollama_model}  fast_path={config.fast_path}  "
          f"grounding={config.prompt_grounding}")
    print("=" * 64)

    for command in DEMO_SESSION:
        print(f"\n$ {command}")
        result = engine.try_fast_path(command) if config.fast_path else None
        if result is not None:
            if result:
                print(result)
            print(f"  [fast-path · no LLM call · exit={engine.last_exit_code}]")
        else:
            print("  [would call LLM — grounded prompt below]")
            grounded = build_grounded_prompt(engine.snapshot(), config)
            for line in grounded.splitlines():
                print(f"  | {line}")

    print("\n" + "-" * 64)
    print("Final snapshot:")
    for line in engine.snapshot().to_prompt_block().splitlines():
        print(f"  {line}")
    print("\nDemo OK. Engine/grounding skeleton runs end-to-end. ✅")


if __name__ == "__main__":
    main()
