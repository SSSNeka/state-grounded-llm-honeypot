# Initial API / Integration Contract (MVP)

This project has no public web API; its "API" is the **integration seam** with
Cowrie's LLM backend plus the **local Ollama HTTP API**. Defining it now (Week 1)
lets the state-engine, integration, and grounding work proceed in parallel.

## 1. Middleware ⇄ Cowrie LLM backend (internal Python contract)

The middleware intercepts each command in Cowrie's LLM command flow:

```
handle_command(command: str, session: SessionCtx) -> str
    snapshot = engine.snapshot()
    fast = engine.try_fast_path(command)        # deterministic? answer directly
    if fast is not None:
        return fast                              # no LLM call
    prompt = build_grounded_prompt(snapshot, config)
    return llm.generate(prompt, command)         # grounded LLM call (Week 4)
```

| Function | Input | Output | Notes |
|---|---|---|---|
| `try_fast_path(command)` | shell command | `str` output, or `None` | `None` ⇒ defer to LLM |
| `snapshot()` | — | `StateSnapshot` | cwd, files, env, `$?` |
| `build_grounded_prompt(snapshot, config)` | snapshot, config | system prompt `str` | grounding can be toggled |

## 2. Middleware ⇄ Ollama (local HTTP, Week 4)

```
POST {OLLAMA_HOST}/api/generate
{
  "model":  "<pinned model, e.g. qwen2.5:3b>",
  "system": "<grounded system prompt incl. state snapshot>",
  "prompt": "<attacker command>",
  "stream": false
}
→ 200 { "response": "<terminal output>", "done": true, ... }
```

Errors: on Ollama timeout/5xx the middleware returns a safe in-character
fallback and logs the event (no stack traces leak to the attacker).

## 3. Harness ⇄ backends

`run_baseline.py --backend {vanilla|grounded}` replays scripted sessions and
emits `results/{before,after}.json` with the four metrics (see `harness/README.md`).

> A formal OpenAPI spec will be added **only if** a control/health HTTP endpoint
> is introduced for the middleware service; the MVP integration is in-process.
