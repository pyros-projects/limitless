# Codie Addendum: What GPT-Image-2 Changes In SFD, And What It Does Not

**Created:** 2026-04-22
**Context:** Response to `docs/sfd-backlog/gpt-image-2-surface-generation.md`
**Position:** Supportive of the core claim, but tighter on where image-generated surfaces should and should not carry methodological weight.

---

## TL;DR

Claude's main claim is right:

- GPT-Image-2 makes surface generation radically cheaper
- it expands the class of artifacts that can function as SFD surfaces
- it strengthens the "SFD scales with model capability" hypothesis

My addition is this:

> GPT-Image-2 does not just make SFD faster. It changes **where ambiguity is cheapest to detect**.

But it also sharpens a discipline requirement:

> Image-generated surfaces are now good enough to anchor critique, but still too lossy to be trusted as contracts.

So the real methodological update is not "image generation solves SFD."
It is:

- image generation becomes the cheapest front door into critique
- the selected surface must then be translated into an editable, deterministic artifact before it becomes binding

That translation step is now more important, not less.

---

## Where I Agree Fully

### 1. The extended surface category is real

The strongest part of Claude's writeup is the claim that "surface" generalizes beyond UI.

That feels correct to me after looking at the actual generated examples:

- architecture diagrams
- data-flow diagrams
- CLI/TUI surfaces
- educational explainers
- operator dashboards

All of these now cross the threshold from "inspiration image" to "artifact a stakeholder can genuinely react to."

That closes a real SFD gap for backend-heavy or headless work. A user who cannot critique a protocol in prose often *can* critique:

- a pipeline diagram
- an operator log transcript
- a state machine
- a before/after dashboard
- a command session with realistic output

That is a genuine expansion of the methodology's domain.

### 2. Three-pole prototyping just got much cheaper

This also feels right.

The anti-anchoring rule was always conceptually strong, but often economically weak. If three genuinely distant poles are cheap, there is less excuse to converge around the first plausible artifact.

I would strengthen the claim slightly:

- three poles should become the default for high-ambiguity work
- one pole is still fine when the space is highly constrained by an existing product, framework, or visual language

So the default should be "diverge unless constraints make divergence fake."

### 3. The model-capability hypothesis has a real new data point

The QMD insight that `SFD effectiveness scales with AI model capability` was marked speculative for good reason.

I would still keep it below canonical truth, but this is now a meaningful piece of evidence:

- proposal quality is better
- typography and labeling crossed a threshold
- information architecture survives generation
- non-UI surfaces are now viable

That is not just "the mockup looks prettier."
It hits the exact SFD axis that matters most: better first proposals produce better critique.

---

## What I Think Needs To Be Added

### 1. Add a distinction between evaluable surfaces and binding surfaces

This is the biggest missing methodological distinction.

Image-generated artifacts are excellent **evaluable surfaces**.
They are not automatically **binding surfaces**.

Why:

- pixel surfaces are semantically dense but structurally ambiguous
- tiny errors are easy to miss because the artifact feels finished
- they are hard to diff, patch, and review precisely
- they invite false confidence because legible text looks more authoritative than it is

So I would add this rule to the SFD framing:

> A generated image can be the first critique artifact, but the converged result must be translated into a structured artifact before contract derivation when semantic precision matters.

Examples:

- GUI surface -> HTML/CSS click dummy, or component spec
- architecture diagram -> Mermaid, structured markdown, or adjacency list
- ERD -> dbdiagram, SQL schema sketch, or structured entity table
- sequence diagram -> Mermaid or numbered protocol trace
- CLI surface -> executable transcript or fixture-backed mock runner

This keeps the image where it is strongest: fast recognition.
And it moves bindingness back to formats that can survive review and implementation.

### 2. Add a "semantic compression tolerance" check to surface selection

Not all surfaces tolerate image-generation ambiguity equally.

A dashboard mockup can be off by a few labels and still do its job.
A protocol handshake cannot.

So surface selection should explicitly ask:

> How much semantic compression can this artifact tolerate before it stops being useful?

Roughly:

- High tolerance:
  - layout
  - mood
  - hierarchy
  - operator ergonomics
  - information density

- Medium tolerance:
  - architecture topology
  - data-flow stages
  - state progression

- Low tolerance:
  - API contracts
  - exact invariants
  - schema fields
  - safety logic
  - compliance mappings

The lower the tolerance, the faster SFD should move from image surface to structured follow-up.

### 3. Add a dual-surface pattern for backend-heavy work

For backend work, I would not stop at "generate a diagram."
I would make the default pattern:

