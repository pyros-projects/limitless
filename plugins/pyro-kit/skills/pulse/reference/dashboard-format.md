# Pulse Dashboard Format

This file defines the exact layout and content of the `/pulse` momentum dashboard. Every
`/pulse` invocation produces this dashboard. Follow this spec exactly — section order,
labels, and formatting are load-bearing because the user reads them as a consistent ritual.

---

## How to Generate the Dashboard

1. Run `git-activity.sh` (via bash preprocessor or inline). Parse its output sections.
2. Read `.pyro/spark.md` for the original spark. Fall back to README/first commits if absent.
3. Read `.pyro/state.md` for phase, pulse_count, and project name.
4. Scan the codebase for TODO, FIXME, HACK markers to estimate progress.
5. Render each section in order. Do not skip sections, even when data is thin.
6. End with the response prompt verbatim.

---

## Dashboard Template

Each section below is a required block. Replace `{placeholders}` with real values.

---

### Section 1: Header

```
## Pulse — {project_name}
**Phase {N}** · **{days_active} days active** · **Pulse #{pulse_count}**
```

- `project_name`: from `.pyro/state.md` project field, or directory name if absent
- `days_active`: today minus `first_commit_date` from git-activity.sh OVERVIEW
- `pulse_count`: from `.pyro/state.md` pulse_count field + 1 (this run counts)

---

### Section 2: Activity

Label: `### Activity`

Required items:
- Commit frequency as an ASCII sparkline for the last 14 days (see sparkline spec below)
- Daily average commits (from `daily_average` in COMMIT_FREQUENCY)
- Days since last commit (from `days_since_last_commit` in OVERVIEW)
- Longest gap: scan the per-day breakdown from COMMIT_FREQUENCY for the longest consecutive
  run of zero-commit days; report the length and approximate date range
- Active branch (from BRANCHES `active_branch`)
- Stale branches: list each `stale:` line from BRANCHES output; if none, omit this line

**Sparkline spec:**
- Use the per-day counts from COMMIT_FREQUENCY (one `YYYY-MM-DD: N` line per day)
- Map each day to a character: `0` → `.`, `1-2` → `_`, `3-5` → `-`, `6-9` → `=`, `10+` → `#`
- Print the last 14 days as a single string, oldest left, newest right
- Label it: `Commits (14d): [sparkline]`
- No spaces between characters; fit within 80 chars

---

### Section 3: Novelty Depletion Signal

Label: `### Novelty Depletion Signal`

This is the core psychological insight of the system. Never omit it.

Data source: `MESSAGE_SENTIMENT` section of git-activity.sh output.

Required items:
- `create_ratio` and `maintain_ratio` as percentages (multiply by 100, round to integer)
- Trend direction: compare `first_half_create_ratio` vs `second_half_create_ratio`
- A trend bar showing first half vs second half (see format below)
- A plain-language interpretation (see interpretation table below)
- If `new_repos_detected > 0`: add a "New Shiny Thing Detector" flag (see format below)

**Trend bar format:**
```
First half:  [####......] {first_half_pct}% create
Second half: [##........] {second_half_pct}% create
```
- Bar is 10 chars wide using `#` for filled, `.` for empty
- Fill proportional to ratio: multiply ratio by 10, round to integer for hash count

**Interpretation table (use first matching condition):**

| Condition | Plain-language text |
|---|---|
| `total_in_window == 0` | "No commits in the window. Cannot assess novelty signal — but the gap itself is a signal." |
| `create_ratio >= 0.60` AND `sentiment_trend != "declining"` | "You're still building new things. Abandonment risk is low right now." |
| `create_ratio >= 0.40` AND `sentiment_trend == "declining"` | "Transitioning from creation to maintenance — this is where abandonment typically happens. The exciting part is shifting to upkeep." |
| `create_ratio < 0.40` AND `sentiment_trend == "declining"` | "Creation work has mostly dried up. You're in maintenance mode. This is the highest-risk zone for abandonment." |
| `create_ratio < 0.40` AND `sentiment_trend != "declining"` | "The exciting part is over. You're in a stable maintenance rhythm — uncommon for solo projects to sustain without a forcing function." |

