# Sweep Manifest — dojo-ai-dev-weekly / 2026-06-12-2

- **Trigger**: `repeat dojo-ai-dev-weekly` (sandbox validation run)
- **Config**: ../config.md, **edition 1** (stated at load)
- **Mode**: trend scan
- **Window**: 2026-05-29 → 2026-06-12 (14d, config)
- **Depth**: SHALLOW per config "Sandbox depth override (operator)" — max 1
  query/venue, n=10, codies-research step (pipeline step 4) skipped, News
  flagged [unverified]
- **Chain**: `social(reddit×7, x) ∥ gh(trending overall + "agent" + SDD
  landscape + OpenSpec releases) → diff(../2026-06-12/) → delivery(issue-draft.md)`
- **Frame suffix**: `-2` (same-day re-sweep; previous frame ../2026-06-12/ intact/immutable)
- **Preflight**: twitter ✓ auth, rdt ✓ auth, gh ✓ (active account:
  pyros-projects), SearXNG 200 (unused — step 4 skipped), papers not in chain
- **Delivery target**: ./issue-draft.md (sandbox — no GitHub issue access per config step 1)

## Venues

Reddit (config list, <1 month old → recon re-confirmation not required):
r/GithubCopilot, r/AI_Agents, r/ClaudeAI, r/LocalLLaMA, r/Rag, r/LangChain,
r/opencode. X: one query (`"github copilot"`, priority topic 1). gh: 4
enumerated pipeline lookups.

## Files (raw/)

| File | What |
| --- | --- |
| r-{githubcopilot,ai_agents,claudeai,localllama,rag,langchain,opencode}-month.json | one `rdt sub <sub> -s top -t month -n 10 --json` per venue; date-filtered to ≥2026-05-29 at triage |
| x-copilot.json | `twitter search '"github copilot"' -t top --min-likes 50 --lang en --since 2026-05-29 -n 10 --json` (no `--exclude retweets` — known CLI trap per config) |
| gh-trending-overall.json | `gh search repos --created=">2026-05-22" --sort=stars --limit 10` |
| gh-trending-agent.json | same + `"agent"` keyword |
| gh-sdd-landscape.json | `gh search repos --sort=stars --limit 10 -- "spec driven development"` |
| gh-openspec-releases.json | `gh api repos/Fission-AI/OpenSpec/releases` (top 5) |
| deep-nerfing.json | `rdt read 1u1s2oz` — Anthropic-nerfing claim (r/LocalLLaMA 1490↑/380c) |
| deep-twomodels.json | `rdt read 1tu82wi` — local-model consensus satire thread (2831↑/709c) |
| deep-promptinjection.json | `rdt read 1u3044z` — opencode prompt-injection/malware incident (93↑/28c) |

## Entity list (diff key for next repeat)

New entities surfaced this frame: superloglabs/superlog, DietrichGebert/ponytail,
study8677/awesome-architecture, MDASH (Microsoft, announced — no repo yet),
Anthropic-nerfing claim (technical report p.13), opencode injection incident
(1u3044z), Copilot app waitlist removal, Qwen-3.6-coding/Gemma-4-creative
consensus. Collision register: "ponytail" and "superlog" are generic words —
qualified by owner (DietrichGebert/, superloglabs/) everywhere; MDASH is a
codename, qualified as "Microsoft MDASH Copilot CLI".

## Adaptations (all operator-override or config-trap driven; NO tool failures)

- SHALLOW override: config's week+month Reddit pair collapsed to a single
  `-t month` query per sub (full 14d window coverage in one query),
  date-filtered at triage (Reddit has no native 14d sort, per config).
- X reduced to 1 query on priority topic 1; known trap honored (no
  `--exclude retweets` combined with min-likes+lang).
- gh's 4 lookups interpreted as named contract steps (not open-ended fan-out)
  and all executed with limit 10 — interpretation recorded here deliberately.
- Deep-reads capped at 3 (config range 3–5, shallow end).
- Step 4 (codies-research) skipped per override → News items [unverified].
- Auto-save to codies-memory inbox skipped: operator write-restriction to
  ~/.hivemind/dojo-ai-dev-weekly/ only.

## Triage rejections (named)

- r/ClaudeAI 1tz1tzv (19194↑) "responding like Claude", 1u18cey (5454↑) "I'm
  ready" — memes, no transferable knowledge.
- r/LocalLLaMA 1tw8eul (2098↑) "Me visiting this sub", 1ttn15z (1473↑) Jensen
  meme — memes.
- r/AI_Agents 1tty1og (136↑) beginner how-to — wrong audience for this issue.
- X @kentcdodds (169 likes) Copilot-app built-in game — fluff; @leereilly
  (105 likes) Rubik's-cube demo — anecdote, kept as sentiment only.
- gh `2aronS/Duel-Agents` (942★) — description too thin to state a "why" and
  research step skipped; named here so the next full run can pick it up.
- gh off-topic: chinese-buy-us-stock-guide, OpenLogi, skylight, b-nnett/goose,
  xiaohei-illustrations, guizang-social-card-skill (see gh-trending.md).

## Diff vs previous frame (../2026-06-12/brief.md) — dropped as already reported

Copilot billing-revolt threads (1tv77df 4757↑, 1tuot1q 2105↑, 1ttlrsq 1537↑,
1ttu30y, 1tudexr, 1turec5, 1ttzj2y), Fable 5 routing 1u1cyx1, rip-AI-out
1u067cf, HITL-theater 1tzbazd, team-killed-agent 1txpn81, AI-inequality
1u1fsdi, RAG 4-approaches 1ttdh20, RAGAS 1u0ynxn (≈ prev 41↑ item),
PDF-parsing 1ttbavs, framework-fatigue 1u05gn6 (≈ prev 105↑ item), SDD harness
1ttts4v, DeepSeek-V4-Flash threads, Gemma 4 drop 1tvtn6m, Fable-5-in-Copilot
tweet, OpenSpec v1.4.0/v1.4.1 releases, all trending repos already in
../2026-06-12/gh-trending.md.

## Staleness check

Topic 3 (loop engineering): 0 dedicated hits this run — NOT counted toward the
2-frame threshold (shallow run carried no dedicated query; structurally thin,
not evidentially thin). All other topics produced in-window signal. No
replacement proposed.

## Crystallize pass

No user-steered deviations (non-interactive run); no tool failures. No config
deltas proposed. Edition remains 1.

## Status

brief.md = synthesis; issue-draft.md = config delivery output (German, 4
sections). Frame immutable once written.
