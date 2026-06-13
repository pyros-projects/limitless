# Limitless

**Pyro's curated Claude Code skill pack for research, prototyping, publishing, search, music, and skill craft.**

This plugin folds the strongest living skills in this repo into one coherent package instead of splitting them across historical sub-plugins.

## Skills

| Skill | What It Does | When to Reach For It |
|---|---|---|
| [**article-pack**](skills/article-pack/) | Turns notes, drafts, or fresh research into complete publishable content packs | When you want articles, posts, decks, threads, or a full promo kit |
| [**codies-research**](skills/codies-research/) | Runs source-backed research with direct answers and strong next-step branching | When you need current facts, verification, comparisons, or note updates |
| [**surface-first-development**](skills/surface-first-development/) | Starts software work from the user-visible surface, then derives contracts and builds inward | When an app, CLI, API, workflow, or agent flow should be prototyped before architecture hardens |
| [**searxng**](skills/searxng/) | Provides privacy-respecting web search through a self-hosted SearXNG instance | When the agent needs direct web search without external API keys |
| [**suno-pack**](skills/suno-pack/) | Turns a track idea into a Suno-ready package — concept document, per-version vocal + instrumental prompts (v5.5/v5.0/v4.5 via `--versions`), v4.5→v5.5 cover pipeline, runnable per-prompt scripts, and a concept-derived `experiments.md` lane book for self-serve experimentation — and executes it for real via `suno-pp-cli`: gated rendering with take-aware downloads and immutable run logs, cover pipelines, library checks, and one-roll experiment lanes (`--mode experimental`) | When you want to make music in Suno — author the pack, render the pack, run the cover pipeline, or roll an experiment |
| [**hivemind**](skills/hivemind/) | Disciplined collective-brain search across five venues — X/Reddit (`twitter`/`rdt`), GitHub (`gh`), web (SearXNG), papers (OpenAlex/arXiv) — with ask-driven pivot chains (discover → enrich/react/verify), evidence-graded receipts, living sweep configs (crystallize on demonstration, `repeat <slug>`, propose-confirm), and `--radar` topic reports backed by a Social-Signal-Radar-compatible mini-KG | When the answer lives in threads, repos, and preprints, not articles — "what's the hot shit in X", "trending repos and what is X saying about them", "repeat ai-dev-weekly" |
| [**dojo**](skills/dojo/) | Verified skill authoring in seven kata: held-out scenarios, baseline-fail tests, bounded-edit pressure loops, subagent trigger evals, and a dojo record per skill | When you create or edit a skill and want proof it changes agent behavior — no skill ships on vibes |
| [**james**](skills/james/) | Persistent constrained reviewer for concept docs, PRDs, plans, specs, design docs, and strategy docs; checks self-containedness inside project-owned scope, saves recipes and review chains under `~/.limitless/james`, fixes what can be fixed, then resumes James for re-review until pass or escalation | After writing or editing planning docs, or whenever the user says "invoke James", "run James", or "James this" |

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
- Keep skill-owned runtime output out of project docs by default:
  generated packs, sweep frames, dojo evidence, and scratch artifacts
  live under `~/.limitless/<skill>/`. Write into the target project only
  when the project artifact itself is the requested deliverable, or when
  the user explicitly chooses that path.

## License

MIT
