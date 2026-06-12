---
name: hivemind
description: This skill should be used when the user wants to know what the collective brain — social media (X/Twitter and Reddit), GitHub, the web, or research papers — is saying, building, or publishing about a topic — trends, sentiment, hot takes, trending repos, paper-vs-practitioner checks. Also runs recurring sweeps saved as configs. Responds to "ask the hivemind", "what's the hot shit in", "what does social media say", "what does reddit/twitter/X think", "what are people saying about", "check the socials", "--radar", "trending repos and what is X saying about them", "which repos get the most mentions", "what does the research say — and do practitioners agree", "repeat <slug>", "wiederhole den Sweep", "freeze this process", "frier den Prozess ein", or any question whose best answer lives in threads, comments, replies, repos, and preprints rather than articles. NOT for single-item lookups ("find me a paper on X", "search the web for Y") — use search/research skills. Read-only research — never posts.
---

# Hivemind — Ask the Collective Brain

## Overview

Orchestrates the `twitter` CLI (X), `rdt` CLI (Reddit), `gh` CLI
(GitHub), SearXNG (web), and the OpenAlex/arXiv APIs (papers) into a
disciplined evidence search: resolve venues, classify the chain, search
scoped, triage by relevance before engagement, deep-read where the
knowledge lives, synthesize answer-first with receipts. The collective
brain includes what people **post** (social), **build** (GitHub),
**publish** (papers), and **write** (web) — each venue carries an
evidence grade, and the brief always says which is which. Social is a
**weak-evidence surface**: good for friction, language, pointers,
sentiment; never factual validation. Papers and repo metadata are what
validation looks like inside the skill.

Hivemind is read-only. The CLIs can post, like, and reply; this skill
never does.

## Phase 0 — Preflight (always, before anything else)

Probe every venue the ask might touch. The result is the **live venue
set** — an input to chain classification (Phase 2): never plan a chain
over a tool that already failed its probe.

```bash
command -v twitter rdt gh
twitter status; rdt status
gh auth status          # SAY which account is active — recipes that
                        # touch specific orgs/repos depend on it
curl -s -m 5 "http://localhost:8888/search?q=test&format=json" -o /dev/null -w "%{http_code}"   # web: expect 200 (403 = json format disabled — see web-playbook)
curl -s -m 5 "https://api.openalex.org/works?search=test&per-page=1" -o /dev/null -w "%{http_code}"  # papers
```

- **Missing/broken tool → offer the 10-second fix FIRST**: `uv tool
  install twitter-cli` / `uv tool install rdt-cli` / docker start for
  SearXNG (web-playbook has the recipe). Ask via AskUserQuestion if
  interactive. **Non-interactive runs: the fix offer leads the reply —
  it is stated BEFORE any degraded or proxy work is performed, not
  appended to the result.**
- **Do not build scraping workarounds (proxies, mirror instances, raw
  JSON endpoints, search-engine site-scoping as a venue substitute)
  before the install offer has been made.**
- Unauthenticated → point at `rdt login` / twitter's auth flow.
- A venue dead and user opts not to fix → degradation rules in "Tool
  failure semantics" below. Degrade, never block — but named venues
  are never silently substituted.

## Modes

Classify the question first — it sets every knob:

| | **Trend scan** ("what's hot in X") | **Knowledge mine** ("what does social media say about Y") |
|---|---|---|
| Window | 7–30 days | 6 months – all time |
| Reddit sort | `top -t week/month` + one `new` pass | `top -t year`, `comments` for depth |
| X tabs | `latest` + `top`, `--since` | `top`, higher floors |
| Signal | repeated independent mentions, velocity, cross-platform echo | depth + agreement of practitioner answers |
| Brief shape | ranked hot-topics with receipts | consensus vs contested practices |

Sentiment questions ("what do people think of X vs Y") are knowledge
mines with both-sides stance mining. `--radar` is a trend scan with the
report pipeline from `references/radar.md`. Mode and chain are
orthogonal: a chained sweep still has a mode per stage venue.

## Phase 1 — Scope (and config lookup)

**Config lookup comes first.** If the ask plausibly matches an existing
config (`ls ~/.hivemind/*/config.md`, match slug/intent), say so —
state the slug and edition — and apply that config's constraints
(especially exclusions) to this sweep. The live ask wins over the
config for this run; any deviation becomes a proposed config delta at
the end, never an auto-edit. Standing preferences that silently fail to
reach ad-hoc sessions are the failure this step exists to prevent.

