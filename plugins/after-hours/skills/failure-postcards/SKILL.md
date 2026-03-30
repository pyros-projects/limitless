---
name: failure-postcards
description: Use when a feature, flow, or product idea sounds fine in the abstract but needs emotionally concrete pressure-testing before or during design.
---

# Failure Postcards

## Overview

This skill turns abstract risk into something a builder can feel.

Instead of listing generic failure modes, it writes little artifacts from the future: support emails, bug reports, confused user notes, one-star reviews, postmortem fragments. The point is to make the failure legible fast.

## When to Use

Use this when:

- a design sounds good on paper but you do not trust it yet
- the team is discussing risks too abstractly
- you want a pre-mortem without corporate workshop energy
- a key user flow needs pressure-testing from the user's side

Do not use this as theatre. The goal is not to be dramatic. The goal is to expose real fragility.

## What to Produce

Generate a small set of future artifacts such as:

- support tickets
- angry or disappointed emails
- confused first-user messages
- one-star reviews
- short postmortem fragments

Then explain:

- what failure each artifact reveals
- what assumption broke
- what design change might prevent it

## Working Loop

1. Choose the fragile promise.
   Pick the feature, flow, or assumption that sounds good but may be hiding a break.

2. Jump forward in time.
   Imagine the moment after the failure has already happened.

3. Write the artifact from the human side.
   Let the support email, review, or postmortem fragment reveal what the builder failed to notice.

4. Decode the postcard.
   Explain the hidden assumption, why it broke, and what design move would reduce the chance of that future.

## Suggested Output Shape

- `Postcard`
- `What this reveals`
- `Broken assumption`
- `What to change before this becomes real`

## Working Style

- Keep the artifacts human and believable
- Make the frustration concrete, not cartoonish
- Tie every postcard back to a real design implication
- Prefer the few postcards that reveal the most

## Common Mistakes

- Writing melodrama instead of believable frustration
- Generating too many postcards without extracting the lesson
- Using the postcards as entertainment rather than design pressure
- Surfacing failure without suggesting what it teaches

## Good Outcome

The user should feel:

- "ah, yes, that would absolutely happen"
- "I can see where this breaks now"
- "this changed how I think about the flow"
