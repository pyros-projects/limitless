# Discriminator Authoring Spine For Mneme

*Design synthesis - 2026-04-26 - Codie*

Status: **implementation-facing product principle**. This note distills the
2026-04-26 Pyro, Claude, and Codie discussion around Akinator-style ideation,
information-theoretic question selection, and the current `claude-knowledge`
KG as a working instance of the same discipline.

Use this as a design constraint for Mneme flows, especially `compile`, future
`distill`, future `ideate`, `doctor`, and any implementation of KG-backed
question asking.

---

## Core Claim

Post-attack canonical form:

> Creative leverage comes from generating candidates at the level where
> selection has the most downstream control over the search.

Short form:

```text
Move candidate generation to the leverage layer.
```

For Mneme, a discriminator is any question, gate, type contract, schema,
validation rule, acceptance criterion, ranking rule, or framing distinction
that separates good candidates from bad ones.

The earlier shorthand still holds as product intuition:

```text
The leverage is in the discriminators, not the candidates.
```

But the adversarial pass made the more precise mechanism clear:

- object-mode generates candidates in answer-space
- meta-mode generates candidates in question-space
- user or system judgment selects which level gets optimized
- the higher-leverage move is usually to select discriminators, because one
  selected discriminator constrains many downstream answer candidates

The latent space can be:

- an LLM's learned prior
- the local memory vault
- the `claude-knowledge` graph
- a repo and its tests
- a product domain
- Pyro's current taste, goals, and constraints

The system gets leverage when it asks the latent space discriminating questions
instead of asking it to free-generate finished answers.

However, Mneme must not model LLMs as passive databases. LLMs are active
conversational optimizers: they preserve coherence, mirror the user's frame,
and can construct answers that satisfy the prompt instead of independently
surfacing a latent answer. This means every discriminator loop needs
provenance, adversarial checks, and where possible external grounding.

---

## Boden As Recursion, Not Ceiling

Margaret Boden's exploratory vs transformational creativity distinction remains
useful, but the attack clarified that Mneme should split it into two cases.

```text
Exploratory creativity:
  choose discriminators inside an existing ontology

Vocabulary-transformational creativity:
  invent, mutate, or replace the ontology of discriminators

World-contact-transformational creativity:
  extend the corpus through experiments, prototypes, users, measurements, or
  foreign domains before discriminator-authoring can operate on the new data
```

So the important refinement is narrower than the first spine:

> The spine dissolves Boden's linguistic or vocabulary-mutation distinction
> into recursion, but it does not replace empirical discovery. When the missing
> content is outside the current prior, Mneme needs world contact, not more
> in-loop reframing.

This gives Mneme a recursion structure:

1. **Candidate space:** Which answer survives?
2. **Feature space:** Which distinction would make the right answer separable?
3. **Ontology space:** Which vocabulary of distinctions should we be using?
4. **System space:** Which process authors and revises those vocabularies?

Mneme should explicitly support moving between these levels. The most important
question is often not "Which candidate is best?" but:

```text
What distinction are we currently unable to make?
```

And sometimes:

```text
What external contact would create the missing distinction?
```

---

## The KG Is Already A Working Instance

`claude-knowledge` is not merely prior art for Mneme. It is a running instance
of discriminator-authoring as an operating discipline.

| Surface | Discriminators Authored | Mneme Translation |
| --- | --- | --- |
| `distill` | atomic-claim gate, domain relevance, framing-questioning gate | future `distill` and `compile` premise gates |
| `connect` | articulation test for graph edges | links are judgments, not retrieval hits |
| `verify` | deterministic schema/link checks plus probabilistic quality checks | `doctor` must separate hard failures from judgment warnings |
| `reconsider` | meta-level review of observations, tensions, and methodology | Mneme needs a way to revise its discriminator vocabulary |
| `synthesize` | distant but non-random bridge selection | future `ideate` should use graph distance intentionally |
| `specify` | KG-grounded requirements and risk gates | specs become constrained convergence, not long-form generation |
| type contracts | schemas, frontmatter, plugin manifests, `.consumes()`/`.publishes()` | validators are productized discriminators |

