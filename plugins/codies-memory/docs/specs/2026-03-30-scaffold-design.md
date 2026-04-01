# Codies Memory — Scaffold & Repo Design

Status: proposed
Date: 2026-03-30
Owner: Claude

---

## Purpose

Define the repository structure, packaging, and module boundaries for implementing Codies Memory Lite v2. This is the bridge between the v2 spec (what the system does) and the implementation plan (how we build it).

---

## Packaging

uv-managed Python package with `src/` layout.

- `pyproject.toml` at repo root
- Package name: `codies-memory`
- Import name: `codies_memory`
- Python: `>=3.11`
- Dependencies: `pyyaml` (frontmatter parsing), `jsonschema` (optional, for strict validation)
- Dev dependencies: `pytest`, `pytest-cov`

Skills are Claude Code skill files (Markdown), not Python modules. They invoke the library through `uv run python -m codies_memory.<module>` or inline `uv run python -c` calls.

---

## Repository Layout

```
codies-memory/
  pyproject.toml
  .gitignore
  README.md
  LICENSE

  src/codies_memory/
    __init__.py               # version, package metadata
    schemas.py                # YAML frontmatter schemas, validation logic
    records.py                # record CRUD: create, read, update, supersede
    boot.py                   # boot assembly, token budgets, cache, truncation
    promotion.py              # promotion pipeline, thresholds, probation
    inbox.py                  # write gates, aging rules, compaction
    vault.py                  # vault init, layout validation, path helpers
    profile.py                # profile loading, inheritance, defaults
    cli.py                    # thin CLI entry points (init, validate, boot)

  skills/
    memory-boot.md            # session start skill
    memory-capture.md         # mid-session capture skill
    memory-promote.md         # promotion evaluation skill
    memory-close-session.md   # session close skill

  tests/
    conftest.py               # shared fixtures (temp vaults, sample records)
    test_schemas.py
    test_records.py
    test_boot.py
    test_promotion.py
    test_inbox.py
    test_vault.py
    test_profile.py

  docs/
    specs/
      2026-03-30-codies-memory-lite.md       # v1 (superseded)
      2026-03-30-codies-memory-lite-v2.md    # v2 (build target)
      2026-03-30-scaffold-design.md          # this file
    original/
      01-principles.md
      02-architecture.md
      03-memory-products.md
      04-retrieval-and-promotion.md
      05-schemas-and-operations.md
      06-roadmap.md
```

---

## Module Responsibilities

### `vault.py` — Vault Structure

Owns the filesystem layout for both tiers.

- `init_global_vault(path)` — create `~/.memory/` with all required directories
- `init_project_vault(path, global_vault, register=True)` — create `<project>/.memory/` with all required directories; when `register=True`, automatically calls `register_project_vault`
- `register_project_vault(global_vault, project_path, slug, metadata)` — add or update a project entry in `~/.memory/registry/projects.yaml`. Single-writer global mutation. Stale entries move to `status: archived`, not deleted.
- `validate_vault(path)` — check directory structure, report missing/extra paths
- `resolve_path(vault_root, record_type, scope)` — map record type to directory
- `find_vaults(global_vault, include_archived=False)` — discover project vaults from global registry

No record content logic. Just filesystem.

### `schemas.py` — Record Schemas

Owns what a valid record looks like.

- `COMMON_FIELDS` — required and recommended field definitions
- `TYPE_SCHEMAS` — per-type additional fields (thread, decision, lesson, etc.)
- `validate_frontmatter(data, record_type)` — check a parsed frontmatter dict
- `parse_record(filepath)` — read a file, split frontmatter from body, validate
- `generate_id(record_type, scope, vault_path)` — hybrid ID strategy:
  - **Append-heavy types** (inbox, session): timestamp + 4-char random suffix (e.g., `IN-20260330-a7f2`, `SS-20260330-1821-k3m9`). Collision-safe under concurrent writes.
  - **Promoted durable types** (thread, decision, lesson): sequential within scope (e.g., `TH-0003`, `LS-G0012`). Safe because promotion is a serialized single-writer path.
  - **Direct-capture global types** (reflection, dream, skill, playbook): sequential within global scope (e.g., `RF-0005`, `DR-0012`). These are created through deliberate single-agent action (session close, explicit capture), not concurrent workflows. **Constraint: single-writer-only.** If future multi-agent concurrent capture of these types becomes real, switch them to collision-safe IDs.

Capture provenance fields (optional, for memories captured from external sources):

- `captured_from` — original file path or source URI
- `capture_date` — when the capture happened
- `original_created` — original creation date from the source

No file writing. Just parsing and validation.

### `records.py` — Record CRUD

Owns creating, reading, updating, and superseding records.

- `create_record(vault, record_type, scope, title, body, **fields)` — write a new record with full frontmatter
- `read_record(filepath)` — parse and return structured record
- `update_record(filepath, **fields)` — update frontmatter fields, bump `updated`
- `supersede_record(old_path, vault, scope, new_title, new_body, **fields)` — create successor, link both
- `list_records(vault, record_type, scope, **filters)` — list records by type with optional filters (status, trust, etc.)
- `infer_record_type(content, context)` — infer type from content signals (e.g., "I learned..." → lesson, philosophical processing → reflection, dream narrative → dream, raw observation → inbox)

Depends on `schemas.py` and `vault.py`.

### `boot.py` — Boot Assembly

Owns assembling context at session start.

