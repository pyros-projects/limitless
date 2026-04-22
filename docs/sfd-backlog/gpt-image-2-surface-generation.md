# GPT-Image-2 and the Generalization of the Surface Step

**Created:** 2026-04-22
**Trigger:** OpenAI released GPT-Image-2 / ChatGPT Images 2.0 on 2026-04-21. Live-tested in-session on grindhouse (Phase 3 ingest pipeline data-flow diagram, via Codie on Codex).
**Status:** Proposal for SFD v0.7 amendments. Not yet merged into the whitepaper or the skill.

**See also:** `docs/sfd-backlog/gpt-image-2-surface-generation-codie-addendum.md` for Codie's follow-up take on where image-generated surfaces should and should not carry methodological weight.

---

## TL;DR

A new image model (GPT-Image-2) makes the surface-generation step of SFD ~100× cheaper than it was a week ago, *and* extends the set of artifacts that qualify as a "surface" far beyond UI mockups. Three-pole prototyping — previously aspirational because of cost — is now the cheap default. And the longstanding SFD MOC gap *"how does SFD handle backend-heavy features with minimal surface?"* closes, not by changing the methodology, but by expanding what counts as an evaluable surface.

This doc captures the reasoning so the whitepaper (currently v0.6) and the `limitless:surface-first-development` skill can be updated coherently.

---

## What changed on 2026-04-21

OpenAI shipped GPT-Image-2 (ChatGPT Images 2.0). The capability delta that matters for SFD:

- **~99% typography accuracy.** Dense small text, labels, tab names, command aliases — all render legibly. Old image models produced fake-looking glyphs in UI mockups; this one produces UIs where every label is a real word.
- **Reasoning mode.** The model "thinks" before it generates. Compositions, information architecture, decision branching in diagrams — all produced with deliberate structure, not pattern-matched noise.
- **Web search during generation.** The model can look up framework docs, real UI screenshots, algorithm references, product comparisons before committing to a layout. This closes the old failure mode "mockup looks great, fights the framework you plan to implement in."
- **Up to 8 images per prompt with character/object continuity.** Multiple distant design variants in one call, while staying in the same visual universe (so comparison is meaningful).
- **~30 seconds per image.**

Pricing and API availability are downstream concerns. The capability is in ChatGPT today, and via Codex (the `gemini-imagegen` skill is Gemini's equivalent; Codex's imagegen skill uses GPT-Image-2).

## Why this matters for SFD specifically

The SFD insight graph says, in three different ways, that the surface step is the hinge:

- [[Recognition is cognitively cheaper than generation...]] — humans should evaluate proposals, not write specs. But someone has to generate the proposal.
- [[The generation effect means critique-based iteration produces deeper stakeholder understanding...]] — the critique happens *on* a concrete surface. No surface, no critique.
- [[SFD effectiveness scales with AI model capability in a way no prior methodology does]] — proposal quality is one of the two axes this scales on.

And it records the core tension:

> *"Prototype concreteness enables evaluation but creates anchoring bias toward first proposals"* — concreteness is both SFD's mechanism and its main failure mode.

Codie's 2026-03-05 lesson is the canonical mitigation: **prototype three genuinely distant design poles** — vary hierarchy, interaction model, emotional tone, not just skin. And the 2026-04-01 Stitch lesson is the companion rule: **screen-led, not token-led** — let the first successful surface pull the design system into existence.

Both of those rules describe what good surface generation looks like. The problem has always been cost. Three distant poles plus screen-led iteration is expensive in human-designer time, expensive in Stitch token-spend, expensive in Figma-wrangling, and historically poor quality from LLM-generated HTML (outputs collapse into the same generic SaaS-dashboard shape regardless of prompt variance).

GPT-Image-2 attacks the single biggest economic barrier here. Three distant poles in one prompt, 30s per image, with continuity so comparison is meaningful. The anti-anchoring mitigation is now cheaper than skipping it.

