# SFD Improvement Backlog

Ranked by severity × frequency × cost-of-fix. Each improvement has: problem observed, proposed fix, rough cost, expected impact.

The top three are critical (they turn "wait 20 minutes for the wrong thing" into "verify in 30 seconds"). The middle band is about closing the gate gaps we hit in the Flock session. The bottom band is quality-of-life.

---

## Critical — stop building the wrong thing

### 1. Phase 0.5: Target Verification (pre-build)

**Problem observed.** A user prompt with "local google stitch" led to 20 minutes of image-editing prototypes because the assistant assumed "stitch" = panorama stitching. Google Stitch is Google's AI UI-design tool. One web search at the start would have caught it. SFD today has no "do I even know what this is?" check.

**Proposed fix.** Before Phase 1 (Identify the Surface), run a target-verification gate. Trigger conditions:
- The prompt contains a proper noun the skill can't map with high confidence
- The prompt references a competitor / product / tool by name
- The prompt uses a domain-specific verb with multiple plausible meanings
- Any term the skill's internal knowledge doesn't resolve cleanly

When triggered:
1. Quick web search (if available).
2. Single confirmation question: "I'm reading '[user phrase]' as [most likely interpretation]. Correct? Y / N / (alt: your one-word clarification)"
3. If N: offer 2-3 alternate interpretations with short descriptions. If still N: *then* ask the user for a one-liner clarification (this is the one place a freeform answer is acceptable because the system has already exhausted its guesses).

**Cost.** 30 seconds. Usually invisible — if the target is obvious, the verification collapses to a single one-liner confirmation.

**Impact.** Prevents the worst-case failure mode entirely. **Highest ROI improvement in the backlog.**

---

### 2. Critique Ladder (replace "what's wrong?" with guided evaluation)

**Problem observed.** SFD's Phase 3 Iteration today asks "tell me what feels wrong, what's missing, and what should work differently." That's expert-level freeform analysis most users aren't equipped to give. Users who aren't design experts don't know what to look for. The result: either shallow feedback ("looks good, ship it"), overwhelmed silence, or unfocused rework.

**Proposed fix.** Replace the single open question with a **guided ladder**:

1. **Coarse judgment** (if multiple prototypes exist):
   "Which one feels closest to what you had in mind? 1 / 2 / 3 / (combination)"

2. **Narrow** (zoom in on the chosen prototype):
   "Prototype 2 has three parts: [A: the nav], [B: the main canvas], [C: the export flow]. Which part feels weakest? A / B / C / (all fine — let's move on)"

3. **Action** (propose concrete next moves):
   "For Part A, I could: (1) research how [competitor] solves this, (2) ask you 3 guided questions, (3) propose 2 alternative versions of Part A. Pick 1 / 2 / 3."

Freeform is always a valid escape, but never *required*.

**Cost.** Small. A few new paragraphs in the SKILL.md under "Phase 3: Iterate to Convergence."

**Impact.** Dramatically lowers the expertise floor for usable SFD output. Users with no design training can converge on a quality result. Also avoids "looks good, ship it" premature convergence by forcing a coarse preference before exiting.

---

### 3. Build-cycle Cadence + Premise-Check Announcement

**Problem observed.** When a prototype build takes 10-20 minutes (multiple HTML files, parallel subagents), the user has no interrupt opportunity until it's done. If the premise is wrong, all that work is landfill. Parallel subagents *multiply* the waste because they all bake the same wrong premise in parallel.

**Proposed fix.** Two sub-rules:

**3a. Announce premise before long work.** Any time SFD is about to spend >5 minutes of wall-clock on a build (especially before dispatching parallel subagents):
> "Working premise: [one-sentence interpretation of the task]. Building this now unless you say otherwise. ~5-minute gap before the next check-in."

Gives the user a 5-second abort window.

**3b. Chunk long builds.** For GUI work that would normally produce a full click-dummy in one shot, produce it **screen-by-screen** with a confirmation beat between screens:
> "Here's the landing screen. Feels right? Y / N / (tweak before I continue)"

Same for CLI: one command-session at a time. For API/library: one scenario file at a time.

