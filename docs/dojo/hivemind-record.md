# Dojo record — hivemind

*Tier: technique · 2026-06-11 · Claude (Fable 5) + Pyro*

## Baseline findings (RED)

Run 2026-06-11, fresh general-purpose subagents, no skill. Honest note:
baseline quality far exceeded the concept doc's assumptions — both agents
self-corrected away from unscoped-search garbage and produced strong
briefs. The frontier-headroom insight cuts both ways. The skill's value
is in the specific gaps below, consistency across runs, token efficiency
(S1 burned 85k tokens, S3 94k — much of it on reinventable plumbing), and
the radar/series machinery no baseline produces.

| Scenario | Criterion | Result | Failure mode observed |
|---|---|---|---|
| S1 | 1 recon before scoped | ⚠️ | Broad X sweep first, yes — but Reddit went scoped immediately |
| S1 | 2 venues from recon, not assumption | ❌ | Subreddits (r/LocalLLaMA, r/AI_Agents…) chosen from priors; first unscoped `rdt search` returned r/all garbage incl. a 600KB post, agent adapted by *assuming* venues rather than frequency-counting results |
| S1 | 3 time-windowed sorting | ✅ | `--since`, top/month used |
| S1 | 4 engagement floors on X | ✅ | `--min-likes 50` |
| S1 | 5 explicit relevance triage | ❌ | Filtering happened implicitly; no stated rejection of high-engagement off-topic items |
| S1 | 6 deep-read ≥2 threads | ✅ | 4 Reddit posts w/ comments, tweet replies pulled |
| S1 | 7 receipts w/ engagement | ✅ | Throughout |
| S1 | 8 next directions | ❌ | None offered |
| S3 | 1 detected missing CLI | ✅ | (given in env note; no `command -v` check performed) |
| S3 | 2 offered install | ❌ | Never mentioned `uv tool install rdt-cli`; instead burned ~6 failed workaround attempts (reddit.com JSON 403, pullpush, jina proxy…) before finding a working redlib instance |
| S3 | 3 continued without blocking | ✅ | Exceeded: got Reddit data via redlib anyway |
| S3 | 4 flagged reduced coverage | ✅ | Rate-limit gaps caveated |
| S2 | (pre-recorded evidence) | ❌ | Manual smoke test 2026-06-11: global `rdt search "suno prompt" -s top` → r/CuratedTumblr + r/antiai viral noise; X top-search → 2k-like off-topic prompting tweets. Note: agent-level baselines partially self-correct; the skill makes the correction *systematic*. |

**Curriculum (what the skill must teach explicitly):**
1. Venue resolution is a *procedure* (frequency-count the recon results), not a vibe or a prior.
2. Relevance triage is *stated*: name what was rejected and why, or state nothing needed rejection.
3. The brief always ends with 2–4 next directions.
4. Degradation protocol: missing CLI → offer the 10-second `uv tool install` BEFORE any proxy spelunking; continue single-platform while the user decides.
5. Preserve baseline strengths — don't suppress initiative (link resolution, ad-hoc parsing, caveat-flagging were all good).

## Pressure-test (GREEN) — 2026-06-11

Fresh subagents, SKILL.md + both playbooks in context, real searches.

| Scenario | Score | Notes |
|---|---|---|
| S1 trend scan | **8/8** | Venues frequency-counted from recon (r/AI_Agents 5, r/ClaudeAI 3, r/LocalLLaMA 3, r/ClaudeCode 2); triage rejections named (15/15 global-control noise, crypto shills, 797-like off-topic virality); 11 deep-reads; 4 next directions |
| S2 knowledge mine | **6/6** | r/SunoAI discovered 20/25 in recon; consensus/contested split; epistemic labels; contradiction resolved by evidence strength (QUALITY_ULTRA placebo). Bonus: auto-save rule fired correctly — judged findings load-bearing for suno-pack from repo context, saved brief to codies-memory inbox |
| S3 degradation | **4/4** | `command -v` check; install offer stated BEFORE any workaround (ordering held); continued degraded with coverage flagged |

First-try pass — no loophole-closing edits required.

## Loopholes closed

| # | Loophole | Edit that closed it |
|---|---|---|
| — | none — all 18 criteria passed first GREEN run | |

Reference-accuracy improvements harvested from the runs (not loopholes —
both playbooks updated): twitter `search` lacks `-c`; `top`+`--min-likes`
can return 0 server-side (drop floor, filter client-side); `-o` emits
bare lists / raw Reddit listings; `rdt read` and `twitter tweet` lack
`-o`; reply fetches can contain injected timeline filler.

