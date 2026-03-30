---
name: ghost-user
description: Use when something seems obvious to the builders and you want a cold first-contact pass from a first-time user with zero context or author knowledge.
---

# Ghost User

## Overview

This skill simulates first contact.

Not a power user.
Not a chaos monkey.
Not a formal usability study.

Just a quiet first-time user moving through the surface with no internal context and no special sympathy for what the builders meant.

## When to Use

Use this when:

- a flow feels "obvious" and you want to verify that
- onboarding is thin or absent
- the product may be assuming too much prior knowledge
- you want a first-contact honesty pass without setting up full user research

Do not use this to invent edge cases for sport. Stay close to plausible first-use reality.

If you have already read project docs, architecture notes, or implementation details in the current session, explicitly say that your ghost-user pass is partially contaminated and flag which observations may be insider-influenced.

## What to Produce

Walk through the product or flow as the ghost user would:

- what they notice first
- what they assume
- what confuses them
- what feels invisible
- what requires author knowledge to decode

Narrate it plainly. The power of this skill is not sophistication. It is honesty.

## Working Loop

1. Forget the author view.
   Start from the surface alone. Do not read README files, docs, architecture notes, or source code before the pass if the raw product surface is available.

2. Walk the first contact honestly.
   What do I see? What do I think this means? What do I try next?

3. Notice the invisible assumptions.
   Where is the product assuming vocabulary, confidence, or prior knowledge the user has not earned yet?

4. End with the highest-leverage fixes.
   Do not drown the user in notes. Point to the few changes that would most improve first contact.

## Suggested Output Shape

- `What I notice first`
- `What I assume`
- `Where I get confused`
- `What required inside knowledge`
- `The 3 highest-leverage fixes`

## Tiny Example

- `What I notice first`: I see a button called `Init`.
- `What I assume`: Maybe it creates something, but I do not know what.
- `Where I get confused`: Clicking it changes the page, but nothing tells me what happened.
- `What required inside knowledge`: Knowing that `Init` means "create a new workspace."
- `The 3 highest-leverage fixes`: Rename the button, add immediate confirmation, and show the created thing in context.

## Working Style

- Stay literal and grounded
- Do not smuggle in insider understanding
- Prefer "I see a button called init and I do not know what that means" over design jargon
- End with the few changes that would most improve first contact

## Common Mistakes

- Performing clever critique instead of staying naive
- Jumping to rare edge cases instead of plausible first contact
- Importing insider knowledge halfway through the walk
- Ending with too many fixes instead of the highest-leverage ones

## Integrity Rule

If the product surface is available, raw surface beats documentation.

If you cannot avoid prior knowledge, say so plainly:

- what you already knew
- which observations may be contaminated
- what a cleaner ghost-user pass would require

## Good Outcome

The user should feel:

- "right, that would not be obvious at all"
- "I can see where we were relying on inside knowledge"
- "this gives me a cleaner first-use path"
