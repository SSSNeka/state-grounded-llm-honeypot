# Admin Dashboard (planned — Weeks 3-6)

A read-only admin dashboard giving the operator a live view of **all
interactions with the honeypot**: sessions, source IPs, the full command
timeline per session, and whether each command was served by the deterministic
**fast-path** or the grounded **LLM**.

> **Status:** Week 1 — documentation only. No code yet. This directory holds the
> plan; implementation starts Week 3 (see `docs/BACKLOG.md`, IDs SGLH-24…29).

## Stack

- **Backend:** FastAPI (Python) — reads Cowrie's structured JSON event log
  (`cowrie.json`), groups events into sessions, exposes REST + a WebSocket live
  feed. Optional SQLite index for analytics.
- **Frontend:** React + Vite — sessions list, per-session command timeline,
  analytics view.

## Planned structure

```
dashboard/
├── backend/        # FastAPI app
│   ├── app/
│   │   ├── main.py           # routes: /api/sessions, /api/sessions/{id}, /api/stream
│   │   ├── ingest.py         # parse cowrie.json → sessions/commands
│   │   └── models.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/       # React + Vite SPA
    ├── src/
    │   ├── pages/  # SessionsList, SessionTimeline, Analytics
    │   └── api/    # REST + WebSocket client
    ├── package.json
    └── Dockerfile
```

## Why read Cowrie's log instead of a new pipeline

Cowrie already emits rich structured events per command and session. Consuming
that log keeps the dashboard a clean, decoupled add-on and keeps the
upstream-able Cowrie changes minimal. The middleware tags each command with its
serving path (fast-path vs LLM) so the dashboard can surface the contribution in
real traffic.

API contract + low-fidelity wireframe: [`../docs/api/dashboard-api.md`](../docs/api/dashboard-api.md).
