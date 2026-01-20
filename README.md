# GLM Server

OpenAI-compatible HTTP server for GLM-4.7-Flash on Apple Silicon.

Uses [mlx-openai-server](https://github.com/cubist38/mlx-openai-server) which has built-in GLM-4 MoE support.

## Requirements

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.11+
- ~20GB RAM for 4-bit, ~35GB for 8-bit

## Quick Start

```bash
# Install
pip install mlx-openai-server

# Download model (first run only, ~18GB for 4-bit)
python -c "from mlx_lm import load; load('mlx-community/GLM-4.7-Flash-4bit')"

# Launch server
./run.sh
```

## Configuration

Edit `run.sh` to adjust:
- `--port` (default: 8000)
- Model path (default: mlx-community/GLM-4.7-Flash-4bit)
- `--max-concurrency` for parallel requests

## API Usage

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4.7-flash",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

Or with OpenAI SDK:
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
response = client.chat.completions.create(
    model="glm-4.7-flash",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Model Options

| Model | Size | RAM | Notes |
|-------|------|-----|-------|
| `mlx-community/GLM-4.7-Flash-4bit` | ~18GB | 24GB+ | Default, good balance |
| `mlx-community/GLM-4.7-Flash-8bit` | ~32GB | 40GB+ | Better quality if RAM allows |

## Tool Calling

GLM-4.7-Flash has native tool calling. The server includes `--tool-call-parser glm4_moe` for proper function call handling.

## For Introspection-by-Proxy

This server is designed for the [introspection-by-proxy](https://github.com/tkellogg/discord-letta-bot/blob/main/state/research/introspection-by-proxy.md) project — providing a weights-accessible model that Strix can probe.

### Tunnel Setup

For remote access, use Cloudflare Tunnel:
```bash
cloudflared tunnel --url http://localhost:8000
```

Or expose via Tailscale for private access.
