# Shared dataset for Mneme mockups

All three mockups (`01-console`, `02-dossier`, `03-atlas`) render this exact
vault snapshot so the comparison is aesthetic and informational, not content.
Data is plausible and grounded in the real Mneme spec/decisions — but it is
**mockup data**, not a live vault read.

Dogfooding note: the flagship compiled dossier is on **Retrieval Packaging**,
compiled from Mneme's own ADR-001 / decisions-resolved / spec. Mneme eating its
own docs is the point.

---

## Vault

- **vault path:** `~/.mneme/vault`
- **resolved project:** `limitless` (cwd `/home/pyro/projects/private/limitless`)
- **storage:** plain markdown + git · `main` · clean · last commit `7e73851` · no auto-push
- **mneme version:** `0.1.0` (phase 1 — shared substrate)
- **generated:** 2026-06-14 · MOCKUP DATA

### Bindings (host adapters)

| host | status | transport | since | capture mission |
|---|---|---|---|---|
| `codex` | ● bound (primary) | stdio MCP | 2026-05-02 | technical decisions, debugging lessons, project state, user prefs |
| `claude` | ● bound | stdio MCP | 2026-05-02 | session state, reflections, lessons, dreams |

### Retrieval sidecar (managed QMD)

- **process:** `~/.mneme/bin/qmd mcp` (stdio) · ● healthy
- **index freshness:** synced 6 min ago (4 new records pending reindex)
- **collections:** `memory`, `compiled`, `insights`, `captures`, `ops`
- **models:** embed `bge-m3` · rerank `bge-reranker-v2-m3` (phase-1 pick)
- **ranking:** layer-priority merge owned by `mneme ask` (compiled > insights > memory > captures); QMD collections are NOT the product ranking contract

---

## Layers

| layer | home | count | purpose |
|---|---|---|---|
| **Operational** | `memory/` | 2 agents · 1 project · 4 lessons · 1 decision · 2 inbox | continue work across sessions |
| **Compiled** | `compiled/` | 3 topics · 6 editions | current-best readable dossiers |
| **Insights** | `insights/` | 214 claims · 8 in tension | durable atomic claims + graph |
| **Captures** | `captures/` | 31 sources | raw material pre-distill |

### Inbox (operational, awaiting triage)

- `IN-20260614-a1f3` — *stale* (9d) · "single-host lock semantics vs concurrent Codex+Claude writes" · trust: speculative
- `IN-20260613-7c02` — *aging* (2d) · "reranker swap bge-v2-m3 → lighter model before phase-1 freeze" · trust: speculative

### Open tensions

- `TS-0007` — **cross-agent:** Claude treats `confidence` as a display annotation; Codie wants it to nudge retrieval ranking. Unresolved. (Both records written; reconciliation is v2.)

---

## Health (what `mneme status` / `mneme doctor` reports)

- ● vault: clean, inside git, no uncommitted private changes
- ● bindings: 2 hosts, both pointing at this vault
- ● QMD: healthy, index fresh (6 min)
- ● hooks: SessionStart / UserPromptSubmit / Stop wired on both hosts
- ◐ **1 stale dossier** — `compiled/host-binding/2026-04-25.md` cites `memory/projects/limitless/decisions/DC-0003.md` which changed 2 days ago. (Staleness is metadata, not a defect — see *dossiers are publications*.)
- ◐ 2 inbox items aging (no stale)
- ◐ 1 open tension (TS-0007)
- ● publication-graph integrity: 1 current head per series, every `supersedes:` resolves, no cycles

---

## Boot packet (what the agent sees at SessionStart — `limitless` project)

```
=== Identity (boot-exempt, unlimited) ===
self/Claude/identity.md  →  name, model, rules, memory-map

=== Project: limitless ===
active decisions   DC-0001 Boot contract: identity is limitless, budget 12000
active threads     TH-0001 Build our own ideation pipeline as a superpowers skill
                   TH-0002 CE multi-persona review as optional SFD gate
                   TH-0003 Apply cc-ecosystem steal-now patterns to limitless
recent lessons     LS-0004 Engine-pattern lesson: Pyro's billing-bounded window
                   LS-0003 Index-document boot pattern beats inlining
                   LS-0001 Fire close-session on clear session-end signals

=== Recent episodes (delta digest, last 3 sessions) ===
2026-06-13  Hivemind 0.11, wd-briefing v2, name-gated lookup
2026-06-12  Memory architecture consolidated ("clunky Mneme")
2026-06-12  suno-pack 0.8.0→0.10.2: dojo, Pins on Mars

=== Boot budget ===
identity  ∞   project   38%   procedural 51%   episodic  22%   total 41% of 12000
```

---

## Flagship compiled dossier — `retrieval-packaging`

> Rendered in full by `02-dossier`. The other two mockups show it as a card / node.

- **series:** `retrieval-packaging`
- **edition:** 3 · **supersedes:** edition 2 (2026-04-24) · **status:** current head
- **generated_at:** 2026-04-26 · `generated_by:` `mneme compile retrieval-packaging --budget high`
- **vintage note:** pre-dates TS-0007 (confidence-vs-trust); currency confirmed 2026-06-14
- **cites (4):** `adr/ADR-001-retrieval-packaging.md` · `decisions-resolved.md` (retrieval row) · `mneme-product-spec.md` (Retrieval Semantics) · `insights/hybrid-search-with-rrf-...`

