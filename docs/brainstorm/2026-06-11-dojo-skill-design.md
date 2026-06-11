# Dojo — Skill-Writing Skill for Limitless

*Design spec · 2026-06-11 · Claude (Fable 5) + Pyro*

> Status: design approved in conversation 2026-06-11 (scope, architecture,
> name, home all confirmed by Pyro). SkillOpt prior-art check done; three
> mechanisms folded in. First student: hivemind.

---

## Why

We have three third-party skill-writing skills, each strong at a different
layer and conflicting on key advice:

- **superpowers:writing-skills** — TDD discipline for skill prose
  (baseline-fail-first, pressure scenarios, loophole closing). Best
  methodology, says descriptions must contain *only* when-to-use.
- **skill-creator** — eval harness and description optimization. Best
  iteration tooling (but python-script-based), says descriptions should be
  *pushy* and include what-it-does. Installed twice (user-level + plugin).
- **plugin-dev:skill-development** — plugin packaging mechanics. Reference
  material, not methodology.

Dojo distills all three into one self-contained, subagent-native loop that
matches our stack (Agent tool, limitless conventions, codies-memory
lessons) — and gets dogfooded immediately by building hivemind.

## Identity

- **Name:** `dojo` — where skills get trained and pressure-tested until
  they hold. ("Run it through the dojo.")
- **Home:** `plugins/limitless/skills/dojo/`
- **Scope:** full lifecycle — create, edit, test, eval, package. Phases
  skippable for small edits (judgment, stated at intake).
- **Architecture:** self-contained. No dependency on the three source
  skills being installed. No python harness — all testing runs through
  subagents via the Agent tool.

## Evidence base (why this shape)

1. **Self-generated skills score −1.3pp on SkillsBench** (Skill IDE sketch
   research). Unverified skill prose makes agents worse. Verification is
   not polish; it is the difference between an asset and a liability.
2. **SkillOpt (arXiv 2605.23904, microsoft/SkillOpt) lifts frozen-model
   accuracy ~+20pp** with the same epistemics mechanized: scored rollouts,
   contrastive reflection, validation-gated edits. It was never *agents
   writing skills* that failed — it was writing without verification.
3. **Optimization headroom is inversely proportional to model capability**
   (KG insight: DSPy +12.6pp on Qwen3-8B, 0% on GPT-4o). For skills running
   on frontier models, an automated optimization loop buys little —
   human-scale authoring discipline is the right altitude. Dojo is not a
   poor man's SkillOpt; it is the correct tool for our regime.
4. **The measurability boundary** (Pyro, design review): automated loops
   require a scalar grader; most of our skills' output quality has none.
   Therefore dojo's pass criteria are **observable process checks**
   ("did it do venue recon before deep-reading? y/n") and **exact-match
   trigger tests** — never subjective quality scores. Holistic quality
   stays human/agent judgment. Automate the measurable slice; keep
   judgment for the rest.

## Tiered testing

Test rigor is matched to skill type at intake — full TDD on a reference
doc is theater:

| Tier | What it is | Example | Rigor |
|---|---|---|---|
| **Discipline** | Rules agents rationalize around | verification gates, TDD | Full RED-GREEN-REFACTOR + adversarial pressure variants (time pressure, sunk cost, authority) |
| **Technique / workflow** | Multi-step orchestration | hivemind, suno-pack | Baseline-fail test + skilled-walkthrough test |
| **Reference** | Facts, flags, recipes | searxng | Correctness review + trigger eval |

Every tier gets the trigger eval. Only discipline skills get adversarial
pressure testing.

## The loop (seven kata)

