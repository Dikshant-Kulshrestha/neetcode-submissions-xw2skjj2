# DSA Notes Agent

Automatically generates personalized study notes from NeetCode solution submissions
and syncs them to a Notion page, matching your own writing style.

## How it works

```
Solve on NeetCode
      ↓
NeetCode auto-commits solution to this repo (Data Structures & Algorithms/{problem}/submission-N.py)
      ↓
GitHub Actions triggers (paths filtered to that folder only)
      ↓
run_pipeline.py detects which problem folder(s) changed
      ↓
generate_notes.py reads all submission files for that problem,
   classifies the topic, and generates a note entry via Claude API
   (matching style_guide.md + example_notes.md)
      ↓
notion_sync.py checks the Notion page:
   - New problem → inserted under the matching topic heading
   - Already exists → flagged under "Pending Review" (never auto-overwritten)
   - Unclassified topic / no matching heading → also flagged under "Pending Review"
```

## Repo structure

```
style_guide.md          # writing style rules fed to the LLM every call
example_notes.md         # real example notes used as few-shot anchors
topics.json               # closed list of valid topic headings for classification
scripts/
  generate_notes.py       # reads a problem folder, calls Claude, outputs JSON note
  notion_sync.py           # takes that JSON, writes it to the Notion page
  run_pipeline.py           # orchestrator: diffs the push, loops the two scripts above
.github/workflows/
  generate-notes.yml        # the GitHub Actions workflow definition
Data Structures & Algorithms/   # NeetCode's auto-committed solutions (untouched by this pipeline)
```


## How "Pending Review" works

Nothing is ever auto-overwritten. If the agent generates a note for a problem that:
- already has an entry somewhere on the page, or
- classifies into a topic with no matching heading yet, or
- the model returns `UNCLASSIFIED` (genuinely doesn't fit any topic)

...it gets appended under a **"Pending Review"** heading (auto-created on first use) with a
tag explaining why, instead of touching existing content. Check this section periodically and
manually merge/move entries into the right place.

## Multi-approach problems

If a problem folder contains multiple `submission-N.py` files, the agent reads all of them
together and decides whether they represent genuinely different algorithmic approaches or
just bugfix iterations of the same one:
- **Different approaches** → one entry with numbered sub-methods (matching the style of
  entries like "Maximum Depth of Binary Tree" in the example notes)
- **Same approach, iterated** → one normal single entry

**Known limitation:** numbered sub-methods currently render as plain text within a single
Notion bullet, not as true nested numbered blocks. Cosmetic issue, not a data-loss issue —
revisit if it bothers you enough to fix the Notion block nesting logic.

## Maintaining note quality over time

The model's output is only as good as `example_notes.md`. If you notice generated notes
drifting toward generic phrasing over time, refresh that file with newer real notes you've
personally written or approved, and re-test against a couple of problems to confirm quality
is back on track.

