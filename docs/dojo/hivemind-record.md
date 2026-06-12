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

### Extension matrix — idea-mining / non-sentiment phrasings (2026-06-11, post-ship)

Question from Pyro: does hivemind trigger on "search the socials for
ideas about…" and other non-sentiment queries? Two fresh judges, live
description list incl. wd-local-websearch as extra collision candidate.

| # | Prompt | Expected | Got (1/2) | Pass |
|---|---|---|---|---|
| 1 | search the socials for ideas about a weekend hack project | hivemind | hivemind / hivemind | ✅ |
| 2 | mine reddit for app ideas in the fitness niche | hivemind | hivemind / hivemind | ✅ |
| 3 | find inspiration on twitter for my landing page copy | hivemind | hivemind / hivemind | ✅ |
| 4 | what features do people wish existed in note-taking apps | hivemind | hivemind / hivemind | ✅ |
| 5 | scan social media for content ideas for my next article | hivemind (not article-pack) | hivemind / hivemind | ✅ |
| 6 | search the web for ideas about team offsites | searxng | searxng / searxng | ✅ |
| 7 | brainstorm ideas for a new plugin with me | brainstorming | brainstorming / brainstorming | ✅ |
| 8 | find recent articles about agent memory | searxng | searxng / searxng | ✅ |

Score: 8/8 both runs · No description change needed. Row 4 shows the
"best answer lives in threads" catch-all carries platform-less community
questions; row 5 shows article-pack doesn't steal idea-sourcing prompts.

## Edit E1 — raw-data persistence (2026-06-11, post-ship)

**Loophole (caught by Pyro):** raw sweep data (recon, fan-out, deep-read
comment trees, triage pool) was written to `/tmp` and discarded — only
the synthesized brief survived. Re-triage required re-searching, and
fetch-time scores made frames irreproducible. Radar was the only mode
producing durable output.

**Bounded edits:** SKILL.md — Phase 3 now targets the frame dir; new
"Every sweep is a frame" section (`~/.hivemind/<slug>/<date>/raw/` +
`manifest.md` with named triage rejections + `brief.md`; `--no-keep`
opt-out); flags list. radar.md — sweep-series contract generalized to
all sweeps. Trigger eval skipped: description unchanged.

**Verification (scenario E1, fresh subagent, `--quick` plan-mode query):
5/5.** Frame created with full raw/ (recon + 4 fan-out + 5 deep-reads +
parsers), manifest with named rejections and adaptations, brief.md
written, zero /tmp leftovers, brief quality unchanged (answer-first,
receipts, 4 next directions). Bonus accuracy fix harvested: raw-listing
shape applies to scoped-search stdout too + `▸ More:` pagination line —
reddit-playbook updated.

**Data rescue:** the three pre-edit sweeps (suno-experiment-techniques,
suno-optimal-prompts 2.7M, agentic-knowledge-graphs raw 4.6M) were
rescued from /tmp into proper frames with retroactive manifests before
the edit landed.

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

---

# Upgrade record — 2026-06-12: Configs by Demonstration & Pivot Chains

*Tier: technique · 2026-06-12 · Claude (Fable 5) + Pyro · ships in
limitless 0.11.0. Design doc:
`docs/brainstorm/2026-06-12-hivemind-crystallize-repeat.md` · battery +
verbatim prompts: `hivemind-scenarios.md` (upgrade section) · evidence:
`hivemind-runs/upgrade-2026-06-12/`*

## Baseline findings (RED)

Current 0.10.2 skill in context (honest "today" condition). T2/T3
baselines skipped on recorded evidence (silent-drift lesson
IN-20260612-1f82; no config concept exists to trigger).

| Scenario | Score | Failure mode observed |
|---|---|---|
| T1A gh→social | 3/5 | Chain never stated; no chain/pivot-entity fields in manifest |
| T1B reddit→gh | 1/5 | Excellent mention mining; gh enrich stage never ran — mention counts with no stars/recency |
| T4 pivot fidelity | 3/3 | Baseline PASS (collision register unprompted) — guards load-bearing behavior, likely tests the model |
| T5 mixed-grade | 4/4 | Baseline PASS — kept as synthesis-discipline guard |
| T6 named venue dead | 0/4 | searxng site:reddit.com scrape BEFORE the install offer ("non-interactive" rationalization); snippets presented as "what reddit says" |

Curriculum: chain stated out loud; enrich is mandatory for entity asks;
manifest gains chain + pivot entity list; fix-offer leads the reply even
non-interactively + proxy-of-<venue> labeling; config verbs. Harvested
bug: Phase 2 example used `twitter search -c` (flag doesn't exist) —
fixed.

## Pressure-test (GREEN)

**29/29, first-try pass** — all seven scenarios (T1A 5/5, T1B 5/5,
T2 4/4, T3 4/4, T4 3/3, T5 4/4, T6 4/4). Highlights: T1B enriched via
one batched GraphQL query and flagged the morning baseline frame's
missing enrich stage against the skill's own rule; T2 refused a config
delta for operator-imposed shallowness ("degradation is not intent");
T6 led with the fix offer and deliberately did not substitute twitter
for the named reddit ask.

## Loopholes closed

| # | Loophole | Edit that closed it |
|---|---|---|
| 1 | Trigger: "find me a paper on X" routed to hivemind (1 of 2 judge runs) | Description carve-out: NOT for single-item lookups — use search/research skills |

## Rejected fixes

| # | Attempted edit | Why it didn't survive |
|---|---|---|
| — | none | (frontmatter-length + YAML-colon fixes were packaging gates, not behavior loopholes) |

## Graduation — holdouts run once, no edits between

| Holdout | Result | Notes |
|---|---|---|
| H3 sandboxed cold replay (`repeat dojo-ai-dev-weekly`) | **6/6 PASS** | Edition stated; recipe + traps honored with zero questions; diff vs previous frame incl. correcting its "GA" framing; German issue-draft per spec; null crystallize pass correct |
| H4 staleness proposal | **3/3 PASS** | Threshold + per-frame evidence cited; propose-confirm held; bonus: proposed re-homing the dead topic to the papers venue |

## Trigger matrix

15 prompts (8 positives incl. "wiederhole den Sweep von letzter Woche"
and "frier den Prozess ein"-family, 7 near-miss negatives), 10-skill
description list + none, exact match. Final description (post carve-out
+ frontmatter trim): **30/30 in both runs**, no collisions. Full matrix
+ per-run outputs in hivemind-scenarios.md kata 6 section.

## Known limitations

- T4/T5 criteria passed baseline — they guard model-level strengths the
  skill standardizes (collision registers, grade labels), not behavior
  the skill creates. Watch on model downgrades.
- "Offer before proxy work" in non-interactive runs can only manifest
  as offer-leads-the-reply + labeled proxy; a subagent cannot actually
  wait for a user decision.
- Cold replay validated against a sandboxed config (local delivery, no
  gh account switch). The real ai-dev-weekly delivery step (issue body
  write, account switch) remains exercised only by the original
  hand-run session.
- Plugin cache reload not possible mid-session: pressure/holdout
  subagents read the new SKILL.md by path. `/reload-plugins` +
  smoke-invoke pending on Pyro's side after pulling 0.11.0.
- SearXNG JSON formats flag lives inside the container — an image
  upgrade/recreate reverts it to 403 (preflight catches it;
  web-playbook documents the fix).
