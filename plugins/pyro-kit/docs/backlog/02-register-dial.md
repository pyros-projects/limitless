# Register Dial: Creative Latitude Control

**Status:** Proposed
**Priority:** High
**Affects:** /spark, /explore, /scout, /remix, excavator agent
**Inspired by:** GSD's research modes (ecosystem/feasibility/implementation/comparison), researchfun's FUN vs CORE switch

---

## Problem

Pyro Kit has no way to control the creative latitude of its skills. You can't say "I want serious enterprise SaaS ideas" vs "give me weird hackable toys." Every skill operates at a single unnamed register -- roughly "creative solo dev project."

This matters because:
- Sometimes you want to build something serious and need grounded, focused exploration
- Sometimes you want to explore the edges and need wild, divergent, novelty-maximizing output
- The same person wants different registers at different times, or even within the same session
- /spark generating "weird art project" thumbnails when you want "production CLI tool" is a waste of iteration

## Proposal

Add a **register** parameter that shapes creative latitude across all generative skills.

### The Four Registers

```yaml
# In .pyro/config.yaml or passed as --register argument
register: serious | balanced | wild | unhinged
```

| Register | What it means | Tone |
|---|---|---|
| **serious** | Business-focused, grounded, practical | Professional engineer solving a real problem |
| **balanced** | Mix of practical and creative (default) | Senior dev with taste, exploring options |
| **wild** | Cross-domain mashups, unexpected vehicles, novel interactions | Creative technologist chasing fascinations |
| **unhinged** | Pure novelty optimization, 10/10 mind-melter standard | Demoscene hacker on a weekend bender |

### How Each Skill Adapts

| Skill | serious | balanced | wild | unhinged |
|---|---|---|---|---|
| /spark | Revenue-oriented thumbnails. User pain points. Market gaps. | Mix of practical and creative | Cross-domain mashups. "What if X met Y." | Pure novelty. FUN rubric scoring. |
| /explore | Engineering tradeoffs. Scalability. Maintenance burden. | Mix of conventional and unconventional | Non-obvious analogies. Game design lenses. | Deliberately absurd directions included |
| /scout | Tier-1 sources. Prior art. Market analysis. | Broad search. Community + official docs. | GitHub 20-200 stars. Qiita/Zenn. Weird papers. | Full researchfun protocol. Non-English. Demoscene. |
| /remix | Industry case studies. Proven patterns. | Standard creative domain lenses | Obscure domain lenses (fermentation, cartography, improv) | Lenses from completely unrelated fields |

### Interface

```
/spark --register wild
/explore --register serious
/scout --register unhinged "memory systems for agents"
```

Or set project-wide default:
```yaml
# .pyro/config.yaml
register: balanced   # default for all skills
```

Per-invocation override always wins over project default.

### Implementation

Each skill reads the register at startup:

```
SET register = $ARGUMENTS.extract("--register") OR .pyro/config.yaml.register OR "balanced"
```

The register modifies the skill's prompt behavior -- it's a prompt-engineering parameter, not a structural change. Each skill's persona section gets a register-conditional:

```
IF register == "serious":
  "Focus on practical, production-grade ideas. Prioritize feasibility, maintainability, and clear user value."
ELSE IF register == "wild":
  "Push into unexpected territory. Cross-pollinate domains. Propose things that sound wrong at first but might be brilliant."
...
```

## Interaction with Project Type

Register controls creative *latitude*. A separate `--type` parameter (see 05-project-type.md) controls the *vehicle*:

```
/spark --type cli --register wild     # wild ideas, but they're all CLIs
/spark --type saas --register serious  # serious SaaS ideas
/spark --register unhinged             # no vehicle constraint, maximum weirdness
```

## Effort Estimate

Low. Configuration parameter + prompt modifiers in each affected skill. No new files, no new skills, no structural changes.

## Open Questions

- Should the register be logged in decisions.md? (Probably yes -- "chose register: wild for this project" is a decision about creative intent)
- Should /pulse suggest changing the register? ("You've been in serious mode for 3 weeks and momentum is dropping -- want to try wild mode to inject novelty?")
- Should the fascination index track which registers produce shipped projects vs abandoned ones?
