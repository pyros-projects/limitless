# Limitless

**Pyro's curated Claude Code skill pack for research, prototyping, publishing, search, music, and skill craft.**

This plugin folds the strongest living skills in this repo into one coherent package instead of splitting them across historical sub-plugins.

## Skills

| Skill | What It Does | When to Reach For It |
|---|---|---|
| [**article-pack**](skills/article-pack/) | Turns notes, drafts, or fresh research into complete publishable content packs | When you want articles, posts, decks, threads, or a full promo kit |
| [**codies-research**](skills/codies-research/) | Runs source-backed research with direct answers and strong next-step branching | When you need current facts, verification, comparisons, or note updates |
| [**surface-first-development**](skills/surface-first-development/) | Starts software work from the user-visible surface, then derives contracts and builds inward | When an app, CLI, API, workflow, or agent flow should be prototyped before architecture hardens |
| [**sfd-v2**](skills/sfd-v2/) | Docket-emitting Surface-First Development: converge any evaluable surface, log clauses at birth, emit contract YAML, self-admit against the Accord, and round-trip the handoff | When surface work needs agent handoff, customer-grade acceptance, or durable contract evidence rather than a lightweight prototype |
| [**searxng**](skills/searxng/) | Provides privacy-respecting web search through a self-hosted SearXNG instance | When the agent needs direct web search without external API keys |
| [**suno-pack**](skills/suno-pack/) | Turns a track idea into a Suno v6 package — concept document, lyric beat-map craft with visible artist/song inspiration audits, v6 vocal + instrumental prompts with v6 settings (Variety, Max Mode, Duration; `--model v6|v6-wild|v6-mini`, optional wild→v6 cover route), moving pre-v6 packs to v6, and a concept-derived `experiments.md` lane book for self-serve experimentation — and renders it for real: `suno` CLI (paperfoot/suno-cli) by default, Claude in Chrome on your own session for captchas and UI-only controls, a paste route for other agents; gated spends, take-aware downloads, immutable run logs, stored-tag checks, covers/remasters, library checks, one-roll experiment lanes (`--mode experimental`), and saga-synced journals | When you want to make music in Suno — author the pack, render it, cover or remaster a take, or roll an experiment |
| [**hivemind**](skills/hivemind/) | Disciplined collective-brain search across five venues — X/Reddit (`twitter`/`rdt`), GitHub (`gh`), web (SearXNG), papers (OpenAlex/arXiv) — with ask-driven pivot chains (discover → enrich/react/verify), evidence-graded receipts, living sweep configs (crystallize on demonstration, `repeat <slug>`, propose-confirm), and `--radar` topic reports backed by a Social-Signal-Radar-compatible mini-KG | When the answer lives in threads, repos, and preprints, not articles — "what's the hot shit in X", "trending repos and what is X saying about them", "repeat ai-dev-weekly" |
| [**dojo**](skills/dojo/) | Verified skill authoring in seven kata: held-out scenarios, baseline-fail tests, bounded-edit pressure loops, subagent trigger evals, and a dojo record per skill | When you create or edit a skill and want proof it changes agent behavior — no skill ships on vibes |
| [**learn-anything**](skills/learn-anything/) | Builds domain-shaped beginner→expert curricula via pedagogy web-recon, emits only Tier 1 through a failable capstone, persists capability state, and reports strengths/blockers; next tiers authored on demand | When you want a sequenced mastery path for any topic (academic, physical, creative, linguistic, professional), a mid-path learning progress report, or the next gated tier after a capstone |
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
