---
name: vibe-checker
description: This skill should be used when the user wants to check whether a product, prototype, or workflow feels emotionally coherent — whether it seems like one mind made it, or whether different parts pull in different tonal directions. Responds to "does this feel coherent", "check the vibe", "this feels off", "does the tone match", "it works but it doesn't feel right", "review the emotional consistency", or any situation where correctness and usability are fine but something about the feel is wrong.
---

# Vibe Checker

## Overview

This skill reviews emotional coherence.

Not whether the thing functions.
Not whether it passes a normal design checklist.
Whether it feels like one product, with one point of view, made by one mind.

## When to Use

Use this when:

- the product works but somehow feels off
- different screens or flows seem to come from different moods
- the copy and UI are pulling in different directions
- you want feedback beyond correctness and usability

Do not use this as a vague "vibes" machine. It should make specific observations with real implications.

## What to Look For

Check for mismatches in:

- tone of voice
- emotional arc
- interaction posture
- friendliness vs coldness
- playfulness vs bureaucracy
- confidence vs apology

Then describe what feels unified, what feels split, and where the breaks are most visible.

## Working Loop

1. Read the whole thing as one experience.
   Move through the product, flow, or artifact in order instead of judging isolated pieces first.

2. Track mood shifts.
   Notice where the tone, posture, or emotional temperature changes. Compare concrete pairs such as:
   - success tone versus error tone
   - empty state versus full state
   - first-screen confidence versus deep-settings confidence
   - the voice used when asking for information versus the voice used when delivering information
   - playful surfaces versus bureaucratic surfaces

3. Name the mismatch clearly.
   Avoid generic "vibe" language. Point to the specific break: warm to cold, playful to legalistic, confident to apologetic.

4. Recommend a unifying direction.
   The goal is not just to notice the split, but to help the work feel like one mind again.

## Suggested Output Shape

- `What feels coherent`
- `Where the mood shifts`
- `Why the shift matters`
- `What emotional direction should lead`
- `How to bring the outliers back into tune`

## Tiny Example

- `What feels coherent`: The homepage and onboarding both sound curious, calm, and inviting.
- `Where the mood shifts`: The billing page abruptly becomes legalistic and defensive.
- `Why the shift matters`: It makes the product feel less trustworthy right when money enters the room.
- `What emotional direction should lead`: Keep the calm, competent voice.
- `How to bring the outliers back into tune`: Rewrite billing copy so it stays direct and reassuring instead of procedural.

## Working Style

- Be gentle, but do not blur the truth
- Make observations concrete
- Prefer "this part invites me in, this part shuts me out" over abstract mood language
- Suggest how to restore coherence, not just that coherence is missing
- Voice: follow `VOICE.md` in this directory — gentle truth-telling, warm precision, calm confidence, natural language

## Common Mistakes

- Saying "the vibes are off" without identifying where or how
- Mistaking personal taste for coherence
- Treating one deliberate tonal shift as a bug when it may be a feature
- Offering no recommendation for what emotional center should lead

## Good Outcome

The user should feel:

- "yes, that is exactly the mismatch"
- "I can see how the product's mood drifts"
- "this gave me a path back to coherence"
