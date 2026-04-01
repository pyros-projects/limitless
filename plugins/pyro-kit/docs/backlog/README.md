# Pyro Kit -- Improvement Backlog

Structured improvement proposals for Pyro Kit. Each spec is self-contained with problem statement, proposal, effort estimate, prior art references, and open questions.

For the original unstructured backlog, see `docs/backlog.md`.

---

## Specs

| # | Title | Priority | Effort | Key Insight |
|---|---|---|---|---|
| 01 | [Decision Log](01-decision-log.md) | High | Low-Med | Decisions are vectors to explore, not just state to persist. Capture on every iterate(), not just convergence. |
| 02 | [Register Dial](02-register-dial.md) | High | Low | Control creative latitude (serious/balanced/wild/unhinged) across all generative skills. |
| 03 | [/scout Skill](03-scout-skill.md) | High | Med-High | Bounded web research with parallel search angles. Findings as proposals, not URLs. |
| 04 | [Prior Art in /explore](04-prior-art-explore.md) | High | Medium | Auto-scout before direction generation. Landscape disclosure per direction. Design space coverage check. |
| 05 | [Project Type](05-project-type.md) | Medium | Low | Constrain vehicle type (cli/web/api/agent/etc.) orthogonal to register. |
| 06 | [Scope Guardrails](06-scope-guardrails.md) | Medium | Low | Catch capability creep in real-time during /explore and /surface. Stolen from GSD. |
| 07 | [Explore Without Artifacts](07-explore-without-artifacts.md) | Medium | Low-Med | Delay persistence until /narrow. Make exploration cheap and disposable. Stolen from OpenSpec. |
| 08 | [Pattern Index](08-pattern-index.md) | Medium | Medium | Cross-project technical learnings. Companion to fascination index. Stolen from Compound Engineering. |
| 09 | [Anti-Clustering](09-anti-clustering.md) | Medium | Low | Verify direction divergence with coverage self-check. Stolen from BMAD + iDesignGPT. |
| 10 | [Session Context](10-session-context.md) | Medium | Medium | Boot packet at session start. Hash-cached, token-budgeted. Stolen from Codie's Memory + GSD. |
| 11 | [Final Novel Ideation](11-novel-ideation-phase.md) | High | Medium | 10 fresh concepts from non-software creative domains + AI frontier gaps. |
| 12 | [Lineage Visualization Command](12-lineage-visualization-command.md) | High | Medium | Generate interactive project lineage from Pyro state and decisions. |

## Dependency Graph

```
02-register-dial -----> 03-scout-skill -----> 04-prior-art-explore
                              |
01-decision-log               |
(independent)                 |
                        05-project-type
                        (independent)

06-scope-guardrails
(independent)

07-explore-without-artifacts
(independent)

08-pattern-index
(independent, pairs with fascination index)

09-anti-clustering -----> 04-prior-art-explore
(can be done independently but pairs well)

10-session-context
(independent, uses decision-log if available)
```

## Recommended Implementation Order

1. **01-decision-log** -- foundational, enables everything else to capture decisions properly
2. **02-register-dial** -- low effort, high impact, unblocks /scout
3. **09-anti-clustering** -- low effort, immediate quality improvement to /explore
4. **06-scope-guardrails** -- low effort, addresses the core abandonment problem
5. **07-explore-without-artifacts** -- low effort, makes exploration cheaper
6. **05-project-type** -- low effort, quality-of-life improvement
7. **03-scout-skill** -- medium effort, requires web search tooling
8. **04-prior-art-explore** -- depends on /scout
9. **08-pattern-index** -- medium effort, value grows over multiple projects
10. **10-session-context** -- medium effort, integrates multiple data sources
11. **11-novel-ideation-phase** -- ideation pack for next-wave strategic bets
12. **12-lineage-visualization-command** -- high-value introspection and re-entry UX

## Research Sources

These specs were informed by deep analysis of:
- **GSD** (Get Sh*t Done): Phase architecture, research agents, discuss/plan/execute separation, scope guardrails
- **BMAD** (Build Measure Analyze Design): Agent roster, party mode, anti-bias protocol, step-file overhead lessons
- **OpenSpec**: Artifact dependency chains, explore-without-artifacts pattern
- **Superpowers**: Brainstorm -> plan -> TDD chain, spec review loop, fresh-context-per-subagent
- **Compound Engineering**: Parallel research agents, compounding knowledge, YAGNI principles
- **Codie's Memory**: Boot packet, promotion pipeline, layered stability model
- **Agent Patterns**: Bounded research pipeline with budget caps and provenance
- **iDesignGPT** (Nature): Design space coverage, diversity, and novelty metrics
- **Schemex** (arXiv): Schema induction from scattered examples
- **Athena**: Hash-based boot packet caching with delta detection
