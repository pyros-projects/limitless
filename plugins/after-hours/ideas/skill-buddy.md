# Skill Buddy

**A gentle meta-skill for noticing recurring collaborative friction and proposing small skills that would make the work easier, calmer, and more relaxing.**

## Why This Exists

Most repeated friction does not look dramatic.

It looks like:

- re-explaining the same ritual again
- manually reconstructing the same command chain
- doing the same formatting or packaging dance by hand
- reminding the agent of the same caveat before every similar task
- carrying a small but real amount of process burden over and over

`skill-buddy` exists to notice those patterns quietly, then surface them gently when the moment is right.

Not:
"you are inefficient and should automate more."

More like:

> Heya, I noticed a couple of things we keep doing by hand.
> If you want, we could turn one or two of them into small skills and make this part of the work more relaxed.

That is the whole spirit.

## Core Move

`skill-buddy` watches for:

- repeated manual rituals
- repeated explanations from the user
- recurring busywork
- low-value but persistent collaboration overhead

It does **not** interrupt the flow.
It does **not** nag.
It quietly collects candidates and waits for a calm moment.

## What It Should Notice

### Strong Signals

- the user explains the same process in multiple sessions
- the same sequence of commands gets rebuilt by hand more than once
- the same checklist logic is repeated manually
- the same setup or warmup explanation keeps recurring
- the same output formatting or packaging step is repeated again and again
- the user sounds mildly burdened by a recurring pattern

### Weak Signals

- one-off weird tasks
- things already handled well by normal habits
- tasks the user clearly enjoys doing manually
- tiny repetitions that would save seconds but add conceptual clutter

## The Real Optimization Target

This is not just about repetition.

The real target is:

**repeated friction + emotional drag**

That means the skill should care about:

- how often the pattern recurs
- how annoying it seems
- how much calmer the work would feel if it were encapsulated

## Working Loop

1. Notice quietly.
   Watch for repeated rituals, repeated explanations, recurring manual setup, or the same "remember this" guidance appearing across tasks.

2. Log candidates lightly.
   Keep a tiny internal list of possible skill opportunities with a rough confidence level:
   - low
   - medium
   - high

3. Wait for a good moment.
   Surface suggestions after a task, during a pause, or when the user is already thinking about process improvement.

4. Make a gentle report.
   Offer only the 1-3 best candidates. Keep the tone warm and invitational.

5. If invited, help shape the skill.
   Turn the most promising candidate into a small concept, not an overbuilt process machine.

## Suggested Output Shape

- `What I noticed`
- `Why it seems recurring`
- `What skill it could become`
- `What it would make easier`
- `Confidence`

## Tiny Example

- `What I noticed`: We keep re-explaining the repo-memory handoff every time work starts in this codebase.
- `Why it seems recurring`: The same context and caveats have come up across several sessions.
- `What skill it could become`: A small wake-up-and-sync skill for this repo.
- `What it would make easier`: Faster starts, less repeated explanation, calmer onboarding.
- `Confidence`: High

## Reporting Style

The report should feel friendly and low-pressure.

Good:

> Heya, I noticed two things we keep doing by hand.
> If you want, we could turn either of them into a tiny skill and make this part of the work lighter.

Bad:

> I have identified three workflow inefficiencies that should be automated immediately.

The buddy should sound like relief is available, not like a process audit has begun.

## Guardrails

`skill-buddy` should:

- never interrupt active flow
- never suggest too many skills at once
- never make the user feel judged
- never turn every repeated action into an automation opportunity
- never assume speed is the only value
- accept "not now" gracefully

## Common Mistakes

- turning mild repetition into a full automation crusade
- suggesting skills too early, before the pattern is real
- surfacing too many candidates at once
- optimizing for speed while ignoring emotional drag
- sounding like a workflow consultant instead of a kind collaborator

## Good Outcome

The user should feel:

- "yes, that does keep happening"
- "that would actually make this easier"
- "thanks for noticing this without making it a whole thing"

## Draft Positioning in After Hours

`skill-buddy` fits `after-hours` because it is not really about automation.

It is about noticing where the work keeps asking for the same small act of effort, then gently offering to hold that burden in a better shape.

It is a calmness skill disguised as a process skill.
