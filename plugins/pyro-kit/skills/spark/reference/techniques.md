# Idea Thumbnail Generation Techniques

Reference for the /spark skill. Each technique is a concrete procedure for converting vague input into a crystallized idea thumbnail. Apply the technique that best matches the type of input received.

---

## Technique 1: Scenario Projection

**Name**: Scenario Projection

**When to use**: Input describes a desired *feeling* or *outcome* rather than a problem. The person knows what they want life to feel like after the tool exists, but not what the tool does. Also effective when input is a single verb ("I want something that helps me *track* things") without a clear subject.

**How it works**:

1. Identify the actor (who is using this?) — default to "the developer themselves" if unspecified
2. Pick a specific moment in the workday or workflow where the tool would be active
3. Write one paragraph: what is the actor doing before the tool fires? What does the tool do? What does the actor do next?
4. From that paragraph, extract: what capability does the tool have? What does it *not* do?
5. Distill to a thumbnail: name + one sentence + the moment it fires

**Example**:

- Input: "I want something that helps me stay in flow while coding"
- Projected scenario: It's 2pm. You're deep in a function. Slack pings. You minimize the notification without reading it. An hour later you surface and open Slack — there are 14 messages, 3 threads, 2 of which needed you. The tool would have sat between "distraction" and "urgent" — it batches, filters, and surfaces only what genuinely requires interruption.
- Extracted capability: interrupt triage — classifies incoming signals by whether they require synchronous response
- Thumbnail: **Interrupt Filter** — A signal triage layer that batches notifications and surfaces only the ones that require you *now*, not the ones that are just loud.

---

## Technique 2: Annoyance Amplification

**Name**: Annoyance Amplification

**When to use**: Input is a frustration, complaint, or recurring irritant. The person is describing something that keeps happening to them. Key signals: "I hate when", "it annoys me that", "every time I do X", "why does Y always".

**How it works**:

1. Identify the exact moment the annoyance peaks (not the general category — the specific instant)
2. Ask: what would have to be *true about the world* for this annoyance to be structurally impossible?
3. The answer to that question is the capability the tool has
4. Work backwards: what data would the tool need? What decision does it make? What does it output?
5. Distill to a thumbnail: the tool is the thing that enforces the condition from step 2

**Example**:

