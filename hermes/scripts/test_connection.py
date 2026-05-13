#!/usr/bin/env python3
# /// script
# dependencies = ["openai>=1.0", "httpx>=0.25"]
# ///
"""
Smoke-test a Hermes endpoint (Ollama or vLLM) to confirm the model is running
and producing valid ChatML-formatted responses.

Usage:
    uv run scripts/test_connection.py
    uv run scripts/test_connection.py --base-url http://localhost:11434/v1 --model hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF
    uv run scripts/test_connection.py --base-url http://localhost:8000/v1 --model NousResearch/Hermes-3-Llama-3.1-8B

Exit codes:
    0  All tests passed
    1  One or more tests failed
    2  Could not connect to endpoint
"""

import argparse
import json
import sys
import time

import httpx
from openai import OpenAI, APIConnectionError, APITimeoutError

DEFAULT_OLLAMA_URL = "http://localhost:11434/v1"
DEFAULT_VLLM_URL = "http://localhost:8000/v1"
DEFAULT_OLLAMA_MODEL = "hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF"
DEFAULT_VLLM_MODEL = "NousResearch/Hermes-3-Llama-3.1-8B"


def check_connection(base_url: str) -> bool:
    try:
        r = httpx.get(f"{base_url}/models", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def run_test(client: OpenAI, model: str, test_name: str, messages: list, expected_contains: str | None = None) -> dict:
    start = time.time()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0,
            max_tokens=256,
            stop=["<|im_end|>"],
        )
        elapsed = time.time() - start
        content = response.choices[0].message.content or ""

        passed = True
        failure_reason = None

        if not content.strip():
            passed = False
            failure_reason = "Empty response"
        elif expected_contains and expected_contains.lower() not in content.lower():
            passed = False
            failure_reason = f"Expected '{expected_contains}' in response, got: {content[:100]!r}"

        return {
            "test": test_name,
            "passed": passed,
            "elapsed_s": round(elapsed, 2),
            "tokens": response.usage.total_tokens if response.usage else None,
            "response_preview": content[:200],
            "failure_reason": failure_reason,
        }
    except APIConnectionError as e:
        return {"test": test_name, "passed": False, "elapsed_s": None, "failure_reason": f"Connection error: {e}"}
    except APITimeoutError:
        return {"test": test_name, "passed": False, "elapsed_s": None, "failure_reason": "Timeout after 60s"}
    except Exception as e:
        return {"test": test_name, "passed": False, "elapsed_s": None, "failure_reason": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Smoke-test a Hermes endpoint")
    parser.add_argument("--base-url", default=None, help="API base URL (default: auto-detect Ollama then vLLM)")
    parser.add_argument("--model", default=None, help="Model ID to test")
    parser.add_argument("--api-key", default="EMPTY", help="API key (default: EMPTY)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    # Auto-detect endpoint
    if args.base_url is None:
        if check_connection(DEFAULT_OLLAMA_URL):
            base_url = DEFAULT_OLLAMA_URL
            model = args.model or DEFAULT_OLLAMA_MODEL
            print(f"[auto] Detected Ollama at {base_url}", file=sys.stderr)
        elif check_connection(DEFAULT_VLLM_URL):
            base_url = DEFAULT_VLLM_URL
            model = args.model or DEFAULT_VLLM_MODEL
            print(f"[auto] Detected vLLM at {base_url}", file=sys.stderr)
        else:
            print("Error: Could not connect to Ollama (port 11434) or vLLM (port 8000).", file=sys.stderr)
            print("Start your Hermes server first, or pass --base-url explicitly.", file=sys.stderr)
            sys.exit(2)
    else:
        base_url = args.base_url
        model = args.model or DEFAULT_VLLM_MODEL

    client = OpenAI(base_url=base_url, api_key=args.api_key)

    tests = [
        {
            "name": "basic_response",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Reply with exactly: 'Hermes is ready.'"},
            ],
            "expected_contains": "Hermes is ready",
        },
        {
            "name": "json_output",
            "messages": [
                {"role": "system", "content": "You output only valid JSON. No explanation."},
                {"role": "user", "content": 'Return {"status": "ok", "model": "hermes"}'},
            ],
            "expected_contains": "status",
        },
        {
            "name": "tool_call_format",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You have access to tools.\n\n<tools>\n"
                        '[{"type":"function","function":{"name":"get_time","description":"Get current time","parameters":{"type":"object","properties":{},"required":[]}}}]\n'
                        "</tools>"
                    ),
                },
                {"role": "user", "content": "What time is it? Use the get_time tool."},
            ],
            "expected_contains": "get_time",
        },
        {
            "name": "multi_turn",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "My favorite color is blue."},
                {"role": "assistant", "content": "That's great! Blue is a calming color."},
                {"role": "user", "content": "What is my favorite color?"},
            ],
            "expected_contains": "blue",
        },
    ]

    results = []
    print(f"\nTesting Hermes endpoint: {base_url}")
    print(f"Model: {model}\n")

    for test in tests:
        print(f"  [{test['name']}] ", end="", flush=True)
        result = run_test(client, model, test["name"], test["messages"], test.get("expected_contains"))
        results.append(result)
        status = "PASS" if result["passed"] else "FAIL"
        elapsed = f"{result['elapsed_s']}s" if result["elapsed_s"] else "N/A"
        print(f"{status} ({elapsed})")
        if not result["passed"]:
            print(f"    Reason: {result['failure_reason']}")

    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    print(f"\nResults: {passed}/{total} passed")

    if args.json:
        print(json.dumps({"endpoint": base_url, "model": model, "results": results}, indent=2))

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
