#!/bin/bash
# GLM-4.7-Flash OpenAI-compatible server
# Requires: pip install mlx-openai-server

MODEL_PATH="${GLM_MODEL:-mlx-community/GLM-4.7-Flash-4bit}"
PORT="${GLM_PORT:-8000}"

echo "Starting GLM server on port $PORT"
echo "Model: $MODEL_PATH"

uv run -m app.main \
    --model-path "$MODEL_PATH" \
    --model-type lm \
    --port "$PORT" \
    --max-concurrency 1
