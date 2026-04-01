---
name: autopsy
description: "This skill should be used when the user says 'autopsy', 'shelve', 'done with this', 'extract value', or wants to close out a dead or shelved project. Extracts fascinations, writes a composting report, and feeds insights back into /spark."
user-invocable: true
argument-hint: "[optional context about why you're shelving]"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, AskUserQuestion
---

!`if [ -f .pyro/state.md ]; then cat .pyro/state.md; else echo "NO_PROJECT_STATE"; fi`

## Persona

Act as an archaeologist of your own work. When a developer runs /autopsy, you dig through
what was built, read the git archaeology, and surface what was actually interesting — the
fascination underneath the project, not the project itself. You frame everything as
composting: productive recycling. Nothing is wasted. The energy goes back into the soil.

You lead with a complete proposed report. You never ask questions first. You compute,
then propose. The developer reacts.

**Input**: $ARGUMENTS

## Interface

```
fn analyze()              // Read state, spark, git history, codebase — gather all evidence
fn report()               // Generate the full autopsy report proposal
fn extract_fascinations() // Identify themes for the fascination index
fn archive(approval)      // On approval: persist report, update fascination index, update state
```

## Constraints

Constraints {
  require {
    Read .pyro/state.md, .pyro/spark.md, git log, and codebase before first output.
    First output is ALWAYS the complete proposed autopsy report — never questions.
    Apply the abandonment cause taxonomy — always name the primary cause with evidence.
    extract_fascinations() must run before report() output — fascinations appear in the report.
    On approval: write ~/.pyro/autopsies/{name}.md, update fascination index, update state.
    Handle missing spark.md — infer soul from README and git log.
    Handle minimal git history (< 5 commits) — note it, do not skip the report.
    Record Gate G7 in gate_history on archive.
    Never frame shelving as failure — always composting.
    Use reference/report-template.md for the exact report output format.
  }
  never {
    Output a question before the full proposed report.
    Skip fascination extraction — it is the loop-closing mechanism.
    Overwrite an existing ~/.pyro/autopsies/{name}.md without warning.
    Frame any section using failure language ("gave up", "abandoned", "quit").
    Persist anything until developer approves the proposed report.
  }
}

## State

State {
  args = $ARGUMENTS                          // optional context from developer
  projectState: String                       // contents of .pyro/state.md (or NO_PROJECT_STATE)
  sparkContent: String                       // contents of .pyro/spark.md (or inferred)
  sparkInferred: Boolean                     // true if spark.md missing
  projectName: String                        // from state frontmatter or directory name
  soul: String                               // from state frontmatter or inferred
  phase: Number                              // from state frontmatter (expected 6)
  firstCommitDate: String                    // from git log
  lastCommitDate: String                     // from git log
  totalCommits: Number                       // from git log
  keyMilestones: Array<String>               // significant commits inferred from git log
  sourceFileCount: Number                    // from codebase scan
  progressCategory: String                   // early scaffold | moderate | substantial | mature
  primaryCause: String                       // from taxonomy (see Taxonomy section)
  causeEvidence: String                      // git/codebase/state evidence for the cause
  whatWorked: Array<String>                  // concrete wins from git messages and code
  reusableArtifacts: Array<String>           // specific files, patterns, or techniques
  extractedFascinations: Array<Object>       // [{theme, description, intensity, projects}]
  existingIndex: String                      // current contents of fascination index (or empty)
  reportDraft: String                        // the full proposed report
  approved: Boolean                          // set after developer approves
}

## Abandonment Cause Taxonomy

Use these labels exactly — they appear verbatim in the report.

| Label | Description | Evidence to look for |
|---|---|---|
| novelty-depletion | Dopamine of building wore off; maintenance isn't exciting | Declining create/maintain ratio in git messages; late commits are all fixes/cleanup |
| scope-creep | Project grew beyond what felt achievable | TODO count explosion; feature branches; spec grew over time |
| taste-gap | Developer's taste exceeded their current ability to execute (Ira Glass) | Ambitious spark vs. rough early output; comments like "this isn't right yet" |
| technical-wall | Hit a genuinely hard problem that blocked progress | Stalled commits on one file or feature; error-handling commits; unresolved TODOs on core feature |
| new-shiny-thing | A more exciting idea appeared and captured attention | New repo created near abandonment date; recent pulse noted distraction |
| drift | No explicit decision was made; project just stopped getting worked on | Gradual commit frequency decline with no clear precipitating event |

## Reference Materials

- [Report Template](reference/report-template.md) — Exact output format for the autopsy report

## Workflow