## The bigger claim: "surface" generalizes beyond UI

This is the update that actually matters.

The SFD foundations — recognition-over-generation, generation effect, propose-react-iterate — don't require the surface to be clickable. They require the surface to be **evaluable**: concrete enough that a stakeholder can react to it cheaply.

UI mockups were the historically-dominant surface type because they were the only artifact cheap to produce *and* legible to non-specialists. Other evaluable artifacts — architecture diagrams, data-flow charts, ERDs, sequence diagrams, state machines, algorithm explainers, infographics — required skilled drawing work. That cost made them impractical as iteration surfaces.

GPT-Image-2 makes all of those roughly uniform in cost. Live evidence: the model produced a legitimate "How Transformers Work" infographic — correct block topology (MHA → Add & Norm → FFN → Add & Norm), real Q/K/V labels, a similarity-score matrix in the right shape, a softmax output distribution bar chart, "stacked L times" semantics — from a single prompt. That's not a pretty picture; that's a pedagogical surface that a reader can recognize-or-reject their mental model against.

**Concrete extension of the "surface" category:**

| Artifact type | Stakeholder evaluates | Previously cheap to produce? |
|---------------|----------------------|------------------------------|
| UI mockup | Whether the flow matches user intent | Yes (Stitch, Figma, hand-written HTML) |
| Architecture diagram | Whether the system shape matches requirements | No — hours of drawing |
| Data-flow diagram | Whether the pipeline stages match what's needed | No |
| ERD | Whether entity relationships match the domain | Partial (dbdiagram, Mermaid) |
| Sequence diagram | Whether a protocol or handshake is correct | Partial (Mermaid) |
| State machine | Whether the lifecycle matches the product | No |
| Algorithm explainer | Whether a computation is conceptually right | No — requires skilled illustrator |
| Infographic | Whether a conceptual model transfers cleanly | No — hours |
| Slide/whiteboard content | Whether design intent is communicable | No — reviewer time |

Every row in the "no" column just moved to "30 seconds." That's the capability jump.

## What this closes in the insight graph

1. **The "backend-heavy features with minimal surface" MOC gap.** The gap was: a pure-backend feature has no UI, so SFD has no cheap evaluable surface, so SFD doesn't apply. The resolution: the surface doesn't have to be UI. A data-flow diagram of an ingest pipeline, an ERD of a schema change, a state-machine of a clip lifecycle — any of these is an evaluable surface for a headless feature. The methodology doesn't change; its applicable domain expands.

2. **The speculative [[SFD effectiveness scales with AI model capability...]] insight gets a data point.** The prediction was: better models → closer first proposals → fewer convergence iterations. GPT-Image-2 is a clean test of the *proposal-quality* axis. The grindhouse mockups (TUI dashboard, GUI catalog, non-interactive CLI) generated from two-sentence prompts are evidence the prediction holds on the specific axis SFD cares most about. The insight can be promoted from "speculative" toward "working-confidence."

3. **The 2026-04-17 Flock failure mode partly resolves.** The Flock incident documented: "contract approval can pass Gate 1+2 with architectural errors that only surface during deeper implementation research." A material chunk of those errors are architectural — missing entity relationships, wrong component boundaries, broken data-flow assumptions. If the stakeholder reacts to the architecture diagram at surface-convergence time, not just the UI, Gate 1 catches structural errors the UI-only surface misses. Not a full fix. But the window of "errors that only surface downstream" shrinks.

4. **"Screen-led, not token-led" gets a proper engine.** Stitch was cheaper than Figma but still token-aware underneath. GPT-Image-2 is purely screen-led — it produces pixels of proposed screens, not component trees with tokens. You derive the design system *afterward*. That's the Stitch lesson executed without Stitch's residual token-awareness.

