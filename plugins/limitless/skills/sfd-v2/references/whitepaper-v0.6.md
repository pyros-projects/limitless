# Surface-First Development

## A Methodology for AI-Assisted Software Creation

**Authors:** Pyro, Claude (Anthropic), Codex (OpenAI)
**Date:** February 8, 2026
**Status:** Draft v0.6

---

## Abstract

Traditional software development methodologies, from waterfall to agile, share a common assumption: development flows from abstract specification toward concrete implementation, typically beginning with backend infrastructure and culminating in user-facing surfaces. This ordering exists not because it produces optimal results, but because the cost of producing a working prototype has historically been too close to the cost of building the real system. In building design, where a sketch costs effectively nothing compared to construction, a surface-first ordering has been standard practice for centuries.

With AI coding agents capable of generating working prototypes at near-zero marginal cost, software's prototype-to-product cost ratio has collapsed by orders of magnitude, approaching the ratio that made surface-first development the obvious default in building design. This paper formalizes **Surface-First Development (SFD)**: a methodology that begins with a working prototype of the outermost interaction layer (UI, CLI, API consumer experience, or operator workflow), iterates that surface to convergence, derives contracts and invariants, and builds inward through vertical slices and progressive hardening.

SFD is grounded in a well-established cognitive asymmetry: humans are better at evaluating concrete proposals than specifying complete systems in advance (Mandler, 1980; Kahneman, 2011). This same asymmetry explains why building design has followed a surface-first ordering for centuries -- converging the experiential design before engineering the structure (AIA, n.d.). We present the methodology, its cognitive and economic foundations, the cross-domain precedent from architectural practice, explicit process gates, a hybrid testing strategy, and measurable evaluation criteria so SFD can be tested empirically rather than adopted as doctrine.

---

## 1. The Problem with Specification-First Development

Every mainstream software development methodology treats specification as the primary creative act. In waterfall, this manifests as comprehensive requirements documents. In agile, it takes the form of user stories and acceptance criteria. In domain-driven design, it appears as ubiquitous language and bounded contexts. The format changes; the underlying assumption does not: someone must describe what the software should do before anyone builds it.

This creates a failure mode that the industry has spent decades trying to mitigate. Specifications are authored in a state of maximum ignorance, before the act of building reveals what the actual problems and opportunities are. The result is predictable:

- Specifications that are too vague to guide implementation, or
- specifications that are detailed but misaligned with user reality.

The Standish Group's CHAOS reports have documented this pattern since 1995, consistently finding that a significant proportion of software projects fail or are challenged, with misaligned requirements among the leading causes (Standish Group, 1995). The specific figures in the CHAOS reports have been contested on methodological grounds (Eveleens & Verhoef, 2010), but the directional finding -- that requirements misalignment is a persistent and costly failure mode -- is consistent with broader empirical evidence. Boehm and Papaccio (1988) demonstrated that the cost of correcting requirements errors increases by orders of magnitude when detected late in development rather than early, establishing the economic case for earlier validation.

Agile improved this by shortening feedback loops. It helped, but it did not eliminate the fundamental burden: the human still has to imagine the system before interacting with it. The entire evolution from waterfall to agile was really an argument about *how often* to synchronize intent with reality, not about whether the specification-first ordering is optimal.

The standard response to this criticism is prototyping. Build something rough, learn from it, throw it away, build the real thing. The software industry has known since at least the 1980s that prototyping produces better outcomes than pure specification (Floyd, 1984). Boehm's spiral model (Boehm, 1988) explicitly incorporated prototyping as a risk-reduction strategy, recognizing that interactive exploration reveals requirements that static analysis cannot.

The reason prototyping never became the default starting point is economic, and it can be reduced to a single variable: the **prototype-to-product cost ratio (PPR)**.

We define PPR operationally as:

> **PPR = (effort to produce a testable surface prototype) / (effort to reach a production release that meets hardening criteria)**

When PPR is low -- when producing a working surface prototype costs a negligible fraction of shipping the real system -- starting with that prototype is obviously efficient. When PPR is high -- when the prototype costs nearly as much as the real thing -- specification-first becomes a rational adaptation, because a text document is the only artifact cheap enough to start with.

Building design has followed a surface-first ordering for centuries. An architect sketches the building on a napkin, iterates with the client, converges the experiential design, and only then hands it to a structural engineer to figure out how to make it stand up. Nobody has ever suggested reversing this process -- calculating structural load tables before knowing what the building looks like. The reason is obvious: the napkin costs nothing. PPR in building design is orders of magnitude below 1. At that ratio, starting with the surface is not just viable, it is the only sane approach.

Software never had a napkin. A working prototype -- a click dummy, a functional CLI simulation, example API consumer code -- used to require substantial engineering effort, often comparable to building the first version of the real system. PPR was high enough that "prototype first" meant building the system nearly twice. The industry rationally chose specification-first, not because specifications are good (everyone knows they are not), but because a Word document was the only artifact cheap enough to start with.

The entire history of specification-first software development was an adaptation to a cost ratio, not a discovery of the optimal process.

AI coding agents have collapsed this ratio by orders of magnitude. A functional surface prototype can now be generated in minutes rather than weeks. Current AI models demonstrate non-trivial software engineering capability across standardized benchmarks (Jimenez et al., 2024; Chen et al., 2021), and this capability is improving rapidly. Whether PPR has collapsed enough for SFD to outperform specification-first in a given project class is an empirical question -- and the evidence framework in Section 10 provides a way to measure it. But the directional shift is clear: software development now has its napkin, and with it, the ability to adopt the same process ordering that building design has validated for millennia.

---

## 2. Prior Art and Differentiation

### 2.1 README-Driven Development (RDD)

Coined by Tom Preston-Werner (GitHub co-founder) in 2010, RDD proposes writing the README before any code (Preston-Werner, 2010). Preston-Werner explicitly distinguished it from Documentation-Driven Development, arguing that a README is the "minimum viable documentation": just enough to clarify what you are building without the overhead of comprehensive specification.

