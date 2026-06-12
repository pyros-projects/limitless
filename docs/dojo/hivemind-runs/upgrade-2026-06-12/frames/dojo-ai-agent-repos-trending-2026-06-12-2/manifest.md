# Manifest — dojo-ai-agent-repos-trending / 2026-06-12-2

- query: "Trending GitHub repos in the AI agent space, last two weeks, and what X is saying about them"
- mode: trend scan (shallow — operator constraint: ≤2 queries/source, n ≤ 10)
- window: 2026-05-29 → 2026-06-12 (14d)
- chain: gh (discover) → x (react)
- venues: gh (account: pyros-projects), x (@PyrosAI). Reddit/web/papers not in chain.
- config: none applied. `ai-dev-weekly` config inspected but covers a different
  intent (weekly meeting prep); live ask won. Slug reused from existing
  `dojo-ai-agent-repos-trending`; `-2` suffix = same-day re-sweep.

## Files (raw/)

- gh-new-aiagent.json — `gh search repos --created=">2026-05-29" --sort=stars --limit 10 -- "AI agent"`
- gh-topic-aiagents.json — `gh search repos --topic=ai-agents --created=">2026-05-29" --sort=stars --limit 10`
- x-orgs.json — `twitter search '"superloglabs" OR "agent0ai" OR "FerroxLabs" OR "DietrichGebert"' -t latest -n 10`
- x-repos.json — `twitter search '"superlog" OR ("ponytail" AI) OR ("dox" "AGENTS.md") OR ("wayland" "AI agent")' -t top -n 10`

## Pivot entity list (discover → react)

1. DietrichGebert/ponytail — 766★, created 2026-06-12 (<1 day) — ~766★/day
2. superloglabs/superlog — 790★, created 2026-06-02 — ~79★/day
3. agent0ai/dox — 662★, created 2026-06-01 — ~60★/day
4. FerroxLabs/wayland — 399★, created 2026-06-05 — ~57★/day
5. (borderline, not pivoted) caezium/Burrow — 626★ — disk-cleaner GUI w/ MCP, tangential

## Collision register

- "agent0ai" → @Agent0ai on X is BOTH the Agent Zero project account AND the
  hub of an A0 crypto prompt-injection-challenge community. Q1 latest-tab hits
  were all challenge/proxy chatter, none named the dox repo → all rejected.
  Qualified in Q2 as `("dox" "AGENTS.md")`, which found the org's own announcement.
- "wayland" → collides with Linux display protocol. Qualified as `("wayland" "AI agent")`;
  still pulled a Claude-Desktop-Linux news roundup mentioning protocol-Wayland (rejected).
  Zero genuine hits for FerroxLabs/wayland.
- "ponytail" → generic word (hair). Qualified as `("ponytail" AI)`; 2 off-topic hits
  still leaked and were rejected at triage.

## Adaptations

- Shallow operator constraint: skipped social venue recon (no reddit in chain;
  X stage is entity-scoped); skipped per-entity `gh repo view` enrich — gh search
  inline fields (stars/created/description) used as enrich data instead.
- X Q1 floors: none (`-t latest`, brand-new niche repos — floor would zero it).
- X Q2: `-t top`, no server-side filters (playbook quirk: top + filters can 0 out);
  triage client-side.
- Skipped deep-read of @liweiyi88 superlog thread (budget exhausted) — left as
  next direction.

## Triage rejections (named)

- ProxyShard/ShardBrowser (gh, 362★) — anti-detect scraping browser, not AI-agent space.
- caezium/Burrow (gh, 626★) — macOS disk cleaner with MCP server; tangential, not pivoted.
- All 10 x-orgs.json hits — @Agent0ai crypto-challenge/Fable-5-proxy chatter; none
  reference the agent0ai/dox repo (collision, see register).
- @Alina_with_Ai (x, 4 likes) — AI image prompt mentioning "ponytail hairstyle"; off-topic.
- @lumedeir0s (x) — Portuguese fan tweet, "ponytail" in username only; off-topic.
- @qcmars (x) — AI news roundup; "Wayland" = display protocol (collision); off-topic.
