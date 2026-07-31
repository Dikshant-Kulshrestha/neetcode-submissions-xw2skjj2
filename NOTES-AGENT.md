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

## One-time setup (for a fresh clone / new machine)

### 1. Anthropic API key
- Sign up at console.anthropic.com (separate from claude.ai)
- Add billing, load a small amount of prepaid credit (e.g. $5-10), leave auto-reload OFF
- Settings → API Keys → Create Key, copy it immediately (shown only once)

### 2. Notion integration
- In Notion: Settings → Integrations → New internal integration → copy its secret key
- Open your notes page → `•••` menu → Connections → add the integration by name
- Get the page ID from the page URL (32-char string, format with dashes:
  `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### 3. GitHub repo secrets
Repo → Settings → Secrets and variables → Actions → New repository secret:
| Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | your `sk-ant-...` key |
| `NOTION_API_KEY` | your Notion integration secret |
| `NOTION_PAGE_ID` | your page's dashed UUID |

### 4. Notion page structure requirement
The page must already have headings (heading_1/2/3 blocks) whose text matches (or closely
matches) the entries in `topics.json`. The pipeline does NOT auto-create topic headings —
if a topic's heading doesn't exist yet, that problem gets flagged in Pending Review instead
of guessing where it belongs. Create the heading yourself first, then push again (or manually
move the flagged entry).

## Local testing (without waiting for a real NeetCode push)

```bash
pip install anthropic requests
export ANTHROPIC_API_KEY=sk-ant-...
export NOTION_API_KEY=secret_...
export NOTION_PAGE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Generate a note for one problem without publishing it
python scripts/generate_notes.py --problem-dir "Data Structures & Algorithms/car-fleet" --out note.json

# Publish that note to Notion
python scripts/notion_sync.py --input note.json

# Or run the full orchestrator against your last commit
python scripts/run_pipeline.py --before HEAD^ --after HEAD
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

## Cost

Pay-as-you-go via Anthropic API, no subscription. At roughly 1-2 submissions/day, expect
well under $1/month. Prepaid credits, auto-reload left off, so spend is hard-capped at
whatever you've loaded — nothing to "cancel."

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Workflow doesn't appear in Actions tab at all | `.github/workflows/generate-notes.yml` wasn't actually pushed, or repo's default branch isn't `main` |
| `No such file or directory` for a script | That script wasn't committed/pushed — check `git status` for untracked files |
| Notion API 404 | Page not shared with the integration, or page ID missing dashes |
| Notion API 400 on block append | Usually a parent-block-type issue (e.g. trying to nest under a non-toggleable heading) |
| Entry lands in Pending Review unexpectedly | Check whether the problem already has an entry elsewhere on the page, or whether the matching topic heading actually exists with matching text |
| Workflow doesn't trigger on a push | Check the push actually touched a file under `Data Structures & Algorithms/` — the `paths:` filter ignores everything else on purpose |
