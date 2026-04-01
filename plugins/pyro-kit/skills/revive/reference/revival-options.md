# Revival Options -- Output Templates

This file defines the output format for each of the four /revive options. Loaded
at execute(choice) time -- not upfront. Each template specifies the exact structure
for the chosen option's output.

---

## Option 1: Full Revival

Produce a concrete re-entry plan. The developer should be able to start working
immediately after reading this.

```
# Re-Entry Plan -- {projectName}

**Path:** Full Revival
**Resume at:** Phase {phase} -- {phase_description}

## First 3 Things to Fix/Update

1. **{item}** (`{file_path}`): {what to do and why}
2. **{item}** (`{file_path}`): {what to do and why}
3. **{item}** (`{file_path}`): {what to do and why}

## Estimated Effort

**To get back to working state:** {N} hours
  - {breakdown item}: {hours}
  - {breakdown item}: {hours}

**To reach next milestone:** {N} hours
  - {milestone description}

## Risks (What Might Have Rotted)

- **Dependencies**: {specific packages or versions that may have updated}
- **APIs**: {external services or interfaces that may have changed}
- **Assumptions**: {design decisions that may no longer hold}

## Next Step

Start with item 1 above. Run `/pulse` after your first session back to
establish a momentum baseline.
```

**State updates (if .pyro/state.md exists):**
- `last_skill: revive`
- `last_activity: {today}`
- `status: active`
- `momentum: steady`

---

## Option 2: Soul Transplant

Produce a new spark.md derived from the original fascination. The spark.md MUST
conform to the state-files.md schema exactly.

**Fascination extraction:** Use the 5-lens detection method from
`skills/autopsy/reference/report-template.md` (Fascination Extraction Guide section):

1. **Lens A -- DOMAIN**: What field or problem space?
2. **Lens B -- MECHANIC**: What interaction or technical mechanic is interesting?
3. **Lens C -- AESTHETIC**: What visual or experiential quality was being pursued?
4. **Lens D -- TENSION**: What interesting problem or contradiction?
5. **Lens E -- EMOTIONAL REGISTER**: What feeling was being designed for?

**Reframing rule:** The transplanted idea is about the FASCINATION, not the old
implementation. "A CLI tool that watches files" becomes "The pull toward making
computers notice what humans care about."

**spark.md output format (exact schema):**

```yaml
---
idea: "{transplanted idea -- reframed around fascination}"
sparked: {today YYYY-MM-DD}
fascination_threads: ["{thread1}", "{thread2}"]
thumbnails_considered: 0
iterations: 0
---

## The Idea
{2-3 paragraphs: what the transplanted thing IS, not what it does.
Reframed around the fascination, not the old implementation.}

## Why This
{Why this direction, drawing from:
- Original fascination threads
- Lessons from what went wrong in the original
- What the developer kept returning to}

## Key Tensions
- {Tension 1: informed by original project's experience}
- {Tension 2}
- {Tension 3}

## Original Input
"[Soul transplant from {projectName}]: {original soul statement}"
```

**Confirmation output:**

```
Soul transplanted. New `.pyro/spark.md` written.

**Transplanted idea:** "{idea}"
**Carried forward:** {fascination_threads}
**Sparked:** {today}

Run `/spark` to explore this transplanted idea, or `/explore` to generate
design directions from it.
```

---

## Option 3: Organ Harvest

Write a harvest manifest to `.pyro/harvest.md`. YAML frontmatter for structured
data, matching all other .pyro/ state files.

**harvest.md format:**

```yaml
---
source_project: "{projectName}"
harvested: {today YYYY-MM-DD}
source_path: "{absolute path to original repo}"
artifacts_count: {N}
---

# Harvest Manifest -- {projectName}

Extracted from {projectName} on {today}. Each artifact includes its
original location and extraction instructions.

## Artifacts

### 1. {Artifact Name}
**Source:** `{file path in original repo}`
**What it does:** {description of what this code/pattern does}
**How to extract:** {specific instructions}
  - Copy: just copy the file and its imports
  - Adapt: copy and modify {specific parts} for new context
  - Refactor: extract {specific function/class} from the larger file
**Dependencies:** {what else it needs -- other files, packages, env vars}

### 2. {Artifact Name}
...
```

**Artifact selection criteria:**
- Non-trivial size (not boilerplate)
- Clean enough to extract without major refactoring
- Solves a general problem (not deeply coupled to project-specific logic)
- Has clear boundaries (a module, a utility, a pattern)

**When fewer than 3 artifacts are extractable:** Still write the manifest with
what is available. Note: "This project's value is more in its concept than its
code -- consider Option 2 (Soul Transplant) for the idea itself."

**Confirmation output:**

```
Harvest manifest written to `.pyro/harvest.md`.

**{N}** artifacts documented from **{projectName}**.

Each artifact has extraction instructions. Copy them into your next project
as needed -- the manifest stays here as a reference.
```

---

## Option 4: Let It Rest

Minimal output. No files written. Redirect to /autopsy for proper composting.

**Output (verbatim):**

```
This project has given what it can.

Run `/autopsy` to extract its fascinations into your index. The themes that
drove this work will feed your next project through `/spark`.
```

No additional analysis, no state changes, no files written. The developer
runs /autopsy as a separate invocation if they choose.

---

## Scoring Reference

For the recommendation algorithm, these are the signal weights:

| Signal | Full Revival | Soul Transplant | Organ Harvest | Let It Rest |
|--------|-------------|----------------|---------------|-------------|
| Recent commits (< 90 days) | +3 | 0 | 0 | 0 |
| High codebase maturity | +3 | -3 | +2 | 0 |
| Fascination alignment | +2 | +2 | -1 | -2 |
| Clear re-entry point | +2 | 0 | 0 | 0 |
| Novelty Depletion cause | -3 | +1 | +1 | +1 |
| Taste Gap cause | -2 | +2 | 0 | 0 |
| Technical Wall cause | 0 | +3 | +1 | 0 |
| Scope Creep cause | 0 | +3 | +1 | 0 |
| Drift cause | 0 | 0 | 0 | +2 |
| 3+ extractable modules | 0 | 0 | +3 | 0 |
| Last commit > 180 days | -2 | 0 | 0 | +2 |
| No fascination alignment | -1 | -1 | +2 | +3 |

**Tie-break order:** Full Revival > Soul Transplant > Organ Harvest > Let It Rest

The tie-break reflects a bias toward action over closure -- when signals are
ambiguous, prefer revival over composting.
