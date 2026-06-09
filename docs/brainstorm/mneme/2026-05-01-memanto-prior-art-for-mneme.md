# Memanto Prior-Art Notes For Mneme

*Comparison note - 2026-05-01 - Codie*

Status: implementation guidance, not a product pivot.

This note compares Memanto (`moorcheh-ai/memanto`, checked locally at
`/tmp/memanto-checkout.DzwUGu/memanto`, commit `be4cfc8`) against the current
`codies-memory` kernel and Mneme product plan.

The comparison intentionally assumes Memanto's external Moorcheh dependency is
replaced by QMD. That removes the need for service credentials and makes the
comparison useful for Mneme's local-first direction.

---

## Bottom Line

Memanto is not a replacement for `codies-memory` or Mneme.

It is useful prior art for product ergonomics:

- broad CLI surface
- typed memories
- recall versus answer UX
- temporal retrieval modes
- batch/file ingest
- connector registry
- status and bootstrap dashboards
- daily summaries and conflict workflows

`codies-memory` remains the better operational kernel because its canonical
truth is local markdown, its boot packet semantics are real, its project
resolution is repo-aware, and its trust/promotion pipeline already matches how
Codie works.

The right synthesis is:

> Memanto's approachable product surface, filtered through Codie-memory's
> local truth, gates, boot packets, and promotion spine.

---

## What Memanto Does Better

### Product Surface

Memanto has a broader, more user-facing command model:

- `remember`
- `recall`
- `answer`
- `upload`
- `agent`
- `session`
- `daily-summary`
- `conflicts`
- `schedule`
- `memory export`
- `memory sync`
- `connect`

Mneme should not copy this surface directly for v0.1, but it should notice that
Memanto gives users obvious verbs for the common memory jobs. Mneme's smaller
surface should still feel similarly direct.

### Recall Versus Answer

Memanto separates:

- raw retrieval: `recall`
- synthesized RAG response: `answer`

Mneme can keep a single `mneme ask` command while adopting this distinction as
modes:

```bash
mneme ask "what did we decide about retrieval?"
mneme ask --raw "retrieval packaging qmd sidecar"
mneme ask --answer "what should I do next?"
```

The useful idea is not the exact command names. The useful idea is that agents
often need either raw evidence to work from or a synthesized answer to hand to a
human. Mneme should make that choice explicit.

### Memory Typing

Memanto's memory type set is practical:

- `instruction`
- `fact`
- `decision`
- `goal`
- `commitment`
- `preference`
- `relationship`
- `context`
- `event`
- `learning`
- `observation`
- `artifact`
- `error`

`codies-memory` currently uses fewer durable record types:

- `inbox`
- `thread`
- `lesson`
- `decision`
- `session`
- `reflection`
- `dream`
- `skill`
- `playbook`

Mneme should not explode top-level directories for every Memanto type. Better:
add a `subtype` or `kind` field where it helps retrieval and presentation.

Recommended mapping:

| Memanto type | Mneme home |
|---|---|
| `instruction` | `self/<agent>/rules.md`, `memory/procedural/`, or `memory/projects/*/decisions/` |
| `fact` | `memory/projects/*/threads/` or `compiled/` after consolidation |
| `decision` | `memory/projects/*/decisions/` |
| `goal` | `memory/projects/*/threads/` or `ops/` |
| `commitment` | `ops/` or project session summaries |
| `preference` | `memory/identity/user.md` |
| `relationship` | `memory/identity/` or `compiled/topics/` |
| `context` | session summaries and boot artifacts |
| `event` | session summaries or timeline-tagged memory |
| `learning` | `lessons/` |
| `observation` | `inbox/` or `threads/` |
| `artifact` | `captures/` or `compiled/` with source refs |
| `error` | `lessons/`, `ops/observations/`, or project threads |

### Metadata Shape

Memanto's record metadata has good field ideas:

- confidence
- provenance
- actor/source
- source reference
- tags
- validation count
- supersession links
- contradiction flag
- TTL or expiry
- created and updated timestamps

Mneme should borrow the metadata vocabulary, but keep it file-first and
operator-readable. Do not turn confidence into a magic number that bypasses the
promotion pipeline. Confidence is an annotation; trust level is a governance
state.

### Temporal Queries

Memanto's temporal query modes are worth borrowing:

- `--as-of`: what did we believe at this time?
- `--changed-since`: what changed after this time?
- `--current-only`: ignore superseded, expired, and archived records

Mneme can implement these over markdown frontmatter plus QMD candidate
retrieval. This is especially valuable for agent work because many memory
questions are really time questions:

- what changed since the last session?
- what was true before this migration?
- what is the current instruction, not the historical one?

### Connector Registry

Memanto's agent connector registry is the strongest borrow for `mneme bind`.
It models host-specific instruction files, skill directories, global versus
project install paths, hooks, and permissions in one table.

Mneme should implement a similar registry for:

- Codex
- Claude Code
- Cursor
- OpenCode
- Gemini CLI
- Goose
- other hosts later

For v0.1, Codex comes first, Claude second. The registry should be ready for
more hosts without making the first bind path generic soup.

### Batch And File Ingest

Memanto supports batch memory ingestion and file upload. Mneme should borrow the
capability, not necessarily the exact behavior:

- `mneme capture --batch <jsonl-or-json>`
- `mneme capture --file <path>`
- optional `--type` / `--subtype`
- provenance stored in frontmatter
- QMD reindex triggered after write

This should write raw material into `captures/` first unless the content is
already clearly an operational record.

### Dashboards

Memanto's `status` and `agent bootstrap` surfaces point at a product gap:
memory systems need a quick "what is going on here?" view.

Mneme should eventually make `mneme status` show:

- vault path
- active host bindings
- QMD health
- index freshness
- inbox aging/stale counts
- compiled dossier staleness
- recent sessions
- unresolved conflicts or drift

This is already compatible with ADR-001.

---

## What Codie-Memory Already Does Better

### Local Truth

`codies-memory` treats markdown files as the canonical record and indexes as
accelerators. That remains non-negotiable for Mneme. A memory system for agents
must be inspectable when the retrieval layer is stale, broken, or unavailable.

### Boot Packets

Memanto has recall and export, but `codies-memory` has actual boot assembly:
identity, procedural memory, project context, working memory, and recent
episodes are loaded with budgets.

Mneme should keep this as a core advantage. "Boot better" is not just a search
query; it is a curated startup artifact.

### Project Resolution

`codies-memory` resolves project memory through:

1. marker file
2. project registry
3. git remote

That is a better fit for coding agents than an agent-only namespace. Mneme
should preserve repo-aware project memory as a first-class concept.

### Promotion And Write Gates

Memanto has confidence/provenance metadata, but `codies-memory` has governance:

- inbox records start speculative
- gates decide visibility
- promotion paths refine raw observations into threads, lessons, and decisions
- trust moves through working, confirmed, canonical

Mneme should not trade this for "store everything with confidence 0.8."
Memory hoarding is how continuity becomes noise.

### Operational Skills

`codies-memory` treats memory skills as part of memory itself. This matters
because the system stores not only facts, but behavior: how an agent should boot,
capture, promote, refresh, and close a session.

---

## What Not To Borrow

Do not borrow:

- cloud or service dependency as the source of truth
- agent-only namespace as the primary structure
- mandatory proactive storage of every important-looking thing
- confidence scores as a replacement for promotion
- destructive conflict resolution that deletes records without preserving a
  clear audit trail
- a large v0 command surface
- a product shape that requires a local REST server for normal agent use

Mneme can expose REST or UI surfaces later, but v0.1 should stay CLI/MCP first.

---

## Borrowing Plan

### Phase 1

Borrow only what strengthens the existing v0.1 loop:

1. Add metadata fields where cheap:
   - `subtype`
   - `confidence`
   - `provenance`
   - `actor_id`
   - `source_ref`
   - `tags`
2. Keep `mneme ask`, but design it with raw/evidence versus synthesized-answer
   modes.
3. Build `mneme bind` around a host registry, starting with Codex.
4. Add `mneme status` output that feels like a dashboard, not just a boolean
   health check.
5. Add `mneme capture --file` only if it writes into `captures/` and records
   provenance cleanly.

### Phase 2

Borrow broader workflows:

1. temporal query flags for `ask`
2. batch ingest
3. conflict report generation
4. daily or session intelligence summaries
5. richer `bootstrap` / startup snapshots

### Phase 3

Borrow product polish:

1. optional local UI
2. scheduled maintenance
3. cross-host connector expansion
4. guided conflict resolution
5. API surface for programmatic integrations

---

## Product Boundary Update

Memanto strengthens the existing Mneme direction rather than replacing it.

The useful product lesson is:

> A memory system should feel easy at the surface, but disciplined underneath.

For Mneme that means:

- Memanto-like verbs where they clarify user intent
- QMD-managed retrieval where it gives strong recall
- `codies-memory`-style local files, boot packets, project resolution, and
  promotion as the load-bearing core

