# Skill Authoring Checklist

Validate any new skill against this checklist before merging. Every checkbox must pass unless explicitly noted as optional.

---

## 1. PICS+Workflow Format

- [ ] SKILL.md has YAML frontmatter with: name, description, user-invocable, argument-hint, allowed-tools
- [ ] Skill follows PICS structure: ## Persona, ## Interface, ## Constraints, ## State
- [ ] ## Workflow section exists with clear control flow
- [ ] Constraints section has both `require {}` and `never {}` blocks
- [ ] Interface section has `fn` signatures for all public commands

## 2. Context Budget

- [ ] SKILL.md is under 500 lines (target, not hard limit)
- [ ] Tier 2 (typical invocation) context is under 1500 lines total
- [ ] Tier 2 = SKILL.md lines + preprocessor output + largest commonly-loaded reference file
- [ ] Reference files are loaded on-demand in workflow, not all at once
- [ ] Reference: see `docs/context-budget-audit.md` for measurement methodology

## 3. Reference Files

- [ ] Maximum 2-3 reference files per skill
- [ ] Each reference file has a clear single purpose
- [ ] Reference files are loaded only when needed in the workflow (not all upfront)
- [ ] Reference file paths use `${CLAUDE_PLUGIN_ROOT}` for portability

## 4. State Files

- [ ] Any .pyro/*.md files written conform to schemas in `docs/schemas/state-files.md`
- [ ] No existing schema fields are renamed or removed (FND-01 freeze policy)
- [ ] New fields added as optional with defaults only
- [ ] Producer/consumer relationship documented in schema file if writing new state

## 5. Skill Catalog Integration

- [ ] Skill appears in `skills/pyro/reference/skill-catalog.md` with all fields
- [ ] Skill appears in `skills/pyro/reference/phase-map.md` under correct phase
- [ ] /pyro list command in `skills/pyro/SKILL.md` includes the skill
- [ ] All three references are consistent (same name, same description)
- [ ] If this skill replaces old skills, the "Replaces" note is present in catalog

## 6. Interaction Pattern

- [ ] First output is always a concrete proposal, never a question (propose-react-iterate)
- [ ] No Socratic questioning ("what do you think?", "how would you...?")
- [ ] No "imagine if..." prompts (freezes the target user)
- [ ] No brainstorming technique menus (meta-decision delays actual work)

## 7. Preprocessor

- [ ] If skill reads .pyro/state.md, uses shell preprocessor: `!` backtick block
- [ ] Preprocessor output is minimal (just the state needed, not full file dumps)
- [ ] Handles missing state gracefully (e.g., "NO_PROJECT_STATE" sentinel)

## 8. Directory Structure

- [ ] Skill lives in `skills/{name}/SKILL.md`
- [ ] Reference files in `skills/{name}/reference/*.md`
- [ ] No files outside the skill's directory (except shared infrastructure)

---

## Foundation Notes

- **FND-02 (SFD wrapper PoC):** Deferred to Phase 3. Skills that wrap SFD phases (/surface, /contract, /build) should not be authored until the Phase 3 PoC validates the wrapper pattern.
- **FND-03 (Interleaving):** When planning new skill work, interleave novel creative skills with mechanical infrastructure to prevent meta-abandonment.
