"""Week 1 smoke tests — confirm the scaffold is wired correctly and runnable.

Run from the middleware/ directory:  python -m pytest
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from state_grounded import Config, StateEngine, __version__  # noqa: E402
from state_grounded.prompt_grounding import build_grounded_prompt  # noqa: E402


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_config_defaults() -> None:
    cfg = Config()
    assert cfg.ollama_model
    assert cfg.fast_path is True


def test_fast_path_mkdir_then_ls_is_consistent() -> None:
    """The core promise: created dirs show up later (no state drift)."""
    eng = StateEngine()
    assert eng.try_fast_path("mkdir /tmp/x") == ""
    eng.try_fast_path("cd /tmp")
    assert "x" in eng.try_fast_path("ls")  # vanilla LLM honeypots forget this


def test_cd_pwd_tracks_directory() -> None:
    eng = StateEngine()
    eng.try_fast_path("mkdir /tmp/x")
    eng.try_fast_path("cd /tmp/x")
    assert eng.try_fast_path("pwd") == "/tmp/x"


def test_cd_missing_dir_sets_error_exit_code() -> None:
    eng = StateEngine()
    out = eng.try_fast_path("cd /nope")
    assert "No such file" in out
    assert eng.last_exit_code == 1


def test_nondeterministic_command_defers_to_llm() -> None:
    eng = StateEngine()
    assert eng.try_fast_path("uname -a") is None


def test_grounded_prompt_contains_state() -> None:
    eng = StateEngine()
    eng.try_fast_path("cd /tmp")
    prompt = build_grounded_prompt(eng.snapshot(), Config())
    assert "cwd: /tmp" in prompt
