# X Playbook — twitter-cli recipes

`twitter` is a uv tool (`uv tool install twitter-cli`). Check
`twitter status` for auth. All commands support `--json`, `-c`
(compact), `-o file`.

## Search anatomy

```bash
twitter search '"<topic>" <variant>' -t top --min-likes 50 --lang en \
  --exclude retweets --since 2026-05-12 -n 30 --json -o x1.json
twitter search '"<topic>"' -t latest --min-likes 10 -n 20 --json -o x2.json
```

- **Quote the topic term** (`'"suno"' prompt`) — unquoted multi-word
  queries drift to adjacent-but-wrong content (live lesson: "suno
  prompt" surfaced a 2k-like GPT-Haskell tweet and generic
  prompting-advice threads).
- Tabs: `-t top` for settled signal, `-t latest` for velocity (trend
  mode), `photos|videos` rarely useful for research.
- `--exclude retweets` always; add `--exclude replies` when noisy.
- `--from <user>` to probe a high-signal author found during recon;
  `--to <user>` for discussions around them.

## The floor ladder (adaptive --min-likes)

| Situation | Floor |
|---|---|
| `top` tab, mainstream topic | start 50 |
| `top` tab, niche topic | start 20 |
| `latest` tab | start 10 |
| <5 hits | halve floor, widen `--since` once; below 5 likes, drop the floor entirely |
| Noisy / engagement-bait heavy | double floor, add `--min-retweets 10`, `--exclude replies` |

State every ladder move in the brief's coverage section.

## Thread mining

```bash
twitter tweet <id> -n 20 --json     # replies: corrections, counterpoints
twitter user-posts <handle> -n 20   # an author who keeps appearing
```

Replies and quote-tweets are X's comment section — a confident claim
with 40 corrective replies is a different datum than the claim alone.

## Known CLI quirks (observed in dojo pressure tests, v0.8.5)

- `twitter search` has **no `-c` flag** (only the global `twitter -c`).
- `-t top` combined with `--min-likes` can return **0 hits server-side**
  even when matching tweets exist. If a floored top-search returns 0 but
  recon showed in-window hits: drop the floor, filter engagement
  client-side from the JSON, and state the adaptation.
- `-o` writes a bare JSON list (stdout wraps in `{ok, data}`); subcommands
  `tweet` and `user-posts` have no `-o` — redirect stdout.
- Reply fetches can include injected timeline-filler tweets — verify each
  "reply" actually references the thread before counting it as evidence.

## Output fields that matter

`id`, `text`, `author.screenName`, `author.verified`, `metrics` (likes,
retweets, replies, quotes, views, bookmarks), `createdAtISO`. Engagement
receipt format: `[@<handle>, <likes> likes]`. Truncated text in table
mode → re-fetch that tweet with `--json` or `--full-text`.

## Engagement ≠ relevance

Likes rank *attention*, not *pertinence*. Triage by relevance first
(read the text), then use engagement to rank among relevant items. Every
sweep should be able to name at least one high-engagement item it threw
away — if it can't, say so explicitly.
