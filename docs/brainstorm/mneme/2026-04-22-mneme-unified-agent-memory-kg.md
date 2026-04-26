# Nous — Unified Agent Memory + Global KG

*Brainstorm · 2026-04-22 · Claude (Opus 4.7, 1M context)*

> Status: supporting vision note. The canonical product direction is now
> `2026-04-23-nous-product-spec.md`; use that document when this note disagrees
> on MVP order, vault shape, or product boundary.

Working name: **nous** (Greek: intellect; short; owned). Alternatives: `cortex`, `compound`, `lexos`.

---

## One-line pitch

Your agent's working memory + shared thinking space. Two speeds in one system: operational (fast lane) and knowledge (slow compounding). Multi-agent native. Retrieval-first. Artifact-producing.

Not a notes app. Not a wiki. Not "Obsidian with AI." A cognitive substrate that *agents operate* and humans query/steer.

## Why this, why now

Three pieces in Pyro's ecosystem are already doing 80% of this work, separately:

- **codies-memory** (`plugins/codies-memory`) — operational memory with layers (identity / procedural / project / episodic / relational), trust pipeline, write gates, boot packets. Strong on fast-lane ops.
- **arscontexta** (third party, `agenticnotetaking/arscontexta`) — derivation engine that scaffolds knowledge systems from conversation. Strong on the methodology layer (15 kernel primitives, atomic claims, maps, self-maintenance).
- **QMD** — hybrid lex+vec+hyde retrieval as an MCP server across all corpora. Strong on the retrieval layer.

Karpathy's recent LLM-Knowledge-Bases tweet (2026-04-22) validates the shape: raw → compile → query → enhance → repeat. The mockup "LexiBase" dresses this as a product.

Two problems with the current state:

1. **Glue-tape.** We wire codies-memory + arscontexta + QMD ourselves. A user installing "one memory system" doesn't exist.
2. **Over-scaffolded.** arscontexta ships 10 skills, 6K lines, a 1,713-line setup, 608K of reference docs read before setup starts. The 80% path (atomic Zettelkasten + hybrid retrieval + operational memory) should take 60 seconds, not 20 minutes.

Nous is what you get when you redesign with both pieces of evidence in hand: the three things we actually use, unified; the ceremony we don't need, cut.

---

## Core architectural commitments

**1. One repo, two speeds — not two systems.**
Operational memory and global KG share a vault, layered by directory. Promotion is the bridge. Not "codies-memory plugin + KG plugin," one system with two layers.

**2. Storage = plain markdown + git.**
Git is history. Files are forever. Anything else (DB, cloud sync, proprietary format) is lock-in masquerading as features.

**3. Multi-agent native from line one.**
Not retrofitted. Each agent gets `self/<name>/`; `memory/` and `insights/` are shared pools. Tensions auto-track claim conflicts between agents. The trust pipeline (speculative → working → confirmed → canonical) is the resolution mechanism.

**4. Retrieval is installed, not optional.**
Hybrid lex+vec+hyde shipped with the plugin. The agent has an MCP tool from day one. Skipping RAG works until you hit ~500 notes. We're already past that.

**5. Agent-native, not human-first.**
The agent is the primary user. Every command is optimized for "agent runs this fluently during work" first, "human invokes it" second.

**6. Fast path by default.**
`/setup --preset=hybrid-agent` produces a working vault in 60 seconds with three seed insights. Conversational derivation is optional and capped at 5 questions.

---

## Directory shape

```
vault/
├── CLAUDE.md              # derived or preset; agent instructions
├── README.md              # human-readable equivalent
├── .nous/                 # plugin state
│   ├── config.yaml
│   ├── derivation.md      # enables /reseed and /architect
│   └── skills/            # installed per-vault
├── self/
│   └── <agent>/           # identity.md, rules.md, goals.md, reminders.md
├── memory/                # OPERATIONAL (fast lane)
│   ├── agents/<name>/     # per-agent sessions, reflections, dreams
│   ├── projects/<name>/   # project-scoped sessions, inbox, decisions
│   ├── procedural/
│   │   └── lessons/       # LS-G#### global lessons
│   ├── identity/user.md   # shared user knowledge
│   └── inbox/             # global inbox (cross-project)
├── insights/              # GLOBAL KG (slow compounding)
│   ├── *.md               # atomic claims with connections
│   └── *-map.md           # MOCs
├── captures/              # raw sources pre-distill
├── sketches/              # rough project ideas
├── specs/                 # KG-grounded specs (post-/specify)
├── archive/               # processed sources
└── ops/                   # SYSTEM SELF-KNOWLEDGE
    ├── observations/
    ├── tensions/
    ├── reconsider-log.md
    └── methodology/
```

