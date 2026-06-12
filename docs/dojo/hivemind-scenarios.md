# Hivemind — Dojo Intake (Scenarios + Pass Criteria)

*Tier: technique · 2026-06-11 · written before any test run (dojo kata 1)*

Source material: `docs/brainstorm/2026-06-11-hivemind-social-search-skill.md`
(archetype questions, hard rules from live smoke tests).

## Training scenarios

### S1 — Trend scan

**Prompt:** "What's currently the new hot shit in AI agent memory systems?"
**Environment note:** twitter and rdt CLIs installed and authenticated; real searches allowed.

Pass criteria (y/n):
1. Ran a recon search before scoped searches
2. Identified ≥2 venues (subreddits) from recon results, not assumption
3. Used time-windowed sorting (`-t week|month` / `--since`)
4. Applied engagement floors on X (`--min-likes`)
5. LLM-triaged for relevance — rejected ≥1 high-engagement-but-off-topic item, or explicitly stated none appeared
6. Deep-read ≥2 threads (comments via `rdt read` / replies via `twitter tweet`)
7. Final answer cites receipts with engagement numbers
8. Offered 2–4 next directions

### S2 — Knowledge mine

**Prompt:** "What does social media say about how optimal Suno prompts look like?"
**Environment note:** same as S1.

Pass criteria (y/n):
1. Venue resolution happened — relevant community (e.g. r/SunoAI) discovered from results or explicitly justified
2. Searches scoped to discovered venue(s)
3. Comments deep-read (`rdt read`), not just post titles
4. Answer splits consensus vs contested
5. Claims labeled observed/claimed/inferred
6. Contradictions resolved or explicitly left open — never averaged

Baseline evidence (pre-recorded 2026-06-11): naive global
`rdt search "suno prompt" -s top -t year` returns r/CuratedTumblr and
r/antiai viral posts with zero Suno content; naive X top-search surfaces
2k-like off-topic prompting tweets. Baseline run not repeated.

### S3 — Degradation

**Prompt:** same as S1, but environment note states: "the `rdt` CLI is NOT installed on this machine; `twitter` is installed and authenticated."

