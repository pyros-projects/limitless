# Reddit Playbook — rdt recipes

`rdt` is a uv tool (`uv tool install rdt-cli`). Auth: `rdt login`
(browser-cookie extraction); check `rdt status`. All search commands
support `--json`, `-c` (compact), `-o file`.

## Venue resolution (the procedure)

```bash
rdt search "<topic>" -s relevance -n 25 --json -c -o "$FRAME/raw/r-recon.json"
python3 -c "import json,collections,os;d=json.load(open(os.environ['FRAME'] + '/raw/r-recon.json'));print(collections.Counter(p['subreddit'] for p in d['data']).most_common(8))"
```

Top 2–4 recurring subreddits = your venues. Sanity-check surprises:
`rdt sub-info <name>` (subscribers, description).

**Cautionary example (live, 2026-06-11):** global
`rdt search "suno prompt" -s top -t year` returned 7.5k-upvote
r/CuratedTumblr and r/antiai posts — viral noise, zero Suno content. The
same intent scoped — `rdt search "prompt structure" -r SunoAI -s top -t
year` — returned the Meta Tags guide and producer threads. Global
top-sort is a virality contest; venues are where the knowledge is.

Recon thin (<8 usable results)? Reformulate with a synonym once, then
ask searxng `best subreddit for <topic>` if still thin.

## Scoped search patterns

```bash
# Knowledge mine
rdt search "<variant>" -r <sub> -s top -t year -n 25 --json -o "$FRAME/raw/rK.json"
rdt search "<variant>" -r <sub> -s comments -t year -n 15 --json -o "$FRAME/raw/r-comments.json"

# Trend scan
rdt search "<variant>" -r <sub> -s top -t month -n 25 --json -o "$FRAME/raw/rT.json"
rdt search "<variant>" -r <sub> -s new -n 15 --json -o "$FRAME/raw/r-new.json"

# Global control (one per sweep, for cross-venue echo detection)
rdt search "<topic>" -s top -t <window> -n 15 --json -o "$FRAME/raw/r-global.json"
```

Pagination: `--after <cursor>` when a promising query maxes out. Bulk:
`rdt export "<query>" --format json -o "$FRAME/raw/r-export.json" -n 100`.

## Comment mining (where the answer lives)

```bash
rdt read <post_id> -s top -n 30 --json > "$FRAME/raw/r-read-<post_id>-top.json"
rdt read <post_id> -s controversial -n 10 --json > "$FRAME/raw/r-read-<post_id>-controversial.json"
```

`--expand-more` to unfold collapsed threads. The post is usually the
question; score the *comments* for receipts. Note `score` and author per
quote you keep. Max 3 kept items per author across the whole sweep.

## Known CLI quirks (observed in dojo pressure tests, v0.4.1)

- The **raw Reddit listing shape** (`data.data.children[].data`) appears
  in `-o` files AND on stdout for subreddit-scoped searches and `rdt
  read` (the compact `{ok, data}` shape is only reliable for unscoped
  compact searches) — always parse shape-tolerantly.
- rdt may append a `▸ More:` pagination hint line after the JSON —
  parse with `json.JSONDecoder().raw_decode` or strip trailing lines.
- `rdt read` has no `-o` — redirect stdout.
- Unquoted multi-word global searches drift to r/all virality; quote the
  phrase (`"agent memory"`) for the recon pass.

## Output fields that matter

`id` (for `rdt read`), `subreddit`, `score`, `num_comments`,
`created_utc`, `permalink`, `selftext`. Engagement receipt format:
`[r/<sub>, <score>↑]`.
