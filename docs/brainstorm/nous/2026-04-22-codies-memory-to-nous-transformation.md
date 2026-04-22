# codies-memory → nous: transformation plan

*Brainstorm · 2026-04-22 · Claude (Opus 4.7, 1M context)*

Companion to `limitless/docs/brainstorm/2026-04-22-nous-unified-agent-memory-kg.md` (vision). This doc answers the question: **if nous is the target, what does codies-memory become?**

TL;DR: **codies-memory is the operational layer of nous.** Most of it is kept, some is extended, a few new modules are added. The refactor is not "rewrite from scratch" — it's "keep 80%, extend 20%."

---

## What codies-memory is today

Counted 2026-04-22:

- **2,938 lines of Python** across 9 modules
- **620 lines of skill markdown** across 5 skills
- **10 record types** (identity, inbox, session, thread, decision, lesson, reflection, dream, skill, playbook, project)
- **5-level trust pipeline** (speculative → working → confirmed → canonical, plus historical)
- **Write gates** (profile bias, probation, contradiction check)
- **Boot packet** with token budget + layer prioritization + cache
- **Per-agent + per-project vaults** at `~/.memory/<agent>/` and `~/.memory/<agent>/projects/<slug>/`

This is real infrastructure. Boot cache, schema validation, contradiction detection, two-scope promotion — none of this is throwaway.

### Current module map

| Module | Lines | Role |
|---|---:|---|
| `cli.py` | 687 | 11 subcommand handlers (init, validate, boot, capture, create, list, status, promote, user, feedback) |
| `vault.py` | 367 | init global/project, resolve, validate layout |
| `promotion.py` | 310 | evaluate_for_promotion, promote_within_project, promote_to_global, elevate_trust, set_probation, check_contradictions |
| `records.py` | 253 | create/read/list records across record types |
| `schemas.py` | 252 | 10 record types, trust levels, scopes, validation, ID generation |
| `boot.py` | 230 | assemble_boot, layer budgets, truncate_to_budget, cache |
| `inbox.py` | 152 | capture, pending_review |
| `profile.py` | 64 | load_profile, write gate bias |

### Current skill map

| Skill | Lines | Role |
|---|---:|---|
| `memory-help` | 230 | human-facing doc dump |
| `memory-boot` | 161 | boot routine wrapper |
| `memory-capture` | 89 | capture wrapper |
| `memory-close-session` | 72 | session close routine |
| `memory-promote` | 68 | promotion wrapper |

---

## What nous adds on top

Four new things codies-memory doesn't have:

1. **Global KG layer** — `insights/` directory with atomic claims + connections + maps. Records become nodes; the graph is the knowledge. Codies-memory lessons are procedural; insights are propositional + linked.
2. **Pipeline skills** — `/distill`, `/connect`, `/deepen`, `/synthesize`, `/harvest`, `/reconsider`, `/verify`, `/specify`, `/reseed`. Codies-memory has capture+promote; nous has the full compounding loop.
3. **Hybrid retrieval** — lex+vec+hyde as MCP server, bundled (QMD pattern). Codies-memory has no retrieval beyond filename globs.
4. **Derivation** — preset-first with optional conversational mode. Codies-memory's vault is schema-fixed; nous's is derived per-domain/per-agent.

Plus one architectural shift:

5. **Multi-agent native.** Codies-memory has per-agent vaults (`~/.memory/<agent>/`). Nous has a **shared vault** with `self/<agent>/` per-agent identity + `memory/agents/<name>/` per-agent operational. Both agents see each other's work by default; conflict opens a tension automatically.

---

## Keep / extend / add / remove — the module map

### KEEP (reuse as-is or near-as-is)

| Module | Why | Changes |
|---|---|---|
| `schemas.py` | Trust levels, scopes, validation, ID generation — all still correct | Add `insight` record type with `description`, `category`, `confidence`, `topics`, `connections` fields |
| `vault.py` | Vault init pattern, resolution logic | Extend scaffold with `insights/`, `captures/`, `sketches/`, `specs/`, `archive/`, `ops/`, `self/<agent>/` |
| `records.py` | Record CRUD is generic and works for any type | Add link validation when type=insight (check wiki-link targets exist) |
| `profile.py` | Write gate bias logic is domain-agnostic | — |

### EXTEND (existing module, new responsibilities)

