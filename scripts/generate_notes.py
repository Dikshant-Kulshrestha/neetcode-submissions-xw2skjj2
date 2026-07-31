#!/usr/bin/env python3
"""
generate_notes.py

Reads all submission files for a single problem folder, classifies the topic,
and generates a styled note entry (matching the user's personal writing style)
via the Claude API.

Designed to be provider-agnostic: the actual API call is isolated in
`call_llm()` so swapping to Gemini/Groq later only requires editing that
one function.

USAGE (local testing, before wiring into GitHub Actions):
    export ANTHROPIC_API_KEY=sk-ant-...
    python generate_notes.py --problem-dir "Data Structures & Algorithms/car-fleet"

Outputs a JSON object to stdout:
    {
      "problem_name": "Car Fleet",
      "topic": "Stack & Monotonic Stack",
      "entry_markdown": "- **Car Fleet** - ..."
    }
"""

import argparse
import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Config / paths (adjust if repo layout changes)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
STYLE_GUIDE_PATH = REPO_ROOT / "style_guide.md"
EXAMPLE_NOTES_PATH = REPO_ROOT / "example_notes.md"
TOPICS_PATH = REPO_ROOT / "topics.json"

MODEL = "claude-sonnet-5"
MAX_TOKENS = 1000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slug_to_title(slug: str) -> str:
    """'car-fleet' -> 'Car Fleet'"""
    return " ".join(word.capitalize() for word in slug.replace("_", "-").split("-"))


def load_submission_files(problem_dir: Path) -> list[dict]:
    """Return [{filename, content}, ...] for every submission-N.py in the folder,
    sorted by submission number."""
    files = sorted(
        problem_dir.glob("submission-*.py"),
        key=lambda p: int("".join(filter(str.isdigit, p.stem)) or 0),
    )
    if not files:
        # fall back to any .py files if naming convention differs
        files = sorted(problem_dir.glob("*.py"))

    result = []
    for f in files:
        result.append({"filename": f.name, "content": f.read_text(encoding="utf-8")})
    return result


def build_prompt(problem_name: str, submissions: list[dict], style_guide: str,
                  example_notes: str, topics: list[str]) -> tuple[str, str]:
    """Returns (system_prompt, user_prompt)."""

    system_prompt = f"""You are generating personal DSA study notes for one specific person, \
matching their exact established writing style. You must follow the style guide and example \
notes below precisely -- do not default to generic AI-assistant phrasing.

STYLE GUIDE:
{style_guide}

REFERENCE EXAMPLE NOTES (verbatim excerpts of the person's real notes -- match this voice exactly):
{example_notes}

CLOSED TOPIC LIST -- you MUST classify this problem into exactly one of these topics, \
verbatim. Do not invent a new topic. If genuinely none fit, use the literal string \
"UNCLASSIFIED" instead:
{json.dumps(topics, indent=2)}

Respond with ONLY a raw JSON object (no markdown fences, no preamble), with exactly these keys:
{{
  "problem_name": "<human readable problem name>",
  "topic": "<one topic from the closed list, or UNCLASSIFIED>",
  "entry_markdown": "<the note entry itself, following the style guide's problem-level format>"
}}
"""

    submissions_block = "\n\n".join(
        f"--- {s['filename']} ---\n{s['content']}" for s in submissions
    )

    multi = len(submissions) > 1
    user_prompt = f"""Problem name (from folder): {problem_name}

Number of submission files: {len(submissions)}
{"NOTE: Multiple submission files exist. First determine whether they represent genuinely "
 "different algorithmic approaches (write ONE entry with numbered sub-methods, per the style "
 "guide) or just bugfix/retry iterations of the same approach (write ONE normal single entry)."
 if multi else ""}

SUBMISSION CODE:
{submissions_block}

Generate the note entry now, following the style guide and reference examples exactly."""

    return system_prompt, user_prompt


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Isolated API call -- swap this function to change providers."""
    try:
        import anthropic
    except ImportError:
        sys.exit("Missing dependency. Run: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def parse_llm_json(raw: str) -> dict:
    """Defensive parsing: strip markdown fences if the model adds them anyway."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        sys.exit(f"Failed to parse LLM output as JSON: {e}\n\nRaw output:\n{raw}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate a styled DSA note for one problem folder.")
    parser.add_argument("--problem-dir", required=True, help="Path to the problem's folder, e.g. "
                         "'Data Structures & Algorithms/car-fleet'")
    parser.add_argument("--out", help="Optional path to write the JSON result to a file.")
    args = parser.parse_args()

    problem_dir = Path(args.problem_dir)
    if not problem_dir.is_dir():
        sys.exit(f"Not a directory: {problem_dir}")

    if not STYLE_GUIDE_PATH.exists():
        sys.exit(f"style_guide.md not found at {STYLE_GUIDE_PATH}")
    if not EXAMPLE_NOTES_PATH.exists():
        sys.exit(f"example_notes.md not found at {EXAMPLE_NOTES_PATH}")
    if not TOPICS_PATH.exists():
        sys.exit(f"topics.json not found at {TOPICS_PATH}")

    style_guide = STYLE_GUIDE_PATH.read_text(encoding="utf-8")
    example_notes = EXAMPLE_NOTES_PATH.read_text(encoding="utf-8")
    topics = json.loads(TOPICS_PATH.read_text(encoding="utf-8"))["topics"]

    submissions = load_submission_files(problem_dir)
    if not submissions:
        sys.exit(f"No submission files found in {problem_dir}")

    problem_name = slug_to_title(problem_dir.name)

    system_prompt, user_prompt = build_prompt(
        problem_name, submissions, style_guide, example_notes, topics
    )

    raw_output = call_llm(system_prompt, user_prompt)
    result = parse_llm_json(raw_output)

    output_json = json.dumps(result, indent=2)
    print(output_json)

    if args.out:
        Path(args.out).write_text(output_json, encoding="utf-8")


if __name__ == "__main__":
    main()
