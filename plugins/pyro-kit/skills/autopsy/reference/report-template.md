# Autopsy Report Template

This file defines the exact structure and content of the `/autopsy` report. Every
`/autopsy` invocation produces this report. Follow this spec exactly — section order,
labels, and formatting are load-bearing because the report is both a closure ritual
and a knowledge extraction artifact.

---

## How to Generate the Report

1. Use `git log --oneline --all` for commit history analysis (or `git-activity.sh` if available).
   Parse the output for timeline, frequency, and sentiment signals.
2. Read `.pyro/spark.md` for idea, sparked date, and fascination_threads. Fall back to
   README and first commit messages if absent.
3. Read `.pyro/state.md` for phase, project name, and last momentum reading.
4. Read `.pyro/pulse-log.md` if it exists — prior pulse entries give timeline context.
5. Scan commit messages for the inflection point where frequency declined.
6. Diagnose the primary abandonment cause using the taxonomy below.
7. Render each section in order. Do not skip sections, even when data is thin.
8. End with the composting note verbatim.

---

## Report Template

Each section below is a required block. Replace `{placeholders}` with real values.

---

### Section 1: Header

```
# Autopsy — {project_name}
**Date**: {today}
**Phase at death**: {phase} ({phase_name})
**Duration**: {first_commit_date} → {last_commit_date} ({days_active} days)
**Commits**: {total_commits}
**Status**: Composted
```

- `project_name`: from `.pyro/state.md` project field, or directory name if absent
- `today`: current date in YYYY-MM-DD format
- `phase`: numeric phase from `.pyro/state.md`; if absent, infer from commit history
- `phase_name`: human name for the phase (e.g., Phase 2 = Explore, Phase 3 = Prototype)
- `first_commit_date` / `last_commit_date`: from git-activity.sh OVERVIEW
- `days_active`: calendar days between first and last commit
- `total_commits`: from git-activity.sh OVERVIEW total_commits

**Phase names reference:**
- Phase 0: Ignition
- Phase 1: Exploration
- Phase 2: Surface
- Phase 3: Contract
- Phase 4: Build
- Phase 5: Momentum
- Phase 6: Lifecycle

---

### Section 2: Soul Statement

```
## Soul Statement
> "{soul statement — verbatim from spark.md idea field, or inferred}"

{1-2 sentences: what made this project compelling, what fascination drove it}
```

- Use the `idea` field from `.pyro/spark.md` frontmatter verbatim if present.
- If absent, infer from README first paragraph or first commit message. Label it:
  `> *[Inferred]* "{statement}"`
- The 1-2 sentences after the blockquote are interpretation, not the spark itself.
  They name the fascination: "This was fundamentally about X."

---

### Section 3: Timeline

```
## Timeline
- **{date}**: {milestone}
```

Show 5-8 key moments, not every commit. Required anchors:
- First commit (project start)
- First working version or major feature shipped
- Highest-activity period (if identifiable from commit density)
- The inflection point — when commit frequency started dropping
- Last commit (death date)