Bold the diagnostic label before the explanation:
- `>= 0.60` AND not declining: **Still in creation mode.**
- `>= 0.40` AND declining: **Transitioning.**
- `< 0.40` AND declining: **Novelty depleted.**
- `< 0.40` AND not declining: **Maintenance phase.**

**New Shiny Thing Detector format** (only when `new_repos_detected > 0`):
```
> [!] New Shiny Thing Detector: {N} new project(s) started since this one
> ({new_repo_names}). Classic distraction pattern.
```
List the `new_repo:` names from the NEW_REPOS section. If none named, show just the count.

---

### Section 4: Progress

Label: `### Progress`

Required items:
- TODO/FIXME/HACK counts from a grep scan of the codebase
- Rough progress estimate as a percentage range
- A note that the estimate is approximate

Format:
```
Open markers: {todo_count} TODOs, {fixme_count} FIXMEs, {hack_count} HAcks
Rough progress: ~{low}-{high}% complete (approximate — based on commit history and open markers)
```

Express the estimate as a range (e.g., `~40-55%`), never a single precise number.
Reason from: total commits relative to commit velocity, TODO density, and whether any
spec or planning files exist (suggesting early-phase work is done).

---

### Section 5: Original Spark

Label: `### Original Spark`

When `.pyro/spark.md` exists with an `idea` field in frontmatter:
```
> "{verbatim idea field text}"
> — sparked {sparked date}
```

When `.pyro/spark.md` is absent or has no `idea` field:
```
> *[Inferred from README/first commits]* "{best-effort one-sentence summary}"
```

The spark is always a blockquote. Never paraphrase a verbatim spark — copy it exactly.
Multi-line sparks: prefix each continuation line with `>`.

---

### Section 6: Three Paths

Label: `### Three Paths`

Always show exactly three paths: Push, Pivot, Shelve. In that order. Each path block:

```
**Push** — {one sentence: what pushing means for this project specifically}
- First step: {concrete action to take today — specific, not generic}
- Effort: {rough time estimate, e.g., "2-3 focused sessions", "1-2 weeks"}
- Preserved: {what you keep if you push}
- Lost: {what you give up by committing to push}
```

```
**Pivot** — {one sentence: what pivoting means here — scope reduction, angle change, etc.}
- First step: {concrete action to take today}
- Effort: {rough estimate}
- Preserved: {what survives a pivot}
- Lost: {what gets cut}
```

```
**Shelve** — {one sentence: what shelving means — intentional pause, not failure}
- First step: {concrete closing action — run /autopsy, write a note, tag the repo}
- Effort: {e.g., "30 minutes to close out cleanly"}
- Preserved: {what you extract by shelving deliberately}
- Lost: {momentum, unfinished state}
```

The first steps must be specific to this project. Never write generic text like
"decide on next steps" or "review the codebase."

---

### Section 7: Recommendation

Label: `### Recommendation`

Single-line format:
```
**I recommend: {Push | Pivot | Shelve}** — {1-2 sentences of evidence-based reasoning
drawn from the data above.}
```

Reasoning must cite at least one concrete signal from the dashboard (days since last commit,
novelty signal state, progress estimate, or spark alignment). State the recommendation with
confidence. It is opinionated but overridable.

---

### Section 8: Response Prompt

End with this block, verbatim. No variation. No additional questions.

```
---
Which path? Say `push`, `pivot`, `shelve`, or `not now`. Or tell me what's actually hard.
```

---

## Complete Example Dashboard

Scenario: `termdiff` is a CLI tool for comparing terminal recordings. 21 days in
development. Commit activity declining. Developer started a new project 5 days ago.
This is Pulse #3.

---

