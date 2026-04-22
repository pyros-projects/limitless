---
name: surface-first-development
description: Use when the user wants to start or reshape an app, tool, CLI, API, automation, or feature from the interaction surface first, by converging on a prototype before deriving contracts and building inward.
---

# Surface-First Development (revised preview v2)

> **Preview draft for review, not the live skill.** Lives in `docs/sfd-backlog/` until Andre approves the direction. Changes from v1: inlined feasibility probe (no agent dispatcher), consolidated 8 Interaction Rules to 4, made opt-out rigorous at every phase/gate.

## Reference

If anything in this skill feels unclear, underspecified, or in tension with a real project situation, stop and read [references/whitepaper-v0.6.md](references/whitepaper-v0.6.md) before improvising.

## Triggers

- User says "let's build", "I want an app/tool/CLI/API that...", "I have an idea for..."
- User describes a product, feature, or tool without specifying architecture or internals
- User says "surface first", "click dummy", "show me what it would look like", "prototype this"
- User says "SFD", "surface-first"
- User wants to start a new project or feature and hasn't locked in a tech approach yet
- User asks "how should this work?" or "what would the UX be?" or "what would the workflow look like?"

## Purpose

Surface-First Development means: always start by building and iterating a working prototype of the outermost interaction layer, converge it with the user, derive contracts, then build inward. Do NOT start with database schemas, backend architecture, API design, or infrastructure. Start with what the user will actually see, touch, type, or call.

## Operating Stance

- Move from concrete artifact to critique, not from abstract discussion to specification.
- Make reasonable product decisions without asking the user to design the system for you.
- Prefer a fast, interactive prototype over a polished explanation of a prototype.
- Treat the user as the evaluator and steering function; your job is to generate proposals they can react to.
- Keep internals provisional until the surface is accepted.

## Interaction Rules (the 4 hard rules)

These override anything else in this skill.

