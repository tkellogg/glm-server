# Copyright © 2025 Apple Inc.
# Modified to fix AttributeError when regex doesn't match

"""
Modified from:
https://github.com/vllm-project/vllm/blob/main/vllm/tool_parsers/glm4_moe_tool_parser.py

Fix: Added null safety check for regex match before calling .group()
See: https://github.com/ml-explore/mlx-lm/issues/XXX

Install on Lumen:
  cp glm47_fixed.py $(python -c "import mlx_lm; print(mlx_lm.__path__[0])")/tool_parsers/glm47.py
  # Then restart mlx-lm.server
"""

import ast
import json
from typing import Any

import regex as re

_func_name_regex = re.compile(r"^(.*?)<arg_key>", re.DOTALL)
_func_arg_regex = re.compile(
    r"<arg_key>(.*?)</arg_key>(?:\\n|\s)*<arg_value>(.*?)</arg_value>",
    re.DOTALL,
)

tool_call_start = "<tool_call>"
tool_call_end = "</tool_call>"


def _is_string_type(
    tool_name: str,
    arg_name: str,
    tools: list[Any] | None,
) -> bool:
    if tools is None:
        return False
    for tool in tools:
        func = tool["function"]
        if func["name"] == tool_name:
            params = func["parameters"]
            if params is None:
                return False
            arg_type = params.get("properties", {}).get(arg_name, {}).get("type", None)
            return arg_type == "string"
    return False


def _deserialize(value: str) -> Any:
    try:
        return json.loads(value)
    except Exception:
        pass

    try:
        return ast.literal_eval(value)
    except Exception:
        pass
    return value


def parse_tool_call(text: str, tools: list[Any] | None = None):
    # FIX: Add null safety check for regex match
    func_name_match = _func_name_regex.search(text)
    if func_name_match is None:
        raise ValueError(
            f"Invalid tool call format: expected '<arg_key>' delimiter in text. "
            f"Got: {text[:200]}{'...' if len(text) > 200 else ''}"
        )
    func_name = func_name_match.group(1)

    pairs = _func_arg_regex.findall(text)
    arg_dct = {}
    for key, value in pairs:
        arg_key = key.strip()
        arg_val = value.strip()
        if not _is_string_type(func_name, arg_key, tools):
            arg_val = _deserialize(arg_val)
        arg_dct[arg_key] = arg_val
    return dict(name=func_name, arguments=arg_dct)
