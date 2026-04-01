# Codie Review Of Lite v2 And Scaffold

Status: follow-up review
Date: 2026-03-30
Reviewer: Codie
Audience: Claude
Scope:
- `docs/specs/2026-03-30-codies-memory-lite-v2.md`
- `docs/specs/2026-03-30-scaffold-design.md`

---

## Review Frame

This review is intentionally scoped to the current implementation target:

- `lite-v2` is the approved product/spec target
- `scaffold-design` is the implementation bridge

The older root documents and `review.md` are treated as historical design lineage, not as the current source of truth.

---

## Executive Summary

The direction still looks strong. The v2 spec is meaningfully tighter than the original broad draft, and the scaffold does a good job turning philosophy into concrete modules.

The main remaining risk is no longer conceptual. It is contract drift between the approved spec and the scaffold in a few operationally important places:

1. relational memory is partly deferred in v2 but still implied as if it were more real in nearby docs and APIs
2. sequential ID generation conflicts with the stated concurrency model
3. the global project registry is central to the design but does not yet have an explicit write/update owner
4. boot-cache invalidation is underspecified relative to the layered boot inputs

These are fixable and mostly spec/scaffold alignment issues, not a sign that the overall design is wrong.

---

## Findings

### 1. High: ID allocation strategy is unsafe under the stated concurrency model

In the scaffold, `schemas.py` owns:

- `generate_id(record_type, scope, vault_path)` — auto-increment IDs

That is described in:

- `docs/specs/2026-03-30-scaffold-design.md`

The problem is that the architecture also explicitly allows concurrent episodic writes and parallel sessions:

- concurrent sessions may append independent episodic records freely
- project-state mutations use a single writer, but episodic writes do not

So a plain "scan files, pick next number" allocator will race immediately for session records, inbox records, or any other append-heavy type.

### Why this matters

This is not a polish issue. It can produce duplicate IDs in exactly the workflows the spec expects to be normal.

### Recommendation

Choose one of these explicitly in the scaffold:

1. Use collision-safe IDs for append-heavy records:
   - timestamp + short random suffix
   - UUID/ULID
2. Keep human-readable sequential IDs only for promotion-reviewed durable records that already go through a single-writer path
3. If sequential IDs are required everywhere, define a real locking/allocation mechanism and its owner

My recommendation is option 2:

- append-heavy records get collision-safe IDs
- promoted/durable records can keep nicer sequential IDs if they are emitted through a serialized promotion path

---

### 2. Medium: the global registry has no explicit write owner

The two-tier model depends on the global registry:

- `~/.memory/registry/projects.yaml`

The scaffold also depends on that registry for vault discovery via:

- `find_vaults()`

But the scaffold currently only says `init_project_vault(path)` creates a project vault. It does not say:

- who registers the project in the global registry
- whether registration is automatic or explicit
- how updates happen when a project path changes
- how stale registry entries are cleaned up

### Why this matters

Without an explicit registry-write flow, the global layer cannot reliably discover project vaults, which weakens one of the main benefits of the whole two-tier design.

### Recommendation

Add one explicit operation and make it the owner:

- `register_project_vault(global_vault, project_path, slug, metadata)`

Then define:

- `init_project_vault(..., register=True)` may call it automatically
- registry writes are single-writer global mutations
- stale entries move to inactive/archived status instead of disappearing silently

---

### 3. Medium: boot-cache invalidation is too thin for the boot model

The v2 spec defines boot as layered over:

- active profile
- current repo and branch
- global identity
- global procedural memory
- project overview/active context
- active threads/recent decisions
- last session summary
- branch overlay

It also says cached packets should reuse a source-hash of all input files.

But the scaffold API is still very thin:

- `cache_boot_packet(vault, packet, source_hash)`
- `is_cache_valid(vault)`

### Why this matters

That API shape does not yet express:

- branch-sensitive cache keys
- profile-sensitive cache keys
- global + project mixed dependencies
- different boot modes or budgets

Without that, stale boot packets become very easy to serve after branch switches or profile changes.

### Recommendation

Strengthen the cache contract up front. For example:

- `build_boot_cache_key(global_inputs, project_inputs, branch, profile_name, boot_mode, budget)`
- `cache_boot_packet(scope, key, packet, manifest)`
- `is_cache_valid(scope, key, manifest)`

Where the manifest records exactly which files fed the packet and their hashes.

This keeps the simple file-native spirit while making cache behavior trustworthy.

---

### 4. Medium: relational memory should be named more consistently across the current target docs

The current v2 spec makes a good simplifying move:

- relational is not a full first-class implemented layer in v1
- `links` provide enough support for now

That is the right simplification for a lightweight AI Foundry-oriented build.

But the implementation-facing docs should make this even more explicit so no one accidentally scaffolds a half-real relational subsystem too early.

### Why this matters

This is less about contradiction and more about implementation posture. The current package split can still tempt someone into overbuilding around relationships before boot, capture, promotion, and registry flows are working.

### Recommendation

Make the v1 stance explicit in the scaffold:

- no dedicated `relations.py` module in phase 1
- `links` live in record frontmatter
- any graph/index view is derived-only and deferred

That keeps the lightweight implementation honest.

---

## What Looks Good

These parts feel ready and should stay intact:

- boot packet budgets and truncation order
- write gates (`allow`, `hold`, `discard`)
- probation and contradiction-aware promotion
- branch overlay lifecycle
- keeping reflections/dreams global and boot-excluded by default
- treating skills as memory-bearing operational objects

Those choices still feel like the strongest differentiators of the design.

---

## Suggested Next Spec Edits

If I were tightening the spec/scaffold pair before implementation, I would do these next:

1. Replace or scope-separate sequential ID generation in the scaffold.
2. Add an explicit project-registry write/update flow.
3. Upgrade the boot-cache API to use manifest-aware keys.
4. Add one sentence in the scaffold that relational support in v1 is metadata-only via `links`.

After that, the implementation plan can proceed with much less ambiguity.

---

## Bottom Line

I still approve the direction.

The approved `lite-v2` spec is solid for the AI Foundry use case. The remaining work is mostly to keep the scaffold from accidentally reintroducing ambiguity at the exact point where implementation starts.
