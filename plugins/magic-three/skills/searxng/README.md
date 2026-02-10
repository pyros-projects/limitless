# SearXNG — Privacy-Respecting Web Search

> **Skill file:** [`SKILL.md`](SKILL.md) — load this into your AI coding agent

## What is SearXNG?

[SearXNG](https://github.com/searxng/searxng) is a self-hosted metasearch engine that aggregates results from 70+ search engines (Google, Bing, DuckDuckGo, etc.) without tracking or profiling. It provides a JSON API that's perfect for AI agent use.

**Core idea:** Give your AI agent web search capability without API keys, rate limits, or privacy concerns.

## Why Use It?

- **No API keys needed** — Self-hosted, no accounts or billing
- **Privacy-respecting** — No tracking, no profiling, no data collection
- **JSON API** — Structured output perfect for AI agents
- **70+ engines** — Aggregates results from Google, Bing, DuckDuckGo, and more
- **Categories** — Filter by general, news, images, videos, tech, science, etc.
- **Self-hosted** — Runs in Docker, fully under your control

## Quick Start

```bash
# Run with Docker (one command)
docker run -d --name searxng --restart always -p 8888:8080 searxng/searxng:latest

# Search (JSON output)
curl -s "http://localhost:8888/search?q=rust+async+tutorial&format=json" \
  | jq '.results[:5]'

# With content snippets
curl -s "http://localhost:8888/search?q=python+fastapi&format=json" \
  | jq -r '.results[:5] | .[] | "## \(.title)\n\(.url)\n\(.content)\n"'
```

## Search Parameters

| Parameter | Values | Example |
|-----------|--------|---------|
| `q` | Search query | `q=rust+async` |
| `format` | `json`, `csv`, `rss` | `format=json` |
| `categories` | `general`, `news`, `it`, `science`, etc. | `categories=it` |
| `language` | `en`, `de`, `fr`, etc. | `language=de` |
| `time_range` | `day`, `week`, `month`, `year` | `time_range=week` |
| `pageno` | Page number | `pageno=2` |

## Use Cases for AI Agents

- **Research** — Gather information before planning a feature
- **Documentation lookup** — Find API docs, tutorials, examples
- **Fact-checking** — Verify claims and find current information
- **Competitive analysis** — Research existing solutions
- **Troubleshooting** — Search for error messages and solutions

## Links

- **Docs:** https://docs.searxng.org/
- **GitHub:** https://github.com/searxng/searxng
- **Public instances:** https://searx.space/ (if you prefer not to self-host)
