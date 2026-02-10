---
name: searxng
description: Search the web using SearXNG, a self-hosted, privacy-respecting metasearch engine. Aggregates 70+ search engines with no tracking. Use as your primary search tool.
homepage: https://docs.searxng.org/
read_when:
  - You need to search the web for information.
  - You want privacy-respecting search without API keys.
  - You need structured JSON search results for programmatic use.
metadata:
  openclaw:
    emoji: "🔍"
---

# SearXNG — Privacy-Respecting Web Search

SearXNG is a self-hosted metasearch engine that aggregates results from 70+ search engines (Google, Bing, DuckDuckGo, etc.) without tracking or profiling. It provides a JSON API perfect for AI agent use.

## Installation

### Docker (recommended)

```bash
docker run -d \
  --name searxng \
  --restart always \
  -p 8888:8080 \
  searxng/searxng:latest
```

This runs SearXNG on `http://localhost:8888`. The `--restart always` flag ensures it starts on boot.

### Docker Compose (alternative)

```yaml
# docker-compose.yml
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8888:8080"
    restart: always
```

```bash
docker compose up -d
```

### Enable JSON Output

By default, SearXNG may not have JSON format enabled. To enable it:

```bash
# Find the settings file inside the container
docker exec searxng cat /etc/searxng/settings.yml | grep -A5 formats

# If json is not listed, override settings:
docker cp searxng:/etc/searxng/settings.yml ./settings.yml
# Edit settings.yml: under 'search:', add 'formats: [html, json, csv, rss]'
docker cp ./settings.yml searxng:/etc/searxng/settings.yml
docker restart searxng
```

### Verify

```bash
curl -s "http://localhost:8888/search?q=test&format=json" | head -c 200
```

You should see JSON output with search results.

## Quick Search

```bash
# Basic search — top 5 results as JSON
curl -s "http://localhost:8888/search?q=YOUR+QUERY&format=json" | jq '.results[:5]'

# Titles and URLs only
curl -s "http://localhost:8888/search?q=YOUR+QUERY&format=json" \
  | jq -r '.results[:5] | .[] | "\(.title)\n\(.url)\n---"'

# With content snippets (best for AI agents)
curl -s "http://localhost:8888/search?q=YOUR+QUERY&format=json" \
  | jq -r '.results[:5] | .[] | "## \(.title)\n\(.url)\n\(.content)\n"'
```

### URL Encoding

Encode spaces as `+` or `%20` in query strings:

```bash
# These are equivalent
curl -s "http://localhost:8888/search?q=rust+async+tutorial&format=json"
curl -s "http://localhost:8888/search?q=rust%20async%20tutorial&format=json"
```

## Search Categories

Target specific content types with `&categories=`:

| Category | Use For |
|----------|---------|
| `general` | Default web search |
| `images` | Image search |
| `videos` | Video search |
| `news` | Recent news |
| `music` | Music/audio |
| `files` | File downloads |
| `it` | Tech/programming |
| `science` | Academic/scientific |
| `social+media` | Social platforms |

```bash
# Search only tech/programming sources
curl -s "http://localhost:8888/search?q=rust+async&format=json&categories=it" | jq '.results[:5]'

# Recent news only
curl -s "http://localhost:8888/search?q=openai&format=json&categories=news" | jq '.results[:5]'
```

## Advanced Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `format` | `json`, `csv`, `rss`, `html` | Output format |
| `language` | `en`, `de`, `fr`, etc. | Result language |
| `time_range` | `day`, `week`, `month`, `year` | Recency filter |
| `safesearch` | `0`, `1`, `2` | Safe search level |
| `pageno` | `1`, `2`, ... | Page number |

```bash
# German results from the past week
curl -s "http://localhost:8888/search?q=ki+nachrichten&format=json&language=de&time_range=week"

# Page 2 of results
curl -s "http://localhost:8888/search?q=python+tutorial&format=json&pageno=2"
```

## Troubleshooting

```bash
# Check if running
docker ps | grep searxng

# View logs
docker logs --tail 50 searxng

# Restart
docker restart searxng

# Full restart (remove + recreate)
docker rm -f searxng
docker run -d --name searxng --restart always -p 8888:8080 searxng/searxng:latest
```

### Common Issues

- **"Connection refused"** — Container isn't running. Check `docker ps` and start it.
- **"format not available"** — JSON output isn't enabled in settings. See installation section.
- **Slow results** — SearXNG queries multiple engines. First query after restart is slower.

## Configuration

SearXNG is highly configurable via `/etc/searxng/settings.yml` inside the container. Key settings:

- **Engines** — Enable/disable specific search engines
- **Formats** — Which output formats are available
- **UI** — Language, theme, default settings
- **Rate limiting** — Protect against abuse

See [SearXNG documentation](https://docs.searxng.org/admin/settings.html) for full reference.

## Links

- **Docs:** <https://docs.searxng.org/>
- **GitHub:** <https://github.com/searxng/searxng>
- **Public Instances:** <https://searx.space/> (if you don't want to self-host)
