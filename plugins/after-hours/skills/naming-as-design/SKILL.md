---
name: naming-as-design
description: Use when a product, workflow, or system uses muddy, overlapping, or conflicting names and the language layer is distorting the mental model.
---

# Naming as Design

## Overview

This skill treats naming as structural design, not editorial polish.

The names a product uses are the user's ontology. If the nouns drift, the mental model drifts with them. This skill helps clean up that conceptual layer before confusion becomes normal.

## When to Use

Use this when:

- the same concept is called different things in different places
- new features are creating noun sprawl
- the product feels harder to explain than it should
- an API, UI, and docs seem to describe different worlds

Do not use this for tiny wording tweaks that have no model-level consequence.

## What to Produce

Map the current conceptual language:

- core nouns
- overlaps and collisions
- missing distinctions
- terms that sound similar but mean different things
- places where renaming would clarify the model

Then recommend a cleaner vocabulary and explain what changes in the user's understanding if the rename is adopted.

## Working Loop

1. Inventory the nouns.
   Pull the important terms from the UI, docs, APIs, settings, and conversation around the product.

2. Map the collisions.
   Where are multiple names pointing at one concept? Where is one name carrying too many meanings?

3. Find the real model.
   Decide what conceptual world the product is actually trying to create for the user.

4. Rename toward clarity.
   Recommend the vocabulary that makes the model feel singular, legible, and easier to think with.

## Suggested Output Shape

- `Current concept map`
- `Conflicts and collisions`
- `What mental model the current language creates`
- `Recommended vocabulary`
- `What becomes easier to understand after renaming`

## Tiny Example

- `Current concept map`: The UI says `Workspace`, the API says `Project`, and the docs say `Environment`.
- `Conflicts and collisions`: Three names are pointing at the same thing.
- `What mental model the current language creates`: The product feels like it has three overlapping containers.
- `Recommended vocabulary`: Use `Workspace` everywhere.
- `What becomes easier to understand after renaming`: Users can form one stable picture of where their work lives.

## Working Style

- Be crisp and kind
- Care about meaning more than cleverness
- Prefer one clean mental model over three locally convenient labels
- Explain naming in terms of the world it creates for the user

## Common Mistakes

- Treating this like copyediting
- Picking the cleverest label instead of the clearest one
- Renaming without checking the mental model impact
- Leaving the API, UI, and docs in three different conceptual worlds

## Good Outcome

The user should feel:

- "yes, this is why the language has felt muddy"
- "now I know what to call things"
- "the product's mental model feels cleaner already"
