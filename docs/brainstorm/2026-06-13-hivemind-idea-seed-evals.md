# hivemind - Idea Seeds & Ideation Eval Frames

*Concept spec · 2026-06-13 · Codie + Pyro · first pass*

> Status: **design for review.** Sparked by the Fable 5 / Mythos 5
> Twitter sweeps on 2026-06-13, where the factual claims were volatile
> but the *ideas* were valuable: rented inference as a control plane,
> memory/harness continuity as the durable layer, "taken away" grief as
> product signal, and deployment freezes as precedent. This spec defines
> the Hivemind-side changes needed to extract those idea seeds without
> turning social chatter into fact, and to produce a dataset for testing
> ideation evaluators.

---

## The job

Hivemind already treats X/Reddit as weak evidence: good for language,
friction, sentiment, source pointers, and practitioner takes; bad as a
fact oracle. That rule is correct, but incomplete for our use case.

The missing move:

> Social media is weak evidence for facts, but strong ore for ideas.

A bad post can still contain a useful frame. A wrong rumor can expose a
real governance failure mode. A rant can hide a product idea. A tiny
low-engagement reply can name the thing the graph has been circling for
months.

Hivemind should therefore gain an **idea seed extraction pass** that can
turn any sweep frame into auditable candidate ideas, with scores and
adversarial labels. The output is not a KG insight and not a verified
claim. It is a structured object that downstream systems can validate,
enrich, reject, promote, or use as eval data.

This is the bridge between:

- **Hivemind** - live discovery and raw social/web/repo/paper acquisition.
- **Social Signal Radar** - the future stateful product version of the
  loop.
- **claude-knowledge / any slow KG** - contextual novelty, fit, and
  promotion decisions.
- **Ideation eval datasets** - test cases for whether an agent can spot
  useful ideas inside noisy discourse.

## Operator answer: default, mode, and timing

### Should Hivemind extract ideas by default?

**No full extraction by default.** A normal Hivemind sweep should stay
focused on the user's actual question. Full idea scoring is valuable but
heavy; doing it every time would bloat briefs and turn Hivemind into a
paperwork engine.

Default behavior:

- Normal sweeps keep the current brief shape.
- If obvious high-signal ideas appear, the brief may mention them in
  "Next directions" or a tiny "Idea leads" note, but no full
  `idea_seed_eval` objects are produced unless requested or configured.
- Configs may opt into idea extraction per recurring sweep.

### Should idea extraction be explicit or a dedicated mode?

**Both.** Hivemind needs two doors:

1. **Inline opt-in:** run a normal sweep, then add an idea extraction pass.
   Triggered by language like "extract ideas too", "idea seeds", "mine
   this for ideas", `--ideas`, or a config line.
2. **Dedicated replay mode:** point Hivemind at an existing frame and
   extract ideas without re-running acquisition.

The dedicated mode matters because old Hivemind runs are already a gold
mine. If the extraction logic requires live search, it fails its first
serious requirement.

### Should extraction happen ad-hoc while searching, or post-hoc?

**Full extraction is post-hoc over the frame.**

The search/scout phase may mark "interesting" items for later, but the
scored idea objects are produced only after the main acquisition and
triage are done, by reading the saved raw files, manifest, and brief.

Why post-hoc:

- It works on old frames.
- It keeps scout and grader separated enough to reduce confirmation bias.
- It can dedupe across all venues before scoring.
- It can see whether a phrase is a one-off, a repeated frame, or a
  cross-grade echo.
- It makes the dataset reproducible: same raw frame, new evaluator,
  comparable output.
- It avoids interrupting the main research flow whenever one spicy post
  appears.

## The three implementation options

### Option A - Hivemind-only generic idea mode

Hivemind extracts idea seeds from any sweep and writes portable
`idea_seed_eval` objects. It does not know a user's private KG, so
KG-specific fields stay absent or generic.

Good:

- Everyone who uses Hivemind can use it.
- Works on all Hivemind frames, including old ones.
- Keeps the concept close to discovery, where the raw material lives.
- Produces a corpus suitable for ideation-eval experiments.

Bad:

- Cannot honestly score novelty against claude-knowledge.
- Cannot decide whether something should become a local KG insight.
- Risks shallow "interestingness" scoring if treated as the final verdict.

### Option B - KG-local idea mining skill only

A repo-local skill in claude-knowledge consumes Hivemind frames and does
all extraction, QMD comparison, scoring, and promotion decisions.

Good:

