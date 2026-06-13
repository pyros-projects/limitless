# hivemind - Idea Seeds & Ideation Eval Frames

*Concept spec · 2026-06-13 · first pass*

> Status: **design for review.** Sparked by volatile AI-dev social sweeps
> where the factual claims were weak but the *ideas* were valuable:
> rented inference as a control plane, harness continuity as the durable
> layer, product shutdowns as user-risk signal, and deployment freezes as
> precedent. This spec defines the Hivemind-side changes needed to extract
> idea seeds without turning chatter into fact, and to produce a dataset
> for testing ideation evaluators.

---

## The job

Hivemind already treats X/Reddit as weak evidence: good for language,
friction, sentiment, source pointers, and practitioner takes; bad as a
fact oracle. That rule is correct, but incomplete for idea discovery.

The missing move:

> Social media is weak evidence for facts, but strong ore for ideas.

A bad post can still contain a useful frame. A wrong rumor can expose a
real governance failure mode. A rant can hide a product idea. A tiny
low-engagement reply can name the thing a team has been circling for
months.

Hivemind should therefore gain an **idea seed extraction pass** that can
turn any sweep frame into auditable candidate ideas, with scores and
adversarial labels. The output is not a verified claim and not a
downstream artifact. It is a structured object that downstream systems can
validate, enrich, reject, promote, or use as eval data.

This is the bridge between:

- **Hivemind** - live discovery and raw social/web/repo/paper acquisition.
- **Social Signal Radar** - the future stateful product version of the
  loop.
- **Downstream context adapters** - project-local novelty, fit, and
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
`idea_seed_eval` objects. It does not know the user's private project
state, so context-specific fields stay absent.

Good:

- Everyone who uses Hivemind can use it.
- Works on all Hivemind frames, including old ones.
- Keeps the concept close to discovery, where the raw material lives.
- Produces a corpus suitable for ideation-eval experiments.

Bad:

- Cannot honestly score novelty against a private knowledge base or
  project roadmap.
- Cannot decide whether something should become a local artifact.
- Risks shallow "interestingness" scoring if treated as the final verdict.

### Option B - Context-local idea mining only

A project-local tool consumes Hivemind frames and does all extraction,
comparison, scoring, and promotion decisions inside one private context.

Good:

- Best contextual scores: context fit, novelty, availability-adjusted value,
  related notes, related product ideas.
- Can write local captures, tickets, specs, or queue items through that
  project's discipline.
- Lets a user point it at arbitrary piles of data, not just Hivemind
  frames.

Bad:

- Not portable; only that context benefits.
- Hivemind users elsewhere lose the feature.
- The generic dataset boundary becomes blurry because labels are already
  contaminated by one corpus.

### Option C - Split primitive: Hivemind extracts, contexts enrich

Hivemind owns a portable **idea candidate layer**. A slower project
knowledge system optionally consumes those candidates and adds contextual
enrichment.

Good:

- Hivemind stays general and lovable.
- Private projects still get serious context-aware scoring.
- Same candidate can be scored by multiple contexts later.
- Clean eval design: separate "can the agent extract the idea?" from
  "can the agent judge fit for this corpus?"
- Old frames work naturally.

Bad:

- Requires a stable interchange schema.
- Adds one more artifact to every idea-enabled frame.

**Recommendation: Option C, implemented in two steps.**

1. Add Hivemind post-hoc idea extraction and frame replay first.
2. Later add context adapters that enrich Hivemind idea seeds with
   project-local search, related artifacts, and promotion decisions.

## Skill interface

