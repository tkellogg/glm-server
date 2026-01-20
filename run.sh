#!/bin/bash
# GLM-4.7-Flash OpenAI-compatible server
# Requires: pip install mlx-openai-server

MODEL_PATH="${GLM_MODEL:-mlx-community/GLM-4.7-Flash-4bit}"
PORT="${GLM_PORT:-8000}"

echo "Starting GLM server on port $PORT"
echo "Model: $MODEL_PATH"

python -m app.main \
    --model-path "$MODEL_PATH" \
    --model-type lm \
    --tool-call-parser glm4_moe \
    --reasoning-parser glm4_moe \
    --message-converter glm4_moe \
    --port "$PORT" \
    --max-concurrency 1 \
    --trust-remote-code