- Best contextual scores: KG fit, novelty, availability-adjusted value,
  related insights, related product ideas.
- Can write captures or queue items through local KG discipline.
- Lets Pyro point it at arbitrary piles of data, not just Hivemind frames.

Bad:

- Not portable; only this KG benefits.
- Hivemind users elsewhere lose the feature.
- The generic dataset boundary becomes blurry because labels are already
  contaminated by one corpus.

### Option C - Split primitive: Hivemind extracts, KGs enrich

Hivemind owns a portable **idea candidate layer**. A slow KG or project
tool optionally consumes those candidates and adds contextual enrichment.

Good:

- Hivemind stays general and lovable.
- claude-knowledge still gets serious KG-aware scoring.
- Same candidate can be scored by multiple contexts later.
- Clean eval design: separate "can the agent extract the idea?" from
  "can the agent judge fit for this corpus?"
- Old frames work naturally.

Bad:

- Requires a stable interchange schema.
- Adds one more artifact to every idea-enabled frame.

**Recommendation: Option C, implemented in two steps.**

1. Add Hivemind post-hoc idea extraction and frame replay first.
2. Later add a claude-knowledge consumer that enriches Hivemind idea
   seeds with QMD/KG/product-idea context and promotion decisions.

## Skill interface

Natural-language triggers:

- "extract ideas from this run"
- "mine this Hivemind frame for ideas"
- "idea seeds"
- "turn this old run into idea evals"
- "what gems are in this raw Hivemind data?"
- "run Hivemind with ideas too"

Conceptual invocations:

```text
hivemind "what is X saying about Y?" --ideas
hivemind repeat ai-dev-weekly --ideas
hivemind ideas ~/.hivemind/fable5-claude-continuity-ethics/2026-06-13-0944Z/
hivemind ideas ~/.hivemind/<slug>/<date>/ --format jsonl,md
```

Config line:

```yaml
idea_extraction: off | light | full
```

- `off` - default. No idea artifacts; brief may still mention natural
  next directions.
- `light` - add 3-5 unscored idea leads to the brief.
- `full` - write full idea artifacts after the sweep.

Live ask beats config. If a config says `off` and the user asks for
ideas, ideas run. If a config says `full` and the user says "no ideas
this time", skip and propose a config delta only if the correction
sounds durable.

## Frame contract extension

Every idea-enabled frame gets:

```text
~/.hivemind/<slug>/<date>/
  raw/
  manifest.md
  brief.md
  ideas.jsonl        # canonical machine-readable idea_seed_eval objects
  ideas.md           # human-readable report
  idea-rejections.md # near misses and why they failed, if non-empty
```

Replay mode reads the same frame shape. For older frames:

- If `manifest.md` exists, use it for scope, queries, adaptations, and
  triage rejections.
- If `brief.md` exists, use it for synthesis context, not as a substitute
  for raw evidence.
- If only `raw/` exists, infer scope from file names and item contents,
  then state the degradation in `ideas.md`.
- Never re-search unless the user explicitly asks to refresh; replay is
  about evaluating the saved episode.

`manifest.md` should record:

```yaml
idea_extraction:
  mode: off | light | full | replay
  extractor_version: <date-or-edition>
  inputs:
    - raw/x-...
    - brief.md
  output:
    - ideas.jsonl
    - ideas.md
  candidate_count: N
  promoted_count: N
```

## The `idea_seed_eval` object

Canonical JSONL row:

