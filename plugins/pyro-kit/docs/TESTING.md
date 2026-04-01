# Pyro Kit Testing Guide

Testing instructions for the Pyro Kit MVP. This covers what to test, how to test it, what to look for, and how to report feedback.

---

## Setup

### Prerequisites

- Claude Code CLI with plugin support
- A git repository with some commit history (for `/pulse` to analyze)
- bash, git

### Install the plugin

For testing, load the plugin directly:

```bash
claude --plugin-dir /path/to/pyro-kit
```

Or for persistent install (from inside Claude Code):

```
/plugin marketplace add /path/to/pyro-kit
/plugin install pyro-kit@pyro-kit
```

### Clean slate (optional)

To test from scratch, remove prior state:

```bash
rm -rf .pyro/
rm -rf ~/.pyro/
```

---

## Test Plan

### Test 1: /pyro init — Fresh Project

**Steps:**
1. Navigate to a git repo without `.pyro/`
2. Run `/pyro init`

**Expect:**
- `~/.pyro/` created with: `config.yaml`, `project-registry.yaml`, `fascination-index.md`, `autopsies/`, `patterns/`
- `.pyro/` created with: `state.md`, `config.yaml`, `pulse-log.md`, `session-notes/`
- Project registered in `~/.pyro/project-registry.yaml` with correct path, name, status: active, phase: 0

**Check:**
- [ ] `cat ~/.pyro/config.yaml` — has `dormancy_threshold_days: 5` and 3 other settings
- [ ] `cat ~/.pyro/project-registry.yaml` — entry has `path:` matching `pwd`, `name:` matching dir name
- [ ] `cat .pyro/state.md` — frontmatter has all fields (project, phase, status, soul, original_spark, last_skill, last_activity, momentum, gate_history, pulse_count)
- [ ] `cat ~/.pyro/fascination-index.md` — starts with `---\nentries: []\n---` (YAML frontmatter, not fenced block)

**Report if:**
- Any file is missing or has wrong content
- Registry entry field order doesn't match: path, name, status, phase, last_activity, spark_date, fascinations
- Error messages on stdout/stderr

---

### Test 2: /pyro init — Idempotency

**Steps:**
1. After Test 1, delete `.pyro/state.md` only: `rm .pyro/state.md`
2. Run `/pyro init` again

**Expect:**
- Script detects existing `.pyro/`, checks each artifact
- Reports: "Repaired: created missing .pyro/state.md"
- Other files left untouched

**Check:**
- [ ] Only `state.md` was recreated
- [ ] `pulse-log.md`, `config.yaml`, `session-notes/` still have their original content
- [ ] No duplicate registry entry created

**Report if:**
- Script creates a fresh `.pyro/` instead of repairing
- Existing files are overwritten
- Duplicate registry entries appear

---

### Test 3: /pyro init — Second Project

**Steps:**
1. Navigate to a DIFFERENT git repo
2. Run `/pyro init`

**Expect:**
- New `.pyro/` created in the second repo
- Second entry appended to `~/.pyro/project-registry.yaml`

**Check:**
- [ ] Registry has exactly 2 entries with different paths
- [ ] Global files (`config.yaml`, `fascination-index.md`) not recreated

**Report if:**
- First project's registry entry is overwritten
- Global state is re-initialized

---

### Test 4: /pyro status

**Steps:**
1. In an initialized project, run `/pyro status`

**Expect:**
- Displays: Project, Phase (0), Status (active), Momentum (steady), Last skill (none), Last activity, Pulse count (0)
- No warnings on a fresh project (unless days_since > 5)

**Check:**
- [ ] All fields render correctly from state.md frontmatter
- [ ] If `soul` is empty, no Soul line shown
- [ ] If `gate_history` is empty, no Gate history section

**Report if:**
- Fields are missing or show raw YAML
- Warnings appear incorrectly on fresh projects

---

### Test 5: /pyro (routing)

**Steps:**
1. In a Phase 0 project with no `spark.md`, run `/pyro` (no arguments)

**Expect:**
- Recommends `/spark` with reasoning
- Does NOT ask "what do you want to do?"
- Ends with phase context line

**Check:**
- [ ] Recommendation is concrete and specific
- [ ] No open-ended questions
- [ ] Phase context line present

**Report if:**
- Routing gives wrong recommendation for current state
- Asks Socratic/open-ended questions

---

### Test 6: /pyro list

**Steps:**
1. Run `/pyro list`

**Expect:**
- All 7 phases listed with correct names: Ignition, Exploration, Surface, Contract, Build, Momentum, Lifecycle
- Current phase (0) marked with indicator
- MVP skills marked [Available]: /spark, /pulse, /autopsy, /pyro
- All other skills marked [Planned]

