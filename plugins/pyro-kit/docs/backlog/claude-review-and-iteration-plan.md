# Claude's Backlog Review & Next Iteration Plan

Date: 2026-03-30
Reviewer: Claude
Context: First deep read of pyro-kit. Fresh eyes on everything.

---

## Backlog Review: What's Good, What's Not, What's Missing

### Tier 1: Build These (high value, clear path)

**#01 Decision Log** — Yes, obviously. This is load-bearing infrastructure. Every other feature that reasons about "why did we choose X" needs this. The append-only format is correct — decisions are a log, not a document. One concern: the open question about append-only vs editable is already answered by the design. Decisions don't change. New decisions supersede old ones. Append-only. Ship it.

**#02 Register Dial** — Yes. Low effort, high leverage. The four registers (serious/balanced/wild/unhinged) are the right granularity. One addition: the register should be persisted in `.pyro/config.yaml` as a project default, not just a per-invocation flag. A CLI project probably wants `serious` as its default, and the user shouldn't have to type `--register serious` every time.

**#06 Scope Guardrails** — Yes. This directly addresses the 60-70% abandonment problem. The GSD heuristic ("clarify behavior or add capability?") is the right test. The someday.md dump is elegant — it acknowledges the idea has value without letting it derail the current scope. Low effort, high return.

**#09 Anti-Clustering** — Yes. The cheapest quality improvement in the backlog. Self-check after direction generation, regenerate if clustered. Pure prompt engineering, no infrastructure. Do it early.

**#07 Explore Without Artifacts** — Yes. Makes exploration genuinely cheap. Right now writing explore.md creates commitment pressure — "I already wrote it down, so I should commit to it." Delaying persistence until /narrow is the correct move. The `save` escape hatch for multi-session work is necessary.

### Tier 2: Build These Eventually (good ideas, lower urgency or higher cost)

**#03 Scout Skill** — Good idea, and the effort is lower than I initially thought. The infra already exists — Pyro has research skills (`codies-research-skill`, the FUN scout in `.claude_old/commands/a/`) that use host-native web search, `gh` CLI, and subagent dispatch. /scout is just a Markdown skill wrapping the same pattern: bounded search, parallel angles, findings formatted as proposals. The bounded pipeline design (3-5 parallel searches, 60-90s, proposals not URLs) is the right shape and proven in existing skills. Could move to v0.2.0 if time allows.

**#04 Prior Art in /explore** — Good but depends on #03. The landscape disclosure per direction is the real value ("3 existing tools do this, your delta is..."). Without /scout, this would just be hallucinated prior art, which is worse than no prior art.

**#10 Session Context / Boot Packet** — Good design, directly inspired by codies-memory. The ~360 token budget and hash-based caching are right. One note: this overlaps with what codies-memory will eventually provide. If pyro-kit uses codies-memory's boot system, #10 becomes "ensure pyro state files are included in the boot assembly" rather than building a separate boot system. Worth considering whether this should be a pyro-kit feature or a codies-memory integration.

**#08 Pattern Index** — Good long-term investment. The fascination index is "what interests you," patterns are "what you've learned." Both compound. But patterns need multiple projects to prove value, and pyro-kit itself is the first real test subject. I'd ship fascination composting thoroughly before adding the pattern companion.

**#12 Lineage Visualization** — Cool, but medium effort for a feature that's primarily retrospective. The value is real (seeing your project journey visually is powerful for re-entry and learning), but it doesn't help you build the current project faster. Defer until the core loop is fully hardened.

### Tier 3: Reconsider (not convinced yet)

**#05 Project Type** — I'm lukewarm. The register dial already constrains creative latitude. Adding a vehicle type (`--type cli`) feels like premature constraint — the best ideas sometimes surprise you about what vehicle they want. "/spark --type cli" means you've already decided the most important design question before the tool even runs. If someone knows they want a CLI, they probably don't need /spark to tell them what to build. The register dial is sufficient for constraining the space.

**#11 Novel Ideation Phase** — This is 10 ideas, not one feature. Some are excellent (Project Pillars, Negative Results Notebook, Idea/Ship toggle). Some are speculative (Project Genetics, Pattern-Based Affective Detection). Bundling them as one backlog item hides that they're actually 10 independent proposals with wildly different effort/value ratios. I'd break this apart: promote the top 3 to their own backlog items, park the rest.

From #11, my picks for promotion:
- **Project Pillars** — Hard constraints that prevent drift. "This project is LOCAL-FIRST and SINGLE-USER. Every decision must pass these two tests." This is the architectural equivalent of scope guardrails. Low effort, high value.
- **Negative Results Notebook** — Frame failures as data, not waste. Pairs naturally with fascination composting. "SQLite-based caching didn't work because X" is a pattern that should persist.
- **Idea/Ship Toggle** — Separate divergent thinking from convergent execution. When you're in Idea View, everything is possible. When you're in Ship View, only what's scoped exists. Mental mode switching is real and underserved.

---

## What's Missing From The Backlog

### Missing: `/contract` Skill (Phase 3)

The SFD methodology has 6 phases. The MVP covers phases 0-1 and 5-6. Phase 2 (/surface) exists but Phase 3 (/contract — derive API contracts, domain invariants, NFRs from converged surface) is listed as "planned" with no backlog item. This is a gap. Contracts are where SFD's "specifications are outputs, not inputs" thesis gets proven. Without /contract, the methodology stops at "we have a prototype that feels right" and never reaches "here are the buildable specs that the prototype implies."