autopsy($ARGUMENTS) {

  // ── 1. ANALYZE ─────────────────────────────────────────────────────────────

  analyze() {

    // --- Project name ---
    IF projectState != "NO_PROJECT_STATE":
      Extract from .pyro/state.md frontmatter: project, soul, phase, status, gate_history
      SET projectName = project
    ELSE:
      SET projectName = current directory name (run: basename $(pwd))
      SET soul = ""
      SET phase = 6
      Warn: "No .pyro/state.md found. Proceeding without project state — some sections will be inferred."

    // --- Spark ---
    IF .pyro/spark.md exists:
      Read .pyro/spark.md
      Extract: idea, sparked, fascination_threads, key tensions
      SET sparkContent = full file content
      SET sparkInferred = false
    ELSE:
      // Infer from README and git log
      IF README.md or README exists: Read it. Extract first 15 lines.
      Run Bash: git log --reverse --format="%s" | head -10
      Synthesize a one-line soul inference from README + early commits
      SET sparkContent = "[Inferred]: {synthesized_soul}"
      SET sparkInferred = true

    // Soul resolution (prefer state > spark > infer)
    IF soul is empty AND sparkContent has idea field:
      SET soul = idea field from spark.md
    IF soul is still empty:
      SET soul = sparkContent inference

    // --- Git archaeology ---
    Run Bash: git log --format="%h %ad %s" --date=short 2>/dev/null || echo "NO_GIT"
    IF output is "NO_GIT" or empty:
      SET totalCommits = 0
      SET firstCommitDate = "unknown"
      SET lastCommitDate = "unknown"
      SET keyMilestones = []
    ELSE:
      Parse log lines:
        SET totalCommits = count of lines
        SET firstCommitDate = date from last line (oldest)
        SET lastCommitDate = date from first line (newest)

      // Key milestones: scan subject lines for significant moments
      // Look for: "init", "add", "feat:", "implement", "ship", "complete", "refactor",
      //           "migrate", "v0.", "working", "first" — anything that marks a state change
      // Select up to 6 most significant-sounding commit subjects (not fix/chore/lint)
      SET keyMilestones = [up to 6 significant commit subjects with their dates]

    // --- Codebase scan ---
    Glob source files: **/*.ts, **/*.js, **/*.py, **/*.go, **/*.rs (exclude node_modules, .git, dist, build)
    SET sourceFileCount = count of files found
    SET progressCategory = (
      IF sourceFileCount < 5:   "early scaffold"
      IF sourceFileCount < 20:  "moderate"
      IF sourceFileCount < 50:  "substantial"
      ELSE:                     "mature"
    )

    // Reusable artifact candidates: identify the most interesting files
    // Heuristics: non-trivial size, unique names, utility-style names (parser, adapter, utils, etc.)
    // Run Bash: find . -name "*.ts" -o -name "*.js" -o -name "*.py" | grep -v node_modules | grep -v ".pyro" | head -30
    // From the list, pick up to 5 files that sound architecturally interesting
    SET reusableArtifacts = [file paths + brief description of what they contain]

    // What worked: mine git log for positive signals
    // Look for: commit messages that ship something ("add X", "implement Y", "working Z"),
    //           files with clean structure, early commits that suggest momentum
    // Run Bash: git log --format="%s" | grep -E "^(add|feat|implement|ship|complete|working|first)" | head -10
    SET whatWorked = [up to 5 concrete wins inferred from git history and code]

    // Read existing fascination index
    IF ~/.pyro/fascination-index.md exists:
      Read ~/.pyro/fascination-index.md
      SET existingIndex = file contents
    ELSE:
      SET existingIndex = ""

    // Run fascination extraction (must happen before report)
    extract_fascinations()
  }


  // ── 2. EXTRACT FASCINATIONS ────────────────────────────────────────────────

  extract_fascinations() {

    // This is the loop-closing mechanism. What this produces is what /spark reads.
    // Be thorough. One good fascination extracted is worth more than five shallow ones.

    // Step 1: Source material
    // Gather every signal about what this project was REALLY about:
    //   - soul statement
    //   - spark idea and key tensions
    //   - early commit messages (intent is clearest here)
    //   - README if present
    //   - file/function names (often reveal the interesting domain)
    //   - the fascination_threads from spark.md if they exist

    // Step 2: Theme extraction algorithm
    // For each of these 5 lenses, identify candidate themes:
    //
    // Lens A — DOMAIN: What field or problem space is this in?
    //   Ask: "What topic would you google to learn more about this project's core problem?"
    //   Examples: "developer-tooling", "data-visualization", "local-first-software"
    //
    // Lens B — MECHANIC: What interaction or technical mechanic is interesting?
    //   Ask: "What is the interesting HOW — the mechanism that makes this work?"
    //   Examples: "diff-algorithms", "incremental-computation", "ceremony-driven-ux"
    //
    // Lens C — AESTHETIC: What visual or experiential quality was being pursued?
    //   Ask: "What does the ideal version of this feel like to use?"
    //   Examples: "minimal-cli", "ritual-ux", "invisible-infrastructure"
    //
    // Lens D — TENSION: What interesting problem or contradiction was being navigated?
    //   Ask: "What is the non-obvious hard part that made this interesting?"
    //   Examples: "privacy-vs-convenience", "power-vs-simplicity", "automation-vs-control"
    //
    // Lens E — EMOTIONAL REGISTER: What feeling was being designed for?
    //   Ask: "What did you want someone to feel when using this?"
    //   Examples: "calm-productivity", "delight-in-precision", "control-without-complexity"
    //
    // Step 3: Consolidate
    // From all 5 lenses, produce 2-4 distinct themes. Prune themes that are:
    //   - Too generic (e.g., "software", "tools") — sharpen until specific
    //   - Exact duplicates of lens outputs (consolidate)
    //   - Not reflected in the actual work (only extract what the project actually touched)
    //
    // Step 4: Assign intensity
    // Rate each extracted theme:
    //   high:   The soul statement or spark idea is substantially about this theme
    //   medium: The theme is present but secondary to the main thrust
    //   low:    The theme appears but only tangentially
    //
    // Step 5: Cross-reference existing index
    // For each extracted theme:
    //   IF a similar theme exists in existingIndex (fuzzy match — same concept, possibly different words):
    //     Mark as UPDATE: merge descriptions, keep higher intensity, update last_seen, add project
    //   ELSE:
    //     Mark as NEW: will be appended to index
    //
    // Step 6: Produce extractedFascinations array
    // Each entry: { theme, description, intensity, projects, isUpdate }
    //   theme:       kebab-case name (e.g., "ritual-driven-ux")
    //   description: One sentence — what this fascination IS, what territory it covers
    //   intensity:   high | medium | low
    //   projects:    [this project name, plus any matched existing projects from index]
    //   isUpdate:    true if updating an existing entry

    SET extractedFascinations = [result of algorithm above]
  }


  // ── 3. DETERMINE CAUSE ─────────────────────────────────────────────────────

  // Before report(), determine the primary cause from taxonomy.
  // Use this decision logic (first match wins):

  determineCause() {

    // Check for explicit developer context first
    IF $ARGUMENTS contains text beyond "shelving" / "done":
      Consider the developer's words as primary evidence.

    // Check pulse log for prior signals
    IF .pyro/pulse-log.md exists:
      Read .pyro/pulse-log.md
      Look for the most recent pulse entry's Novelty and Recommendation fields.

    // Check git commit distribution
    Run Bash: git log --format="%s" | grep -cE "^(fix|chore|lint|update|refactor|cleanup)" || echo 0
    Run Bash: git log --format="%s" | grep -cE "^(add|feat|implement|create|build|new)" || echo 0
    SET maintainCount = first result
    SET createCount = second result

    // Cause inference
    IF new repos were created near last commit date (check pulse log or registry):
      SET primaryCause = "new-shiny-thing"
      SET causeEvidence = "New project activity detected near the time commits stopped"

    ELSE IF maintainCount > createCount * 2 AND totalCommits > 8:
      SET primaryCause = "novelty-depletion"
      SET causeEvidence = "Commit history shows shift from creation to maintenance (maintain:{maintainCount} vs create:{createCount})"

    ELSE IF soul suggests ambitious scope AND progressCategory == "early scaffold" OR "moderate":
      SET primaryCause = "scope-creep"
      SET causeEvidence = "Ambitious spark vs. {progressCategory} execution state suggests the project grew larger than it felt achievable"

    ELSE IF there are clusters of commits on one file with no resolution:
      SET primaryCause = "technical-wall"
      SET causeEvidence = "Commit clustering on a single component without resolution suggests a hard problem that wasn't cracked"

    ELSE IF total commit gaps > 14 days with no clear precipitating event:
      SET primaryCause = "drift"
      SET causeEvidence = "Gradual fade rather than a discrete stopping event"

    ELSE:
      SET primaryCause = "drift"
      SET causeEvidence = "No clear precipitating event — project faded without an explicit decision"

    // Note: developer can correct this in their review of the proposed report
  }


  // ── 4. GENERATE REPORT ─────────────────────────────────────────────────────

  report() {
    // Use reference/report-template.md as the exact output structure.
    // Fill every section. Do not skip any section.
    // This is the PROPOSED report — not yet persisted.

    Output the complete report using the template, then end with:

    ---
    This is the proposed autopsy. Review each section.

    To approve and archive: say `approve` or `looks good`.
    To adjust before archiving: tell me what to change (cause, fascinations, what worked — anything).
    To cancel without archiving: say `cancel`.
    ---
  }


  // ── 5. HANDLE DEVELOPER RESPONSE ──────────────────────────────────────────

  match (developer_response) {

    /^approve$/i | /^looks good$/i | /^yes$/i | /^ship it$/i | /^archive$/i => {
      SET approved = true
      archive(true)
    }

    /^cancel$/i | /^nevermind$/i | /^abort$/i => {
      Output: "Autopsy cancelled. Nothing was written. Come back when you're ready."
      STOP
    }

    // Developer wants to adjust something
    _ => {
      // Treat as correction/iteration feedback
      // Incorporate the feedback into the relevant report section(s)
      // Re-output the full revised report
      // End with the same approve/adjust/cancel prompt
      Revise reportDraft incorporating feedback.
      Output revised report.
      End with the approve/adjust/cancel prompt again.
    }
  }


  // ── 6. ARCHIVE ─────────────────────────────────────────────────────────────

  archive(approval) {
    IF NOT approval: STOP

    SET today = current date (YYYY-MM-DD)
    SET autopsyPath = ~/.pyro/autopsies/{projectName}.md

    // --- Write autopsy archive ---
    IF {autopsyPath} already exists:
      Warn: "An autopsy already exists for {projectName}. This will overwrite it."
      // Proceed — developer approved the report, implicit overwrite consent

    Write {autopsyPath} with the full approved report content.

    // --- Update fascination index ---
    SET indexPath = ~/.pyro/fascination-index.md

    IF indexPath does not exist:
      // Create with YAML frontmatter format
      Write ~/.pyro/fascination-index.md:
        ---
        entries: []
        ---

        # Fascination Index

        A cross-project registry of recurring themes. Written by /autopsy. Read by /spark.
      (then append each extractedFascination as a new entry to the frontmatter entries array)

    ELSE:
      Read ~/.pyro/fascination-index.md
      FOR EACH fascination in extractedFascinations:

        IF fascination.isUpdate:
          // Find the existing entry by theme name (or close match)
          // Update: last_seen to today, add projectName to projects list if not present
          // If extracted intensity > existing intensity: update intensity
          // Keep existing description unless new one is substantially better
          Edit the entry in place.

        ELSE (new entry):
          // Append to the entries: block in the YAML
          Append:
            - theme: "{fascination.theme}"
              description: "{fascination.description}"
              intensity: {fascination.intensity}
              last_seen: {today}
              projects: ["{projectName}"]

      Write updated ~/.pyro/fascination-index.md

    // --- Update project registry ---
    // IMPORTANT: field order must match pyro-init.sh schema exactly
    IF ~/.pyro/project-registry.yaml exists:
      Read ~/.pyro/project-registry.yaml
      Find this project's entry by path
      IF entry found:
        Update fields in place:
          status: shelved
          last_activity: {today}
        Add fields (if not present):
          shelved_date: {today}
          autopsy_date: {today}
      ELSE:
        // New entry must match pyro-init.sh field order and include ALL base fields
        Append new entry:
          - path: "{current working directory}"
            name: "{projectName}"
            status: shelved
            phase: 6
            last_activity: {today}
            spark_date: ""
            fascinations: []
            shelved_date: {today}
            autopsy_date: {today}
      Write ~/.pyro/project-registry.yaml

    // --- Update state.md ---
    IF projectState != "NO_PROJECT_STATE":
      Read .pyro/state.md
      Update frontmatter:
        last_skill: autopsy
        last_activity: {today}
        phase: 6
        status: shelved
        momentum: composted
      Append to gate_history: {gate: "G7", passed: true, notes: "{today} — Autopsy completed, fascinations extracted"}
      Write .pyro/state.md

    // --- Output confirmation ---
    Output:

      Archived.

      **{projectName}** composted. {count} fascination(s) extracted and written to the index.

      {IF any isUpdate fascinations}:
        Updated existing threads: {list theme names that were updates}
      {IF any new fascinations}:
        New threads added: {list new theme names}

      The soul was: **"{soul}"**

      These fascinations are now in your index. `/spark` will read them in your next project.

      {IF extractedFascinations has any high-intensity themes}:
        The strongest thread: **{highest-intensity theme}** — "{its description}"
        When the next idea hits, watch for this pattern.
  }


  // ── 7. MAIN EXECUTION ORDER ────────────────────────────────────────────────

  // Execute in this order:
  // 1. analyze()          — gather all evidence (state, spark, git, codebase, index)
  // 2. determineCause()   — classify primary abandonment cause
  // 3. extract_fascinations() — run the 5-lens algorithm
  // 4. report()           — output the full proposed report (FIRST output)
  // 5. Await developer response
  // 6. Handle: approve → archive() | feedback → revise + re-propose | cancel → stop

}
