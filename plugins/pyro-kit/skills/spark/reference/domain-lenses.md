# Creative Domain Lenses

Shared reference for /spark, /remix, and /reframe skills. Each lens is a complete vocabulary and set of reframing questions for thinking about software projects through a non-developer domain.

Using a lens: identify the relevant vocabulary, apply the key analogies to the project's actual structure, then work through the reframing questions. The questions are prompts for concrete evaluation ("what is the X in your project?"), not open-ended brainstorming prompts.

---

## Lens 1: Game Design

Game design is the discipline of creating systems where player choices produce meaningful, interesting outcomes. It is fundamentally about *motivation architecture* — why does a player keep engaging? — and *feedback loop engineering* — how does the system respond to player actions in ways that reinforce continued play?

### Core Vocabulary

| Term | Definition in software/project context |
|------|----------------------------------------|
| **Mechanic** | A single rule or interaction type in the system (e.g., "you can tag items"). Each mechanic has a verb: collect, build, avoid, match. |
| **Feedback loop** | A cycle where player action produces a response that affects future action. Tight loops = high engagement. Loose loops = disengagement. |
| **Progression system** | The structure by which capability or access expands over time. Determines whether users feel growth or stagnation. |
| **Core loop** | The 2-5 minute cycle a player repeats most often. Everything else supports or varies the core loop. |
| **Player motivation** | The intrinsic or extrinsic drive to continue playing. Mastery (getting better), autonomy (making choices), discovery (finding new things), social (connection). |
| **Difficulty curve** | The rate at which challenge increases relative to player skill. Poor curves cause boredom (too flat) or frustration (too steep). |
| **Juicy feedback** | Feedback that is satisfying beyond its informational content — animations, sounds, haptics that reward action viscerally. |
| **Fail state** | A defined condition where the player loses progress. Fail states make success meaningful; absent fail states produce "spreadsheet games." |

### Key Analogies

- Onboarding is a tutorial level — the core loop should be learnable in the first session without documentation
- User retention is player retention — the question is "is the core loop rewarding enough to repeat tomorrow?"
- Feature complexity is difficulty design — each new feature increases cognitive load; must be offset by skill growth
- Empty state (new user, no data) is the "you start with nothing" game opening — it must make the first action obvious
- Loading and processing time is game lag — imperceptible is good, noticeable requires juicy feedback to bridge

### Reframing Questions

1. **What is the core loop in your project?** Name the 2-5 step cycle that a typical user repeats most often and identify where the feedback arrives in that cycle.
2. **What is the fail state?** If there is no fail state, what replaces the stakes that make success meaningful?
3. **What progression exists?** Is there a visible capability expansion or discovery arc, or does the experience feel identical on day 30 as day 1?
4. **Which player motivation does this serve?** Mastery, autonomy, discovery, or social — and is the product designed toward that motivation or accidentally working against it?
5. **Where is the core loop leaking?** Identify the step in the core loop where users are most likely to stop and ask "what do I do now?" — that is the loop's weakest joint.

### Example Application

**Project**: A writing tool that helps you maintain consistency across a long document.

**Lens applied**: The core loop is "write → inconsistency flagged → correct → continue." Currently the feedback arrives post-hoc (you run a check after writing). Applying game design: the feedback should arrive *during* the loop, not after. The "juicy feedback" principle says that corrections should feel satisfying, not punitive. The progression system is missing entirely — on day 1 and day 100 the tool behaves identically. A game designer would add a "consistency score" that rises as your document matures, giving users a visible growth artifact.

---

## Lens 2: Music

Music is the discipline of organizing sound through time to produce emotional and intellectual experiences. Its vocabulary concerns *tension and resolution*, *repetition and variation*, and *the relationship between structure and expression*. For software, music thinking reveals how the experience of using a tool unfolds over time — the rhythm of interaction, the harmony between components, and where the composition needs contrast.

### Core Vocabulary

| Term | Definition in software/project context |
|------|----------------------------------------|
| **Composition** | The overall structure of an experience — how sections are arranged, what comes first, what resolves last |
| **Harmony** | The consonance or dissonance between simultaneous elements. In software: visual harmony, data model harmony, API harmony |
| **Rhythm** | The cadence of interaction — how fast events arrive, what the expected beat is, where the pauses are |
| **Tension/Resolution** | A raised expectation followed by its satisfaction. In software: a loading state that resolves, a form that submits, a problem statement with a clear answer |
| **Arrangement** | The distribution of roles across instruments — in software, which layer handles what concern (UI, logic, data) |
| **Dynamics** | Volume variation — loud moments (primary actions, confirmations) vs. quiet moments (secondary info, defaults) |
| **Motif** | A short recurring pattern that creates coherence. In software: a repeated interaction pattern, a consistent visual element |
| **Bridge** | A contrasting section that prevents monotony and recontextualizes what came before. In a product: the moment of realization, the pivot point |