Then: topic terms + jargon variants, window (mode default unless
`--window`), depth (`--quick` ≈ 2 queries/platform, default ≈ 3–4,
`--deep` ≈ 6+ and subagent fan-out per venue). Do the research; ask the
user only when ambiguity is material.

## Phase 2 — Recon (venues AND chain — NEVER skip, NEVER assume)

### Venue resolution (social) — a procedure, not a prior

Even when you're sure you know the right subreddit, run the recon and
let the data confirm:

```bash
rdt search "<topic>" -s relevance -n 25 --json -c   # broad, unscoped
twitter search '"<topic>"' -t top -n 20 --json
```

- **Frequency-count the `subreddit` field** of the Reddit results: the
  top 2–4 recurring communities are your venues. Sanity-check surprises
  with `rdt sub-info <name>`.
- From the X pass, harvest recurring hashtags, jargon variants, and
  high-signal authors.
- Recon thin? Reformulate with synonyms once, then optionally ask
  searxng "best subreddit for <topic>".
- The unscoped recon results themselves are *not* evidence — global
  top-sorted Reddit is viral-noise-dominated (the r/antiai lesson).
  Recon finds *where*; the scoped passes find *what*.

### Chain classification — which venue discovers, which react

When the ask spans venues, classify the **chain** and **state it out
loud before fan-out** — it goes in the manifest and the brief's
coverage section, like adaptations do:

```
discover → pivot(entities) → enrich | react | verify
```

- **discover** — open-ended search in ONE venue; output = entity list
  (repo names, paper titles, tools, authors)
- **enrich** — factual per-entity lookup (gh stars/releases, OpenAlex
  citations) — metadata, not opinions
- **react** — social/web search per entity — sentiment, friction, takes
- **verify** — chase claims to primary sources (papers venue is its
  natural home; subsumes `--verify`)

The ask defines the order. "Trending repos and what is X saying" =
gh discovers → social reacts. "Most mentioned repos on reddit" =
reddit discovers → gh enriches. Getting this backwards produces
plausible garbage (popularity of old repos instead of trends).

Rules:
- Plain social asks: today's behavior exactly — no chain. Zero
  ceremony when one venue answers the question.
- **An entity ask is incomplete without its enrich stage.** "Which
  repos are mentioned most" answered without per-entity gh metadata
  (stars, recency, what it is) is half an answer.
- Inferred chains: 2 stages typical, 3 max — more is a research
  project, not a sweep. Config-authored chains are exempt.
- Material ambiguity about the intended chain → ask the user.

## Phase 3 — Fan-out (parallel, scoped)

Per venue + one global control, JSON saved to the sweep's frame
directory with **venue-prefixed names** (`r-*.json`, `x-*.json`,
`gh-*.json`, `web-*.json`, `oa-*.json`, `arx-*.xml`) — create the frame
at the start of Phase 2 so recon files land there too. Recipes, floor
ladders, and venue quirks live in the playbooks:
`references/reddit-playbook.md`, `references/x-playbook.md`,
`references/gh-playbook.md`, `references/web-playbook.md`,
`references/papers-playbook.md`. Read the playbook for every venue the
chain touches. Core social patterns:

```bash
rdt search "<variant>" -r <sub> -s top -t <window> -n 25 --json -o rN.json
twitter search '"<topic>" <variant>' -t top --min-likes 50 --lang en \
  --exclude retweets --since <start> -n 30 --json -o xN.json
```

Adaptive floors: <5 hits → halve floor, widen window once; noisy → double
floor, add `--exclude replies`. State every adaptation you make.

**Pivot discipline (chained sweeps):** the entities extracted from the
discover stage become the scoped queries of the next stage — never
re-query the generic topic. Qualify collision-prone entity names
(generic words, name-squatted projects) with org, URL, or context
terms; record the qualification decisions. Write the **pivot entity
list** out explicitly — it goes in the manifest and is the diff key
for `repeat`.

## Phase 4 — Triage & deep-read

