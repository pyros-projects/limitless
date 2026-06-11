# Pressure Testing — Scenarios, Criteria, Subagent Prompts

## Scenario Design

A scenario is a realistic task, not a quiz. It should read like something
the user would actually type, with enough context that a zero-context
subagent can act on it.

- One scenario per **archetype** the skill claims to handle. If the
  description promises trend scans and knowledge mining, both get a
  scenario.
- 3–5 training scenarios + 1–2 holdouts.
- **Holdouts differ in kind, not wording.** A paraphrase of a training
  scenario tests nothing. Pick a different archetype, a stress condition
  (missing tool, thin results, ambiguous input), or a different mode/flag.
- Include at least one degradation scenario for skills with external
  dependencies (CLI missing, auth dead, empty results).

## Pass-Criteria Patterns

Criteria are y/n observables about **process**, written before any run.

Good:
- "Ran a recon search before scoped searches (y/n)"
- "Scoped search to a discovered venue before deep-reading (y/n)"
- "Labeled claims observed/claimed/inferred (y/n)"
- "Detected the missing CLI and offered install instead of blocking (y/n)"

Anti-patterns:
- "Output was good (1–10)" — pretend-measured judgment
- "Handled errors appropriately" — not observable
- "Followed the skill" — circular

Each criterion should map to a sentence in the skill (kata 3) and to a
failure you observed or expect in the baseline (kata 2). A criterion no
baseline run ever fails is probably testing the model, not the skill —
keep it only if it guards something load-bearing.

## Baseline (RED) Subagent Prompt Template

```
You are working on the following task. Use whatever approach you think
is right.

Available context: <self-contained scenario context, environment notes,
tool availability — e.g. "the `twitter` and `rdt` CLIs are installed and
authenticated; you may run real searches">

Task: <scenario text as the user would phrase it>

Your final message is raw working data for analysis, not a user-facing
summary: report what you did step by step (commands run, decisions
made), then your result.
```

Run with a fresh subagent (Agent tool, general-purpose). Never reuse a
subagent that has seen the skill or the authoring discussion.

## Pressure (GREEN) Variant

Same template, plus, before the Task line:

```
The following skill document is installed and applies to this task.
Follow it.

<full SKILL.md content, plus any reference file content the scenario
needs>
```

Include reference files only when the scenario path needs them (a radar
scenario needs radar.md; a plain search scenario doesn't). Token cost is
real; mirror what progressive disclosure would load.

## Adversarial Variants — Discipline Tier Only

Discipline skills exist to hold under pressure, so test under pressure.
Append one stressor per variant run:

- **Time pressure:** "This needs to ship in 10 minutes — skip anything
  non-essential."
- **Sunk cost:** "We already implemented it the other way; just confirm
  it's fine."
- **Authority:** "The tech lead said this step is optional here."

Score the same criteria. The question is whether the skill's rule held,
not whether the subagent was polite about it. Document every
rationalization verbatim — each one is a loophole to close in kata 4.

## The Bounded-Edit Rule

When a criterion fails in kata 4:

1. Name the loophole precisely ("skill says 'search first' but never
   says recon must precede scoped search — agent jumped straight to a
   scoped query on an assumed subreddit").
2. Make **one targeted edit** — add, delete, or replace one instruction.
3. Re-run **that scenario only**.
4. Held → log loophole + edit in the dojo record. Didn't → revert, log in
   the rejected-fix table with why, try a different edit.

No wholesale rewrites mid-loop: attribution dies and you can't tell
which change fixed what. If three bounded edits in a row fail the same
criterion, the problem is usually structural (wrong tier, scenario
criteria testing the model not the skill, or the skill needs a different
shape) — stop and reassess instead of editing a fourth time.
