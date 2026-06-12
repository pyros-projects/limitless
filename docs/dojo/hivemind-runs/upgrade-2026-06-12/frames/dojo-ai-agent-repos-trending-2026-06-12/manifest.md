# Manifest — dojo-ai-agent-repos-trending / 2026-06-12

- **Query:** Trending GitHub repos in the AI agent space, last two weeks, + X/Twitter chatter about them.
- **Mode:** Trend scan (shallow / operator-constrained: max 1-2 queries per source, n ≤ 10).
- **Window:** 2026-05-29 → 2026-06-12.
- **Platforms:** GitHub (gh CLI + trending page scrape) and X (twitter CLI v0.8.5). Reddit NOT used — out of task scope; reduced coverage flagged in brief.
- **Venues:** No subreddit recon (no Reddit); X searched globally with repo-name terms.

## Files (raw/)
| file | what |
|---|---|
| gh1-new-repos.json | `gh search repos --created ">2026-05-29" --sort stars --limit 10 -- "ai agent"` |
| gh2-trending-weekly.html | `curl https://github.com/trending?since=weekly` (parsed twice: first regex grabbed sponsor links for 3 entries; re-parsed h2 anchors → correct names) |
| x1-trending-leaders.json | `twitter search '(last30days OR headroom OR "taste-skill" OR "agent-reach") agent' -t top --min-likes 20 --lang en --exclude retweets --since 2026-05-29 -n 10` → **0 hits (known CLI quirk)** |
| x2-breakouts.json | `twitter search '(superlog OR vigils OR ponytail OR "career-ops" OR "pm-skills") (agent OR claude OR github)' -t top --min-likes 10 --lang en --exclude retweets --since 2026-05-29 -n 10` → **0 hits (same quirk)** |
| x1b-trending-leaders-unfiltered.json | x1 retry, filters dropped per x-playbook bisect rule → 10 hits |
| x2b-breakouts-unfiltered.json | x2 retry (dropped career-ops/pm-skills terms, kept superlog/vigils/ponytail), filters dropped → 10 hits |

## Adaptations
1. `-t top` + `--min-likes`/`--lang`/`--exclude retweets` zeroed out server-side (documented twitter-cli v0.8.5 quirk). Dropped all filters, applied relevance/engagement triage client-side. One retry per query; no extra fan-out.
2. Trending-page HTML parsed with throwaway python; sponsor-link mismatch fixed by re-parsing h2 anchors (no re-fetch).
3. No deep-read pass (thread mining of replies) — omitted under shallow constraint; flagged as next direction.

## Triage rejections (named, with reasons)
- `@wassielawyer, 2,254 likes` (x2b) — Singapore BTO/property fiction; matched "ponytail" (hair) + "agent" (real-estate). Highest-engagement item in the whole sweep; off-topic noise.
- `@pupposandro, 155 likes` (x1b) — "Luce Spark: 35B MoE on a 16 GB GPU" article; matched "headroom" as an English word, not the repo.
- `@b4dchan, 27 likes` (x2b) — "agent provocateurs ... at peace vigils"; matched "vigils" off-topic.
- `@tekbog 55, @sushilwtf 8, @hecubian_devil 2, @0xwhrrari 0` (x2b) — generic Claude/agent chatter, not about any trending repo.
- `@Qmin_AI 0 likes, @JulianGoldieSEO 0 & 12 likes` (x1b) — headroom marketing/engagement-bait posts; kept only as corroboration that a headroom promo wave exists, not as takes.
- GitHub side: apple/container, microsoft/markitdown, NVIDIA/cosmos, trivy, opencv, svelte, tolaria, Open-LLM-VTuber, open-notebook excluded from "agent space" ranking (adjacent or unrelated domains).

## Coverage gaps
- superloglabs/superlog: zero X mentions found in this shallow pass.
- Reddit unqueried; reply threads not mined; `addyosmani/agent-skills` (reported #1 by AI-Rank tweet) seen only second-hand [claimed], not verified against GitHub directly.