## Rejected fixes

| # | Attempted edit | Why it didn't survive |
|---|---|---|
| — | none | |

## Graduation — 2026-06-11, holdouts run once, no edits between

| Holdout | Result | Notes |
|---|---|---|
| H1 people sentiment (Codex CLI vs Claude Code) | **3/3 PASS** | Venues frequency-counted (r/ClaudeAI 11, r/ClaudeCode 6, r/codex 3); both-sides stance mining with receipts and per-venue bias caveats; epistemic labels throughout, pricing claims flagged unverified; bonus: detected astroturfing dimension and discounted engagement accordingly |
| H2 radar thin-topic (`--radar "agentic knowledge graphs"`) | **5/5 PASS + 1 n/a** | Full pipeline; 243 posts triaged → 6 topics; radar.json schema-verified by orchestrator (provenance + observed_at on every claim, enrichment ≤3/topic); radar.html rendered from JSON on fanzine template, browser-verified both views, 0 console errors; correct `~/.hivemind/agentic-knowledge-graphs/2026-06-11/` + index.html. Criterion 2 (thin-results adaptation) **n/a — scenario assumed thinness that didn't materialize** (25 recon hits); adaptive behavior was nonetheless demonstrated and stated (flag bisection, client-side floors, out-of-window exclusions) |

Post-graduation reference-accuracy edit (not a loophole): x-playbook quirk
list extended — `-t top` breaks server-side with `--exclude`/`--lang` too
(flag bisection procedure added); `--min-likes` on `latest` may be
silently unenforced.

## Trigger matrix

Run 2026-06-11, two fresh routing-judge subagents, identical prompts,
14-skill description list (full research-skill neighborhood: codies-research,
searxng, deep-research, article-pack + read-only trap).

| # | Prompt | Expected | Got (run 1 / run 2) | Pass |
|---|---|---|---|---|
| 1 | what's the hot shit in rust tooling right now | hivemind | hivemind / hivemind | ✅ |
| 2 | what does social media say about MCP security | hivemind | hivemind / hivemind | ✅ |
| 3 | what does reddit think of the new Suno version | hivemind | hivemind / hivemind | ✅ |
| 4 | check the socials for reactions to the Claude release | hivemind | hivemind / hivemind | ✅ |
| 5 | ask the hivemind about local LLM agents | hivemind | hivemind / hivemind | ✅ |
| 6 | what are people saying about devcontainers | hivemind | hivemind / hivemind | ✅ |
| 7 | --radar AI coding agents | hivemind | hivemind / hivemind | ✅ |
| 8 | is twitter hyped about anything new in image gen | hivemind | hivemind / hivemind | ✅ |
| 9 | search the web for SearXNG docker setup | searxng | searxng / searxng | ✅ |
| 10 | what's the latest on the EU AI Act, with sources | codies-research | codies-research / codies-research | ✅ |
| 11 | write me a deep research report on vector DB pricing | deep-research | deep-research / deep-research | ✅ |
| 12 | write me an article about agent memory | article-pack | article-pack / article-pack | ✅ |
| 13 | look up the twitter API docs | searxng or codies-research (declared) | codies-research / codies-research | ✅ |
| 14 | post this on twitter | none (read-only) | none / none | ✅ |

Score: 14/14, both runs in full agreement · Collisions: none — the
codies-research boundary ("what's the latest on X, with sources") held.

## Known limitations

- **X CLI server-side filter bugs** (top tab × min-likes/exclude/lang →
  0 hits; latest × min-likes unenforced): worked around via documented
  flag-bisection + client-side filtering, but coverage depends on the
  unfiltered result page the CLI returns.
- **X auth is cookie/session-fragile**; `rdt login` likewise
  cookie-based. A dead session degrades to single-platform per Phase 0.
- **Radar HTML quality depends on the session model** — the template
  constrains structure, not taste. Sweep №1 had no prior frame, so the
  delta-baking path (NEW/GONE stickers, ▲ heat) is designed but not yet
  exercised — verify on the second sweep of any topic.
- **H2's thin-results criterion went n/a** (topic wasn't thin); the
  adaptive-floor ladder is exercised, but true zero-result reformulation
  has only baseline-level evidence.
- Trigger matrix tests clean-room routing, not live harness selection
  with conversation context.
- Engagement numbers in briefs are fetch-time snapshots; Reddit/X scores
  drift.

**Belt rank: pressure-test 18/18 · graduation 8/8 (+1 n/a) · triggers
14/14.** Shipped 2026-06-11 in limitless v0.7.0.