1. **Relevance triage is explicit and stated.** Read titles/snippets
   across all results. Engagement is a tiebreaker *among relevant items
   only* — a 2k-like off-topic tweet is noise (the Haskell-tweet lesson).
   In the brief, name what you rejected and why, or state "nothing
   needed rejection." Silent filtering doesn't count.
2. Select 3–5 threads per platform by relevance × engagement × recency.
   Engagement proxies differ per venue — likes/upvotes (social),
   stars-per-day + release recency (gh), citations *with the lag rule*
   (papers), domain authority (web); each playbook states its ladder.
3. **Deep-read where the knowledge lives:** `rdt read <id> -s top -n 30
   --json` (the post is the question; comments are the answer);
   `twitter tweet <id> -n 20 --json` (replies carry corrections and
   counterpoints).
4. Discipline: dedup by URL/ID (papers: by DOI/arXiv id); max 3 items
   per author; cluster the same story across platforms — cross-platform
   echo is a strong trend signal, flag it.

## Phase 5 — Synthesis (answer first)

The brief, in order:

1. **TL;DR** — direct answer, 3–5 sentences.
2. **Consensus** — claims with receipts, graded per venue:
   `[r/SunoAI, 446↑]`, `[@user, 2.1k likes]`, `[gh, 2.3k★, created
   2026-05]`, `[arXiv 2606.xxxxx, 0 cites — too fresh]`, `[openalex,
   127 cites]`. Engagement shown, not implied.
3. **Contested** — disagreements with both sides linked. Resolve by
   evidence strength or say it's unresolved. **Never average
   contradictions.**
4. **Best takes** — 2–4 verbatim quotes that earn it.
5. **Freshness & coverage** — window actually covered, venues used,
   **the chain that ran**, degradations and triage rejections stated.
6. **Next directions — always, 2–4, materially different.** Deepen one
   thread, verify a claim against primary sources, watch an author,
   widen the window. Each phrased as an executable follow-up. A brief
   without next directions is unfinished.

Epistemic labels throughout: `[observed]` (in the posts/data),
`[claimed]` (asserted by posters/authors), `[inferred]` (your
synthesis). **Cross-grade echo beats cross-platform echo**: the same
thing showing up as paper + repo + social chatter is the strongest
signal hivemind can emit; social-only echo is labeled possible hype.
Social engagement never validates a factual claim — a 2k-like
assertion is `[claimed]` until a paper, repo, or primary source backs
it.

**Auto-save rule:** if the findings are load-bearing (feeding a
suno-pack, article-pack, or a project decision), save the brief to the
codies-memory inbox; otherwise offer it. Answer-first either way.

## Every sweep is a frame (working-data persistence)

Raw results are never discarded — re-triage beats re-search, and scores
are fetch-time snapshots no re-run can reproduce. Every sweep (not just
radar) writes a frame:

```
~/.hivemind/<topic-slug>/<date>/
  raw/          recon + fan-out JSON (venue-prefixed), deep-read JSON,
                throwaway parsers
  manifest.md   query, mode, window, venues, file list, adaptations,
                NAMED triage rejections with reasons — plus, for
                chained sweeps: the chain (e.g. `chain: gh → x,reddit`)
                and the explicit pivot entity list
  brief.md      the final synthesis (copy of what the user got)
  radar.json + radar.html   (radar mode only)
```

- Same contract as radar sweeps (`references/radar.md`): deterministic
  slug, near-match check before creating, `-2` suffix on same-day
  re-sweeps, frames immutable once written.
- The manifest must let a future session re-triage without re-searching
  — rejected items are listed with the reason, not silently dropped.
- `--no-keep` opts out for throwaway lookups (working files go to /tmp
  as before). Default is keep.
- These frames are the acquisition feed for a future Social Signal
  Radar: pull, not push — hivemind writes and walks away.

## Configs — living recipes for recurring intents

`~/.hivemind/<topic-slug>/config.md` — topic level, beside the dated
frames, never inside them. The frame says what *happened*; the config
says what to do *next time*. Template + worked structure:
`references/config-template.md`. Hard rule everywhere: **propose-
confirm only** — the skill never silently rewrites user intent; every
accepted change = edition bump + dated changelog line.

**Crystallize.** After any sweep that smells recurring (user says
"weekly", "again next time", names a cadence, asks to freeze the
process — or auf Deutsch) — or on explicit request — offer to
write/update the config. Source material: the frame's manifest plus
every user correction observed in the session. Corrections map to
config lines; muted topics → exclusions; the output the user finally
accepted → the format spec. Nothing is written before the user
confirms.