```markdown
## Pulse — termdiff
**Phase 4** · **21 days active** · **Pulse #3**

---

### Activity

Commits (14d): ..._-==_-...__

Daily average: 1.4 commits/day
Days since last commit: 6

Longest gap: 6 days (Feb 23 – Mar 1) — current streak

Active branch: main
Stale branches: feature/replay-mode (18 days), feature/diff-colors (22 days)

---

### Novelty Depletion Signal

Create: 28% · Maintain: 58% · Other: 14%

First half:  [#####.....] 52% create
Second half: [##........] 22% create
Trend: declining

**Novelty depleted.** Creation work has mostly dried up. You're in maintenance mode.
This is the highest-risk zone for abandonment.

> [!] New Shiny Thing Detector: 1 new project started since this one
> (noted, sparked 2026-02-24). Classic distraction pattern.

---

### Progress

Open markers: 14 TODOs, 2 FIXMEs, 1 HACK
Rough progress: ~55-65% complete (approximate — based on commit history and open markers)

---

### Original Spark

> "A CLI tool that diffs two terminal recordings and shows exactly what changed —
> useful for writing tutorials and documentation where you need to demonstrate a
> before/after."
> — sparked 2026-02-19

---

### Three Paths

**Push** — Finish the core diff engine and ship a 0.1 that does the one thing the
spark describes, ignoring the replay and color features.
- First step: Close the two stale branches and write a SCOPE.md listing what is out
  of scope for 0.1
- Effort: 3-4 focused sessions to reach a shippable 0.1
- Preserved: The original idea gets realized; you have something usable
- Lost: The replay-mode and diff-colors features (for now)

**Pivot** — Narrow to a simpler problem: plain-text diff of shell history files
instead of full terminal recordings. Smaller scope, faster to useful.
- First step: Write a 20-line prototype that diffs two .bash_history files and
  prints the delta
- Effort: 1 session to validate if the narrowed idea is interesting
- Preserved: The comparison insight from the original spark
- Lost: The rich terminal recording format; the tutorial use case as originally scoped

**Shelve** — Close this out deliberately now rather than letting it drift.
- First step: Run `/autopsy` to extract what you learned; tag the repo `v0-shelved`
  so you can find it
- Effort: 30 minutes to close cleanly
- Preserved: Everything you built is intact and findable; the fascinations go into
  your thread library
- Lost: Momentum; the 55-65% that is built stays unfinished

---

### Recommendation

**I recommend: Push** — The spark is specific and the core diff engine is more than
halfway done. The 6-day gap and declining novelty signal are real, but this project
is close enough to a 0.1 that shelving would leave a complete idea unfinished.
Closing the stale branches and scoping to the original use case should get you to
shippable in a week.

---
Which path? Say `push`, `pivot`, `shelve`, or `not now`. Or tell me what's actually hard.
```

---

## Edge Cases

**No git history (`not_a_git_repo: true` or zero commits):**
Render the header and spark sections normally. Replace Activity, Novelty Depletion, and
Progress with a single line: "No git history found. Activity metrics unavailable."
Still show all three paths and a recommendation based on what is available.

**Zero commits in window but history exists:**
Show the sparkline as all dots. Set novelty signal to the "No signal" row. Note in Activity:
"No commits in the last {N} days — project may be dormant."

**No `.pyro/spark.md`:**
Use the inferred spark format. Read the first commit message and README (if present) to
construct the one-sentence summary. Label it clearly as inferred.

**Days since last commit is 0:**
Write "committed today" rather than "0 days since last commit."

**`pulse_count` is missing from state.md:**
Default to 1 for the first pulse.

---

## Formatting Constraints

- Target 80 chars wide. Wrap long prose lines at natural break points.
- Sparklines and trend bars use ASCII only: `.` `_` `-` `=` `#` `[` `]` `>` `!`
- Use `---` horizontal rules between all sections.
- Progress is always a range (`~40-55%`), never a single precise number.
- The response prompt is the last thing in the output. Nothing follows it.
