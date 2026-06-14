# Week 1 Report — Planning, Setup & MVP Start

**Project:** State-Grounded LLM Honeypot (Cowrie + Ollama)
**Track:** Industrial
**Week:** 1 of 6 · **Date:** 2026-06-14

> Fill the `[bracketed]` placeholders (team names, channels, repo/PR links) with
> your real values before submitting.

---

## 1. Team & Roles

The proposal defines four role areas (Cowrie/Python engineering, ML/LLM, Cybersecurity/QA, and shared docs/CI). With **6 members** we split those areas so every core epic has a clear owner and a backup.

| # | Member | Email | Primary role | Responsibilities |
|---|---|---|---|---|
| 1 | [Nikita Serov] | [n.serov@innopolis.university] | Team Lead / Backend | Coordination, planning, Cowrie integration, upstream PR |
| 2 | [Pavel Troshkin] | [p.troshkin@innopolis.university] | Backend / State Engine | Virtual filesystem, cwd/env model, deterministic fast-path |
| 3 | [Maksim Kalinin] | [ma.kalinin@innopolis.university] | Integration / Dashboard Backend | Wire state engine into Cowrie LLM command flow; FastAPI dashboard backend |
| 4 | [Egor Neialov] | [e.neialov@innopolis.universityl] | ML / LLM Engineer | Ollama setup, model selection/pinning, prompt grounding |
| 5 | [Aresenii Boiko] | [ar.boiko@innopolis.university] | QA / Evaluation | Harness, scripted sessions, metrics, before/after + ablation |
| 6 | [Denis Safin] | [d.safin@innopolis.university] | DevOps / Dashboard Frontend | Docker/Compose, CI, README, system requirements, demo; React admin dashboard UI |

Roles are primary, not exclusive — pairs back each other up.

---

## 2. Course Familiarization

The team reviewed the project guidelines, the three track definitions (Research / Startup / Industrial), and the grading rubric, and agrees on a shared reading of expectations:

- The deliverable must be a **non-trivial contribution to an existing product**, demonstrably implemented, **measurable against a baseline**, with **impact beyond the course grade**, and meeting basic quality/documentation/usability standards. This maps cleanly to the **Industrial** track.
- Because the contribution is proven empirically (before/after benchmark, ablation), we also adopt **research-style evaluation artifacts** (research questions, methodology, metrics, baselines) alongside the Industrial user stories — included in §5.

---

## 3. Project & Track Statement

### 3.1 Chosen project

**State-Grounded LLM Honeypot** — a self-hosted deception layer for the Cowrie SSH/Telnet honeypot with an embedded **local** LLM (via Ollama). It adds a **state-tracking middleware** between the attacker session and the LLM that maintains an authoritative model of the system (virtual filesystem, cwd, environment variables, exit codes, process table) and injects a fresh state snapshot into the LLM context before every generation. It also ships an **admin dashboard** (FastAPI + React) that gives the operator a live view of every interaction with the honeypot — sessions, commands, and how each command was served (deterministic fast-path vs. grounded LLM).

### 3.2 Chosen track

**Industrial** — we extend an existing open-source product (Cowrie) with a non-trivial architectural contribution and aim to upstream it.

### 3.3 Problem statement

LLM-powered honeypots already exist (Cowrie ships an experimental LLM backend; shelLM, Beelzebub, and Galah are standalone projects), so "adding an LLM" is no longer a contribution. They share one documented weakness: **state drift in multi-turn sessions**. The model keeps only a short window of recent commands in context, so it forgets created/deleted files, loses the current directory, and contradicts the session's real environment — e.g. after `mkdir /tmp/x` a later `ls /tmp` may not show `x`, and `cd /var && pwd` may lie. These inconsistencies are the **cheapest way for an attacker to fingerprint and abandon the trap**. We eliminate this drift with an authoritative state engine and prompt grounding, and prove the effect with reproducible before/after measurements.

### 3.4 Point-by-point justification against Industrial acceptance criteria

