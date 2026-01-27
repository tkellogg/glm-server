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
    match = _func_name_regex.search(text)
    if match is None:
        raise ValueError(
            f"Invalid tool call format: expected '<arg_key>' delimiter in text. "
            f"Got: {text[:200]}{'...' if len(text) > 200 else ''}"
        )
    func_name = match.group(1)
    # ... rest of function unchanged
```

This provides:
1. Null safety check before accessing `.group()`
2. Clear error message with partial input for debugging
3. `ValueError` instead of cryptic `AttributeError`

## Environment

- mlx-lm version: 0.30.5
- Model: GLM-4.7-Flash-4bit (mlx-community/GLM-4.7-Flash-4bit)
- Platform: macOS (Apple Silicon)
