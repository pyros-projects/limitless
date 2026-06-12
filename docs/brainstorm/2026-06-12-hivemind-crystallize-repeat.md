# hivemind — Configs by Demonstration & Pivot Chains

*Brainstorm · 2026-06-12 · Claude (Fable 5) + Pyro · one concept, second pass*

> Status: **design for review.** Both halves were exposed by the same
> 2026-06-12 `ai-dev-weekly` session: a multi-topic trend sweep (social
> + gh + verification) whose recipe was shaped live by mid-session
> corrections (window 7d→14d, topics extended, output format rewritten
> twice) — and whose pipeline already hand-rolls `gh` trending and
> websearch **outside the skill contract**. Two gaps, one concept:
> recurring intents need a living recipe (Part 1), and sweeps need more
> venues with ask-driven ordering (Part 2). The first config produced
> this way already exists: `~/.hivemind/ai-dev-weekly/config.md`
> (edition 1, hand-crystallized). Related KG capture:
> `captures/2026-06-12-canon-evidence-from-the-skill-layer.md`
> (engine + definitions; "config = contract"; self-managed config
> lifecycle as unclaimed territory).
>
> History: briefly split across two docs (crystallize-repeat +
> pivot-chains); merged same day — it's one concept.

---

## The job

Hivemind sweeps are currently one-shot and social-only. Both limits
broke in the same real session:

**No living recipe.** Frames persist *what happened* (manifest.md,
immutable), but recurring intents have no *living recipe*. Repeating
last week's sweep requires the conversation that produced it. User
preferences revealed mid-session (windows, topics, output formats,
muted subjects) evaporate unless someone hand-writes them down.

The inversion: **the session is the requirements interview.** Instead
of configuring upfront (wizard-style, predicting what you'll want), the
user just runs a sweep and steers; the skill records what the steering
revealed and crystallizes it into a config. Next time: "repeat
ai-dev-weekly". Mid-session corrections are exactly the data a wizard
can't elicit — nobody knows they want "one flowing paragraph, no
What/Why labels" until they've seen the labeled version.

**Social-only, fixed order.** Real questions don't respect the
X+Reddit boundary, and neither does venue *order*:

- "weekly trending git repos and what twitter says about them"
  → gh **discovers**, social **reacts**
- "check out the most mentioned git repos on reddit"
  → reddit **discovers** (mention mining), gh **enriches**
- "what's hot in RAG research and does the community care"
  → papers discover, social reacts
- "is the hype around X backed by actual science"
  → social/web discover the claims, papers **verify**

Same venues, opposite chains. A fixed pipeline gets these wrong in a
way that produces *plausible garbage* — mention-mining Reddit when the
user asked for trending-then-reactions returns popularity of old repos,
not trends. The order is part of the question.

The identity reframe that keeps this honest: hivemind is "ask the
collective brain" — and the collective brain includes what people
**build** (GitHub), **publish** (papers), and **write** (web), not
just what they **post**. The synthesis discipline (receipts, epistemic
labels, named rejections) is the product; the venues are inputs.

---

## Part 1 — Configs by demonstration

### The config file

`~/.hivemind/<topic-slug>/config.md` — topic level, *beside* the dated
frame dirs, never inside them.

| | manifest.md (existing) | config.md (new) |
|---|---|---|
| Scope | one sweep (dated frame) | the recurring intent |
| Mutability | immutable once written | living, edition-bumped |
| Tense | past — what happened | future — what to do next time |

Sections (template in `references/`): intent + audience, topic list
(with a staleness rule), pipeline recipe (venues, chain, windows,
floors, known CLI quirks and keyword traps discovered in past runs),
output format + delivery target, persistence rules, dated changelog
with edition numbers.

**The canonical worked example already exists:**
`~/.hivemind/ai-dev-weekly/config.md` (edition 1, hand-crystallized
2026-06-12 from a real session). The `references/` template is
*distilled from that file*, not invented — an implementer should read
it first; every section named above is present there with real values,
including the recorded CLI trap (`--exclude retweets` + min-likes
combination returns empty) and the keyword traps (unscoped "RAG"/
"agentic" collide with non-tech usage).

Hard rule: **propose-confirm only.** The skill never silently rewrites
user intent. Every accepted change = edition bump + dated changelog
line naming what changed and why.

### Verbs

1. **Crystallize.** After any sweep that smells recurring (user says
   "weekly", "again next time", names a cadence, or asks to freeze the
   process) — or on explicit request — offer to write/update
   `config.md`. Source material: the frame's manifest (queries,
   adaptations, named rejections) plus every user correction observed
   in the session. Corrections map to config lines; muted topics map
   to an exclusions list; the output the user finally accepted maps to
   the format spec.

