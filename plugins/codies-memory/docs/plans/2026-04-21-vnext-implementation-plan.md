# Codies Memory vNext Implementation Plan

> **For agentic workers:** Treat this as a planning artifact, not an execution transcript. Keep tasks small, preserve repo-relative file references, and verify each phase before moving on.

**Goal:** Evolve `plugins/codies-memory` from a strong file-vault and promotion system into a clearer marketplace product with first-class QMD retrieval guidance, lightweight warm-memory artifacts, usage-aware refresh logic, and an optional background learner that never replaces canonical file truth.

**Architecture:** `filesystem truth + QMD retrieval + warm summaries + optional background extraction`

**Tech Stack:** Python 3.11+, Markdown skill docs, `argparse`, `pytest`, `uv`, QMD MCP integration as external runtime dependency

**Design:** `docs/specs/2026-04-21-codies-memory-vnext-marketplace-design.md`

---

## Scope

This plan covers four staged outcomes:

1. Clarify the marketplace product boundary and retrieval story
2. Add a warm-memory layer as derived file-native artifacts
3. Add lightweight usage tracking to keep warm memory relevant
4. Add an optional local background learner that emits only low-trust candidates

This plan does not require:

- replacing canonical markdown records
- embedding QMD into the plugin package
- forcing an always-on daemon
- shipping all four stages in one release

---

## Recovered Prior Findings

These findings were recovered from the dedicated `limitless` project memory plus QMD-backed recall across Codie memory.

They should shape the implementation unless proven obsolete:

1. **Multiline body handling is still a likely CLI ergonomics bug**
   Records created with `create --body` and escaped newlines can be saved with literal `\n` sequences instead of real line breaks. The current `--body-file` support is a mitigation, but the plan should still explicitly harden multiline input behavior and documentation.

2. **QMD freshness must be part of the retrieval contract**
   A missing QMD result does not always mean the memory is absent. Older notes show the collection index can lag behind on-disk writes. Retrieval docs should instruct operators to check `qmd status` and collection timestamps before trusting a miss.

3. **The canonical model still lacks a clean home for side-thread ideas and follow-up nudges**
   Two active project threads remain unresolved:
   - meaningful adjacent idea threads that are too durable for inbox noise but not yet their own project
   - short future system nudges like “after this project, update the memory skills to mention QMD”
   The vNext plan should explicitly decide their routing instead of assuming warm memory or the learner will solve them indirectly.

4. **Managed-package distribution remains a real future improvement, but not a vNext blocker**
   Publishing `codies-memory` as a managed Python package would reduce stale clone drift and clean up installs, but this is separate distribution work and should stay out of the core vNext implementation slices unless packaging work is explicitly pulled in.

---

## File Map

### Existing Files To Modify

| File | Purpose |
|------|---------|
| `README.md` | Marketplace-facing plugin positioning and installation story |
| `INSTALL.md` | Standalone installation and full-mode guidance |
| `skills/memory-boot/SKILL.md` | Boot workflow, retrieval guidance, and operator expectations |
| `skills/memory-help/SKILL.md` | Memory concepts and preferred retrieval workflow |
| `src/codies_memory/boot.py` | Existing boot assembly logic, likely home for summary refresh integration hooks |
| `src/codies_memory/cli.py` | New subcommands or flags for summary rebuild / usage / learner flows |
| `src/codies_memory/vault.py` | New paths for warm artifacts or staged learner outputs if needed |
| `tests/test_boot.py` | Warm-summary and budget tests |
| `tests/test_cli.py` | CLI surface tests for new summary / usage / learner commands |
| `tests/test_docs_operator_surface.py` | Docs and skill operator-surface assertions |

### New Files Likely Needed

| File | Purpose |
|------|---------|
| `src/codies_memory/warm.py` | Build and refresh warm-memory artifacts |
| `src/codies_memory/usage.py` | Usage ledger read/write and relevance heuristics |
| `src/codies_memory/learner.py` | Optional background extraction orchestration |
| `tests/test_warm.py` | Unit tests for summary generation and scoping |
| `tests/test_usage.py` | Unit tests for usage tracking and ranking |
| `tests/test_learner.py` | Unit tests for learner staging behavior |
| `docs/specs/2026-04-21-codies-memory-vnext-marketplace-design.md` | Existing design doc; keep in sync if implementation shifts materially |

