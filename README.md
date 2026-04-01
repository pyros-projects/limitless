<p align="center">
  <img src="assets/banner.png" alt="Limitless" width="100%">
</p>

<h1 align="center">Limitless</h1>

<p align="center">
  <strong>A small, sharp marketplace of Claude Code skills that punch above their weight.</strong>
</p>

*A curated collection of Claude Code plugins — from research and content generation to full creative lifecycle management.*

---

## What Is This?

A curated Claude Code plugin marketplace with high-leverage skills designed to unlock capabilities you didn't know you needed. Four plugins covering research, content creation, product intelligence, creative lifecycle management, and persistent agent memory.

**The goal:** Make you (and Claude) limitless.

---

## Plugins

| Plugin | Skills | What It Does |
|--------|--------|--------------|
| [**limitless**](plugins/limitless/) | 4 | Article generation, research, surface-first prototyping, and privacy-respecting web search. |
| [**after-hours**](plugins/after-hours/) | 7 | Calm, high-taste product intelligence: identity, subtraction, naming, coherence, and first-contact honesty. |
| [**pyro-kit**](plugins/pyro-kit/) | 17 | Complete 7-phase creative lifecycle: idea excavation, design exploration, prototyping, contracts, building, momentum tracking, and anti-abandonment composting. |
| [**codies-memory**](plugins/codies-memory/) | 4 | Persistent agent memory with agent-namespaced vaults, promotion pipelines, trust levels, and CLI write commands. Requires `uv sync` setup — see INSTALL.md. |

---

## Installation

### 1. Add the Marketplace

In Claude Code, run:

```
/plugin marketplace add pyros-projects/limitless
```

### 2. Browse & Install

```
/plugin                                    # Browse available plugins
/plugin install limitless@limitless        # Curated Pyro skill pack
/plugin install after-hours@limitless      # Calm, wholesome product-intelligence skills
/plugin install pyro-kit@limitless         # Full creative lifecycle toolkit
/plugin install codies-memory@limitless    # Persistent agent memory (requires uv sync)
```

### 3. Manage

```
/plugin enable limitless@limitless         # Enable
/plugin enable after-hours@limitless       # Enable
/plugin enable pyro-kit@limitless          # Enable
/plugin enable codies-memory@limitless     # Enable
/plugin disable limitless@limitless        # Disable
/plugin disable after-hours@limitless      # Disable
/plugin disable pyro-kit@limitless         # Disable
/plugin disable codies-memory@limitless    # Disable
/plugin uninstall limitless@limitless      # Uninstall
/plugin uninstall after-hours@limitless    # Uninstall
/plugin uninstall pyro-kit@limitless       # Uninstall
/plugin uninstall codies-memory@limitless  # Uninstall
```

---

## Philosophy

> "I don't have delusions of grandeur, I have an accurate assessment of my own abilities."
> — Eddie Morra, *Limitless*

These plugins embody:

- **Depth over breadth** — Keep the pack small, useful, and opinionated
- **Research-first** — Don't just execute, understand first
- **Concrete over ceremonial** — Skills should make the agent stronger in live work
- **Taste and restraint** — Some of the best help is subtraction, naming, coherence, and clarity
- **Delightful surprises** — Dice-rolled podcast hosts, whitepaper-backed SFD, calm late-night product intelligence

---

## Coming Soon

The roadmap includes future skills or plugin branches for:

- **deep-research** — Multi-source synthesis with citation tracking
- **codebase-oracle** — Instant deep understanding of any codebase
- **pitch-deck** — Investor-ready presentations from a business concept
- **data-story** — Charts, visualizations, and narratives from raw data
- **brand-forge** — Brand kits, style guides, design systems

See [docs/brainstorm/plugin-ideas.md](docs/brainstorm/plugin-ideas.md) for the full idea backlog.

---

## License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <em>"What would you do if you could do anything?"</em>
</p>