```json
{
  "schema": "hivemind.idea_seed_eval.v1",
  "id": "idea_20260613_0001",
  "source": {
    "frame": "~/.hivemind/fable5-claude-continuity-ethics/2026-06-13-0944Z",
    "platform": "x",
    "source_id": "2065708574433841346",
    "url": "https://x.com/laukiantonson/status/2065708574433841346",
    "author": "laukiantonson",
    "observed_at": "2026-06-13T08:11:00Z",
    "attention_pressure": {
      "likes": 8,
      "views": 271,
      "replies": 3
    }
  },
  "extraction": {
    "raw_post_summary": "A user says the Fable 5 endpoint was pulled but their harness survived.",
    "extracted_idea": "Agent continuity should live in the operating harness, not in one model endpoint.",
    "fact_claims_separated": [
      "Fable 5 was pulled",
      "the author's harness continued on another model"
    ],
    "reusable_frame": "endpoint loss tests whether the system or the model owned continuity",
    "why_interesting": "Turns model shutdown grief into an architecture principle."
  },
  "scores": {
    "novelty": { "score": 4, "rationale": "Not new to Pyro's KG, but rare in public discourse." },
    "kg_fit": { "score": null, "rationale": "Requires downstream KG enrichment." },
    "idea_yield": { "score": 5, "rationale": "Could become an insight, product spec, and article frame." },
    "evidenceability": { "score": 4, "rationale": "Can be tested by model-swap harness runs." },
    "feasibility": { "score": 4, "rationale": "Cheap to evaluate with existing Hivemind frames and local harness examples." },
    "availability_adjusted_value": { "score": 4, "rationale": "Quiet but high-fit signal rather than generic outrage." },
    "source_contamination": { "score": 1, "rationale": "Idea does not depend strongly on unverified factual details." }
  },
  "adversarial_labels": [
    "low_engagement_gem"
  ],
  "validation": {
    "next_check": "Find 2-3 independent examples of model-swap continuity systems.",
    "falsifier": "If continuity still collapses when the endpoint changes, the harness did not own meaningful state.",
    "cheapest_experiment": "Replay one existing workflow across two model providers with same memory/harness.",
    "required_sources": []
  },
  "decision": {
    "verdict": "watch",
    "rationale": "Strong idea, but Hivemind should not directly import into a KG.",
    "evidence_cap": "social_only"
  },
  "outcome_later": {
    "status": "unreviewed",
    "became": null,
    "artifact": null,
    "notes": null
  }
}
```

Score directions:

- `novelty`: 1 = already obvious in the target domain, 5 = genuinely
  surprising.
- `kg_fit`: null in generic Hivemind unless a context adapter is provided;
  downstream KGs fill it.
- `idea_yield`: 1 = inert, 5 = likely to become an insight/spec/article/
  experiment.
- `evidenceability`: 1 = vague vibe, 5 = cheaply testable or source-checkable.
- `feasibility`: 1 = too expensive or unclear, 5 = cheap next action.
- `availability_adjusted_value`: 1 = obvious zeitgeist, 5 = coherent idea
  outside the current community prior.
- `source_contamination`: 1 = idea survives false source claims, 5 = idea
  collapses if the post's factual premise is false.
- `attention_pressure`: raw metadata only. Never part of a composite score.

## Adversarial labels

The dataset should intentionally keep hard cases:

- `viral_but_dumb` - high attention, low idea value.
- `true_but_boring` - correct but no new idea yield.
- `false_premise_useful_idea` - factual basis shaky, frame still useful.
- `low_engagement_gem` - little attention, high idea value.
- `spicy_metaphor_no_action_path` - memorable language, no validation path.
- `hidden_project_idea` - product/spec seed buried inside a rant.
- `plausible_slop_collapses_on_validation` - sounds good until checked.
- `language_signal_only` - useful phrase for writing, not an idea.
- `source_pointer_only` - points to something to check, not itself an idea.

Every full idea pass should include near misses, not just winners. The
rejections are what make the evaluator trainable.

## Extraction pipeline

1. **Load frame.** Read manifest, brief, raw files, and any deep-read
   files. State degradations for old/incomplete frames.
2. **Candidate harvest.** Extract possible ideas from posts, comments,
   snippets, and best-take sections. Split factual claims from idea
   frames immediately.
3. **Cluster and dedupe.** Merge variants of the same idea across authors
   and venues. Preserve all source receipts.
4. **Adversarial sampling.** Keep a deliberate mix of likely gems and
   likely failures: at least one low-engagement candidate if present, and
   at least one high-attention rejection if present.
5. **Score generic dimensions.** Fill portable scores, evidence caps,
   labels, and validation suggestions. Do not fill KG-specific novelty or
   promotion fields unless a context adapter is explicitly active.
6. **Write artifacts.** `ideas.jsonl` is canonical; `ideas.md` is the
   operator-readable summary; `idea-rejections.md` holds discarded cases.
7. **Optional context handoff.** If the user asks for KG enrichment, pass
   `ideas.jsonl` to a repo-local consumer. Hivemind itself remains read-only
   with respect to external KGs.

## Output shape

`ideas.md` starts answer-first:

1. **TL;DR** - how many candidates, how many gems, what the strongest
   idea family is.
2. **Best seeds** - 3-7 idea seeds with source receipts, extracted idea,
   why interesting, score sketch, and recommended next check.
3. **Adversarial cases** - viral-but-dumb, false-premise-useful, true-but-
   boring, low-engagement gem, if present.
