---
name: surface-first-development
description: This skill should be used when the user wants to build, prototype, or reshape an app, tool, CLI, API, automation, or feature by starting from the interaction surface first. Responds to "let's build", "prototype this", "I have an idea for an app/tool", "show me what it would look like", "surface first", "SFD", "click dummy", "what would the UX be", "what would the workflow look like", or any request where the user describes what something should do without specifying architecture. Converges on a working prototype before deriving contracts and building inward.
---

# Surface-First Development

## Reference

If anything in this skill feels unclear, underspecified, or in tension with a real project situation, stop and read [references/whitepaper-v0.6.md](references/whitepaper-v0.6.md) before improvising. Treat that whitepaper as the authoritative reference for the methodology.

If this `SKILL.md` and the whitepaper ever feel misaligned, follow the whitepaper and then update the skill so the drift is removed.

## Triggers

- User says "let's build", "I want an app/tool/CLI/API that...", "I have an idea for..."
- User describes a product, feature, or tool without specifying architecture or internals
- User says "surface first", "click dummy", "show me what it would look like", "prototype this"
- User says "SFD", "surface-first"
- User wants to start a new project or feature and hasn't locked in a tech approach yet
- User asks "how should this work?" or "what would the UX be?" or "what would the workflow look like?"

## Purpose

You are following the **Surface-First Development** methodology. The core principle: always start by building and iterating a working prototype of the outermost interaction layer, converge it with the user, derive contracts, then build inward.

Do NOT start with database schemas, backend architecture, API design, or infrastructure. Start with what the user will actually see, touch, type, or call.

## Operating Stance

- Move from concrete artifact to critique, not from abstract discussion to specification.
- Make reasonable product decisions without asking the user to design the system for you.
- Prefer a fast, interactive prototype over a polished explanation of a prototype.
- Treat the user as the evaluator and steering function; your job is to generate proposals they can react to.
- Keep internals provisional until the surface is accepted.

## The Propose-Choose-Proceed Rule

This is the governing interaction pattern for the entire SFD process. Every decision point — from research directions to surface proposals to contract shapes to slice ordering — follows this loop:

1. **Propose** 2-3 concrete directional options. Not vague buckets — each option should be specific enough that the user can picture what choosing it means.
2. **User chooses** one (or more), or discards all with feedback. If discarded, generate a new batch informed by the feedback. Repeat until the user approves a direction.
3. **Proceed** only after explicit user approval.

This prevents the failure mode where you barrel ahead on assumptions and the user has to interrupt to course-correct. It also prevents the opposite failure mode where you ask open-ended questions and the user has to do the design work. The sweet spot: you do the thinking, the user does the steering.

The pattern applies everywhere — Phase 2 research directions, Phase 3 prototype concepts, Phase 4 iteration proposals, Phase 5 contract alternatives, Phase 6 slice ordering, Phase 7 hardening priorities. If you're about to make a significant directional choice, present options first.

## First Move

When this skill is triggered:

1. Identify the primary interaction surface.
2. Explore the problem space (research or generate concept directions).
3. Get user approval on a direction before building anything.
4. Build the smallest believable prototype that covers the critical path.
5. Put it in front of the user quickly.
6. Ask for critique of behavior and flow, not implementation.

Do not begin with architecture diagrams, schema design, backend planning, or large requirement questionnaires unless the user explicitly forces that order.

## Expected Artifact by Surface Type

| Surface | First artifact |
|---|---|
| GUI app | Click dummy or runnable mock UI |
| CLI tool | Executable prototype or realistic terminal session |
| API / library | Example consumer code that shows the desired developer experience |
| Data / ops workflow | Simulated runbook, monitoring view, or operator journey |
| Agent / automation | Trigger-to-outcome walkthrough with realistic state transitions |

If you are only describing the artifact instead of producing it, you are probably not following SFD yet.

## Why This Works

Humans are better at evaluating concrete proposals than writing abstract specs. Your job is to generate proposals fast so the human can react, critique, and steer. The human directs; you generate. Never ask the user to write a specification. Show them something and let them tell you what's wrong with it.

---

## The Process

### Phase 1: Identify the Surface

Determine what type of interaction surface the project has. Ask the user ONLY if it's genuinely ambiguous.