Key design move: `memory/` and `insights/` are distinct directories but the same vault. Promotion moves records up (operational lesson → KG insight). QMD indexes everything together with per-collection scoping.

---

## Skill surface — 11, not 30

### Input (4)
- `/capture` — fast drop to inbox, zero ceremony
- `/seed` — register source for processing pipeline
- `/distill` — inbox/captures → atomic insights
- `/specify` — sketch → KG-grounded project spec

### Compounding (4)
- `/connect` — backward pass across claims
- `/deepen` — update old claims with new evidence
- `/synthesize` — novel claims via trisociation/bridge/counterfactual/distant combination
- `/harvest` — operational → global promotion (lessons from sessions/inbox/decisions)

### Meta (3)
- `/reconsider` — challenge assumptions against accumulated observations + tensions
- `/verify` — quality gate (schema + link + description)
- `/reseed` — regenerate from derivation.md when structural drift accumulates

**What's deliberately missing:**
- `/help` → that's the README
- `/tutorial` → that's a working example vault
- `/ask` → that's `/graph` + retrieval
- `/architect` + `/recommend` split → one skill, two confidence modes
- `/upgrade` → `/reseed --incremental`

**Output skills live in a separate optional pack** (`/article-pack`, `/infinite-loop`, `/slide-deck`). Keeps core lean. The KG pays off in artifacts, not browsing.

---

## Multi-agent semantics

- **Shared memory pool.** Sessions tagged with agent ID. Claude and Codie see each other's sessions by default; per-agent filter available.
- **Per-agent identity.** Each has their own goals, rules, reflections, dreams at `self/<name>/`. The agent reads only its own on boot.
- **Claim provenance.** Every insight carries `origin: <agent>` in frontmatter. Multi-agent claims get a promotion signal (independent validation).
- **Tension auto-detection.** When agent A writes a claim that contradicts a claim by agent B, a tension opens automatically in `ops/tensions/`. Humans or either agent resolve.
- **Handoff protocol.** Session close writes a summary + boundary marker. Next session (same or different agent) runs a delta digest over memory records newer than the boundary. Lightweight 3-7 bullet orientation before work starts.

---

## Retrieval layer

Hybrid lex+vec+hyde (QMD pattern) bundled with the plugin. Not recommended — installed.

Collections:
- `insights` — global KG
- `memory` — operational (all subdirs)
- `self-<agent>` — per-agent identity + reflections (filtered on boot)
- `captures` — raw pre-distill sources
- `ops` — observations, tensions, methodology

First sub-query gets 2× weight. Position-aware RRF fusion. MCP server exposes `search`, `get`, `multi_get`, `status`.

---

## Derivation — optional, not mandatory

Three presets cover 80% of users:

| Preset | For | Default vocab | Active features |
|---|---|---|---|
| `atomic-research` | researchers, academic work | notes/insights | atomic, wiki-links, maps, heavy processing |
| `project-ops` | developers, project-centric | projects/lessons | operational focus, lighter KG |
| `hybrid-agent` | agent-operated, both speeds | insights + memory | full stack (the default) |

**Fast path:** `/setup --preset=hybrid-agent --domain="AI agent research"` → working vault in 60 seconds with three seed insights. Three questions max, only if ambiguity remains.

**Slow path:** conversational derivation for niche domains. Five questions max, not "2-4 turns but actually 20 minutes." Derivation runs on the agent itself when the agent is the user (self-vaults — this is the novel move from the arscontexta critique).

---

## Hook layer (thin, four hooks)

1. **Session start** → boot identity + surface delta digest + check condition triggers (captures/, orphans, tensions, aging inbox)
2. **Write to `insights/`** → validate schema (canonical enums, title-as-claim, description quality, at least one link or topic)
3. **Session close** → write session summary + commit + push
4. **Periodic (opt-in cron)** → `/harvest --since N --dry-run` notification

---

## What I'd explicitly NOT build

