# Product Backlog & Kanban

Prioritized backlog for the 6-week build. Priorities: **P0** (must, MVP), **P1**
(should), **P3** (stretch — only if time allows). Importable version:
[`backlog.csv`](backlog.csv) (Trello / Jira / GitHub Projects).

> **Live board:** [Linear — CAP](https://linear.app/capstone-inno/team/CAP/active).
> This file mirrors it; the CSV maps directly to Linear / Jira / GitHub Projects columns.

## Kanban snapshot (Week 1)

### ✅ Done
- **SGLH-3** · Setup · Repo scaffold (structure, README, .gitignore, LICENSE, runnable demo) · P0
- **SGLH-4** · Setup · Docker support (Dockerfile per component + docker-compose.yml) · P0

### 🔄 In Progress
- **SGLH-5** · Harness · Define scripted-session format + versioned sample sessions · P0

### 📋 Todo (this week, P0)
- **SGLH-1** · Setup · Fork Cowrie; run its LLM backend against local Ollama
- **SGLH-2** · Setup · Select & pin the LLM (`qwen2.5:3b` default; 7-8B candidates)
- **SGLH-6** · Harness · Implement session runner + metric scoring
- **SGLH-7** · Harness · Record baseline ("before") on vanilla Cowrie + LLM

### 🗓 Backlog (later weeks)

| ID | Epic | Story | Pri | Week |
|---|---|---|---|---|
| SGLH-8 | State Engine | Virtual filesystem model (create/delete/modify) | P0 | 2 |
| SGLH-9 | State Engine | Track cwd + basic env vars | P0 | 2 |
| SGLH-10 | State Engine | Deterministic fast-path (`cd pwd mkdir rm touch ls`) | P0 | 2 |
| SGLH-11 | State Engine | env (`export`/`echo $VAR`), `$?`, `whoami`, process table | P0 | 3 |
| SGLH-12 | Integration | Integrate engine into Cowrie LLM command flow | P0 | 3 |
| SGLH-24 | Dashboard | FastAPI backend: read Cowrie JSON log; `/api/sessions` + `/api/sessions/{id}` | P0 | 3 |
| SGLH-13 | Grounding | Inject state snapshot into LLM prompt | P0 | 4 |
| SGLH-14 | Grounding | Basic response normalization | P1 | 4 |
| SGLH-15 | Grounding | End-to-end multi-turn smoke tests | P0 | 4 |
| SGLH-25 | Dashboard | Live events feed (WebSocket `/api/stream`) | P0 | 4 |
| SGLH-26 | Dashboard | React UI: sessions list (IP, start time, command count) | P0 | 4 |
| SGLH-27 | Dashboard | React UI: per-session command timeline + fast-path/LLM badge | P0 | 4 |
| SGLH-16 | Evaluation | "After" numbers + before/after comparison | P0 | 5 |
| SGLH-17 | Evaluation | Ablation study (each component's contribution) | P0 | 5 |
| SGLH-18 | Evaluation | Charts + results write-up | P1 | 5 |
| SGLH-28 | Dashboard | Analytics view (commands/session, LLM call rate, top commands) | P1 | 5 |
| SGLH-19 | Packaging | One-command Compose deploy (full stack) | P0 | 6 |
| SGLH-29 | Dashboard | Add dashboard to Compose; basic error handling | P0 | 6 |
| SGLH-20 | Packaging | README sysreqs + setup; CI/tests | P1 | 6 |
| SGLH-21 | Delivery | Record demo (vanilla vs grounded) | P0 | 6 |
| SGLH-22 | Delivery | Upstream PR/issue to Cowrie; finalize report | P0 | 6 |
| SGLH-23 | Stretch | Refusal scrubber / output validator / latency norm / PI defense / TI enrichment | P3 | 6 |

## Definition of Done (per story)
Code merged via PR · unit/smoke tests pass · CI green · docs updated · no
secrets/model weights committed.
