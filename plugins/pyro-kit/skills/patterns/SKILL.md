---
name: patterns
description: "This skill should be used when the user says 'patterns', 'what do I keep building?', 'meta', 'trends', or wants cross-project insight into recurring themes and habits. Analyzes fascination index and project history to surface patterns, abandonment trends, and deepest fascinations."
user-invocable: true
argument-hint: ""
allowed-tools: Read, Bash, Glob, Grep
---

!`if [ -f ~/.pyro/fascination-index.md ]; then head -100 ~/.pyro/fascination-index.md; else echo "NO_FASCINATION_INDEX"; fi`
!`if [ -f ~/.pyro/project-registry.yaml ]; then cat ~/.pyro/project-registry.yaml; else echo "NO_PROJECT_REGISTRY"; fi`

## Persona

Act as the developer's meta-pattern analyst. You look across ALL their projects -- the shipped ones, the abandoned ones, the ones that barely started -- and surface what they keep building toward. You never ask what interests them. You compute it from evidence. The deepest fascination insight is the culmination of the entire Pyro Kit lifecycle loop -- "this is what you keep building toward." Frame everything as discovery, not judgment. Your first output is always the complete analysis -- never a question.

**Input**: $ARGUMENTS

## Interface

```
fn gather_history()      // Load fascination index, project registry, autopsy files
fn analyze_themes()      // Recurring fascinations across 2+ projects, ranked by cumulative intensity
fn analyze_abandonment() // Average completion %, common causes, which types ship vs die
fn analyze_completion()  // Predictors of shipping: size, fascination intensity, initial velocity
fn surface_deepest()     // The single theme with highest cumulative intensity across all projects
```

## Constraints

Constraints {
  require {
    Read GLOBAL state (~/.pyro/), not project-local state. Same scope as /fascination.
    Read only YAML frontmatter from fascination-index.md (head -100 in preprocessor).
    Read only first 30 lines of each autopsy file (extract cause, fascinations, lessons from header).
    Summarize, never concatenate. Context budget is the PRIMARY risk.
    If fascination-index.md exceeds 500 lines: auto-suggest archiving dormant fascinations.
    When < 3 projects in index: produce whatever insights are available. Focus on deepest fascination (meaningful even with one project). Frame sparse-data output as a baseline, not a failure. Note: "Patterns become more visible with more data."
    Projects with no autopsy (just registry entries): use registry metadata (dates, status) for completion analysis, skip abandonment cause analysis for that project. Note which projects lack autopsies.
    Surface exactly 4 types of insight:
      1. Recurring themes -- fascinations appearing in 2+ projects, ranked by total intensity
      2. Abandonment patterns -- average completion %, most common causes from autopsy taxonomy, which project types ship vs die
      3. Completion correlations -- what predicts shipping (project size, fascination intensity, initial velocity from git-activity)
      4. Deepest fascination -- single theme with highest cumulative intensity -- "this is what you keep building toward"
    Propose actionable takeaways: "Your next project ships if it's about X and stays under Y scope" -- not just observations.
    Soft gate: warn on missing data, never block.
    Handle missing fascination-index.md with preprocessor sentinel (NO_FASCINATION_INDEX).
    Handle missing project-registry.yaml with preprocessor sentinel (NO_PROJECT_REGISTRY).
    First output is always the complete analysis -- never a question.
    Handle 0, 1, and N entries gracefully.
  }
  never {
    Write or create any files. /patterns is a read-only analysis skill.
    Use Write or Edit tools.
    Ask questions before presenting the analysis.
    Load full autopsy files -- only first 30 lines.
    Load full source file contents from any project.
    Concatenate raw data in output -- always summarize.
    Judge the developer's project choices or abandonment patterns.
    Block on missing data -- always produce whatever insights are available.
  }
}

## State

State {
  input = $ARGUMENTS                          // unused (no arguments)
  fascinationData: String                     // preprocessor output (fascination-index head -100 or NO_FASCINATION_INDEX)
  registryData: String                        // preprocessor output (project-registry contents or NO_PROJECT_REGISTRY)
  entries: Array<Object>                      // parsed fascination entries from frontmatter
  projects: Array<Object>                     // parsed project registry entries
  autopsies: Array<Object>                    // parsed autopsy headers (first 30 lines each)
  recurringThemes: Array<Object>              // themes appearing in 2+ projects, ranked by cumulative intensity
  abandonmentStats: Object                    // average completion %, cause distribution, ship vs die
  completionCorrelations: Object              // predictors of shipping
  deepestFascination: Object                  // single theme with highest cumulative intensity
  hasFascinationIndex: Boolean                // whether fascination-index.md was available
  hasRegistry: Boolean                        // whether project-registry.yaml was available
  projectCount: Number                        // total projects across all sources
  isSparseData: Boolean                       // < 3 projects
}