| Module | Current | Extension |
|---|---|---|
| `boot.py` | Assembles global + project packets with token budgets | **Add delta-digest layer:** find memory records newer than last session summary, list them for the agent. This is the routine we codified in claude-knowledge/CLAUDE.md today — bake it into boot. |
| `promotion.py` | Project → global lesson promotion + contradiction check | **Add lesson → insight promotion:** when a lesson is referenced from 2+ projects or reaches `confirmed` trust, offer KG enrichment (add description, category, connections). Make contradiction check write to `ops/tensions/` when conflicting claims exist. |
| `inbox.py` | Capture + pending review | **Add `/seed` path:** tracked capture that registers with processing queue (dupe check, archive folder, task queue update). |
| `cli.py` | 11 subcommands | **Add pipeline subcommands:** `search`, `graph`, potentially `distill`/`connect` as scripted operations (or keep skill-invoked). Add `import` for migrating legacy `~/.memory/<agent>/` vaults. |

### ADD (new modules)

| Module | Responsibility |
|---|---|
| `retrieval.py` | QMD-style hybrid lex+vec+hyde. Wrap existing QMD if we can bundle it; otherwise port the core (BM25 + embeddings + reranking). Exposes `search(query_doc, collections=...)`. |
| `derivation.py` | Preset loader (3 presets: atomic-research, project-ops, hybrid-agent). Optional conversational mode capped at 5 questions. Writes `derivation.md` for `/reseed`. |
| `graph.py` | KG operations: orphan detection, map membership, link health, synthesis candidates (bridge-node, distant-pair). |
| `generators.py` | Output artifacts when the output pack is installed (article-pack, slide-deck, infinite-loop SPA). Lives here OR in separate `nous-output` plugin — TBD by plugin-boundary decision. |
| `agents.py` | Multi-agent semantics: resolve agent from context, per-agent identity load, auto-tension on claim conflict. |

### REMOVE

| What | Why |
|---|---|
| `memory-help` skill | Replaced by README. Skills-as-help is an anti-pattern (rotates, duplicates docs, adds surface). |
| `feedback` subcommand | Fine to keep as a mechanism, but frame it as bug report not "feedback" — current implementation is a text dump. |
| Per-agent independent vaults (`~/.memory/<agent>/`) | Replace with shared vault + per-agent identity. Old vaults imported via `import` subcommand. |

### RENAME / CONSOLIDATE SKILLS

| Old (codies-memory) | New (nous) | Change |
|---|---|---|
| `memory-boot` | `/wake-up` (or just `boot` via CLI) | Extend with delta digest; drop the "memory-" prefix since nous is one system |
| `memory-capture` | `/capture` | Fast-lane drop, zero ceremony |
| `memory-close-session` | `/close-session` | Same logic, maybe add auto-commit hook |
| `memory-promote` | `/promote` | Add lesson → insight path |
| `memory-help` | — | Delete. Link README from CLAUDE.md. |

Plus the 11 nous skills from the vision doc:
- Input: `/capture`, `/seed`, `/distill`, `/specify`
- Compounding: `/connect`, `/deepen`, `/synthesize`, `/harvest`
- Meta: `/reconsider`, `/verify`, `/reseed`

Some of these already exist in `claude-knowledge/.claude/skills/` (distill, connect, deepen, synthesize, harvest, reconsider, verify, specify, reseed). Port those verbatim; they're already battle-tested.

---

## Directory layout delta

### Codies-memory today

```
~/.memory/<agent>/
├── identity/
├── procedural/
│   ├── lessons/
│   └── skills/
├── projects/<slug>/
│   ├── identity/
│   ├── inbox/
│   ├── sessions/
│   ├── threads/
│   ├── decisions/
│   └── lessons/ (legacy)
├── reflections/
├── dreams/
├── threads/
├── decisions/
├── boot/
├── inbox/
└── registry/
```

### Nous shared vault

```
<vault>/
├── .nous/
│   ├── config.yaml
│   ├── derivation.md
│   └── skills/
├── self/<agent>/
│   ├── identity.md
│   ├── rules.md
│   ├── goals.md
│   └── reminders.md
├── memory/
│   ├── agents/<name>/
│   │   ├── sessions/
│   │   ├── reflections/
│   │   └── dreams/
│   ├── projects/<slug>/
│   │   ├── inbox/
│   │   ├── sessions/
│   │   ├── threads/
│   │   └── decisions/
│   ├── procedural/lessons/
│   ├── identity/user.md
│   └── inbox/
├── insights/           # NEW — global KG
│   ├── *.md
│   └── *-map.md
├── captures/           # NEW — raw sources pre-distill
├── sketches/           # NEW — rough project ideas
├── specs/              # NEW — KG-grounded specs
├── archive/            # NEW — processed sources
└── ops/                # NEW — system self-knowledge
    ├── observations/
    ├── tensions/
    ├── reconsider-log.md
    └── methodology/
```

Three changes to internalize:

1. `~/.memory/<agent>/` → **shared vault at a project-agnostic path** (e.g., `~/.nous/` or user-chosen). Per-agent content moves under `self/<agent>/` and `memory/agents/<name>/`.
2. `identity/` (agent-level) splits into `self/<agent>/` (per-agent) and `memory/identity/user.md` (shared user knowledge).
3. Everything downstream of `captures/` is net-new: the KG pipeline + synthesis + meta-maintenance.

---

## Migration path

### For existing codies-memory users

New CLI subcommand: `nous import --from codies-memory --agent <name>`

Steps:
1. Read `~/.memory/<agent>/` layout.
2. Move `identity/` → `self/<agent>/` (files `self.md`, `rules.md`, `user.md` → preserved).
3. Move `procedural/lessons/` → `memory/procedural/lessons/` (already matches; just path shift).
4. Move `projects/<slug>/` → `memory/projects/<slug>/` (add agent tag to sessions).
5. Move `reflections/`, `dreams/` → `memory/agents/<name>/reflections/`, `memory/agents/<name>/dreams/`.
6. Leave `insights/` empty (new layer; populate via `/distill`).
7. Create seed `derivation.md` from detected preset — probably `hybrid-agent` for existing codies-memory users.
8. Write symlinks from old paths so existing skills don't break during transition.

### For our current setup

We already ran this informally on 2026-04-15 (codies-memory merged into claude-knowledge). The layout at `/home/pyro/projects/agents/claude-knowledge/memory/` is already ~70% nous-shaped:

- `memory/identity/user.md` ✓
- `memory/procedural/lessons/LS-G####` ✓
- `memory/projects/<slug>/` ✓
- `memory/inbox/` ✓
- `memory/registry/` ✓ (should move to `.nous/config.yaml`)

Missing nous pieces that the merge didn't install:
- `self/<agent>/` (we have `self/` but not per-agent split)
- `memory/agents/<name>/` (we'd need to add if Codie joins the same vault)
- `.nous/derivation.md` (we have `ops/derivation.md` — rename/move)

So the claude-knowledge repo is literally a nous prototype without the `.nous/` frontmatter. Refactoring is maybe 2-3 hours for the structure, plus whatever the new modules take.

---

## What this buys us

1. **codies-memory doesn't die.** Its best parts (trust pipeline, write gates, boot packet, schema validation) are the operational core of nous. Users who install nous get all of codies-memory included.
2. **KG + operational in one system.** No more "install codies-memory, then arscontexta, then wire up QMD." One plugin.
3. **Multi-agent natively.** Claude + Codie in one shared vault with per-agent identity. The thing we've been doing manually for weeks becomes the default.
4. **The 11-skill surface.** Not 30 skills across 3 plugins. Not 10 ceremonial arscontexta skills. Eleven opinionated, composable verbs.
5. **Derivation without ceremony.** 60-second fast path with presets; 5-question optional derivation for niche domains; agent-on-itself derivation for self-vaults.

---

## What's risky about this path

1. **Scope creep.** Nous is larger than codies-memory. Risk of 6-month project instead of 6-week.
   *Mitigation:* ship v0.1 with only codies-memory + KG directory scaffold + QMD bundled. Defer pipeline skills to v0.2, maintenance to v0.3.

2. **arscontexta overlap.** Some users may already have arscontexta vaults.
   *Mitigation:* `nous import --from arscontexta` subcommand. Share the derivation methodology idea; diverge on implementation simplicity.

3. **Name churn.** "Nous" is working. If we rename late, migration compounds.
   *Mitigation:* pick the name early. My vote: `nous` or `compound`.

4. **Multi-agent semantics are underspecified.** Shared vault sounds great; conflict resolution is harder than stated.
   *Mitigation:* v0.1 ships single-agent with multi-agent hooks present but unexercised. v0.3 is when we actually pressure-test Claude+Codie sharing the same vault.

5. **Backward compat promises.** If we guarantee `~/.memory/<agent>/` still works, we carry that weight forever.
   *Mitigation:* import is one-shot, not continuous compat. Old paths deprecated after v0.2.

---

## Concrete next action

If this plan survives a second read:

1. Register `nous` as a limitless plugin directory at `plugins/nous/`.
2. Copy codies-memory's Python package as the starting core (`plugins/nous/src/nous/`).
3. Add `insights/` + `captures/` + `ops/` scaffolding to `vault.py::init_global_vault`.
4. Bundle QMD (or port the hybrid retrieval primitive) as `retrieval.py`.
5. Port the 9 pipeline skills from `claude-knowledge/.claude/skills/` into `plugins/nous/skills/`.
6. Write `derivation.py` with 3 presets, no conversational mode yet.
7. Write `import.py` to migrate claude-knowledge's existing layout in one shot, as the validation test.

That's v0.1. Probably 2-3 solid sessions of work, most of it copy-paste-and-rename, because the hard code already exists in three separate places.