### Optional Future Files

| File | Purpose |
|------|---------|
| `skills/memory-refresh/SKILL.md` | Optional explicit maintenance skill if summary rebuilding becomes common |
| `scripts/run_learner.py` | Thin operator-facing launcher for background extraction |

---

## Implementation Principles

- Canonical vault files remain the source of truth.
- QMD is the preferred retrieval path when available, but the plugin must degrade gracefully without it.
- Warm artifacts are derived markdown, not hand-maintained truth.
- The learner may write `speculative` or staged records only.
- Promotion, trust elevation, and scope boundaries stay explicit.
- Search scope may be broad; boot injection must remain narrow.
- Historical operator-surface bugs and routing gaps should be resolved explicitly, not assumed to disappear as a side effect of new architecture.

---

## Phase 1: Retrieval-First Product Clarification

**Outcome:** The plugin docs and skills tell the truth about the system: `codies-memory` owns structured memory writes and lifecycle semantics, while QMD is the preferred retrieval layer when present.

### Task 1: Update Marketplace And Operator Messaging

**Files:**
- Modify: `README.md`
- Modify: `INSTALL.md`

- [ ] Update the plugin description so it no longer reads like retrieval is missing.
- [ ] Introduce the two supported operating modes:
  - standalone: canonical vault only
  - full mode: canonical vault plus QMD retrieval
- [ ] Clarify that QMD is not packaged inside this plugin but is the recommended recall path when available.
- [ ] Add a short “How recall works” section to `INSTALL.md`:
  - boot for scoped startup context
  - QMD for cross-store recall
  - canonical files for deep truth

### Task 2: Update Skills To Treat QMD As The Preferred Read Path

**Files:**
- Modify: `skills/memory-boot/SKILL.md`
- Modify: `skills/memory-help/SKILL.md`

- [ ] In `memory-boot`, add a retrieval step after boot that says:
  - use QMD first when searching across memory layers
  - fall back to local file inspection only if QMD is unavailable or too narrow
- [ ] In `memory-help`, add a short “Recall workflow” section:
  - `qmd status`
  - `qmd query`
  - `qmd get`
- [ ] In both skills, document the freshness caveat:
  - check `qmd status` and collection timestamps before treating a missing hit as absence
  - distinguish “not found in the current index” from “does not exist on disk”
- [ ] Keep the wording product-level and operator-friendly; do not assume internal repo knowledge.

### Task 3: Verify Operator Surface

**Files:**
- Modify: `tests/test_docs_operator_surface.py`

- [ ] Add assertions that docs mention `QMD` or `qmd` in the right places.
- [ ] Add assertions that the plugin clearly distinguishes standalone mode from full mode.
- [ ] Add assertions that the retrieval docs mention freshness or reindex/timestamp checking so the operator surface does not overclaim search completeness.
- [ ] Ensure tests do not overfit exact prose; verify operator truth, not wording style.

### Task 4: Harden Multiline Record Creation Ergonomics

**Files:**
- Modify: `src/codies_memory/cli.py`
- Modify: `tests/test_cli.py`
- Modify if needed: `INSTALL.md`
- Modify if needed: `skills/memory-help/SKILL.md`

- [ ] Decide the intended behavior for multiline `create` input:
  - normalize escaped `\n` sequences in `--body`
  - or keep `--body` literal and steer multiline content strongly toward `--body-file`
- [ ] Prefer one truthy operator path rather than a half-supported ambiguity.
- [ ] Add focused tests for:
  - single-line `--body`
  - multiline `--body-file`
  - escaped newline handling if supported
- [ ] Update operator docs so agents stop relying on fragile shell quoting for rich multiline records.

### Phase 1 Verification

- [ ] Run:

```bash
cd plugins/codies-memory
uv run pytest -q tests/test_docs_operator_surface.py tests/test_cli.py
```

- [ ] Manual read-through:
  - a new operator should understand the difference between boot, retrieval, and canonical truth
  - no document should imply that the plugin internally owns all retrieval infrastructure

