#!/bin/bash
# GLM-4.7-Flash OpenAI-compatible server
# Requires: pip install mlx-openai-server

#MODEL_PATH="${GLM_MODEL:-mlx-community/GLM-4.7-Flash-4bit}"
MODEL_PATH=mlx-community/GLM-4.7-Flash-4bit
PORT="${GLM_PORT:-8000}"

echo "Starting GLM server on port $PORT"
echo "Model: $MODEL_PATH"

uv run mlx_lm.server --model $MODEL_PATH --port $PORT --max-tokens=15000