SFD shares RDD's philosophy: start with the consumer experience. But where RDD produces a static text document, SFD produces a working interactive artifact. A README requires the author to imagine the consumer experience and describe it in prose. An SFD surface prototype *is* the consumer experience, generated by an AI and iterated through direct interaction. This distinction matters because it shifts the cognitive task from generation (hard) to recognition and critique (easier), a distinction grounded in dual-process theory (Kahneman, 2003).

### 2.2 Outside-In TDD (London School)

Outside-In TDD starts from the outermost layer of the application and writes failing tests that drive implementation inward. Freeman, Pryce, Mackinnon, and Walnes (2004) formalized this approach, and Freeman and Pryce (2009) expanded it into a complete methodology in *Growing Object-Oriented Software, Guided by Tests*. It shares SFD's directional principle: build from the outside in.

The difference is in the starting artifact. Outside-In TDD starts from a *test* of user behavior. SFD starts from a *working simulation* of user behavior. A test asserts "when the user clicks X, Y should happen." A surface prototype lets the user actually click X and see what happens, then decide whether Y was the right outcome. Tests can be derived from a converged surface prototype, but they are not the starting point.

### 2.3 Design Thinking and UX Prototyping

The design thinking movement, formalized by Brown (2008) at IDEO and developed further at Stanford's d.school (Plattner, Meinel, & Leifer, 2011), has long advocated for rapid prototyping and user testing. SFD extends these principles into the full engineering lifecycle by reducing handoff loss: prototype artifacts are intended to evolve into production systems through progressive hardening, rather than being discarded and rebuilt.

### 2.4 Agile and Lean Discovery

SFD is compatible with discovery-focused agile practices. It does not reject iterative planning; it reorders implementation emphasis so convergence of user-visible behavior happens earlier and more concretely than traditional sprint-based discovery typically achieves.

### 2.5 Building Design: The Oldest Surface-First Discipline

The strongest precedent for SFD comes from outside software entirely. The design and construction of physical buildings has followed a surface-first ordering for centuries, formalized today in the American Institute of Architects' five standard phases of design services: Schematic Design, Design Development, Construction Documents, Bidding, and Construction Administration (AIA, n.d.).

The parallels to SFD are remarkably direct:

**Schematic Design is surface prototyping and iteration.** In the first design phase, the architect produces sketches, floor plans, 3D models, and renderings -- not to solve structural problems, but to make the building's spatial and experiential qualities tangible enough to evaluate. The client interacts with these artifacts, reacts, critiques, and the architect iterates until a direction is agreed upon. As practitioners describe the process: the architect presents ideas using "images of other projects, hand sketches, and models to help visualize the size, shape, and relationship of spaces," then listens, observes client reactions, and refines accordingly. This is Phase 2-3 of SFD -- generate a surface proposal, iterate to convergence through critique -- applied to physical space rather than software interfaces.

**Convergence is a formal gate before deep engineering begins.** The schematic design phase concludes with an explicit client sign-off before the project proceeds. If multiple design options were explored, one must be chosen before moving forward. The structural engineer's job is not to dictate the shape of the building but to figure out how to make the converged shape stand up. This is precisely the SFD principle of deriving contracts from converged surface behavior: the engineering requirements are derived from the design, not the other way around.

**Engineering feedback can begin during surface iteration without breaking the surface-first ordering.** In practice, especially for complex buildings, structural and MEP (mechanical, electrical, plumbing) engineers are often consulted during schematic design -- to sanity-check structural spans, verify that floor plates can accommodate mechanical systems, flag code risks, and provide early cost feedback. This does not make the process backend-first. The engineering input constrains and informs the surface without dictating it, unless safety or compliance makes a constraint non-negotiable. SFD should adopt the same principle: performance envelope checks, security threat modeling, data lifecycle constraints, and concurrency model sanity checks can and should begin during surface iteration, but they constrain rather than drive the surface design.

**The cognitive rationale is explicitly acknowledged.** Architects know that schematic design is the cheapest time to make changes. The design is malleable and no specifications have been determined. As the process progresses, changes become more difficult and more expensive. This mirrors the cost-of-change argument for SFD: converge the surface early, when changes are cheap, before engineering commitments make changes expensive.

**Progressive hardening is the standard workflow.** The subsequent phases -- Design Development, Construction Documents, Construction Administration -- progressively add engineering reality to the converged form. In Design Development, structural, mechanical, electrical, and plumbing systems are designed to support the approved schematic. In Construction Documents, every detail is specified with full precision. The building is not redesigned from scratch when the structural engineer arrives; it is hardened. Sketches become dimensioned drawings become construction specifications -- exactly as an SFD surface prototype becomes a real system through vertical slices and progressive hardening.

**The phase ordering exists for the same cognitive reason.** Architects discovered centuries before cognitive psychology formalized the insight that clients are far better at evaluating a proposed spatial experience than they are at specifying one from scratch. A client who cannot draw a floor plan can immediately tell you that a room feels too small, that the kitchen should face the garden, or that the entrance lacks presence. Recognition and critique are natural; generation from nothing is not. Architectural practice exploits this asymmetry by defaulting to "here is a proposal, react to it" rather than "describe what you want in writing."

The key difference between building design and software development is PPR (see Section 1). Buildings always had an extremely low PPR: a sketch costs effectively nothing compared to construction. Software's PPR was historically high enough that a working prototype cost nearly as much as the real implementation. AI coding agents have collapsed software's PPR by orders of magnitude, which is why the same process ordering now becomes viable for software.

This cross-domain validation matters. The surface-first ordering is not an untested theoretical proposal. It is the standard practice of arguably the oldest engineering discipline on Earth, arrived at independently for the same cognitive and economic reasons that motivate SFD. The fact that software development historically followed a different ordering was never evidence that specification-first is superior -- it was evidence that software's PPR was too high.

---

## 3. The Cognitive Foundation

SFD is grounded in a well-established cognitive asymmetry: humans are significantly better at evaluating concrete proposals than they are at generating abstract specifications from scratch.