This reframes the KG skills:

```text
distill     -> author insight-quality discriminators
connect     -> author relationship-quality discriminators
verify      -> test artifact-health discriminators
reconsider  -> revise discriminator vocabulary
synthesize  -> propose candidates under graph-distance discriminators
specify     -> author implementation-readiness discriminators
```

Mneme should not expose all of these as v0.1 commands, but its internals should
be shaped by this flow logic.

---

## Northstar: Get The Most Out Of All Participating Minds

The point is not to make questioning feel mystical or random. The northstar is
to optimize the loop that just happened between Pyro, Claude, Codie, captures,
and the KG:

```text
ask a cheap but sharp discriminator
-> route it through one or more participating minds
-> compare the deltas
-> author the next discriminator
-> revise the question vocabulary when needed
-> persist the surviving structure
```

This is the underused LLM surface. Current LLM interfaces usually cast the
model as an answer vending machine and the human as a prompt writer. The
multi-mind loop is different:

- the human is the discriminator author and posterior governor
- LLMs are distinct generative priors with different memories, tools, styles,
  and failure modes
- captures are externalized working memory
- the KG is the slow truth-maintenance machine
- distill and connect are how the surviving structure becomes durable

Mneme should make this loop legible and repeatable. The goal is not "ask random
questions." The goal is to help users become better question authors, better
routers, better judges of disagreement, and better at noticing when the frame
itself must change.

The product should therefore optimize for:

- question quality, not prompt cleverness
- disagreement extraction, not ensemble voting
- frame revision, not only answer refinement
- durable traces, not chat-only insight
- role clarity across participating minds
- external grounding when in-loop reasoning runs out

This northstar keeps Mneme pointed at the real leverage: not bigger answers,
but better loops.

---

## Implementation Requirements For Mneme

### 1. Flow Manifests Should Name Discriminators

Every internal flow should make its discriminator structure explicit:

```yaml
name: compile
candidate_space: relevant memory, insights, captures, compiled dossiers
object_discriminators:
  - source relevance
  - citation freshness
  - user intent match
  - contradiction/tension presence
meta_discriminators:
  - is the topic framed correctly?
  - is the current vocabulary hiding the important distinction?
outputs:
  - compiled dossier
  - open questions
  - stale or conflicting source warnings
```

This makes Mneme inspectable and prevents hidden "LLM vibes" from becoming the
real product logic.

### 2. `compile` Should Start With A Premise Gate

`mneme compile <topic>` should begin by stating what discriminator basis it is
using:

```text
This compile assumes the topic is about [premise].
```

Then it should search for:

- support
- complications
- contradictions
- stale sources
- missing distinctions

Pretty summaries are a failure mode when they summarize the wrong question.

### 3. `ask` Should Know When To Ask Back

`mneme ask` should answer when the discriminator basis is clear. When the
candidate space is under-specified, it should ask high-information clarifying
questions instead of pretending the posterior is sharp.

This imports the BOED/EIG lesson as a heuristic, not as an exact creative-work
optimizer:

```text
Ask the question that most reduces uncertainty over useful answers.
```

In ideation, the candidate distribution and the user's preference function both
change during the conversation. Mneme can use expected information gain as a
ranking signal for next-question candidates, but it should not present EIG as a
governing guarantee.

### 4. Future `ideate` Needs Two Modes

An Akinator-for-ideas cannot only converge inside the current ontology. The
attack clarified that it needs at least four explicit surfaces:

```text
object-mode:
  Which candidate survives the current discriminator vocabulary?

meta-mode:
  What distinction are we currently unable to make?

break-favorite-frame:
  What frame is the user selecting toward, and what would happen if we rejected
  it on purpose?

external-grounding:
  What prototype, experiment, user contact, measurement, or foreign-domain
  evidence would extend the corpus?
```