### Key Analogies

- Navigation is composition — where you start and what the journey toward the end feels like
- Consistent UI patterns are motifs — they create familiarity that lets users focus on content, not interface
- Cognitive load is dynamics — important things should be loud, ambient things should be quiet; an interface where everything is equally loud is noise
- Onboarding is an overture — it introduces the main themes before developing them
- Error states are dissonance — they must resolve or the piece never lands

### Reframing Questions

1. **What is the rhythm of interaction?** At what cadence do inputs and responses arrive, and does the current response time match the expected beat?
2. **Where is the dissonance in your project?** Identify one place where two elements feel out of harmony — a UI element that clashes with the data model, an API that contradicts the user mental model.
3. **What is the motif?** Name the single interaction pattern that repeats most across the product — is it consistent enough to become a recognizable signature?
4. **Where does the composition need a bridge?** Identify a section of the experience that feels monotonous or disorienting — this is where a structural contrast or change of key would serve the user.
5. **What resolves?** Every tension that the product creates (a loading state, an unfinished action, an unanswered question) — does each one have a resolution, and is the resolution satisfying?

### Example Application

**Project**: A task management tool that keeps losing users after week 2.

**Lens applied**: The rhythm diagnosis — users interact in bursts (morning planning, afternoon check-ins) but the tool treats all interactions as equivalent. Musically, this is a composition without dynamics — everything is mezzo-forte all the time. The fix is to design "loud" moments (the morning plan, the end-of-day close) and "quiet" moments (mid-task status ticks). The motif analysis reveals the tool has no consistent signature interaction — every action feels different. A music arranger would choose one motif (e.g., "swipe to complete") and repeat it everywhere.

---

## Lens 3: Screenwriting

Screenwriting is the craft of constructing story through scene, character, and dialogue. Its vocabulary is about *conflict driving structure*, *character motivation producing behavior*, and *pacing determining emotional impact*. For software, screenwriting thinking reframes users as characters with goals, obstacles, and arcs — and the product as the world they inhabit.

### Core Vocabulary

| Term | Definition in software/project context |
|------|----------------------------------------|
| **Three-act structure** | Setup (establish character + world), Confrontation (character meets obstacle), Resolution (obstacle resolved, character changed). Maps to onboarding → core usage → completion/return |
| **Character arc** | The change a character undergoes through the story. In software: how the user is different (more capable, more informed) after using the product |
| **Conflict** | The engine of story. Without conflict (obstacle between character and goal) there is no story. In software: the friction between user goal and current reality that the product resolves |
| **Scene** | A unit of story where something changes. Each screen, flow, or session is a scene — it must end differently than it began |
| **Dialogue** | The words characters say — in software: the microcopy, labels, and system messages. Dialogue reveals character and moves plot; bad dialogue stalls both |
| **Pacing** | The rate at which the story moves. Too slow = boredom, too fast = confusion. In software: information density and step count in a flow |
| **Subtext** | What characters mean vs. what they say. In software: what users intend vs. what they type. The product must handle subtext, not just text |
| **Hook** | The opening beat that makes the audience commit to watching. In software: the first 30 seconds of a new user's experience |

### Key Analogies

- User personas are character sheets — they need a goal, an obstacle, a flaw, and a motivation, not just demographics
- Empty state is act one — it must establish stakes and make the user's first action obvious
- Error messages are villain dialogue — they define the obstacle; good villain dialogue is clear about what it wants
- The "aha moment" is the act two midpoint — the moment the user understands what the product actually is
- Retention is whether users want to know what happens in act three

### Reframing Questions

1. **What is the user's character arc?** Define how a user who completes a full interaction cycle is different from a user who arrived — if there is no arc, they have no reason to return.
2. **What is the conflict in your project?** Name the specific obstacle between the user's goal and the current reality that your product removes — this is the only thing the product needs to do.
3. **What is the hook?** Describe the first 30 seconds of a new user experience and identify whether it establishes stakes, or just introduces features.
4. **Where does the pacing break?** Find the flow with the highest drop-off and count the steps between the user's goal and the moment it's achieved — each unnecessary step is a pacing error.
5. **What does your dialogue reveal about your product's character?** Read three random system messages or labels aloud — what personality does the voice have, and is that the character you intended?

### Example Application

**Project**: A developer documentation site.

**Lens applied**: Character arc analysis — the user arrives wanting to solve a specific problem. The current site treats every user as a new character beginning act one (read the overview, understand the concepts). But most users are in act two or three (they have context, they have a specific problem). Screenwriting fix: the hook should branch immediately — "I'm starting fresh" (act one) vs. "I have a specific problem" (act two). The conflict analysis reveals that documentation sites' real conflict is "user can't find the answer" — which means the search experience is the villain, not the content.

---

