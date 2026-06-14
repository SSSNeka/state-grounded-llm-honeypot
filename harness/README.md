# Evaluation Harness

Reproducible, before/after benchmark for the state-grounding contribution. It
replays a **versioned set of scripted attacker sessions** against a target
backend and scores four metrics. Using scripted sessions (rather than waiting
to catch a live attacker) makes the result reproducible within the 6-week window.

## Metrics

| Metric | What it measures | How |
|---|---|---|
| **State Consistency Rate** | Output agrees with true session state | Sessions mutate FS/cwd/env, then verify; share of consistent responses |
| **Detection / Fingerprintability** | How easily the trap is spotted | Honeypot-detection heuristics (state mismatches, anomalies) + latency distribution; share of tripped signals |
| **Latency (p50/p95) + LLM call rate** | Performance & cost | Share of commands served deterministically without the LLM; timings |
| **Engagement (secondary)** | Attacker engagement depth | Session length / command count on synthetic sessions |

**Baseline** = vanilla Cowrie LLM backend (same pinned model, no middleware).
**After** = the state-grounded build. Expectation: ↑ consistency, ↓ detection
signals, ↓ p95, ↓ LLM call rate.

## Layout

```
harness/
├── run_baseline.py   # CLI runner + session loader (Week 1 skeleton)
├── sessions/         # versioned scripted attacker sessions (JSON)
└── results/          # generated before/after results (git-ignored)
```

## Usage (planned)

```bash
python run_baseline.py --backend vanilla  --out results/before.json
python run_baseline.py --backend grounded --out results/after.json
```

Week 1 ships the CLI, the session format, a sample session, and the loader.
Scoring + the Cowrie driver are implemented per the roadmap (see
`../docs/WEEK1-REPORT.md`).
