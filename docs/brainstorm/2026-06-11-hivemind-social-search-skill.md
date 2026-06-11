# Hivemind — Social Media Search Skill for Limitless

*Concept · 2026-06-11 · Claude (Fable 5, via Claude Code)*

> Status: reviewed by Pyro 2026-06-11 — all open questions decided yes,
> radar mode added. Ready for implementation. Research grounded in live CLI
> smoke tests, the last30days-skill methodology, and our in-house research
> skills.

---

## Why

Pyro keeps typing "pls use the twitter cli and the rdt cli" — that's a skill
trigger wearing a trenchcoat. The two CLIs are installed, authenticated, and
LLM-friendly; what's missing is the orchestration layer that knows *how* to
search social media well instead of just *that* it can.

Archetype questions this skill must answer:

1. **Trend scan** — "What is currently the new hot shit in X?"
2. **Knowledge mine** — "What does social media say about how optimal Suno
   prompts look like?"

Both are social-evidence questions where Google gives you SEO spam and the
real answer lives in r/SunoAI comment threads and quote-tweet pile-ons.

---

## Tooling inventory (verified 2026-06-11)

Both CLIs are uv tools (`uv tool install twitter-cli` / `uv tool install
rdt-cli`), both authenticated, both emit structured JSON with `--json` and
have LLM-friendly compact modes (`-c`).

### `twitter` (twitter-cli v0.8.5)

| Capability | Flags |
|---|---|
| Search tabs | `-t top\|latest\|photos\|videos` |
| Engagement floors | `--min-likes N`, `--min-retweets N` (maps to `min_faves:`/`min_retweets:`) |
| Time window | `--since YYYY-MM-DD`, `--until YYYY-MM-DD` |
| Noise control | `--exclude retweets\|replies\|links`, `--lang en`, `--has links\|media…` |
| Author scoping | `--from user`, `--to user` |
| Thread deep-read | `twitter tweet <id> -n N` (replies), `twitter user-posts` |
| Output | `--json`, `-c` compact, `-o file`, `--filter` (score-based) |
| Auth check | `twitter status` |

JSON includes full metrics per tweet: likes, retweets, replies, quotes,
views, bookmarks, verified flag, ISO dates.

### `rdt` (rdt-cli v0.4.1)

| Capability | Flags |
|---|---|
| Search | `rdt search QUERY -r subreddit -s relevance\|hot\|top\|new\|comments -t hour…all -n N` |
| Comment deep-read | `rdt read <post_id> -s best\|top\|new\|controversial\|qa -n N --expand-more` |
| Venue inspection | `rdt sub <name>`, `rdt sub-info <name>` |
| Bulk export | `rdt export QUERY --format json -o file` |
| Output | `--json`, `-c` compact, `--after` pagination |
| Auth check | `rdt status` (cookie-based via `rdt login`) |

JSON includes score, num_comments, subreddit, selftext, permalink, created_utc.

---

## What the research taught us

### From last30days-skill (27.7k stars, the reference implementation)

Source: [github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill),
esp. `docs/how-search-works.md`.

1. **Resolve venues before searching.** v3's biggest quality win: find the
   right subreddits, handles, and hashtags *before* a single search fires.
   Keyword-only search is the failure mode.
2. **Multi-query expansion, parallel execution.** 2–4 query variants per
   platform, run concurrently, not one broad query.
3. **Engagement-weighted scoring with real metrics.** A 1,500-upvote thread
   beats a blog post nobody read. Fetch actual counts, not estimates.
4. **Hard recency filter + depth tiers.** quick (15–25 threads) / default
   (30–50) / deep (70–100), with proportional timeouts.
5. **Dedup + clustering + author caps.** Same story on Reddit and X merges
   into one cluster; max 3 items per author so no single voice dominates.
6. **Fallbacks everywhere.** If filtering kills everything, keep top 3 by
   relevance. Retry with backoff. Skip a dead platform rather than fail.

### From our own skills

- **codies-research** — the operator loop: scope → acquire → grade while
  collecting → resolve contradictions → *answer first* → offer 2–4 next
  directions. No planning theater, no raw-result dumps. Hivemind inherits
  this DNA wholesale.
