# DSA Solutions | Dikshant-Kulshrestha

This repository contains my solutions to coding interview problems, covering core Data Structures and Algorithms concepts commonly tested in software engineering interviews.

## Goal
My goal is to systematically work through the NeetCode roadmap and master the following topics:

- Arrays & Hashing
- Two Pointers
- Stack & Monotonic Stack
- Binary Search
- Sliding Window
- Linked Lists
- Trees
- Heap / Priority Queue
- Backtracking
- Graphs
- Dynamic Programming
- Greedy Algorithms

## Automated Notes Pipeline

Alongside solving problems, I built a small automation pipeline that turns each submission into a personalized study note, synced automatically to my notes page:

```
NeetCode submission → auto-commit → GitHub Actions → Claude API → Notion
```

On every push, a GitHub Actions workflow detects the newly solved problem, generates a note in my own writing style (matched to a style guide + real examples), classifies it by topic, and syncs it to my Notion page — including safeguards to never overwrite existing notes, flagging conflicts for manual review instead.

Built with: GitHub Actions, Python, Anthropic (Claude) API, Notion API.

Full technical writeup: [`NOTES-AGENT.md`](./NOTES-AGENT.md)

## About Me
MS Computer Science student at the University at Buffalo with prior Software Development experience. Interested in Software Engineering, Computer Systems, and Algorithm Design.

## Progress
Currently working through the roadmap one topic at a time and documenting accepted solutions in this repository.
