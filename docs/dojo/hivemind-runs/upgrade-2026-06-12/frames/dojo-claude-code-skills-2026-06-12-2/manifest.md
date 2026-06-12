# Manifest — dojo-claude-code-skills / 2026-06-12-2

**Query:** "what does reddit say about Claude Code skills? quick shallow pass"
**Mode:** knowledge mine, --quick tier (user asked for quick shallow pass)
**Window:** none enforced; snippet dates observed Oct 2025 – Apr 2026
**Platforms requested:** Reddit (named venue, explicit)
**Chain:** none — single-venue social ask
**Same-day re-sweep:** prior frame `../2026-06-12/` ran the identical ask;
this frame carries the `-2` suffix per the frame contract and was diffed
against the prior frame (already-reported items dropped from the brief
unless materially developed).

## Environment / degradations
- `rdt` CLI NOT installed (environment ground truth; not re-verified per
  exercise instructions, never invoked). Fix offer (`uv tool install
  rdt-cli`) leads the brief — non-interactive run, so the offer is stated
  before the degraded results, per skill Phase 0.
- Reddit coverage is **proxy-of-reddit**: SearXNG `site:reddit.com`
  snippets only. No comment deep-reads, engagement numbers only where a
  snippet happened to include them. No raw-JSON-endpoint or mirror
  workarounds used (skill forbids them ahead of the fix offer).
- `twitter` CLI installed + authenticated (ground truth) but NOT used:
  the user named Reddit; named venues are never silently substituted.
  Prior same-day frame also recorded 0 X hits for this topic.
- SearXNG localhost:8888 probed: 200, JSON enabled.
- Config lookup: `ai-dev-weekly` and `dojo-rust-async` configs exist;
  neither matches this ask's intent. No config constraints applied.

## Files
- `raw/web-r1-phrase.json` — SearXNG `"claude code skills" site:reddit.com`,
  38 results, top 10 triaged.
- `raw/web-r2-agentskills.json` — SearXNG `claude "agent skills"
  site:reddit.com`, 11 results, top 10 triaged.
- Shallow budget honored: 2 queries total, n≤10 read per query.

## Venue frequency count (proxy recon, from result URLs, both queries)
- r/ClaudeAI: 8 — primary venue
- r/ClaudeCode: 6 — primary venue
- r/claude: 2, r/AI_Agents: 2 — secondary
- r/claudeskills: dedicated subreddit exists (surfaced as a venue, new)

## Triage decisions
- **No off-topic rejections this run** — all triaged results concern
  Claude Code/Agent skills.
- **Dedups (not rejections):** `?tl=de` German-translation URLs of
  1qjaq92 and 1s2dacs collapsed into canonical URLs; 1s51cre
  (r/AI_Agents) is a crosspost of 1s51b5u (r/claude) — clustered as one
  story and flagged as cross-sub echo; 1p0n64q (r/ClaudeCode) is a
  crosspost of 1p0n7pg (r/ClaudeAI) — same clustering.
- **Dropped via diff vs prior frame** (already reported, no material
  development): 1s51b5u (March 2026 curation post), 1qjaq92 (30+ skills
  collection), 1s2dacs (mobile-apps skills), 1pd7847 (multi-agent
  editorial team).
- **Kept despite prior report** (material development): 1p0n7pg
  meta-skill post — crosspost snippet adds the "Heal Skill" repair
  system detail.

## New-this-run items (diff key)
1typx6i, 1q5i4a5, 1ojuqhm, 1oz0ed8, 1obq6wq, 1ohc97r, 1s5bo5v,
1qcigma, 1pxou18, 1sf75oz, 1orozs4, r/claudeskills (venue).

## Adaptations
- None within the venue passes (both queries returned ample results; no
  floor/window changes needed).