- **searxng** — focused queries beat broad ones; reformulate on poor
  results; 5–10 results per query is plenty. Also available as an optional
  third leg (web context, venue discovery) since it's already self-hosted.
- **deep-research harness** — adversarial verification of claims. Overkill
  for v1, but the "social media says X" → "primary source confirms?"
  handoff is a natural `--verify` extension.

### From live smoke tests (the load-bearing evidence)

**Global Reddit search is poisoned by viral noise.** `rdt search "suno
prompt" -s top -t year` returned r/CuratedTumblr memes and r/antiai rants
(7.5k upvotes, zero Suno content). The same query scoped: `rdt search
"prompt structure" -r SunoAI -s top -t year` returned "The Guide to Meta
Tags in Suno AI" and producer experience threads — exactly the target
content. **Venue resolution is not optional; it is the difference between
garbage and gold.**

**Engagement ≠ relevance on X.** `twitter search "suno prompt" -t top
--min-likes 20` surfaced a 2,056-like tweet about GPT Haskell prompts and
Simon Willison on minimal prompting — popular, adjacent, wrong. An LLM
triage pass between fetch and deep-read is mandatory.

### Prior art in our own garden

`claude-knowledge/sketches/social-signal-radar.md` is the big sibling: a
persistent social-evidence graph with decay semantics and KG admission
contracts. **Hivemind is not that product.** Hivemind is the interactive,
on-demand search layer — but it should be built so a future Radar can use
it as its scout primitive (structured JSON intermediate results, explicit
provenance per claim). Radar's key epistemic rule already applies to us:
*social media is a weak-evidence surface — useful for friction, language,
pointers, and sentiment; insufficient as factual validation.* Hivemind's
synthesis must label claims accordingly.

---

## The search flow

Two modes, one pipeline. Mode changes the knobs, not the structure.

| | **Trend scan** ("new hot shit in X") | **Knowledge mine** ("what does social media say about Y") |
|---|---|---|
| Time window | 7–30 days | 6 months – all time |
| Reddit sort | `top -t week/month` + `new` for the bleeding edge | `top -t year`, `comments` for discussion depth |
| X tab | `latest` + `top`, `--since` recent | `top`, engagement floors higher |
| Signal | repeated independent mentions, velocity | depth + agreement of practitioner answers |
| Synthesis | ranked "what's hot" clusters with receipts | consensus vs. contested practices, best takes |

### Phase 0 — Preflight (once per session)

```
command -v twitter && command -v rdt
```

- Missing → offer install via AskUserQuestion:
  `uv tool install twitter-cli` / `uv tool install rdt-cli`.
- Present → `twitter status` / `rdt status`. Unauthenticated → point at
  `rdt login` (browser cookie extraction) / twitter's auth flow, and offer
  to continue single-platform. **One dead platform degrades, never blocks.**

### Phase 1 — Scope

