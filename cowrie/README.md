# Cowrie (fork)

This directory holds our **fork of [Cowrie](https://github.com/cowrie/cowrie)**,
the SSH/Telnet honeypot, including its experimental LLM backend. The
state-tracking middleware integrates directly into Cowrie's LLM command flow.

## Week 1 status

The fork is vendored here during Week 1. Until it is, `Dockerfile` pulls the
upstream `cowrie/cowrie` image so the Compose stack stays valid end-to-end.

## Setup (Week 1 task)

```bash
# from the repo root
git submodule add https://github.com/cowrie/cowrie cowrie   # or vendor a fork
# then point cowrie/Dockerfile at the local build (see TODO in that file)
```

## Where our contribution plugs in

- **Weeks 2-3:** the deterministic fast-path + state engine intercept commands
  before the LLM backend.
- **Week 4:** prompt grounding injects the state snapshot into the backend's
  LLM context before each generation.
- **Week 6:** the change is submitted upstream as a PR/issue.

License: Cowrie is BSD 3-Clause; the fork retains it.
