# State-Grounded LLM Honeypot — Cowrie image (placeholder for Week 1)
#
# In Week 1 we fork Cowrie into this directory. Until the fork is vendored,
# this Dockerfile pulls upstream Cowrie so `docker compose` is valid end-to-end.
# Once our fork lives here, switch the base to a local build:
#
#   FROM python:3.12-slim
#   COPY . /cowrie
#   RUN pip install --no-cache-dir -e /cowrie
#
# TODO(week1): replace the upstream image below with the local fork build.
FROM cowrie/cowrie:latest

# The state middleware is mounted/installed alongside Cowrie's LLM backend
# in Weeks 2-3 (deterministic fast-path) and Week 4 (prompt grounding).