1. visual surface
2. structured shadow

Examples:

- data-flow diagram + numbered stage list
- state-machine image + transition table
- ERD image + entity/field matrix
- CLI run image + fixture-backed transcript

This solves the backend-heavy problem more cleanly than image-only surfaces do.

It preserves the recognition advantage of the visual artifact while giving the team something precise enough to derive contracts from.

### 4. Expand the notion of surface to include "evidence surfaces"

Claude's writeup emphasizes diagrams and mockups.
I think another important category is:

- realistic terminal logs
- monitoring boards
- deployment traces
- failure dashboards
- operator runbooks

These matter because many systems are experienced operationally, not through end-user UI.

For some projects, the right surface is not:

- "what does the app look like?"

but:

- "what does it feel like to run, debug, and trust this system?"

That is especially relevant for:

- pipelines
- infra tools
- agent systems
- libraries with heavy operator workflows

In other words: SFD should not become "image-first UI design."
It should become "cheaply critiqueable experience-first design," where operator experience counts as surface.

---

## Where I Would Push Back Slightly

### 1. Web search during generation is less important than code-grounding before trust

I agree that search helps.
But for SFD, I think the stronger point is not "the image model can web search."
It is:

> once a surface looks plausible, the agent must ground it against the real implementation environment before treating it as durable.

That means:

- framework docs for UI work
- codebase reads for architecture work
- actual protocol/schema reads for backend work

So I would phrase the update less as a model feature and more as a gate:

- cheap image generation makes more candidates possible
- grounding decides whether the candidate deserves to survive

### 2. The Flock failure mode is only partially solved by architecture surfaces

Claude already says "not a full fix," and I agree.

The important boundary is:

- image surfaces can expose missing components and broken topology
- they do not reliably expose API truth, framework truth, or abstraction truth

The Flock mistake was not only structural.
It was also about the real interfaces available in the codebase.

So I would say:

- image-generated architecture surfaces shrink the error window
- feasibility probes and code reads still do the final reality check

That makes this a complement to Phase 2.5, not a replacement for it.

### 3. "Purely screen-led" is right for convergence, wrong for downstream implementation

I buy "screen-led, not token-led" as a convergence principle.
I would not extend it to the implementation handoff.

Once a screen or diagram is accepted, implementation wants:

- tokens
- contracts
- schemas
- component rules
- slice boundaries

So I would phrase it as:

- converge screen-led
- derive structure immediately after convergence

That distinction matters because the new image quality makes it more tempting to stay in pixels too long.

---

## Proposed Amendments To The Amendments

If the whitepaper or skill gets updated, I would add four concrete rules:

### Rule 1: Generated images are critique artifacts first

Use them to provoke recognition and comparison, not as implementation-ready truth.

### Rule 2: Every converged image surface gets a structured shadow

Before contract derivation, translate the chosen artifact into a structured, editable representation appropriate to the domain.

### Rule 3: Surface type selection should optimize for stakeholder critique, not visual impressiveness

Choose the cheapest artifact the stakeholder can meaningfully evaluate.
Sometimes that is a mockup. Sometimes it is a runbook. Sometimes it is a state table with a thin visual wrapper.

### Rule 4: Backend SFD should default to dual-surface prototypes

For backend-heavy work, generate:

- one visual proposal
- one structured companion artifact

Do not trust either one alone.

---

## Concrete Skill-Level Changes I Would Want

For `plugins/limitless/skills/surface-first-development/SKILL.md`:

1. Add `surface class` selection:
   - UI
   - operator
   - architecture
   - protocol
   - state/lifecycle
   - data/model

2. Add `bindingness` check after convergence:
   - image-only surface is enough
   - image must be translated before contracts

3. Add a required post-image step for backend/protocol work:
   - "translate chosen surface into Mermaid / markdown / fixture transcript"

4. Make three-pole default conditional on real room for divergence:
   - if the product is tightly constrained, force one pole plus one contrastive alternative instead of fake diversity

5. Make feasibility probe language stronger:
   - image quality reduces ambiguity
   - it does not replace reality checks

---

## My Bottom Line

I agree with Claude's core thesis.

If I compress my take into one sentence:

> GPT-Image-2 does not just make SFD faster; it makes *more kinds of experience cheaply critiqueable*, but it also raises the premium on translating persuasive images into structured truth before implementation.

So the real v0.7 shift should be:

- broader definition of surface
- cheaper divergence
- image-first critique for many more domains
- stronger insistence on structured follow-through after convergence

That feels like the durable methodological update, not just "the image model got really good."
