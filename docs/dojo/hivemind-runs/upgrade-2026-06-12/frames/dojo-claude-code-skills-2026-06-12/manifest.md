# Manifest — dojo-claude-code-skills / 2026-06-12

**Query:** "what does reddit say about Claude Code skills? quick shallow pass"
**Mode:** knowledge mine, shallow/--quick tier (user asked for quick shallow pass)
**Window:** none enforced (snippet dates observed: Oct 2025 – Mar 2026)
**Platforms requested:** Reddit (explicit). X attempted as substitute coverage only.

## Environment / degradations
- `rdt` CLI NOT installed (environment ground truth, not re-verified). Per skill
  Phase 0: install offered to user in brief (`uv tool install rdt-cli`); NOT
  auto-installed; no scraping workarounds (no raw reddit JSON endpoints, no
  mirrors) used. Reddit coverage degraded to SearXNG snippets — no comment
  deep-read, engagement numbers mostly unavailable.
- `twitter` CLI installed + authenticated (ground truth). Two passes returned
  0 results; X coverage dropped, flagged.
- Recon (Phase 2 unscoped rdt/twitter passes) impossible without rdt; venue
  resolution done by frequency-counting subreddits in SearXNG result URLs.

## Files
- `raw/searxng-reddit-scoped.json` — SearXNG `"Claude Code" skills site:reddit.com`,
  top 10 used. Localhost:8888 instance.
- `raw/x1.json` — `twitter search '"Claude Code" skills' -t top --min-likes 50
  --lang en --exclude retweets -n 10` → 0 hits.
- `raw/x2.json` — adaptation: floor halved to 25, phrase quoting dropped → 0 hits.

## Adaptations (stated)
- X floor 50 → 25 + dropped phrase quoting after <5 hits (skill floor ladder).
  Still 0 → dropped platform, did not exceed shallow budget with further retries.

## Venue frequency count (from result URLs)
r/ClaudeAI ×5, r/ClaudeCode ×3, r/claude ×1, r/vibecoding ×1.

## Triage rejections (named, with reasons)
- r/vibecoding `1pihn0c` "Antigravity + Claude Code + Gemini 3 Pro" — toolchain
  combo post, not about skills → off-topic, rejected.
- `?tl=de` URLs are Reddit machine-translations of English posts — kept the
  underlying posts (distinct IDs), noted translation artifact; snippets in
  German treated as same-content.
- Everything else retained as relevant.

## Claims needing verification
- "/skill load <url>" as the install mechanism (r/ClaudeCode `1s2dacs`,
  translated snippet) — does not match known Claude Code commands; [claimed],
  unverified, flagged in brief.