This spec is an implementation handoff for the Hivemind skill contract,
not a claim that a standalone `hivemind` binary already exists. In this
repository, "implementation" means updating the Hivemind skill instructions
and directly referenced `references/*.md` files. If a future CLI/runtime is
added, it should expose the same command shape and artifact contract.

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
hivemind ideas ~/.hivemind/model-continuity-risk/2026-06-13/
hivemind ideas ~/.hivemind/<slug>/<date>/ --format jsonl,md
```

`hivemind ideas <frame-path>` is replay mode. It reads an existing frame and
does not perform live venue acquisition.

`--format` is only a presentation/output filter for replay mode:

- `--format all` or omitted writes all artifacts.
- `--format jsonl` writes `ideas.jsonl` and `idea-rejections.jsonl`.
- `--format md` writes `ideas.md` and `idea-rejections.md`.
- comma-separated values combine those sets, so `--format jsonl,md` is the
  same as `all`.

For the first wedge, full extraction should use `all`; narrower formats are
allowed only when the user explicitly asks for a partial replay artifact.

Config line:

```yaml
idea_extraction: off | light | full
```

- `off` - default. No idea artifacts; brief may still mention natural
  next directions.
- `light` - add 3-5 unscored idea leads to the brief only. No JSONL
  artifacts are written in live sweeps. In replay mode, `--light` writes
  only a sidecar `ideas.md`.
- `full` - write full idea artifacts after the sweep.

Live ask beats config. If a config says `off` and the user asks for
ideas, ideas run. If a config says `full` and the user says "no ideas
this time", skip and propose a config delta only if the correction
sounds durable.

Flag interactions:

- `--ideas` means `idea_extraction: full` unless the user says "light".
- `repeat <slug> --ideas` runs the saved config, then performs the idea
  pass over the newly written frame.
- `--radar --ideas` runs the radar pipeline first, then writes idea
  artifacts beside the radar artifacts. `radar.json` remains unchanged.
- `--no-keep --ideas` may run, but artifacts are temporary and are not an
  eval dataset. Write them under `/tmp/hivemind-ideas-<slug>-<date>/` and
  state that they will not be durable.
- If a config sets `idea_extraction`, the live ask still wins for that run;
  only durable corrections become proposed config deltas.

## Frame contract extension

Every live sweep with `idea_extraction: full` writes the idea artifacts
before the frame is closed:

```text
~/.hivemind/<slug>/<date>/
  raw/
  manifest.md
  brief.md
  ideas.jsonl        # canonical machine-readable idea_seed_eval objects
  idea-rejections.jsonl # canonical machine-readable rejected/near-miss rows; may be empty
  ideas.md           # human-readable report
  idea-rejections.md # human-readable rejection report; says "No rejections" if empty
```

Full extraction always creates all four idea files. Empty JSONL files are
valid zero-byte files. Empty markdown reports should contain a one-line
explicit empty-state sentence rather than being omitted.

Replay mode reads an existing frame but **does not mutate it**. Existing
frames are immutable. Replay writes a sidecar run:

```text
~/.hivemind/<slug>/idea-runs/<source-date>-<run-id>/
  manifest.md
  source-frame.md
  ideas.jsonl
  idea-rejections.jsonl
  ideas.md
  idea-rejections.md
```

`run-id` is deterministic per source frame and day: start at `001`, then
increment (`002`, `003`, ...) if that sidecar directory already exists.
This makes repeated evaluator runs comparable without overwriting earlier
outputs.

`source-frame.md` records the exact source frame path, files consumed,
missing pieces, and whether live refresh was explicitly requested. The
source frame's original `manifest.md` is never edited during replay.

Replay mode preflight is file preflight, not venue preflight. It checks
that the frame path exists and that raw files can be read/parsed. It does
not probe `twitter`, `rdt`, `gh`, web, or papers unless the user asks to
refresh the frame.

For older frames:

- If `manifest.md` exists, use it for scope, queries, adaptations, and
  triage rejections.
- If `brief.md` exists, use it for synthesis context, not as a substitute
  for raw evidence.
- If only `raw/` exists, infer scope from file names and item contents,
  then state the degradation in `ideas.md`.
- Never re-search unless the user explicitly asks to refresh; replay is
  about evaluating the saved episode.

For live `full` extraction, append this block to the source frame's
`manifest.md` before the frame closes:

```yaml
idea_extraction:
  mode: full
  extractor_version: <date-or-edition>
  source_frame: self
  source_frame_mutated: true
  inputs:
    - raw/x-...
    - brief.md
  output:
    - ideas.jsonl
    - idea-rejections.jsonl
    - ideas.md
    - idea-rejections.md
  harvested_count: N        # raw possible seeds before dedupe
  selected_count: N         # rows in ideas.jsonl
  rejection_count: N        # rows in idea-rejections.jsonl