### Premise gate (compile opens with this)

> *This compile assumes the question is "how does Mneme package retrieval as part of the product, not as an external dependency." If you're asking "which embedding model is best," that's a different dossier.*

### Answer (current-best understanding)

Mneme ships **QMD as a managed sidecar**, not as a user-installed dependency.
`mneme init` installs `~/.mneme/bin/qmd` and the configured retrieval models;
`mneme bind <host>` writes the host's MCP entry to launch the same managed
`qmd mcp` command over **stdio** (the proven transport). The user never installs
or configures a retrieval service separately.

The critical invariant: **QMD provides candidate retrieval; Mneme owns
product-ranking semantics.** Collection filters are not layer priority. `mneme ask`
merges and ranks with explicit layer weights so `compiled/` can outrank `insights/`,
insights outrank `memory/`, and `captures/` stays a deeper-excavation path. This
prevents "QMD decided what matters" from becoming invisible product logic.

### Support

- ADR-001 records the managed-sidecar decision over three rejected alternatives
  (in-process, optional install, hosted).
- The reference integration (claude-knowledge ↔ QMD) already proves the stdio MCP
  + multi-collection shape Mneme adopts.
- KG evidence: hybrid lex+vec+hyde search with RRF outperforms pure keyword or
  pure semantic for agent memory (LongMemEval convergence).

### Complications

- `mneme doctor` must treat retrieval as a product subsystem: model availability,
  index freshness, transport health, host MCP binding health, fallback behavior
  when vector search is unavailable, and whether layer-priority ranking is applied.
- Index freshness is load-bearing for trust: a QMD miss must not read as "the
  memory doesn't exist" when the index is stale relative to the newest vault file
  (LS-0002 discipline — surface staleness, don't silently serve it).

### Contradictions / open

- **TS-0007** (cross-agent): whether `confidence` stays a display annotation
  (Claude) or nudges retrieval ranking (Codie). This dossier treats it as
  display-only; edition 4 will revisit if TS-0007 resolves toward ranking.

### What this dossier does NOT claim

- It does not claim the reranker model is final (bge-reranker-v2-m3 is the
  phase-1 empirical pick; a lighter alternative is on IN-20260613-7c02).
- It does not claim graph/temporal retrieval arms ship in v1 — those are phase 3,
  consistent with the five-archetypes insight (Mneme deliberately defers the
  temporal/entity graph archetype).

### Provenance / source refs

```
[1] adr/ADR-001-retrieval-packaging.md          (decision record)
[2] decisions-resolved.md :: Retrieval Packaging (managed QMD sidecar)
[3] mneme-product-spec.md :: Retrieval Semantics (layer-priority invariant)
[4] insights/hybrid-search-with-rrf-outperforms... (KG evidence, confidence: confirmed)
```

### Edition history (backwards links only)

- **ed 3** (2026-04-26, current) — added layer-priority invariant + stdio-first transport correction
- **ed 2** (2026-04-24) — superseded by ed 3 · had ranked QMD collections as layer priority (the bug ed 3 fixes)
- **ed 1** (2026-04-23) — superseded by ed 2 · initial "bundle QMD" framing, pre-transport decision

---

## Dossier browser (all compiled topics)

| series | current ed | generated | vintage | cites | status |
|---|---|---|---|---|---|
| `retrieval-packaging` | ed 3 | 2026-04-26 | current | 4 | ● current |
| `host-binding` | ed 2 | 2026-04-25 | **stale** | 3 | ◐ a cited source changed |
| `agent-memory-architecture` | ed 1 | 2026-04-23 | current | 6 | ● current |

---

## Sample `mneme ask` result (rendered by Console)

```
$ mneme ask "how does mneme handle retrieval?"

[compiled] compiled/retrieval-packaging/ed-3.md          trust: canonical · 2026-04-26
  Mneme ships QMD as a managed sidecar; mneme ask owns layer-priority ranking…
  vintage note: pre-dates TS-0007 (confidence-vs-trust) → see Contradictions
[insight]  insights/hybrid-search-with-rrf-outperforms...  confidence: confirmed
  Hybrid lex+vec+hyde + RRF beats pure keyword or semantic for agent memory.
[memory]   memory/projects/limitless/lessons/LS-0003.md   trust: working · 2026-06-10
  Index-document boot pattern beats inlining everything in boot packets.
[capture]  captures/2026-04-26-adr-001-retrieval-packaging.md  raw · pre-distill
  (deeper excavation only)

→ answer grounded in 1 dossier (current) + 1 confirmed insight + 1 working lesson.
→ 4 records, ~612 tokens of 8192 budget · retrieval trace: --trace to see arms
```

---

## Why three paradigms (the tension these mockups exist to test)

The spec's **MVP Non-Goals** say: *"no custom UI … Obsidian can be the human
viewer. Mneme is the agent-operated substrate and CLI/MCP surface."*

Each mockup argues one position on that line:

- **01-console** — agrees with the spec. The CLI is the product; render it well.
- **02-dossier** — finds the must-design surface *inside* the spec: the compiled
  dossier is a published artifact, and publications get designed whether or not
  there's an "app."
- **03-atlas** — disagrees on purpose. What if Mneme shipped its own viewer
  instead of ceding the human surface to Obsidian? What's gained, what's lost.