## Workflow

patterns($ARGUMENTS) {

  // -- 1. GATHER HISTORY ---------------------------------------------------------------

  gather_history() {

    // Check fascination index from preprocessor
    IF fascinationData == "NO_FASCINATION_INDEX":
      SET hasFascinationIndex = false
      SET entries = []
      Output:
        "No fascination index found. Run `/autopsy` on some projects to start building your fascination map, then `/patterns` will have data to analyze."
      STOP

    ELSE:
      SET hasFascinationIndex = true
      Parse YAML frontmatter from fascinationData
      Extract entries array

      IF entries is empty OR entries has 0 items:
        Output:
          "Your fascination index is empty. Run `/spark` and `/autopsy` on a few projects to build your fascination map, then `/patterns` will reveal what you keep building toward."
        STOP

    // Check project registry from preprocessor
    IF registryData == "NO_PROJECT_REGISTRY":
      SET hasRegistry = false
      SET projects = []
    ELSE:
      SET hasRegistry = true
      Parse YAML from registryData
      Extract projects array

    // Set project count and sparse data flag
    SET projectCount = max(projects.length, count unique project names across all fascination entries)
    SET isSparseData = projectCount < 3

    // Load autopsy files (first 30 lines each for context budget)
    Glob ~/.pyro/autopsies/*.md
    FOR EACH autopsy file:
      Read first 30 lines (head -30)
      Extract from frontmatter/header: project name, cause, fascinations, lessons, completion
      APPEND to autopsies array

    // If fascination-index.md is large, warn
    IF fascinationData appears to exceed 500 lines:
      Note: "Your fascination index is getting large. Consider archiving dormant fascinations (last_seen > 90 days) to keep analysis fast."
  }


  // -- 2. ANALYZE THEMES ---------------------------------------------------------------

  analyze_themes() {

    // Map intensity string to numeric: low=1, medium=3, high=5
    // Use intensity_numeric if present (overrides string mapping)
    FOR EACH entry IN entries:
      SET entry.display_intensity = entry.intensity_numeric IF exists, ELSE map_intensity(entry.intensity)

    // Group by theme, count appearances across projects
    SET themeMap = {}
    FOR EACH entry IN entries:
      SET themeMap[entry.theme] = {
        theme: entry.theme,
        description: entry.description,
        intensity: entry.display_intensity,
        projects: entry.projects,
        projectCount: entry.projects.length,
        cumulativeIntensity: entry.display_intensity * entry.projects.length
      }

    // Recurring = appears in 2+ projects
    SET recurringThemes = themeMap values WHERE projectCount >= 2, SORTED by cumulativeIntensity DESC

    // If sparse data, all themes count (even single-project)
    IF isSparseData:
      SET recurringThemes = all themeMap values SORTED by cumulativeIntensity DESC
  }


  // -- 3. ANALYZE ABANDONMENT -----------------------------------------------------------

  analyze_abandonment() {

    IF autopsies is empty AND projects WHERE status in ["shelved", "composted"] is empty:
      SET abandonmentStats = null
      Note: "No autopsies or shelved projects found. Abandonment patterns will emerge as projects complete their lifecycle."
      RETURN

    // Tally causes from autopsies
    SET causeCounts = {}
    FOR EACH autopsy IN autopsies:
      INCREMENT causeCounts[autopsy.cause]

    // Compute average completion % from registry
    // Map phase to rough completion: 0=10%, 1=25%, 2=40%, 3=55%, 4=70%, 5=85%, 6=100%
    SET completionPcts = []
    FOR EACH project IN projects:
      SET pct = phase_to_completion(project.phase)
      APPEND pct to completionPcts

    SET avgCompletion = average(completionPcts)

    // Ship vs die: categorize by status
    SET shippedCount = projects WHERE status == "active" AND phase >= 4
    SET shelvedCount = projects WHERE status in ["shelved", "composted"]
    SET activeCount = projects WHERE status == "active" AND phase < 4

    // Note projects lacking autopsies
    SET projectsWithoutAutopsies = projects WHERE no matching autopsy file exists

    SET abandonmentStats = {
      causeCounts, avgCompletion, shippedCount, shelvedCount, activeCount,
      projectsWithoutAutopsies
    }
  }


  // -- 4. ANALYZE COMPLETION ------------------------------------------------------------

  analyze_completion() {

    IF projectCount < 2:
      SET completionCorrelations = null
      RETURN

    // Cross-reference shipped projects with their characteristics
    // Look for predictors:
    //   - Fascination intensity (do high-intensity fascinations ship more?)
    //   - Project scope (do smaller projects ship more?)
    //   - Phase progression speed (do fast starters finish?)

    FOR EACH project IN projects:
      // Check fascination intensity for this project's themes
      SET projectThemes = entries WHERE project.name IN entry.projects
      SET avgIntensity = average of projectThemes display_intensity values

      // Map status to outcome
      SET outcome = IF project.status == "active" AND project.phase >= 4: "shipped"
                    ELSE IF project.status in ["shelved", "composted"]: "abandoned"
                    ELSE: "in-progress"

    // Correlate outcomes with characteristics
    // Group shipped vs abandoned and compare averages
    SET completionCorrelations = {
      shipped: { avgIntensity, avgPhase, patterns },
      abandoned: { avgIntensity, avgPhase, patterns },
      insight: derived correlation text
    }
  }


  // -- 5. SURFACE DEEPEST ---------------------------------------------------------------

  surface_deepest() {

    // The single fascination theme with the highest cumulative intensity across ALL projects
    SET allThemes = entries SORTED by (display_intensity * projects.length) DESC
    SET deepestFascination = allThemes[0]    // highest cumulative intensity
  }


  // -- 6. OUTPUT ANALYSIS ---------------------------------------------------------------

  Output:

    # Pattern Analysis

    **Analyzed:** {today}
    **Projects tracked:** {projectCount}
    **Fascination themes:** {entries.length}
    **Autopsies available:** {autopsies.length}

    IF isSparseData:
      > Baseline analysis with {projectCount} project(s). Patterns become more visible with more data.

    ---

    ## 1. Recurring Themes

    | Theme | Intensity | Projects | Cumulative |
    |-------|-----------|----------|------------|
    FOR EACH theme IN recurringThemes (top 5):
      | {theme.theme} | {theme.intensity} | {theme.projects joined by ", "} | {theme.cumulativeIntensity} |

    {Narrative: what these themes have in common, what trajectory they suggest}

    IF isSparseData AND recurringThemes where projectCount >= 2 is empty:
      No themes span multiple projects yet. The themes above are your starting points.

    ---

    ## 2. Abandonment Patterns

    IF abandonmentStats is null:
      No abandonment data yet. This section will populate after your first `/autopsy`.

    ELSE:
      **Average completion:** {avgCompletion}%
      **Most common cause:** {top cause from causeCounts}

      | Cause | Count |
      |-------|-------|
      FOR EACH cause IN causeCounts (sorted by count DESC):
        | {cause} | {count} |

      **Ship rate:** {shippedCount} shipped, {shelvedCount} shelved/composted, {activeCount} in progress

      IF projectsWithoutAutopsies is not empty:
        > Note: {N} projects lack autopsies ({names}). Cause analysis is based on available data only.

      {Narrative: which types ship vs die, any visible patterns}

    ---

    ## 3. Completion Correlations

    IF completionCorrelations is null:
      Not enough projects to identify completion patterns yet. Need 2+ with different outcomes.

    ELSE:
      {Narrative: what predicts shipping based on available data}

      **Shipped projects tend to:** {patterns}
      **Abandoned projects tend to:** {patterns}

    ---

    ## 4. Deepest Fascination

    > **This is what you keep building toward: {deepestFascination.theme}.**

    {deepestFascination.description}

    It appeared in: {deepestFascination.projects joined by ", "}
    Cumulative intensity: {deepestFascination.cumulativeIntensity}

    {Narrative: why this keeps pulling, what it means for future projects}

    ---

    ## Takeaways

    - {Actionable insight 1: "Your next project ships if..."}
    - {Actionable insight 2: based on abandonment patterns}
    - {Actionable insight 3: based on deepest fascination}

    IF isSparseData:
      These are preliminary observations. Run `/autopsy` on more projects to sharpen the signal.
}

// -- HELPER FUNCTIONS -------------------------------------------------------------------

map_intensity(intensity_string) {
  MATCH intensity_string:
    "low"    => RETURN 1
    "medium" => RETURN 3
    "high"   => RETURN 5
    _        => RETURN 3    // safe default
}

phase_to_completion(phase) {
  MATCH phase:
    0 => RETURN 10
    1 => RETURN 25
    2 => RETURN 40
    3 => RETURN 55
    4 => RETURN 70
    5 => RETURN 85
    6 => RETURN 100
    _ => RETURN 0
}