5. **Recognition-over-generation works harder.** Historically: "evaluate one proposal with residual anchoring risk." Going forward: "evaluate N alternatives side-by-side, where recognition is actually doing its thing." The generation-effect critique loop stays intact but operates on comparison — which is what humans are good at.

## Proposed SFD amendments (v0.7)

### 1. Extend the definition of "surface"

The whitepaper's current framing is UI-leaning. The v0.7 amendment should explicitly state:

> A **surface** is any concrete artifact a stakeholder can evaluate through recognition. UIs are the prototypical example, but architecture diagrams, data-flow charts, ERDs, sequence diagrams, state machines, and algorithm explainers all qualify. The choice of surface type is driven by what the stakeholder can meaningfully critique, not by what's visible to an end user.

This unlocks SFD for backend-heavy, library-design, and protocol-design features where the previous framing didn't obviously fit.

### 2. Three-pole prototyping becomes the default (not an aspiration)

Previously: "prototype three genuinely distant design poles" was a strong Codex lesson, honored when the team could afford it.

Going forward: three poles are the default. The skill should generate three pole candidates (via image model or otherwise) unless the agent explicitly argues monoculture — e.g., the surface is fully determined by external constraints (regulation, existing brand, integration requirement) and genuine variance isn't possible.

The anti-anchoring mitigation is now economically trivial. Skipping it should require justification, not effort.

### 3. Surface State Inventory becomes a pixel-checklist

Currently: the SSI is a 10-category convergence checklist the agent works through.

Going forward: the SSI is a checklist the agent applies *against a concrete artifact* (the mockup / diagram / infographic). For each category, the agent checks whether the artifact covers it — "does this mockup show empty states?", "does this diagram show error paths?", "does this ERD show inheritance?". The inventory stays load-bearing; the thing being inventoried becomes concrete instantly.

### 4. Design-system derivation moves downstream

Currently: design-system tokens (palette, typography, spacing, component rules) are often produced alongside or before mockups.

Going forward: mockups come first. Tokens get extracted *from* the converged mockup as a downstream artifact. This is the 2026-04-01 Stitch lesson ("screen-led, not token-led") made into the default rather than a workaround.

This is also where the implementing agent (Claude or similar) still earns significant keep — turning pixels into a real, implementable design-system doc is a different job from generating pixels.

### 5. Surface generation integrates web search when available

The skill should instruct the agent to use framework docs, competitor screenshots, algorithm references during surface generation *before* proposing the first mockup. For UI surfaces: pull the target framework's component catalog. For data-flow surfaces: read the actual pipeline code. For architecture surfaces: consult reference implementations.

This directly attacks the old failure mode "mockup fights framework reality" — the Flock-incident class of contract errors.

### 6. Surface convergence remains human-in-the-loop

This is the important non-change. GPT-Image-2 generates *candidate* surfaces, not *converged* surfaces. Convergence still requires recognition-based human critique. The economics shifted; the methodology shape did not.

Empirical evidence from the live test: the model produced a data-flow diagram of grindhouse's ingest pipeline that was ~75–80% accurate against the real code — *under conditions where it had no code access, only a prose summary*. With code access (via `codex:rescue`), accuracy should be meaningfully higher. But even under ideal conditions, the convergence pass catches semantic simplifications and local hallucinations that only a reader who knows the system can spot.

The lesson: the capability is strong enough to produce surfaces worth critiquing. It is not strong enough to skip the critique.

## Specific workflow insertion points

### In the SFD skill (`limitless:surface-first-development`)

- **Phase 1 (Identify the Surface):** add "choose surface type" step — UI, data-flow, architecture, ERD, sequence, state, infographic — based on what the stakeholder can critique.
- **Phase 2 (Generate Proposals):** default to N=3 distant poles via image model. Prompts should vary on *structural* axes (hierarchy, interaction model, information density, emotional tone), not just palette.
- **Phase 3 (Iterate to Convergence):** the critique ladder stays; the artifact type it operates on is now broader.
- **Phase 4 (Derive Contract):** the contract is still extracted from the converged surface. Nothing changes here.