This asymmetry has been studied extensively in cognitive psychology. Mandler (1980) demonstrated that recognition and recall operate through fundamentally different cognitive processes, with recognition being significantly less effortful than recall. Tulving (1985) extended this through the theory of synergistic ecphory, showing that memory retrieval (and by extension, evaluation) is strongest when triggered by concrete cues rather than abstract prompts. In the context of software requirements, this means that a working prototype serves as a powerful retrieval cue for what the stakeholder actually wants.

Kahneman's (2011) dual-process framework provides additional theoretical grounding. System 1 (fast, intuitive) processes are well-suited for evaluating whether a concrete prototype "feels right." System 2 (slow, deliberate) processes are required for generating complete specifications from scratch. SFD restructures development to leverage System 1 for the creative steering function and reserves System 2 for the technical implementation work where deliberate analysis is genuinely needed.

This asymmetry is observable across domains. An art director who cannot paint can reliably distinguish good work from bad. A music listener who cannot compose can identify when a melody feels wrong. A user who cannot write requirements documents can immediately tell you that a prototype does not match what they need. Recognition, evaluation, and critique are cognitively cheap operations. Generation from nothing is expensive and error-prone.

A related phenomenon is the generation effect (Slamecka & Graf, 1978): information that is actively generated is better remembered and understood than information passively received. In SFD, the stakeholder's critique-and-redirect interaction with the prototype is itself a form of generation, meaning the resulting design decisions are more deeply understood by the stakeholder than decisions recorded in a specification document they merely read and approved.

Traditional development methodologies force the expensive operation: "Write down what you want before we build it." SFD restructures the process around the cheap operation: "Here is a concrete proposal. Does this match what you want? No? What is wrong with it?"

This restructuring is only viable when PPR is low enough (see Section 1). Historically, software's PPR was too high -- building a working prototype required nearly as much effort as building the final product. AI coding agents have collapsed PPR by orders of magnitude, making proposal generation cheap enough to be the default starting point rather than a luxury.

The iteration loop in SFD:

1. Human provides rough intent (natural language, informal).
2. AI generates a working surface prototype.
3. Human evaluates the prototype through direct interaction.
4. Human provides critique ("not like this, more like that").
5. AI regenerates or modifies the prototype.
6. Repeat until convergence.
7. Derive contracts and invariants from the converged surface.
8. Build internals to support the converged surface.

At every step, the human performs evaluation and direction rather than exhaustive specification. The AI handles generation, which is the task it is increasingly good at. The result is a division of cognitive labor that plays to the strengths of each participant.

---

## 4. The Methodology

### 4.1 Identify the Surface

The first step is to determine what the end-user actually interacts with. This determines the type of prototype. The general principle: **the surface is whatever the end-user (human or system) directly touches.**

| Product Type | Interaction Surface | Prototype Form |
|---|---|---|
| Web/mobile application | GUI | Click dummy (HTML/React/native shell) |
| CLI tool | Terminal interaction | Scripted session / executable prototype |
| API / Library | Consumer code experience | Example integration code |
| Data pipeline | Operator workflow | Runbook + simulated observability |
| Agent / Automation | Trigger-to-outcome chain | Scenario simulation |

For a REST API, the surface is not the endpoint definitions -- it is the experience of a developer writing code against those endpoints. For a CLI, it is not the argument parser -- it is the terminal session of a user accomplishing their task.

### 4.2 Generate a Surface Proposal

Provide the AI agent with a rough description of intent and constraints. The description should be informal and directional. Over-prescribing at this stage reintroduces the specification-first failure mode.

Example prompt styles:

- "Build me a click dummy for an app that lets teams track their weekly goals with clear overdue handling."
- "Show me what an ideal terminal session would look like for a tool that migrates database schemas with rollback paths."
- "Write the code a developer would write to integrate with this authentication service, including refresh and error handling."

The AI's output will be imperfect. That is by design. The purpose is not to get it right on the first try but to produce a concrete artifact that can be evaluated and critiqued.

### 4.3 Iterate to Convergence

Interact with the prototype directly. Click through the UI. Read the CLI transcript. Examine the example API consumer code. Identify everything that feels wrong, missing, or misaligned with your intent.

Convergence means: **stakeholders can walk through all critical flows without encountering unresolved behavioral mismatches.**

Key practices during iteration:

- **Critique behavior, not implementation.** Say "when I click this, I expect to see X" rather than "change the state management to use Redux."
- **Explore edge cases interactively.** "What happens if I enter nothing here?" is more productive than trying to enumerate edge cases speculatively.
- **Let the AI propose solutions.** When something feels wrong, describe the problem, not the fix. The AI may find a better solution than the one you would have specified.
- **Capture decisions and rejected alternatives.** Record why a particular approach was chosen over another. This context is valuable during hardening and for cross-session persistence.

### 4.4 Derive Contracts

After convergence, extract the contracts and invariants that the surface implicitly demands:

- **API contracts:** What endpoints, methods, payloads, and error shapes does the surface require?
- **Domain invariants:** What business rules must the backend enforce for the surface behavior to remain valid?
- **Non-functional requirements:** What latency, availability, or throughput does the surface experience require?
- **Acceptance criteria:** What specific behaviors constitute "working correctly" as demonstrated in the converged prototype?

This keeps specification as a derivative of validated behavior rather than a speculative precursor to it. The contracts are precise because they describe something that already exists and has been interactively verified, not something imagined. This approach directly addresses the cost-of-change curve identified by Boehm (1981): by grounding contracts in observed behavior rather than speculation, the probability of late-stage requirements corrections is reduced.

### 4.5 Build Inward with Vertical Slices

Implement via thin end-to-end slices from surface to data and infrastructure. Each slice makes one surface flow real -- from user interaction through domain logic to persistence and back. This preserves feedback velocity while avoiding a "pretty mock forever" trap.

Any implementation approach can be used within slices -- TDD, SpecDriven Development, or direct implementation. SFD's opinion is about what constrains the architecture (surface demands) and in what order work proceeds (outside-in), not about how internal code is written.

### 4.6 Progressive Hardening

Evolve the prototype toward production by replacing simulated components with real implementations:

1. Mock data -> real persistence
2. Placeholder auth -> real identity flow
3. Simulated behavior -> domain logic
4. Happy-path only -> robust error handling and validation
5. Baseline performance -> SLO-driven optimization

