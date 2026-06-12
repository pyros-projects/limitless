# Brief — Trending AI-agent GitHub repos (2026-05-29 → 2026-06-12) + X chatter

## TL;DR
The last two weeks in the AI-agent space belong to **agent skills and context infrastructure**, not new frameworks. The breakout repos are `mvanhorn/last30days-skill` (+12.4k stars/wk, multi-platform social research skill), `chopratejas/headroom` (+11.3k/wk, 60-95% token compression layer), `Leonxlnx/taste-skill` (+8.4k/wk, anti-slop design taste), `Panniantong/Agent-Reach` (+5.2k/wk, agent internet access), plus skill marketplaces (`phuryn/pm-skills`, `santifer/career-ops`). X chatter converges on one meta-take: skills/plugins are becoming the distribution format for agent behavior — "the new IDE layer." [inferred from cross-source agreement]

## Trending repos (GitHub, observed)
**Established-repo star velocity (trending weekly page):**
| repo | +stars/wk | what |
|---|---|---|
| mvanhorn/last30days-skill | +12,422 | agent skill: research any topic across Reddit/X/YouTube/HN/Polymarket |
| chopratejas/headroom | +11,282 | compress tool outputs/logs/RAG chunks before the LLM; 60-95% fewer tokens |
| Leonxlnx/taste-skill | +8,413 | "gives your AI good taste", anti-generic-slop |
| Panniantong/Agent-Reach | +5,186 | "give your agent eyes": read/search Twitter, Reddit, YouTube, GitHub, Bilibili |
| santifer/career-ops | +4,111 | AI job-search system on Claude Code, 14 skill modes |
| phuryn/pm-skills | +4,005 | 100+ PM agentic skills marketplace |
| CopilotKit/CopilotKit | +2,751 | frontend stack for agents, AG-UI protocol |
| aaif-goose/goose | +2,509 | open-source extensible AI agent |

**New repos created in-window (gh search, by stars):** superloglabs/superlog (789 — AI agents that self-heal software via observability), DietrichGebert/ponytail (763 — created TODAY, "agent thinks like the laziest senior dev"), caezium/Burrow (626 — macOS GUI + MCP server), FerroxLabs/wayland (399 — perceive/reason/act agent), duncatzat/vigils (388 — local control plane: see what agents do, approve what matters, keep secrets out).

## What X is saying
**Consensus** (relevance-triaged; engagement shown):
- Skills-as-products is the story of the cycle. "The theme this week: code knowledge graphs and agent skill packs are becoming the new IDE layer" [@sharbel, 86 likes]; AI-Rank daily: agent-skills repos at #1/#2, "open-source AI is shifting from model-call demos to reusable agent systems" [@charlie_26c, 0 likes — bot-grade source, weak signal, but consistent]. Official skill packs from Anthropic/Google/Stripe circulating via VoltAgent/awesome-agent-skills [@tom_doerr, 111 likes]. [observed]
- last30days-skill is framed as a free disruption of paid AI search: "Perplexity charges $240/yr... someone built /last30days and made it free forever. 28,700 GitHub stars" [@cyrilXBT, 198 likes] [claimed — star count not independently verified]. The author's own dogfooding thread (agent autonomously fixed the tool overnight) pulled 46k views [@mvanhorn, 189 likes]. [observed]
- headroom rides the "context is the bottleneck" narrative: "Most people think they need bigger context windows. They actually need fewer tokens" [@JulianGoldieSEO, 12 likes]; feature rundown at [@GithubProjects, 77 likes]. Notably the wave includes obvious marketing-bait accounts — hype is partly manufactured. [observed + inferred]
- taste-skill is spreading by integration: bundled into Open Design's "design skill stack" alongside Hallmark, billed as "the design skills everyone on X is talking about" [@tuturetom, 13 likes; quoting @nexudotio]. [observed]

**Contested / gaps:** No substantive criticism captured at this depth — the anti-takes (does headroom's compression hurt answer quality? are skill marketplaces slop?) didn't surface in 2 shallow queries. superlog: zero X chatter found despite 789 stars in 10 days. Unresolved, not averaged.

**Best takes:**
> "The theme this week: code knowledge graphs and agent skill packs are becoming the new IDE layer." — @sharbel
> "Most AI agents aren't slow because they're dumb. They're slow because they're reading too much." — @JulianGoldieSEO (on headroom)
> "Not what editors curated. Not what algorithms pushed. What real people actually cared about enough to upvote, like, share, or bet money on." — @cyrilXBT (on last30days-skill)

## Freshness & coverage
Window 2026-05-29 → 2026-06-12 fully covered. GitHub: 2 queries (gh search created-in-window; trending-weekly scrape). X: 2 queries (n=10 each), retried once after the documented `-t top`+filters zero-hit quirk, filters applied client-side. Reddit not queried (out of task scope) — reduced coverage. Rejected noise named in manifest, headline rejection: 2,254-like "ponytail" real-estate fiction tweet.

## Next directions
1. Mine replies on @cyrilXBT's last30days tweet and @mvanhorn's thread (`twitter tweet 2063874926273265967 -n 20`) — corrections/skepticism live there.
2. Verify headroom's 60-95% claim against the repo's benchmarks (`gh repo view chopratejas/headroom`) — currently [claimed] only.
3. Reddit pass (r/ClaudeAI, r/LocalLLaMA, `-t week`) for the practitioner counter-narrative X didn't surface.
4. Watch @tom_doerr and @sharbel as recurring high-signal repo curators; `twitter user-posts` weekly.
