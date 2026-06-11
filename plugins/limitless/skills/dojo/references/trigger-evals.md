# Trigger Evals — Matrix, Routing Judge, Scoring

The description is the only part of a skill that is always in context —
it does the triggering. This eval measures whether it triggers when it
should and stays quiet when it shouldn't. Triggering is exactly
measurable: which skill did the router pick.

## Matrix Design

10–15 prompts total:

- **~60% should-trigger positives** — phrased the way the user actually
  talks, not the way the description talks. Include slang, partial
  phrasings, and flag-style invocations ("--radar X"). If the skill has
  modes, cover each mode at least once.
- **~40% near-miss negatives** — prompts that *sound* adjacent but belong
  to another installed skill or to no skill at all. The best negatives
  name the same nouns ("twitter", "skill", "research") but a different
  job. For each negative, write down the expected owner.

A read-only skill should include a write-action negative ("post this on
twitter" → none). A research skill should include negatives owned by the
*other* research skills, because that's where collisions live.

## Harvesting the Description List

The routing judge needs the full competitive landscape: every installed
skill's `name: description` pair. The authoring session has this in its
own context (the available-skills listing) — copy it into the eval
prompt, including the new/updated skill's description. Do not abbreviate
the list; collisions hide in skills you didn't think were related.

## Routing-Judge Subagent Prompt Template

```
You are a skill-routing judge. Below is the list of installed skills
(name: description). For each user prompt, answer with the single skill
name you would invoke, or "none". Output one line per prompt:
"<n>: <skill-name>". No explanations.

SKILLS:
<full list including the new skill>

PROMPTS:
<numbered matrix>
```

Run with a fresh subagent. Then run the identical prompt with a second
fresh subagent — two runs catch flaky routing that one run hides.

## Scoring

- Exact match per row; a prompt passes only if both runs agree on the
  expected answer. Report `X/N` plus a per-row table in the dojo record.
- **Every positive must hit.** A missed positive means the user will type
  that phrase one day and nothing will happen.
- **Any negative landing on the new skill is a collision.** Collisions
  are worse than misses: they silently steal another skill's traffic.
- Ambiguous rows (two skills are both defensible owners) are allowed only
  if declared at matrix-design time, with both acceptable answers listed.

## Tuning

- **Missed positive** → add that phrasing (or its pattern) to the
  description's "Responds to" list. Don't add the literal prompt; add the
  shape ("what are people saying about X").
- **Collision** → sharpen the differentiator. Usually the fix is scoping
  a noun: "research" → "social media research"; "search" → "search
  Reddit and X". Check the colliding skill's description to find the
  word doing the damage.
- Re-run the full matrix (both subagents) after every description change
  — a fix for one row can break another.
- Three tuning rounds without convergence means the skill's territory
  overlaps an existing skill's for real. That's a scoping problem, not a
  description problem — go back to intake.