**Repeat.** `repeat <slug>` (or "wiederhole <slug>"):
- Load the config; **say which edition is running**.
- Execute the recipe as a normal sweep (full frame contract). The
  config's prose pipeline is the contract — execute what it says, in
  the order it says, including non-venue stages (delivery steps).
- **Diff against the previous frame**: compare pivot entities and
  story titles; drop anything already reported unless there's a
  material development. Previous frame missing/corrupt → run without
  the diff, say so.
- **Staleness check**: a topic thin for the threshold named in the
  config (default: 2 consecutive frames) → propose a replacement,
  citing the evidence from each thin frame. Propose — don't swap.
- Deliver per the config's output spec (language, structure, target).
- Close with a **crystallize pass**: every user-steered deviation this
  run becomes a proposed delta. Tool failures do NOT (see below).

**Lookup** is Phase 1's config check — the counterpart of crystallize:
demonstration captures what the user says; lookup replays what they
already said.

Precedence: **live ask > config > recon classification.**

## Tool failure semantics

What happens after a declined fix offer depends on one distinction:

- **Inferred venue** (the user asked by role: "what does the community
  think") → substitute within the role (x ↔ reddit for react, OpenAlex
  ↔ arXiv for papers) and state the substitution as an adaptation in
  brief + manifest.
- **Named venue** (by the user or a config) → substitution changes the
  question; **never silent**. Discover-stage venue dead → the sweep
  can't honestly run: say so, offer the nearest alternative chain, the
  user decides. Later-stage venue dead → run the remaining stages,
  flag the gap. If a proxy is used at all (only after the offer), its
  results are labeled `proxy-of-<venue>` — never presented as the
  venue itself.
- **Mid-sweep failure** (passed preflight, dies during fan-out): adapt
  within the stage if possible, else mark the stage degraded; manifest
  records what was attempted and what's missing.
- **Degradation is not intent.** Never propose a config delta from a
  tool failure. Exception: a recipe detail persistently broken across
  2+ runs (renamed flag, dead venue) → propose a config fix labeled
  *repair*.

## Flags

- `--quick | --deep` — depth tier. `--deep` fans out one subagent per
  venue (each gets a self-contained brief: topic, venue, window, pass
  criteria — subagents have no conversation context).
- `--platform x|reddit|both` — default both (social asks).
- `--window 7d|30d|90d|1y|all` — overrides mode default.
- `--verify` — before synthesis, chase the top contested claim(s) to
  primary sources (papers first, then docs/repos) and mark
  verified/refuted.
- `repeat <slug>` — execute a saved config (see Configs).
- `--radar "<topic>"` (alias `--report`) — full sweep → topic clusters →
  stance mining → budgeted enrichment → `radar.json` + `radar.html` in
  `~/.hivemind/<slug>/<date>/`. Read `references/radar.md` first.
- `--no-keep` — skip frame persistence (throwaway lookup; working files
  to /tmp).

## Initiative

Baseline agents did good things the skill must not suppress: resolving
shortlinks, writing throwaway parsers for odd JSON, building collision
risk registers for ambiguous entity names, caveating flaky sources.
Keep that initiative — the skill constrains *sequence and evidence
discipline*, not creativity inside the phases.

## References

- `references/reddit-playbook.md` — rdt recipes, venue-resolution
  procedure, comment mining. Read at Phase 2–4.
- `references/x-playbook.md` — twitter-cli recipes, floor ladder, thread
  mining. Read at Phase 3–4.
- `references/gh-playbook.md` — gh CLI recipes (trending, releases,
  enrichment), star proxies, collision traps. Read when the chain
  touches gh.
- `references/web-playbook.md` — SearXNG recipes, categories, json-403
  fix, fediverse note. Read when the chain touches web.
- `references/papers-playbook.md` — OpenAlex/arXiv recipes, citation-lag
  rule, science aggregator. Read when the chain touches papers.
- `references/config-template.md` — config structure, crystallize
  mapping, changelog discipline. Read for any config verb.
- `references/radar.md` — radar pipeline, KG schema, sweep series
  contract, HTML template usage. Read only for `--radar`.