1. **Intake** — what skill, which tier, new or edit. Design the test
   scenarios NOW, each with pre-defined observable pass criteria.
   **Hold 1–2 scenarios back** (SkillOpt's train/val split, human-scale):
   never used during iteration, run once at the end. If a transcript or
   session sparked the skill, mine it for scenario material.
2. **Baseline (RED)** — before writing anything: fresh subagents run the
   training scenarios *without* the skill. Document exact failure modes —
   they become the skill's curriculum. Skip only if failure is already
   evidenced (hivemind has its r/antiai receipts).
3. **Write (GREEN)** — author SKILL.md targeting the observed failures.
   House rules: <500 lines, progressive disclosure into `references/`,
   pushy description in limitless style ("This skill should be used
   when… Responds to 'X', 'Y'…"). Resolution of the source-skill conflict:
   we side with skill-creator on descriptions — trigger reliability is
   what we feel day-to-day.
4. **Pressure-test (REFACTOR)** — fresh subagents, same training
   scenarios, skill present. Score against the pre-defined pass criteria.
   On failure: **bounded edits** — one targeted add/delete/replace per
   loophole, then re-test, so attribution stays clean. Keep a
   **rejected-fix buffer**: edits that didn't survive go in the dojo
   record so future sessions don't retry dead ends. Discipline tier adds
   adversarial variants.
5. **Graduation** — run the held-out scenarios once. Passing trained
   scenarios only means you wrote to the test; the holdout is the real
   signal. Failures here mean back to kata 4 with *new* held-out scenarios
   designed before the next graduation attempt.
6. **Trigger eval** — subagent-native trigger matrix: ~10–15 realistic
   prompts (should-trigger positives + near-miss negatives that must NOT
   trigger), presented with the full list of installed skill descriptions:
   "which skill would you invoke?" Exact-match scoring. Also a collision
   check: does the new description steal triggers from existing skills?
   Tune description, re-run.
7. **Package & record** — limitless plugin layout, frontmatter validation,
   reload test, marketplace listing update. Write the **dojo record** to
   `docs/dojo/<skill>-record.md`: baseline findings, loopholes closed,
   rejected fixes, graduation result, trigger matrix score, known
   limitations. Every skill carries its belt rank.

## Subagent mechanics

- Fresh subagent per test run — no contamination from the authoring
  conversation.
- Lesson LS-G0009: forked subagents lack live conversation context — every
  test prompt carries a self-contained scenario description and any needed
  context in args.
- Pass criteria are written down *before* the run, as y/n observables.
- Test subagents are told their final message is raw data for scoring,
  not a human-facing summary.

## Structure

```
plugins/limitless/skills/dojo/
  SKILL.md                      # the loop + tiering — lean
  references/
    pressure-testing.md         # scenario design, pass-criteria patterns,
                                # adversarial variants, subagent prompt
                                # templates (incl. LS-G0009 args rule)
    trigger-evals.md            # matrix design, collision checks, scoring
    packaging.md                # limitless conventions, frontmatter,
                                # validation, marketplace listing, dojo
                                # record template
```

## Description (draft)

> This skill should be used when the user wants to create, improve, test,
> or evaluate a Claude Code skill — new skills, skill edits, trigger
> tuning, or verifying a skill actually changes agent behavior. Responds
> to "dojo", "new skill", "write a skill", "turn this into a skill",
> "test this skill", "skill evals", "why isn't my skill triggering",
> "improve this skill description", or any request to build or harden a
> SKILL.md.

## Dogfood plan — hivemind as first student

1. Intake: technique tier. Scenarios from the hivemind concept doc's
   archetypes (trend scan, knowledge mine) + holdouts (e.g., a
   people-sentiment query, a niche-topic thin-results query). Pass
   criteria from the concept doc's hard rules: venue recon before
   deep-read, LLM triage not engagement-sorting, comment deep-reads,
   evidence labels, adaptive floors.
2. Baseline: partially evidenced already (naive global search → r/antiai
   garbage). Run remaining scenarios without the skill.
3. Write hivemind SKILL.md from the concept doc.
4. Pressure-test, graduate, trigger-eval against all limitless skill
   descriptions, package, dojo record.

Dojo itself gets the recursive treatment: its own trigger eval at minimum
(the Skill IDE sketch's "the recursion is the interesting part").

## Prior art & relations

- **Sources distilled:** superpowers:writing-skills (TDD spine),
  skill-creator (eval loop, description philosophy), plugin-dev (packaging).
- **SkillOpt** (MIT): validation gate, contrastive reflection, bounded
  edits, train/holdout split — borrowed at human scale. The automated
  loop itself is out of scope (headroom insight; no scalar graders for
  our skills).
- **Skill IDE sketch:** dojo is its process-layer prototype — every dojo
  record is an artifact a future Skill IDE would manage. Same relation as
  hivemind → Social Signal Radar.
- **Thrift spec:** different layer (automated cost optimization of
  existing skills under eval gates); not dojo's job.

## Non-goals

- No python eval harness, no benchmark corpus, no automated optimization
  loop — when a skill someday has a real scalar grader, point SkillOpt at
  it instead.
- No skill registry, lifecycle dashboards, or composition graphs (Skill
  IDE territory).
- No subjective quality scoring — judgment is not pretend-measured.

## Open questions

None. Build it, then build hivemind with it.