| Criterion | How the project satisfies it |
|---|---|
| **Existing product/project** | **Cowrie** SSH/Telnet honeypot and its experimental LLM backend (BSD-3). We fork it rather than build a new honeypot. |
| **Gap / issue / opportunity** | **State drift in multi-turn LLM sessions** — a concrete, reproducible defect (forgotten files, wrong cwd, env contradictions) that enables honeypot fingerprinting. Confirmed by recent literature (SoK: Honeypots & LLMs 2025; LLMHoney; HoneyGPT; shelLM). |
| **Non-trivial contribution** | An **architectural state-tracking middleware**: authoritative session-state engine + deterministic fast-path + prompt grounding integrated into Cowrie's LLM command flow. This is design work, not tool gluing. |
| **Integrates into the target system** | Plugs directly into Cowrie's LLM backend command flow; deterministic commands answered by the engine, the rest grounded before the LLM call. |
| **Measurable effect** | Before/after on a reproducible harness: ↑ state consistency, ↓ detectability/fingerprinting signals, ↓ latency p95, ↓ LLM call rate — plus an ablation isolating each component. |
| **Impact beyond course grading** | Real value to Cowrie and its users (harder-to-detect honeypot, lower compute), delivered as an **upstream PR/issue** to `cowrie/cowrie`. |
| **Quality / documentation / usability** | Single-repo one-command Docker Compose deploy, pinned model, unit tests, CI (GitHub Actions), README with system requirements. |