## Lens 4: Architecture

Architecture is the discipline of designing built environments — spaces that humans inhabit, move through, and are affected by. Its vocabulary concerns *flow and circulation*, *structure and load*, *form and program*, and the relationship between the experience of a space and the intent behind it. For software, architecture thinking makes invisible structures visible and asks whether the structural decisions serve the people inhabiting the system.

### Core Vocabulary

| Term | Definition in software/project context |
|------|----------------------------------------|
| **Program** | The intended uses of a space — what activities happen here? In software: the use cases the system is designed to support |
| **Circulation** | How people move through a space — the paths, corridors, and transitions. In software: navigation, user flows, state transitions |
| **Load-bearing** | The elements that the structure depends on — remove them and it collapses. In software: the core data model, the primary API contract |
| **Form follows function** | Shape should emerge from purpose. In software: UI structure should emerge from the user's task, not from aesthetic preference |
| **Site** | The context and constraints of a location — orientation, neighbors, climate. In software: the user's environment, device constraints, existing workflows |
| **Threshold** | The moment of transition between two spaces — arriving, entering, crossing. In software: first login, mode switches, permission escalations |
| **Structural integrity** | The building's ability to bear load over time. In software: the codebase's ability to support feature additions without collapse |
| **Fenestration** | The placement of windows — where light enters. In software: where data visibility enters the UI — what users can see about system state |

### Key Analogies

- Technical debt is deferred maintenance — it doesn't make the building dangerous immediately, but compound interest on ignored problems always does
- API design is structural engineering — public APIs are load-bearing; changing them requires shoring the whole building
- Onboarding is the entrance sequence — the experience of arriving matters; a poor entrance primes users to feel lost
- Navigation is circulation — users should be able to find where they're going from anywhere, the way a good building has sight lines
- Permission levels are thresholds — they create meaningful spatial boundaries that affect how users inhabit the system

### Reframing Questions

1. **What is the program of your project?** List the 3-5 activities the system is genuinely designed to support — not features, but human activities. Are any features present that serve no item on this list?
2. **Where does circulation break?** Identify the place in the user flow where users take the longest or most circuitous path to reach their goal — this is poor corridor design.
3. **What is load-bearing in your project?** Name the 1-2 data structures or contracts that everything else rests on — and evaluate whether they are designed to bear the load that is actually placed on them.
4. **Where is form fighting function?** Find a UI pattern that looks clean but makes the user's task harder — this is a building designed for photographs, not for living in.
5. **What are the thresholds in your project?** List every point where the user crosses from one "room" to another — are those transitions designed or accidental?

### Example Application

**Project**: A project management tool with 47 features.

**Lens applied**: Program analysis — what are the 3-5 human activities this supports? Planning, tracking, communicating, reporting. Circulation analysis: users currently need 4 clicks to move a task from "in progress" to "done" — the corridor to the most common destination is too long. Load-bearing analysis: the task data model is load-bearing and has been patched 12 times — structural integrity is at risk. The architecture recommendation: reduce the corridor (inline task status changes), reinforce the load-bearing wall (refactor task model), and audit every feature against the program list.

---

## Lens 5: Improv

Improv is the performing art of creating scenes spontaneously with other performers. Its core disciplines are *listening*, *accepting and building on offers*, *supporting scene partners*, and *committing fully*. For software, improv thinking reframes the product as a scene partner — how well does it listen? Does it accept what the user offers? Does it support the user's intent or block it?

### Core Vocabulary

| Term | Definition in software/project context |
|------|----------------------------------------|
| **Yes, and** | Accept what your scene partner offers and add to it. In software: accept what the user inputs without rejecting it, and extend it toward their goal |
| **Offer** | Any action or statement that establishes something in the scene. In software: every user input is an offer — what does the system do with it? |
| **Block** | Refusing or ignoring an offer. In software: validation errors that reject input without helping, dead ends, missing affordances |
| **Heightening** | Taking what the scene has established and amplifying it. In software: smart defaults, autocomplete, context-aware suggestions that make the user feel understood |
| **Callback** | Referencing something from earlier in the scene to create resonance. In software: remembering previous inputs, showing patterns in history, "you usually do X at this point" |
| **Support** | Prioritizing your scene partner's success over your own moment. In software: the interface that puts the user's goal first, not the product's metric |
| **Scene** | A unit with a clear beginning, middle, and end where something changes. In software: a session, a task completion, a workflow |
| **Tag out** | Replacing a performer in a scene. In software: handing off to another system, tool, or context |

### Key Analogies

- Form validation is blocking — "no, that's wrong" with no path forward is a blocked offer
- Autocomplete is "yes, and" — it accepts the partial input and extends it
- Undo is "let's try that again" — improv has no undo, but software should, because real users make mistakes
- Contextual help is a good scene partner listening and offering — it appears when the offer was confusing, not on a schedule
- Error recovery that suggests the correct path is support — it prioritizes getting the user where they're going