- Input: "I hate that I lose context every time I switch between repos"
- Peak annoyance moment: Opening a repo you haven't touched in three weeks and having no idea where you left off or what the current state is
- What would make this impossible: if your context were persisted externally from the repo and instantly recalled when you open it
- What the tool does: captures a "context snapshot" when you leave a repo (what you were doing, what's incomplete, what the next step is) and surfaces it when you return
- Thumbnail: **Repo Resume** — Captures your working context when you leave a project and surfaces a "where you left off" brief when you return, so cold repo opens feel warm.

---

## Technique 3: Fascination Threading

**Name**: Fascination Threading

**When to use**: Input is too vague to project or amplify — it's more of a mood than a direction. Also use this when the fascination index contains strong recent signals that haven't been acted on yet. Most effective when the person expresses curiosity about a domain unrelated to their immediate problem ("I've been thinking about X lately").

**How it works**:

1. Read `~/.pyro/fascination-index.md` for current and recurring fascinations
2. Look for the intersection: where does the vague input *touch* a fascination theme?
3. Generate the idea that lives at that intersection — it should use vocabulary from the fascination domain to describe a software problem
4. Identify what makes this idea different from a "normal" solution to the same problem (the fascination is the differentiator)
5. Distill to a thumbnail that makes the intersection explicit

**Example**:

- Input: "I want to build something with AI but I don't know what"
- Fascination index signals: board game mechanics (recurring), emergent systems, rules that produce surprising outcomes
- Intersection: AI systems where the interesting part is the *rule structure*, not the output — like a game where the mechanics produce emergent play
- Idea: a tool for designing AI agent prompts as *game rules* — you define win conditions, turn structure, and action constraints, and the agent operates within them
- Thumbnail: **Rulebook** — Design AI agent behavior as board game mechanics: turns, win conditions, legal moves. The rules make the behavior legible and auditable without reading prompts.

---

## Technique 4: Constraint Inversion

**Name**: Constraint Inversion

**When to use**: The problem domain has obvious "that's just how it works" assumptions that everyone treats as fixed. Use this when someone is restating conventional wisdom as a constraint ("well, you can't really do X without Y"). Also effective when multiple standard approaches have been tried and failed — signals that an assumed constraint is the real obstacle.

**How it works**:

1. List 3-5 things that are "obviously true" about the problem domain
2. For each, ask: what if this weren't true?
3. Pick the inversion that produces the most interesting capability delta — the one where removing the constraint doesn't just make things easier, it makes a *different kind of tool* possible
4. Design the tool that operates in the inverted world
5. Acknowledge the real constraint and identify what would need to be true for the inversion to hold (this becomes scope or the core technical bet)

**Example**:

- Input: "I want to improve my code review process"
- Obvious constraints: (1) reviews happen after code is written, (2) reviewers need context from the author, (3) review quality depends on reviewer attention
- Most interesting inversion: what if reviews happened *during* writing, not after? (Invert constraint 1)
- Inverted world: instead of sending code to a reviewer when it's done, the reviewer's model is active *while you write* — flagging as you go, not post-hoc
- Tool: an ambient code reviewer that watches your working branch in real time and surfaces issues at the point of creation, not the point of submission
- Thumbnail: **Live Review** — An ambient reviewer that flags issues as you write rather than after you submit — turns code review from a gate into a conversation.

---

## Technique 5: Domain Transplant

**Name**: Domain Transplant

**When to use**: The problem space is mature and crowded — every obvious approach has been tried. Use this when input sounds like "a better version of [existing tool]" or when the person is stuck comparing against existing solutions. Also useful as a creativity injection when Scenario Projection and Annoyance Amplification produce predictable thumbnails.

**How it works**:

1. Identify the actual problem being solved (strip away the existing solution framing)
2. Pick a non-tech domain that has *solved an analogous problem* with its own vocabulary and structure (see `domain-lenses.md` for available lenses)
3. Apply that domain's core vocabulary to the problem: what is the "score" here? What is the "edit"? What is "mise en place"?
4. Let the domain vocabulary generate constraints that the tech framing wouldn't impose — these become features
5. Distill to a thumbnail that uses the domain metaphor as its core concept

**Example**:

- Input: "I want a better way to manage my personal knowledge base"
- Existing solution framing: smarter search, better tags, AI summaries
- Domain transplant: music (arrangement, tracks, listening sessions)
- Applying music vocabulary: notes aren't "stored," they're *arranged* — you create a "session" where you pull relevant tracks together for a specific listening purpose, then the arrangement dissolves when the session ends
- What the domain imposes: knowledge is *contextual and temporal*, not archival; you don't retrieve notes, you compose a session
- Thumbnail: **Session Notes** — Knowledge management structured around listening sessions rather than a permanent archive — you arrange notes into a temporary session for a specific context, then let it dissolve.

---

## Bonus Technique: Signal Clustering

**Name**: Signal Clustering

**When to use**: The person has given multiple disconnected inputs over time — a list of half-ideas, a set of annoyances, or a dump of "things I've been thinking about." Use this when input length is high but coherence is low. Not for single-sentence inputs.

**How it works**:

1. List all the signals from the input
2. Group them by the underlying *need* they express (not surface topic — deeper motivation)
3. Find the group with the most signals
4. The thumbnail is the tool that addresses the need the largest cluster points to
5. Name the need explicitly in the thumbnail so it's clear what was heard

**Example**:

- Input: "I keep forgetting what I was doing. I want better notes but I hate writing notes. I lose track of time when I'm in flow. I wish someone would just tell me what to do next."
- Signals: forgetting context, low-friction capture, time blindness in flow, decision fatigue about next action
- Largest cluster: external memory that requires zero active effort (forgetting + low-friction + automatic)
- Thumbnail: **Ambient Log** — Passively captures your working context from editor and terminal activity so you never have to write notes — just ask "what was I doing?" and it knows.
