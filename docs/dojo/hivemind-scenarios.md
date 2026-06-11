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
