# Manifest — dojo-github-repo-mentions / 2026-06-12-2 (same-day re-sweep)

## Query
Which GitHub repos are getting the most mentions on r/LocalLLaMA and r/ClaudeAI lately.

## Mode / window / chain
- Mode: trend scan ("lately")
- Window: top `-t month` + one `new` pass per venue
- Chain: **reddit (discover) → gh (enrich)** — stated before fan-out
- Platform: Reddit + GitHub. Venues named by the user; twitter authenticated but unused (scoping, not degradation).
- gh active account: pyros-projects

## Operator constraints (dojo run)
Shallow: 1–2 queries per venue, `-n 10`, no deep fan-out, no deep-reads. Slug prefixed `dojo-`.

## Same-day re-sweep note
`dojo-github-repo-mentions/2026-06-12` exists with a complete brief (identical query). Frame contract → this frame carries the `-2` suffix. Diff against the morning frame: discover-stage entities are **identical** at the repeated-mention level (llama.cpp 3, smallcode 2, minebench 2; same high-engagement singles, scores drifted ±10 — fetch-time snapshots). Material new content this run: the **gh enrich stage the morning frame skipped** (8 entities, one batched GraphQL call) + a partially rotated `new`-sort slate on r/ClaudeAI.

## Adaptations
- Phase 2 venue recon skipped: venues user-named AND budget capped.
- No global control pass (budget).
- No deep-reads: comment-level repo mentions NOT counted; titles/urls/selftext only.
- Enrichment batched into a single GraphQL query with aliases to keep gh at 1 query.

## Queries run (5 total, in order)
```
rdt search "github.com" -r LocalLLaMA -s top -t month -n 10 --json -o raw/r1-localllama-top-month.json
rdt search "github"     -r LocalLLaMA -s new          -n 10 --json -o raw/r2-localllama-new.json
rdt search "github.com" -r ClaudeAI   -s top -t month -n 10 --json -o raw/r3-claudeai-top-month.json
rdt search "github"     -r ClaudeAI   -s new          -n 10 --json -o raw/r4-claudeai-new.json
gh api graphql (one batched query, 8 repo aliases)    -> raw/gh-enrich.json
```

## Pivot entity list (discover → enrich)
ggml-org/llama.cpp (3 posts) · doorman11991/smallcode (2) · ammaar-alam/minebench (2) ·
ikawrakow/ik_llama.cpp · levy-street/world-of-claudecraft · huawei-csl/kvarn ·
cactus-compute/needle · open-gsd/get-shit-done-redux

## Collision / qualification register
- `open-gsd/get-shit-done-redux` → GitHub redirect to **open-gsd/gsd-core** (repo renamed). Treated as same entity; rename corroborates the migration post `[observed]`.
- `cactus-compute/needle` vs `cactus-compute/cactus`: same post mentions both; enriched `needle` (the announced artifact).
- `smallcode`: one of its 2 posts is the fork-stealing drama post — counted but caveated.

## Triage rejections (named, with reasons)
- `paddlepaddle/p` — truncated URL artifact in selftext.
- `am17an/228edfb84ed082aa88e3865d6fa27090` — gist hash, not a repo.
- `lagunaswift/rockyvoice.git` — trailing `.git` artifact; single low-signal mention, not enriched.
- `mattpocock/skills`, `lnilluv/pi-ralph-loop` — appear only in a 0-upvote "is a 3090 enough" thread; off-topic for mention-trend counting.
- 7/40 posts had no parseable repo link, incl. the two 1.2k↑ npm supply-chain-attack posts (no repo URL in post body).

## Files
- raw/r1..r4 — 10 posts each (raw Reddit listing shape)
- raw/parse_repos.py — shape-tolerant throwaway parser (reused from morning frame)
- raw/gh-enrich.json — batched GraphQL enrichment (8 repos)
- brief.md — final synthesis
