#!/usr/bin/env python3
"""
This file takes the JSON output of generate_notes.py and syncs it to the Notion page:
- If the problem is new (no existing entry found under any heading), appends
  the entry as a bullet under the matching topic heading.
- If the problem already has an entry anywhere on the page, it is NEVER
  overwritten or merged automatically, it's appended instead to a
  dedicated "Pending Review" section at the top of the page, with a note
  pointing back to the existing entry, for manual consideration.


note.json is the output of generate_notes.py
"""

import argparse
import json
import os
import sys
import re
from pathlib import Path

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
PENDING_REVIEW_HEADING = "Pending Review"


def get_headers():
    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        sys.exit("NOTION_API_KEY environment variable not set.")
    return {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def get_page_id():
    page_id = os.environ.get("NOTION_PAGE_ID")
    if not page_id:
        sys.exit("NOTION_PAGE_ID environment variable not set.")
    return page_id


def fetch_all_blocks(page_id: str, headers: dict) -> list[dict]:
    """Fetch all top-level blocks of the page (paginated)."""
    import requests

    blocks = []
    cursor = None
    while True:
        url = f"{NOTION_API_BASE}/blocks/{page_id}/children?page_size=100"
        if cursor:
            url += f"&start_cursor={cursor}"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        blocks.extend(data["results"])
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]
    return blocks


def block_plain_text(block: dict) -> str:
    """Extract plain text from a block's rich_text, regardless of block type."""
    block_type = block.get("type")
    rich_text = block.get(block_type, {}).get("rich_text", [])
    return "".join(rt.get("plain_text", "") for rt in rich_text)


def is_heading(block: dict) -> bool:
    return block.get("type") in ("heading_1", "heading_2", "heading_3")


def find_heading_block_id(blocks: list[dict], topic: str) -> str | None:
    """Find the block ID of the heading matching the given topic (fuzzy match
    on core text, since your headings are numbered e.g. '4. Binary Search')."""
    topic_lower = topic.lower().strip()
    for block in blocks:
        if is_heading(block):
            text = block_plain_text(block).lower()
            # strip leading numbering like "4. " before comparing
            text_stripped = re.sub(r"^\d+[\.\)]\s*", "", text).strip()
            if topic_lower in text_stripped or text_stripped in topic_lower:
                return block["id"]
    return None


def find_existing_entry(blocks: list[dict], problem_name: str) -> dict | None:
    """Search ALL bulleted-list blocks on the page for one whose bolded
    problem name matches. Returns the block if found, else None."""
    problem_lower = problem_name.lower().strip()
    for block in blocks:
        if block.get("type") == "bulleted_list_item":
            text = block_plain_text(block).lower()
          
            if text.startswith(problem_lower):
                return block
    return None


def markdown_bullet_to_notion_block(entry_markdown: str) -> dict:
    #Convert a single-level markdown bullet into a Notion bulleted_list_item block.
    text = entry_markdown.lstrip("- ").strip()

    # Split on the bold problem name to build rich_text with bold formatting
    match = re.match(r"\*\*(.+?)\*\*\s*-\s*(.*)", text, re.DOTALL)
    if match:
        bold_part, rest = match.groups()
        rich_text = [
            {"type": "text", "text": {"content": bold_part}, "annotations": {"bold": True}},
            {"type": "text", "text": {"content": f" - {rest}"}},
        ]
    else:
        rich_text = [{"type": "text", "text": {"content": text}}]

    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text},
    }
    # TODO (polish): entries with numbered sub-methods (multi-approach
    # problems) contain literal "\n    1. ..." in entry_markdown -- these
    # currently get flattened into one bullet's text rather than true nested
    # numbered_list_item child blocks. Revisit once basic sync is
    # working, since Notion's nested block API needs a second append call
    # with the parent bullet's ID as target.         


def find_section_end_block_id(blocks: list[dict], heading_id: str) -> str:
    """Given a heading block's ID, find the ID of the LAST block belonging to
    that section (i.e. the block immediately before the next heading, or the
    last block on the page if this is the final section). Returns a block ID
    to use as the `after` anchor for insertion, so new entries land at the
    end of the correct topic section rather than the bottom of the page."""
    found_heading = False
    last_id_in_section = heading_id
    for block in blocks:
        if block["id"] == heading_id:
            found_heading = True
            continue
        if found_heading:
            if is_heading(block):
                break  # reached the next section
            last_id_in_section = block["id"]
    return last_id_in_section


