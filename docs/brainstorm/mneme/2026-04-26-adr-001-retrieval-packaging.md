# ADR-001: Retrieval Packaging

*Architecture Decision Record - 2026-04-26 - Claude*

Status: **proposed** — awaits Pyro sign-off before phase 1 implementation

---

## Context

Mneme (working name) is a local-first memory and knowledge substrate for AI agents. The canonical product spec (`2026-04-23-mneme-product-spec.md`) bundles retrieval into the product experience — `mneme ask` is part of the MVP command surface alongside `init`, `bind`, `capture`, `compile`, `status`, `doctor`. The user must not need to install or operate a separate retrieval system.

The retrieval requirement, distilled from the spec:

- query the four conceptual layers (`compiled/`, `memory/`, `insights/`, `captures/`) plus `ops/`
- combine multiple search strategies (BM25 keyword, semantic vector, hypothetical document)
- preserve source layer, trust, recency, provenance, and host/agent origin in results
- prefer compiled dossiers when available, then insights, then memory, then raw captures
- be diagnosable from `mneme doctor`
- survive offline (gracefully degrade when models or indices are unavailable)
- accept new content with low-latency reindexing on capture/edit

The reference implementation already exists. **claude-knowledge integrates QMD as the retrieval backend** for a 1,584-document multi-collection corpus (`insights`, `claudes-codies-memory`, `codies-codies-memory`, `basic-memory`). The integration ships via QMD's MCP server, exposing `mcp__qmd__query`, `mcp__qmd__get`, `mcp__qmd__multi_get`, and `mcp__qmd__status`. This is empirically the closest existing instance of what mneme needs.

This ADR decides how mneme packages retrieval given that QMD already exists and is the obvious candidate.

---

## Decision Drivers

1. **One-install UX.** The user installs mneme, not mneme-and-also-QMD-and-also-models.
2. **Avoid reinventing the wheel.** QMD's lex/vec/hyde combination, RRF blending, multi-collection scoping, and intent-disambiguation are non-trivial and already work.
3. **Lifecycle clarity.** Retrieval should start when needed, stop when mneme stops, and not require user-managed processes.
4. **Source-of-truth invariant.** The vault is the truth; the index is derivable. If the index is lost, retrieval degrades but the vault still works.
5. **MCP-binding compatibility.** When `mneme bind <host>` runs, the host (Claude Code, Codex, future) gets MCP tools that work without separate MCP configuration.
6. **Future flexibility.** The packaging choice should allow swapping retrieval implementations later without breaking the user-facing surface.
7. **Defensible install footprint.** Retrieval requires embedding models (~90MB+ for `all-MiniLM-L6-v2`, more for rerankers). The packaging must handle these without making installation hostile.

---

## Considered Options

### Option 1: QMD as External Dependency (Wrapper)

Mneme documents that QMD is required, the user installs both, mneme calls QMD's MCP server.

**Pros:**
- Zero retrieval code in mneme.
- Full QMD capability.
- QMD evolves independently.

**Cons:**
- Two installs. Violates one-install UX requirement.
- User manages MCP lifecycle (port, restart on crash).
- Version-skew risk if mneme expects QMD features that the installed version doesn't have.
- `mneme doctor` cannot fully diagnose retrieval because QMD is outside its process tree.

**Verdict:** fails decision driver #1 (one-install UX). Not viable for v1.

### Option 2: Embedded QMD (Vendored Library)

Mneme bundles QMD as a vendored dependency, calls QMD's library API directly in-process.

**Pros:**
- True one-install.
- Tightest integration: function calls, no IPC, no MCP indirection inside mneme itself.
- Easy to diagnose because everything is in one process.

**Cons:**
- Mneme package size grows by QMD's dependency tree (Python ecosystem: torch, transformers, FAISS or similar).
- QMD must support being run as a library (not just an MCP server). Not currently the primary distribution shape.
- License/distribution alignment required.
- Vendoring couples release cadences. QMD bug fixes require a mneme release.
- The MCP-binding requirement still has to be solved separately — mneme needs to expose MCP tools to host harnesses, so even with embedded QMD, an MCP layer must exist somewhere.

**Verdict:** plausible but heavy. Not the right v1 choice given that the MCP layer has to exist anyway.

### Option 3: Sidecar (Managed Subprocess)

Mneme installs QMD as a managed subprocess that mneme starts and stops. The QMD MCP server runs on a known socket/port; mneme configures host bindings to point at it.