---

## Phase 2: Warm Memory Layer

**Outcome:** Boot has small derived summaries that act as maps, not territory.

### Task 1: Define Warm Artifact Contract

**Files:**
- Modify: `src/codies_memory/vault.py`
- Add: `src/codies_memory/warm.py`

- [ ] Define stable warm artifact locations:
  - `~/.memory/<agent>/boot/global-summary.md`
  - `~/.memory/<agent>/projects/<slug>/boot/project-summary.md`
  - `~/.memory/<agent>/projects/<slug>/boot/recent-episodes.md`
- [ ] Decide whether source manifests live alongside summaries as JSON or markdown sidecars.
- [ ] Keep these artifacts explicitly derived and rebuildable.

### Task 2: Implement Summary Builders

**Files:**
- Add: `src/codies_memory/warm.py`
- Modify: `src/codies_memory/boot.py`

- [ ] Implement a builder for global summary from:
  - identity
  - durable user profile
  - global procedural memory
- [ ] Implement a builder for project summary from:
  - `project/`
  - active decisions
  - active threads
  - latest relevant session context
- [ ] Implement a builder for recent episodes from:
  - the newest sessions only
  - bounded token/line budgets
- [ ] Reuse current boot-budget thinking from `boot.py` instead of inventing a second unrelated budgeting system.

### Task 3: Add CLI Surface For Warm Refresh

**Files:**
- Modify: `src/codies_memory/cli.py`

- [ ] Add an explicit refresh command such as:
  - `codies-memory refresh --agent <name>`
  - or `codies-memory warm rebuild --agent <name>`
- [ ] Support refreshing:
  - global-only
  - current project only
  - both
- [ ] Prefer a command shape that remains usable from skills and direct shell workflows.

### Task 4: Test Scoping And Budget Behavior

**Files:**
- Add: `tests/test_warm.py`
- Modify: `tests/test_boot.py`
- Modify: `tests/test_cli.py`

- [ ] Verify global summary excludes project-local details.
- [ ] Verify project summary stays scoped to the resolved project vault.
- [ ] Verify recent episodes stay bounded and do not dump entire session history.
- [ ] Verify rebuild behavior is deterministic for the same input set.

### Phase 2 Verification

- [ ] Run:

```bash
cd plugins/codies-memory
uv run pytest -q tests/test_warm.py tests/test_boot.py tests/test_cli.py
```

- [ ] Manual smoke check:
  - initialize a fake vault
  - build warm summaries
  - confirm summaries are concise and human-readable

---

## Phase 2B: Routing Gaps For Adjacent Ideas And System Nudges

**Outcome:** The canonical memory model gains an explicit answer for non-project-adjacent durable thoughts that do not fit cleanly into the current project execution flow.

### Task 1: Choose The Smallest Viable Routing Model

**Files:**
- Modify: `docs/specs/2026-04-21-codies-memory-vnext-marketplace-design.md`
- Modify if needed: `src/codies_memory/schemas.py`
- Modify if needed: `src/codies_memory/vault.py`

- [ ] Decide how to route:
  - adjacent idea threads that are not yet their own project
  - short follow-up system nudges
- [ ] Evaluate the smallest viable options first:
  - `_general` or equivalent holding area
  - dedicated tags/conventions on existing records
  - dedicated subdirectory without introducing a whole new trust model
- [ ] Avoid adding a new record type unless the routing problem cannot be solved with existing semantics plus clearer placement.

### Task 2: Implement The Chosen Routing

**Files:**
- Modify: `src/codies_memory/vault.py`
- Modify: `src/codies_memory/records.py`
- Modify if needed: `src/codies_memory/cli.py`

- [ ] Add the minimal filesystem and record-resolution support needed for the chosen routing shape.
- [ ] Preserve existing promotion rules unless the new routing truly requires new transitions.
- [ ] Keep project-local execution memory separate from side-thread idea capture.

### Task 3: Document The Pattern

**Files:**
- Modify: `skills/memory-help/SKILL.md`
- Modify if needed: `skills/memory-capture/SKILL.md`
- Modify if needed: `README.md`