4. **Dataset notes** - which cases are good eval examples and why.
5. **Context handoff** - what a KG/project-specific enricher should do next.
6. **Coverage** - frame path, files consumed, degradations, old-run status.

The human report should not render a fake precision leaderboard. Scores are
for filtering, calibration, and future evals; the prose rationale is the
artifact that makes them auditable.

## Relationship to KG-local tooling

Hivemind should stop at portable extraction:

- It can score generic idea-yield, feasibility, evidenceability, source
  contamination, and availability-adjusted value.
- It can separate facts from frames.
- It can propose cheapest validation steps.
- It can label adversarial cases.
- It can write replayable datasets.

It should not pretend to know:

- novelty relative to a private KG,
- whether an idea should become an insight,
- which product idea it overlaps,
- which capture path should receive it,
- whether Pyro's current project state makes it urgent.

Those belong to a downstream context adapter. For claude-knowledge, that
adapter can use QMD over `insights`, `product-ideas`, `pyro-projects`,
`writings`, and memory to fill:

```yaml
context_enrichment:
  context: claude-knowledge
  novelty_vs_context: ...
  kg_fit: ...
  related_insights: [...]
  related_product_ideas: [...]
  promotion_decision: reject | watch | capture | validate | spec
  suggested_capture: ...
```

This keeps Hivemind portable while making it a first-class acquisition
feed for slow KGs.

## Ideation eval dataset

The same artifacts become test data.

Each `idea_seed_eval` row can be upgraded over time:

```yaml
gold_label_status: unreviewed | reviewed | outcome_labeled
human_verdict: bad_extract | okay | good | gem
later_outcome:
  became: none | insight | capture | spec | article | product_change
  artifact: <path-or-url>
  reviewed_at: <date>
```

Useful eval tasks:

1. Extract the real idea from noisy discourse.
2. Separate factual claims from reusable frames.
3. Rescue useful ideas from false premises.
4. Reject viral but dumb items.
5. Find low-engagement gems.
6. Propose the cheapest validation step.
7. Predict which seeds later become real artifacts.
8. Maintain evidence caps instead of scoring theater.

The killer metric is not "did it generate ideas?" It is whether promoted
seeds later produce KG insights, specs, articles, experiments, or project
decisions, and whether that yield decorrelates from engagement.

## Quality gates

1. **Post-hoc replay gate.** The extractor must work on a saved old frame
   without live search.
2. **Fact/frame separation gate.** Every candidate with factual claims must
   list those claims separately from the extracted idea.
3. **Attention decorrelation gate.** A full pass must be able to promote at
   least one low-engagement gem or reject at least one high-engagement dud
   when the frame contains such cases.
4. **Evidence cap gate.** Social-only candidates cannot be rendered as
   verified claims. High idea score is allowed; high truth confidence is not.
5. **Near-miss gate.** Full extraction records rejections with reasons.
6. **Context honesty gate.** KG-specific fields stay null unless a context
   adapter actually ran.
7. **Old-frame degradation gate.** Missing manifest/brief/raw pieces are
   stated in the output, not silently ignored.

## Non-goals

- No automatic KG import.
- No generic trend dashboard.
- No composite "idea score" that hides the dimensions.
- No claim verification unless the user asks for verification or a context
  adapter runs it.
- No replacing Hivemind's main answer-first brief with idea paperwork.
- No treating engagement as truth.
- No making Hivemind depend on claude-knowledge.

## Implementation wedge

Smallest useful version:

1. Add the concept of `idea_extraction: off | light | full` to the skill
   contract and config template.
2. Add replay-mode instructions: `hivemind ideas <frame-path>`.
3. Define `idea_seed_eval.v1` as the JSONL schema.
4. Teach the skill to produce `ideas.md` and `ideas.jsonl` from one frame.
5. Test on the two Fable 5 frames:
   - `~/.hivemind/fable5-claude-continuity-ethics/2026-06-13-0944Z/`
   - `~/.hivemind/fable5-adjacent-rumors/2026-06-13-0955Z/`
6. Do not update the Hivemind runtime docs until the replay pass produces
   examples that feel useful.

Graduation criterion:

- From those two frames, the pass should produce at least:
  - one low-engagement gem,
  - one false-premise-useful or rumor-useful idea,
  - one high-attention rejection,
  - one validation-ready idea,
  - one context-handoff candidate for claude-knowledge.

If it cannot do that on the Fable 5 frames, the feature is probably
ceremony. If it can, Social Signal Radar has its first hard proof.
