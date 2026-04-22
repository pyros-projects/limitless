# Flow Example: Flock Agent Skills (the session we just lived)

Shows how the revised SFD skill would handle the Flock agent-skills project we just completed. The key add: Phase 2.5 Feasibility Probe catches the `SkillsContextProvider` design error *before* we write contracts, not two hours later during `ce:plan` research.

## Context recap

Real sequence from this session:
1. `ce:ideate` picked the selected path (#5 + #7 + #2)
2. SFD built surface prototype — 4 scenarios + WALKTHROUGH.md
3. Andre approved surface (Gate 1 converged)
4. I wrote `.sfd/contracts.md` — designed `SkillsContextProvider` as primary integration seam
5. Andre approved contracts after manual review
6. `ce:plan` Phase 1 research dispatched → found `SkillsContextProvider` can't work (ContextProvider returns artifacts only, not tools/signatures). Plus: `.with_skills` belongs on `AgentBuilder` not `FlockAgent`. Plus: `changelog.query(skill_name=...)` is fiction.
7. Plan document had to include a "Corrections to Origin Contracts" section superseding the approved contracts.

**The cost:** one round of wrong contracts that had to be rewritten. Not landfill, but friction.

## How revised SFD handles it

Phases 0.5 and 1 are fine in the original flow (target was unambiguous; surface is clearly "API/library").

Let's pick up at Phase 2.5 — **the new addition.**

---

### [Phase 3 convergence — same as original, ends with Andre approving the surface]

**Assistant:**
> Surface converged. Moving to contract derivation. **OK? Y / N**

**Andre:** `Y`

### [Phase 2.5 — Feasibility Probe]

This is the new gate. Rule: default-ON for API / library / agent surfaces. Agent-skills is an API/library surface, so it fires.

**Assistant:**
> About to derive contracts. Quick feasibility check: I'll read the specific files the surface assumes (~2 min — just reading and checking).
>
> **A.** Run (recommended — surface touches engine internals)
> **B.** Skip (I'm confident in the shape)

**Andre:** `A`

*[skill lists the surface assumptions to check: (1) `ContextProvider` interface — does `get_artifacts` really allow tool injection? (2) `with_skills` return type — where do fluent methods like `with_tools` actually live? (3) `changelog.query(skill_name=...)` — does this API shape exist?]*

*[skill uses its own Read/Grep tools, ~2 min]*

*[Read `src/flock/core/context_provider.py`, `src/flock/core/agent.py`, `src/flock/models/changelog.py`. Each assumption checked against actual code.]*

**Assistant:**
> Probe found **3 assumption violations**:
>
> 1. **`SkillsContextProvider` as integration seam.** `BaseContextProvider.get_artifacts` returns `list[Artifact]` only — can't inject tools or mutate signatures. The surface's "inject 3 tools via context provider" path doesn't work.
> 2. **`.with_skills` target.** Fluent methods like `.with_tools`, `.with_mcps`, `.with_context` live on `AgentBuilder`, not `FlockAgent`. Return type should be `AgentBuilder`, not `Self`.
> 3. **Changelog API.** `changelog.query(skill_name=..., since=...)` in the surface is fiction. Real API is `query_changelog(after_seq, limit, filters=ChangelogFilter(produced_by=[...]))` — no skill-name field. Optimizer trainset reconstruction has to correlate artifact pairs from agents that attach the skill.
>
> Options:
>
> **A.** Fix contracts now (recommended) — I'll rewrite the integration plan using three seams instead of one: config-time `AgentBuilder.with_skills` mutates `agent.tools` + `agent.description`; per-invocation `SkillsComponent` attaches demos; signature instructions flow through existing `signature_builder` path. Changelog trainset is best-effort from artifact pairs.
> **B.** Accept limitations — document the design holes in contracts and proceed; plan will have to rework them anyway.
> **C.** Re-open Phase 3 — one of the surface's flows might be wrong, not just the implementation detail.

**Andre:** `A`

*[contracts now get written with the CORRECT integration model from the start — no "Corrections to Origin Contracts" section needed in the plan]*

---

### [Phase 4 — contracts derived, now internally consistent]

**Assistant:**
> Contracts derived and aligned with the codebase reality:
>
> - `AgentBuilder.with_skills(*sources, runtime=False, token_budget=8000) -> AgentBuilder`
> - `SkillsComponent(AgentComponent)` per-invocation demo attachment
> - Signature instructions via `agent.description` merge (existing path)
> - Optimizer trainset via `query_changelog(filters=ChangelogFilter(produced_by=[...]))` artifact-pair reconstruction
>
> Plus: frontmatter schema, discovery algorithm, script runners, error taxonomy.
>
> **A.** Looks complete — proceed to planning.
> **B.** One thing missing: [freeform hint].
> **C.** Re-open Phase 3.

**Andre:** `A`

*(Contracts frozen. Gate 2 closed. Plan can proceed against a clean foundation.)*

---

## The contrast

| | Original session | Revised SFD |
|---|---|---|
| Feasibility check | None between Gate 1 and Gate 2 | Phase 2.5 fires default-ON for API/library |
| Wrong contracts written | Yes — SkillsContextProvider, wrong `with_skills` return, fictional changelog API | Caught by probe in 2 min |
| Who caught the errors | `ce:plan` Phase 1 research (2 hours later) | SFD Phase 2.5 probe (2 min later) |
| Plan document | Needed "Corrections to Origin Contracts" section | Plan builds on correct contracts from start |
| User effort to action findings | Had to re-read contracts + reason through corrections | Three multiple-choice answers (`Run` / `A`) |
| Mechanism | N/A in original; `ce:plan` dispatched research agent | SFD skill itself reads files inline — no agent handoff, no external dispatcher. Fully standalone. |
| Total friction | Medium — plan was long, contracts had to be mentally patched | Low — caught early, contracts correct once |

## Design principle this demonstrates

**The feasibility probe isn't a "nice-to-have" gate. It's a cheaper version of work that was happening anyway.** `ce:plan`'s Phase 1 research did the same work — just 2 hours later, after contracts were frozen and started rotting.

Running the probe at Phase 2.5 is strictly cheaper than catching it at `ce:plan`:
- Same assumption-checking
- Same target files
- Faster (2 min inline vs ~5 min with agent handoff)
- Standalone — doesn't depend on a research-agent ecosystem being installed
- Contracts don't have to be rewritten, plan doesn't need a corrections section

For GUI/CLI surfaces where the surface ≈ architecture, the probe is default-OFF because there's nothing to probe. For API/library/agent surfaces where the surface *implies* internal architecture, default-ON catches the exact class of error we just lived through.

## Keystrokes the user typed in the feasibility gate

```
A Y A
```

Three responses. No freeform prose. System did the research and translated findings into a next-action choice.
