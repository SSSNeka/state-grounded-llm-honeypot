# Architecture

## Data flow

```
attacker ──► Cowrie session ──► [State Middleware] ──► Ollama (local LLM)
                  │                   │   ▲
                  │                   ▼   │
                  │           authoritative session state:
                  │           - virtual filesystem (created/deleted/modified)
                  │           - cwd, env vars, exit code ($?), users
                  │           - process table / PIDs
                  │                   │
                  │                   ▼
                  │       prompt grounding: state snapshot injected
                  │       into the LLM context before each generation
                  │
                  ▼
        Cowrie JSON event log (cowrie.json)
                  │
                  ▼
        [Dashboard backend: FastAPI]  ──REST + WebSocket──►  [Dashboard frontend: React]
        parses events → sessions/commands                    sessions list · command
        (optional SQLite index)                              timeline · analytics
                                                             (admin operator)
```

## Components

1. **State engine** (`middleware/src/state_grounded/state_engine.py`)
   A lightweight, authoritative model of the session. Deterministic commands
   (`cd`, `pwd`, `mkdir`, `rm`, `touch`, `export`, `whoami`, `echo $VAR`,
   `ls` on known paths) update the state and are answered **directly** — no LLM
   call. This is both accuracy (no drift) and speed (fewer/zero LLM calls).

2. **Prompt grounding** (`middleware/src/state_grounded/prompt_grounding.py`)
   Before each LLM generation, a fresh snapshot (cwd, files here, env vars, last
   exit code) is injected into the system prompt, so the model answers within
   the true reality of the session instead of hallucinating.

3. **Response normalization** *(MVP boundary)*
   A light check for gross contradictions with state. A full output
   validator / refusal scrubber is a stretch goal.

4. **Admin dashboard** (`dashboard/`, built Weeks 3-6)
   - **Backend (FastAPI):** tails/parses Cowrie's structured JSON event log
     (`cowrie.json`), groups events into sessions, and exposes a REST API
     (`/api/sessions`, `/api/sessions/{id}`) plus a WebSocket live feed
     (`/api/stream`). An optional SQLite index is added only if needed for
     analytics performance. See [`api/dashboard-api.md`](api/dashboard-api.md).
   - **Frontend (React + Vite):** three core screens — sessions list, per-session
     command timeline (with a fast-path-vs-LLM badge per command), and an
     analytics view. Read-only; no attacker-facing surface.
   - **Why read the log instead of a new pipeline:** Cowrie already emits rich
     structured events, so the dashboard stays a clean, decoupled add-on and the
     upstream-able Cowrie changes remain minimal.

## Design decisions

- **Deterministic-first.** Whatever can be computed exactly is computed exactly;
  the LLM is the fallback for genuinely open-ended output. This directly attacks
  the documented weakness (state drift) and lowers the timing fingerprint.
- **Self-hosted / local-only.** The LLM runs on the deployer's machine via
  Ollama; no external APIs. Privacy and reproducibility.
- **Single repo, one command.** Cowrie + Ollama + middleware via Docker Compose;
  model weights pulled with `ollama pull` at setup, never committed to git.
- **Pinned model.** The model version is pinned for reproducible before/after
  measurements.

## Interfaces (Week 1 contracts)

- `StateEngine.try_fast_path(command) -> str | None`
  Returns the exact output for a deterministic command, or `None` to defer to
  the LLM.
- `StateEngine.snapshot() -> StateSnapshot`
  Current authoritative state.
- `build_grounded_prompt(snapshot, config) -> str`
  The system prompt fed to the LLM.

The HTTP/contract surface against Cowrie's LLM backend is captured in
[`api/llm-backend-contract.md`](api/llm-backend-contract.md).
