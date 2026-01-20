#!/usr/bin/env python3
"""Quick test to verify server is responding correctly."""

import sys
from openai import OpenAI

def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/v1"

    client = OpenAI(base_url=base_url, api_key="not-needed")

    # Test 1: Basic completion
    print("Testing basic completion...")
    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[{"role": "user", "content": "Say hello in one word."}],
        max_tokens=10
    )
    print(f"Response: {response.choices[0].message.content}")

    # Test 2: Tool calling
    print("\nTesting tool calling...")
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        }
    }]

    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
        tools=tools,
        tool_choice="auto"
    )

    if response.choices[0].message.tool_calls:
        print(f"Tool call: {response.choices[0].message.tool_calls[0].function}")
    else:
        print(f"No tool call, response: {response.choices[0].message.content}")

    print("\nServer is working!")

if __name__ == "__main__":
    main()