**Cost.** A few rules added to Phase 2. The chunking is the real work — it requires the skill to commit to incremental output rather than deliverable-dump.

**Impact.** Turns the worst case from "60 minutes wasted before critique" into "60 seconds wasted before critique." This is the direct fix for the feedback-starvation pain.

---

## High — catch architectural errors before contracts

### 4. Phase 2.5: Feasibility Probe (optional, fast, post-surface)

**Problem observed.** In the Flock agent-skills session, the `.sfd/contracts.md` document was approved at Gate 1. Two hours later, `ce:plan` dispatched research agents and found three design errors: `SkillsContextProvider` can't inject tools (it only returns artifacts), `.with_skills` belongs on `AgentBuilder` not `FlockAgent`, `changelog.query(skill_name=...)` is fiction. Contracts had to be rewritten. The errors were caught late because SFD has no feasibility check between surface convergence and contract derivation.

**Proposed fix.** Optional gate between Phase 3 (convergence) and Phase 4 (contracts). Runs when any of:
- The surface depends on specific internal architecture (engine internals, framework APIs, interface contracts)
- The user explicitly asks for it
- SFD detects "contracts will touch internal abstractions" signals

Mechanism (inline, no external dispatcher — keeps standalone promise):
- Skill lists the specific assumptions the surface makes (e.g., "`ContextProvider` can inject tools", "`with_skills` on `FlockAgent`", "`changelog.query(skill_name=...)` exists")
- Skill uses its own Read / Grep / Glob tools to check each assumption against the real codebase
- Produces findings as a short list (assumption → actual → verdict)
- User decides (multiple choice): A) fix contracts now / B) accept limitations / C) re-open surface

**Cost.** ~2 minutes inline (no agent handoff, no research ecosystem required). Skippable for pure frontend/CLI where surface ≈ architecture. Works in any environment where the skill has file-read access — fully standalone.

**Impact.** Catches the Flock-skills class of error at the cheapest point. Optional keeps speed high for non-architectural work.

---

### 5. Inherit Multiple-Choice-with-Recommendation Rule

**Problem observed.** SFD today says "make opinionated choices, don't ask too many questions." Correct principle, but when SFD *does* need to ask (ambiguity, divergent paths, critique), the existing skill has no guidance on *how*. Meanwhile, `superpowers:brainstorming` and `ce:brainstorm` both encode a strong rule:

> "Every question MUST include your recommendation and reasoning. Never present a bare question without stating what you would choose. The user should be able to approve with a single word."

SFD should adopt this verbatim and extend it.

**Proposed fix.** Add to Operating Stance:

> **Every decision point is multiple choice with a recommendation and optional freeform escape.** Never "tell me what X is" — if the user knew, they'd have said it. Never ask a bare question. The user should be able to approve any proposal with a single word. Freeform is a valid escape hatch but never required.

Applies to: target verification, surface-type identification, critique ladder steps, contract confirmations, slice prioritization, hardening order.

**Cost.** Text-only change. Discipline to follow it consistently is the real work.

**Impact.** Matches the northstar. Makes SFD navigable by yes/no. Lowers cognitive load for the user.

---

## Medium — standalone readiness

### 6. Remove Hard Dependencies on CE / OpenSpec / Beads

**Problem observed.** SFD's "Integration with Other Skills" section currently references OpenSpec and Beads as if users will have them. In reality, users pick SFD precisely because they want a lightweight, self-contained workflow — many won't have those plugins.

**Proposed fix.** Downgrade all integrations to **soft** — "if [plugin] is available, you can hand off. Otherwise, here's the standalone equivalent:"

- OpenSpec hand-off → **standalone:** write `.sfd/contracts.md` (we already do this)
- Beads task tracking → **standalone:** use built-in task tools or `.sfd/tasks.md` list
- CE brainstorming → **standalone:** SFD's own Phase 0/0.5/1 covers pre-surface exploration
- CE planning → **standalone:** after Gate 2, emit an implementation plan into `.sfd/plan.md` or route to any planning skill the user has

**Cost.** Text-only, plus maybe 15 lines of standalone plan-writing template.

**Impact.** SFD works in any plugin environment. Matches the user's stated constraint.

---

### 7. Merge `.sfd/decision-log.md` + `.sfd/contracts.md`

