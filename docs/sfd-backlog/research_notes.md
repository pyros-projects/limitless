# Research Notes: What I Borrowed, What's New

## Skills I reviewed for inspiration

### `superpowers:brainstorming` — heavy borrower

**Location:** `~/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.6/skills/brainstorming/SKILL.md`

**What I borrowed verbatim (or nearly so):**
- **The multiple-choice-with-recommendation rule.** Superpowers states: *"Every question MUST include your recommendation and reasoning. Never present a bare question without stating what you would choose. The user should be able to approve with a single word."* I adopted this as Interaction Rule #2 in the revised SFD.
- **"One question at a time"** as a hard rule. Superpowers has this as a Key Principle.
- **Visual Companion offer pattern.** Superpowers' approach of offering the browser as its own message (not bundled with a clarifying question) and deciding per-question whether to use it is clean. I lifted the pattern into Phase 1.5. Kept it optional + lightweight so SFD stays standalone.
- **Hard gate against premature implementation.** Superpowers has a `<HARD-GATE>` around invoking implementation skills until the design is approved. SFD already has this in spirit (Gate 1 → Gate 2 → Gate 5), but making it explicit in the Interaction Rules helps enforcement.

**What I did NOT borrow:**
- The "Checklist with task-per-item" structure. Superpowers mandates task-creation-per-item before proceeding. Fine for brainstorming but too much ceremony for SFD's fast-iterate loop.
- The requirement to always propose 2-3 approaches before settling. Works for brainstorming's "what to build" question; would be overkill for every SFD decision point.
- The writing-plans handoff as terminal state. SFD has its own Gate 2-5 flow; forcing a handoff to a specific planning skill would break standalone-ness.

### `ce:brainstorm` — lighter borrower

**Location:** `~/.claude/plugins/cache/compound-engineering-plugin/compound-engineering/2.65.0/skills/ce-brainstorm/SKILL.md`

**What I borrowed:**
- **Single-select > multi-select preference.** CE states: *"Prefer single-select multiple choice. Use multi-select rarely and intentionally — only for compatible sets such as goals, constraints, non-goals, or success criteria that can all coexist."* Adopted into Interaction Rule #3.
- **Scope assessment (Lightweight / Standard / Deep).** Not a direct lift, but the principle — match ceremony to size — influenced how Phase 0.5 collapses for unambiguous targets and how Phase 2.5 is conditional.
- **Use platform blocking question tool when available.** CE references `AskUserQuestion` in Claude Code. I implicitly assume this — multiple choice responses naturally map to it.

**What I did NOT borrow:**
- The full ce-brainstorm phase structure (Phase 0 Resume/Assess/Route, Phase 1.2 Product Pressure Test, etc.). Too much for SFD. The pressure-test angle is valuable but better handled by the critique ladder's Rung 1 ("does this feel roughly right?" — if no, rethink).
- Requirements document template. SFD derives contracts post-surface; ce:brainstorm writes requirements pre-planning. Different artifact class.
- External research / framework-docs routing. SFD's Phase 2.5 Feasibility Probe covers the one case that matters most (codebase feasibility); deeper external research is a separate skill's job.

### `compound-engineering:ce-ideate` — not borrowed, but informed

**What I learned from it:**
Multi-frame divergent ideation is powerful when you need "40 ideas to pick from." It is NOT what SFD needs pre-surface. If the target is ambiguous, the fix is **target verification** (narrow to 1 interpretation), not **divergent exploration** (generate 40 interpretations). If after verification there are 2-4 legitimate design paths, SFD can build them in parallel and let the critique ladder pick — no full ideation phase needed.

So ce:ideate stays a separate skill users invoke BEFORE SFD when the problem space is genuinely open-ended. SFD itself doesn't duplicate it.

### `limitless:codies-research` and `wd-agent-skills:wd-research` — reference pattern

Didn't borrow directly, but these confirm the pattern: **research is a separate, optional, fast step**. SFD's Phase 2.5 Feasibility Probe adopts the same shape — one targeted dispatch, findings translated into action choice.

### `superpowers:writing-plans` — not needed for SFD internals

Relevant as a hand-off target (if superpowers is installed, users can go from Gate 2 contracts → writing-plans). Kept as a soft integration in "Integration with Other Skills," not a hard requirement.

### Other skills checked briefly

- `compound-engineering:frontend-design` — has design-review rigor and a screenshot verification loop. Consider for future SFD Phase 6 hardening step (verify visual quality of GUI surfaces). Out of scope for this round.
- `skill-creator:skill-creator` — mostly about skill authorship; not relevant to SFD internals. It informed the *shape* of this preview (what a well-structured SKILL.md looks like).
- `limitless:searxng` — a web-search adapter. If adopted, it could power the Phase 0.5 Target Verification search. Keep as optional.
- `compound-engineering:document-review` — runs a structured review on docs. Could be useful for reviewing the `.sfd/sfd.md` state file at gate transitions. Defer.

## What's net-new in revised SFD (not from any existing skill)

1. **Critique Ladder (Rung 1 → 2 → 3).** No other skill encodes this pattern. Brainstorming skills go coarse → narrow by asking questions; SFD's critique ladder goes coarse → narrow by **proposing options** with the user picking from them. Especially powerful because it doesn't require the user to be a design expert.

2. **Chunked build with confirmation beats.** Other skills produce their deliverable in one shot. SFD's rule — *"never more than ~5 min of silent build without a y/n checkpoint"* — is new. Directly fixes the feedback-starvation pain.

3. **Premise-check announcement before parallel subagents.** The "Working premise: [one sentence]. Building unless you say otherwise" rule before any long operation. None of the other skills surface their working premise the same way; most just fire.

4. **Phase 0.5 Target Verification with collapse rule.** The specific pattern of "run verification, but invisibly skip if the target is high-confidence" is new. Prevents over-questioning while still catching the Google Stitch case.

5. **Phase 2.5 Feasibility Probe as a gate.** Other skills defer this to planning-time research (`ce:plan` does it). Making it an SFD gate at the cheapest point is new.

6. **The "every decision is multiple choice" hard rule applied uniformly to critique.** Other skills relax this rule at critique time ("tell me what feels wrong"). SFD revised holds the line: even critique is multiple choice via the ladder.

7. **Standalone promise.** Explicit downgrade of all integrations to soft, with built-in fallbacks.

## The meta-lesson

The existing ecosystem (superpowers, CE, limitless) has excellent individual patterns. SFD's value-add is **composing them into a single fast loop that drives from target-verification to converged surface to correct contracts without any required freeform input from the user.**

Nothing here is radical. It's assembly — mostly well-established patterns (multiple-choice-with-recommendation, single-question-at-a-time, visual companion, one-targeted-research-dispatch) into a tighter, more opinionated workflow with one genuinely new pattern (the critique ladder) that raises the floor for non-expert users.
