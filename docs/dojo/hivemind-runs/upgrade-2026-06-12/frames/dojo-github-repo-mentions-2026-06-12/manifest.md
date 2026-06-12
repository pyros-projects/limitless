# Manifest — dojo-github-repo-mentions / 2026-06-12

## Query
Which GitHub repos are getting the most mentions on r/LocalLLaMA and r/ClaudeAI lately.

## Mode / window / platform
- Mode: trend scan ("lately")
- Window: top `-t month` + one `new` pass per venue (≈ 30 days + bleeding edge)
- Platform: Reddit only — venues named by the user; twitter CLI authenticated but unused (scoping decision, not a degradation)

## Operator constraints (dojo run)
Shallow pass mandated: max 1–2 queries per venue, `-n 10`, no deep fan-out, no deep-reads. Frame slug prefixed `dojo-` per operator instruction.

## Adaptations
- **Phase 2 recon skipped**: venues user-specified AND query budget capped at 2/venue. Recon queries would have consumed the entire budget.
- **No global control pass**: same budget reason.
- **No deep-reads (`rdt read`)**: shallow constraint; comment-level repo mentions are therefore NOT counted — post titles/urls/selftext only.
- Near-match frame check: `dojo-ai-agent-repos-trending/2026-06-12` exists but is an incomplete frame (one GitHub-API raw file, no manifest) answering a different question (GitHub-side trending, not Reddit mention counts). Kept distinct slug.

## Queries run (4 total, in order)
```
rdt search "github.com" -r LocalLLaMA -s top -t month -n 10 --json -o raw/r1-localllama-top-month.json
rdt search "github"     -r LocalLLaMA -s new          -n 10 --json -o raw/r2-localllama-new.json
rdt search "github.com" -r ClaudeAI   -s top -t month -n 10 --json -o raw/r3-claudeai-top-month.json
rdt search "github"     -r ClaudeAI   -s new          -n 10 --json -o raw/r4-claudeai-new.json
```

## Files
- raw/r1-localllama-top-month.json … raw/r4-claudeai-new.json — 10 posts each (raw Reddit listing shape)
- raw/parse_repos.py — throwaway shape-tolerant parser (regex `github\.com/owner/repo` over url+selftext+title, per-post dedup, owner blocklist for non-repo paths)

## Triage rejections / artifacts (named)
- `paddlepaddle/p` — regex artifact: selftext truncated mid-URL in PP-OCRv6 post; real repo almost certainly PaddlePaddle/PaddleOCR. Excluded from rankings.
- `am17an/228edfb…` — gist.github.com link, not a repo. Excluded.
- `doorman11991/smallcode` count caveat: 1 of its 2 mentions is the "Beware!! Users trying to fork and steal your projects" drama post (also sole source of `noobezlol/lightagent`) — controversy mention, not adoption signal.
- `mattpocock/skills`, `lnilluv/pi-ralph-loop` — from a 0-upvote question post; weakest signal in set.
- 7 posts had no parseable repo link (listed in parser output), incl. two high-engagement r/ClaudeAI supply-chain-attack posts (1292↑, 1195↑) that discuss npm/Claude Code malware without linking a specific repo.

## Known limits
40 posts total from 4 shallow queries; counts of 2–3 are snapshot-level, not robust statistics. Comment sections unmined. Searching the literal term "github" biases toward posts that link repos in the body, against discussion-only mentions.
