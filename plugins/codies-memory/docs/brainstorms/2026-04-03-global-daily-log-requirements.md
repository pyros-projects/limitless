---
date: 2026-04-03
topic: global-daily-log
---

# Global Daily Log, Default Project, and --short Flag

## Problem Frame

Session records are project-scoped only. When a session spans multiple projects or happens outside any project context, there is nowhere to write it. The workaround -- creating a fake project vault just to have somewhere to land a session record -- is ugly and pollutes the project registry.

Additionally, there is no cross-project view of what happened on a given day. Boot shows the last session for the current project, but has no awareness of work done elsewhere. An agent booting into project A has no idea it just spent three hours on project B.

## Requirements

Implementation paths in this document are relative to the `codies-memory`
plugin root.

**Default Project**

- R1. `init --type global` creates a `_general` project vault alongside the global vault structure, registered in `projects.yaml` with slug `_general`, no `working_dir` key, and no `git_remote` key. This is the chosen creation model for new global vaults. `init_project_vault` gains parameters `write_marker: bool = True` and `working_dir: Path | None = None` (made optional). When `working_dir` is None: marker file is skipped, git remote detection is skipped, and `register_project_vault` omits `working_dir` from the entry. The slug `_general` is reserved -- `init_project_vault` rejects it when called by users directly.
- R2. When `resolve_project_vault` returns None, the CLI commands `create` and `capture` auto-fallback to `_general` (resolved as `global_vault / "projects" / "_general"`), but only for project-scoped record types. Global-scoped types (reflection, dream, skill, playbook, identity) still route to the global vault as before -- they never touch `_general`. The `_resolve_project_vault` helper in `src/codies_memory/cli.py` is updated to return `_general` instead of calling `sys.exit(1)`. For pre-existing global vaults that do not yet have `_general`, this fallback path creates `_general` on first use with the same directory layout and registry shape as R1. Other commands (`status`, `boot`, `validate`, `list`) do not fallback -- they report which vault resolved (or None) and behave accordingly.
- R3. `_general` behaves like any other project vault -- same directory structure, same record types, same promotion paths. The only difference is: no marker file, no working_dir in registry.
- R4. `status` and `boot` show which vault was resolved. Note: these commands do not fall back to `_general` -- they display the resolved project vault (which may be None). If a prior `create`/`capture` wrote to `_general`, boot will load `_general` as the project context only if it resolves via the normal three-tier lookup (which it won't, since `_general` has no marker or working_dir). Boot's cross-project awareness comes from the global daily log (R9), not from loading `_general`.

**Global Daily Log**

- R5. A `sessions/` directory is added to the global vault structure (`GLOBAL_DIRS`). The directory is created lazily on first daily log write (not eagerly in `init_global_vault`) to avoid breaking `validate_vault` on existing vaults. Global-vault validation passes when `sessions/` is absent. If `sessions/` exists, it must be a directory; an empty directory is valid; any `*.md` files inside it are validated as `daily-log` records. No new public CLI command validates an arbitrary daily-log file path; direct file-level validation, if used by tests or helpers, follows the existing record-validation file-exists behavior.
- R6. A daily log file is created (or appended to) at `~/.memory/<agent>/sessions/YYYY-MM-DD.md` whenever a CLI command creates a user-initiated record (`create`, `capture`). The daily log is not written by `promote`, `supersede_record`, or other internal record-creation paths.
- R7. Each entry in the daily log is a single line: `- [[RECORD-ID]] <short> (<project-slug-or-global>)`. The project slug is derived from the vault path (`vault.name` for project vaults under `global_vault/projects/<slug>/`, or `"global"` for global-scoped records where the vault IS the global vault).
- R8. The daily log file uses type `daily-log` (not `session`) to avoid collisions with project session records. Frontmatter is write-once on creation: `id` (format: `DL-YYYYMMDD`), `title` (the date, `YYYY-MM-DD`), `type: daily-log`, `status: active`, `trust: canonical`, `scope: global`, `created`, `updated` (both set once to the same timestamp, `updated` never bumped -- present only to satisfy `REQUIRED_FIELDS` validation). The file date and id use the agent process's local date. `created` and `updated` use ISO 8601 local-offset timestamps with seconds precision, e.g. `2026-04-03T16:41:00+02:00`. Body is pure append, frontmatter is never rewritten. The `DL-YYYYMMDD` ID format is generated directly by `append_daily_log`, not via `generate_id()`, since daily log files are one-per-day and not created through `create_record`.
- R9. Boot reads the **tail** of the most recent global daily log file from the global vault's `sessions/` directory (not the whole file -- read the last N lines to avoid loading a full busy-day log). Use a constant such as `DAILY_LOG_TAIL_LINES = 25` for the initial implementation. In the boot packet, render the tail under a `Global Daily Log` subsection in the existing recent-activity/session layer. That layer means "last project session plus cross-project daily activity"; if a token or character budget is enforced, include the latest project session first, then add newest daily-log lines until the remaining budget is full, dropping older daily-log lines first.
- R10. `("daily-log", "global")` is added to `_PATH_MAP` pointing to `sessions/`. `daily-log` is added to `_ID_PREFIXES` as `DL` and to `TYPE_EXTRA_FIELDS` (empty set). `daily-log` and `daily-logs` are added to the `type_aliases` dict in `cmd_list` so that `codies-memory list daily-log --scope global` works.

**--short Flag**

- R11. `create` gets an optional `--short` argument: a one-line summary used in the daily log entry. Sanitization: single-line only, strip leading/trailing whitespace, collapse internal newlines to spaces, hard-cap at 120 characters before writing to the daily log. Truncation uses the sanitized value.
- R12. `capture` gets an optional `--short` argument with the same purpose.
- R13. The CLI passes `--short` (or the title as fallback when `--short` is omitted) directly to `append_daily_log` -- no read-back from record frontmatter. For `capture`, the fallback is the auto-generated title (`content[:80]`), which may be noisy; agents should prefer providing `--short` for captures.
- R14. The `short` value is stored in the record's frontmatter so it is available for search and display. `short` is added to the universal known-fields set in `validate_frontmatter` (alongside `probation_until`, `promoted_from`, etc.) rather than per-type in `TYPE_EXTRA_FIELDS`. This avoids unknown-field warnings for all record types including `daily-log`.

**Auto-Linking**

- R15. A new function `append_daily_log(global_vault, record_id, short_text, project_slug)` in `src/codies_memory/records.py` handles appending to the daily log. CLI commands (`cmd_create`, `cmd_capture`) call this after `create_record` returns. This is the integration point -- not `create_record` itself, which stays pure. `promote_within_project`, `promote_to_global`, and `supersede_record` call `create_record` directly and never trigger the daily log.
- R16. `capture()` in `src/codies_memory/inbox.py` does not change. The CLI `cmd_capture` handler calls `append_daily_log` after calling `capture()`, passing the global vault path it already has.
- R17. The `user` command does not auto-link (identity operations are not record-producing commands).
- R18. The `feedback` command does not auto-link (meta operations about the memory system itself).

**Skill Updates**

- R19. **memory-close-session** (`skills/memory-close-session/SKILL.md`): Update to include `--short "one-line summary"` in the `create session` command template (if omitted, the title is used as the daily log entry). Note that sessions can land in `_general` when no project vault exists. Mention that a daily log entry is auto-generated -- the agent does not need to write it manually. Update or remove any promotion-evaluation snippet that hard-exits when no named project vault resolves; after this change, no-project session closeout is valid and routes through `_general`.
- R20. **memory-capture** (`skills/memory-capture/SKILL.md`): Add `--short "one-line summary"` to capture examples and explain its purpose (one-liner for the daily log). Note that captures work even without a project vault (falls back to `_general`). Update the **Scope Routing** section to note that project types fall back to `_general` when no project vault is resolved.
- R21. **memory-boot** (`skills/memory-boot/SKILL.md`): Explain that the boot packet now includes a global daily log showing cross-project activity. If the resolved project vault is `_general`, note in the boot output explanation that records are landing in the default project, not a named project. Dependency: this skill update depends on R9 (boot reads global daily log) -- update the skill doc only after the boot code change lands.
- R22. **memory-help** (`skills/memory-help/SKILL.md`): Update the following sections:
  - **Record Types table**: Add `daily-log` type (`global only | auto-generated, append-only body, do not create or edit manually`). Update **Session row**: change scope from `project` to `project (or _general)` and update "When to create" to note sessions land in `_general` when no project vault exists.
  - **Project Resolution**: Replace "if none match, there's no project vault" with: "For `create` and `capture`, if no project vault resolves, the command falls back to `_general`. Other commands (`status`, `boot`, `validate`, `list`) report which vault resolved (or None) without fallback."
  - **Commands > Create**: Add `--short "one-line summary"` to the command syntax.
  - **Commands > Capture**: Add `--short "one-line summary"` to the command syntax.
  - **Vault Structure**: Add `sessions/` directory under the global vault (for daily logs; created lazily on first write, not during init). Add `_general/` under `projects/` with a note that it is the default catch-all project.
  - **Concepts**: Add a "Daily Log" concept section explaining: (1) every `create` and `capture` operation auto-appends to a daily cross-project index at `~/.memory/<agent>/sessions/YYYY-MM-DD.md`, (2) each entry is a single line: `- [[RECORD-ID]] <short-text> (project-slug-or-global)`, (3) only user-initiated operations trigger entries — promotion and internal record-creation do not.
- R23. **memory-promote** (`skills/memory-promote/SKILL.md`): No changes required for daily log or `_general` features. If the skill contains stale examples that assume `Path('.memory')`, leave them out of this change unless they directly conflict with the new daily-log or `_general` behavior.

## Success Criteria

- An agent can close a session when not inside any project -- the record lands in `_general` and appears in the daily log.
- An agent booting into any project sees cross-project activity from the daily log in its boot packet.
- Running `codies-memory list daily-log --scope global --agent claude` shows daily log files.
- The daily log is human-readable and scannable without tooling.
- `create` and `capture` without a resolved project vault route project-scoped records to `_general`; `status`, `boot`, `validate`, and `list` do not silently route to `_general`.
- `reflection`, `dream`, `skill`, `playbook`, and other global-scoped records still write to the global vault and log daily entries with project slug `global`.
- Validation passes for a legacy global vault with no `sessions/` directory, passes for an empty `sessions/` directory, and validates any daily-log markdown files once present.

## Acceptance Tests

- `test_init_global_creates_general_project`: `codies-memory init --type global --agent testbot` creates `projects/_general/` with the normal project-vault directories, registers slug `_general`, and omits `working_dir` and `git_remote` keys from that registry entry.
- `test_user_cannot_init_reserved_general_slug`: direct project initialization with slug `_general` fails clearly and does not overwrite the reserved default project.
- `test_create_without_project_routes_to_general`: in a working directory with no marker, registry match, or git remote match, `create session --short ...` writes the session under `projects/_general/sessions/` and appends one daily-log entry tagged `(_general)`.
- `test_capture_without_project_routes_to_general`: in the same no-project condition, `capture --short ...` writes an inbox item under `projects/_general/inbox/` and appends one daily-log entry tagged `(_general)`.
- `test_status_boot_validate_list_do_not_fallback`: the non-creating commands report no resolved project vault in a no-project directory and do not silently read or write `projects/_general/`.
- `test_global_scoped_records_stay_global`: global-scoped records such as `reflection` or `dream` write to the global vault, not `_general`, and append daily-log entries tagged `(global)`.
- `test_short_sanitization_and_storage`: `--short` strips leading/trailing whitespace, collapses internal newlines to spaces, truncates to 120 characters, is stored in record frontmatter, and is the exact value used in the daily-log line.
- `test_daily_log_frontmatter_and_append`: first write creates `sessions/YYYY-MM-DD.md` with `id: DL-YYYYMMDD`, `type: daily-log`, local-offset ISO timestamps, and append-only body; second write appends exactly one line without rewriting frontmatter.
- `test_daily_log_validation_modes`: validation passes when `sessions/` is absent, passes when it exists but is empty, and validates present daily-log markdown files as `daily-log` records.
- `test_boot_includes_latest_daily_log_tail`: boot renders a `Global Daily Log` subsection using only the newest `DAILY_LOG_TAIL_LINES` entries and drops older daily-log lines before dropping the latest project session when budget pressure exists.
- `test_promote_and_supersede_do_not_log`: promotion and supersede paths create no daily-log entries because they bypass the CLI-layer auto-link wrapper.
- `test_append_uses_single_append_write`: the append helper uses `os.open(... O_APPEND ...)` and one `os.write` call per encoded entry, or a test-visible equivalent one-append-write implementation.

## Scope Boundaries

- The daily log is append-only. Frontmatter is write-once, body is append-only. No editing, compaction, or aging.
- No changes to the promotion system -- daily logs are not promotable.
- No changes to the trust pipeline -- daily logs are `trust: canonical` (ground truth log) but not part of the speculative->confirmed pipeline.
- `promote` and `supersede_record` do not trigger the daily log -- they call `create_record` directly, not the CLI-layer logging wrapper.

## Key Decisions

- **Auto-fallback to `_general`**: When no project vault resolves, `create` and `capture` fall through to `_general`. `resolve_project_vault` still returns None; the `_resolve_project_vault` CLI helper constructs the `_general` path from the global vault. Commands that don't create records (`status`, `boot`, `validate`, `list`) do not fallback -- they report the resolved vault.
- **Eager new-vault default plus lazy legacy repair**: New `init --type global` runs create `_general` immediately. Existing global vaults are repaired lazily when `create` or `capture` first needs `_general`, so no migration command is required before the feature can be used.
- **CLI-layer integration point**: Daily log appending lives in the CLI command handlers, not in `create_record()`. This keeps `create_record` pure (no global vault dependency) and naturally excludes promote/supersede from daily logging. The integration point is `append_daily_log()` called by `cmd_create` and `cmd_capture`.
- **`daily-log` as distinct type**: Daily log files use `type: daily-log`, not `type: session`. This avoids collision with project session records and makes the type system honest about the structural difference.
- **`short` as frontmatter field**: Stored on the record for searchability. Primarily used by the daily log, but available for QMD and other contexts.
- **Write-once frontmatter**: Daily log frontmatter is set once on creation (`updated` included but set to same value as `created`, never bumped). Body-only appending means no read-modify-write, no race conditions on frontmatter.
- **Lazy `sessions/` directory**: Created on first daily log write, not during `init_global_vault`. Avoids breaking `validate_vault` on existing vaults.

## Dependencies / Assumptions

- Existing tests (188) must continue passing -- all changes are additive.
- `sessions/` directory is created lazily, so existing global vaults need no migration.
- `_general` is created eagerly for new global vaults and lazily repaired for existing global vaults on first fallback write, so existing global vaults need no migration.
- `_general` slug is reserved. `init_project_vault` should reject user attempts to create a project with this slug.
- QMD collection for `claudes-codies-memory` will automatically pick up the new `sessions/` directory on next reindex.
- Thread safety: daily log entries are single lines (~100-200 bytes). Implement the append path with a single byte write using `os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o644)` and `os.write(fd, encoded_line)` or an equivalent helper that demonstrably performs one append write per entry. Do not rely on a buffered `TextIOWrapper.write()` call as the atomicity guarantee. This is an acceptable local-file risk; no cross-host locking is required.

## Outstanding Questions

### Deferred to Implementation Verification

- [Affects R7][Technical] Verify in tests that `vault.name` reliably gives the project slug for all supported vault layouts. Edge case: `_general` itself -- `vault.name` yields `_general` which is correct for daily log attribution. Global-scoped records where vault IS the global vault use `"global"` as the slug.

## Next Steps

-> /ce:plan for structured implementation planning
