"""Reproducible evaluation harness — runner (WEEK 1 SKELETON).

Replays versioned scripted attacker sessions against a target backend
(`vanilla` Cowrie LLM backend or our `grounded` build) and scores the metrics
defined in README.md: state consistency, detectability, latency, LLM call rate.

Week 1 ships the CLI shape, session loader, and metric stubs so the team has a
stable interface and the topology is documented. The scoring logic + Cowrie
driver are implemented in Week 1's later half / Week 5.

Usage (planned):
    python run_baseline.py --backend vanilla  --out results/before.json
    python run_baseline.py --backend grounded --out results/after.json
"""

from __future__ import annotations

import argparse
import glob
import json
import os

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")


def load_sessions(path: str = SESSIONS_DIR) -> list[dict]:
    """Load every versioned scripted session (JSON) from the sessions dir."""
    sessions = []
    for f in sorted(glob.glob(os.path.join(path, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            sessions.append(json.load(fh))
    return sessions


def run(backend: str, sessions: list[dict]) -> dict:
    """Replay sessions against `backend` and compute metrics.

    TODO(week1b/week5): drive the real backend, capture per-command output and
    latency, then compute:
      - state_consistency_rate  (matched expectations / total state checks)
      - detection_signals       (honeypot-fingerprint heuristics tripped)
      - latency_p50 / latency_p95
      - llm_call_rate           (LLM calls / total commands; fast-path lowers it)
    """
    raise NotImplementedError(
        "Scoring + backend driver land later (see TODO). Week 1 ships the "
        "harness skeleton, CLI, and session loader."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="State-grounded honeypot harness")
    parser.add_argument("--backend", choices=["vanilla", "grounded"], required=True)
    parser.add_argument("--out", default="results/run.json")
    args = parser.parse_args()

    sessions = load_sessions()
    print(f"Loaded {len(sessions)} scripted session(s) from {SESSIONS_DIR}")
    for s in sessions:
        print(f"  - {s['id']}: {s['description']}")

    print(f"\nBackend '{args.backend}' scoring is not implemented yet (Week 1 skeleton).")
    print("Session loader works; metric computation lands per the roadmap.")
    # results = run(args.backend, sessions)  # enabled when scoring is implemented


if __name__ == "__main__":
    main()