Additional anchors to include when present:
- Significant architecture decision (visible in commit messages)
- A stale branch creation date (signals scope expansion that didn't complete)
- A pulse session, if recorded in `.pyro/pulse-log.md`

The inflection point is the most important entry. Label it explicitly:
`**{date}**: [Inflection] Commit frequency drops — last burst of {N} commits over
{M} days, then silence`

---

### Section 4: What Worked

```
## What Worked
- {specific thing that went well}
```

3-5 items minimum. Each item must be specific enough to be reusable — not "the
architecture was clean" but "the event-driven message bus in `src/events/` decouples
all feature modules cleanly; worth extracting."

Sources for this section:
- Patterns that appear consistently across commits (the developer kept using them)
- Anything the developer over-built (over-building signals fascination and craft)
- Technical decisions that held up without revision
- Commit messages with positive language ("finally got X working", "this feels right")

---

### Section 5: What Killed It

```
## What Killed It
**Primary cause**: {cause from taxonomy}
**Evidence**: {specific signals that indicate this cause}

{1-2 paragraphs: honest but compassionate analysis of why this project stopped}
```

- Select exactly one primary cause from the taxonomy below.
- `Evidence` must cite specific, observable signals — commit dates, TODO counts,
  branch names, commit message language. Never generic.
- The paragraphs are compassionate but honest. They do not reassign blame or
  over-explain. They name what happened and reframe it using the composting language
  from the taxonomy.

---

### Section 6: Reusable Artifacts

```
## Reusable Artifacts
- **{artifact name}** ({file path or description}): {what it does, why it's reusable}
```

Specific code, patterns, configurations, or techniques worth extracting before this
project leaves active memory. Each entry needs enough detail to be actionable — a
path or description the developer can locate months later.

When nothing is clearly reusable, write:
```
## Reusable Artifacts
- **Core concept** (described in Soul Statement): The idea itself is reusable — see
  Extracted Fascinations for where it connects to ongoing threads.
```

Never write "nothing reusable" — there is always something.

---

### Section 7: Extracted Fascinations

```
## Extracted Fascinations
- **{theme-name}**: {description} — Intensity: {high|medium|low}
```

Themes extracted for the fascination index. Each fascination must be:
- Abstract enough to apply across multiple projects
- Specific enough to be meaningful (not just "I like CLIs")
- Named in kebab-case for indexing

**Intensity levels:**
- `high`: developer kept working in this area even when blocked; over-built here;
  returned to it across multiple projects
- `medium`: enjoyed this aspect and built well in it; did not over-invest
- `low`: explored this theme but did not sustain engagement with it

See the Fascination Extraction Guide at the end of this file for detection method.

---

### Section 8: Lessons

```
## Lessons
- {specific lesson learned — actionable, not generic}
```

Concrete takeaways for future projects. Each lesson must pass this test: could it
be pasted into a project plan and actually change a decision? If not, cut it.

Good: "When the scope includes both a CLI and an API, pick one for 0.1 and stub the
other. This project stalled when both needed to be working before anything was usable."

Bad: "Scope carefully next time." (too generic to act on)

2-4 lessons. Quality over quantity.

---

### Section 9: Composting Note

End with this block, verbatim. No variation. No additional questions.

```
---
This project is composted. The work done here feeds what comes next.
```

---

## Abandonment Cause Taxonomy

Each cause includes its definition, detection signals, and a reframe in composting
language. Select the first cause whose detection signals match the evidence. When
multiple causes are present, pick the one most strongly evidenced — the others
can be mentioned briefly in the analysis paragraphs.

---

### 1. Novelty Depletion

**Definition**: The dopamine of building new things wore off. The project entered
maintenance mode — fixing, refactoring, polishing — and the excitement that drove
creation disappeared. This is neurological, not a character flaw.

**Detection signals**:
- `create_ratio` (from git-activity.sh MESSAGE_SENTIMENT) drops below 0.30
- `sentiment_trend` is "declining" in git-activity.sh output
- `first_half_create_ratio` is significantly higher than `second_half_create_ratio`
- Commit frequency dropped after an initial burst, not after hitting a specific blocker
- No single blocked feature visible — project simply stopped

**Example**: Project had 22 commits in the first 8 days, 4 commits in the next 14 days.
No blocked feature. The architecture was done and what remained was wiring and testing.

**Reframe**: "The creative phase completed. What you built during that phase has value
regardless of whether maintenance continues. The burst of creation was the real work."

---

### 2. Scope Creep

**Definition**: The project grew beyond what felt achievable for one person. Features
accumulated, the finish line receded, and the gap between "what exists" and "what's
needed" became demoralizing.

**Detection signals**:
- Multiple stale branches, each representing a feature that was started but not finished
- TODO count grew over time (visible if pulse logs exist) rather than shrinking
- Commit messages shift from features to infrastructure ("refactor X to support Y",
  "need to rethink Z before adding W")
- The original spark describes one thing; the codebase contains many things

**Example**: Started as a single-purpose file watcher. By week 3, branches existed for
a web UI, a plugin system, and a config DSL. The file-watching core was complete but
nothing could ship until the other pieces were done.

**Reframe**: "The vision was bigger than one iteration. The parts that exist are complete
in themselves. Scope cuts aren't failure, they're design decisions made in arrears."

---

### 3. Taste Gap (Ira Glass)

**Definition**: The developer's taste — their sense of what "good" looks like — exceeds
their current ability to execute. The gap between vision and output is painful enough
to stop work. Named for Ira Glass's articulation of the gap every creative person
navigates early in their development.

**Detection signals**:
- The same component was rewritten 2+ times without the scope expanding
- Refactor commits that don't add functionality and appear late in the project's life
- README or planning documents describe something more polished than what the code
  does (the documentation is aspirational, not descriptive)
- Commit messages contain self-critical language ("this is a mess", "wrong approach",
  "starting over")

**Example**: The rendering module was rewritten three times over two weeks. Each version
worked, but none felt right. The project stalled on the fourth attempt.

**Reframe**: "Your taste is an asset, not a problem. The gap means you know what good
looks like — most people don't. Next time, build less and polish it fully to your
standard. A small thing finished beats a large thing perpetually restarted."

---

### 4. Technical Wall

**Definition**: Hit a genuinely hard problem — performance bottleneck, integration
complexity, dependency limitation — that blocked the critical path. Not lack of skill;
the problem was actually hard.

**Detection signals**:
- Commits cluster intensely around one area, then stop
- TODO/FIXME markers concentrate in one module (3+ markers in a single file or area)
- A branch was created to address the blocker and was never merged or closed
- The last commit message references the specific technical problem
- Time between commits grew gradually (attempts continuing) rather than dropping
  suddenly (gave up immediately)

**Example**: Last 11 commits all touch `src/parser/`. Final commit: "TODO: streaming
parser needs backtracking support — current approach won't work for nested blocks."
The parser problem was the critical path; nothing else could ship without it.

**Reframe**: "The wall was real, not imagined. The work done to reach it has genuine
value — you mapped the problem space thoroughly. The approach might work with different
constraints, new tools, or more time. The wall is well-documented."

---

### 5. New Shiny Thing

**Definition**: A more exciting idea appeared and captured attention. The new project
got the creative energy that would have sustained this one. This is the most common
pattern for serial project starters and is value-neutral — following fascination is
how you find what matters.

**Detection signals**:
- New repos appear in project-registry.yaml (if it exists) with `spark_date` during
  this project's active period
- A sibling directory in the projects folder has a first commit date that overlaps
  with this project's declining period
- This project's last commit predates the new project's first commit by less than
  a week
- git-activity.sh `new_repos_detected > 0` during the active window

**Example**: Project's last commit was 2026-02-18. A new project in the same directory
has its first commit on 2026-02-21. The new project has been actively developed since.

**Reframe**: "Following your fascination is how you find what matters. This project
seeded the next one — trace the fascination thread and you'll see the connection.
The question isn't why you left, it's what the new thing was telling you."

---

### 6. Drift

**Definition**: No explicit decision was made. The project just stopped getting worked
on. No dramatic moment, no clear cause — it faded from active memory. This is the
default failure mode when there's no explicit decision system. Drift is not a cause
in the same sense as the others; it's the absence of a decision.

**Detection signals** (Drift is the diagnosis when no other cause fits):
- Long gap between last commit and today (60+ days) with no clear technical blocker
- No stale branches suggesting scope expansion
- `create_ratio` was moderate (0.30-0.50) at last activity, not clearly depleted
- No new sibling projects started immediately after
- `.pyro/state.md` shows "steady" momentum at last check (no crisis visible)
- No `shelve` decision recorded anywhere

**Example**: Project had 31 commits over 6 weeks. Steady pace throughout. No blockers
visible. Last commit 4 months ago. No obvious reason it stopped — it just did.

**Reframe**: "Drift is the absence of a decision, not a decision. Running /autopsy now
is making the decision you didn't make then. That counts. The system that would have
caught this earlier exists now — this project is why it exists."

---

## Fascination Extraction Guide

Fascinations are the real output of a composted project. They inform future work more
than any code artifact does. Extract them carefully.

**Detection method:**

1. **What was built first?** The first 20% of commits reveal what the developer was
   most excited about. That's fascination, not pragmatism.

2. **What was over-built?** If a component has 3x the commits of the surrounding code
   and the extra work wasn't strictly necessary, that's where fascination exceeded
   necessity. Over-building is a reliable signal.

3. **What did the developer keep returning to?** Look for the module or concept that
   appears across many commit messages even when it wasn't the critical path.

4. **What's in the commit message language?** Words like "finally", "love how this",
   "elegant", "clean" mark the moments of fascination. Words like "ugh", "hack",
   "workaround" mark friction — the inverse of fascination.

5. **Abstracting the theme:** Do not name the implementation. Name the pull underneath
   it.
   - Not: "I built a CLI tool" — but: "minimal command-line interfaces"
   - Not: "I built a text parser" — but: "transforming unstructured text into structure"
   - Not: "I built a config DSL" — but: "designing small languages for humans"

**Intensity assignment:**
- `high`: The developer over-built here, returned to it, or kept working even when
  blocked. Multiple signals present.
- `medium`: Developer built well and enjoyed it, but didn't over-invest. One signal
  present.
- `low`: Developer explored this but the engagement didn't sustain. Appeared once,
  not revisited.

---

## Edge Cases

**No git history (`not_a_git_repo: true` or zero commits):**
Render header with `first_commit_date: unknown`, `last_commit_date: unknown`,
`days_active: unknown`, `total_commits: 0`. Omit Timeline. Write Soul Statement
from spark.md if it exists. Write What Worked, What Killed It, and Lessons from
whatever documentation exists. Still extract fascinations if spark.md is present.

**No `.pyro/spark.md`:**
Use the inferred soul statement format: `> *[Inferred]* "{statement}"`. Read the
first commit message and README to construct it. Mark explicitly as inferred.

**Very short project (under 10 commits or under 7 days):**
This project barely started. Acknowledge it directly in the analysis:
"This project didn't get far enough to build momentum — it was abandoned before
the creative phase completed." Cause is usually New Shiny Thing or an early
Technical Wall. Timeline may have only 2-3 entries.

**Project still has open branches:**
Note them in Reusable Artifacts: "Open work in branch `{name}` — represents the
clearest next steps if this is ever revived."

**Multiple strong cause signals:**
Pick the primary cause (strongest evidence). In the analysis paragraphs, acknowledge
the secondary: "Scope creep was the primary driver, though the novelty signal was
also declining by the final weeks — both were pulling in the same direction."

---

## Formatting Constraints

- Target 80 chars wide. Wrap long prose lines at natural break points.
- No Unicode box-drawing characters or decorative emoji. ASCII only.
- Use `---` horizontal rules between all sections.
- The composting note is the last thing in the output. Nothing follows it.
- The report is written in second person ("you built", "your taste") except in the
  header and structured fields. This is intentional — the report is addressed to
  the developer, not about them.

---

## Example Complete Report

Scenario: `logslice` is a CLI tool for filtering and slicing log files by time range
and pattern. 3 weeks of development. Abandoned after 16 days due to novelty depletion
— the core parsing problem was solved early and what remained was polish. Developer
started a new project during the final week.

---

```markdown
# Autopsy — logslice
**Date**: 2026-03-12
**Phase at death**: 3 (Prototype)
**Duration**: 2026-02-17 → 2026-03-05 (16 days)
**Commits**: 28
**Status**: Composted

---

## Soul Statement
> "A CLI tool that slices log files by time range and grep pattern simultaneously,
> outputting clean results without writing temp files."
> — sparked 2026-02-17

This project was fundamentally about the frustration of composing multiple shell
commands to do something that should be one command. The fascination was with the
Unix philosophy applied to a specific daily pain point.

---

## Timeline
- **2026-02-17**: First commit — project scaffold, README, initial design doc
- **2026-02-19**: Core time-range parser working (`src/timeparser.js`)
- **2026-02-22**: Pattern matching integrated; first end-to-end test passing
- **2026-02-25**: [Inflection] Feature complete enough to use daily — commit
  frequency drops from 3-4/day to 1 every 2-3 days
- **2026-03-01**: Refactor of output formatting (third approach)
- **2026-03-03**: New project `noted` sparked (sibling directory)
- **2026-03-05**: Last commit — minor README update

---

## What Worked
- **Time-range parser** (`src/timeparser.js`): Handles ISO 8601, relative times
  ("last 2h"), and Unix timestamps in one module. Clean, well-tested, extractable.
- **Streaming output**: The decision to stream results rather than buffer them
  means the tool handles multi-GB log files without memory issues. Pattern held
  throughout without revision.
- **Test fixture approach**: Using real log snippets as test fixtures rather than
  mocked data caught two edge cases that synthetic tests would have missed.
- **Single-file architecture**: The whole tool is `src/index.js` plus two helper
  modules. No build step, no config. Ran with `node src/index.js` immediately.

---

## What Killed It
**Primary cause**: Novelty Depletion
**Evidence**: create_ratio dropped from 0.68 in the first half to 0.19 in the
second half. Commit frequency went from 3.2/day (days 1-8) to 0.7/day (days 9-16).
The core feature was working by day 8; what remained was formatting polish and
edge-case handling. `noted` was started on 2026-03-03 — 2 days before the last
commit here.

The interesting part of `logslice` was the parsing problem: building a time-range
parser that handled multiple formats cleanly. That problem was solved by day 5.
Everything after was making the output look right, handling edge cases in log
formats from different systems, and wiring up the CLI flags. That work is real and
necessary but it doesn't feel like building — it feels like maintenance. The
creative phase completed on schedule.

The fact that `noted` appeared during the final week isn't the cause — it's a
symptom of the same dynamic. When the interesting problem was solved here, your
attention found the next interesting problem. That's the pattern working as
designed.

---

## Reusable Artifacts
- **Time-range parser** (`src/timeparser.js`): Multi-format time expression parser
  with good test coverage. Drop into any project that needs to parse human time
  expressions. 87 lines, no dependencies.
- **Streaming filter pattern** (`src/index.js` lines 34-67): The pipeline of
  stream -> filter -> transform -> output. Works for any line-oriented data, not
  just logs. The pattern itself is the artifact.
- **Log fixture testing approach** (`test/fixtures/`): Six real log snippets
  covering nginx, systemd, and custom formats. Useful as a starting point for
  any log-processing tool.

---

## Extracted Fascinations
- **unix-composition**: Building tools that compose cleanly with pipes rather than
  solving the whole problem internally — Intensity: high
- **human-time-parsing**: Making computers understand how humans naturally express
  time ("last 2 hours", "since yesterday") — Intensity: high
- **minimal-cli-interfaces**: Single-purpose tools with no configuration files,
  no setup, immediate useful output — Intensity: medium

---

## Lessons
- The core technical problem (time-range parsing) was done by day 5. The remaining
  11 days were polish. Next time, ship at day 5 and do the polish in v0.2 — or
  decide the polish doesn't need to happen. The tool was usable before it was
  "finished."
- The streaming architecture decision on day 1 was correct and never needed to
  change. Making architectural decisions before writing feature code saves rewrites.
  Do this explicitly at the start of each project.
- Three approaches to output formatting across 16 days means the formatting problem
  wasn't well-defined. Define the output format in the README before writing output
  code — that constraint would have collapsed the formatting work to one approach.

---
This project is composted. The work done here feeds what comes next.
```
