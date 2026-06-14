# Admin Dashboard — API Contract & Wireframe (planned, W3-6)

Read-only dashboard over the honeypot's interaction stream. Backend = FastAPI,
frontend = React + Vite. Data source = Cowrie's structured JSON event log
(`cowrie.json`); the middleware tags each command with its serving path
(`fast-path` vs `llm`).

## REST API

### `GET /api/sessions`
List sessions (most recent first). Query: `?limit=50&offset=0`.

```json
[
  {
    "session_id": "a1b2c3",
    "src_ip": "203.0.113.7",
    "started_at": "2026-06-14T10:00:01Z",
    "ended_at": "2026-06-14T10:03:12Z",
    "command_count": 14,
    "llm_calls": 5,
    "fast_path_calls": 9
  }
]
```

### `GET /api/sessions/{session_id}`
Full command timeline for one session.

```json
{
  "session_id": "a1b2c3",
  "src_ip": "203.0.113.7",
  "commands": [
    {
      "ts": "2026-06-14T10:00:05Z",
      "input": "mkdir /tmp/x",
      "output": "",
      "served_by": "fast-path",
      "exit_code": 0
    },
    {
      "ts": "2026-06-14T10:00:09Z",
      "input": "uname -a",
      "output": "Linux svr01 5.15.0 ...",
      "served_by": "llm",
      "exit_code": 0
    }
  ]
}
```

### `WS /api/stream`
WebSocket; pushes new command/session events as they occur:

```json
{ "type": "command", "session_id": "a1b2c3", "input": "ls", "served_by": "fast-path", "ts": "..." }
```

### `GET /api/stats` (analytics, W5)
```json
{ "total_sessions": 128, "total_commands": 1422, "llm_call_rate": 0.36,
  "avg_commands_per_session": 11.1, "top_commands": [["ls", 210], ["cat", 142]] }
```

Errors: standard HTTP codes; empty/missing log returns `200` with `[]` (handled
gracefully, no 500). No attacker-facing surface.

## Low-fidelity wireframe

```
┌──────────────────────────────────────────────────────────────┐
│  State-Grounded Honeypot — Admin            ● live (WS)        │
├──────────────┬───────────────────────────────────────────────┤
│ SESSIONS     │  SESSION a1b2c3  ·  203.0.113.7  ·  14 cmds     │
│ (auto-update)│  ───────────────────────────────────────────── │
│              │  10:00:05  $ mkdir /tmp/x        [fast-path] ✓0 │
│ ▸ a1b2c3 14  │  10:00:07  $ cd /tmp            [fast-path] ✓0 │
│   203.0.113.7│  10:00:08  $ ls                  [fast-path] ✓0 │
│              │            x                                    │
│ ▸ d4e5f6  3  │  10:00:09  $ uname -a                 [LLM] ✓0 │
│   198.51.100.9            Linux svr01 5.15.0 ...               │
│              │                                                 │
│ [ Analytics ]│  commands: 14   LLM: 5 (36%)   fast-path: 9     │
└──────────────┴───────────────────────────────────────────────┘
```

Three core screens: **Sessions list** (left, live), **Session timeline**
(right, with per-command `fast-path`/`LLM` badge + exit code), **Analytics**
(metrics + charts, W5). Maps to user stories US-8…US-11 and backlog SGLH-24…29.