- [ ] Explain when to use the new side-thread/nudge routing path versus normal project inbox capture.
- [ ] Give one clear example for each of:
  - adjacent idea thread
  - future follow-up nudge

### Task 4: Test The Routing Boundary

**Files:**
- Modify or add: `tests/test_vault.py`
- Modify or add: `tests/test_records.py`
- Modify or add: `tests/test_cli.py`

- [ ] Verify adjacent ideas can be captured durably without pretending to be current-project implementation work.
- [ ] Verify follow-up nudges have a stable home and are not forced into lessons or decisions prematurely.
- [ ] Verify the new routing does not break existing project-vault resolution or list behavior.

### Phase 2B Verification

- [ ] Run:

```bash
cd plugins/codies-memory
uv run pytest -q tests/test_vault.py tests/test_records.py tests/test_cli.py
```

---

## Phase 3: Usage Tracking

**Outcome:** Warm artifacts can prefer repeatedly useful memory instead of only recency.

### Task 1: Add Usage Ledger

**Files:**
- Add: `src/codies_memory/usage.py`
- Modify: `src/codies_memory/vault.py`

- [ ] Define a lightweight file-native ledger location, for example:
  - `~/.memory/<agent>/boot/usage.json`
  - or project-local equivalents under `projects/<slug>/boot/`
- [ ] Keep the schema simple:
  - record path or record id
  - usage count
  - last used timestamp
  - usage source

### Task 2: Add Explicit Usage Recording Surface

**Files:**
- Modify: `src/codies_memory/cli.py`

- [ ] Add a small explicit command such as:
  - `codies-memory mark-used <path> --agent <name>`
  - or `codies-memory usage record <path> --agent <name>`
- [ ] Make this command safe to call from future skills or QMD-adjacent tooling.

### Task 3: Integrate Usage Into Warm Ranking

**Files:**
- Modify: `src/codies_memory/warm.py`

- [ ] Prefer durable records with repeated usage over merely recent records when selecting content for summaries.
- [ ] Do not let usage overwhelm scoping or trust semantics.
- [ ] Preserve a bias toward `confirmed` and `canonical` records when ties exist.

### Task 4: Test Relevance Heuristics

**Files:**
- Add: `tests/test_usage.py`
- Modify: `tests/test_warm.py`

- [ ] Verify repeated usage improves inclusion probability in summaries.
- [ ] Verify low-trust noise does not dominate warm outputs because of accidental repeated access.
- [ ] Verify missing usage data falls back to sane recency/trust behavior.

### Phase 3 Verification

- [ ] Run:

```bash
cd plugins/codies-memory
uv run pytest -q tests/test_usage.py tests/test_warm.py tests/test_cli.py
```

- [ ] Manual sanity check:
  - mark one durable lesson as used several times
  - rebuild summaries
  - confirm it becomes easier to surface without leaking unrelated project detail

---

## Phase 4: Optional Background Learner

**Outcome:** The system can learn passively without changing what counts as canonical truth.

### Task 1: Define Learner Input Boundary

**Files:**
- Add: `src/codies_memory/learner.py`
- Modify if needed: `INSTALL.md`

- [ ] Decide the first supported evidence source:
  - session summaries
  - hook artifacts
  - recent command logs
- [ ] Start with one evidence source only.
- [ ] Document that learner support is optional and local-only.

### Task 2: Define Learner Output Boundary

**Files:**
- Add: `src/codies_memory/learner.py`
- Modify: `src/codies_memory/schemas.py`

- [ ] Choose the safest output shape for v1 learner support:
  - staged inbox records
  - speculative lessons with explicit provenance
  - a separate candidate-review directory
- [ ] The safest first choice is likely staged project inbox records or a dedicated candidate area, not direct lesson creation.
- [ ] Add provenance fields needed to trace learner-created records back to their evidence source.

### Task 3: Add Operator Surface

**Files:**
- Modify: `src/codies_memory/cli.py`
- Add optional: `scripts/run_learner.py`

- [ ] Add an explicit entrypoint such as:
  - `codies-memory learn run --agent <name>`
  - or `codies-memory learner run --agent <name>`
