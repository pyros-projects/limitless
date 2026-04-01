# Project Type Parameter

**Status:** Proposed
**Priority:** Medium
**Affects:** /spark, /explore, /surface, /scope
**Inspired by:** BMAD's analysis-phase agent routing by project type, SFD whitepaper Appendix C surface type examples

---

## Problem

Pyro Kit skills can't distinguish between building a CLI tool, a SaaS app, a library, or a game. This means:
- /spark generates thumbnails across all vehicle types when you know you want a CLI
- /explore proposes directions including "what if it were a web app" when you've already decided it's a library
- /surface detects surface type via keyword heuristics (lines 165-177) but only after exploration

Sometimes you know the vehicle before you know the idea. "I want to build a CLI tool that does... something" is a valid starting point.

## Proposal

Add an optional `--type` parameter that constrains the vehicle across all generative skills.

### Available Types

```
cli      -- Command-line tool
web      -- Web application (SPA, dashboard, landing page)
api      -- Library or API (consumed by other developers)
service  -- Backend service, pipeline, or system
agent    -- AI agent, automation, or LLM-powered tool
game     -- Game or interactive experience
plugin   -- Extension for an existing platform (Claude Code, VS Code, etc.)
```

### Interface

```
/spark --type cli "something about git archaeology"
/explore --type api
/surface                  # inherits type from explore.md if set
```

Or set in project config:
```yaml
# .pyro/config.yaml
project_type: cli
```

### How Skills Adapt

| Skill | With --type set | Without --type |
|---|---|---|
| /spark | All thumbnails are constrained to the specified vehicle | Thumbnails may propose any vehicle |
| /explore | All directions use the same vehicle, diverge on other axes | Directions may diverge on vehicle type |
| /surface | Skips surface type detection, uses specified type | Detects via keyword heuristics (current behavior) |
| /scope | Soul statement contextualized to vehicle constraints | Generic soul statement |

### Interaction with Register

`--type` controls the vehicle. `--register` controls creative latitude. They're orthogonal:

```
/spark --type cli --register wild     # Wild CLI ideas
/spark --type saas --register serious  # Serious SaaS ideas  
/spark --register unhinged             # No vehicle constraint, maximum weirdness
```

### State Persistence

When set, project_type is stored in `.pyro/state.md` frontmatter and inherited by downstream skills unless overridden.

## Effort Estimate

Low. Argument parsing + prompt conditioning. No structural changes.

## Open Questions

- Should /explore be allowed to suggest a different vehicle type if the idea clearly wants it? ("Your spark is about visual data -- CLI might not be the best vehicle. Want to explore GUI directions too?")
- Should the type list be extensible? (User could add "tui", "mobile", "discord-bot")
