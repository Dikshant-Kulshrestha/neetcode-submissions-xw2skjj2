# DSA Notes Agent

Automatically generates personalized study notes from NeetCode solution submissions and syncs them to a Notion page, matching the author's existing writing style.

## How It Works

```text
Solve on NeetCode
      ↓
NeetCode auto-commits the solution to this repo
(Data Structures & Algorithms/{problem}/submission-N.py)
      ↓
GitHub Actions triggers
(paths are filtered to the relevant folder)
      ↓
run_pipeline.py detects the changed problem folder
      ↓
generate_notes.py reads all submission files for the problem,
classifies the topic, and generates a note entry via the Claude API
using style_guide.md and example_notes.md
      ↓
notion_sync.py checks the Notion page:
   - New problem → inserted under the matching topic heading
   - Existing problem → added to "Pending Review"
   - Unclassified topic / missing heading → added to "Pending Review"
```

## Repository Structure

```text
style_guide.md
# Writing style rules provided to the LLM on every generation

example_notes.md
# Existing notes used as few-shot examples and style references

topics.json
# Closed list of valid topic headings for classification

scripts/
  generate_notes.py
  # Reads a problem folder, calls Claude, and outputs a JSON note

  notion_sync.py
  # Takes the generated JSON and writes the note to the Notion page

  run_pipeline.py
  # Orchestrates the pipeline by detecting changed problems
  # and running the generation and sync stages

.github/workflows/
  generate-notes.yml
  # GitHub Actions workflow definition

Data Structures & Algorithms/
# NeetCode's auto-committed solutions
# This directory remains untouched by the pipeline
```

## Pending Review

The pipeline never automatically overwrites existing notes.

Generated notes are placed under a **Pending Review** heading when:

* The problem already has an entry somewhere on the Notion page.
* The classified topic does not have a corresponding heading.
* The model returns `UNCLASSIFIED` because the problem does not clearly fit an existing topic.

Each pending entry includes a tag identifying the reason for review. The section is automatically created when the first pending entry is generated.

This provides a safeguard against accidental overwrites while allowing ambiguous or duplicate entries to be handled separately from the main notes.

## Multi-Approach Problems

When a problem folder contains multiple `submission-N.py` files, all submissions are analyzed together to distinguish between genuinely different algorithmic approaches and iterative bug-fix submissions.

* **Different approaches** → A single note entry containing numbered sub-methods, consistent with entries such as "Maximum Depth of Binary Tree" in `example_notes.md`.
* **Same approach, iterated** → A single standard note entry representing the final approach.

Numbered sub-methods currently render as plain text within a single Notion bullet rather than as true nested numbered blocks. This is a cosmetic limitation and does not affect note content or data integrity.

## Maintaining Note Quality

The quality and consistency of generated notes depend heavily on `example_notes.md`. As the personal writing style evolves, newer notes that accurately represent the preferred style can be incorporated into the file. Periodic testing against recently solved problems provides a way to verify that generated notes continue to reflect the intended level of detail, structure, and phrasing.