**Check:**
- [ ] Phase names match phase-map.md exactly
- [ ] All planned skills from skill-catalog.md appear
- [ ] Current phase indicator is accurate
- [ ] No skills are listed that don't exist in the catalog

**Report if:**
- Phase names don't match (e.g., "Reckoning" instead of "Momentum")
- Missing skills
- Wrong availability tags

---

### Test 7: /spark — Full Flow

**Steps:**
1. In a Phase 0 project, run `/spark`
2. Provide a vague input: "something about terminal tools bugs me"
3. React to the thumbnails (select one by number, or say "none of these" to get new ones)
4. In the expansion phase, try: "dig deeper" (should dispatch excavator agent)
5. Provide feedback to iterate
6. When satisfied, approve to crystallize

**Expect:**
- 3-5 idea thumbnails generated (not Socratic questions)
- Each thumbnail has: name, one-liner, fascination thread labels
- Expansion shows deeper exploration of selected idea
- "dig deeper" dispatches the excavator agent
- Crystallization writes `.pyro/spark.md` and updates `.pyro/state.md`

**Check:**
- [ ] Thumbnails are concrete proposals, not questions
- [ ] `.pyro/spark.md` has YAML frontmatter with: idea, sparked, domain, original_input, soul, thumbnails_considered, technique_used, fascination_threads
- [ ] `.pyro/state.md` updated: phase still 0, last_skill: spark, last_activity: today, original_spark: the idea sentence
- [ ] `gate_history` has entry: `{gate: "G0", passed: true, notes: "...Idea crystallized..."}`
- [ ] `~/.pyro/project-registry.yaml` entry updated: last_activity matches today
- [ ] If `~/.pyro/fascination-index.md` has entries, they influence thumbnail generation

**Report if:**
- Thumbnails are generic or don't relate to your input
- Asks "what kind of project?" or similar Socratic questions
- State files missing fields or in wrong format
- gate_history writes a plain string instead of `{gate, passed, notes}` object
- Registry `last_activity` not updated

---

### Test 8: /spark — Resume Flow

**Steps:**
1. After crystallizing, run `/spark` again in the same project

**Expect:**
- Detects existing `spark.md`
- Offers to view/refine existing spark, or start fresh

**Check:**
- [ ] Does not silently overwrite existing spark
- [ ] Existing spark content is preserved if user chooses to keep it

---

### Test 9: /spark — Fascination Threading

**Steps:**
1. Create a fake fascination index: edit `~/.pyro/fascination-index.md` and add an entry in the frontmatter
2. Run `/spark` in a new project

**Expect:**
- /spark reads the fascination index
- Fascination themes subtly influence thumbnail generation (mentioned as thread labels)
- Tone: "you've been fascinated by X" not "based on your data"

**Check:**
- [ ] Fascination themes appear in thumbnails
- [ ] Natural language, not clinical

**Report if:**
- Fascinations are ignored entirely
- Tone feels like data analysis rather than creative nudge

---

### Test 10: /pulse — Full Dashboard

**Steps:**
1. In a project with `spark.md` and some git history (10+ commits over several days)
2. Run `/pulse`

**Expect:**
- Full 8-section dashboard renders:
  1. Header (project name, phase, days active, pulse count)
  2. Activity (sparkline, daily average, days since last commit, longest gap)
  3. Novelty Depletion Signal (create/maintain ratios, trend bar, interpretation)
  4. Progress (TODO/FIXME/HACK counts, rough percentage range)
  5. Original Spark (verbatim quote from spark.md)
  6. Three Paths (Push, Pivot, Shelve — each with first step, effort, preserved, lost)
  7. Recommendation (cited evidence)
  8. Response prompt (verbatim: "Which path? Say `push`, `pivot`, `shelve`, or `not now`.")

**Check:**
- [ ] Header has NO emoji (no fire emoji before "Pulse")
- [ ] Sparkline uses only these characters: `.` `_` `-` `=` `#`
- [ ] Novelty signal shows create/maintain percentages and trend bars
- [ ] Original spark is quoted VERBATIM from spark.md `idea` field
- [ ] Three paths have project-SPECIFIC first steps (not generic)
- [ ] Recommendation cites a specific signal from the dashboard
- [ ] Response prompt is the LAST thing — nothing follows it

**Report if:**
- Any section is missing or out of order
- Dashboard has emoji in header
- Spark is paraphrased instead of quoted
- Paths have generic advice ("review the codebase")
- Recommendation doesn't cite evidence

---

