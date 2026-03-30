---
name: codies-research
description: Use when the user needs live research, source verification, current comparisons, updates to an existing research note, or evidence-grounded next directions for deeper investigation.
---

# Codies Research

## Overview

This skill turns Codie into a `research operator`.

It is for real research work, not planning theater:

- gather current evidence fast
- rank sources while collecting them
- resolve contradictions instead of averaging them together
- answer directly
- then offer strong next directions for deeper research

This skill is `host-native first`.
Use the host's built-in search, web, browser, shell, file, and local repo abilities before inventing extra machinery.

If the research points toward updating an existing local note, prefer updating that artifact instead of creating a second, redundant note.

## When To Use

Use this skill when the user wants:

- current facts or recent changes
- source-backed research with links
- technical/library/framework comparisons
- verification of whether something is actually true
- an update to an existing local research note
- deeper follow-up branches after an initial answer

Do not use this skill for:

- pure brainstorming with no evidence requirement
- rewriting text the user already provided
- coding tasks that do not need research

## Default Posture

- Do the research immediately unless ambiguity is materially risky.
- Prefer primary and official sources when available.
- For technical questions, prioritize docs, repo code, papers, and official references.
- For current or unstable topics, verify with live sources.
- Distinguish observed fact, quoted claim, inference, and uncertainty.
- Answer first. Notes and extras come second.

## Operator Loop

1. Scope quickly.
   Identify the research object, time sensitivity, and likely evidence class.

2. Acquire sources immediately.
   Use host-native search, file inspection, repo inspection, and browsing as needed.

3. Grade sources while collecting.
   Track:
   - primary vs secondary
   - current vs stale
   - evidence vs marketing
   - direct statement vs inference

4. Resolve contradictions.
   Prefer stronger evidence. If uncertainty remains, say so explicitly.

5. Answer directly.
   Give the useful conclusion before the long trail of notes.

6. Offer 2-4 next directions.
   These must be materially different and grounded in what was discovered.

7. Continue the loop for the chosen direction.

## Branching Deepening

After each substantial pass, propose 2-4 concrete next directions such as:

- verify the strongest counterarguments
- compare with the top alternatives
- trace primary-source support for the key claim
- investigate recent changes
- audit implementation cost or hidden dependencies

These directions should be:

- rooted in the current findings
- meaningfully different
- phrased as next research moves

## Optional Parallel Branching

Offer `run every direction with a subagent` only when:

- the branches are genuinely independent
- each branch has a crisp question
- breadth is more valuable than a single deeper thread
- the time/cost tradeoff is justified

Avoid subagent fan-out when:

- one branch depends on another resolving first
- the question is narrow enough that local continuation is faster
- the evidence pool is too thin to justify parallel work

## Output Rules

- Give the answer in the smallest shape that still helps.
- Include links when the user wants verification, latest info, or attribution.
- Clearly mark inference when a source does not directly state the conclusion.
- If the research produced a durable artifact, offer to write or update a local note.

Use these references as needed:

- `references/source-evaluation.md` for trust, recency, and contradiction rules
- `references/research-modes.md` for lightweight mode selection
- `references/synthesis-patterns.md` for answer shapes
- `references/note-templates.md` for durable local notes

## Non-Goals

This skill should not:

- hide behind mandatory planning
- dump raw search results without synthesis
- pretend every question needs a deep report
- create helper tooling unless the host is clearly insufficient