At each stage, the surface behavior that was validated during iteration is preserved. The user experience does not regress; it only gains real functionality behind what was previously simulated.

Progressive hardening is not always feasible. When the prototype's technical foundation is fundamentally incompatible with production requirements (e.g., a React click dummy for a system that must be native mobile), a clean reimplementation is necessary. But the converged surface still serves as an unambiguous behavioral reference.

---

## 5. The Surface as Product Anchor

In the strongest form of SFD, the surface is the permanent product anchor throughout the lifecycle:

**All changes flow outside-in.** When a feature is added or modified, the process begins at the surface: "How should this change look, feel, and behave for the user?" The surface prototype is updated first, iterated to convergence, and then internals are modified to support it. This prevents the common failure mode where backend changes subtly alter user experience in unreviewed ways.

**Architecture is permanently demand-driven.** No internal component exists unless the surface requires it. This is not merely a starting principle (like YAGNI); it is enforced continuously because every change starts at the surface and flows inward.

**Documentation is a derivative.** User-facing documentation describes a working, validated system rather than a speculative design. Internal documentation (architecture decisions, API contracts) is derived from what actually supports the surface.

This stance is conditional. When compliance, safety, or invisible system properties dominate, surface anchoring must be combined with formal models, invariants, and traceable specifications. SFD does not claim the surface is always the most important concern -- it claims that when the surface IS the product, it should drive the process.

---

## 6. Testing Strategy: Surface-Anchored Hybrid

SFD should not be interpreted as "E2E tests only" or as an inversion of the testing pyramid. A robust SFD testing profile is a hybrid:

- **Surface-level acceptance tests** for converged user behavior -- the primary regression safety net.
- **Integration tests** for cross-component correctness.
- **Targeted unit tests** for high-complexity domain logic.
- **Property and invariant tests** for critical domain rules.
- **Contract tests** for API and provider boundaries.

The SFD-specific contribution is that acceptance tests are derived from converged surface behavior rather than written speculatively. They encode "what the surface looked like when we agreed it was right," which is an unusually precise acceptance criterion.

---

## 7. Process Gates

SFD benefits from explicit gates to prevent drift and enforce rigor:

### Gate 1: Surface Converged
- All critical flows demonstrated and accepted.
- **Surface State Inventory** completed (see below).
- Known open questions and UX gaps logged explicitly.
- Decision log captured (what was tried, what was rejected, and why).

**Surface State Inventory.** Convergence is not "we clicked around and it felt fine." For every surface unit (screen, command, API endpoint, operator workflow step), the following states must be explicitly classified as **in-scope** (demonstrated and accepted), **deferred** (acknowledged but not blocking convergence), or **not applicable**:

- Empty / zero-data state
- Loading / in-progress state
- Success / happy path
- Validation failure (user error)
- System failure (backend error, timeout, unavailable dependency)
- Partial failure (some items succeed, others fail)
- Permission denied / unauthorized
- Conflict (concurrent edit, optimistic lock failure)
- Rate limit / throttle / retry
- Offline / degraded mode

The inventory prevents the most common failure mode of surface-first approaches: the prototype lies by omission. A click dummy that only shows the happy path has not converged -- it has merely demonstrated one path through a much larger state space. The inventory makes the scope of convergence auditable.

### Gate 2: Contracts Frozen (Rev N)
- API contracts, event schemas, and data boundaries versioned.
- Domain invariants documented.
- Non-functional requirements specified with measurable targets.

### Gate 3: Architecture Review
- Hot paths, scaling risks, and security considerations reviewed.
- Hardening plan established (which simulated components need replacement, in what order).

### Gate 4: Hardening Complete
- All simulated components replaced with production implementations.
- Security, observability, and SLO criteria met.
- Surface behavior verified against converged baseline (acceptance tests pass).

### Gate 5: Release Readiness
- Regression evidence documented.
- Rollback plan in place.
- Monitoring and alerting configured for surface-critical paths.

---

## 8. The Scaling Hypothesis

SFD has a property that is unusual among development methodologies: its effectiveness appears to scale directly with AI model capability.

Two factors drive this:

1. **Proposal quality.** A more capable model produces surface prototypes closer to the human's intent on the first attempt, requiring fewer iteration cycles to converge.

2. **Structural quality during hardening.** A more capable model generates prototype internals with better architecture, reducing the refactoring needed when hardening toward production.

Both factors improve with model capability. This means SFD should become faster, cheaper, and applicable to increasingly complex systems as models improve. Early evidence supports this trajectory: successive generations of coding-capable models (from GPT-3.5 through GPT-4, Claude 3 through Claude 4, and their successors) have shown substantial improvements on standardized software engineering benchmarks (Jimenez et al., 2024; Chen et al., 2021), and the practical utility of AI-assisted prototyping has increased accordingly.

This is an empirical hypothesis, not an axiom. It generates a testable prediction: the class of systems for which SFD outperforms traditional approaches should expand with each generation of AI models. Validating or refuting this requires longitudinal comparison studies across model generations.

---

## 9. Failure Modes and Limitations

### 9.1 Prototype Debt

AI-generated prototypes optimize for speed and apparent correctness, not internal quality. Progressive hardening of a poorly structured prototype can propagate structural problems throughout the system.

Mitigation: explicit hardening milestones (Gate 3 and Gate 4) with architecture review. Treat hardening as an explicit refactoring opportunity, and be willing to rewrite internal components while preserving surface behavior.

### 9.2 E2E Fragility

Over-indexing on end-to-end tests creates slow and flaky suites with poor error localization. The traditional testing pyramid exists for good reasons.

Mitigation: the surface-anchored hybrid testing strategy (Section 6). Acceptance tests anchor user-visible behavior; unit and property tests provide speed and localization.

### 9.3 Non-Surface Complexity

Systems whose core complexity lives below any interaction surface -- financial calculation engines, physics simulations, distributed consensus protocols, safety-critical control systems -- cannot have their hard problems solved through surface iteration. SFD can drive the interaction layer for such systems, but the domain core requires traditional engineering approaches.

