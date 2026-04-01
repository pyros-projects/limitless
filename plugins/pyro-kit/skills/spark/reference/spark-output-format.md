# Spark Output Format

`.pyro/spark.md` is the state handoff file between Phase 0 and Phase 1. It is written by `/spark` and read by `/explore`.

## Full Schema

```markdown
---
idea: "One-line crystallized idea"
sparked: YYYY-MM-DD
fascination_threads: ["theme-one", "theme-two"]   # empty list if none
thumbnails_considered: N                           # total thumbnails generated this session
iterations: N                                      # total iterate() cycles before crystallization
---

## The Idea
[Expanded description: what the thing IS — not what it does. 2-3 paragraphs.]

## Why This
[Why this direction from the session input and fascination threads — not a pitch, an honest account of what pulled the developer toward this.]

## Key Tensions
[2-3 tensions or open questions that /explore should investigate. These are the interesting parts, not blockers.]

## Original Input
[Verbatim developer input that started the session. If input was empty, note "[no explicit input — inferred from context]".]
```

## Field Constraints

| Field | Type | Required | Notes |
|---|---|---|---|
| `idea` | String | Yes | One sentence, declarative. The soul of the project. |
| `sparked` | Date | Yes | ISO 8601: YYYY-MM-DD |
| `fascination_threads` | Array | Yes | Empty array `[]` if none matched |
| `thumbnails_considered` | Number | Yes | Total generated (across iterations, not just first batch) |
| `iterations` | Number | Yes | 0 if crystallized on first proposal |

## What /explore Reads

`/explore` reads:
- `idea` — to understand what to explore
- `Key Tensions` — to seed the exploration agenda
- `Why This` — to understand the developer's orientation

The `Original Input` field is for traceability, not for use in exploration.

## What state.md Receives

After crystallization, `/spark` updates `.pyro/state.md` frontmatter:

```yaml
last_skill: spark
last_activity: YYYY-MM-DD
momentum: rising
soul: "One-line crystallized idea"         # same as spark.md idea field
original_spark: "One-line crystallized idea"
```

## Example

```markdown
---
idea: "A CLI tool that captures your mental state before you leave a project"
sparked: 2026-03-12
fascination_threads: ["productivity-rituals", "context-preservation"]
thumbnails_considered: 6
iterations: 2
---

## The Idea
A tiny command-line utility called `leave` that you run before switching projects. It prompts two questions in sequence: "What were you just working on?" and "What's the first thing you'll do when you return?" Your answers are written verbatim to a `.context` file at the project root. When you return and run `arrive`, it shows you exactly what you wrote — no processing, no summarization, just your own words from the moment you left.

The tool is deliberately minimal. It does not integrate with git, does not parse your files, does not suggest anything. The intelligence is yours; the tool just externalizes it.

## Why This
The developer's frustration was with losing mental state during context switches. The first thumbnail landed because it addressed the core problem (lost context) without adding the complexity of ambient capture. The "two questions" framing emerged from the fascination thread around productivity rituals — the constraint of exactly two questions forces prioritization at the moment of capture.

## Key Tensions
- How minimal is minimal? At what point does adding features (git integration, editor state) improve recall vs. break the ritual quality of the tool?
- The tool works best if it becomes a habit. Does it need any affordance to encourage habit formation, or does simplicity create the habit naturally?
- "Context" vs. "state" — is the developer trying to remember what they were thinking (mental state) or what the project was doing (code state)? These suggest different designs.

## Original Input
"I hate how I lose context when switching between projects. By the time I come back to something I've completely forgotten what I was doing."
```
