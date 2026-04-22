# SFD Improvement Backlog — Cover Page

**Created:** 2026-04-17
**Methodology:** Surface-First Development, applied to SFD itself (meta)
**Context:** Andre asked me to improve the `limitless:surface-first-development` skill based on gaps surfaced during the Flock agent-skills session (contracts-level architectural errors caught late) and a prior session (a "Google Stitch" prompt that led to 20 minutes of wrong prototyping because the target wasn't verified).

## The Northstar

> In some future it should be in theory possible to reach an amazing piece of software by just saying "yes" (or no) to everything the bot writes.

Not a hard requirement. But the operational rule *is* hard:

**No required long-form prose input, ever.** Every decision point is multiple choice + recommendation + optional freeform escape. The critique phase especially — never "tell me what's wrong." Instead, a guided ladder: coarse judgment → narrow choice → action. The system carries expertise; the user carries judgment.

## What's in this directory

| File | What it is | Read first? |
|---|---|---|
| `WALKTHROUGH.md` | This cover page. | Yes |
| `sfd_improvement_ideas.md` | Ranked backlog: 9 improvements ranging from critical (target verification, feedback cadence) to nice-to-have (merged state files, progress visuals). Each has problem, proposed fix, cost, impact. | Yes (next) |
| `skill_revised_preview.md` | The proposed new SKILL.md — standalone, no CE hard dependency, critique-ladder pattern encoded in interaction rules. Think of this as the "prototype" of the improved skill. | Yes (the main artifact) |
| `flow_example_google_stitch.md` | Walkthrough: how the new skill handles the Google Stitch case. Shows Phase 0.5 target verification catching the ambiguity in 30 seconds instead of 20 minutes. | Review to feel the new flow |
| `flow_example_flock_skills.md` | Walkthrough: how the new skill handles the Flock agent-skills session we just lived. Shows Phase 2.5 feasibility probe catching the `SkillsContextProvider` mistake before contracts are written. | Review to feel the new flow |
| `research_notes.md` | What I borrowed from `superpowers:brainstorming` (multiple-choice-with-recommendation rule; visual companion offer pattern) and `ce:brainstorm` (single-question-at-a-time, scope assessment). What's new in SFD-improved. | Optional context |

## Reading order I'd recommend

1. `sfd_improvement_ideas.md` — scan the 9 items to see the scope
2. `skill_revised_preview.md` — read the new SKILL.md end-to-end to feel how it reads
3. One flow example (Google Stitch is shorter) — see the critique ladder in action
4. Open questions at the bottom of this file — decide what to cut/keep/defer

## Key design principles baked into the prototype

1. **No required prose input.** Every question is multiple-choice with recommendation + freeform escape.
2. **Critique ladder replaces "what's wrong?"** — coarse preference → narrow weakness → next action.
3. **Phase 0.5 Target Verification** — before any build, confirm the target interpretation if any proper nouns / domain terms / competitor references are in play. Web search + single confirmation question.
4. **Phase 2.5 Feasibility Probe** — optional, fast, after surface convergence, before contracts. Catches "we can't actually use the scheduler" at the cheapest point.
5. **Short build cycles between checkpoints** — never more than ~60 seconds without a y/n or multiple-choice gate. Parallel subagents announce their premise first so the user can abort.
6. **Standalone** — no hard dependency on CE, OpenSpec, Beads. Integrations are soft: "if these are installed, we can hand off."
7. **Visual companion offer** borrowed from `superpowers:brainstorming` — for GUI work, offer a browser mockup channel as an optional tool.

## Open questions I want Andre to decide

All of these are multiple-choice. No prose required.

**Q1.** Which target dir for the improvement eventually lands in production?
- A. Replace `limitless/skills/surface-first-development/SKILL.md` directly after review
- B. Ship as `surface-first-development-v2` side-by-side and deprecate v1 after dogfood
- **Recommendation: A** — the skill is young enough that clean replacement is cleaner than dual-running

**Q2.** Should Phase 0.5 Target Verification be always-on or skippable?
- A. Always runs — cheap enough (one question) that no skip is needed
- B. Skippable via trigger keyword (user can say "skip verification")
- C. Always runs but collapses to a single-line "I'm reading [X] as [Y]. Correct?" when the target is obvious
- **Recommendation: C** — always runs, but invisible when the target is unambiguous

**Q3.** Should Phase 2.5 Feasibility Probe be default-on or default-off?
- A. Default-on — runs silently and catches errors
- B. Default-off — opt-in via user signal or SFD's own detection of architectural-dependency signals
- C. Default-on for API/library/agent surfaces, default-off for GUI/CLI where surface ≈ architecture
- **Recommendation: C** — matches the actual severity distribution

**Q4.** Critique ladder — should it be mandatory or can the user short-circuit?
- A. Always the critique path
- B. User can always say "converged" and skip the ladder
- C. System uses the ladder by default but auto-converges if the user's answer to the first question ("which prototype is best?") includes enthusiasm signals ("love it", "ship it", "this is great")
- **Recommendation: C** — respects both the discipline and the user's momentum

**Q5.** Visual companion — should SFD inherit it from superpowers:brainstorming or require that plugin?
- A. Require `superpowers` plugin — use its visual companion verbatim
- B. Build a lightweight version into SFD (just "here's an HTML file, open it") with no browser-launcher infra
- C. Skip visual companion entirely; SFD's existing artifacts (click dummies) already cover the GUI case
- **Recommendation: B** — keeps standalone promise; lightweight browser helper is ~20 lines

**Q6.** Should the new Phase 0 (Target Verification) require web search capability?
- A. Yes, hard requirement — if no web search, the phase fails and SFD refuses to proceed with ambiguous targets
- B. Soft — if no web search, fall back to direct confirmation question only ("I'm reading X as Y, correct?")
- C. Soft + warn — proceed with the user's literal phrasing but warn loudly that no verification happened
- **Recommendation: B** — most environments have web search, and the direct-confirmation fallback is still a big improvement over silent guessing

## Status

This is a **surface prototype** of the improved SFD skill. Nothing is wired into limitless/ yet. Review the files, pick a direction on Q1-Q6, and we can converge on the actual skill replacement.

I treated the answers to these questions the same way SFD-improved would treat them: multiple choice + recommendation. You can approve them in one word.
