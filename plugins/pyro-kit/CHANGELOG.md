# Changelog

## [0.1.0] - 2026-03-12

### Added
- Plugin scaffold: manifest, hooks, scripts, skills, agents directories
- `/pyro` skill — lifecycle navigator with init, status, list, and routing subcommands
- `/spark` skill — Phase 0 idea excavation using propose-react-iterate
- `/pulse` skill — momentum dashboard with git analysis, novelty depletion, and push/pivot/shelve paths
- `/autopsy` skill — value extraction and composting for shelved/dead projects
- Excavator agent — deep pre-idea exploration dispatched by /spark
- `pyro-init.sh` — initializes `~/.pyro/` global state and `.pyro/` project state
- `session-init.sh` — SessionStart hook for dormancy detection and context injection
- `git-activity.sh` — git history analyzer for commit frequency, sentiment, and branch health
- Reference files: phase-map, skill-catalog, techniques, domain-lenses, thumbnail-format, spark-output-format, fascination-reading-guide, dashboard-format, report-template
- README and testing guide

### Fixed (post-review)
- `/pyro init` uses `${CLAUDE_PLUGIN_ROOT}` for portable script path resolution
- `gate_history` entries use `{gate, passed, notes}` object format across all skills (was plain strings)
- `/autopsy` creates fascination-index.md with YAML frontmatter (was fenced code block)
- `/pulse` shelve no longer sets terminal state — records G6 gate, sets momentum to stalled, defers terminal state to `/autopsy`
- `/pulse` "not now" is only valid after dashboard renders (was allowing fast exit before dashboard)
- `/spark` updates `~/.pyro/project-registry.yaml` `last_activity` on crystallize
- `git-activity.sh` correctly classifies conventional commits (`feat:`, `fix:`, `refactor:`, etc.)
- `git-activity.sh` validates `WINDOW_DAYS` parameter (prevents division by zero)
- `git-activity.sh` emits `trend:` field in COMMIT_FREQUENCY section
- `pyro-init.sh` repairs individual missing artifacts instead of skipping existing `.pyro/`
- `session-init.sh` emits warning when state.md can't be parsed (was silent exit)
- `/pyro list` phase names aligned with canonical phase-map.md
- Dashboard header uses plain text (removed emoji conflicting with ASCII constraint)
- Autopsy report template phase names aligned with phase-map.md
- Autopsy report template uses `git log` consistently (was referencing `git-activity.sh 99999`)
- Plugin manifest description accurately reflects 4-skill MVP scope
- Excavator agent uses existing knowledge only (removed web search per PRD constraint)
- SDD updated: added pyro-init.sh to directory map, spark.md and pulse-log.md schemas, fascination-index canonical schema, /spark reference file documentation, original_spark semantics clarification