2. **Repeat.** `repeat <slug>` (or "wiederhole <slug>"):
   - Load `config.md`; say which edition is running.
   - Execute the recipe as a normal hivemind sweep (full frame
     contract: raw/, manifest.md, brief.md — unchanged).
   - **Diff against the previous frame's brief**: stories already
     reported are dropped unless there's a material development
     (a weekly that re-reports last week is worthless). With a chain,
     the manifest's pivot entity list is the diff key — compare
     entities (repos, papers), not just story titles.
   - **Staleness check**: a topic returning thin results for 2
     consecutive frames triggers a replacement proposal (the config's
     staleness rule names the threshold).
   - Deliver per the config's output spec.
   - Close with a crystallize pass: any deviation the user steered
     this run becomes a proposed config delta.

3. **Lookup.** At the start of any *ad-hoc* sweep request: if the ask
   plausibly matches an existing config slug, say so and apply that
   config's constraints (especially exclusions) before sweeping. The
   counterpart of crystallize — demonstration captures what the user
   *says*; lookup replays what they *already said*. Without it,
   standing preferences silently fail to reach ad-hoc sessions (the
   2026-06-12 silent-drift lesson, captured as IN-20260612-1f82).

### Config chains are free-form

The config always owns its chain, and the chain is free-form:

- A `chain:` line names the recipe's shape for fast orientation, but
  the pipeline **prose is the contract** — hivemind executes what the
  config says, in the order it says, including stages that aren't
  registry venues at all (ai-dev-weekly's "locate the issue and write
  into its body" is delivery, not a venue; fine).
- **Precedence: live ask > config > recon classification.** Recon's
  chain classification (Part 2) is the fallback for ad-hoc asks with
  no config; a config is the user's already-stated intent (the lookup
  verb's whole point); a live deviation wins for the run and becomes a
  proposed delta.
- The 2–3 stage cap (Part 2) applies to *inferred* chains only. An
  explicit config chain is user-authored and as long as the intent
  needs.
- **No migration, ever.** ai-dev-weekly edition 1 runs as-is — its
  prose steps already are a chain. What the venue registry adds to
  config-land: crystallize writes better recipes (playbook-grounded
  floors, traps, evidence grades instead of session improvisation),
  and preflight/degradation discipline covers the venues it
  recognizes. Venue knowledge splits naturally — universal mechanics
  and traps live in playbooks, discovered once; intent-specific
  steering stays in the config. Configs remain self-contained enough
  for cold replay either way.

---

## Part 2 — Venues & pivot chains

### Venue registry

Each venue = one playbook reference (the existing
`reddit-playbook.md` / `x-playbook.md` pattern) declaring its tool,
recipes, engagement proxies, floor ladder, and **evidence grade**:

| Venue | Tool | Evidence grade | Engagement proxy |
|---|---|---|---|
| `x`, `reddit` | twitter / rdt CLI (as today) | weak — sentiment, pointers | likes, upvotes |
| `gh` | `gh` CLI (exists, authed) | medium — metadata factual, stars ≠ quality | stars-per-day, release recency, fork ratio |
| `web` | SearXNG (`localhost:8888`, JSON) | varies — secondary sources | domain authority, recency |
| `papers` | OpenAlex + arXiv APIs; SearXNG `categories=science` as aggregator | **strong — primary sources** | citations (lag-aware), venue, recency |

Web-venue note (tested 2026-06-12): SearXNG's `social media` category
is **fediverse-only** (lemmy posts/comments, mastodon users/hashtags) —
useful breadth for FOSS/dev topics, never a substitute for the x/reddit
venues. SearXNG has no X engine at all, and its reddit engine 403s
(Reddit blocks anonymous JSON search; left disabled). `rdt` and
`twitter` CLIs remain the only real social tools.

**Papers tooling (verified working 2026-06-12, both free, no keys):**

- **OpenAlex** — `https://api.openalex.org/works?search=<q>&mailto=<email>`
  ~250M works, citation counts, filters/sorts, 100k req/day polite
  pool. The structured-triage workhorse.
- **arXiv API** — `http://export.arxiv.org/api/query?search_query=all:%22<q>%22&sortBy=submittedDate&sortOrder=descending`
  Freshest preprints — where AI/ML research actually lands first.
  Atom XML; a throwaway parser is fine (Initiative section applies).
- SearXNG `categories=science` aggregates Scholar/PubMed/Crossref/
  OpenAIRE for breadth when the instance is up.
- *Rejected:* Semantic Scholar (free key exists but unauthenticated
  pool is shared and tight — adds a credential for nothing OpenAlex
  doesn't cover); any paid API.
- Citation-lag rule: for papers younger than ~6 months, citations are
  meaningless — triage by recency + venue + author track record, and
  say so in the brief.

### Pivot chains

Recon (Phase 2) classifies not just the mode (trend scan vs knowledge
mine) but the **chain**: which venue *discovers* (produces the entity
list) and which venues *enrich/react/verify* (queried per-entity).

```
discover → pivot(entities) → enrich | react | verify
```

The pivot is the load-bearing step: entities extracted from the
discover stage (repo names, paper titles, tool names, author handles)
become the scoped queries of the next stage. Stage roles:

- **discover** — open-ended search in one venue; output = entity list
- **enrich** — factual lookup per entity (gh stars/releases, OpenAlex
  citations) — adds metadata, not opinions
- **react** — social/web search per entity — adds sentiment, friction,
  hot takes
- **verify** — chase claims to primary sources (subsumes today's
  `--verify`; papers venue is its natural home)

Rules:

- **The chain is classified out loud.** It appears in the brief's
  coverage section and the manifest, like adaptations do today.
  Material ambiguity in the ask → ask the user (existing Phase 1 rule).
- Default for plain social asks: today's behavior exactly — social
  venues, no chain. Zero regression for "what does reddit think of X".
- Inferred chains are short: 2 stages typical, 3 max. More = a
  research project, not a sweep (codies-research / deep-research
  territory). Config-authored chains are exempt (Part 1).

### Frame contract extension (not a break)

- Every stage's raw output lands in `raw/` with venue-prefixed names
  (`gh-*.json`, `oa-*.json`, `arx-*.xml`, `web-*.json`).
- `manifest.md` records the chain (`chain: gh → x,reddit`) and the
  **pivot entity list explicitly** — that list is the diff key for
  `repeat`.
- Receipts notation extends per grade: `[gh, 2.3k★, created 2026-05]`,
  `[arXiv 2506.xxxxx, 0 cites — too fresh]`, `[openalex, 127 cites]`.
- **Cross-grade echo generalizes cross-platform echo**: the same thing
  showing up as paper + repo + social chatter is the strongest trend
  signal hivemind can emit; social-only echo is labeled as possible
  hype. The "social is weak evidence, never factual validation" rule
  survives unchanged — papers/gh are what validation now looks like
  *inside* the skill instead of outside it.

### Preflight extension

- `gh`: `gh auth status` — and **say which account is active**; venue
  recipes that touch work repos depend on it (streams rule).
- `web`: probe `localhost:8888`; down → offer the docker start fix
  first (the searxng skill's own setup section), degrade with a
  flagged coverage gap if declined. (Instance was down on 2026-06-12 —
  the probe is not hypothetical.)
- `papers`: curl probe to OpenAlex; no install, no auth. arXiv as
  fallback if OpenAlex is unreachable.
- Existing rule holds: degrade and flag, never block; no scraping
  workarounds before the fix offer.

### Tool failure semantics (preflight feeds recon)

Preflight runs before recon, so its output — the **live venue set** —
is an *input* to chain classification: a chain is never planned over a
tool that already failed its probe. Fix-offer-first stays the rule;
what happens after a declined fix depends on one distinction:

- **Inferred venue** (user asked by role: "what does the community
  think") → recon substitutes within the role (x ↔ reddit for react,
  OpenAlex ↔ arXiv for papers) and states the substitution as an
  adaptation in brief + manifest.
- **Named venue** (by the user or by a config) → substitution changes
  the question; never silent. Dead venue in the *discover* stage means
  the sweep can't honestly run: say so, offer the nearest alternative
  chain, user decides. Dead venue in a later stage: run the remaining
  stages, flag the gap in coverage.

**Mid-sweep failure** (tool passed preflight, dies during fan-out —
e.g. an engine starts 403ing): the adaptive-floor logic generalizes —
adapt within the stage if possible, otherwise mark the stage degraded;
the manifest records what was attempted and what's missing.

**Degradation is not intent.** The crystallize pass never turns a tool
failure into a config delta — broken tools are circumstance, not
steering; configs change when the user changes their mind, not when
reddit has a bad day. The one exception is *repair*: a recipe detail
that is persistently broken (renamed CLI flag, dead venue across 2+
runs) may yield a proposed config fix, labeled as repair — consistent
with the stale-recipe rule under Error handling, and distinct from an
intent change.

---

## What does NOT change

- The frame contract (immutability, manifest discipline, named triage
  rejections, `--no-keep`) stays exactly as is.
- Radar mode untouched; a radar series can carry a config like any
  other topic dir.
- Sweep methodology (recon → fan-out → triage → deep-read → synthesis)
  unchanged — config and chain parameterize the phases, never replace
  them.
- Brief format, epistemic labels, auto-save rule unchanged (receipts
  notation extends per evidence grade, see Part 2).

## Approaches considered

- **Separate "research-loops" skill** owning configs and calling
  hivemind — rejected: second engine over the same frames; the config
  is meaningless without the sweep mechanics it parameterizes.
- **Config as YAML frontmatter on the topic dir** — rejected: the
  recipe is prose-shaped (steer hints, traps, audience framing);
  markdown with a changelog reads and anneals better. Frontmatter for
  the scalar fields only (cadence, window, edition).
- **Auto-crystallize without confirm** — rejected: configs are
  contracts; silent rewrites destroy trust in them.
- **Separate skills per venue** (gh-mind, paper-mind) — rejected: the
  value is the pivot *between* venues and one synthesis discipline
  over mixed evidence; separate skills reinvent the frame contract N
  times.
- **Fixed multi-venue pipeline** (always social → gh → web) —
  rejected: the dynamic-order examples in The job produce garbage
  under any fixed order. The chain must come from the ask.
- **Venue plugins as configs** (registry in `~/.hivemind/venues/`) —
  deferred: YAGNI until a venue arrives that isn't one of these five.
  Playbook references are enough.
- **Semantic Scholar as primary papers API** — rejected (rate-limit
  pool; see registry).

## Error handling

- `repeat <slug>` with no config → say so, offer a normal sweep +
  crystallize at the end.
- Config conflicts with the live ask ("repeat ai-dev-weekly but only
  Reddit") → the ask wins for this run; the deviation becomes a
  proposed delta, not an auto-edit.
- Stale recipe details (dead venue, renamed CLI flag) → adapt per the
  existing adaptive-floor rules, record in manifest, propose the
  config fix in the crystallize pass (labeled as repair).
- Previous frame missing/corrupt → run without the dedup diff, say so.
- Chain ambiguous and material → ask; otherwise state the chosen chain
  and proceed (it's reviewable in the brief).
- Discover stage returns < 3 entities → widen once per the adaptive
  floor rules; still thin → deliver the thin result with the gap
  named, don't pad with a different chain.
- OpenAlex down → arXiv-only with a coverage flag (and vice versa).
- SearXNG down → web venue degrades to flagged absence; gh/papers
  unaffected (direct APIs).
- Entity extraction pollution (e.g. repo names that are common words —
  the "RAG"/"agentic" keyword-trap lesson generalizes): scope pivot
  queries with qualifiers (`"<repo>" github`, author/org names);
  playbooks carry the trap list.

## Testing (dojo)

Tier: technique. Scenarios:

1. **Cold replay**: fresh subagent, no conversation context, only
   `repeat ai-dev-weekly` + the config file — must execute the recipe
   (correct venues, window, output shape) without asking the user
   anything the config already answers.
2. **Crystallize-on-deviation**: scripted session with two mid-sweep
   corrections — the proposal must contain both; nothing written
   before confirm.
3. **Staleness**: synthetic frames where one topic is thin twice —
   replacement proposal must fire, naming the evidence.
4. **Lookup**: ad-hoc ask overlapping an existing config with an
   exclusion — output must honor the exclusion and say which config
   bound it.
5. **Chain classification**: the two contrasting asks ("trending
   repos + what twitter says" vs "most mentioned repos on reddit")
   must produce opposite chains, stated in the brief.
6. **Pivot fidelity**: synthetic discover results; enrich/react
   queries must be scoped to the extracted entities, not the original
   topic terms.
7. **Mixed-grade synthesis**: brief must label evidence grades and
   never present social echo as validation; cross-grade echo flagged
   when present.
8. **Preflight degradation**: SearXNG down — fix offered first, then
   flagged degradation; no scraping workaround attempted.
9. **Citation-lag**: fresh papers triaged by recency/venue, with the
   lag caveat in the brief.

Trigger eval — positives: "repeat ai-dev-weekly", "wiederhole den
Sweep von letzter Woche", "frier den Prozess ein", "trending repos
and what does X say about them", "most mentioned repos on reddit",
"what does the research say about Y, and do practitioners agree".
Negatives: one-off "what's hot in X" without recurrence smell must
not trigger crystallize offers; "review this repo", "find me a paper
on Z" (single-venue lookups with no collective-brain angle) must not
route to hivemind at all. SKILL.md description needs the
corresponding trigger phrases at implementation time.

First real test object: `~/.hivemind/ai-dev-weekly/config.md` (edition
1) — the cold-replay scenario can run against it as-is.

## Non-goals

- No scheduling/cron (user-triggered; `/loop` exists for cadence).
- No cross-config inheritance or global defaults file.
- No sync with any other engine's config stores — one config per
  intent, owned here.
- Not a literature-review tool — papers venue surfaces and verifies;
  deep reading of papers belongs to codies-research / deep-research.
- No paid APIs, no API keys, no scraping workarounds.
- No new output engine — brief format, frames, radar all unchanged;
  config and chains parameterize the existing phases.