1. **No required freeform prose input.** Ever. If the user knew the answer as prose, they would have included it in the prompt. Every decision point is multiple choice with a recommendation. Freeform is always *available* (via the multiple-choice tool's freeform field) but never *required*.
2. **Every question comes with a recommendation.** Never a bare question. Always state what you would pick and why. The user should be able to approve with a single keystroke.
3. **One question at a time.** Do not batch several unrelated questions into one message.
4. **Chunk long work.** Any build expected to take >5 minutes of wall-clock, or any parallel-subagent dispatch, starts with "Working premise: [one sentence]. Building unless you say otherwise." Long builds split into screen-sized / command-sized / scenario-sized chunks with a one-line confirmation beat between each.

Everything else in this skill (the critique ladder, opt-out rules, phase structure) is an *application* of these four.

## Opt-Out Rule (universal)

**Every phase, every gate, every check in this skill is skippable.** When SFD is about to run something the user didn't explicitly request — a verification, a probe, a ladder step — it presents a skip option as part of the question. The user should never have to learn a magic override keyword or dig into docs; "skip" is always one of the offered choices.

Opt-out visibility is the price of ceremony. If adding a check, you must also surface its skip option.

## First Move

When triggered:

1. Run Phase 0.5 (Target Verification) if any target term is ambiguous — often collapses invisibly.
2. Identify the primary interaction surface (Phase 1).
3. Build the smallest believable prototype of the critical path (Phase 2) — chunked per Rule 4.
4. Run the critique ladder (Phase 3).
5. Optional: Feasibility Probe (Phase 2.5) before contracts if surface depends on internal architecture.
6. Derive contracts, build inward, harden.

## Expected Artifact by Surface Type

| Surface | First artifact |
|---|---|
| GUI app | Click dummy or runnable mock UI |
| CLI tool | Executable prototype or realistic terminal session |
| API / library | Example consumer code that shows the desired developer experience |
| Data / ops workflow | Simulated runbook, monitoring view, or operator journey |
| Agent / automation | Trigger-to-outcome walkthrough with realistic state transitions |

If you are only *describing* the artifact instead of producing it, you are probably not following SFD yet.

## Why This Works

Humans are better at evaluating concrete proposals than writing abstract specs. Your job is to generate proposals fast so the human can react, critique, and steer. The human directs; you generate. Never ask the user to write a specification. Show them something and let them tell you what's wrong with it — but **lead them through how to tell you** (critique ladder, Phase 3).

---

## The Process

### Phase 0.5: Target Verification

Runs **before** Phase 1 when the prompt contains any of:
- A proper noun (product name, framework, tool, competitor) the skill cannot map with high confidence
- A domain-specific verb with multiple plausible meanings (e.g., "stitch", "forge", "weave", "bake")
- A reference to an external product or feature ("like X but for Y")
- A term the skill's internal knowledge can't resolve cleanly

**Protocol:**

1. If web search is available, run one quick search for the ambiguous term.
2. Form the single most likely interpretation.
3. Ask one confirmation question:

> "I'm reading '[user phrase]' as **[most likely interpretation]**.
> **A.** Yes — proceed.
> **B.** No — one of: [alt 1], [alt 2], [alt 3].
> **C.** Skip verification, I know what I'm doing.
> (Freeform always available via the input field.)"

4. If **A**: log interpretation, proceed. If **B**: user picks alternate, proceed. If **C**: skip this phase entirely.

**Collapse rule:** when the target is unambiguous, collapse to a single one-liner *inside* Phase 1: "Reading this as [target]. Surface type: [X]." The user can interject but no confirmation is forced.

**Cost.** 30 seconds when triggered. Zero when collapsed.

### Phase 1: Identify the Surface

Determine the interaction surface type. Prefer the decision table:

| If the user wants... | The surface is... | You build... |
|---|---|---|
| A web/mobile app | GUI | Click dummy (HTML/React, functional navigation, mock data) |
| A CLI tool | Terminal session | Executable prototype OR scripted session transcript |
| An API or library | Developer experience | Example consumer/integration code |
| A data pipeline | Operator workflow | Simulated deploy/monitor/debug session |
| An automation/agent | Trigger-to-outcome flow | Scenario walkthrough |

When unambiguous, state it and move on. When ambiguous:

> "This could be a **GUI app** (recommended, since you mentioned a dashboard) or a **CLI tool**.
> **A.** GUI
> **B.** CLI
> **C.** Both
> (Or tell me in one word.)"

### Phase 1.5: Visual Companion Offer (GUI work only, optional)

For GUI surfaces, offer an optional browser companion as its own message:

> "Some prototypes may be easier to evaluate in a browser than in the terminal. Launch a local preview window?
> **A.** Yes.
> **B.** No — terminal only.
> **C.** Skip the question entirely (defaults to B for the rest of the session)."

Skip this phase for CLI / API / library / pipeline surfaces.

### Phase 2: Generate Surface Proposal (chunked)

Build a working prototype. Apply Rule 4 rigorously:

1. **Announce the premise** before any build expected to take >5 minutes:
   > "Working premise: [one-sentence interpretation + scope]. First chunk starts now unless you say otherwise."

2. **Chunk output.** Never produce a silent 20-minute deliverable. Break into:
   - **GUI:** one screen/component at a time
   - **CLI:** one command + response pair at a time
   - **API/library:** one scenario file at a time
   - **Pipeline/agent:** one trigger-to-outcome walkthrough at a time

3. **Confirmation beat between chunks:**
   > "Landing screen done.
   > **A.** Keep going.
   > **B.** Tweak this first.
   > **C.** Stop — show me everything so far and we decide."

4. **Skip-chunking opt-out.** At the first confirmation beat, user can choose:
   > "You can skip chunking for the rest of this build — I'll produce everything in one shot and we review at the end.
   > **Keep chunked (recommended) / Skip chunking for this build**"

5. **Go fast, not deep.** Mock data, placeholder logic, simulated responses. Surface must look real, nothing behind it needs to work.
6. **Make decisions.** Don't ask for layout, colors, flow, copy. Make opinionated choices. Critique ladder will surface the mismatches.
7. **Show, don't describe.** Produce the artifact, not a description.

After all chunks complete:

> "Prototype ready.
> **A.** Move to critique ladder (recommended).
> **B.** Ship as-is, skip critique.
> **C.** I already know what to change — let me tell you."

### Phase 2.5: Feasibility Probe (optional, inline — no agent dispatch)

Runs between Phase 3 convergence and Phase 4 contracts. Default behavior:

- **On** for API / library / agent surfaces (surface implies internal architecture)
- **Off** for GUI / CLI surfaces (surface ≈ architecture)
- User can always force on or off

**Protocol (inline, no external dispatcher):**

1. Announce:
   > "About to derive contracts. Quick feasibility check: I'll read the specific files the surface assumes (takes ~2 min — I'm just reading and checking).
   > **A.** Run (recommended — surface touches internal abstractions).
   > **B.** Skip."

2. If **A**, the skill itself:
   - Lists the specific assumptions the surface makes (e.g., "assumes `ContextProvider` can inject tools", "assumes `with_skills` lives on `FlockAgent`", "assumes `changelog.query(skill_name=...)` exists")
   - Uses its own Read / Grep / Glob tools to check each assumption against the real codebase
   - Produces findings as a short list (assumption → actual → verdict)

3. Present findings as multiple choice:
   > "Probe found **N assumption violations**: [short list, each one line].
   > **A.** Fix contracts now (I'll rewrite the integration plan based on what's actually there) — recommended.
   > **B.** Accept limitations (document the holes and proceed; plan will have to rework them).
   > **C.** Re-open Phase 3 (a surface decision is architecturally impossible)."

Never present freeform findings. Always translate into next-action choice.

**Why inline instead of agent-dispatched:** the probe is "read N specific files and check assumptions" — 2-3 minutes of disciplined reading, not a research task. Keeps SFD standalone (no research-agent infrastructure required) and faster (no context handoff).

### Phase 3: Iterate via Critique Ladder

Do **not** ask "what feels wrong?" or "what's missing?" Lead the user through a three-rung ladder. Freeform is available on every rung via the multiple-choice tool's input field — users who already know what's wrong just type it and skip the ladder entirely.

**Rung 1 — Coarse judgment:**

If multiple prototypes were built:
> "Which feels closest to what you had in mind?
> **1 / 2 / 3**
> (Or type: `combination`, or your own one-line reaction.)"

If one prototype:
> "Walk through this. Does it feel roughly right?
> **A.** Yes, ship this.
> **B.** Almost, but one part is off.
> **C.** Not quite — different angle needed.
> **D.** Skip the ladder, I'll tell you directly."

If **A** (or enthusiasm signals — "love it", "ship it", "this is great"): auto-advance to Phase 4.
If **D** or a freeform answer: jump straight to applying the feedback; no ladder climbing.

**Rung 2 — Narrow:**

If the user picked B or C and didn't go freeform:
> "The prototype has three parts: **A. [name]**, **B. [name]**, **C. [name]**.
> Which feels weakest?
> **A / B / C**
> (Or `all fine — converged`, or type a one-line observation.)"

**Rung 3 — Action:**

For the weak part:
> "For Part [X]:
> **1.** Research how [Competitor/Framework] solves it (~5 min)
> **2.** Ask 3 guided questions to narrow the fix (~2 min)
> **3.** Propose 2 alternate versions to compare (~5 min)
> **4.** Skip the ladder and tell me directly.
> (Or type the fix in one sentence.)"

Whichever the user picks, execute, then return to Rung 2 until "all fine — converged."

**Convergence signal:**
> "Surface converged. Move to contract derivation?
> **A.** Yes (recommended).
> **B.** One more critique round.
> **C.** Let me re-open Phase 2 — premise was wrong."

### Phase 4: Derive Contracts

Extract from the converged surface:

1. **API contracts** — every data operation, method, payload, error shape implied
2. **Domain rules** — business-logic invariants required for surface behavior
3. **Non-functional requirements** — real-time? offline? sub-second? scale targets?
4. **Acceptance criteria** — testable assertions per flow

Write to `.sfd/sfd.md`.

Confirm:

> "Contracts derived.
> **A.** Looks complete — proceed to build-inward.
> **B.** Something's missing (type what).
> **C.** Re-open Phase 3."

### Phase 5: Build Inward (Vertical Slices)

1. **One slice at a time.** Each makes one surface flow real end-to-end.
2. **Slice ordering** — if non-obvious:
   > "Build which flow first?
   > **A. [login]** (recommended — enables everything else).
   > **B. [dashboard]**.
   > **C. [settings]**.
   > (Or type a different ordering.)"
3. **Keep the surface working.** Non-live flows keep mocks. User should always be able to click through.
4. **Acceptance tests anchored to converged behavior.** Before or during implementation.

### Phase 6: Progressive Hardening

Replace simulated components in this order (user can pick alternate):

1. Mock data → real persistence
2. Placeholder auth → real identity
3. Simulated behavior → domain logic
4. Happy-path only → error handling, validation, loading states
5. Baseline perf → optimization

After each step, *visually or functionally* confirm the surface flows still work as converged.

---

## State File Format

One file: `.sfd/sfd.md` (single source of truth per project).

```markdown
## SFD Project State

### Target
[Confirmed interpretation from Phase 0.5, or "skipped by user"]

### Surface Type
[GUI / CLI / API / Pipeline / Agent]

### Convergence Status
[Iterating / Converged YYYY-MM-DD / Re-opened for feature X]

### Decisions
- YYYY-MM-DD: [decision] — [rationale, alternatives rejected]

### Derived Contracts
- [endpoint / interface / behavior]: [shape]

### Gate Status
- [ ] Gate 0.5: Target Verified (or skipped)
- [ ] Gate 1: Surface Converged
- [ ] Gate 1.5: Feasibility Probed (or skipped / N/A)
- [ ] Gate 2: Contracts Frozen
- [ ] Gate 3: Architecture Review
- [ ] Gate 4: Hardening Complete
- [ ] Gate 5: Release Ready

### Hardening Status
- [ ] Persistence (currently: mock data)
- [ ] Auth (currently: placeholder)
- [ ] Domain logic (currently: simulated)
- [ ] Error handling (currently: happy-path)
- [ ] Performance (currently: unoptimized)
```

---

## Gate Checklist

Each gate can be marked "skipped by user" if the user opted out of its checks.

### Gate 0.5: Target Verified
- [ ] Ambiguous terms confirmed against user's intent (or skip logged)
- [ ] Target logged in `.sfd/sfd.md`

### Gate 1: Surface Converged
- [ ] Critical flows demonstrated via chunked build
- [ ] Convergence confirmed via critique ladder or direct user signal
- [ ] Decision log captures key choices and rejected alternatives

### Gate 1.5: Feasibility Probed (optional)
- [ ] Probe run if surface touches internal architecture (or skip logged)
- [ ] Findings triaged into A (fix)/B (accept)/C (re-open)
- [ ] Chosen action executed

### Gate 2: Contracts Frozen
- [ ] API contracts documented
- [ ] Domain invariants identified
- [ ] Non-functional requirements specified with targets
- [ ] User confirmed contracts via A/B/C choice

### Gate 3: Architecture Review
- [ ] Tech stack confirmed via multiple-choice presentation
- [ ] Hot paths and scaling risks identified
- [ ] Hardening order established
- [ ] Security considerations reviewed

### Gate 4: Hardening Complete
- [ ] All mock/simulated components replaced
- [ ] Acceptance tests passing against real implementation
- [ ] Error handling and validation in place
- [ ] Observability configured

### Gate 5: Release Ready
- [ ] Regression suite passing
- [ ] Rollback plan documented
- [ ] Monitoring on surface-critical paths

---

## Anti-Patterns (Don't Do This)

1. **Don't ask for a spec before building.** Build → critique ladder → derive.
2. **Don't start with the database schema.** Schema serves surface.
3. **Don't build backend before surface is converged.**
4. **Don't throw away the prototype.** Harden it.
5. **Don't gold-plate the prototype.** Fast and opinionated beats slow and polished.
6. **Don't ask bare questions.** (Rule 2 — every question = MC + recommendation.)
7. **Don't require freeform input.** (Rule 1 — freeform is always available, never required.)
8. **Don't produce silent 20-minute builds.** (Rule 4 — chunk with confirmation beats.)
9. **Don't guess at ambiguous targets.** Run Phase 0.5.
10. **Don't add a check without an opt-out.** Every gate is skippable. If you're adding ceremony, you're also adding its skip option.

---

## When NOT to Use SFD

- The project has no meaningful interaction surface (pure background service, embedded firmware).
- The core challenge is algorithmic/mathematical/protocol-level and the surface is trivial.
- Regulatory requirements demand formal specs before implementation.
- The user explicitly asks for a different approach.

In those cases:
> "This project's complexity is mostly below the surface layer.
> **A.** Use [appropriate alternative] for the core, SFD for the interaction layer.
> **B.** Skip SFD entirely.
> **C.** Proceed with SFD anyway (I'll keep it light)."

---

## Integration with Other Skills (all optional, soft)

SFD is standalone. These are hand-off *options* if plugins are installed. None are required.

- **OpenSpec** (if available): after Gate 2, export contracts as OpenSpec artifact
- **Beads** (if available): after Gate 2, create tasks for slices + hardening steps
- **Compound Engineering `ce:plan`** (if available): after Gate 2, deep implementation plan
- **Superpowers `writing-plans`** (if available): after Gate 2, compact plan

If none are installed, SFD writes its own minimal plan into `.sfd/plan.md` at Gate 2: ordered slices + hardening steps, no ceremony.

Present hand-off as multiple choice:
> "Contracts frozen. Next step:
> **A.** [best available planning tool] (recommended).
> **B.** SFD's built-in plan file.
> **C.** Stop here — I'll pick it up manually."

---

## Session Start Protocol

When resuming an SFD project:

1. Read `.sfd/sfd.md` if it exists.
2. Determine current gate.
3. Present as multiple choice:

> "Resuming SFD project [X]. Current: Gate [N] — [one-sentence status].
> **A.** Continue from where we left off (recommended).
> **B.** Re-open the last gate.
> **C.** Show me the decision log before deciding."

If no `.sfd/sfd.md` but project artifacts exist:
> "No SFD state file, but I see [X].
> **A.** Reconstruct and continue.
> **B.** Start fresh.
> **C.** Show me what you see first."

## Execution Heuristic

1. What is the surface?
2. What is the smallest artifact that makes it real enough to critique?
3. What did the user answer in the critique ladder?
4. What contract does that answer imply?
5. What is the next thin slice inward?
6. **Am I about to ask a bare question?** Convert to MC with recommendation. (Rule 2.)
7. **Am I about to require prose?** The user can't give you prose they couldn't already give. Convert to MC. (Rule 1.)
8. **Am I about to build silently for >5 minutes?** Chunk it. (Rule 4.)
9. **Am I adding a check?** I must also surface its skip option. (Opt-Out Rule.)

## End of Session Protocol

1. Update `.sfd/sfd.md` with new decisions + current gate.
2. Wrap up:
> "Wrapping up.
> **A.** Commit state file.
> **B.** Leave uncommitted.
> **C.** Show me the diff first."
