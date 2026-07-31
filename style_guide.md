# Personal Notes Style Guide

This document defines the exact writing style the notes-generation agent must follow.
It is fed into every prompt alongside 2-3 real example entries as few-shot anchors.

## Voice & tone
- No first-person or second-person address. Never "I", "you", "we". Write in direct,
  impersonal technical explanation — as if documenting the mechanism itself, not narrating
  a personal experience of solving it.
- Dense and technical, but readable — every sentence should carry real information, no filler
  ("this is an interesting problem", "let's dive in", etc. are banned).
- Assume the reader already knows basic DS&A vocabulary (pointers, recursion, hash maps).
  Do not re-explain fundamentals.

## Structure

### Topic-level (only written once per topic section, not per problem)
- One short paragraph (1-2 sentences) summarizing the core technique/pattern behind the whole
  topic. Example: "Maintain range that moves step-by-step through the data and increment the
  results at each step. The idea is to use the results of the last window to obtain the current
  window's results."
- This is only generated/edited when a topic section is first created, not on every new problem.

### Problem-level entry (this is what gets generated per problem)
- **Problem name is ALWAYS bolded with `**double asterisks**` — this is non-negotiable
  formatting, never write it as plain text.**
- Format: `- **Problem Name** - explanation` as a single bullet, OR when there are multiple
  distinct approaches, a bullet with a numbered sub-list:
  ```
  - **Problem Name** - There are N methods to solve this question.
      1. Method label → explanation
      2. Method label → explanation
  ```
- Explanation is written as continuous prose within the bullet, not further sub-bulleted,
  UNLESS listing multiple distinct approaches (see above).
- Reference actual variable/function names from the code in backticks-free plain text
  (e.g., `prev`, `curr`, `l1`, `l2` — matching the example's convention of using the exact
  identifiers from the solution).
- Explain the *why*, not just the *what*. Don't just describe steps — explain why the
  technique works (e.g. Floyd's cycle detection example explains WHY fast/slow pointers
  must meet, not just that they do).
- State the key insight/observation that unlocks the problem before or while describing the
  mechanism (e.g. "Notice that the reordered list consists of two halves..." before
  describing the split-reverse-merge steps).
- Keep each entry roughly 2-5 sentences unless multiple methods are being documented, in
  which case each method gets 1-3 sentences.
- Occasionally use a bolded callout in the middle of an entry for a critical gotcha or
  precondition, formatted as `**NOTE -**` followed by the note, e.g. "**NOTE -** both of the
  questions below can be better solved by writing two different test cases..."
- If a video resource would help (as marked "VIDEO EXPLANATION" in existing notes), do NOT
  fabricate links — only note "VIDEO EXPLANATION" as a flag for the user to attach one later,
  or omit entirely rather than invent a URL.

## Multiple-approach problems (submission-0, 1, 2... in one folder)
When a problem folder contains multiple submission files representing genuinely different
approaches (not just retries/bugfixes of the same approach):
- Produce ONE entry for the problem, not multiple.
- Use the numbered sub-method format shown above.
- Order methods from simplest/most naive to most optimized, matching the existing example
  (Recursive DFS → Iterative BFS → Iterative DFS, ending with a bonus/related technique).
- Give each method a short descriptive label before the arrow/explanation (e.g.
  "Recursive DFS →", "Iterative BFS →").
- If the submissions are actually just bugfix iterations of the SAME approach (not different
  algorithms), treat it as a single normal entry, not a multi-method one — only split into
  numbered methods when the underlying algorithmic approach genuinely differs.

## What to never include
- No time/space complexity notation unless it appears in the existing notes' style for that
  kind of problem (the example notes don't consistently state Big-O, so don't force it in
  every entry — only include if genuinely clarifying, phrased in plain text e.g. "O(n) time").
- No motivational or evaluative commentary ("great problem", "tricky one", "classic pattern").
- No emoji, no exclamation marks.
- No restating the problem statement itself — jump straight into the technique.

## Reference examples (few-shot anchors — see companion file for full text)
See `example_notes.md` for the verbatim reference entries this style is derived from,
covering: Binary Search, Sliding Window, Linked List, Binary Tree topics.