### Reframing Questions

1. **Where does your project block users?** Identify every validation error, dead end, or missing affordance — each is a "no" without a "and here's how." Rewrite each block as a "yes, and."
2. **What callbacks exist in your project?** List the places where the system references something the user did previously — are there enough to make users feel recognized, or does every session start from zero?
3. **Is the interface supporting the user or stealing focus?** Find the three places where the interface asks the most of the user's attention — is that attention being asked for their benefit or the product's?
4. **What offers are users making that the system ignores?** Identify inputs or signals the system receives but doesn't act on — these are blocked offers waiting to become features.
5. **What is the scene the user is trying to play?** Define the scene (goal + context) for your most common user task — and evaluate whether the system is a good scene partner for that scene or an obstacle to it.

### Example Application

**Project**: A CLI tool for managing deployment configurations.

**Lens applied**: Block audit — every error message that says "invalid syntax" without showing the correct syntax is a block. The offer the user is making is "I want to configure X" — the system is blocking it with "that's wrong." Yes-and reframe: every error should include the valid alternatives. Callback analysis: the CLI has no memory — every run starts from scratch. Adding a "last run" command that replays the previous valid configuration is a callback that makes the tool feel like a scene partner, not a gatekeeper.

---

## Lens 6: Cooking

Cooking is the craft of transforming raw ingredients through technique and process into a cohesive, balanced, and pleasurable experience. Its vocabulary concerns *preparation and sequence*, *flavor balance and contrast*, *technique as the difference between ingredients and food*, and *the service moment*. For software, cooking thinking reveals how components combine, where the preparation work is hidden, and whether the final experience is balanced or overwhelming.

### Core Vocabulary

| Term | Definition in software/project context |
|------|----------------------------------------|
| **Mise en place** | "Everything in its place" — all prep done before cooking begins. In software: data loading, auth checks, context initialization that must complete before the user's session starts |
| **Flavor profile** | The characteristic combination of tastes — sweet, sour, salty, bitter, umami. In software: the characteristic combination of product qualities — powerful, simple, opinionated, flexible |
| **Technique** | The method applied to ingredients — sauté, braise, emulsify. In software: the algorithms, patterns, and abstractions applied to data |
| **Balance** | No single element overwhelming the dish. In software: no single concern (performance, features, simplicity) dominating at the expense of others |
| **Plating** | The presentation — how the finished dish appears before being eaten. In software: the initial screen, empty state, and first impression |
| **Reduction** | Concentrating flavors by removing excess liquid. In software: distilling a feature to its essence by removing scope until only the core remains |
| **Emulsification** | Combining two things that don't naturally mix by finding a common agent. In software: integration between systems that have incompatible data models |
| **Seasoning** | Small adjustments that elevate the whole dish. In software: microcopy, transition animations, default values — small additions that dramatically improve the experience |

### Key Analogies

- Performance optimization is mise en place — work done before the user arrives so the session feels instantaneous
- Feature bloat is over-seasoning — when every flavor is loud, none of them is tasted
- API design is recipe design — a recipe (interface contract) that requires 17 ingredients to make a simple dish needs reduction
- Onboarding is the amuse-bouche — a small, considered bite that sets expectations for the meal ahead
- Error states are a dish that doesn't taste right — the cook (developer) knows why it happened, but the guest (user) just knows something is off

### Reframing Questions

1. **What is the flavor profile of your project?** Name 3-4 qualities that characterize the experience — and identify whether those qualities are in balance or whether one is overwhelming the others.
2. **Where is the mise en place missing?** Identify any moment where the user is waiting for the system to prepare itself — loading states that could have been pre-computed, data that could have been pre-fetched.
3. **What needs reduction?** Find the feature, flow, or interface that is trying to do too much and identify what remains if you reduce it to its essence.
4. **What is the seasoning in your project?** List the small additions (copy, transitions, defaults, keyboard shortcuts) that would elevate the experience without adding complexity — and evaluate whether any of them are present.
5. **How is the plating?** Evaluate the first screen a user sees — does it communicate the flavor profile of the product, or does it reveal the kitchen (internal complexity) instead of the dish?

### Example Application

**Project**: A dashboard for monitoring API health.

**Lens applied**: Flavor profile analysis — the product is trying to be powerful (every metric exposed), simple (clean design), and real-time (live updates simultaneously). These three are in tension: power and simplicity conflict, and real-time updates break visual calm. A chef would choose a dominant flavor: this is a *calm monitoring tool* (simplicity as the dominant note) with power available on request. Reduction: remove real-time polling from the default view; make it opt-in. Mise en place: pre-compute trend lines so the dashboard loads with context, not spinners. Seasoning: color-code by severity so a glance tells the story before the user reads a number.