**Related work / gap citations:** SoK: Honeypots & LLMs 2025 ([arXiv:2510.25939](https://arxiv.org/html/2510.25939v3)); LLMHoney ([arXiv:2509.01463](https://arxiv.org/html/2509.01463v1)); HoneyGPT ([arXiv:2406.01882](https://arxiv.org/html/2406.01882)); shelLM / "LLM in the Shell" ([arXiv:2309.00155](https://arxiv.org/abs/2309.00155)); [Cowrie LLM backend docs](https://docs.cowrie.org/en/stable/LLM.html); [Cowrie repo](https://github.com/cowrie/cowrie).

---

## 4. Project Plan

### 4.1 Week-by-week roadmap

| Week | Focus | Build / investigate | Deliverable |
|---|---|---|---|
| **1** | Setup, baseline & harness | Fork Cowrie; run LLM backend on local Ollama; pin model; build harness + scripted sessions; scaffold + Docker | Reproducible harness + documented baseline ("before"); runnable scaffold |
| **2** | State tracker (part 1) | Virtual filesystem model; cwd + basic env; deterministic fast-path (`cd pwd mkdir rm touch ls`) | Working FS+cwd engine with unit tests |
| **3** | State tracker (part 2) + integration + **dashboard backend** | `export`/`echo $VAR`, `$?`, `whoami`, process table; integrate into Cowrie command flow; **FastAPI backend that reads Cowrie's JSON event log and exposes a REST + WebSocket events API** | Full engine integrated; deterministic commands answered without the LLM; dashboard API serving live events |
| **4** | Prompt grounding + **dashboard frontend** | Inject state snapshot into LLM prompt; basic response normalization; multi-turn smoke tests; **React UI: live sessions list, per-session command timeline, fast-path-vs-LLM indicator** | State-grounded "after" build, end-to-end; dashboard showing live interactions |
| **5** | Measurement & ablation + **dashboard analytics** | Run full harness on "after"; before/after comparison; ablation; charts; **dashboard metrics view (commands/session, LLM call rate, top commands)** | Before/after report with charts + ablation; dashboard with analytics |
| **6** | Packaging, demo & upstream | One-command Compose deploy **incl. dashboard**; README/sysreqs; CI; demo recording (showing the dashboard); upstream PR | Self-hosted package, demo, docs, PR, final report |

### 4.2 Milestones

| Week | Milestone |
|---|---|
| 1 | Harness + baseline ("before") captured |
| 2–3 | State engine implemented & integrated into Cowrie |
| 3 | Dashboard backend serving live honeypot events |
| 4 | Prompt grounding → working "after" build; dashboard UI showing live interactions |
| 5 | Before/after results + ablation; dashboard analytics view |
| 6 | Self-hosted package (incl. dashboard) + demo + upstream PR |

### 4.3 Dependencies

- Harness scoring (W1) and baseline numbers depend on Cowrie+Ollama running (W1).
- Cowrie integration (W3) depends on the state engine (W2).
- Prompt grounding (W4) depends on integration (W3).
- Measurement/ablation (W5) depends on the "after" build (W4) **and** the harness (W1).
- **Dashboard backend (W3)** depends on Cowrie emitting structured JSON events (W1 setup); **dashboard frontend (W4)** depends on that backend API.
- Demo + upstream PR (W6) depend on results (W5) and a clean package (W6).

### 4.4 Known risks & mitigations

| Risk | Mitigation |
|---|---|
| Local model latency | Small model (3B default; 7–8B optional) + deterministic fast-path cuts LLM calls |
| Can't catch a live attacker in 6 weeks | Evaluate on our own reproducible scripted sessions; live deploy is a bonus, not a dependency |
| Upstream may not merge in time | An **open PR** + working fork is sufficient for grading; merge is out of our control |
| Scope creep | Required MVP = state tracker + grounding + harness + measurements + dashboard; everything in §7 of the proposal stays stretch-only |
| **Dashboard competes with core for time** | Dashboard is sequenced **after** the engine (W3-6) and reads Cowrie's existing JSON log (no new capture pipeline), so it never blocks the measurable core contribution |
| Hardware constraints | Budget ~10 GB disk + ~4 GB (3B) / ~6–8 GB (7–8B) RAM/VRAM; documented in README |

### 4.5 Backlog (Kanban)

Prioritized backlog: [`BACKLOG.md`](BACKLOG.md) · importable [`backlog.csv`](backlog.csv).
**Live board:** [Linear — CAP](https://linear.app/capstone-inno/team/CAP/active).

---

## 5. Requirements

This is an Industrial-track project with a strong evaluation component, so we provide **both** user stories (Industrial) **and** research-style artifacts (for the measurement).

### 5.1 User stories

| ID | As a… | I want to… | so that… |
|---|---|---|---|
| US-1 | honeypot operator | deploy the whole system with one command | I can run it without manual wiring |
| US-2 | honeypot operator | run the LLM locally (no external API) | attacker data and prompts never leave my machine |
| US-3 | honeypot operator | pin the model version | my results are reproducible |
| US-4 | attacker (adversary model) | get **consistent** shell output across many turns | *(this is what we must defeat — the trap should not reveal itself via state drift)* |
| US-5 | security researcher | run a before/after benchmark | I can quantify the consistency/detectability improvement |
| US-6 | Cowrie maintainer | review a clean, tested PR | the contribution can be merged upstream |
| US-7 | operator on weak hardware | use a small model with a deterministic fast-path | the honeypot stays responsive and cheap |
| US-8 | honeypot operator | see all interactions on an **admin dashboard** (sessions, source IP, commands, timestamps) | I can monitor attacker activity at a glance |
| US-9 | honeypot operator | drill into a single session's command timeline | I can follow exactly what an attacker did, step by step |
| US-10 | honeypot operator | see whether each command was served by the **fast-path or the LLM** | I can observe the contribution working in real traffic |
| US-11 | honeypot operator | watch new interactions appear **live** | I can react to active intrusions without refreshing |

**Acceptance criteria (key stories):**

- **US-1** — `cp .env.example .env && docker compose up` brings Cowrie + Ollama + middleware online; the model is pulled at setup; documented in README.
- **US-2** — No outbound calls to third-party LLM APIs; Ollama runs in-stack; verified by network inspection.
- **US-4 (defeated drift)** — In scripted multi-turn sessions, created/deleted files, cwd, and env remain consistent; `mkdir /tmp/x` → later `ls /tmp` shows `x`; `cd /var && pwd` returns `/var`. Measured by **State Consistency Rate**.
- **US-5** — `run_baseline.py --backend {vanilla|grounded}` produces comparable JSON results for all four metrics; a before/after table + ablation are generated.
- **US-7** — Deterministic commands are served without an LLM call; **LLM call rate** and **p95 latency** drop versus baseline.
- **US-8/US-9** — The dashboard lists all sessions with source IP, start time, and command count; clicking a session shows its ordered command/response timeline with timestamps.
- **US-10** — Each command row shows a `fast-path` vs `LLM` badge, sourced from the middleware/Cowrie event log.
- **US-11** — New events appear without a manual refresh (WebSocket/poll); verified by replaying a session while the dashboard is open.

### 5.2 MVP scope

**IN (required):**
- State engine: virtual filesystem, cwd, env vars, exit code, basic process table.
- Deterministic fast-path for common commands (`cd pwd mkdir rm touch ls export echo $VAR whoami`).
- Prompt grounding: state snapshot injected into the LLM context each turn.
- Integration into Cowrie's LLM backend command flow.
- Reproducible harness + versioned scripted sessions; before/after + ablation.
- **Admin dashboard (FastAPI + React): live sessions list, per-session command timeline, fast-path-vs-LLM indicator, and a basic analytics view.**
- One-command Docker Compose deploy (incl. dashboard); pinned local model; README/sysreqs; unit tests + CI.
- Upstream PR/issue to Cowrie.

**OUT (stretch / not required):**
- Refusal scrubber; full output validator with auto-correction; latency normalizer + cache; prompt-injection defense; threat-intel (IoC / MITRE ATT&CK) enrichment.
- Live internet deployment / catching real attackers.
- Multi-model A/B beyond the single pinned model.
- Dashboard extras beyond the core views: authentication/multi-user, alerting/notifications, geolocation maps, historical persistence beyond Cowrie's log retention.

### 5.3 Research-style artifacts (evaluation)

**Research questions / hypotheses**

- **RQ1:** Does an authoritative state engine + prompt grounding measurably increase multi-turn **state consistency** vs. the vanilla Cowrie LLM backend?
- **RQ2:** Does it measurably **reduce honeypot detectability/fingerprintability**?
- **RQ3:** Does the deterministic fast-path **reduce LLM call rate and p95 latency** (and thus the timing fingerprint)?
- **H1–H3:** the grounded build improves consistency (H1), reduces detection signals (H2), and lowers LLM call rate + p95 (H3) versus baseline on the same inputs.

**Methodology** — Controlled before/after on identical inputs. *Baseline:* vanilla Cowrie LLM backend with the same pinned model. *After:* same, plus our middleware. An **ablation** isolates each component (state tracker, prompt grounding, fast-path).

**Dataset / data collection** — A **versioned set of scripted attacker sessions** committed to the repo (FS/cwd/env mutations + verification commands). Format defined Week 1 (sample in `harness/sessions/`). This removes the dependency on catching a live attacker within 6 weeks; a live deploy is an optional bonus.

**Evaluation plan (metrics, baselines, success criteria)**

| Metric | Definition | Baseline | Success |
|---|---|---|---|
| State Consistency Rate | share of responses consistent with true state | vanilla Cowrie LLM | measurable ↑ vs baseline |
| Detection / Fingerprintability | share of honeypot-detection heuristics tripped | vanilla Cowrie LLM | measurable ↓ vs baseline |
| Latency p50/p95 + LLM call rate | timings; share of commands served without the LLM | vanilla Cowrie LLM | ↓ p95 and ↓ LLM call rate |
| Engagement (secondary) | session length / command count | vanilla Cowrie LLM | ≥ baseline (no regression) |

**Related-work / gap analysis** — see §3.4 citations. The gap (state drift enabling fingerprinting) is documented across the cited work; no existing LLM honeypot ships an authoritative state-grounding layer integrated into Cowrie.

---

## 6. Tech Stack (with justification)

| Layer | Choice | Why |
|---|---|---|
| Target product | **Cowrie** (fork of its LLM backend) | The existing product we contribute to; mature, widely used, BSD-3, has the LLM backend we improve |
| Core language | **Python** | Cowrie is Python; keeps the contribution native and upstream-able |
| LLM runtime | **Ollama**, self-hosted/local | Runs open models locally — privacy (nothing leaves the machine) + reproducibility; no external API cost/dependency |
| Model | **`qwen2.5:3b`** default; `qwen2.5:7b` / `llama3.1:8b` candidates | 3B keeps weak hardware responsive; pinned version for reproducible measurements |
| Middleware | Custom **state engine + prompt grounding** (Python) | The non-trivial contribution; deterministic-first design attacks state drift and cuts latency |
| Packaging | **Docker + Docker Compose** | Single-repo, one-command self-hosted deploy; model pulled via `ollama pull` (weights never in git) |
| Evaluation | **Python harness** + versioned scripted sessions | Reproducible before/after; not reliant on live attackers |
| **Dashboard backend** | **FastAPI** (Python) | Same language as the rest of the stack; lightweight async REST + WebSocket for live events; reads Cowrie's structured JSON event log |
| **Dashboard frontend** | **React + Vite** | Component-based SPA for the sessions list / command timeline / analytics; fast dev loop; talks to the FastAPI API over REST + WebSocket |
| **Event source / store** | Cowrie **JSON event log** (+ optional **SQLite** index) | Cowrie already emits structured per-command/session events — we consume those rather than build a new capture pipeline; a small SQLite index is added only if needed for query/analytics performance |
| Quality/tooling | **pytest**, **GitHub Actions** CI, README/sysreqs | Meets Industrial quality/documentation bar; supports a clean upstream PR |

The core honeypot is a server-side layer; the **admin dashboard** adds the only UI (React) and a thin **FastAPI** backend. A heavyweight database is intentionally avoided: the dashboard consumes Cowrie's existing JSON event stream, with an optional SQLite index for analytics. This keeps the dashboard a clean add-on that never blocks the measurable core contribution, and keeps the upstream-able Cowrie changes minimal.

---

## 7. Project Setup (this week)

A fresh repository was scaffolded (the prior week-by-week code folders are set aside; we are starting clean from the plan):

```
state-grounded-llm-honeypot/
├── middleware/   # state engine + prompt grounding (Python) — runnable demo + tests
├── harness/      # evaluation harness skeleton + sample scripted session
├── cowrie/       # Cowrie fork target (+ placeholder Dockerfile/README)
├── dashboard/    # admin dashboard — planned (FastAPI backend + React frontend), built W3-6
├── docs/         # this report, backlog, architecture, API contract
├── scripts/      # pull_model.sh
├── docker-compose.yml   # cowrie + ollama + middleware (+ planned dashboard)
├── .env.example
├── .gitignore · LICENSE · README.md
```

**Runnable boilerplate (Hello World):** `python -m state_grounded` replays a short scripted session through the state engine and prints, after each command, the grounded prompt the LLM *would* receive — proving the snapshot/grounding flow end-to-end on sample data with no Cowrie/Ollama required yet. `python -m pytest` runs green smoke tests (see §9).

**Docker support:** `Dockerfile` for the middleware and a placeholder for Cowrie; `docker-compose.yml` wires **Cowrie + Ollama + middleware**. `docker compose up --build middleware` runs the demo in a container today; the full stack comes online as features land. Model weights are pulled with `scripts/pull_model.sh` at setup — never committed.

---

## 8. Initial Design & Skeleton

- **Architecture & integration contract:** [`ARCHITECTURE.md`](ARCHITECTURE.md) and the initial API/integration contract [`api/llm-backend-contract.md`](api/llm-backend-contract.md) (Backend deliverable — the integration seam with Cowrie's LLM backend and the local Ollama HTTP API; a formal OpenAPI spec is only added if a control/health endpoint is introduced).
- **Backend skeleton:** `state_engine.py` (authoritative state + `try_fast_path`/`snapshot`), `prompt_grounding.py` (snapshot → system prompt), `config.py` (env-driven). Clearly marked `TODO(week2/3/4)` for the work ahead.
- **ML/Research setup:** Ollama service defined in Compose; model pinned via `.env`; experimentation = the harness + versioned scripted sessions. Sample dataset entry in `harness/sessions/sample_fs_consistency.json`; data plan in `harness/README.md`.
- **Dashboard (planned, W3-6):** the structure and contract are documented now; code starts Week 3. Backend = FastAPI reading Cowrie's JSON event log, exposing `GET /api/sessions`, `GET /api/sessions/{id}`, and a `WS /api/stream` live feed (draft in [`api/dashboard-api.md`](api/dashboard-api.md)). Frontend = React/Vite SPA with three core screens: **sessions list**, **session command timeline** (with fast-path/LLM badges), and **analytics**. Low-fidelity screen/flow sketch in [`api/dashboard-api.md`](api/dashboard-api.md). The `dashboard/` directory holds a docs placeholder this week (no code yet).
- **Designers:** no dedicated designer role; the dashboard's low-fidelity wireframe/flow is captured in text/ASCII in the dashboard API doc and will be turned into real screens in W4.

---

## 9. MVP Features Implemented This Week & Functional Journey

The MVP core is the middleware. This week delivers a **runnable vertical slice** of it:

- A working **state engine skeleton** that already defeats the headline failure mode on the deterministic path: `mkdir /tmp/x` → `cd /tmp` → `ls` **shows `x`** (the exact case vanilla LLM honeypots get wrong).
- A **prompt-grounding builder** that renders the live snapshot into the system prompt.
- A **deterministic fast-path** for `pwd`, `cd`, `mkdir`, `ls` answered without any LLM call, with correct exit codes.

**Functional journey (demo output, `python -m state_grounded`):** a scripted session runs end-to-end; deterministic commands are served from state (`[fast-path · no LLM call]`), and a non-deterministic command (`uname -a`) correctly **defers to the LLM** and prints the grounded prompt it would receive. Smoke tests assert the consistency promise:

- `test_fast_path_mkdir_then_ls_is_consistent` — created dir survives later `ls`.
- `test_cd_pwd_tracks_directory` — cwd tracked across `cd`.
- `test_cd_missing_dir_sets_error_exit_code` — correct `$?` on failure.
- `test_nondeterministic_command_defers_to_llm` — `uname -a` → LLM.
- `test_grounded_prompt_contains_state` — snapshot present in prompt.

*(Add a screenshot/GIF of the demo run and `pytest` output here for submission.)*

---

## 10. Links (fill in)

- **Repository:** https://github.com/SSSNeka/state-grounded-llm-honeypot
- **PRs/Issues (skeleton & features):** [PR #… scaffold], [Issue #… harness], [PR #… state engine]
- **API / integration contract:** [`docs/api/llm-backend-contract.md`](api/llm-backend-contract.md)
- **Dashboard API + wireframe (planned):** [`docs/api/dashboard-api.md`](api/dashboard-api.md)
- **Backlog / Kanban board:** [`docs/BACKLOG.md`](BACKLOG.md) · [Linear board](https://linear.app/capstone-inno/team/CAP/active)
- **Dataset / data-collection plan:** [`harness/sessions/`](../harness/sessions) · [`harness/README.md`](../harness/README.md)
- **Experimentation setup / runner:** [`harness/run_baseline.py`](../harness/run_baseline.py)
- **Initial baseline result:** [link once `results/before.json` is produced]
- **Industrial baseline measurement:** vanilla Cowrie LLM backend, same pinned model — captured by the harness (see §5.3).

---

## 11. Internal Demo & Next Steps

**Internal demo (Week 1):** the team ran `python -m state_grounded` and `pytest`. The scaffold runs end-to-end; the deterministic consistency case passes; the LLM-deferral path is wired.

**Observations / immediate improvements:**
- State engine is intentionally minimal — full VFS semantics (`rm -r`, `mv`, `cp`, file contents, permissions) are next (W2).
- Harness scoring + the Cowrie driver are stubs — needed before baseline numbers can be recorded (W1 second half).
- Cowrie fork not yet vendored — `cowrie/Dockerfile` currently uses the upstream image (W1).

**Next steps (entering Week 2):**
1. Vendor the Cowrie fork; run its LLM backend against local Ollama; pin the model (SGLH-1, SGLH-2).
2. Finish harness scoring + record the **baseline** "before" numbers (SGLH-6, SGLH-7).
3. Start the full virtual filesystem model + fast-path (SGLH-8…10).