### In Spec Kit (e.g., GitHub's `speckit` framework)

Insert a mockup-generation step between `/speckit.plan` and `/speckit.tasks` for any UI-bearing or architecture-bearing phase. Tasks then key off the chosen mockup ("implement the detail panel as shown in `mockups/browse-v2.png`") rather than off freeform plan prose. This sharpens task specification and closes the feedback gap that produced grindhouse's Phase 3.1 retrofit.

### For backend features in any SFD-driven project

Before writing code for a pipeline, protocol, data model, or algorithm:

1. Generate three candidate data-flow (or sequence, or ER, or state-machine) surfaces.
2. Pick one.
3. Derive the contract from the chosen surface.
4. Implement toward the contract.

This is SFD-for-backend that wasn't practical before.

## Evidence base and caveats

**Grounded evidence:**
- Grindhouse Phase 3.1 scar: the CLI design system was added as a feedback iteration *after* Phase 3 implementation because dogfooding found the CLI had no personality. In a GPT-Image-2 world, the CLI mockup is generated pre-Phase-3 and implementation targets it. The scar is a permanent receipt that the old surface-generation step had a hole for non-UI-but-visual artifacts (like CLI output).
- Live test 2026-04-22: Codie generated a grindhouse ingest-pipeline data-flow diagram. Brand-consistent, information-dense, ~75–80% semantically accurate against the real code. Full gap analysis in `/home/pyro/projects/private/spec-test/specit/grindhouse/specs/001-video-dataset-management/mockups/grindhouse-ingest-pipeline-data-flow-diagram-v1.png`.
- Same session produced three coherent grindhouse UI surfaces (TUI dashboard, GUI catalog manager, non-interactive CLI pipeline log) from two-sentence prompts with no design-system input.

**Important caveat on the live test:** Codie was invoked through the `chat-codie` skill, which explicitly blocks code access ("Do NOT analyze the repository, read files, or investigate code"). The 75–80% accuracy figure is therefore measuring "how faithfully does the model render a human's text description of the code," not "how accurately can it generate an engineering surface from a real codebase." For a proper capability measurement, `codex:rescue` (which has file-read access) should be used. The accuracy floor with code access is expected to be meaningfully higher.

**Open empirical questions:**
- How many regeneration cycles does the model need, on average, to reach stakeholder sign-off on a surface?
- Does the error pattern in missed details cluster (model is systematically weak on certain semantic structures) or scatter (errors are essentially random)?
- How does three-pole generation affect final convergence quality vs. single-pole + iteration?
- Does the extended "surface" category (non-UI) achieve the same generation-effect critique quality as UI-mockup-based SFD?

These are measurable on grindhouse and on any future project using the updated SFD skill.

## Proposed next actions

1. **SFD whitepaper update.** Draft v0.7 incorporating the above amendments. Target: within the week that this doc was written.
2. **SFD skill update.** Update `plugins/limitless/skills/surface-first-development/SKILL.md` with the new default (three poles), the expanded "surface" definition, and the image-model integration point.
3. **Update the insight graph.** Promote [[SFD effectiveness scales with AI model capability...]] from speculative toward working-confidence. Add a new insight: *"Image models with reasoning and web search generalize SFD beyond UI surfaces to any evaluable visual artifact."* Link it to the MOC and to the Codex three-poles lesson.
4. **Grindhouse follow-through.** Generate three-pole data-flow proposals for Phase 5 (Caption) and Phase 6 (Browse) before implementation. Treat the resulting mockups as first-class spec artifacts.

## One-line summary for the whitepaper index

> SFD v0.7 amendment: the surface step generalizes from UI mockups to any evaluable visual artifact, and three-pole prototyping becomes the default — both enabled by GPT-Image-2's reasoning, web-search, and multi-image generation capabilities shipped 2026-04-21.
