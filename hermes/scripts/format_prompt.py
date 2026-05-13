#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Format a conversation into Hermes ChatML format.

Reads a JSON messages array (OpenAI format) and outputs the raw ChatML string
ready to send to a Hermes model's /completions endpoint or tokenizer.

Usage:
    # From JSON string
    uv run scripts/format_prompt.py --messages '[{"role":"user","content":"Hello"}]'

    # From file
    uv run scripts/format_prompt.py --file conversation.json

    # With system prompt override
    uv run scripts/format_prompt.py --system "You are Hermes." --messages '[{"role":"user","content":"Hi"}]'

    # Add generation prompt (open assistant tag — default: true)
    uv run scripts/format_prompt.py --no-generation-prompt --messages '[...]'

    # Count tokens (approximate, character-based)
    uv run scripts/format_prompt.py --count-tokens --messages '[...]'

Exit codes:
    0  Success
    1  Invalid input (bad JSON, empty messages, unknown role)
"""

import argparse
import json
import sys

VALID_ROLES = {"system", "user", "assistant", "tool"}


def format_chatml(messages: list[dict], add_generation_prompt: bool = True) -> str:
    """Convert an OpenAI-style messages list to Hermes ChatML format."""
    if not messages:
        raise ValueError("messages list is empty")

    parts = []
    for i, msg in enumerate(messages):
        role = msg.get("role")
        content = msg.get("content", "")

        if role not in VALID_ROLES:
            raise ValueError(f"Unknown role '{role}' at index {i}. Valid roles: {sorted(VALID_ROLES)}")

        if content is None:
            content = ""

        parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")

    prompt = "\n".join(parts)

    if add_generation_prompt:
        prompt += "\n<|im_start|>assistant\n"

    return prompt


def approximate_token_count(text: str) -> int:
    # Rough heuristic: ~4 characters per token for English text.
    # Special tokens each count as 1 token.
    special_tokens = text.count("<|im_start|>") + text.count("<|im_end|>")
    plain_chars = len(text) - special_tokens * len("<|im_start|>")
    return special_tokens + max(1, plain_chars // 4)


def main():
    parser = argparse.ArgumentParser(
        description="Format a conversation into Hermes ChatML format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--messages", "-m", help="JSON array of message objects")
    input_group.add_argument("--file", "-f", help="Path to JSON file containing messages array")
    parser.add_argument("--system", "-s", help="Prepend a system message with this content")
    parser.add_argument(
        "--no-generation-prompt",
        action="store_true",
        help="Do not append the open <|im_start|>assistant tag",
    )
    parser.add_argument("--count-tokens", action="store_true", help="Print approximate token count to stderr")
    parser.add_argument("--json", action="store_true", help="Output as JSON with metadata")
    args = parser.parse_args()

    # Read messages
    if args.file:
        try:
            with open(args.file) as f:
                raw = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    elif args.messages:
        raw = args.messages
    else:
        # Try reading from stdin
        if sys.stdin.isatty():
            print("Error: Provide --messages, --file, or pipe JSON via stdin.", file=sys.stderr)
            parser.print_help(sys.stderr)
            sys.exit(1)
        raw = sys.stdin.read()

    try:
        messages = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(messages, list):
        print("Error: Expected a JSON array of message objects.", file=sys.stderr)
        sys.exit(1)

    # Optionally prepend system message
    if args.system:
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = args.system
        else:
            messages = [{"role": "system", "content": args.system}] + messages

    add_gen_prompt = not args.no_generation_prompt

    try:
        result = format_chatml(messages, add_generation_prompt=add_gen_prompt)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.count_tokens:
        count = approximate_token_count(result)
        print(f"Approximate tokens: {count}", file=sys.stderr)

    if args.json:
        output = {
            "prompt": result,
            "message_count": len(messages),
            "roles": [m["role"] for m in messages],
            "has_generation_prompt": add_gen_prompt,
        }
        if args.count_tokens:
            output["approximate_tokens"] = approximate_token_count(result)
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