SFD is most powerful when the interaction surface IS the primary source of system complexity, which is true for the majority of business software but not for all software.

### 9.4 Anchoring Bias

A known risk of starting with a concrete prototype is anchoring bias (Tversky & Kahneman, 1974): stakeholders may fixate on early design choices because they were the first ones encountered, even when better alternatives exist. The prototype becomes a cognitive anchor that constrains rather than enables exploration.

Mitigation: explicit divergent iteration rounds during the convergence phase. Before declaring convergence, deliberately explore at least one structural alternative ("What if we organized this completely differently?"). The decision log should capture rejected alternatives with reasoning, ensuring that convergence reflects genuine preference rather than anchoring.

### 9.5 Team Convergence Overhead

For a solo practitioner, convergence is a personal judgment call. For teams, convergence means consensus on an interactive artifact. Interactive prototypes have more surface area for disagreement than documents because there is more to react to.

Mitigation: explicit convergence protocols -- time-boxed review sessions with defined sign-off criteria and designated decision-makers.

### 9.6 Context Loss Across Sessions

AI agents have limited context windows and no persistent memory across sessions. A surface prototype that was iterated to convergence in one session may lose its design rationale in the next.

Mitigation: persist decision logs, convergence snapshots, and rejected alternatives in durable project memory. Integration with context-preservation tools (such as OpenSpec, Beads, or similar) is recommended for multi-session projects.

### 9.7 Cognitive Load in Complex Prototypes

Sweller's (1988) cognitive load theory suggests that overly complex prototypes can overwhelm the evaluator's working memory, degrading the quality of critique. Goncales, Farias, da Silva, and Fessler (2021) found that cognitive load is a significant factor in software comprehension tasks.

Mitigation: keep individual surface prototypes focused on one workflow or interaction area at a time. Compose the full system understanding incrementally rather than attempting to evaluate everything in a single artifact.

### 9.8 The Regulation Objection

A common objection to surface-first approaches is that regulated industries require specifications before implementation can begin, making SFD inapplicable. Building design provides a direct counterexample.

Building construction is among the most heavily regulated engineering disciplines in existence. Structural load codes, fire safety standards, seismic requirements, accessibility laws (ADA), zoning ordinances, energy codes, environmental impact requirements, and building department permits all constrain what can be built and how. Failure to comply risks structural collapse, fire deaths, and criminal liability. Despite this -- or rather, entirely compatible with it -- the industry starts with the surface. Architects converge the experiential design with clients before structural engineers prove it meets code.

The critical distinction is between **constraints on the solution space** and **constraints on the process ordering**. Regulations define what the final system must satisfy. They do not dictate that you must begin by writing specifications rather than by prototyping. In architectural practice, code compliance is verified during the hardening phases (Design Development and Construction Documents), not as a precondition for Schematic Design. The architect does not start by reading the building code and deriving a shape from it. They start with what the building should feel like, converge that with the client, and then verify and adapt the design for code compliance during progressive hardening.

The same principle applies to software. HIPAA, SOC 2, GDPR, PCI-DSS, FDA 21 CFR Part 11, and similar regulatory frameworks define what the system must satisfy at release. They are hardening requirements -- constraints that must be met before Gate 4 (Hardening Complete) and Gate 5 (Release Readiness). They do not require that the development process start with a specification document rather than a surface prototype. An SFD project in a regulated domain would converge the interaction surface, derive contracts, and then verify regulatory compliance during hardening -- exactly as an architect converges the building design and then proves it meets structural codes.

Where regulatory constraints DO affect SFD is when they impose specific documentation artifacts as deliverables -- audit trails, formal verification records, traceability matrices. These are additional outputs that must be produced during hardening, not arguments against starting with the surface. SFD's process gates (Section 7) provide natural attachment points for regulatory documentation: Gate 2 for contract and invariant traceability, Gate 3 for architecture and security review, Gate 4 for compliance verification.

---

## 10. Evidence Framework

To evaluate SFD against alternatives rigorously, track the following metrics across comparable projects:

### 10.1 Delivery Metrics

- **PPR (Prototype-to-Product Ratio):** Effort to testable surface prototype / effort to production release meeting Gate 4-5 criteria. The central metric for validating SFD's economic premise.
- Time to first interactive prototype
- Time to converged surface
- Lead time from convergence to production release
- Number of iteration cycles to convergence

### 10.2 Rework Metrics

- Requirement churn after surface convergence
- Rewrite ratio during hardening phase
- Defect escape rate post-release
- API contract revision frequency after Gate 2

### 10.3 Quality Metrics

- Production incident rate
- Test flake rate (surface-level vs. unit-level)
- Mean time to localize regressions

### 10.4 Product Metrics

- User task success rate on key workflows
- Time-on-task for critical flows
- Support ticket volume tied to UX mismatch
- Feature adoption rate

### 10.5 Suggested Study Design

- Compare SFD vs. baseline process on matched work items.
- Use at least 3 project classes: interaction-heavy app, API product, domain-heavy system.
- Run for at least one quarter.
- Report both wins and failures transparently.
- Control for team experience and AI model capability.

---

## 11. Comparison Matrix

| Property | Waterfall | Agile | RDD | Outside-In TDD | SFD | Building Design |
|---|---|---|---|---|---|---|
| Starting artifact | Requirements doc | Story / backlog item | README | Failing behavior test | Working surface prototype | Sketch / 3D model |
| Primary creative act | Upfront specification | Iterative planning | Consumer narrative | Behavior specification | Critique and iteration | Critique and iteration |
| Cognitive mode | Generation | Mixed | Generation | Generation | Recognition / evaluation | Recognition / evaluation |
| Prototype cost | N/A | Medium-high | N/A | N/A | Near-zero (AI-generated) | Near-zero (pencil/CAD) |
| AI dependence | None | Optional | None | None | Strongly enabled | None (always had cheap medium) |
| Architecture driver | Spec | Emergent | README | Tests | Surface demands | Converged spatial design |
| Strength | Predictability | Adaptation | Clarity of intent | Behavior correctness | Product-fit convergence speed | Proven over centuries |
| Main risk | Wrong spec lock-in | Drift / process variance | Under-specification | Test maintenance | Prototype debt | Scope creep from tangibility |
| Scales with AI capability | No | Marginally | No | No | Yes (hypothesis) | N/A |

