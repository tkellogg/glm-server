#!/usr/bin/env python3
"""Test that the parser fix produces clear errors instead of AttributeError."""

import sys
sys.path.insert(0, '.')

# Test the fixed parser
from glm47_fixed import parse_tool_call

# Test case 1: Malformed tool call without <arg_key>
print("Test 1: Malformed tool call without delimiter")
try:
    result = parse_tool_call("just some random text without the delimiter")
    print(f"  FAIL: Expected ValueError, got result: {result}")
except ValueError as e:
    print(f"  PASS: Got ValueError: {e}")
except AttributeError as e:
    print(f"  FAIL: Got AttributeError (the bug we're fixing): {e}")
except Exception as e:
    print(f"  FAIL: Got unexpected {type(e).__name__}: {e}")

# Test case 2: Valid tool call
print("\nTest 2: Valid tool call")
try:
    valid_text = "get_weather<arg_key>location</arg_key><arg_value>Denver</arg_value>"
    result = parse_tool_call(valid_text)
    print(f"  PASS: Parsed successfully: {result}")
except Exception as e:
    print(f"  FAIL: Got {type(e).__name__}: {e}")

# Test case 3: Empty tool call
print("\nTest 3: Empty tool call")
try:
    result = parse_tool_call("")
    print(f"  FAIL: Expected ValueError, got result: {result}")
except ValueError as e:
    print(f"  PASS: Got ValueError: {e}")
except Exception as e:
    print(f"  FAIL: Got unexpected {type(e).__name__}: {e}")

# Test case 4: Partial/truncated tool call
print("\nTest 4: Partial/truncated tool call (model output cut off)")
try:
    result = parse_tool_call("get_weather<arg_key>loc")  # truncated
    print(f"  FAIL: Expected ValueError, got result: {result}")
except ValueError as e:
    print(f"  PASS: Got ValueError: {e}")
except Exception as e:
    print(f"  FAIL: Got unexpected {type(e).__name__}: {e}")

print("\n---")
print("The ValueError message includes the malformed text, which will")
print("bubble up through the HTTP API and be visible to Synth Wave.")
