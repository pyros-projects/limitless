# Shared sample dataset for hivemind --radar mockups

All mockups render this exact data so Pyro compares aesthetics, not content.
Mockup data — plausible but fictional.

## Sweep metadata

- query: "AI Agents"
- window: 2026-05-12 → 2026-06-11 (30d)
- platforms: X, Reddit
- volume: 214 posts triaged, 41 deep-read
- generated: 2026-06-11 · hivemind v0.1 · MOCKUP DATA

## Topics

### t1 — Agent Memory Systems
- type: tool · heat: 32 · velocity: rising · connects: t4, t5
- POSITIVE: "Persistent memory is what finally makes agents feel like colleagues instead of goldfish — teams report real continuity wins." — r/ClaudeAI · u/contextkeeper · 890↑
- NEGATIVE: "Most 'agent memory' is RAG with extra steps and a worse failure mode: confidently stale context." — @evalwonk (X) · 1.2k likes
- CONTESTED: graph-based vs plain-file memory; no resolution, both camps ship.
- ENRICHMENT: github.com/letta-ai/letta · arxiv.org/abs/2604.11883 ("Memory Architectures for LLM Agents", May 2026)
- SYNTHESIS: Memory moved from demo feature to procurement checkbox this month. The fight is structure (KG vs files), not value. [inferred]

### t2 — MCP Everywhere
- type: release · heat: 28 · velocity: rising · connects: t3, t6
- POSITIVE: "MCP hitting critical mass — every SaaS now ships a server; integration time collapsed from weeks to an afternoon." — r/mcp · u/portforward · 640↑
- NEGATIVE: "An MCP server for everything means an attack surface for everything. Nobody is auditing these." — @secfault (X) · 980 likes
- CONTESTED: registry quality (spam servers) vs open growth.
- ENRICHMENT: github.com/modelcontextprotocol/servers · MCP spec changelog 2026-05
- SYNTHESIS: MCP is now plumbing, not news. Discourse shifted from "what is it" to "who vets it." [observed]

### t3 — Claude Code Skills Ecosystem
- type: tool · heat: 24 · velocity: rising · connects: t2, t4
- POSITIVE: "Skills turned my CLI into a team of specialists. The marketplace moment is here." — @tooluser (X) · 2.1k likes
- NEGATIVE: "90% of published skills are README wrappers. Discovery is broken without quality signals." — r/ClaudeCode · u/skillskeptic · 410↑
- CONTESTED: open marketplace vs curation.
- ENRICHMENT: github.com/anthropics/claude-code · awesome-claude-skills list
- SYNTHESIS: Skills are the new plugins; the discourse is a marketplace-curation debate with one viral take per week. [observed]

### t4 — Multi-Agent Orchestration
- type: technique · heat: 19 · velocity: steady · connects: t1, t3
- POSITIVE: "Orchestrator + specialist subagents cut our pipeline cost 60% vs one mega-prompt." — r/AI_Agents · u/swarmherd · 530↑
- NEGATIVE: "Every multi-agent demo dies in production. Coordination overhead eats the gains." — @distsys_dan (X) · 760 likes
- CONTESTED: when fan-out beats a single strong model.
- ENRICHMENT: arxiv.org/abs/2605.02991 (orchestration patterns survey)
- SYNTHESIS: Steady drumbeat, not hype spike — practitioners trading patterns, skeptics citing prod failures. Both right at different scales. [inferred]

### t5 — Context Rot
- type: debate · heat: 14 · velocity: rising · connects: t1
- POSITIVE: "Naming it 'context rot' finally gives teams language for why long sessions degrade." — r/LocalLLaMA · u/tokenbudget · 380↑
- NEGATIVE: "It's not rot, it's bad context management. Stop blaming the model for your prompt hygiene." — @ctxwindow (X) · 540 likes
- CONTESTED: model limitation vs operator error.
- ENRICHMENT: arxiv.org/abs/2603.17440 (long-context degradation study)
- SYNTHESIS: Fast-rising vocabulary battle; the term is winning even where the diagnosis is disputed. [observed]

### t6 — Prompt Injection Panic
- type: news · heat: 11 · velocity: steady · connects: t2
- POSITIVE: "Good week for security: three major agent frameworks shipped injection mitigations." — r/netsec · u/escapeseq · 290↑
- NEGATIVE: "Mitigations are theater while agents can still exfiltrate via any tool with network access." — @redteamtea (X) · 1.5k likes
- BACKGROUND (news-type enrichment): triggered by a May 2026 disclosed exploit chain in a popular MCP server.
- ENRICHMENT: disclosure writeup · OWASP LLM Top 10 (2026 update)
- SYNTHESIS: Security discourse is reactive and event-driven; expect a spike with every disclosure. [observed]

### t7 — Local Agents on Small Models
- type: technique · heat: 8 · velocity: cooling · connects: t6
- POSITIVE: "Qwen-flavored 8B models now run useful agent loops fully offline. Privacy people are thrilled." — r/LocalLLaMA · u/airgapped · 310↑
- NEGATIVE: "Local agents remain a hobby. Tool-calling reliability under 30B is still a coin flip." — @gpupoor (X) · 420 likes
- COOLING NOTE: mentions down ~40% vs April.
- ENRICHMENT: github.com/ollama/ollama · r/LocalLLaMA weekly agents thread
- SYNTHESIS: Real but niche; conversation migrated to dedicated communities, mainstream attention cooled. [observed]

## Best takes (for pull quotes / tickers)

1. "Agents don't have a memory problem, they have a forgetting problem — and we keep shipping amnesia as a feature." — @evalwonk
2. "MCP is HTTP for agents now. You don't get a medal for supporting it, you get filed under 'works'." — r/mcp
3. "Your multi-agent system is just one agent with extra latency until proven otherwise." — @distsys_dan

## Footer (all mockups)

"Social media is a weak-evidence surface — stances are sentiment, not validation. · Backed by radar.json (Social-Signal-Radar-compatible)"
