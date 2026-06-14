#!/usr/bin/env bash
# Pull the pinned LLM into the running Ollama container.
# Weights are never committed to git — this fetches them at setup time.
set -euo pipefail

MODEL="${OLLAMA_MODEL:-qwen2.5:3b}"
echo "Pulling pinned model: ${MODEL}"
docker compose exec ollama ollama pull "${MODEL}"
echo "Done. Available models:"
docker compose exec ollama ollama list
