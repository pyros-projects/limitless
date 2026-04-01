# Fascination Reading Guide

How `/spark` reads and uses `~/.pyro/fascination-index.md`.

## What the Fascination Index Contains

The fascination index is a cross-project registry of recurring themes — topics, mechanics, aesthetics, or emotional registers that a developer returns to across projects. It is written by `/autopsy` when a project is shelved or completed.

A typical entry looks like:

```yaml
entries:
  - theme: "productivity-rituals"
    description: "Tools and systems that work through ceremony rather than automation"
    intensity: high
    last_seen: 2025-11-03
    projects: ["day-timer", "focus-block"]

  - theme: "minimal-cli-tools"
    description: "Command-line tools that do one thing with no configuration"
    intensity: medium
    last_seen: 2025-09-14
    projects: ["leave", "context-snap"]
```

## How /spark Uses It

### Step 1: Read at session start

Read `~/.pyro/fascination-index.md` before generating any thumbnails. Extract all entries.

### Step 2: Match against input

Scan each entry for relevance to the developer's input (topic, domain, emotional register, scale). Use loose matching — a fascination with "local-first software" is relevant to a prompt about "syncing annoys me."

Do NOT force matches. If nothing genuinely connects, `fascinationThreads = []` and move on silently.

### Step 3: Thread into thumbnails

When a fascination theme is relevant:
- Design at least one thumbnail that explicitly draws from that theme's pattern
- Label that thumbnail with `← [theme name]`
- After the thumbnail set, call out the connection in one sentence

When calling out the connection, use language like:
- "I noticed your past fascination with [theme] — thumbnail 2 connects to that thread."
- "You've built around [theme] before — thumbnail 3 takes that direction."

Do NOT say:
- "Based on your history..." (sounds like surveillance)
- "You seem to always..." (presumptuous)
- "Given your pattern of..." (clinical)

### Step 4: Record in spark.md

When crystallizing, record the theme names used in `fascination_threads: []`.

## Empty or Missing Index

If `~/.pyro/fascination-index.md` does not exist or has `entries: []`:
- Continue normally
- Do not mention the absence to the developer
- Generate thumbnails without fascination thread labels
- `fascination_threads: []` in the output spark.md

## Intensity Weighting

If the index includes intensity levels, weight accordingly:
- `high` intensity: definitely check for relevance
- `medium` intensity: check if domain is close
- `low` intensity: only thread in if the match is unusually strong

## What NOT to Do

- Do not thread in a fascination just to show the index was read
- Do not generate thumbnails that are purely about a past fascination if it doesn't connect to the input
- Do not mention every fascination in the index — only the relevant ones
- Do not tell the developer they "always" do something based on 1-2 past projects
