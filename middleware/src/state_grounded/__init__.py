"""State-Grounded LLM Honeypot — middleware package.

Maintains an authoritative model of the attacker's session state and grounds
the local LLM in that state. Week 1 ships the package skeleton + a runnable
demo; the full engine arrives in Weeks 2-4 (see docs/WEEK1-REPORT.md).
"""

__version__ = "0.1.0"

from .config import Config
from .state_engine import StateEngine, StateSnapshot

__all__ = ["Config", "StateEngine", "StateSnapshot", "__version__"]