def append_block_after(page_id: str, anchor_block_id: str, block: dict, headers: dict):
    """Insert a block immediately after a specific existing block, using
    Notion's `after` parameter -- this is what makes correct mid-page
    placement possible, instead of always appending to the page's end."""
    import requests

    url = f"{NOTION_API_BASE}/blocks/{page_id}/children"
    resp = requests.patch(
        url, headers=headers, json={"children": [block], "after": anchor_block_id}
    )
    resp.raise_for_status()
    return resp.json()


def append_block(page_id_or_block_id: str, block: dict, headers: dict):
    import requests

    url = f"{NOTION_API_BASE}/blocks/{page_id_or_block_id}/children"
    resp = requests.patch(url, headers=headers, json={"children": [block]})
    resp.raise_for_status()
    return resp.json()


def ensure_pending_review_section(page_id: str, blocks: list[dict], headers: dict) -> str:
    """Find or create the 'Pending Review' heading at the TOP of the page.
    Returns its block ID."""
    for block in blocks:
        if is_heading(block) and block_plain_text(block).strip().lower() == PENDING_REVIEW_HEADING.lower():
            return block["id"]

    # Not found -- create it. NOTE: Notion API appends to the END of children,
    # not the top. For a true "top of page" placement, this block should be
    # manually moved once, or the page pre-seeded with this heading ahead of
    # time.
    heading_block = {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": PENDING_REVIEW_HEADING}}]},
    }
    result = append_block(page_id, heading_block, headers)
    return result["results"][0]["id"]


def main():
    parser = argparse.ArgumentParser(description="Sync a generated note entry to Notion.")
    parser.add_argument("--input", required=True, help="Path to JSON file from generate_notes.py")
    args = parser.parse_args()

    note = json.loads(Path(args.input).read_text(encoding="utf-8"))
    problem_name = note["problem_name"]
    topic = note["topic"]
    entry_markdown = note["entry_markdown"]

    headers = get_headers()
    page_id = get_page_id()

    print(f"Fetching current page blocks...")
    blocks = fetch_all_blocks(page_id, headers)

    if topic == "UNCLASSIFIED":
        print(f"Topic UNCLASSIFIED for '{problem_name}' -> routing to Pending Review.")
        review_heading_id = ensure_pending_review_section(page_id, blocks, headers)
        anchor_id = find_section_end_block_id(blocks, review_heading_id)
        note_block = markdown_bullet_to_notion_block(
            f"**{problem_name}** - [UNCLASSIFIED TOPIC] {entry_markdown.split(' - ', 1)[-1]}"
        )
        append_block_after(page_id, anchor_id, note_block, headers)
        print("Flagged for review (unclassified topic).")
        return

    existing = find_existing_entry(blocks, problem_name)
    if existing:
        print(f"'{problem_name}' already has an entry on the page -> routing to Pending Review "
              f"(NOT overwriting).")
        review_heading_id = ensure_pending_review_section(page_id, blocks, headers)
        anchor_id = find_section_end_block_id(blocks, review_heading_id)
        note_block = markdown_bullet_to_notion_block(
            f"**{problem_name}** - [POSSIBLE DUPLICATE, existing entry found under a topic "
            f"section -- compare manually] {entry_markdown.split(' - ', 1)[-1]}"
        )
        append_block_after(page_id, anchor_id, note_block, headers)
        print("Flagged for review (duplicate).")
        return

    heading_id = find_heading_block_id(blocks, topic)
    if not heading_id:
        print(f"No heading found matching topic '{topic}' -> routing to Pending Review.")
        review_heading_id = ensure_pending_review_section(page_id, blocks, headers)
        anchor_id = find_section_end_block_id(blocks, review_heading_id)
        note_block = markdown_bullet_to_notion_block(
            f"**{problem_name}** - [NO MATCHING HEADING FOUND for topic '{topic}'] "
            f"{entry_markdown.split(' - ', 1)[-1]}"
        )
        append_block_after(page_id, anchor_id, note_block, headers)
        print("Flagged for review (missing heading).")
        return

    note_block = markdown_bullet_to_notion_block(entry_markdown)
    anchor_id = find_section_end_block_id(blocks, heading_id)
    append_block_after(page_id, anchor_id, note_block, headers)
    print(f"Added new entry for '{problem_name}' under topic '{topic}'.")


if __name__ == "__main__":
    main()
