"""
Client for sending paper analysis requests to the Claude API.
"""

import json
import os
import re

import anthropic

from .prompt_builder import build_analysis_prompt


MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
EXPECTED_KEYS = {"difficulty_score", "difficulty_label", "difficulty_rationale", "prerequisites", "summary"}


def analyze_paper(paper: dict) -> dict:
    """
    Send a paper metadata dict to Claude for analysis.

    Builds a structured prompt, calls the Claude API, parses the JSON
    response, and validates that all expected fields are present.

    Returns a dict with keys: difficulty_score, difficulty_label,
    difficulty_rationale, prerequisites, summary.

    Raises RuntimeError if the response cannot be parsed or is missing fields.
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_analysis_prompt(paper)

    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text
    return _parse_and_validate(raw)


def _parse_and_validate(raw: str) -> dict:
    """Strip markdown fences, parse JSON, and validate expected keys."""
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Claude returned a response that could not be parsed as JSON.\n"
            f"Parse error: {exc}\n"
            f"Raw response:\n{raw}"
        ) from exc

    missing = EXPECTED_KEYS - result.keys()
    if missing:
        raise RuntimeError(
            f"Claude's response is missing expected fields: {sorted(missing)}\n"
            f"Received fields: {sorted(result.keys())}"
        )

    return result
