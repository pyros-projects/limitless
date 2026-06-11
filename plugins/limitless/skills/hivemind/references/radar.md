# Radar Mode — Topic Report with a KG Backend

`--radar "<topic>"` (alias `--report`) turns a trend-scan sweep into two
artifacts. **The KG is the primary output; the HTML is a view over it.**

1. `radar.json` — a small, Social-Signal-Radar-compatible evidence graph
   of the sweep (frozen frame).
2. `radar.html` — self-contained visualization rendered FROM the JSON
   using the fanzine template (`assets/radar-template.html`).

## Pipeline (after Phases 0–4 in trend-scan mode, ≥ default depth)

5. **Topic clustering** — group triaged findings into 5–9 topics. Phase 4
   cross-platform clusters are seed candidates. Rank by heat = mentions ×
   cross-platform echo × velocity.
6. **Stance mining** — per topic, sort deep-read material into
   positive / negative / contested camps; pick the strongest
   representative opinion per camp with receipts (platform, author,
   engagement, timestamp). Stance is sentiment, never a truth claim.
7. **Enrichment — HARD BUDGET: 1–3 lookups per topic.** Classify the
   topic type, fetch accordingly:
   - tool/library/release → GitHub repo (`gh search repos`, searxng)
   - research-flavored → arXiv/paper link
   - news/event → 2–3 sentence background with source
   - technique/practice → canonical guide or docs
   The budget is a design rule, not a suggestion — enrichment is where
   radar runs balloon.
8. **Emit & render** — write `radar.json` first, then render
   `radar.html` from it. Open the HTML path for the user at the end.

## radar.json schema

```json
{
  "radar": { "query": "...", "window": "30d", "generated_at": "...",
             "platforms": ["x", "reddit"] },
  "topics": [{
    "id": "t1",
    "label": "...",
    "type": "tool | technique | news | debate | release",
    "heat": { "mentions": 14, "cross_platform": true,
              "velocity": "rising | steady | cooling" },
    "stances": {
      "positive": [{ "claim": "...", "source": {
        "platform": "reddit", "url": "...", "author": "...",
        "engagement": 446, "observed_at": "..." } }],
      "negative": ["…same shape…"],
      "contested": ["…same shape…"]
    },
    "evidence": ["…every receipt that survived triage, same source shape…"],
    "enrichment": [{ "kind": "github | arxiv | background | guide",
                     "url": "...", "note": "..." }]
  }]
}
```

Compatibility rules (inherited from the Social Signal Radar sketch):
every claim carries provenance + `observed_at` (decay-ready); stances
encode sentiment and engagement, never validation; **pull, not push** — a
future Radar imports this file under its own admission contract.

## Sweep series — directory contract

Default root `~/.hivemind` (Linux/macOS; `%USERPROFILE%\.hivemind` on
Windows). Override: `HIVEMIND_DIR` env var.

```
~/.hivemind/<topic-slug>/
  2026-06-11/radar.json + radar.html
  2026-06-28/radar.json + radar.html
  index.html                      ← regenerated each sweep (back catalog)
```

- Deterministic slug ("AI Agents" → `ai-agents`); check for near-match
  dirs before creating (`ai-agent` vs `ai-agents` must not fork). Same-day
  re-sweep → `-2` suffix, never overwrite.
- **Frames are immutable.** Links go backwards only (issue №3 links №2,
  №1). Relative links (`../2026-05-28/radar.html`) — they work from disk.
- `index.html` is the only mutable file: a back-issues cover listing all
  sweeps with headline topics.
- **Cross-frame features happen at generation time, not view time.** If a
  previous frame exists, read its radar.json and bake real deltas into
  the new frame: heat changes (▲ +12), NEW / BACK AGAIN / GONE stickers,
  stance flips. The browser never fetches across files (file:// CORS).

## Using the template

`assets/radar-template.html` is the fanzine: graph-paper discourse MAP
view (heat-sized boxes, elbow connectors, HOT/COOLING stickers) +
data-sheet REPORT view ("THE HYPE / THE BEEF" stance face-offs,
caution-tape contested strips, rubber-stamp epistemic tags), marquee
ticker for best takes, torn-tape view toggle.

Render by replacing the embedded data (topics, stances, receipts,
ticker quotes, sweep metadata) while keeping the structure, both views,
the node-click → report-sheet jump, and the visual language intact. Keep
it a single self-contained file — inline CSS, no external JS, fonts via
Google Fonts link. The fixed template is deliberate: sweeps must be
comparable at a glance.
