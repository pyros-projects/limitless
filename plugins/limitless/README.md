# Limitless

**Pyro's curated Claude Code skill pack for research, prototyping, publishing, and search.**

This plugin folds the strongest living skills in this repo into one coherent package instead of splitting them across historical sub-plugins.

## Skills

| Skill | What It Does | When to Reach For It |
|---|---|---|
| [**article-pack**](skills/article-pack/) | Turns notes, drafts, or fresh research into complete publishable content packs | When you want articles, posts, decks, threads, or a full promo kit |
| [**codies-research**](skills/codies-research/) | Runs source-backed research with direct answers and strong next-step branching | When you need current facts, verification, comparisons, or note updates |
| [**surface-first-development**](skills/surface-first-development/) | Starts software work from the user-visible surface, then derives contracts and builds inward | When an app, CLI, API, workflow, or agent flow should be prototyped before architecture hardens |
| [**searxng**](skills/searxng/) | Provides privacy-respecting web search through a self-hosted SearXNG instance | When the agent needs direct web search without external API keys |

## Installation

### Via the Limitless marketplace

```bash
/plugin marketplace add pyros-projects/limitless
/plugin install limitless@limitless
```

### Manual

Copy the skill folders you want into your local Claude Code skills area, or point your agent tooling at the specific `SKILL.md` files.

## Philosophy

- Keep the pack small and high-leverage
- Prefer living skills over historical bundles
- Ship skills that make the agent materially more capable, not just more ceremonial
- Let each skill stay opinionated and sharp

## License

MIT