- [ ] Keep it batch-oriented first; do not build an always-on daemon in the first slice.
- [ ] Optionally add flags for:
  - `--working-dir`
  - `--source`
  - `--dry-run`

### Task 4: Refresh Warm Artifacts After Learning

**Files:**
- Modify: `src/codies_memory/learner.py`
- Modify: `src/codies_memory/warm.py`

- [ ] After learner writes candidates, trigger or recommend a warm-summary rebuild.
- [ ] Keep refresh failures non-fatal so learner output is not lost if summary generation fails.

### Task 5: Test Safety Boundaries

**Files:**
- Add: `tests/test_learner.py`
- Modify: `tests/test_cli.py`

- [ ] Verify learner output never auto-promotes to high-trust records.
- [ ] Verify learner-created records carry provenance.
- [ ] Verify `--dry-run` produces inspectable output without mutating the vault.
- [ ] Verify learner failure does not corrupt existing canonical files.

### Phase 4 Verification

- [ ] Run:

```bash
cd plugins/codies-memory
uv run pytest -q tests/test_learner.py tests/test_cli.py tests/test_schemas.py
```

- [ ] Manual smoke check:
  - create a fake session artifact
  - run learner in `--dry-run`
  - inspect proposed outputs
  - run without `--dry-run`
  - confirm only low-trust or staged records are written

---

## Sequencing

Recommended delivery order:

1. Phase 1 first
   Reason: correct product messaging and skill guidance before adding new code paths

2. Phase 2 second
   Reason: warm memory is the smallest high-leverage functional addition

3. Phase 2B third
   Reason: adjacent-idea and nudge routing is a canonical model gap, not a retrieval garnish

4. Phase 3 fourth
   Reason: usage tracking sharpens warm memory but depends on Phase 2 artifacts

5. Phase 4 last
   Reason: background learning is the highest-risk slice and should sit on a stable warm layer

If the project needs a smaller first release, stop after Phase 2.

---

## Risks And Stop Rules

### Risk 1: Warm Memory Becomes Redundant With Boot Packet

Stop rule:

- If warm summaries do not materially improve scannability or routing versus the existing boot packet, do not keep both shapes without narrowing one of them.

### Risk 2: Usage Tracking Adds Complexity Without Better Retrieval

Stop rule:

- If usage tracking does not noticeably improve summary relevance in tests or manual checks, keep it out of the first shipping slice.

### Risk 3: Learner Output Pollutes Canonical Memory

Stop rule:

- If learner implementation requires silent promotion or weak provenance to feel useful, the design is wrong. Keep learner outputs staged or speculative only.

### Risk 4: QMD Coupling Becomes Hard Dependency

Stop rule:

- If any code path makes the plugin unusable without QMD, back it out. Retrieval integration should improve the full mode, not break standalone mode.

### Risk 5: New Routing Types Accidentally Create Taxonomy Sprawl

Stop rule:

- If solving adjacent ideas and nudges requires multiple new record classes or a second promotion system, back up and choose a simpler routing model.

---

## Release Shape Recommendation

### Recommended First Release

Ship:

- Phase 1: retrieval-first clarification
- Phase 2: warm memory layer
- optional narrow slice from Phase 2B only if the routing model stays very small

Hold:

- the rest of Phase 2B unless the routing pain is blocking live use
- Phase 3: usage tracking unless Phase 2 feels noisy
- Phase 4: background learner until warm summaries are clearly useful

This gives the plugin a stronger marketplace story quickly:

- better docs
- better retrieval guidance
- better boot ergonomics
- safer multiline operator behavior if Phase 1 Task 4 lands

without taking on the risk of autonomous learning too early.

### Future Follow-On: Managed Package Distribution

Keep this as a separate future track after vNext core work:

- publish `codies-memory` as an installable managed package for non-plugin agents
- keep `uv run` from the plugin checkout as the development path
- revisit when package publishing credentials and release process are available

---

## Done Criteria

This plan is complete when:

- `codies-memory` clearly documents its relationship to QMD
- warm summaries exist and are rebuildable from canonical records
- boot remains scoped and concise
- standalone mode still works without QMD
- optional usage tracking and learner features, if shipped, never weaken trust semantics or canonical file ownership