### Test 11: /pulse — Response Handling

**Steps:**
1. After seeing the dashboard, respond with each option:

**Test "push":**
- [ ] Records push decision in pulse-log.md
- [ ] Updates state.md: momentum, last_skill, last_activity, increments pulse_count
- [ ] Does NOT change phase

**Test "pivot":**
- [ ] Records pivot decision
- [ ] Updates state similarly

**Test "shelve":**
- [ ] Records shelve decision in pulse-log.md
- [ ] Sets momentum to "stalled" (NOT "declining", NOT terminal)
- [ ] Does NOT set status to "shelved" or phase to 6
- [ ] gate_history gets: `{gate: "G6", passed: true, notes: "...Shelve decision..."}`
- [ ] Tells you to run `/autopsy`

**Test "not now":**
- [ ] Dashboard was ALREADY shown (no fast exit before dashboard)
- [ ] No decision recorded in pulse-log.md
- [ ] State unchanged except maybe last_activity

**Report if:**
- Shelve sets terminal state (status: shelved or phase: 6)
- "not now" skips the dashboard
- gate_history writes a string instead of object
- pulse-log.md entry is missing or malformed

---

### Test 12: /pulse — Minimal Git History

**Steps:**
1. In a project with < 5 commits
2. Run `/pulse`

**Expect:**
- Dashboard still renders
- Activity section notes limited data
- Novelty signal may show "insufficient data"
- Still shows all three paths and recommendation

**Check:**
- [ ] No crashes or empty sections
- [ ] Graceful handling of sparse data

---

### Test 13: /pulse — No Git Repo

**Steps:**
1. In a directory that is NOT a git repo (with `.pyro/state.md` present)
2. Run `/pulse`

**Expect:**
- Activity, Novelty Depletion, Progress sections note "No git history found"
- Still shows spark, three paths, recommendation based on available data

**Check:**
- [ ] No error/crash from git-activity.sh
- [ ] Dashboard renders with available sections

---

### Test 14: /autopsy — Full Flow

**Steps:**
1. In a project that had `/pulse shelve` recorded
2. Run `/autopsy`

**Expect:**
- Reads full project state, spark, git history
- Generates 9-section autopsy report:
  1. Header, 2. Timeline, 3. Trajectory, 4. Cause of Death, 5. What Worked,
  6. What Didn't, 7. Fascinations, 8. Transplant Candidates, 9. Epitaph
- Abandonment cause from taxonomy (novelty depletion, scope creep, taste gap, technical wall, new shiny thing, drift)
- Fascinations extracted using 5-lens method (Domain, Mechanic, Aesthetic, Tension, Emotional Register)

**Check:**
- [ ] Report written to `~/.pyro/autopsies/{project-name}.md`
- [ ] `~/.pyro/fascination-index.md` updated with new entries (YAML frontmatter format, not fenced block)
- [ ] `~/.pyro/project-registry.yaml` entry updated: status: composted, phase: 6
- [ ] `.pyro/state.md` updated: status: composted, phase: 6, momentum: composted
- [ ] gate_history gets: `{gate: "G7", passed: true, notes: "...Autopsy completed..."}`
- [ ] Registry entry has ALL fields: path, name, status, phase, last_activity, spark_date, fascinations

**Report if:**
- Fascination index created with fenced YAML block instead of frontmatter
- Registry entry missing fields or in wrong order
- State not updated to terminal (composted)
- Abandonment cause doesn't match the project's actual signals

---

### Test 15: /autopsy — Fascination Loop

**Steps:**
1. After completing autopsy in Test 14, go to a NEW project
2. Run `/pyro init`, then `/spark`

**Expect:**
- `/spark` reads the fascination index (now populated from autopsy)
- Fascination themes influence new thumbnails
- The loop is closed: dead project feeds new ideas

**Check:**
- [ ] Fascinations from the autopsied project appear as thread labels
- [ ] New thumbnails connect to old fascinations where relevant

**Report if:**
- Fascination index is not read
- Parse errors from the index format

---

### Test 16: Session Hook — Dormancy Detection

**Steps:**
1. Edit `~/.pyro/project-registry.yaml`: set one project's `last_activity` to 30 days ago
2. Start a new Claude Code session in that project's directory

**Expect:**
- Session hook fires, detects dormancy
- Injects context suggesting `/pulse` check-in

**Check:**
- [ ] Dormancy message appears in session context
- [ ] Threshold matches `~/.pyro/config.yaml` `dormancy_threshold_days`

**Report if:**
- No dormancy detection despite stale last_activity
- Hook crashes or times out (2s timeout)

---

### Test 17: Session Hook — Cross-Project Dormancy

