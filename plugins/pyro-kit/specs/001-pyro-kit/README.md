# Specification: 001-pyro-kit

## Status

| Field | Value |
|-------|-------|
| **Created** | 2026-03-12 |
| **Current Phase** | Ready |
| **Last Updated** | 2026-03-12 |

## Documents

| Document | Status | Notes |
|----------|--------|-------|
| product-requirements.md | completed | Full framework PRD — ~25 skills, 7 phases, SFD philosophy, anti-abandonment, fascination index |
| solution-design.md | completed | Plugin architecture, PICS+Workflow skills, hybrid state, 8 ADRs confirmed, 4-skill MVP |
| implementation-plan.md | completed | 7 phases, 20 tasks, 4-skill MVP then 5 expansion waves |

**Status values**: `pending` | `in_progress` | `completed` | `skipped`

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-12 | Framework scope (not just skills) | User wants BMAD/Superpowers scale, not a handful of standalone skills |
| 2026-03-12 | SFD propose-react-iterate pattern for ALL skills | User explicitly hates Socratic questioning; wants agent to propose concrete things, user just reacts |
| 2026-03-12 | Full lifecycle coverage (feeling → shipped) | User wants "yes I like this" to theoretically get from nothing to shipped project |
| 2026-03-12 | Built on Surface-First Development methodology | User's own project — the philosophical foundation for the entire framework |
| 2026-03-12 | All 8 ADRs approved (plugin, PICS+Workflow, hybrid state, SFD composition, skill orchestrator, SessionStart hook, YAML-indexed fascination, 4-skill MVP) | User approved all architecture decisions in SDD review |
| 2026-03-12 | Implementation plan: 7 phases with 4-skill MVP first, 5 expansion waves after | MVP (/spark, /pulse, /pyro, /autopsy) delivers unique value fast; remaining ~21 skills added in waves |

## Context

**Pyro Kit** is a Surface-First Development framework for the full project lifecycle. It applies the propose-react-iterate pattern (from the user's SFD methodology) at every phase — from pre-idea excavation through implementation to shipping or composting.

**Key insight**: The user's preferred interaction model is "agent proposes concrete things, user evaluates and steers." This is SFD's cognitive asymmetry principle applied everywhere: humans evaluate better than they generate. The framework should be usable by someone who only says "yes I like this" or "more like that."

**Prior research**: Extensive research exists in `.internal/research/ideation-research/` (13 pieces covering 40+ tools, thinking frameworks, solo dev tools, and a feasibility study). Key files:
- `12-solo-creative-developer-tools.md` — 30+ tools landscape
- `13-pyro-kit-feasibility.md` — Gap analysis, architecture, psychology of abandonment
- `11-structured-thinking-frameworks.md` — 7 thinking methodologies

**User profile**: Solo creative developer, 20+ GitHub repos, most abandoned at 60-70%. Highly creative but jumps to coding before thinking through. Doesn't care about market research or teams — wants to push ideas to their full potential.

**Related project**: Surface-First Development at `~/projects/agents/surface-first-development/` (whitepaper v0.6, SKILL.md, MIT licensed).

---
*This file is managed by the specify-meta skill.*