---

## 12. When to Use SFD

**Best fit:**

- Interaction-heavy products where the surface IS the product
- Ambiguous or evolving requirements
- Small teams or solo builders with strong AI tooling
- Rapid product discovery and refinement
- Greenfield projects where interaction model is not yet established

**Compatible with regulated environments.** Regulatory and compliance requirements (HIPAA, SOC 2, GDPR, PCI-DSS, etc.) constrain what the system must satisfy at release, not the order in which it is developed. Building design -- one of the most heavily regulated engineering disciplines -- follows a surface-first ordering and verifies code compliance during hardening, not as a precondition for design (see Section 9.8). SFD's process gates provide natural attachment points for regulatory documentation and audit artifacts.

**Combine with traditional approaches when:**

- Significant domain complexity exists below the surface layer (the hard problem is not what the user sees but what happens underneath)
- Safety-critical systems where formal verification or mathematical proof of correctness is required before any implementation
- Large teams require coordination beyond what surface prototypes provide

**Not a strong fit as primary driver when:**

- The system has no meaningful interaction surface (embedded firmware, pure background services)
- The core challenge is mathematical, protocol-level, or safety proof
- Organizational culture requires fully predefined artifact chains as preconditions for approval (this is a political constraint, not a technical one -- building design demonstrates that regulated industries can and do start with the surface)

---

## 13. Conclusion

Surface-First Development is not a radical new invention. It is the formalization of a practice that becomes optimal when PPR drops low enough. Building design, where PPR has always been orders of magnitude below 1, has followed a surface-first ordering for centuries (AIA, n.d.). Software methodologies like README-Driven Development (Preston-Werner, 2010), Outside-In TDD (Freeman & Pryce, 2009), and design thinking (Brown, 2008) pointed in the same direction but were constrained by software's historically high PPR. AI coding agents have collapsed that ratio, giving software its equivalent of the architect's napkin.

The methodology's core claim: when generating working prototypes is cheap, the optimal development process starts with a working prototype of the interaction surface and works inward, rather than starting with abstract specifications and working outward. This exploits the cognitive asymmetry between recognition and generation (Mandler, 1980; Kahneman, 2011) rather than fighting it.

This claim is conditional. SFD is most effective for interaction-centric software, and it should be combined with traditional approaches when domain complexity lives below the surface or when safety-critical systems require formal verification. Regulatory constraints, however, are not inherently incompatible with SFD -- building design demonstrates that even heavily regulated engineering disciplines can and do start with the surface and verify compliance during hardening. The methodology includes explicit process gates, a hybrid testing strategy, and an evidence framework precisely so that its effectiveness can be measured and its boundaries discovered empirically.

As AI models improve, SFD's applicability range should expand -- better proposals mean faster convergence, and better code generation means less rework during hardening. Whether this scaling hypothesis holds, and how far it extends, is an empirical question that the evidence framework in Section 10 is designed to answer.

---

## References

American Institute of Architects. (n.d.). Defining the architect's basic services. AIA. https://www.aia.org/resource-center/defining-the-architects-basic-services (Describes the five standard phases of architectural design services: Schematic Design, Design Development, Construction Documents, Bidding, and Construction Administration.)

Anderson, J. R., & Bower, G. H. (1974). A propositional theory of recognition memory. *Memory & Cognition*, 2(3), 406-412.

Boehm, B. W. (1981). *Software Engineering Economics*. Prentice-Hall.

Boehm, B. W. (1988). A spiral model of software development and enhancement. *Computer*, 21(5), 61-72. https://doi.org/10.1109/2.59

Boehm, B. W., & Papaccio, P. N. (1988). Understanding and controlling software costs. *IEEE Transactions on Software Engineering*, 14(10), 1462-1477. https://doi.org/10.1109/32.6191

Brown, T. (2008). Design thinking. *Harvard Business Review*, 86(6), 84-92.

Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. D. O., Kaplan, J., ... & Zaremba, W. (2021). Evaluating large language models trained on code. *arXiv preprint arXiv:2107.03374*. https://arxiv.org/abs/2107.03374

Eveleens, J. L., & Verhoef, C. (2010). The rise and fall of the Chaos report figures. *IEEE Software*, 27(1), 30-36. https://doi.org/10.1109/MS.2009.154

Floyd, C. (1984). A systematic look at prototyping. In R. Budde, K. Kuhlenkamp, L. Mathiassen, & H. Zullighoven (Eds.), *Approaches to Prototyping* (pp. 1-18). Springer. https://doi.org/10.1007/978-3-642-69796-8_1

Freeman, S., & Pryce, N. (2009). *Growing Object-Oriented Software, Guided by Tests*. Addison-Wesley.

Freeman, S., Pryce, N., Mackinnon, T., & Walnes, J. (2004). Mock roles, not objects. In *Companion to the 19th Annual ACM SIGPLAN Conference on Object-Oriented Programming Systems, Languages, and Applications* (pp. 236-246). ACM. https://doi.org/10.1145/1028664.1028765

Goncales, L. J., Farias, K., da Silva, B., & Fessler, J. (2021). Measuring the cognitive load of software developers: A systematic mapping study. *IEEE/ACM International Conference on Program Comprehension (ICPC)*, 42-52.

Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. (2024). SWE-bench: Can language models resolve real-world GitHub issues? *arXiv preprint arXiv:2310.06770*. https://arxiv.org/abs/2310.06770

Kahneman, D. (2003). Maps of bounded rationality: Psychology for behavioral economics. *American Economic Review*, 93(5), 1449-1475. https://doi.org/10.1257/000282803322655392

Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

Mandler, G. (1980). Recognizing: The judgment of previous occurrence. *Psychological Review*, 87(3), 252-271. https://doi.org/10.1037/0033-295x.87.3.252

Plattner, H., Meinel, C., & Leifer, L. (Eds.). (2011). *Design Thinking: Understand, Improve, Apply*. Springer.