Pass criteria (y/n):
1. Detected the missing CLI (checked, didn't assume)
2. Offered installation (`uv tool install rdt-cli`)
3. Continued single-platform (X) rather than blocking on the install
4. Flagged reduced coverage in the final answer

## Edit E1 — raw-data persistence (2026-06-11, behavior-rule change)

**Change:** every sweep persists working data as a frame
(`~/.hivemind/<slug>/<date>/raw/` + `manifest.md` + `brief.md`) instead
of `/tmp`; `--no-keep` opts out. Trigger eval skipped — description
unchanged.

**Verification scenario E1:** "--quick: what does r/ClaudeCode think
about plan mode?" (fresh subagent, updated bundle)

Pass criteria (y/n):
1. Sweep dir created at `~/.hivemind/<slug>/<date>/` with `raw/`
   containing recon + fan-out JSON
2. `manifest.md` present: query, window, venues, file list, and NAMED
   triage rejections with reasons
3. `brief.md` written in the frame dir
4. No kept working data left in `/tmp`
5. Brief quality unchanged: answer-first, receipts, next directions

## Holdouts — NOT to be used during iteration (dojo kata 5)

### H1 — People/product sentiment

**Prompt:** "What do people on social media think about Codex CLI vs Claude Code these days?"

Pass criteria (y/n):
1. Venue recon performed
2. Both-sides stance mining with receipts (positive and negative per product)
3. No truth-claims derived from sentiment (epistemic labels present)

### H2 — Radar mode on a thin topic

**Prompt:** "--radar 'agentic knowledge graphs'"

Pass criteria (y/n):
1. Full sweep pipeline runs (recon → fan-out → triage → cluster → stances → enrichment)
2. Thin-results adaptation triggered and stated (floor lowered or window widened)
3. radar.json emitted; every claim carries provenance + observed_at
4. radar.html rendered from the JSON using the fanzine template (both views present)
5. Enrichment ≤3 lookups per topic
6. Files land in `~/.hivemind/agentic-knowledge-graphs/<date>/`

---

# Upgrade battery — 2026-06-12: Configs by Demonstration & Pivot Chains

*Tier: technique · written before any test run (dojo kata 1). Source:
`docs/brainstorm/2026-06-12-hivemind-crystallize-repeat.md`. Operator
constraint: search depth LOW everywhere — shallow caps baked into every
prompt; 4 of 8 scenarios are fully synthetic (zero network).*

Baseline policy: T1A/T1B/T4/T5/T6 get live RED runs (current 0.10.2
SKILL.md in context — the honest "today" condition). T2/T3 baselines
skipped per dojo rule "failure already concretely evidenced": the
2026-06-12 ai-dev-weekly session is the recorded evidence — preferences
evaporated mid-session (silent-drift lesson IN-20260612-1f82), no agent
offered any config mechanism, and the current skill contains no config
concept to trigger one.

## Training scenarios

### T1A — Chain classification: gh discovers, social reacts

**Prompt:** "What are the trending GitHub repos in the AI agent space
from the last two weeks, and what is X/Twitter saying about them? Keep
it quick and shallow — at most 1-2 queries per source, small result
counts (-n 10ish)."
**Env note:** twitter + rdt CLIs installed and authenticated; gh CLI
authenticated; real searches allowed but SHALLOW.

Pass criteria (y/n):
1. Chain stated explicitly before fan-out: gh = discover, social = react
2. gh used for discovery (search by created/stars), not social
3. Social queries scoped to repo names extracted from gh results, not
   to the generic topic
4. Chain + pivot entity list recorded in manifest (frame contract)
5. Receipts carry venue-appropriate notation (★/dates for gh)

### T1B — Chain classification: reddit discovers, gh enriches

**Prompt:** "Check out which GitHub repos are getting the most mentions
on r/LocalLLaMA and r/ClaudeAI lately — quick shallow pass, 1-2 queries
per venue, small -n."
**Env note:** same as T1A.

Pass criteria (y/n):
1. Chain stated explicitly: reddit = discover (mention mining),
   gh = enrich
2. Reddit mined first; repo entities extracted from posts/comments
3. gh used per-entity for factual enrichment (stars/recency/release),
   NOT generic gh trending
4. Chain + entity list in manifest
5. Enrichment adds metadata only — no social claims presented as
   gh-validated facts

### T2 — Lookup: standing config binds an ad-hoc ask

**Setup:** synthetic config at `~/.hivemind/dojo-rust-async/config.md`
(intent: rust async runtimes; exclusion: "mute async-std content —
deprecated, user doesn't care"; edition 1).
**Prompt:** "what does reddit think about rust async runtimes these
days? quick shallow pass, 1-2 queries, small -n."
**Env note:** rdt installed/authenticated; configs may exist under
`~/.hivemind/<slug>/config.md`.

Pass criteria (y/n):
1. Checked for an existing config matching the ask before sweeping
2. Stated which config bound the sweep (slug + edition)
3. Honored the exclusion (async-std absent or explicitly excluded)
4. Config not silently rewritten (no writes to config.md)

### T3 — Crystallize-on-deviation (zero network)

**Setup:** scripted session transcript provided inline: a completed
sweep (synthetic manifest + brief excerpts) during which the user made
two corrections ("make the window 30 days, not 7" and "drop the
per-platform sections — one merged ranked list") and closed with "good,
let's do this monthly before my newsletter".
**Prompt:** "Wrap up the session."

Pass criteria (y/n):
1. Recurrence smell detected → crystallize offered
2. Proposal contains BOTH corrections mapped to concrete config lines
3. Nothing written to ~/.hivemind before user confirmation
4. Proposal carries edition + dated changelog structure

### T4 — Pivot fidelity (zero network, dry-run queries)

**Setup:** synthetic gh discover output provided inline: 5 repos
including one trap name (`memory` by org `acme-ai` — generic word).
**Prompt:** "Continue the sweep: plan the react stage for community
reaction. Write the EXACT queries you would run (do not execute)."

Pass criteria (y/n):
1. Queries scoped to the extracted repo entities, not the original
   topic terms
2. Trap entity qualified (org name / "github" qualifier), not searched
   as bare generic word
3. Pivot entity list written out for the manifest

### T5 — Mixed-grade synthesis + citation lag (zero network)

**Setup:** synthetic raw results inline from three venues: 2 arXiv
papers (3 weeks old, 0 citations), 1 gh repo (800★ in 2 months), 5
tweets incl. a 2k-like claim "X makes RAG obsolete" with no source.
**Prompt:** "Synthesize the brief from this sweep data."

Pass criteria (y/n):
1. Receipts per evidence grade ([gh, 800★, created…], [arXiv …, 0
   cites — too fresh], [@user, 2k likes])
2. The 2k-like claim labeled [claimed], NOT presented as validated
3. Cross-grade echo flagged where paper+repo+social align
4. Citation-lag caveat on fresh papers (recency/venue triage, not
   "uncited therefore weak")

### T6 — Tool failure: named venue dead (no silent substitution)

**Prompt:** "what does reddit say about Claude Code skills? quick
shallow pass."
**Env note:** "`command -v rdt` returns nothing on this machine — the
rdt CLI is NOT installed. Do not install tools without offering first.
twitter CLI installed and authenticated. SearXNG runs at
localhost:8888."

Pass criteria (y/n):
1. Missing CLI detected; 10-second fix (`uv tool install rdt-cli`)
   offered FIRST
2. Reddit was NAMED → no silent substitution (no lemmy/X/web results
   presented as the answer to "what does reddit say")
3. Nearest-alternative offered explicitly as a user decision (or
   honest can't-run with options)
4. No scraping workarounds before the fix offer

## Holdouts — NOT to be used during iteration (kata 5)

### H3 — Cold replay, sandboxed (differs in kind: full config execution)

**Setup:** sandboxed copy of the real ai-dev-weekly config at
`~/.hivemind/dojo-ai-dev-weekly/config.md` with delivery target
rewritten to a local file (NO `gh auth switch`, NO GitHub issue write —
safety edits only, recipe otherwise verbatim) + the real 2026-06-12
frame copied in as previous frame. Shallow-depth note appended (1 query
per venue, -n 10).
**Prompt:** "repeat dojo-ai-dev-weekly"

Pass criteria (y/n):
1. Config loaded; edition stated
2. Recipe executed (venues, window, traps respected) without asking
   anything the config already answers
3. Diff vs previous frame attempted; repeats dropped or no-overlap
   stated
4. Output per config format spec (German, single-paragraph items,
   the four sections)
5. Frame written under the sandbox slug per frame contract
6. Closing crystallize pass: deviations proposed, nothing auto-written

### H4 — Staleness proposal (differs in kind: config lifecycle rule)

**Setup:** synthetic config (3 topics, staleness rule "thin 2
consecutive sweeps → propose replacement") + two synthetic prior frames
where topic 3 was thin in both; this run's recon (provided inline)
shows topic 3 thin a third time.
**Prompt:** "Here are this run's recon results — continue the repeat."

Pass criteria (y/n):
1. Staleness rule fired, citing the config's threshold
2. Replacement proposed with evidence from BOTH prior frames named
3. Propose-confirm honored — config not silently edited

## Verbatim subagent prompts + results (appended during kata 2–6)

### Kata 2 — baseline (RED) runs, 2026-06-12

All baselines: fresh general-purpose subagents, current 0.10.2 SKILL.md
pointed at by path (subagents read it + references themselves — honest
"today" condition). Shared prompt skeleton (T1A shown verbatim; others
differ only in Task line / env note / inlined fixture as noted):

> You are working on the following task. Use whatever approach you
> think is right.
>
> Available context: The hivemind skill is installed for social-media
> research — read /home/pyro/projects/private/limitless/plugins/limitless/skills/hivemind/SKILL.md
> first and follow it where it applies, including any reference files
> it points you to (they live in references/ beside it). Environment:
> the `twitter` and `rdt` CLIs are installed and authenticated; the
> `gh` CLI is installed and authenticated; SearXNG runs at
> localhost:8888. Real searches are allowed. IMPORTANT operator
> constraints: keep ALL searches SHALLOW — at most 1-2 queries per
> source, result counts -n 10 or smaller, no deep fan-out; if you
> persist any frame under ~/.hivemind, prefix the topic slug with
> `dojo-`.
>
> Task: "What are the trending GitHub repos in the AI agent space from
> the last two weeks, and what is X/Twitter saying about them? Keep it
> quick and shallow — at most 1-2 queries per source, small result
> counts."
>
> Your final message is raw working data for analysis, not a
> user-facing summary: report what you did step by step (commands run,
> decisions made, in order), then your result.

- T1B Task: "Check out which GitHub repos are getting the most mentions
  on r/LocalLLaMA and r/ClaudeAI lately — quick shallow pass, 1-2
  queries per venue, small -n."
- T4: planning-only variant; fixture `fixtures/t4-discover.json` inlined
  verbatim; Task: "Continue the sweep: plan the next stage — community
  reaction to these findings. Write the EXACT queries you would run (do
  not execute them), plus anything you would record for the sweep's
  records."
- T5: synthesis-only variant; fixture `fixtures/t5-sweep-data.md`
  inlined verbatim; Task: "Synthesize the brief from this sweep data."
- T6: env note replaced with: "Environment ground truth for this
  exercise (treat as fact, do not re-verify): `command -v rdt` returns
  nothing — the rdt CLI is NOT installed on this machine. Do NOT invoke
  rdt, and do NOT install any tool without offering to the user first.
  The `twitter` CLI is installed and authenticated. SearXNG runs at
  localhost:8888." Task: "what does reddit say about Claude Code
  skills? quick shallow pass."

**Results:**

| Run | Score | One-line result |
|---|---|---|
| T1A | 3/5 | gh-discovery + repo-scoped X queries done well; chain never STATED, manifest has no chain/pivot-entity fields (c1 ❌, c4 ❌) |
| T1B | 1/5 | Superb reddit mention-mining (regex parser, 37 repos, named triage); gh enrich stage never ran — no stars/recency on any entity (c1 ❌, c3 ❌, c4 ❌, c5 ❌) |
| T4 | 3/3 | Baseline PASS — built a collision risk register unprompted ("never search the bare word memory"), org/URL-qualified queries, entity tally planned for manifest. Criterion likely tests the model; kept as load-bearing guard |
| T5 | 4/4 | Baseline PASS — grade-aware receipts, [claimed] on the 2k-like hype tweet, three-way cross-grade echo flagged, citation-lag caveat verbatim ("too young for citation signal, not a red flag") |
| T6 | 0/4 | Ran searxng `site:reddit.com` scrape BEFORE surfacing the install offer (rationalization: "I run non-interactively, the offer is surfaced in the brief instead"); snippets presented as "what reddit says"; no user decision point |

**Curriculum (what GREEN must teach explicitly):**
1. The chain is *classified and stated out loud* — discover/enrich/
   react/verify roles, in brief coverage + manifest (T1A/T1B c1).
2. Entity asks get their enrich stage: "most mentioned repos" without
   per-entity gh metadata is an incomplete answer (T1B c3).
3. Manifest extension: `chain:` line + explicit pivot entity list
   (T1A/T1B c4).
4. Named-venue degradation ORDER: fix offer comes before ANY proxy
   work, even non-interactively (offer leads the reply); proxy results
   are labeled proxy-of-<venue>, never presented as the venue; the
   substitute is a user decision (T6 c1–c4).
5. Configs: lookup-before-sweep, crystallize offer, propose-confirm
   (T2/T3, evidence-based).
6. Bug harvested by T4 subagent: SKILL.md Phase 2 example uses
   `twitter search … -c`, which the x-playbook quirk list says doesn't
   exist — fix in GREEN.
7. Preserve baseline strengths: collision registers, throwaway
   parsers, mixed-grade synthesis — encode as standard, don't suppress.

### Kata 4 — pressure (GREEN) runs, 2026-06-12

Fresh subagents, upgraded SKILL.md + playbooks read from disk by path
(same prompt skeleton as kata 2; T2/T3 prompts per battery — T2 env
note adds "Saved sweep configs may exist under ~/.hivemind/<slug>/
config.md"; T3 inlines fixtures/t3-transcript.md and forbids writes
without transcript-user confirmation).

| Run | Score | Notes |
|---|---|---|
| T1A | **5/5** | Chain stated up front + in manifest; pivot list with ★/day; collision register; same-day `-2` suffix honored; gh account stated (pyros-projects) |
| T1B | **5/5** | reddit(discover)→gh(enrich) stated; entities mined then enriched via ONE batched GraphQL query; diffed against the morning baseline frame and noted it "skipped the gh enrich stage — SKILL says an entity ask is incomplete without it" |
| T2 | **4/4** | Config found, "edition 1" stated, async-std exclusion honored, config untouched; correctly refused a config delta for operator-imposed shallowness ("degradation is not intent") |
| T3 | **4/4** | Crystallize offered on "monthly" smell; proposal maps BOTH corrections + the floor adaptation that held; explicit "nothing written until confirm"; edition + changelog present; template structure followed |
| T4 | **3/3** | Entity-scoped queries, qualification register, explicit pivot list labeled "diff key for repeat"; bonus: "auth asserted != auth probed" |
| T5 | **4/4** | Cross-grade echo is the lead sentence; 2k-like claim downgraded with engagement-vs-evidence inversion named; citation-lag rule cited verbatim |
| T6 | **4/4** | Fix offer is the FIRST line of the reply; proxy-of-reddit labeling throughout; twitter deliberately not substituted (named venue); no comment scraping |

**29/29 — first-try pass, no loophole-closing edits required.**
Subtlety noted for the record: in non-interactive runs the "offer
before proxy work" rule can only manifest as offer-leads-the-reply +
labeled proxy; T6's criterion intends exactly that and passes.

### Kata 5 — graduation (holdouts run once, no edits between), 2026-06-12

H3 prompt (verbatim Task line): "repeat dojo-ai-dev-weekly" — sandbox
config at ~/.hivemind/dojo-ai-dev-weekly/config.md (real ai-dev-weekly
recipe; delivery rewritten to local issue-draft.md, no gh account
switch, shallow depth override appended; previous frame copied in).
H4 prompt: continue "repeat dojo-agent-evals" mid-run with inline
ground-truth recon results (topic 3 thin a third time); "Do not write
anything to config.md."

| Holdout | Result | Notes |
|---|---|---|
| H3 cold replay | **6/6 PASS** | Edition stated; depth override honored; CLI trap respected (no --exclude retweets with min-likes+lang); diff vs previous frame itemized incl. a CORRECTION of the prior frame's "GA" framing; German 4-section issue-draft.md delivered; frame at 2026-06-12-2 per contract; null crystallize pass correct (no deviations → no deltas, edition stays 1). Sound judgment call recorded: 4 config-enumerated gh lookups treated as contract steps, not open fan-out |
| H4 staleness | **3/3 PASS** | Threshold cited (2, met at strike 2 — conservative reading noted); evidence from ALL thin frames (1/0/0 relevant); propose-confirm held with A/B/C options + drafted changelog line; bonus: Option B proposes re-homing the topic to the papers venue — venue-graph reasoning unprompted |

### Kata 6 — trigger eval, 2026-06-12

Matrix: 15 prompts (8 positives incl. 2 German, 7 near-miss negatives),
judge given 10-skill description subset + none. Prompt file preserved at
hivemind-runs/upgrade-2026-06-12/trigger-eval-prompt*.md (v1, v2, final).

- Runs 1–2 (initial description): 29/30 — collision: "find me a paper
  on retrieval-augmented generation" → hivemind in run 1 (unstable).
- Bounded fix: explicit NOT-for-single-item-lookups carve-out added to
  the description. Runs 3–4: **30/30, identical**.
- Frontmatter gate then failed twice (1145 > 1024; then YAML colon+space
  — both known Codex-loader failure modes from suno-pack). Trimmed to
  1014 + colon→dash. Final runs 5–6 with shipped description: **30/30**
  (prompt 10 split searxng/codies-research across runs — both legal).
