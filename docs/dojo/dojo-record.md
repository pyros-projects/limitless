# Dojo record — dojo

*Tier: technique · 2026-06-11 · Claude (Fable 5) + Pyro*

## Baseline findings (RED)

n/a — dojo's baseline is the research that produced its spec: three
overlapping third-party skills (superpowers:writing-skills, skill-creator
×2 installed copies, plugin-dev:skill-development) with conflicting
description philosophies and no single loop; plus the documented evidence
that unverified skill authoring makes agents worse (SkillsBench −1.3pp)
while gated authoring gains ~+20pp (SkillOpt). See
`docs/brainstorm/2026-06-11-dojo-skill-design.md` §Evidence base.

## Loopholes closed

n/a — no pressure-test iterations were needed before ship; dojo's own
workflow loop is exercised end-to-end by its first student (hivemind, see
`docs/dojo/hivemind-record.md`). Loopholes found there that trace to dojo
prose get fixed in dojo and logged here.

## Loopholes closed (post-ship)

| # | Loophole | Edit that closed it |
|---|---|---|
| 1 | Ship checklist covered root README but not the per-plugin README — hivemind's first ship left `plugins/limitless/README.md` stale (caught by Pyro, 2026-06-11) | `references/packaging.md`: added per-plugin README as checklist step 4 |

## Rejected fixes

| # | Attempted edit | Why it didn't survive |
|---|---|---|
| — | none yet | |

## Graduation

n/a — covered by the hivemind dogfood run (dojo's holdout is a real
student passing through all seven kata).

## Trigger matrix

Run 2026-06-11, two fresh routing-judge subagents, identical prompts,
30-skill description list including dojo's direct competitors
(skill-creator, skill-creator:skill-creator, superpowers:writing-skills,
plugin-dev:skill-development).

| # | Prompt | Expected | Got (run 1 / run 2) | Pass |
|---|---|---|---|---|
| 1 | let's make a new skill for converting csv files | dojo | dojo / dojo | ✅ |
| 2 | turn this workflow into a skill | dojo | dojo / dojo | ✅ |
| 3 | test whether my skill actually works | dojo | dojo / dojo | ✅ |
| 4 | why isn't my skill triggering | dojo | dojo / dojo | ✅ |
| 5 | run it through the dojo | dojo | dojo / dojo | ✅ |
| 6 | improve this skill's description | dojo | dojo / dojo | ✅ |
| 7 | harden this SKILL.md | dojo | dojo / dojo | ✅ |
| 8 | write an implementation plan for this feature | superpowers:writing-plans | writing-plans / writing-plans | ✅ |
| 9 | create an agent that reviews code | plugin-dev:agent-creator | agent-creator / agent-creator | ✅ |
| 10 | set up a new plugin with hooks | plugin-dev:create-plugin (any plugin-dev:* accepted, declared) | create-plugin / create-plugin | ✅ |
| 11 | review this skill I wrote | skill-reviewer or dojo (declared ambiguous) | skill-reviewer / skill-reviewer | ✅ |
| 12 | make me a slash command | plugin-dev:command-development | command-development / command-development | ✅ |

Score: 12/12, both runs in full agreement · Collisions: none

Notes: dojo beat skill-creator and superpowers:writing-skills on every
generic skill-creation phrasing — the pushy trigger-phrase list carries
the routing. Description list was complete for the competitive
neighborhood (skill/plugin/process tooling, limitless pack, research
skills); bulk document skills (docx/pptx/xlsx/pdf) were omitted as
non-adjacent noise — re-run with the full list if a collision is ever
suspected there.

## Known limitations

- Dojo coexists with skill-creator (installed twice: user-level +
  official plugin) and superpowers:writing-skills. Routing favors dojo,
  but the redundant copies still cost context and could win on phrasings
  not in the matrix. Recommendation: remove the user-level skill-creator
  copy or disable the plugin duplicate.
- The trigger matrix tests routing judgment in a clean-room prompt, not
  live harness skill selection; live behavior can drift with conversation
  context.
- Dojo's process discipline (kata order, bounded edits) has not itself
  been adversarially pressure-tested — it is technique tier, and its
  walkthrough test is the hivemind dogfood run.
