# /scout -- Bounded Web Research Skill

**Status:** Proposed (extends existing backlog items #1 and #3)
**Priority:** High
**Affects:** /spark, /explore, /pulse, fascination index
**Inspired by:** GSD's gsd-phase-researcher, Agent Patterns bounded pipeline, researchfun FUN protocol, Compound Engineering parallel research agents

---

## Problem

Pyro Kit operates entirely from the agent's internal knowledge. No skill can search the web. This means:
- /spark generates thumbnails without knowing what already exists
- /explore proposes directions without checking prior art
- The fascination index never discovers new fascinations from the outside world
- Design space exploration is blind to the current landscape

The existing backlog items (#1 Explorative Web Excavation, #3 Web Scout Skill) capture the vision. This spec adds architectural specifics stolen from production frameworks.

## Proposal

A first-class `/scout` skill that performs bounded, surgical web research and presents findings as proposals (thumbnails, not URLs).

### Architecture: Bounded Pipeline

Stolen from Agent Patterns + GSD:

```
Query Formation -> Parallel Search -> Dedupe -> Read -> Extract -> Verify -> Propose
```

**Budget caps** (configurable):
- Max 10 URLs per search angle
- Max 90 seconds per search angle
- Max 3-5 parallel search angles
- Provenance required: url + quote + confidence level

**Fresh subagent** (stolen from GSD):
Research runs in a spawned subagent with fresh context. Main session stays lean. Researcher produces structured output consumed by the calling skill.

### Search Angles (Parallel)

Each scout invocation fires 3-5 parallel searches with different angles:

| Angle | What it finds | Example query |
|---|---|---|
| Prior art | Existing tools solving the same problem | "CLI tool for [X]" on GitHub |
| Adjacent domain | Solutions from other fields | "[core concept] in game design / music / architecture" |
| Wild inspiration | Weird repos, obscure papers | GitHub 20-200 stars, arXiv, Qiita |
| Failure archaeology | Abandoned attempts at similar ideas | "[concept] deprecated / abandoned / post-mortem" |
| Technical feasibility | Whether the core mechanism works | Library docs, implementation examples |

Angles are selected based on the register dial:
- **serious**: prior art + technical feasibility + adjacent domain
- **balanced**: all five angles
- **wild**: adjacent domain + wild inspiration + failure archaeology
- **unhinged**: wild inspiration x3 + adjacent domain + failure archaeology

### Output Format: Proposals, Not Results

Scout output matches /spark's thumbnail format so findings feed naturally into the lifecycle:

```markdown
## Scout Report: [query]
**Register:** wild | **Angles:** 4 | **Sources:** 23 | **Duration:** 78s

### Finding 1: [Title]
[One vivid paragraph: what this is, why it's relevant, what it changes about the design space]
Source: [url] | Confidence: high
Prior art delta: [how your idea differs from this]

### Finding 2: [Title]
...

### Prior Art Alert
[thing] is 70% of what you're building. Specific delta: [what yours does differently].

### Wild Card
[Something from an adjacent domain that might reshape the approach entirely]

### Landscape Summary
- **Crowded areas:** [what's well-served]
- **Open gaps:** [what nobody's built]
- **Your unique angle:** [what the findings suggest your differentiation is]
```

### Integration Points

| Calling skill | How it uses /scout | When |
|---|---|---|
| /spark | Seeds thumbnail generation with web findings | Optional, on `--scout` flag or when register is wild/unhinged |
| /explore | Prior art sweep before direction generation | Optional auto-scout (see 04-prior-art-explore.md) |
| /pulse | Find "new shiny things" the developer might be distracted by | When detecting new-repo-creation as abandonment signal |
| /fascination | Discover new fascinations from web trends | On explicit invocation |

### State Persistence

Scout reports saved to `.pyro/scout/` with timestamps:
```
.pyro/scout/
  2026-03-14-memory-systems.md
  2026-03-15-cli-archaeology.md
```

Findings that get used by /spark or /explore are automatically cross-referenced in decisions.md.

### Register Integration

The register dial (see 02-register-dial.md) controls:
- Which search angles are activated
- Source filtering (tier-1 only vs everything)
- The FUN scoring rubric threshold for "interesting enough to report"
- Whether non-English sources are included

## Effort Estimate

Medium-High. New skill + subagent architecture + web search tooling integration. Requires available web search tools (SearXNG, Brave API, or similar).

## Dependencies

- Web search capability (MCP tool or script)
- Register dial (02-register-dial.md) for wildness control
- Subagent spawning for fresh context

## Prior Art

- **GSD gsd-phase-researcher**: Multi-source research (Context7 HIGH -> WebFetch MED -> WebSearch LOW) in fresh subagent with 200k context
- **Agent Patterns research-agent**: Bounded pipeline with budget caps, dedup, policy check, provenance tracking
- **Compound Engineering**: Parallel research subagents (repo-research-analyst + learnings-researcher)
- **researchfun**: FUN scoring rubric, falsification protocol, 10/10 mind-melter standard