Preston-Werner, T. (2010). Readme driven development. https://tom.preston-werner.com/2010/08/23/readme-driven-development.html

Slamecka, N. J., & Graf, P. (1978). The generation effect: Delineation of a phenomenon. *Journal of Experimental Psychology: Human Learning and Memory*, 4(6), 592-604. https://doi.org/10.1037/0278-7393.4.6.592

Standish Group. (1995). *The CHAOS Report*. The Standish Group International.

Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257-285. https://doi.org/10.1207/s15516709cog1202_4

Tulving, E. (1985). Memory and consciousness. *Canadian Psychology*, 26(1), 1-12.

Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124-1131. https://doi.org/10.1126/science.185.4157.1124

---

## Appendix A: Glossary

- **Surface:** The outermost interaction layer of a system -- whatever the end-user (human or system) directly touches. Formally: the externally observable behavior of the system under a defined environment model. This includes UI screens, CLI commands, API responses as experienced by a consumer, operator dashboard views, and any other point where a human or external system interacts with the product.
- **Surface Prototype:** A working, interactive simulation of the surface, generated by an AI agent and iterable through conversation.
- **Surface State Inventory:** The enumeration of observable states for each surface unit (screen, command, endpoint), classified as in-scope, deferred, or not applicable. Used to define convergence criteria at Gate 1.
- **Convergence:** The state in which stakeholders can walk through all critical flows without encountering unresolved behavioral mismatches, verified against an accepted Surface State Inventory.
- **Progressive Hardening:** The process of evolving a surface prototype into production software by replacing simulated components with real implementations while preserving validated surface behavior.
- **PPR (Prototype-to-Product Cost Ratio):** The ratio of the effort to produce a testable surface prototype to the effort required to reach a production release that meets hardening criteria. When PPR is low (as in building design, or software with AI agents), surface-first development becomes the optimal ordering. When PPR is high, specification-first becomes a rational adaptation.
- **Surface-Anchored Hybrid Testing:** Acceptance tests anchored to converged surface behavior, supported by integration, unit, property, and contract tests.
- **Contracts:** API contracts, domain invariants, and non-functional requirements derived from the converged surface prototype.

## Appendix B: Minimal Workflow Template

1. Identify the interaction surface.
2. Capture intent, constraints, and non-negotiables.
3. Generate surface prototype.
4. Iterate to convergence; log decisions and rejected alternatives.
5. Complete Surface State Inventory for all surface units.
6. Derive contracts and invariants (Gate 1 -> Gate 2).
7. Architecture review (Gate 3).
8. Build inward via vertical slices with progressive hardening.
9. Verify surface behavior against converged baseline (Gate 4).
10. Release with regression protection and rollback plan (Gate 5).

## Appendix C: Extended Example Workflows

### C.1 Web Application

```
Developer: "Build me a click dummy for a project management tool
            where teams can track weekly goals and see progress
            at a glance."

AI Agent:   [generates React click dummy with dashboard,
             goal creation flow, progress visualization]

Developer:  [clicks through] "The dashboard is too busy.
             I want to see just this week's goals, not all of them.
             And the progress should be a simple bar, not a pie chart."

AI Agent:   [regenerates with focused weekly view and progress bars]

Developer:  [clicks through] "Better. But what happens when a goal
             is overdue? There is no indication."

AI Agent:   [adds overdue state with visual indicator and
             overdue filter option]

Developer:  [clicks through] "This feels right. Let's build it."

--> Convergence reached (Gate 1).
    Derive contracts: REST endpoints for goals CRUD, WebSocket
    for real-time progress, overdue calculation rules (Gate 2).
    Architecture review: confirm tech stack, persistence
    strategy, auth approach (Gate 3).
    Progressive hardening begins:
      Mock data -> PostgreSQL
      Simulated auth -> OAuth2 flow
      Static goals -> full CRUD with validation
      Happy path -> error handling, loading states, offline
    Verify surface behavior matches converged baseline (Gate 4).
    Release with monitoring on goal-critical paths (Gate 5).
```

### C.2 CLI Tool

```
Developer: "Show me what an ideal terminal session looks like
            for a tool that analyzes git repositories for
            code quality trends over time."

AI Agent:   [generates a scripted terminal session showing
             commands, flags, output formatting, error messages]

             $ cqt analyze ./my-repo --since 6m
             Analyzing 847 commits over 6 months...

             Code Quality Trend: my-repo
             ================================
             Complexity:  ████████░░ 78/100 (+5 from 6m ago)
             Test Coverage: ██████░░░░ 62/100 (-3 from 6m ago)
             ...

Developer:  "I want the default to be the current branch only,
             not the whole repo. And add a --compare flag that
             shows two branches side by side."

AI Agent:   [regenerates session transcript with updated defaults
             and comparison output]

Developer:  "What does the error look like if you run this outside
             a git repo?"

AI Agent:   [shows error handling scenario]

             $ cqt analyze .
             Error: not a git repository (or any parent up to /)
             Hint: run this command inside a git repository,
                   or specify a path: cqt analyze /path/to/repo

Developer:  "Good. This is the CLI I want."

--> Convergence reached (Gate 1).
    Derive contracts: CLI argument schema, output formats
    (human-readable + JSON), exit codes, git integration
    requirements (Gate 2).
    The terminal transcript becomes the acceptance test suite
    and the behavioral reference for implementation.
    Vertical slices: branch analysis first, then comparison,
    then historical trends.
```

### C.3 API / Library

