# Bug Report: AttributeError in glm47.py tool parser when regex doesn't match

## Description

The `parse_tool_call` function in `mlx_lm/tool_parsers/glm47.py` crashes with `AttributeError: 'NoneType' object has no attribute 'group'` when the model emits tool call text that doesn't contain the expected `<arg_key>` delimiter.

## Root Cause

Line 56 calls `.group(1)` directly on the regex match result without checking if the match is `None`:

```python
func_name = _func_name_regex.search(text).group(1)
```

If the input `text` doesn't contain `<arg_key>`, the regex returns `None`, and `.group(1)` raises `AttributeError`.

## Reproduction

This occurs when GLM-4.7-Flash (or similar models) emits malformed tool call text, which can happen due to:
- Context pressure causing truncated outputs
- Model generating text that looks like a tool call but isn't properly formatted
- Partial tool call starts that get cut off

## Proposed Fix

```python
def parse_tool_call(text: str, tools: list[Any] | None = None):
    func_name_match = _func_name_regex.search(text)
    if func_name_match is None:
        raise ValueError(
            f"Invalid tool call format: expected '<arg_key>' delimiter in text. "
            f"Got: {text[:200]}{'...' if len(text) > 200 else ''}"
        )
    func_name = func_name_match.group(1)
    # ... rest of function unchanged
```

This provides:
1. Null safety check before accessing `.group()`
2. Clear error message with partial input for debugging
3. `ValueError` instead of cryptic `AttributeError`

## Error Bubbling

When this `ValueError` is raised, it propagates up through the mlx-lm server and results in an HTTP 500 error. The error message appears in the server logs. Clients (like Synth Wave) will see the 500 status and can check server logs for the detailed error.

To fully expose the error in the HTTP response body, the server would need try/catch around `parse_tools()` calls in `server.py` lines 1326, 1342, 1363. This is a separate enhancement.

## Testing

Run `python test_error_bubbling.py` in this directory to verify the fix:
- Malformed text without delimiter → ValueError with clear message
- Valid tool calls → Parse successfully
- Empty text → ValueError

## Installation (Local Testing)

```bash
# Find your mlx-lm install location
MLX_PATH=$(python -c "import mlx_lm; print(mlx_lm.__path__[0])")

# Backup original
cp "$MLX_PATH/tool_parsers/glm47.py" "$MLX_PATH/tool_parsers/glm47.py.bak"

# Install fix
cp glm47_fixed.py "$MLX_PATH/tool_parsers/glm47.py"

# Restart mlx-lm.server
```

## Environment

- mlx-lm version: 0.30.5
- Model: GLM-4.7-Flash-4bit (mlx-community/GLM-4.7-Flash-4bit)
- Platform: macOS (Apple Silicon)
