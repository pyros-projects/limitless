# Web Playbook — SearXNG as a hivemind venue

Evidence grade: **varies** — articles and docs are secondary sources;
official docs and primary announcements rank above blog echo. Grade
per result, not per venue.

## Preflight

```bash
curl -s -m 5 "http://localhost:8888/search?q=test&format=json" -o /dev/null -w "%{http_code}"
```

- **000 / connection refused** → instance down. The 10-second fix
  (offer it FIRST): `docker start searxng` — or if no container
  exists: `docker run -d --name searxng --restart always -p 8888:8080
  searxng/searxng:latest` (then the 403 fix below).
- **403** → JSON format disabled (default after fresh container or
  image upgrade — the setting lives inside the container and dies with
  it). Fix: copy `/etc/searxng/settings.yml` out, add `- json` under
  `search: formats:`, copy back, `docker restart searxng`.
- SearXNG down does NOT degrade gh/papers — those use direct APIs.

## Recipes

```bash
# General — top 5 with snippets (best agent shape)
curl -s "http://localhost:8888/search?q=<query>&format=json" | jq -r '.results[:5][] | "## \(.title)\n\(.url)\n\(.content)\n"'

# Recency
curl -s "http://localhost:8888/search?q=<query>&format=json&time_range=week&categories=news"

# Tech scoping
curl -s "http://localhost:8888/search?q=<query>&format=json&categories=it"
```

Encode spaces as `+`. Narrow queries beat broad; two precise queries
beat one vague one. 5–10 results per query is the signal ceiling.

## Categories worth knowing

- `news` — recency-sorted, good for the verify stage on current events
- `it` — tech/programming sources
- `science` — academic aggregator (arxiv, google scholar, pubmed,
  semantic scholar, openaire). Breadth tier for the papers venue;
  structured triage still goes through OpenAlex/arXiv directly
  (papers-playbook).
- `social media` — **fediverse-only** (lemmy posts/comments, mastodon
  users/hashtags; tested 2026-06-12). Useful breadth for FOSS/dev
  topics; NEVER a substitute for the x/reddit venues. SearXNG has no X
  engine at all, and its reddit engine 403s (Reddit blocks anonymous
  JSON; engine left disabled). `rdt` and `twitter` remain the only
  real social tools.

## The proxy rule

`site:reddit.com` (or any site-scoped web search standing in for a
dead venue CLI) is a **proxy, not the venue**. It is only used after
the fix offer was declined, and its results are labeled
`proxy-of-reddit` (snippet-level, no comments, no engagement data) —
never presented as "what reddit says".

## Triage

Domain authority + recency. Dedup by canonical URL (strip trackers).
Blog echo of a primary announcement is one story, not N — cluster and
cite the primary.