**Steps:**
1. Have 2 projects registered
2. Set project A's `last_activity` to 20 days ago
3. Start a session in project B

**Expect:**
- Hook detects project A is dormant
- Mentions project A in additional context

**Check:**
- [ ] Dormant project A is named in the context
- [ ] Current project (B) is NOT flagged as dormant

---

### Test 18: git-activity.sh — Direct Script Test

**Steps:**
```bash
bash pyro-kit/scripts/git-activity.sh 30
```

**Expect:**
- Structured output with sections: OVERVIEW, BRANCHES, COMMIT_FREQUENCY, FILE_ACTIVITY, MESSAGE_SENTIMENT, NEW_REPOS
- COMMIT_FREQUENCY has a `trend:` field (increasing/stable/declining/insufficient_data)

**Check:**
- [ ] `trend:` field present in COMMIT_FREQUENCY section
- [ ] Conventional commits (`feat:`, `fix:`, `refactor:`) classified correctly (not as `other`)
- [ ] `create_ratio` and `maintain_ratio` sum reasonably (with `other_ratio`)
- [ ] No errors on invalid input: `bash pyro-kit/scripts/git-activity.sh abc` (should default to 30 days)
- [ ] No errors with zero: `bash pyro-kit/scripts/git-activity.sh 0` (should default to 30)

**Report if:**
- `trend:` field missing
- `feat:` commits counted as `other` in MESSAGE_SENTIMENT
- Division by zero errors
- Script crashes on non-numeric input

---

### Test 19: git-activity.sh — Non-Git Directory

**Steps:**
```bash
cd /tmp && bash /path/to/pyro-kit/scripts/git-activity.sh 30
```

**Expect:**
- Clean structured output with zero values
- `not_a_git_repo: true` in OVERVIEW
- Exit code 0 (not error)

**Check:**
- [ ] No error messages to stderr
- [ ] Exit code is 0
- [ ] All sections present with zero/empty values

---

### Test 20: Excavator Agent

**Steps:**
1. During `/spark` expansion phase, say "dig deeper"

**Expect:**
- Excavator agent dispatched
- Returns 6-section output: Prior Art Awareness, Day in the Life, Use Case Spectrum, Technical Feasibility, Surprising Connections, Kill Conditions
- Does NOT perform web searches

**Check:**
- [ ] Prior Art section uses existing knowledge, not web results
- [ ] No WebSearch or WebFetch tool calls in agent execution
- [ ] Output enriches the expansion without being prescriptive

**Report if:**
- Agent tries to web search (tool should not be in its allowed list)
- Output is generic market research rather than idea enrichment

---

## Edge Cases to Exercise

| Scenario | What to try | What should happen |
|----------|------------|-------------------|
| Empty input to /spark | Just say "/spark" with no feeling | Should prompt for input or propose from fascinations |
| Very long spark | Provide a 500-word rambling input | Thumbnails should distill, not echo |
| /pulse on day 1 | Run immediately after init + spark | Should handle gracefully with minimal data |
| Rapid /pulse spam | Run /pulse 3 times in a row | pulse_count increments, log appends each time |
| /autopsy without /pulse shelve | Run /autopsy on an active project | Should work (autopsy isn't gated on pulse) |
| Unicode in project name | Init in a dir with spaces/unicode | Scripts should handle with quoting |
| Concurrent projects | Init 5+ projects, switch between them | Registry tracks all, no cross-contamination |

---

## Feedback Format

When reporting issues, include:

```
**Skill**: /spark | /pulse | /autopsy | /pyro | scripts
**Test #**: (from this doc)
**Steps**: What you did
**Expected**: What should have happened
**Actual**: What actually happened
**Files**: Any relevant state file contents (state.md, spark.md, etc.)
**Severity**:
  - P0: Broken — skill doesn't work at all
  - P1: Wrong — works but produces incorrect output
  - P2: Drift — works but doesn't match spec/docs
  - P3: Polish — works correctly but could be better
```

---

## Known Limitations (MVP)

- **No validation on state.md edits**: If you manually edit state.md with invalid YAML, skills may behave unexpectedly
- **Soft gating only**: Gates warn but never block — you can run any skill in any phase
- **Single-user**: No multi-user or team support
- **Local state only**: `.pyro/` and `~/.pyro/` are filesystem-based, no cloud sync
- **Planned skills**: 20+ skills show as [Planned] in `/pyro list` — they're roadmap items, not stubs
- **Fascination index is append-heavy**: Over many projects, the index may grow large — no pruning yet
- **git-activity.sh assumes main branch**: Cross-branch analysis is limited
