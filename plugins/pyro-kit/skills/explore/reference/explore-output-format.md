# Explore Output Format

`.pyro/explore.md` is the state handoff file between /explore and /narrow (Phase 3). It is written by `/explore` and read by `/narrow`.

## Full Schema

```markdown
---
idea: "One-line crystallized idea (copied from spark.md)"
explored: YYYY-MM-DD
directions_count: 4
leaning: ""
contrasts_performed: []
iterations: 0
---

## Direction A: [Name]
**Scenario:** [1 paragraph]
**Sketch:** [inline sketch]
**Key Bet:** [one assumption]

## Direction B: [Name]
**Scenario:** [1 paragraph]
**Sketch:** [inline sketch]
**Key Bet:** [one assumption]

## Direction C: [Name]
**Scenario:** [1 paragraph]
**Sketch:** [inline sketch]
**Key Bet:** [one assumption]

## Direction D: [Name]
**Scenario:** [1 paragraph]
**Sketch:** [inline sketch]
**Key Bet:** [one assumption]

## Reactions
[Developer reactions logged during session, date-prefixed]

## Contrasts
[Side-by-side tradeoff tables from contrast(A, B) calls]

## Leaning
[Developer's current preference and reasoning]
```

## Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer |
|-------|------|----------|---------|----------|----------|
| `idea` | String | Yes | N/A | `/explore` (copied from spark.md) | `/narrow` |
| `explored` | Date (YYYY-MM-DD) | Yes | N/A | `/explore` (date of first exploration) | `/narrow` |
| `directions_count` | Number | Yes | `4` | `/explore` (number of directions generated) | `/narrow` |
| `leaning` | String or Array | Yes | `""` (empty) | `/explore` (developer's preferred direction(s)) | `/narrow` |
| `contrasts_performed` | Array of strings | Yes | `[]` (empty) | `/explore` (pairs compared, e.g., "A-C") | `/narrow` |
| `iterations` | Number | Yes | `0` | `/explore` (reaction cycle count) | Diagnostic |

## What /narrow Reads

`/narrow` reads:
- `leaning` -- which direction the developer chose (the convergence target)
- `directions_count` -- how many alternatives were considered
- `contrasts_performed` -- which tradeoffs were explicitly evaluated
- Direction body content -- the scenario, sketch, and key bet of the leaning direction
- `## Reactions` -- developer's expressed preferences and concerns
- `## Leaning` -- the reasoning behind the final choice

## Update Rules

- **Append-only reactions:** New reactions append to the ## Reactions section, never overwrite.
- **Contrasts accumulate:** Each contrast(A, B) call appends a table to ## Contrasts and adds the pair to `contrasts_performed`.
- **Leaning overwrites:** The `leaning` field and ## Leaning section update in place when the developer changes their preference.
- **Iterations increment:** Each react/iterate cycle increments `iterations`.
- **Directions may be replaced:** On iterate(), directions can be regenerated. The latest set is what's in the file.