| If the user wants... | The surface is... | You build... |
|---|---|---|
| A web/mobile app | GUI | Click dummy (HTML/React, functional navigation, mock data) |
| A CLI tool | Terminal session | Executable prototype OR scripted session transcript |
| An API or library | Developer experience | Example consumer/integration code |
| A data pipeline | Operator workflow | Simulated deploy/monitor/debug session |
| An automation/agent | Trigger-to-outcome flow | Scenario walkthrough |

### Phase 2: Explore the Problem Space

Before building anything, understand the landscape. The goal is to arrive at an informed concept direction that both you and the user believe in — not to produce a research paper, but to avoid building a prototype grounded in ignorance.

**The "Already Exists" Check — do this throughout Phase 2, not as a separate step:**

Your job during discovery is to map what exists so the user can make informed decisions about where to spend their building energy. Two things to watch for:

- **If the user's idea already exists** (or something very close), say so immediately. Don't wait for the user to ask "isn't this already a thing?" — surfacing that is YOUR job. Name the existing tool, explain what it does, and then focus on the interesting part: what does the user's vision do that the existing tool doesn't? Those differences are where the real project lives. The user may know the tool exists and want to build anyway (for control, philosophy, learning, or because the existing tool is bad) — that's their call. Your job is to make sure they have the information, not to talk them out of building.
- **If parts of the idea are solved by existing libraries, frameworks, or protocols**, surface them as building blocks. The user's building energy should go toward the unique value, not toward re-solving solved problems. "We should use X for rendering and build the feedback layer on top" is almost always a better direction than "let's build a renderer from scratch." Frame concept directions around what to USE (commodity) and what to BUILD (the differentiator).

This isn't a one-time gate — it applies at every decision point throughout the process. If mid-conversation you realize a library handles something you were about to propose building, say so. The user should never have to be the one pointing out "doesn't X already do this?"

**Step 1: Propose research directions**

Present 2-3 research directions as concrete options. Each direction should focus on a different angle of the problem space — e.g., existing tools and their gaps, technical approaches, target user segments, or prior art in adjacent domains. Format as a numbered list the user can pick from:

