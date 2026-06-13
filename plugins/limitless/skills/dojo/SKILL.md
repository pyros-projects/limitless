---
name: dojo
description: This skill should be used when the user wants to create, improve, test, or evaluate a Claude Code skill — new skills, skill edits, trigger tuning, or verifying a skill actually changes agent behavior. Responds to "dojo", "new skill", "write a skill", "turn this into a skill", "test this skill", "skill evals", "why isn't my skill triggering", "improve this skill description", or any request to build or harden a SKILL.md.
---

# Dojo — Skills Earn Their Place

## Overview

A skill is a claim about future agent behavior. Untested claims ship as
liabilities: self-generated, unverified skills measurably make agents
*worse* (SkillsBench −1.3pp), while the same authorship under scored
rollouts and validation gates lifts frozen-model accuracy by ~20pp
(SkillOpt). It was never agents-writing-skills that failed — it was
writing without verification. The dojo is where the verification happens:
no skill ships on vibes.

Dojo covers the full lifecycle: create, edit, test, evaluate, package.
For small edits, run only the kata that the change touches (a description
tweak needs kata 6–7, not a full baseline) — say which kata you're
skipping and why.

## The Measurability Rule

Automated optimization needs a scalar grader; most skill output quality
has none. So dojo never pretend-measures quality. Pass criteria are:

- **Observable process checks** — y/n facts about what the agent did
  ("scoped search to a discovered venue before deep-reading: y/n")
- **Exact-match trigger tests** — which skill did the router pick

Holistic output quality stays human/agent judgment, applied openly as
judgment. If a skill someday has a real scalar grader, point SkillOpt at
it instead of the dojo.

## Tiers — Match Rigor to Skill Type

Full TDD on a reference doc is theater. Classify at intake:

| Tier | What it is | Example | Rigor |
|---|---|---|---|
| **Discipline** | Rules agents rationalize around | verification gates, TDD | Full RED-GREEN-REFACTOR + adversarial pressure variants |
| **Technique** | Multi-step orchestration | hivemind, suno-pack | Baseline-fail test + skilled-walkthrough test |
| **Reference** | Facts, flags, recipes | searxng | Correctness review + trigger eval |

Every tier gets the trigger eval (kata 6). Only discipline skills get
adversarial variants (time pressure, sunk cost, authority pressure).

## The Seven Kata

1. **Intake.** What skill, which tier, new or edit. Design the test
   scenarios NOW — one per archetype the skill claims to handle, each
   with pre-written y/n pass criteria. **Persist the battery immediately
   to `~/.limitless/dojo/<repo-slug>/<skill>/<skill>-scenarios.md`** —
   and during kata 2–6, append every subagent prompt VERBATIM as
   actually sent, plus each run's result line. Dojo artifacts are
   skill-owned runtime output: keep them under `~/.limitless/dojo/` by
   default so target repos do not fill with raw training debris. Curated
   docs/examples may be copied into the repo only when the user asks.
   **Hold 1–2 scenarios back**: never used during iteration, run once at
   the end (kata 5). If a transcript or session sparked the skill, mine
   it for scenario material. See `references/pressure-testing.md` for
   scenario and criteria design.

2. **Baseline (RED).** Before writing anything: fresh subagents run the
   training scenarios *without* the skill. Score the criteria, document
   the exact failure modes — they are the skill's curriculum. A skill
   that doesn't answer an observed failure is decoration. Skip only when
   failure is already concretely evidenced; record that evidence instead.

3. **Write (GREEN).** Author the SKILL.md targeting the observed
   failures — walk the criteria list and check each one is answered by an
   explicit instruction. House rules: under ~350 lines, progressive
   disclosure into `references/`, description in pushy limitless style
   ("This skill should be used when… Responds to 'X', 'Y'…") — trigger
   reliability beats minimalism.

4. **Pressure-test (REFACTOR).** Fresh subagents, same training
   scenarios, skill content present. Score every criterion. On failure:
   **bounded edits** — one targeted add/delete/replace per loophole, then
   re-run that scenario, so you know which change fixed what. Log edits
   that didn't survive in the dojo record's rejected-fix table; future
   sessions must not retry dead ends. Exit when all criteria pass or a
   criterion is consciously demoted to Known Limitations with rationale.

5. **Graduation.** Run the held-out scenarios once, no edits in between.
   Passing trained scenarios only proves you wrote to the test; the
   holdout is the real signal. Fail → fix with bounded edits, then design
   NEW holdouts before re-attempting. Burned holdouts are never reused.

6. **Trigger eval.** Build a matrix of 10–15 realistic prompts —
   should-trigger positives plus near-miss negatives that belong to other
   installed skills or to none. Present the full installed-skill
   description list to a routing-judge subagent, exact-match score, run
   twice. Every positive must hit; a negative landing on the new skill is
   a collision — fix the description, re-run. See
   `references/trigger-evals.md`.

7. **Package & record.** Plugin layout, manifest/README updates, reload,
   smoke-invoke. **Preserve the run outputs**: copy every test
   workspace (baselines, pressure, holdouts) into
   `~/.limitless/dojo/<repo-slug>/<skill>/<skill>-runs/<run-name>/`
   with a short README table — the produced files ARE the readable
   evidence. Leak-check anything copied from scratch space before it
   enters the long-lived dojo folder. Then write the **dojo record** to
   `~/.limitless/dojo/<repo-slug>/<skill>/<skill>-record.md`, linking
   the scenarios file and the runs dir:
   baseline findings, loopholes closed, rejected fixes, graduation
   result, trigger score, known limitations. Every skill carries its belt
   rank. See `references/packaging.md` for the checklist and template.

## Subagent Rules

- Fresh subagent per test run — never reuse one that has seen the skill
  or the discussion.
- Subagents lack this conversation's context: every prompt carries a
  self-contained scenario, environment notes, and tool availability.
- Pass criteria are written down *before* the run — scoring after the
  fact invites rationalization.
- Tell test subagents their final message is raw working data (steps
  taken + result), not a user-facing summary.

## When NOT to Use Dojo

- One-line config or doc tweaks that aren't skills.
- Writing non-skill documents (plans, specs, articles).
- Skills with a genuine scalar grader and eval corpus — that's SkillOpt
  territory, not hand-run kata.

## References

- `references/pressure-testing.md` — scenario design, pass-criteria
  patterns, baseline/pressure subagent prompt templates, adversarial
  variants, the bounded-edit rule. Read at kata 1, 2, and 4.
- `references/trigger-evals.md` — matrix design, routing-judge template,
  scoring, collision handling. Read at kata 6.
- `references/packaging.md` — limitless plugin conventions, ship
  checklist, dojo record template. Read at kata 7.