```

For replay extraction, the sidecar idea run `manifest.md` records:

```yaml
idea_extraction:
  mode: replay
  extractor_version: <date-or-edition>
  source_frame: <path>
  source_frame_mutated: false
  inputs:
    - raw/x-...
    - brief.md
  output:
    - ideas.jsonl
    - idea-rejections.jsonl
    - ideas.md
    - idea-rejections.md
  harvested_count: N        # raw possible seeds before dedupe
  selected_count: N         # rows in ideas.jsonl
  rejection_count: N        # rows in idea-rejections.jsonl
```

## The `idea_seed_eval` object

`ideas.jsonl` and `idea-rejections.jsonl` both use the same base schema.
Rows in `ideas.jsonl` have `decision.verdict` of `watch`, `candidate`, or
`validate`. Rows in `idea-rejections.jsonl` have `decision.verdict` of
`reject`, `language_only`, or `source_pointer`.

Required top-level fields:

- `schema`
- `id`
- `frame`
- `sources`
- `extraction`
- `scores`
- `adversarial_labels`
- `validation`
- `decision`
- `outcome_later`

Optional fields are represented as `null`, never by inventing private
context. Context-specific fields live in a separate adapter output.

ID rules:

- Idea IDs are deterministic within one idea run: `idea_<YYYYMMDD>_0001`,
  `idea_<YYYYMMDD>_0002`, and so on in output order.
- Rejection IDs use the same sequence with a rejection prefix:
  `rejection_<YYYYMMDD>_0001`, `rejection_<YYYYMMDD>_0002`, and so on.
- Output order is stable: sort selected candidates by verdict tier
  (`validate`, `candidate`, `watch`), then descending `idea_yield`, then
  descending `evidenceability`, then earliest source path/ID. Sort
  rejections by adversarial label, then earliest source path/ID.
- If the same idea run is repeated from the same inputs and extractor
  version, IDs should be identical.

Canonical JSONL row:

```json
{
  "schema": "hivemind.idea_seed_eval.v1",
  "id": "idea_20260613_0001",
  "frame": {
    "source_frame": "~/.hivemind/model-continuity-risk/2026-06-13/",
    "idea_run": "~/.hivemind/model-continuity-risk/idea-runs/2026-06-13-001/",
    "mode": "replay"
  },
  "sources": [
    {
      "platform": "x",
      "source_id": "2065708574433841346",
      "url": "https://x.com/example/status/2065708574433841346",
      "path": "raw/x-continuity.json",
      "title": null,
      "author": "example_author",
      "observed_at": "2026-06-13T08:11:00Z",
      "evidence_role": "primary",
      "attention_pressure": {
        "likes": 8,
        "views": 271,
        "replies": 3
      }
    }
  ],
  "extraction": {
    "raw_source_summary": "A user says a model endpoint changed but their harness survived by switching providers.",
    "extracted_idea": "Agent continuity should live in the operating harness, not in one model endpoint.",
    "fact_claims_separated": [
      "A model endpoint changed",
      "The author's harness continued on another provider"
    ],
    "reusable_frame": "endpoint loss tests whether the system or the model owned continuity",
    "why_interesting": "Turns endpoint volatility into an architecture principle."
  },
  "scores": {
    "novelty_within_frame": { "score": 4, "rationale": "Rare among the sources in this frame, not just a repeated slogan." },
    "idea_yield": { "score": 5, "rationale": "Could become an insight, product spec, and article frame." },
    "evidenceability": { "score": 4, "rationale": "Can be tested by model-swap harness runs." },
    "feasibility": { "score": 4, "rationale": "Cheap to evaluate with existing saved workflows." },
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
    "rationale": "Strong idea, but Hivemind should not decide project-specific promotion.",
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

`sources` is always an array, even for one source. Multi-source clusters
append one source object per receipt.

Source object fields:

- `platform`: `x | reddit | github | web | paper | brief | manifest | other`
- `source_id`: source-native ID when available, else `null`
- `url`: canonical URL when available, else `null`
- `path`: frame-local path to the raw/deep-read/brief file
- `title`: source title, repo name, paper title, or thread title when available
- `author`: author/org/source name when available
- `observed_at`: ISO timestamp when known, else `null`
- `evidence_role`: `primary | supporting | counterexample | language | pointer`
- `attention_pressure`: object with platform-native engagement fields, or `null`

`attention_pressure` examples:

```yaml
x: { likes: 120, reposts: 9, replies: 4, views: 8200 }
reddit: { score: 233, comments: 157, upvote_ratio: 0.91 }
github: { stars: 1840, forks: 120, pushed_at: "2026-06-13T08:00:00Z" }
web: { rank_hint: 3, domain: "example.com" }
paper: { citations: 12, venue: "arxiv", published_at: "2026-06-01" }
```

Missing or unavailable engagement fields are omitted rather than guessed.

Score directions:

- `novelty_within_frame`: 1 = repeated everywhere in this frame, 5 =
  surprising relative to the frame's own sources. This is not project-level
  novelty.
- `idea_yield`: 1 = inert, 5 = likely to become an insight/spec/article/
  experiment.
- `evidenceability`: 1 = vague vibe, 5 = cheaply testable or source-checkable.
- `feasibility`: 1 = too expensive or unclear, 5 = cheap next action.
- `availability_adjusted_value`: 1 = obvious zeitgeist, 5 = coherent idea
  outside the current community prior.
- `source_contamination`: 1 = idea survives false source claims, 5 = idea
  collapses if the post's factual premise is false.
- `attention_pressure`: raw metadata only. Never part of a composite score.

Enums:

- `decision.verdict`: `reject | language_only | source_pointer | watch |
  candidate | validate`
- `decision.evidence_cap`: `social_only | source_pointer |
  primary_followed | verified | tested`
- `outcome_later.status`: `unreviewed | reviewed | outcome_labeled`
- `outcome_later.became`: `null | none | insight | capture | spec |
  article | experiment | product_change | config_change`

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
   labels, and validation suggestions. Do not fill project-specific novelty,
   fit, or promotion fields in the Hivemind artifact.
6. **Write artifacts.** `ideas.jsonl` and `idea-rejections.jsonl` are the
   canonical machine-readable outputs; `ideas.md` and `idea-rejections.md`
   are operator-readable summaries.
7. **Optional context handoff.** If the user asks for project-specific
   enrichment, pass `ideas.jsonl` and `idea-rejections.jsonl` to a context
   adapter. Hivemind itself remains read-only with respect to external
   projects and knowledge bases.

## Output shape

`ideas.md` starts answer-first:

1. **TL;DR** - how many candidates, how many gems, what the strongest
   idea family is.
2. **Best seeds** - 3-7 idea seeds with source receipts, extracted idea,
   why interesting, score sketch, and recommended next check.
3. **Adversarial cases** - viral-but-dumb, false-premise-useful, true-but-
   boring, low-engagement gem, if present.
4. **Dataset notes** - which cases are good eval examples and why.
5. **Context handoff** - what a project-specific enricher should do next.
6. **Coverage** - frame path, files consumed, degradations, old-run status.

The human report should not render a fake precision leaderboard. Scores are
for filtering, calibration, and future evals; the prose rationale is the
artifact that makes them auditable.

## Relationship to context adapters

Hivemind should stop at portable extraction:

- It can score generic idea-yield, feasibility, evidenceability, source
  contamination, and availability-adjusted value.
- It can separate facts from frames.
- It can propose cheapest validation steps.
- It can label adversarial cases.
- It can write replayable datasets.

It should not pretend to know:

- novelty relative to a private knowledge base,
- whether an idea should become a project artifact,
- which local product idea it overlaps,
- which local capture/ticket/spec path should receive it,
- whether a project's current state makes it urgent.

Those belong to a downstream context adapter. The adapter takes the
Hivemind files as input and writes a separate enrichment file keyed by
`idea_seed_eval.id`; it does not mutate the original Hivemind JSONL.

```yaml
context_enrichment.v1:
  source_ideas: ideas.jsonl
  context_name: <project-or-knowledge-base>
  adapter_version: <date-or-edition>
  rows:
    - idea_id: idea_20260613_0001
      novelty_vs_context: 1-5
      context_fit: 1-5
      related_artifacts:
        - <path-or-url>
      promotion_decision: reject | watch | capture | validate | spec | article
      suggested_destination: <path-or-url-or-null>
      rationale: <why this context cares or does not care>
```

This keeps Hivemind portable while making it a first-class acquisition
feed for slower project knowledge systems.

## Ideation eval dataset

The same artifacts become test data.

Each `idea_seed_eval` row can be upgraded over time by updating
`outcome_later`:

```yaml
outcome_later:
  status: unreviewed | reviewed | outcome_labeled
  human_verdict: null | bad_extract | okay | good | gem
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

The killer metric is not "did it generate ideas?" It is whether selected
seeds later produce artifacts, experiments, or project decisions, and
whether that yield decorrelates from engagement.

## Quality gates

1. **Post-hoc replay gate.** The extractor must work on a saved old frame
   without live search.
2. **Fact/frame separation gate.** Every candidate with factual claims must
   list those claims separately from the extracted idea.
3. **Attention decorrelation gate.** A full pass must be able to select at
   least one low-engagement gem or reject at least one high-engagement dud
   when the frame contains such cases.
4. **Evidence cap gate.** Social-only candidates cannot be rendered as
   verified claims. High idea score is allowed; high truth confidence is not.
5. **Near-miss gate.** Full extraction records rejections with reasons.
6. **Context honesty gate.** Project-specific fields stay out of Hivemind
   artifacts unless a context adapter actually ran, and adapter output is
   written separately.
7. **Old-frame degradation gate.** Missing manifest/brief/raw pieces are
   stated in the output, not silently ignored.

## Non-goals

- No automatic downstream import.
- No generic trend dashboard.
- No composite "idea score" that hides the dimensions.
- No claim verification unless the user asks for verification or a context
  adapter runs it.
- No replacing Hivemind's main answer-first brief with idea paperwork.
- No treating engagement as truth.
- No making Hivemind depend on any private project, memory system, or
  knowledge graph.

## Implementation wedge

Smallest useful version:

1. Add the concept of `idea_extraction: off | light | full` to the skill
   contract and config template.
2. Add replay-mode instructions: `hivemind ideas <frame-path>`.
3. Define `idea_seed_eval.v1` as the JSONL schema.
4. Teach the skill to produce `ideas.jsonl`, `idea-rejections.jsonl`,
   `ideas.md`, and `idea-rejections.md` from one frame.
5. Add the contract to `plugins/limitless/skills/hivemind/SKILL.md` and,
   if it grows large, a directly referenced `references/idea-seeds.md`.
6. Test on two saved frames or synthetic fixtures that satisfy the fixture
   contract below.

Context adapters are explicitly **not part of the first wedge**. The first
wedge only defines the handoff surface that adapters can consume later.

For this document, the "Hivemind runtime docs" are the Hivemind
`SKILL.md` plus directly referenced files in its `references/` directory.
There is no separate runtime document required for the first wedge.

Fixture contract:

- Fixture A contains at least one low-engagement but high-yield idea.
- Fixture B contains at least one high-engagement but low-yield item.
- Fixture C contains at least one false-premise-useful or rumor-useful idea.
- Fixture D contains at least one source-pointer-only item.
- At least one fixture includes multiple sources that cluster into one idea.

Real saved frames are preferred. If the named frames are unavailable, create
minimal synthetic frames under `/tmp/hivemind-idea-fixtures/` with
`manifest.md`, `brief.md`, and `raw/*.json` that exercise the same cases.

Graduation criterion:

- From the fixture set, the pass should produce at least:
  - one low-engagement gem,
  - one false-premise-useful or rumor-useful idea,
  - one high-attention rejection,
  - one validation-ready idea,
  - one multi-source clustered idea,
  - one context-handoff candidate with no private context filled in.

If it cannot do that on a fixture set built from real or synthetic saved
frames, the feature is probably ceremony. If it can, Social Signal Radar
has its first hard proof.