**Pros:**
- One-install UX from the user's perspective: `mneme init` runs the QMD setup transparently.
- Clean lifecycle: mneme owns process start/stop, restart-on-crash, graceful shutdown.
- Full QMD capability without reimplementation.
- MCP-binding is natural: the QMD MCP server is the MCP endpoint that hosts get bound to.
- `mneme doctor` can diagnose by introspecting the subprocess (PID, port, last-query latency, model availability).
- Future-flexible: the sidecar can be swapped for embedded QMD or a smaller core without changing the user-facing surface or the host bindings.
- Maps cleanly to claude-knowledge's existing integration: QMD already runs as an MCP server with multi-collection scoping; mneme adopts the same shape with managed lifecycle.

**Cons:**
- Process management complexity (PID files, port allocation, crash detection, restart loops).
- First-run cost: QMD model download (`all-MiniLM-L6-v2` ~90MB, optional reranker model larger). Must be scripted into `mneme init` with progress feedback.
- Two binaries on disk (mneme + qmd) even if user perception is one install.

**Verdict:** matches all seven decision drivers. The complexity cost is concentrated in `mneme init` / `mneme doctor` / process supervision code, which is the right place for it.

### Option 4: Smaller Retrieval Core (Reimplement Subset)

Mneme reimplements a smaller version of QMD: BM25 + a single embedding model + simple RRF fusion.

**Pros:**
- Smallest install footprint.
- Tailored API surface.
- Fully self-contained.

**Cons:**
- Reinvents non-trivial retrieval engineering that already works in QMD.
- Loses QMD-specific features that claude-knowledge already depends on (lex/vec/hyde combination, position-aware blending, intent-aware reranking, multi-collection scoping).
- Maintenance burden grows linearly with retrieval feature requests.
- Locks mneme into a specific retrieval implementation early; harder to swap later.
- Worse for the bet that QMD continues to evolve faster than mneme's retrieval team can match.

**Verdict:** premature optimization. The right time for this is *after* mneme proves product-market fit and the QMD interface stabilizes — at which point the subset that mneme actually uses will be empirically clear.

---

## Decision

**Adopt Option 3 (Sidecar) for v1**, with a documented path to Option 1 (Wrapper) once QMD stabilizes as a standalone install Pyro is willing to require.

The sidecar approach:

- `mneme init` installs the QMD binary into `~/.mneme/bin/qmd` (or wherever appropriate), downloads required models into `~/.mneme/models/`, writes the QMD config into `~/.mneme/config/qmd.yaml`.
- `mneme bind <host>` writes host-specific MCP configuration that points at the managed QMD socket. Examples:
  - For Codex: writes the QMD MCP server entry into Codex's config so the agent can call `mcp__qmd__query` etc.
  - For Claude Code: writes equivalent into `~/.claude/.mcp.json` or the project-scoped MCP config.
- `mneme status` shows QMD subprocess health: PID, uptime, last-query latency, index size per collection, model availability.
- `mneme doctor` runs end-to-end retrieval diagnostics: can it reach the socket, can it run a test query, are models loaded, are indices fresh, is the vault path resolved correctly.
- `mneme capture` (and other write paths) trigger incremental reindex via QMD's index API; the index lives in `~/.mneme/index/` separate from the vault.
- On `mneme` shutdown (SIGTERM, normal exit), the sidecar receives a graceful stop signal and persists any in-flight index state.

QMD collections map to mneme's vault layers:

| QMD collection | Mneme source path |
|---|---|
| `insights` | `vault/insights/*.md` |
| `compiled` | `vault/compiled/**/*.md` |
| `memory` | `vault/memory/**/*.md` (excluding inbox under aging policy) |
| `captures` | `vault/captures/*.md` |
| `ops` | `vault/ops/**/*.md` |

The default search scope (compiled → insights → memory → captures, per spec) is encoded as default `collections` parameter ordering on `mneme ask`.

---

## Consequences

### Positive

- **One install** from the user's perspective. `mneme init` produces a working retrieval system.
- **Lifecycle is owned by mneme.** The user never has to start, stop, restart, or update QMD directly.
- **Diagnosable.** `mneme doctor` and `mneme status` give the user actionable signal about retrieval health.
- **MCP-native.** `mneme bind` configures host MCP without the user touching MCP config files. This is critical for the bind-codex-first phase since the codex CLI's MCP integration must be turnkey.
- **Reuses claude-knowledge's working integration shape.** The existing claude-knowledge ↔ QMD pattern is already battle-tested with 1,584 docs across 4 collections. Mneme v1 inherits the proven pattern instead of inventing a new one.
- **Future-swappable.** If retrieval needs change (smaller footprint, different model, alternative engine), the sidecar can be replaced without changing the user-facing CLI or host bindings.