```
Developer: "Write the code a developer would write to use
            an authentication library that handles OAuth,
            magic links, and API keys."

AI Agent:   [generates example integration code]

             from myauth import Auth

             auth = Auth(provider="google")

             # OAuth flow
             redirect_url = auth.login()
             token = auth.callback(request.params)

             # Magic link
             auth.send_magic_link("user@example.com")
             token = auth.verify_magic_link(code)

             # API key
             key = auth.create_api_key(user_id, scopes=["read"])
             user = auth.verify_api_key(request.headers["X-API-Key"])

Developer:  "The three auth methods should not be separate APIs.
             I want a unified interface where the method is
             configured, not coded."

AI Agent:   [regenerates with unified interface]

             auth = Auth(methods=["oauth:google", "magic_link",
                                  "api_key"])

             # Same entry point regardless of method
             challenge = auth.initiate(identifier="user@example.com")
             token = auth.verify(challenge_id=challenge.id,
                                 response=code)

Developer:  "Now show me error handling and token refresh."

AI Agent:   [extends example with error cases and refresh flow]

Developer:  "This is the API I would want to use."

--> Convergence reached (Gate 1).
    The example code becomes the README, the integration
    test suite, and the public API contract (Gate 2).
    Internal implementation proceeds against the converged
    consumer experience.
```

### C.4 Data Pipeline (Operator Workflow)

```
Developer: "Walk me through what it looks like to deploy,
            monitor, and debug a failure in a real-time
            event processing pipeline."

AI Agent:   [generates operator workflow]

             # Deploy
             $ pipeline deploy events-v2 --env staging
             Deploying events-v2 to staging...
             Health check: 3/3 consumers connected
             Backfill: not required (schema compatible)
             Status: RUNNING

             # Monitor (steady state)
             $ pipeline status events-v2
             Throughput:  12,847 events/sec (p99 latency: 23ms)
             Dead letter: 0 events (last 24h)
             Consumer lag: 340ms (within SLO)

             # Failure scenario
             $ pipeline status events-v2
             WARNING: Consumer lag: 47s (SLO breach)
             Dead letter: 1,204 events (last 1h)
             Root cause: downstream-api timeout (see trace abc123)

             $ pipeline dlq inspect events-v2 --last 10
             [shows structured dead letter entries with
              error context and replay option]

             $ pipeline dlq replay events-v2 --filter "error:timeout"
             Replaying 1,204 events... done (3 still failing)

Developer:  "I want the deploy step to show a diff of what
             is changing, and require confirmation for
             production."

AI Agent:   [regenerates deploy flow with diff and
             confirmation gate]

Developer:  "Good. This is how I want operators to work
             with this system."

--> Convergence reached (Gate 1).
    Derive contracts: CLI schema, health check protocol,
    DLQ format, SLO thresholds, deployment safety
    gates (Gate 2).
    Note: the hard engineering (backpressure, exactly-once
    semantics, partition handling) is NOT solved by this
    surface. Those require traditional engineering.
    SFD contributed the operator experience; domain
    engineering contributes the internals.
```

---

## Appendix D: Relationship to SpecDriven Development

SFD and SpecDriven Development (as implemented with tools like OpenSpec and Beads) are complementary, not competing:

- **SFD** addresses the discovery and design phase: how do you figure out what to build?
- **SpecDriven Development** addresses the persistence and execution phase: how do you ensure agents maintain context, track progress, and don't lose the thread across sessions?

A natural combined workflow:

1. Use SFD to discover and converge the interaction surface.
2. Derive contracts and capture the converged state as an OpenSpec artifact.
3. Use Beads to track implementation tasks during hardening.
4. When requirements evolve, return to Step 1: update the surface, re-converge, update specs.

SFD provides the "what" and the "why." SpecDriven Development provides the "how it stays coherent over time."

---

## Appendix E: SFD Artifact Stack

Every SFD project produces the following artifacts, listed in the order they emerge. This list is intended to make SFD adoptable by teams without requiring them to reverse-engineer the methodology from the paper.

### 1. Intent Document
**Created:** Before surface generation (Phase 1)
**Contains:** Problem statement, target users, constraints, non-negotiables, known unknowns.
**Purpose:** Anchors the surface generation to a shared understanding of what the project is for. Not a specification -- it captures intent and boundaries, not solutions.

### 2. Surface Prototype
**Created:** Phase 2-3 (generate, iterate)
**Contains:** Working, interactive simulation of the outermost interaction layer. May be a click dummy, a CLI session, example API consumer code, or an operator workflow walkthrough.
**Purpose:** The primary artifact for stakeholder evaluation and critique. Iterated to convergence.

### 3. Decision Log
**Created:** During iteration (Phase 3), maintained through hardening
**Contains:** What was tried, what was rejected, and why. Includes rejected alternatives with rationale.
**Purpose:** Prevents revisiting settled decisions. Provides audit trail for design choices.

### 4. Surface State Inventory
**Created:** Before Gate 1
**Contains:** For every surface unit, a classification of observable states as in-scope, deferred, or not applicable (see Gate 1 definition in Section 7).
**Purpose:** Makes convergence auditable. Prevents the prototype from lying by omission.

### 5. Derived Contracts
**Created:** Gate 1 -> Gate 2
**Contains:** API contracts (schemas, error shapes, status codes), domain invariants, event schemas, data boundaries, non-functional requirements with measurable targets.
**Purpose:** Formal engineering commitments derived from converged surface behavior. Versioned and frozen at Gate 2 (revision policy defined).

### 6. Acceptance Test Suite
**Created:** Derived from converged surface at Gate 2
**Contains:** Behavioral tests encoding "what the surface looked like when we agreed it was right." One test per critical flow per in-scope state in the Surface State Inventory.
**Purpose:** Regression protection during hardening. The primary verification that hardening preserves surface behavior.

### 7. Hardening Plan
**Created:** Gate 3 (Architecture Review)
**Contains:** Which simulated components need replacement, in what order. Hot paths, scaling risks, security considerations. Harden-vs-rewrite decision for each component. Regulatory compliance verification points.
**Purpose:** Turns hardening from ad hoc replacement into a planned engineering effort.

### 8. Release Readiness Evidence
**Created:** Gate 4 -> Gate 5
**Contains:** Acceptance test results, contract test results, property test results (where applicable), performance benchmarks against NFR targets, security review sign-off, rollback plan, monitoring and alerting configuration, SLO verification.
**Purpose:** Demonstrates that the hardened system meets production standards while preserving the converged surface behavior.

---

SFD provides the "what" and the "why." SpecDriven Development provides the "how it stays coherent over time."

---

*This document is a living artifact. It should be revised as empirical evidence accumulates and as the tooling landscape evolves.*