**Recommendation:** Add a backlog item for /contract. It should read the converged surface.md, extract contracts citing specific surface behaviors, and produce contract.md with versioned API/domain/NFR sections.

### Missing: `/narrow` Skill Spec

/explore generates directions, /narrow is supposed to synthesize reactions into a locked direction. /narrow is referenced by #07 (explore without artifacts) but has no dedicated spec or backlog item. It's the convergence moment for Phase 1 — the point where exploration becomes commitment. This deserves its own skill definition.

### Missing: Feedback Loop From /build Back to /surface

The SFD whitepaper describes vertical slices (Phase 5) that make surface flows real one at a time. But there's no mechanism for what happens when building a slice reveals that the surface was wrong. In practice, building always reveals surface problems. There should be a feedback path: /build discovers a surface assumption was wrong → surface.md gets updated (not silently overridden) → the decision log captures why. Without this, surface.md becomes a historical artifact that diverges from reality, which is exactly what specs-first development suffers from.

### Missing: Multi-project Portfolio View

/pulse checks momentum for one project. But solo developers typically have 3-5 projects in various states. A portfolio-level view ("which of my projects needs attention? which should I shelve? where am I spread too thin?") would be the natural extension of the anti-abandonment thesis. The project registry exists. The fascination index exists. A `/portfolio` or `/pulse --all` that reads across all registered projects would surface: "You have 4 active projects, 2 are stalled, 1 is in novelty depletion. Recommendation: shelve X, focus on Y."

This connects to #11's Energy Budget Router idea, but it's more concrete and more immediately useful.

---

## Next Iteration Plan: v0.2.0

### Theme: Harden the Core Loop

v0.1.0 proved the core skills work. v0.2.0 should make them robust, persistent, and quality-assured. No new phases. Just make the existing phases work better.

### Scope: 6 Items

```
v0.2.0 Iteration Plan
======================

1. Decision Log (#01)             — foundational, enables everything
2. Register Dial (#02)            — low effort, immediate quality control
3. Anti-Clustering (#09)          — low effort, /explore quality improvement
4. Scope Guardrails (#06)         — low effort, addresses core abandonment problem
5. Explore Without Artifacts (#07) — makes exploration cheap
6. Project Pillars (from #11)     — hard constraints that prevent drift

Total estimated effort: Low to Medium
Expected: 1-2 focused sessions
```

### Why These 6

- **#01** is infrastructure. Everything downstream needs it.
- **#02** is a knob that makes every generative skill better.
- **#09** is a quality gate that costs nothing to add.
- **#06** catches scope creep before it kills projects.
- **#07** removes the commitment pressure from exploration.
- **Pillars** (extracted from #11) give projects hard identity constraints. "This is LOCAL-FIRST and SINGLE-USER" prevents architectural drift the same way scope guardrails prevent feature drift.

### Why NOT These Others

- **#03 (Scout)** — Lower effort than I initially estimated (existing research skills prove the pattern). Still deferred to v0.3.0 for scope, but could be pulled into v0.2.0 if the core 6 ship fast.
- **#04 (Prior Art)** — Depends on #03.
- **#05 (Project Type)** — Not convinced it's needed beyond register dial.
- **#08 (Pattern Index)** — Needs multiple projects to prove value.
- **#10 (Session Context)** — May be subsumed by codies-memory integration.
- **#11 (Novel Ideation)** — Break apart first. Pillars promoted, rest parked.
- **#12 (Lineage)** — Retrospective, not core loop.

### Build Order

```
1. #01 Decision Log
   - Add decisions.md schema
   - Add append logic to /spark, /explore, /surface, /pulse
   - Test: decisions persist across session crash

2. #02 Register Dial
   - Add --register flag to generative skills
   - Persist default in .pyro/config.yaml
   - Test: --register wild produces noticeably different /spark output

3. #09 Anti-Clustering
   - Add coverage self-check after direction generation in /explore
   - Regenerate weakest direction if clustered
   - Test: /explore with anti-clustering produces more diverse directions

4. #06 Scope Guardrails
   - Add scope check heuristic to /explore and /surface
   - Create someday.md for deferred capabilities
   - Test: new capability suggestion triggers guardrail

5. #07 Explore Without Artifacts
   - Refactor /explore to stay conversational
   - Add /narrow as the persistence trigger
   - Add save/resume for multi-session exploration
   - Test: /explore alone produces no .pyro/ files

6. Project Pillars (from #11)
   - Add pillars to .pyro/state.md (set during /spark or /explore)
   - Skills check proposals against pillars
   - Test: proposal violating a pillar triggers warning
```

### v0.3.0 Preview (After v0.2.0)

```
v0.3.0: External Intelligence
- /scout skill (#03)
- Prior art in /explore (#04)
- /contract skill (new — Phase 3)
- /narrow skill spec (new)
- Build→Surface feedback loop (new)
```

### v0.4.0 Preview

```
v0.4.0: Portfolio & Memory
- Pattern Index (#08)
- Session Context (#10) or codies-memory integration
- Portfolio view (new)
- Negative Results Notebook (from #11)
```