**Problem observed.** In the Flock session, we ended up with two files under `.sfd/`: one for decisions, one for contracts. They referenced each other and had redundancy. Confusing to navigate.

**Proposed fix.** Single file: `.sfd/sfd.md` with sections:
- Project Context
- Decision Log
- Derived Contracts
- Gate Status
- Hardening Status

**Cost.** Small edit to the skill's "Decision Log Format" section.

**Impact.** Easier to navigate; reduces cross-reference churn.

---

### 8. Visual Companion Offer (borrowed from superpowers:brainstorming)

**Problem observed.** For GUI surface work, a text-only back-and-forth is lossy. `superpowers:brainstorming` has a "Visual Companion" — browser-based mockup channel the user can opt into. SFD currently produces HTML click-dummies in files but has no "let me show you in a browser" affordance.

**Proposed fix.** Adopt the companion offer pattern: when Phase 2 anticipates visual content (layout comparisons, wireframe variants), offer the browser channel as an *optional tool*, not a mode:

> "I can show you prototypes in a browser window if helpful. Y / N"

If yes: launch a local server with the prototypes, use browser for visual questions (layout choices, mockup comparisons), use terminal for conceptual questions (requirements, scope, tradeoffs).

Keep it **lightweight** — no heavy framework dependency. A local Python http.server serving the generated HTML is enough.

**Cost.** Moderate. Need a minimal browser-launcher helper. Can borrow directly from superpowers if the user has that plugin; ship a minimal fallback otherwise.

**Impact.** Dramatically better GUI iteration experience. Optional, so no cost for CLI/API work.

---

## Low — polish

### 9. Session-Start Recap as Multiple Choice

**Problem observed.** SFD's Session Start Protocol says "read the decision log, determine current gate status, report to user." Today the report is freeform text ("We're at Gate 2. Last session we converged on the dashboard UI."). Cognitive load is on the user to decide what to do next.

**Proposed fix.** End the recap with a multiple-choice "next move":
> "We're at Gate 2. Last session we [X]. Next moves: A) continue with contracts / B) probe feasibility first / C) re-open surface / D) pause. Recommend A. Pick?"

**Cost.** Text-only.

**Impact.** Smooth resumption. No friction.

---

## Out of scope / deferred

- **Auto-ideate when surface is ambiguous.** I considered importing ce-ideate's multi-frame divergent exploration but concluded: when the target is ambiguous, the fix is Phase 0.5 Target Verification (narrow it), not divergent explosion. If after verification there are still 2-4 legitimate design paths, "build them in parallel and let the user pick via critique ladder" is cleaner than a full ideation phase.
- **Deep alternatives phase.** Similar reasoning. If the user wants deep alternatives, they can invoke `ce:ideate` or `superpowers:brainstorming` before SFD. SFD's job is to drive to a concrete surface fast.
- **OpenSpec/Beads auto-detection.** Nice to have — detect which persistence tools are available and route accordingly. Low priority; can wait until SFD-v2 ships.
- **Auto-commit decision log at phase transitions.** Might be nice; easy to add later. Not architectural.

---

## Cost summary (rough)

| Improvement | Cost | Impact |
|---|---|---|
| 1. Target Verification | 30s per session | Kills worst failure mode |
| 2. Critique Ladder | Text-only | Dramatically lowers expertise floor |
| 3. Build Cadence + Premise-Check | Text-only + chunking discipline | Turns 60-min wrong builds into 60-sec aborts |
| 4. Feasibility Probe (inline) | ~2 min when fired, skippable, no dispatcher | Catches late-binding architectural errors, standalone |
| 5. MC-with-Recommendation rule | Text-only | Matches northstar; reduces cognitive load |
| 6. Remove hard deps on CE/OpenSpec/Beads | Text-only + 15-line template | Standalone as promised |
| 7. Merge state files | Text-only | Easier navigation |
| 8. Visual Companion offer | ~50 lines helper + text | Big GUI-work win |
| 9. Session-start recap MC | Text-only | Smooth resume |

Net: one meaningful code helper (item 8), everything else is a SKILL.md rewrite. See `skill_revised_preview.md` for the full rewrite.