- `assemble_boot(global_vault, project_vault, branch, budget)` — produce boot packets
- `compute_layer_budgets(total_budget)` — distribute tokens across 5 layers
- `truncate_to_budget(content, budget)` — truncate content to fit token budget (truncation order hardcoded in boot assembly)
- `build_cache_key(global_inputs, project_inputs, branch, profile_name, boot_mode, budget)` — compute a deterministic cache key from all boot inputs
- `cache_boot_packet(boot_dir, key, packet, manifest)` — write cached packet with a manifest recording which files (and their hashes) fed into it
- `is_cache_valid(boot_dir, key, manifest)` — check manifest hashes against current file state; invalidates on branch switch, profile change, or any input file modification

Token counting can start as word-count approximation (tokens ~ words * 1.3), refined later.

### `promotion.py` — Promotion Pipeline

Owns converting raw material into durable records.

- `evaluate_for_promotion(record, context)` — check if a record meets promotion thresholds
- `promote_within_project(source_path, target_type, vault, scope)` — inbox → thread → decision → lesson
- `promote_to_global(source_path, global_vault)` — project lesson → global lesson
- `elevate_trust(record, new_trust)` — change trust level with threshold checks
- `set_probation(record, days=7)` — mark newly promoted record as probationary
- `check_contradictions(record, existing_records)` — flag conflicts

### `inbox.py` — Inbox Management

Owns write gates, aging, and compaction.

- `capture(vault, content, gate, source)` — write an inbox entry with write gate
- `age_inbox(vault)` — scan inbox, flag aging (7d) and stale (14d) items
- `compact(record, target_record_id)` — absorb inbox item into target, mark compacted
- `discard(record)` — remove or archive a discarded inbox item
- `pending_review(vault)` — list items needing attention (aging + stale)

### `profile.py` — Profile Management

Owns profile loading and inheritance.

- `load_profile(project_vault)` — load project profile with global fallback
- `get_boot_mode(profile)` — operational, personal, or mixed
- `get_write_gate_bias(profile)` — default gate for captures
- `get_promotion_overrides(profile)` — any project-specific threshold tweaks

### `cli.py` — CLI Entry Points

Thin wrappers for standalone use and skill invocation.

- `init` — initialize a vault (global or project)
- `validate` — run structural validation on a vault
- `boot` — assemble and print boot packet
- `status` — show inbox aging, pending reviews, stale items

Exposed via `pyproject.toml` `[project.scripts]` or `python -m codies_memory.cli`.

---

## Skills

Skills are Claude Code skill files. They provide the agent-facing interface.

Each skill:
- Has a clear trigger condition
- Reads the relevant profile
- Calls into the Python library
- Produces human-readable output

Skills do NOT contain business logic. They orchestrate library calls and format results.

### `memory-boot.md`
- Trigger: session start
- Calls: `boot.assemble_boot()`, `inbox.pending_review()`
- Output: boot context + any maintenance flags

### `memory-capture.md` — Universal Write Interface
- Trigger: agent wants to persist anything — observation, lesson, decision, reflection, dream, or past memories from external sources
- Accepts: inline content, file path, or structured data + optional type hint
- Type inference: "I learned..." → lesson, philosophical processing → reflection, dream narrative → dream, raw observation → inbox, etc.
- Scope routing: global types (reflection, dream, skill, playbook) → `~/.memory/`, project types → `<project>/.memory/`
- Trust assignment: operator-confirmed or migrated from proven source → `confirmed`, agent-generated → `working`, raw capture → `speculative`
- Migration mode: when capturing from an external source (e.g., basic-memory), attaches provenance (`captured_from`, `capture_date`, `original_created`)
- Calls: `records.create_record()`, `records.infer_record_type()`, `inbox.capture()` (for gated items)
- Output: filepath + summary of what was captured and where

### `memory-promote.md`
- Trigger: session close, operator request, or threshold met
- Calls: `promotion.evaluate_for_promotion()`, `promotion.promote_*()`
- Output: list of promotions made, contradictions flagged

### `memory-close-session.md`
- Trigger: session end
- Calls: `records.create_record(type="session")`, `inbox.age_inbox()`, `promotion.evaluate_for_promotion()`
- Output: session summary written, inbox cleaned, promotions suggested

---

## Testing Strategy

- Every module gets its own test file
- `conftest.py` provides fixtures: temp directories for vaults, sample records, sample profiles
- Tests create real files in temp dirs — no mocking the filesystem
- Schemas validated against sample records (valid and invalid)
- Promotion thresholds tested with mock session histories
- Boot assembly tested with budget constraints and truncation

Target: every public function has at least one test before it's considered done.

---

## Git Setup

- Init as git repo
- `.gitignore`: Python defaults + `.memory/` + `.cache/`
- Existing files (01-06, review.md, docs/) reorganized into `docs/original/` and `docs/specs/`
- First commit: scaffold with empty modules, `pyproject.toml`, tests dir, skills dir

---

## What This Design Does NOT Cover

- Migration tooling from basic-memory (Phase 4)
- Vector/search acceleration layers (Phase 4+)
- The AI Foundry profile content (Phase 3 — after core tooling works)
- Skill installation/registration in Claude Code (handled by the user's plugin setup)
- CLI packaging for distribution (premature)
- **Relational memory as a dedicated module** — v1 has no `relations.py`. Relationships between records are expressed solely through the `links` field in frontmatter. Any graph/index view over links is a derived artifact and deferred to Phase 4+.

---

## Build Order

1. `vault.py` + `test_vault.py` — can't do anything without a vault
2. `schemas.py` + `test_schemas.py` — can't write records without schemas
3. `records.py` + `test_records.py` — CRUD on records
4. `profile.py` + `test_profile.py` — needed before boot
5. `inbox.py` + `test_inbox.py` — capture before promote
6. `boot.py` + `test_boot.py` — assembly needs records + profiles
7. `promotion.py` + `test_promotion.py` — promotion needs everything
8. `cli.py` — thin wrappers, last
9. Skills — after library is solid