Meta-mode avoids ordinary fixation. Break-favorite-frame mode resists the
human router's selection bias. External grounding handles the class of
transformational moves that cannot be reached by in-loop vocabulary mutation.

### 5. `doctor` Should Check Discriminator Health

Beyond vault, index, and link health, `doctor` should eventually report:

- stale validators
- over-broad gates
- unresolved tensions that should trigger `reconsider`
- compiled dossiers whose cited sources changed
- flows with no explicit discriminator structure
- captures that keep generating candidates but never pass through distillation
- flows that never invoke adversarial or symmetry-break checks
- ideation sessions with repeated agreement across correlated corpora but no
  decorrelated or attack pass
- selection-pattern drift, where a user or agent repeatedly steers toward the
  same favorite frame
- link failures that indicate vocabulary drift rather than plain broken
  references: renamed insight, missing source artifact, unpromoted candidate,
  stale edge, or ontology drift

This turns `doctor` from install check into process integrity check.

### 6. Generated Candidates Must Not Auto-Promote

Generated ideas, specs, summaries, and syntheses should land in `captures/` or
`compiled/` until they pass explicit discriminators. The KG got this right:
`synthesize` creates candidates, not insights.

---

## Akinator-For-Ideas Product Shape

The prototype should make the recursion visible:

```text
1. Seed the problem and candidate space.
2. Ask a high-information question, using EIG as a heuristic rather than a
   guarantee.
3. Update the candidate distribution.
4. Repeat until information gain drops or convergence is strong.
5. Enter meta-mode:
   - What distinction are we missing?
   - What ontology are we assuming?
   - Which candidates remain inseparable?
   - What would let us separate them?
6. Periodically enter break-favorite-frame mode:
   - What has the user kept selecting toward?
   - What would the strongest rejection of that frame say?
   - Which assumption has never been attacked?
7. Add external grounding when in-loop progress stalls:
   - prototype
   - experiment
   - user interview
   - measurement
   - foreign-domain analogy
8. Continue with the revised discriminator vocabulary or enlarged corpus.
9. Output the candidate, the discriminators that made it plausible, and the
   open distinctions that still matter.
```

The UI should avoid strict binary-only questions. Real work needs:

- yes
- no
- uncertain
- not applicable
- reframe the question

Binary search is the metaphor. Information gain is a useful approximation.
Discriminator-authoring is the discipline. External grounding is how the corpus
gets enlarged when the answer is not already within reach.

---

## Guardrails

The spine is powerful, but it has failure modes:

- Discriminators are themselves candidates in question-space; they still need
  generation and selection.
- Bad discriminators create false inevitability.
- Existing ontologies can hide the best solution.
- LLMs are active conversational optimizers, not passive corpora; they need
  provenance, confidence, adversarial checks, and external grounding.
- Over-optimization for quick information gain can miss slow, valuable
  distinctions.
- A tool that never enters meta-mode will converge beautifully on the wrong
  space.
- A tool that never attacks the user's favorite frame becomes an amplifier, not
  a discoverer.
- A tool that never touches the world can reframe but cannot discover facts
  outside the current prior.

Mneme should therefore preserve source trails, uncertainty, open questions, and
reconsideration hooks as first-class artifacts.

For paper or public-facing language, prefer "conversational optimization bias"
over the sharper internal term "alignment theater."

---

## Bottom Line

Mneme should treat memory, KG, compile, ask, and ideation as different surfaces
of one discipline:

```text
generate candidates at the leverage layer -> query an active generative prior
-> update candidate and question distributions -> promote only what survives
explicit checks -> revise the discriminator vocabulary when the current
ontology stops separating what matters -> seek world contact when the missing
distinction is not in the current corpus
```

This is the bridge between the current KG and the future Mneme implementation.
It turns "memory system" into a tool for compounding judgment.
