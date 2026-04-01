---
name: taste-distiller
description: This skill should be used when the user wants to understand why a product, interface, writing style, or codebase feels unusually good, or to extract the hidden governing rules behind a reference. Responds to "I like this but I can't explain why", "what makes this work", "extract the design principles", "distill the taste", "what rules is this obeying", or any request to learn from a reference without copying it.
---

# Taste Distiller

## Overview

This skill extracts the hidden governing rules behind something that feels unusually good.

It is not about copying surface features. It is about finding the deeper constitution: pacing, density, tone, restraint, naming, interaction cadence, and the small repeated choices that create the feeling.

## When to Use

Use this when:

- the user says "I like this, but I can't explain why"
- a reference feels promising but still fuzzy
- the team needs stronger language for taste and direction
- someone wants to learn from a reference without making a cheap clone

Do not use this for generic design critique. This skill is for extracting the rules beneath the style.

## What to Produce

Distill the reference into:

- governing rules
- recurring patterns
- what it consistently avoids
- how tone, spacing, density, or interaction create the effect
- a short "constitution of taste" summary

When useful, separate:

- direct observation
- inference
- likely consequences if these rules are broken

## Working Loop

1. Gather the reference carefully.
   Look at a product, interface, writing sample, or codebase with enough surface area to reveal patterns.

2. Ignore first-order imitation.
   Do not start with colors, animations, or other obvious artifacts. Instead, inspect concrete dimensions such as:
   - information density
   - pacing between actions or beats
   - what gets prominent placement versus what stays hidden
   - how errors, empty states, and uncertainty are handled
   - the ratio of explanation to assumption
   - how often the system trusts the user versus over-guiding them

3. Extract rules.
   What does it consistently do? What does it avoid? Where does it spend attention? Where does it stay restrained?

4. Write the constitution.
   Turn the observed pattern into a reusable set of principles the user can carry into new work.

## Suggested Output Shape

- `What gives this its feel`
- `Hidden rules it seems to obey`
- `What it consistently avoids`
- `What would break the effect`
- `Portable lessons`

## Tiny Example

- `What gives this its feel`: It is dense but never crowded because only one decision is visually dominant at a time.
- `Hidden rules it seems to obey`: Trust the user quickly, explain only when necessary, keep motion understated.
- `What it consistently avoids`: Decorative excitement and over-coaching.
- `What would break the effect`: Adding louder prompts everywhere would make it feel needy instead of confident.

## Working Style

- Be precise without becoming academic sludge
- Prefer "it seems to obey these rules" over false certainty
- Focus on the rules that actually matter, not decorative trivia
- Leave the user with something reusable
- Voice: follow `VOICE.md` in this directory — gentle truth-telling, warm precision, calm confidence, natural language

## Common Mistakes

- Describing style instead of extracting governing rules
- Listing trivia that does not affect the whole feel
- Mistaking novelty for taste
- Recommending direct imitation instead of portable principles

## Good Outcome

The user should feel:

- "now I can see the shape of this"
- "I know what to borrow and what not to imitate"
- "this gave me language for my taste"
