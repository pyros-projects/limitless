# Thumbnail Format

A thumbnail is a one-paragraph concrete scenario. It is NOT:
- A feature list
- A pitch or value proposition
- A description of what the tool "would" do

It IS:
- Present tense, as if the thing already exists
- Specific: a particular person, a particular moment, a particular feeling
- Vivid enough that the developer can feel whether it resonates

## Structure

**[One-line title]** [← fascination thread label if applicable]

[One paragraph, 3-5 sentences:]
- Sentence 1: What is this thing? One declarative statement.
- Sentence 2-3: A specific moment in use. Who is doing what? What do they see/feel?
- Sentence 4-5: What changes for them? What's the before/after?

## What Makes a Good Thumbnail Set

The 3-5 thumbnails should DIVERGE, not cluster. They should represent genuinely different angles:
- Different users or contexts
- Different core mechanics or metaphors
- Different scales (personal tool vs. team tool vs. ambient utility)
- Different emotional registers (playful vs. serious, fast vs. slow)

If all thumbnails feel similar, regenerate with explicit divergence instructions.

## Fascination Thread Labels

If a thumbnail connects to a theme from the fascination index, label it:

`**3. [Title]** ← [theme name from fascination index]`

Only label when the connection is genuine — don't force associations. At most 1-2 thumbnails in a set should carry labels.

## Example (Topic: "I hate how I lose context when switching projects")

**1. The Context Capsule**
A tiny CLI tool that snapshots your mental state before you close a project. Before you switch away, it prompts: "What were you just thinking about? What's the next thing?" — two questions, nothing more. It writes a `.context` file. When you return, it shows you exactly what you were thinking, in your own words, from the moment you left.

**2. The Interrupt Log** ← productivity rituals
An always-on background process that watches for hard context switches — branch changes, new terminal windows, focus shifts to a new repo. It automatically captures the last 3 terminal commands and any open editor tabs into a timestamped note. You never have to remember to capture; it captures for you.

**3. The Resumption Ceremony**
A short daily ritual: open your project and get a 30-second "previously on..." — the last decision you made, the file you were editing, the test that was failing. It's not a task manager. It's a narrator. The goal is to get your brain back to where it was, not to tell you what to do next.
