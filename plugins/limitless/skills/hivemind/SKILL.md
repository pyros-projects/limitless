---
name: hivemind
description: This skill should be used when the user wants to know what social media (X/Twitter and Reddit) is saying or thinking about a topic — trends, community knowledge, sentiment, or hot takes. Responds to "ask the hivemind", "what's the hot shit in", "what's currently hot in", "what does social media say", "what does reddit/twitter/X think", "what are people saying about", "check the socials", "social search", "--radar", or any question whose best answer lives in threads, comments, and replies rather than articles. Read-only research — never posts.
---

# Hivemind — Ask the Collective Brain

## Overview

Orchestrates the `twitter` CLI (X search) and `rdt` CLI (Reddit) into a
disciplined social-evidence search: resolve venues first, search scoped,
triage by relevance before engagement, deep-read where the knowledge
actually lives (comments and replies), synthesize answer-first with
receipts. Social media is a **weak-evidence surface** — good for
friction, language, pointers, and sentiment; never factual validation.
The brief always says which is which.

Hivemind is read-only. The CLIs can post, like, and reply; this skill
never does.

## Phase 0 — Preflight (always, before anything else)

```bash
command -v twitter && command -v rdt
twitter status; rdt status
```

- **Missing CLI → offer the 10-second fix FIRST**: `uv tool install
  twitter-cli` / `uv tool install rdt-cli`. Ask via AskUserQuestion if
  interactive; never silently skip a platform. **Do not build scraping
  workarounds (proxies, mirror instances, raw JSON endpoints) before the
  install offer has been made** — a working install beats an hour of
  spelunking.
- Unauthenticated → point at `rdt login` / twitter's auth flow.
- One platform dead and user opts not to fix → continue single-platform
  and **flag reduced coverage in the final brief**. Degrade, never block.

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
report pipeline from `references/radar.md`.

## Phase 1 — Scope

Topic terms + jargon variants, window (mode default unless `--window`),
depth (`--quick` ≈ 2 queries/platform, default ≈ 3–4, `--deep` ≈ 6+ and
subagent fan-out per venue). Do the research; ask the user only when
ambiguity is material.

## Phase 2 — Recon (venue resolution — NEVER skip, NEVER assume)

Venue resolution is a **procedure, not a prior**. Even when you're sure
you know the right subreddit, run the recon and let the data confirm:

```bash
rdt search "<topic>" -s relevance -n 25 --json -c   # broad, unscoped
twitter search '"<topic>"' -t top -n 20 --json -c
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

## Phase 3 — Fan-out (parallel, scoped)

Per venue + one global control, JSON to temp files. Recipes and the
adaptive floor ladder live in `references/reddit-playbook.md` and
`references/x-playbook.md`. Core patterns:

```bash
rdt search "<variant>" -r <sub> -s top -t <window> -n 25 --json -o rN.json
twitter search '"<topic>" <variant>' -t top --min-likes 50 --lang en \
  --exclude retweets --since <start> -n 30 --json -o xN.json
```

Adaptive floors: <5 hits → halve floor, widen window once; noisy → double
floor, add `--exclude replies`. State every adaptation you make.

## Phase 4 — Triage & deep-read

1. **Relevance triage is explicit and stated.** Read titles/snippets
   across all results. Engagement is a tiebreaker *among relevant items
   only* — a 2k-like off-topic tweet is noise (the Haskell-tweet lesson).
   In the brief, name what you rejected and why, or state "nothing
   needed rejection." Silent filtering doesn't count.
2. Select 3–5 threads per platform by relevance × engagement × recency.
3. **Deep-read where the knowledge lives:** `rdt read <id> -s top -n 30
   --json` (the post is the question; comments are the answer);
   `twitter tweet <id> -n 20 --json` (replies carry corrections and
   counterpoints).
4. Discipline: dedup by URL/ID; max 3 items per author; cluster the same
   story across platforms — cross-platform echo is a strong trend
   signal, flag it.

## Phase 5 — Synthesis (answer first)

The brief, in order:

1. **TL;DR** — direct answer, 3–5 sentences.
2. **Consensus** — claims with receipts: `[r/SunoAI, 446↑]`,
   `[@user, 2.1k likes]`. Engagement shown, not implied.
3. **Contested** — disagreements with both sides linked. Resolve by
   evidence strength or say it's unresolved. **Never average
   contradictions.**
4. **Best takes** — 2–4 verbatim quotes that earn it.
5. **Freshness & coverage** — window actually covered, platforms used,
   degradations and triage rejections stated.
6. **Next directions — always, 2–4, materially different.** Deepen one
   thread, verify a claim against primary sources, watch an author,
   widen the window. Each phrased as an executable follow-up. A brief
   without next directions is unfinished.

Epistemic labels throughout: `[observed]` (in the posts), `[claimed]`
(asserted by posters), `[inferred]` (your synthesis).

**Auto-save rule:** if the findings are load-bearing (feeding a
suno-pack, article-pack, or a project decision), save the brief to the
codies-memory inbox; otherwise offer it. Answer-first either way.

## Flags

- `--quick | --deep` — depth tier. `--deep` fans out one subagent per
  venue (each gets a self-contained brief: topic, venue, window, pass
  criteria — subagents have no conversation context).
- `--platform x|reddit|both` — default both.
- `--window 7d|30d|90d|1y|all` — overrides mode default.
- `--verify` — before synthesis, chase the top contested claim(s) to
  primary sources (docs, repos, papers) and mark verified/refuted.
- `--radar "<topic>"` (alias `--report`) — full sweep → topic clusters →
  stance mining → budgeted enrichment → `radar.json` + `radar.html` in
  `~/.hivemind/<slug>/<date>/`. Read `references/radar.md` first.

## Initiative

Baseline agents did good things the skill must not suppress: resolving
shortlinks, writing throwaway parsers for odd JSON, caveating flaky
sources. Keep that initiative — the skill constrains *sequence and
evidence discipline*, not creativity inside the phases.

## References

- `references/reddit-playbook.md` — rdt recipes, venue-resolution
  procedure, comment mining. Read at Phase 2–4.
- `references/x-playbook.md` — twitter-cli recipes, floor ladder, thread
  mining. Read at Phase 3–4.
- `references/radar.md` — radar pipeline, KG schema, sweep series
  contract, HTML template usage. Read only for `--radar`.
