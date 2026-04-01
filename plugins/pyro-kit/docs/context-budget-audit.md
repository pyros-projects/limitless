# Context Budget Audit

Measured context budgets for all MVP skills and agents. All measurements are actual line counts from source files using `wc -l`.

## Summary Table

| Skill | SKILL.md | Preprocessor | Tier 1 (Always) | Tier 2 (Typical) | Tier 3 (Maximum) | Under Budget? |
|-------|----------|-------------|------------------|-------------------|-------------------|---------------|
| /spark | 339 | ~15 | 354 | 489 | 965 | Yes |
| /pulse | 409 | ~60 | 469 | 812 | 812 | Yes |
| /autopsy | 479 | ~15 | 494 | 1050 | 1050 | Yes |
| /pyro | 243 | ~15 | 258 | 359 | 575 | Yes |
| excavator | 108 | 0 | 108 | 108 | 108 | Yes |

All MVP skills are under the 1500-line Tier 2 budget.

## Budget Rule

Per INF-02, the budget target is **less than 1500 lines per invocation measured at Tier 2** (typical invocation). Tier 2 represents what is actually loaded during a normal workflow path: the SKILL.md, preprocessor output, and the reference files that are commonly loaded during a typical session.

Any skill exceeding 1500 lines at Tier 2 must be split or have reference files restructured before shipping.

**Current status:** All 5 MVP skills/agents are well within budget. The highest Tier 2 cost is `/autopsy` at 1050 lines (70% of budget).

## Measurement Method

Context budget is measured in three tiers to reflect the on-demand loading model of Claude Code skills:

**Tier 1 -- Always Loaded:** SKILL.md file + shell preprocessor output. This is loaded every time the skill is invoked, regardless of workflow path.

**Tier 2 -- Typical Invocation:** Tier 1 + the reference files loaded during a normal workflow path. Most skills load 1-2 reference files during typical use, not all of them. This is the budget target because it represents actual cost during real use.

**Tier 3 -- Maximum:** Tier 1 + ALL reference files if every workflow branch is taken. This is the theoretical ceiling. It would require the user to trigger every possible feature path in a single session.

### Why Tier 2 is the budget target

Reference files are loaded on-demand via `@reference/filename.md` patterns in SKILL.md workflow sections. They are only loaded when the workflow reaches a branch that needs them. Budgeting against Tier 3 would over-count by assuming every reference file is loaded simultaneously, which does not reflect real usage.

### Preprocessor output

Shell preprocessor commands (`!` backtick blocks in SKILL.md) execute before the skill runs and inject their stdout into the context. The output size depends on the current project state. Estimates below use a typical project with an initialized `.pyro/state.md` (~15 lines) and for `/pulse`, an additional `git-activity.sh` output (~45 lines).

---

## /spark

**SKILL.md:** 339 lines
**Preprocessor:** `cat .pyro/state.md` -- ~15 lines (state.md frontmatter + body)

### Reference Files

| File | Lines | Loaded When |
|------|-------|-------------|
| `thumbnail-format.md` | 49 | During `excavate()` -- always in a typical session |
| `spark-output-format.md` | 86 | During `crystallize()` -- always in a typical session |
| `fascination-reading-guide.md` | 78 | During `excavate()` if fascination index exists |
| `techniques.md` | 147 | During `excavate()` for technique selection |
| `domain-lenses.md` | 251 | Only if fascination threading activates cross-domain reframing |
| **Total reference** | **611** | |

### Tier Breakdown

- **Tier 1 (Always):** 339 + 15 = **354 lines**
- **Tier 2 (Typical):** 354 + 49 (thumbnail-format) + 86 (spark-output-format) = **489 lines**
  - A typical `/spark` session generates thumbnails (needs format guide) and crystallizes (needs output format). Fascination reading and techniques are commonly loaded too, which would bring typical to 702 lines -- still well under budget.
- **Tier 3 (Maximum):** 354 + 611 (all reference files) = **965 lines**

---

## /pulse

**SKILL.md:** 409 lines
**Preprocessor:** `cat .pyro/state.md` (~15 lines) + `git-activity.sh 30` output (~45 lines) = ~60 lines

### Reference Files

| File | Lines | Loaded When |
|------|-------|-------------|
| `dashboard-format.md` | 343 | During `dashboard()` -- always loaded (the dashboard is the primary output) |
| **Total reference** | **343** | |

### Tier Breakdown

- **Tier 1 (Always):** 409 + 60 = **469 lines**
- **Tier 2 (Typical):** 469 + 343 (dashboard-format) = **812 lines**
  - The dashboard is always rendered, so Tier 2 equals Tier 3 for `/pulse`.
- **Tier 3 (Maximum):** 469 + 343 = **812 lines**

Note: `git-activity.sh` itself (the script file) is NOT loaded into context -- only its stdout output is injected via the shell preprocessor. The ~45 line estimate is for a project with 30 days of git history.

---

## /autopsy

**SKILL.md:** 479 lines
**Preprocessor:** `cat .pyro/state.md` -- ~15 lines

### Reference Files

| File | Lines | Loaded When |
|------|-------|-------------|
| `report-template.md` | 556 | During `report()` -- always loaded (the report is the primary output) |
| **Total reference** | **556** | |

### Tier Breakdown

- **Tier 1 (Always):** 479 + 15 = **494 lines**
- **Tier 2 (Typical):** 494 + 556 (report-template) = **1050 lines**
  - The report template is always loaded since the report is the skill's primary output. Tier 2 equals Tier 3.
- **Tier 3 (Maximum):** 494 + 556 = **1050 lines**

`/autopsy` has the highest Tier 2 cost at 1050 lines (70% of budget). If expansion adds more reference files, this skill will need careful budget management.

---

## /pyro

**SKILL.md:** 243 lines
**Preprocessor:** `cat .pyro/state.md` -- ~15 lines

### Reference Files

| File | Lines | Loaded When |
|------|-------|-------------|
| `skill-catalog.md` | 216 | During `list` command |
| `phase-map.md` | 101 | During `route()` for phase name resolution |
| **Total reference** | **317** | |

### Tier Breakdown

- **Tier 1 (Always):** 243 + 15 = **258 lines**
- **Tier 2 (Typical):** 258 + 101 (phase-map) = **359 lines**
  - A typical `/pyro` invocation routes the developer to the next skill, using `phase-map.md` for phase context. The `skill-catalog.md` is only loaded for the explicit `list` command.
- **Tier 3 (Maximum):** 258 + 317 (all reference files) = **575 lines**

`/pyro` is the lightest skill at Tier 2 (359 lines), which is appropriate for an orchestrator that should load quickly.

---

## excavator (Agent)

**Agent file:** 108 lines (`agents/excavator.md`)
**Preprocessor:** None (agents do not have shell preprocessors)
**Reference files:** None

### Tier Breakdown

- **Tier 1 (Always):** **108 lines**
- **Tier 2 (Typical):** **108 lines**
- **Tier 3 (Maximum):** **108 lines**

The excavator is a sub-agent spawned by `/spark` during the `expand()` workflow when the developer requests a deep exploration ("dig deeper"). It has no reference files of its own.

---

## Budget Health Summary

| Metric | Value |
|--------|-------|
| Skills under budget (Tier 2 < 1500) | 5/5 |
| Highest Tier 2 | /autopsy at 1050 lines (70%) |
| Lowest Tier 2 | excavator at 108 lines (7%) |
| Average Tier 2 | 564 lines (38%) |
| Total Tier 3 ceiling (all skills combined) | 3510 lines |

No skills require restructuring. The budget provides headroom for expansion-phase additions to reference files.