### Negative

- **First-run install is heavier than a pure-markdown product would be.** Model download takes minutes on a slow connection. Mitigation: `mneme init --offline` mode that defers model installation; `mneme doctor` reports which retrieval features are degraded until models are available.
- **Two binaries to maintain in distribution.** Mneme's release process must coordinate QMD version pinning. Mitigation: pin to a known QMD version per mneme release; document upgrade path.
- **Process management adds failure modes.** Crashed QMD process, port collisions, stale PID files. Mitigation: `mneme doctor` repair commands; defensive restart logic; configurable port range with auto-fallback.
- **The sidecar is part of mneme's blast radius.** Misbehavior in QMD impacts mneme's retrieval. Mitigation: timeouts on all retrieval calls; `mneme ask` returns degraded results (e.g., file-system grep) when QMD is unavailable rather than failing hard.

### Neutral

- The sidecar pattern is conventional (databases, language servers, Jupyter kernels all do this). Engineers familiar with similar tools will recognize the shape.
- This decision can be revisited in v0.3 once QMD's MCP API stabilizes. Migration to a wrapper approach is a config-file change, not a user-facing rewrite.

---

## Implementation Notes

### Phase 1 retrieval-related work (concrete tasks)

1. `mneme init` subcommand:
   - install QMD binary
   - download `all-MiniLM-L6-v2` (BM25 doesn't need a model; vec does)
   - allocate a port (default 7842 with collision-fallback up to 7847)
   - write `~/.mneme/config/qmd.yaml` with vault path, collection map, model paths
   - smoke-test: launch QMD, run a no-op query, shut down
2. `mneme` daemon supervisor:
   - launch QMD on `mneme` startup (if any subcommand needs it)
   - monitor PID, restart on crash with exponential backoff
   - graceful shutdown on `mneme stop` or signal
   - log retrieval events to `~/.mneme/log/qmd.log`
3. `mneme bind <host>`:
   - for Codex: write MCP server entry
   - for Claude Code: write MCP server entry
   - smoke-test: invoke a one-shot query through the host's MCP runtime, confirm result shape
4. `mneme ask <query>`:
   - construct the right `searches` array (lex+vec by default; +hyde when `--deep`)
   - apply default collection ordering (compiled → insights → memory → captures)
   - render results with source layer, trust, recency annotations
5. `mneme doctor`:
   - reachability: socket open?
   - functional: test query returns?
   - models: loaded?
   - indices: fresh? compare last-indexed time vs newest vault file
   - bindings: each bound host's MCP config still points at the right socket?

### What the QMD team is asked to provide

For this ADR to succeed cleanly, QMD should expose (if it doesn't already):

- a `--config <path>` flag for collection mapping
- an HTTP/socket health endpoint mneme can poll
- a stable MCP tool surface (the current `mcp__qmd__query` etc.) that mneme can pin to a version
- an indexer API (`qmd index --collection <name> --path <vault-subpath>`) callable from mneme on capture events
- a graceful-shutdown contract (responds to SIGTERM, persists index state)

If QMD is missing any of these, mneme either patches them upstream or wraps them with a shim before sidecar adoption is clean.

### Open questions deferred to implementation

- Exact reranker model choice (`bge-reranker-v2-m3` vs lighter alternatives) — pick during phase 1 with empirical comparison on the existing claude-knowledge corpus.
- Whether `mneme compile` (phase 2) writes its dossiers as a separate QMD collection (`compiled`) or reuses the insights collection with a marker. Recommend separate collection for clean ranking semantics.
- How `mneme status --remote` behaves once remote sync ships in v0.3+ — the sidecar architecture is local-only by design; remote sync is orthogonal.

---

## References

- Canonical product spec: `2026-04-23-mneme-product-spec.md`
- Original vision: `2026-04-22-mneme-unified-agent-memory-kg.md`
- Codie's product-boundary correction: `2026-04-22-codie-addendum-mneme-product-boundary-and-compiled-layer.md`
- Reference integration: `~/projects/agents/claude-knowledge` ↔ QMD MCP server (1,584 docs, 4 collections, lex/vec/hyde combination)
- Claude-knowledge usage of QMD: see CLAUDE.md "QMD — Local Search Engine" section

---

*Authored by Claude (Opus 4.6, 1M context) on 2026-04-26 at Pyro's request, given the canonical product spec from 2026-04-23 and Pyro's decisions on compiled-layer mechanism (on-demand-with-cache), host scope (Codex first, Claude second), and retrieval timing (ADR before code). This decision is the prerequisite for phase 1 implementation work.*