> Here are a few angles I can research before we prototype:
> 1. **[Direction A]** — [what you'd look into and why it matters]
> 2. **[Direction B]** — [what you'd look into and why it matters]
> 3. **[Direction C]** — [what you'd look into and why it matters]
>
> Pick one or more, or tell me to skip research / try different directions.

If the user discards all directions, ask what's off and generate a new batch. If the user says "skip research" or the topic clearly doesn't need it (they already know the space, or it's a personal tool with no competitive landscape), move to Step 3 directly.

**Step 2: Research and present findings**

Use available research skills (web search, documentation lookup, etc.) to investigate the chosen direction(s). Keep research focused — you're building context for a prototype, not writing a thesis.

Present findings as a concise summary, structured as:
1. **What already exists** — name specific tools, libraries, and projects. If something IS the user's idea (or 80%+ of it), flag it prominently: "This already exists — it's called X. Here's what it does and where it differs from your vision."
2. **What's commodity** — libraries, frameworks, and protocols that solve parts of the problem. Recommend using them: "We should use X for this part rather than building our own."
3. **What's the actual gap** — the part that doesn't exist yet. This is where the user's project has value.

This structure prevents the failure mode where you present a landscape survey and then propose building something the survey just showed already exists. The gap analysis IS the research output — everything else is context.

**Step 3: Propose concept directions**

Based on research (or your own knowledge if research was skipped), propose 2-3 concept directions for the prototype. Each should be a distinct take on how to solve the user's problem — different enough that choosing one meaningfully shapes what the prototype looks like.

Each direction should clearly state what you'd **use** (existing tools/libraries) vs what you'd **build** (the unique value). If a direction is mostly "use existing tool X," that's a valid direction — and often the best one.

> Based on what I found, here are three directions we could take:
> 1. **[Concept A]** — [what the tool would feel like, key differentiator]. Uses: [existing tools]. Builds: [new parts].
> 2. **[Concept B]** — [what the tool would feel like, key differentiator]. Uses: [existing tools]. Builds: [new parts].
> 3. **[Concept C]** — [what the tool would feel like, key differentiator]. Uses: [existing tools]. Builds: [new parts].
>
> Which resonates? Or should I think in a different direction?

If the user discards all concepts, ask what's missing and generate a new batch. If the user wants more research first, loop back to Step 1.

**Step 4: Lock direction**

Once the user picks a concept direction, confirm it explicitly:

> "Locked in: [chosen direction]. Building the first prototype around this."

Only now proceed to Phase 3.

### Phase 3: Generate Surface Proposal

Build a working prototype of the surface immediately. Rules:

1. **Go fast, not deep.** Use mock data, placeholder logic, and simulated responses. The surface must look and feel real to interact with, but nothing behind it needs to work yet.
2. **Make decisions.** Don't ask the user to specify layout, colors, flow structure, field names, or copy. Make opinionated choices. The user will correct what's wrong — that's faster than asking upfront.
3. **Cover the critical path.** Build the 2-3 most important user flows end to end. Don't build every screen or every edge case yet.
4. **Show, don't describe.** Never respond with a written description of what the prototype would look like. Build it and let the user interact with it.

After generating, tell the user:

> "Here's a first prototype of [what it is]. Click/walk through it and tell me what feels wrong, what's missing, and what should work differently. Don't worry about internals — we'll handle those after we nail the experience."

**Good enough for round one:** believable, navigable, and critiqueable. Not production-ready, not deeply wired, not exhaustive.

### Phase 4: Iterate to Convergence

The user will critique the prototype. Your job:

1. **Listen for behavioral critique.** "This should do X when I click Y." Act on it.
2. **Ignore implementation preferences** unless the user insists. If they say "use Redux" or "make this a microservice," gently redirect: "Let's nail the behavior first, then I'll pick the best implementation approach."
3. **Probe edge cases yourself.** After addressing the user's feedback, proactively show: "By the way, here's what happens when [edge case]. Does this feel right?"
4. **Track decisions.** Maintain a running log of what was changed and why, including alternatives that were tried and rejected.

**Convergence check:** After each iteration round, ask:

> "Walk through the [key flows]. Is there anything that still feels wrong or missing?"

When the user says something like "this feels right," "let's build it," "I'm happy with this," or "ship it" — convergence is reached. State this explicitly:

> "Surface converged. Moving to contract derivation."

### Phase 5: Derive Contracts

Before writing any backend/internal code, extract what the converged surface demands:

1. **API contracts:** List every data operation the surface performs. What endpoints, methods, payloads, and error shapes are implied?
2. **Domain rules:** What business logic must be true for the surface behavior to remain valid? (e.g., "a goal can only be marked overdue if its deadline has passed and it's not complete")
3. **Non-functional requirements:** Does the surface imply real-time updates? Offline capability? Sub-second response times?
4. **Acceptance criteria:** Translate the converged surface flows into testable assertions.

Present these to the user for confirmation:

> "Based on the converged surface, here are the contracts the backend needs to fulfill: [list]. Does this capture everything? Anything I'm missing?"

### Phase 6: Build Inward (Vertical Slices)

Now build the internals. Rules:

1. **One slice at a time.** Each slice makes one surface flow real, end to end — from user interaction through logic to persistence and back.
2. **Start with the highest-value flow.** Ask the user which flow matters most if not obvious.
3. **Keep the surface working.** At every point, the prototype should still be interactive. Flows that aren't yet backed by real implementation continue to use mocks. The user should always be able to click through everything.
4. **Write acceptance tests anchored to converged behavior.** Before or during implementation, encode the converged surface flows as automated tests.

When in doubt about slice order, implement the slice that makes the most important user-visible flow real first.

### Phase 7: Progressive Hardening

Replace simulated components with real implementations in this general order:

1. Mock data -> real persistence
2. Placeholder auth -> real identity
3. Simulated behavior -> domain logic
4. Happy-path only -> error handling, validation, loading states
5. Baseline perf -> optimization

After each hardening step, verify the surface still behaves as converged.

---

## Decision Log Format

Maintain this throughout the project. It survives sessions and prevents re-litigating settled decisions.

Use this canonical file path for the decision log:

- `.sfd/decision-log.md`

```markdown
## SFD Decision Log

### Surface Type
[GUI / CLI / API / Pipeline / Agent]

### Convergence Status
[Iterating / Converged on YYYY-MM-DD / Re-opened for feature X]

### Decisions
- [Date] [What was decided] — [Why, and what alternatives were rejected]
- [Date] ...

### Derived Contracts
- [Endpoint/interface]: [shape]
- ...

### Hardening Status
- [ ] Persistence (currently: mock data)
- [ ] Auth (currently: placeholder)
- [ ] Domain logic (currently: simulated)
- [ ] Error handling (currently: happy-path)
- [ ] Performance (currently: unoptimized)
```

---

## Gate Checklist

Use these gates to track progress. Don't skip gates.

### Gate 1: Surface Converged
- [ ] Critical flows demonstrated and accepted by user
- [ ] Edge cases explored interactively
- [ ] Decision log captures key choices and rejected alternatives
- [ ] Open UX questions logged (if any)

### Gate 2: Contracts Frozen
- [ ] API contracts documented
- [ ] Domain invariants identified
- [ ] Non-functional requirements specified with targets
- [ ] User confirmed contracts match surface expectations

### Gate 3: Architecture Review
- [ ] Tech stack confirmed
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

1. **Don't ask for a spec before building.** "Can you write requirements first?" — No. Build a surface prototype and iterate. The spec is derived, not authored.
2. **Don't start with the database schema.** The schema serves the surface, not the other way around.
3. **Don't build backend before the surface is converged.** You will build the wrong backend.
4. **Don't throw away the prototype.** Harden it. If a full rewrite is truly needed, the converged surface is still the behavioral reference.
5. **Don't gold-plate the prototype.** Fast and opinionated beats slow and polished. The user will fix what's wrong.
6. **Don't ask open-ended questions.** Present options, don't ask the user to design. "Which of these three directions?" is good. "What do you want it to look like?" is bad. The user steers; you generate.

---

## When NOT to Use SFD

Recognize when SFD is not the right primary approach and tell the user:

- The project has no meaningful interaction surface (pure background service, embedded firmware).
- The core challenge is algorithmic, mathematical, or protocol-level and the surface is trivial.
- Regulatory requirements demand formal specs before implementation.
- The user explicitly asks for a different approach.

In these cases, say:

> "This project's complexity is mostly below the surface layer. I'd suggest we [appropriate alternative] for the core, and use surface-first only for the interaction layer on top."

---

## Integration with Other Skills

### With OpenSpec
After Gate 1 (surface converged), export the converged state and contracts as an OpenSpec artifact. This gives the project persistent, structured context that survives session boundaries.

### With Beads
After Gate 2 (contracts frozen), create Beads tasks for each vertical slice and hardening step. This gives you a persistent task tracker that survives context compaction and session switches.

### Workflow
```
SFD Phase 1-4 (discover + research + prototype + converge)
    |
    v
Gate 1 --> OpenSpec: capture converged surface + contracts
    |
    v
Gate 2 --> Beads: create tasks for slices + hardening
    |
    v
SFD Phase 6-7 (build + harden, tracked in Beads)
    |
    v
Gates 3-5 (review, verify, release)
```

---

## Session Start Protocol

When resuming work on an SFD project:

1. Check `.sfd/decision-log.md` first. If it exists, read it. If not, search for an existing SFD decision log and standardize on `.sfd/decision-log.md`.
2. Determine current gate status.
3. Report to user: "We're at [Gate N]. Last session we [summary]. Next step is [what]."
4. If no log found but project artifacts exist, reconstruct state from code and ask user to confirm.

## Execution Heuristic

Use this mental loop throughout the session:

1. What is the surface?
2. Do I understand the problem space well enough to prototype? (If not → Phase 2)
3. Am I about to make a directional choice? (If yes → Propose-Choose-Proceed)
4. What is the smallest artifact that makes it real enough to critique?
5. What did the user react to?
6. What contract does that reaction imply?
7. What is the next thin slice inward?

## End of Session Protocol

Before ending a session:

1. Update the decision log with any new decisions.
2. Update gate checklist with current status.
3. Update hardening status.
4. Commit state files only if the user asks for a commit or the repo workflow requires it.
5. Report summary: what was accomplished, what gate you're at, what comes next.