Classify the question: mode (trend/knowledge), topic terms + jargon
variants, time window, depth tier (`quick` ≈ 2 queries/platform, `default`
≈ 3–4, `deep` ≈ 6+ plus pagination). Only ask the user when ambiguity is
material (codies-research posture: do the research, don't interrogate).

### Phase 2 — Recon (venue resolution — the last30days steal)

Cheap, fast, parallel:

- `rdt search "<topic>" -s relevance -n 25 -c --json` → frequency-count the
  `subreddit` field; top 2–4 communities are the venues. Sanity-check odd
  winners with `rdt sub-info`.
- `twitter search "<topic>" -t top -n 20 -c --json` → harvest recurring
  hashtags, jargon, and high-signal authors (for optional `--from` probes).
- Optional: searxng `"best subreddit for <topic>"` when Reddit recon is thin.

Output: 2–4 subreddits, refined query variants ("suno prompt" → "style
prompt", "meta tags", "exclude styles"), notable authors.

### Phase 3 — Fan-out (parallel scoped searches)

All searches run in one parallel batch, results to JSON files in a temp dir.

Reddit (per venue + one global):
```
rdt search "<variant>" -r <sub> -s top -t <window> -n 25 --json -o r1.json
rdt search "<variant>" -r <sub> -s new -n 15 --json -o r2.json   # trend mode
```

X (quoted topic term to prevent drift):
```
twitter search '"<topic>" <variant>' -t top --min-likes 50 --lang en \
  --exclude retweets --since <window-start> -n 30 --json -o x1.json
twitter search '"<topic>"' -t latest --min-likes 10 -n 20 --json -o x2.json
```

**Adaptive floors:** start `--min-likes 50` (top) / 10 (latest); if a query
returns < 5 hits, halve the floor and widen the window once before declaring
the venue thin. If results are noisy, double the floor and add `--exclude
replies`.

### Phase 4 — Triage & deep-read

The phase last30days does with code and we do with judgment:

1. **Relevance triage (LLM).** Read titles/snippets across all result
   files. Discard topic drift regardless of engagement (the Haskell-tweet
   problem). Engagement breaks ties *among relevant* items only.
2. **Select 3–5 threads per platform** by relevance × engagement × recency.
3. **Deep-read where the knowledge actually lives:**
   - `rdt read <id> -s top -n 30 --json` — Reddit comments are the ground
     truth layer; the post is often just the question.
   - `twitter tweet <id> -n 20 --json` — replies and quote-tweets carry the
     corrections and counterpoints.
4. **Discipline:** dedup by URL/ID; max 3 items per author; cluster the
   same story/claim appearing on both platforms (cross-platform
   corroboration is a *strong* trend signal — flag it).

### Phase 5 — Synthesis (answer first)

The brief, in order:

1. **TL;DR** — direct answer in 3–5 sentences.
2. **Consensus** — what the hivemind agrees on, each claim with receipts:
   `[r/SunoAI, 446↑]`, `[@user, 2.1k likes]`. Engagement shown, not implied.
3. **Contested** — where practitioners disagree; both sides with links.
   Resolve by evidence strength, or say it's unresolved (codies-research
   rule: resolve contradictions, don't average them).
4. **Best takes** — 2–4 verbatim quotes that earn their place (the
   last30days "Best Takes" pattern; concrete beats summarized).
5. **Freshness note** — date range actually covered, anything that changed
   recently (trend mode: velocity callouts).
6. **Next directions** — 2–4 materially different follow-ups: deepen one
   thread, verify a claim against primary sources, watch an author, widen
   the window. Each executable as a follow-up invocation.

Epistemic labeling throughout: `[observed]` (in the posts), `[claimed]`
(asserted by posters), `[inferred]` (our synthesis). Social evidence is
weak evidence; the brief never pretends otherwise.

Optionally offer to save the brief as a research note (artifact, not
default — answer-first posture).

---

## Skill interface

```
/limitless:hivemind what's the new hot shit in agent memory systems?
/limitless:hivemind --deep what does social media say about optimal Suno prompts?
/limitless:hivemind --platform reddit --window 90d best practices for skill descriptions
/limitless:hivemind --radar "AI Agents"
```

- `--quick | --deep` — depth tier (default between).
- `--platform x|reddit|both` — default both.
- `--window 7d|30d|90d|1y|all` — overrides mode default.
- `--verify` — chase the top contested claim(s) to primary sources before
  synthesizing (deep-research handoff).
- `--radar "<topic>"` — radar mode: HTML topic report backed by a
  Radar-compatible mini-KG (see below). `--report` accepted as alias.

Trigger phrases for the description: "ask the hivemind", "what's the hot
shit in", "what does social media say", "what does reddit/twitter/X think",
"social search", "check the socials", "what are people saying about".

## Radar mode (`--radar`)

*Added 2026-06-11 after Pyro's review. `--report` is an alias; `--radar` is
the real name — it tells the truth about what the artifact is and wires the
Social Signal Radar connection into the vocabulary now.*

### What it does

`/limitless:hivemind --radar "AI Agents"` runs a trend-scan sweep and
produces two artifacts instead of an inline brief:

1. **`radar.json`** — the backend: a small, Social-Signal-Radar-compatible
   evidence KG of the sweep. **This is the primary output.**
2. **`radar.html`** — a self-contained visualization rendered *from* the
   JSON: hot topics ranked by heat, per-topic main positive and negative
   opinions with receipts, per-topic enrichment links.

The order matters: the KG is the artifact, the HTML is a view over it. That
keeps every sweep reproducible, diffable, and importable — and prevents the
HTML from quietly becoming the data.

### Pipeline delta

Phases 0–4 run unchanged in trend-scan mode (radar implies at least default
depth; `--deep` recommended). Then, instead of the Phase 5 brief:

5. **Topic clustering** — group triaged findings into 5–9 hot topics. The
   cross-platform clusters from Phase 4 are seed candidates; rank by heat
   (mention count × cross-platform corroboration × velocity).
6. **Stance mining** — per topic, sort the deep-read material (comments,
   replies, quote-tweets) into positive / negative / contested camps and
   pick the strongest representative opinion per camp, each with receipts
   (link, author, engagement, timestamp). Stance is sentiment about the
   topic, never a truth claim — epistemic labels carry over.
7. **Enrichment (budgeted)** — per topic, the agent classifies the topic
   type on the fly and fetches supporting context accordingly:
   - tool/library/release → GitHub repo link (`gh search`, searxng)
   - research-flavored → arXiv / paper link
   - news/event → 2–3 sentence background explainer with source
   - technique/practice → canonical guide or docs link
   **Hard budget: 1–3 lookups per topic.** Enrichment is the scope-creep
   magnet of this mode; the budget is a design rule, not a suggestion.
8. **Emit & render** — write `radar.json`, render `radar.html` from it
   (single self-contained file, inline CSS — the last30days pattern; visual
   language: the fanzine template, see below). Default location:
   `~/.hivemind/<topic-slug>/<date>/radar.{json,html}` — see
   "Sweep series" below for the directory contract.

### KG sidecar schema (sketch)

```json
{
  "radar": { "query": "AI Agents", "window": "30d",
             "generated_at": "...", "platforms": ["x", "reddit"] },
  "topics": [{
    "id": "t1",
    "label": "...",
    "type": "tool | technique | news | debate | release",
    "heat": { "mentions": 14, "cross_platform": true, "velocity": "rising" },
    "stances": {
      "positive": [{ "claim": "...", "source": {
        "platform": "reddit", "url": "...", "author": "...",
        "engagement": 446, "observed_at": "..." } }],
      "negative": ["..."],
      "contested": ["..."]
    },
    "evidence": ["...every receipt that survived triage, with provenance..."],
    "enrichment": [{ "kind": "github", "url": "...", "note": "..." }]
  }]
}
```

Radar-compatibility rules, inherited from the sketch:

- Every claim carries provenance and `observed_at` — decay-ready by
  construction, even though hivemind itself never applies decay.
- All social evidence is weak evidence; the schema encodes stance and
  engagement, never validation.
- **Pull, not push:** a future Social Signal Radar imports `radar.json`
  under its own admission contract. Hivemind emits and walks away.

Strategically, this makes hivemind the de-risking prototype for Social
Signal Radar: each sweep is a frozen radar frame, and Radar-the-product
reduces to accumulation + decay + admission over a pile of frames we'll
already have.

## Packaging

- `plugins/limitless/skills/hivemind/SKILL.md` — the pipeline above, lean.
- `references/x-playbook.md` — twitter-cli flag recipes, floor heuristics.
- `references/reddit-playbook.md` — rdt recipes, venue-resolution patterns.
- `references/radar.md` — radar pipeline detail, KG schema, HTML render
  guidance + topic-type enrichment table.
- No scripts in v1: both CLIs are already agent-friendly; orchestration is
  judgment, not plumbing. (Index-document pattern per lesson LS-0003 —
  small SKILL.md, drill into references.)

## Name

**`hivemind`** — recommended. It names what you're querying (the collective
brain), reads naturally in both modes ("ask the hivemind"), and isn't taken
anywhere in the marketplace. Alternates considered: `zeitgeist` (trend-only
connotation), `vox-populi` (pretty but long), `street-talk` (collides
tonally with after-hours), `social-pulse` (pyro-kit already has `pulse`).

## Non-goals (v1)

- **No posting/engagement.** Read-only research; the CLIs can post, the
  skill never does.
- **No persistent watches/daemons.** That's Social Signal Radar territory.
- **No persistent evidence graph.** `--radar` emits a per-run KG snapshot
  (Radar-compatible, frozen at sweep time), but accumulation, decay, and
  admission into curated KGs remain Social Signal Radar territory.
- **No YouTube/TikTok/HN adapters.** Two platforms done well beats six done
  shallow. searxng covers incidental web context.

## Decisions (Pyro, 2026-06-11)

All four original open questions resolved **yes**:

1. **Auto-save to memory: yes.** When findings are load-bearing (feeding a
   suno-pack, article-pack, or project decision), the brief auto-saves to
   the codies-memory inbox. Casual lookups stay inline — answer-first
   posture unchanged; load-bearing is the trigger, not every run.
2. **`--verify` ships in v1.** Top contested claim(s) get chased to primary
   sources via the deep-research handoff before synthesis. Flag-gated, so
   the default run stays fast.
3. **Subagent fan-out for `--deep`: yes.** One agent per venue (subreddit /
   X query family), per codies-research parallel-branching rules: branches
   are independent, each has a crisp question, breadth beats depth at this
   tier. Sequential remains the path for quick/default.
4. **Side-by-side test of `twitter search --filter`: yes.** Run it during
   implementation. LLM triage remains the source of truth until the test
   shows the CLI's score-based filter adds signal rather than hiding it.

Plus one addition from the same review: **radar mode** (`--radar`, alias
`--report`) — see the Radar mode section above.

## Radar visual language (decided 2026-06-11)

Four dual-view mockups (map/graph view + flat report view, shared sample
data) live in `docs/brainstorm/hivemind-mockups/`:

1. `01-sonar.html` — phosphor CRT operations room, rotating sweep beam
2. `02-broadsheet.html` — printed intelligence broadsheet, engraved Fig. 1
3. `03-observatory.html` — night-sky star chart, observation log
4. `04-fanzine.html` — neo-brutalist signal zine ← **Pyro's pick**

The fanzine becomes the radar HTML template: graph-paper discourse map with
heat-sized boxes and elbow connectors, data-sheet report view with
"THE HYPE / THE BEEF" stance face-offs, marquee ticker for best takes,
caution-tape contested strips, rubber-stamp epistemic tags. Map view and
report view toggle via torn-tape tabs; clicking a map node jumps to its
report sheet. Fixed template (not bespoke per sweep) so sweeps stay
comparable at a glance.

## Sweep series — shared topic directories (decided 2026-06-11)

Same-topic sweeps share a per-topic directory of immutable, date-stamped
frames. Default root: `~/.hivemind` on Linux/macOS, `%USERPROFILE%\.hivemind`
on Windows (same dotdir convention as `.ssh`/`.gitconfig` — one rule on
every platform, and the skill runs in bash-like shells everywhere anyway).
Overridable via `HIVEMIND_DIR` env var.

```
~/.hivemind/
  ai-agents/
    2026-06-11/radar.json + radar.html
    2026-06-28/radar.json + radar.html
    index.html                          ← regenerated each sweep
```

The directory IS the topic identity — in Social Signal Radar terms, a
proto-watch: a time series of frozen frames. Radar's import path collapses
to "point the importer at the directory."

Contract:

1. **Deterministic slugs** ("AI Agents" → `ai-agents`) plus a near-match
   check at sweep time so `ai-agents` and `ai-agent` don't fork into
   separate series. Same-day re-sweep gets a `-2` suffix, never an
   overwrite.
2. **Frames are immutable.** Never rewrite an old frame. Links go
   backwards only, zine-back-catalog style: issue №3 links to №2 and №1;
   old issues don't know about the future. Relative links
   (`../2026-05-28/radar.html`) work from disk and any static server.
3. **`index.html` is the only mutable file** — a "back issues" cover page
   listing all sweeps with their headline topics, regenerated each sweep.
   Fully static.
4. **Cross-frame features happen at generation time, not view time.**
   Sweep N+1 reads sweep N's `radar.json` while building and bakes deltas
   in as static content: real heat changes (▲ +12), new topics, vanished
   topics, stance flips — rendered as "NEW" / "BACK AGAIN" / "GONE"
   stickers in the fanzine language. The browser never fetches across
   files (would break on `file://` CORS anyway), so every `radar.html`
   stays fully self-contained.

Side effect of normal use: the directory quietly accumulates the frame
archive Social Signal Radar will eventually import. Velocity stops being
an in-window inference and becomes a measured delta as soon as a topic has
two frames.