- **No custom UI.** Obsidian is the IDE (wiki-links native). Vault-graph as HTML artifact for sharing.
- **No cloud/sync.** Git is sync. GitHub is backup.
- **No auth/permissions.** Local files.
- **No templates-you-configure.** Presets (validated combinations) or derivation, nothing else.
- **No `/tutorial` skill.** A working example vault teaches faster.
- **No prose ceremony in setup.** No ASCII banners, no "I'm about to create your cognitive architecture." Let the first 3 insights be the welcome.
- **No finetuning in core.** Infrastructure is there (every atomic claim is a training pair), but the loop ships as `nous-anneal` module post-MVP.

---

## Differentiation

| vs | What's different |
|---|---|
| **arscontexta** | Same derivation paradigm, half the surface. Retrieval + operational memory as defaults not add-ons. Multi-agent native. `hybrid-agent` preset as the third built-in. |
| **LexiBase mockup / Karpathy wiki** | We don't chase the UI — UI is commodity. Methodology + agent-native design + multi-agent semantics are the moat. |
| **plain Obsidian + AI plugin** | Obsidian is storage + view. Nous is *agent-operated* with self-maintenance loops, quality gates, compounding pipelines. Obsidian can still be the viewer. |
| **codies-memory (standalone)** | Adds the KG layer (atomic claims, connections, maps, synthesis), retrieval, derivation. Codies-memory *is* nous's operational layer. |

---

## Relationship to existing code

Nous is not written from scratch. It's a reorganization + extension of what exists:

- **Core memory layer** ← `plugins/codies-memory/` (Python package: boot, inbox, profile, promotion, records, schemas, vault + 5 skills). Keeps 80%, refactors ~20%.
- **KG layer** ← `projects/agents/claude-knowledge/` (insights, maps, captures, specs, sketches, ops/). Lift the directory model, the 11-skill surface, the methodology docs.
- **Retrieval layer** ← QMD (already an MCP server; already indexes across collections). Bundle it.
- **Derivation layer** ← arscontexta's kernel.yaml + generators, radically simplified. Keep the 15 kernel primitives and three-space separation. Drop the ceremonial onboarding.

See `plugins/codies-memory/docs/brainstorms/2026-04-22-codies-memory-to-nous-transformation.md` for the specific transformation plan.

---

## MVP feature cut (provisional)

**v0.1 (minimum shipping surface):**
- Directory scaffold, presets (3), `/setup --preset`, `/capture`, `/distill`, `/connect`
- QMD bundled
- One agent identity pool (multi-agent hooks present but not exercised)
- Session start/close hooks

**v0.2 (compounding):**
- `/deepen`, `/synthesize`, `/verify`, `/specify`
- Trust pipeline enforced (write gates)
- Condition triggers
- Derivation (conversational mode, 5 questions max)

**v0.3 (maintenance + multi-agent):**
- `/reconsider`, `/harvest`, `/reseed`
- Multi-agent identity pools, auto-tensions on claim conflict
- Cross-agent handoff protocol

**v0.4 (output pack):**
- `/article-pack`, `/infinite-loop`, `/slide-deck` as separate plugin

**v0.5+ (advanced):**
- `nous-anneal` (synthetic-data → small reader finetune)
- Graph synthesis modes (bridge-node, distant-pair)
- Web clipper integration

---

## Open questions

- **Name.** `nous` is short and owned-feeling but has a philosophy-nerd connotation. Alternatives: `cortex`, `compound`, `lexos`, `recall`, `threads`.
- **Plugin boundaries.** One monolith vs `nous-core` + `nous-derivation` + `nous-output` as separate installable plugins?
- **Backward compat with codies-memory.** Import existing `~/.memory/<agent>/` vaults? Symlink compatibility during transition?
- **arscontexta relationship.** Friendly fork? Rewrite? PR upstream the improvements? Depends on maintainer's openness.
- **Finetuning module.** When does `nous-anneal` make sense — 500 insights? 1000? Never, if retrieval stays ahead?

---

## The test of the idea

Karpathy's closing line from the tweet: *"I think there is room here for an incredible new product instead of a hacky collection of scripts."*

The test isn't whether we can build it. We already have 80%. The test is whether the methodology layer (atomic claims, discovery-first design, compounding pipelines, trust pipeline, multi-agent handoff) can stay the moat while we commodify the rest.

If yes: `nous` is a legitimate product.
If no: it's the `~/.memory/Claude/` pattern we already run, renamed. Which is still valuable, just not a product.

My bet: it's legitimate. The methodology IS the moat. Everything else in this space is racing toward Notion-with-AI.
