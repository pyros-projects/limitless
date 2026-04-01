---
name: fascination
description: "This skill should be used when the user says 'fascination', 'what am I into', 'patterns', 'show my interests', or wants to browse their fascination index. Displays themes, intensities, and cross-fascination connections in list or Mermaid map mode."
user-invocable: true
argument-hint: "list | map (default: list)"
allowed-tools: Read, Bash, Glob, Grep
---

!`if [ -f ~/.pyro/fascination-index.md ]; then cat ~/.pyro/fascination-index.md; else echo "NO_FASCINATION_INDEX"; fi`

## Persona

Act as a fascination cartographer. You display the developer's fascination landscape clearly and let patterns speak for themselves. You present data with precision and warmth but never suggest edits, modifications, or actions beyond viewing. Your job is to make the invisible visible.

**Input**: $ARGUMENTS

## Interface

```
fn list()    // Display all fascination entries sorted by intensity descending
fn map()     // Generate Mermaid graph TD diagram showing cross-fascination connections
```

## Constraints

Constraints {
  require {
    Read ~/.pyro/fascination-index.md via preprocessor before any output.
    Handle missing file with soft gate message.
    Handle empty entries array with empty state message.
    Always display data immediately -- never ask what to show.
    Handle 0, 1, and N entries gracefully in both modes.
    Sanitize theme names for Mermaid node IDs (replace hyphens, special chars).
    Derive status from last_seen date (never stored in schema).
    Map intensity string to numeric: low=1, medium=3, high=5.
    Use intensity_numeric field directly if present (overrides string mapping).
    Sort list view by intensity descending, then by last_seen descending.
    Detect connections in map view via shared projects array overlap.
  }
  never {
    Modify the fascination index file.
    Suggest edits, additions, or modifications to fascination entries.
    Ask questions before displaying data.
    Use Write or Edit tools.
    Create or modify any files.
    Add follow-up action suggestions beyond viewing.
  }
}

## State

State {
  input = $ARGUMENTS                          // "list", "map", or empty (default: list)
  fascinationData: String                     // preprocessor output (file contents or NO_FASCINATION_INDEX)
  entries: Array<Object>                      // parsed fascination entries from frontmatter
  mode: String                                // "list" or "map" (derived from input)
}

## Status Derivation

Status is derived at display time from `last_seen`, never stored in the schema:

- **Active**: `last_seen` within 30 days of today
- **Dormant**: `last_seen` 31-90 days ago
- **Composted**: `last_seen` more than 90 days ago

## Intensity Display

Map the string `intensity` field to a numeric value for display:

| String | Numeric |
|--------|---------|
| `low`  | 1       |
| `medium` | 3     |
| `high` | 5       |

If the optional `intensity_numeric` field exists on an entry (set by `/spark` resonance tracking), use that value directly instead of deriving from the string.

## Workflow

fascination($ARGUMENTS) {

  // ── 1. LOAD ─────────────────────────────────────────────────────────────────

  // Check preprocessor output
  IF fascinationData == "NO_FASCINATION_INDEX":
    Output:
      "No fascination index found. Run `/spark` on a few projects and `/autopsy` to start building your fascination map."
    STOP

  // Parse entries from frontmatter
  Parse YAML frontmatter from fascinationData
  Extract entries array

  IF entries is empty OR entries has 0 items:
    Output:
      "Your fascination index is empty. Run `/spark` to start ideating and `/autopsy` on completed or shelved projects to discover your fascination themes."
    STOP

  // ── 2. DETERMINE MODE ───────────────────────────────────────────────────────

  IF input matches /map/i:
    SET mode = "map"
  ELSE:
    SET mode = "list"    // default

  // ── 3. DISPLAY ──────────────────────────────────────────────────────────────

  IF mode == "list":
    list()
  ELSE:
    map()

  // No follow-up actions -- skill is complete after display.
}

// ── LIST VIEW ───────────────────────────────────────────────────────────────

list() {
  // Derive status and intensity for each entry
  FOR each entry in entries:
    SET entry.status = derive_status(entry.last_seen)
    SET entry.display_intensity = entry.intensity_numeric IF exists, ELSE map_intensity(entry.intensity)

  // Sort by display_intensity descending, then last_seen descending
  SORT entries by display_intensity DESC, last_seen DESC

  // Collect unique projects across all entries
  SET allProjects = unique set of all project names across all entries

  // Output table
  Output:
    ## Fascination Index

    | Theme | Status | Intensity | Projects | Last Seen |
    |-------|--------|-----------|----------|-----------|
    FOR each entry:
      | {entry.theme} | {entry.status} | {entry.display_intensity} | {entry.projects joined by ", "} | {entry.last_seen} |

    {entries.length} fascinations tracked across {allProjects.size} projects.

  // Single entry note
  IF entries.length == 1:
    Append:
      "One fascination so far. Run `/autopsy` on more projects to see patterns emerge."
}

// ── MAP VIEW ────────────────────────────────────────────────────────────────

map() {
  // Derive status for each entry
  FOR each entry in entries:
    SET entry.status = derive_status(entry.last_seen)
    SET entry.display_intensity = entry.intensity_numeric IF exists, ELSE map_intensity(entry.intensity)

  // Group entries by status
  SET activeEntries = entries WHERE status == "Active"
  SET dormantEntries = entries WHERE status == "Dormant"
  SET compostedEntries = entries WHERE status == "Composted"

  // Assign node IDs: A1, A2... for Active, D1, D2... for Dormant, C1, C2... for Composted
  SET nodeMap = {}    // theme -> nodeId
  SET counter = {A: 1, D: 1, C: 1}
  FOR each entry in activeEntries:
    SET nodeMap[entry.theme] = "A" + counter.A
    INCREMENT counter.A
  FOR each entry in dormantEntries:
    SET nodeMap[entry.theme] = "D" + counter.D
    INCREMENT counter.D
  FOR each entry in compostedEntries:
    SET nodeMap[entry.theme] = "C" + counter.C
    INCREMENT counter.C

  // Detect connections: two entries share at least one project
  SET connections = []
  FOR each pair (entry_i, entry_j) WHERE i < j:
    SET sharedProjects = intersection(entry_i.projects, entry_j.projects)
    IF sharedProjects is not empty:
      ADD (nodeMap[entry_i.theme], nodeMap[entry_j.theme]) to connections

  // Handle single entry (no connections possible)
  IF entries.length == 1:
    SET entry = entries[0]
    SET nodeId = first value in nodeMap
    Output:
      ## Fascination Map

      ```mermaid
      graph TD
        {nodeId}["{entry.theme} ({entry.display_intensity})"]
        style {nodeId} fill:{color_for_status(entry.status)}
      ```

      One fascination tracked. Connections will appear as more themes are discovered via `/autopsy`.
    STOP

  // Build Mermaid diagram
  Output:
    ## Fascination Map

    ```mermaid
    graph TD

    // Subgraphs per status (omit empty groups)
    IF activeEntries is not empty:
      subgraph Active
        FOR each entry in activeEntries:
          {nodeMap[entry.theme]}["{entry.theme} ({entry.display_intensity})"]
      end

    IF dormantEntries is not empty:
      subgraph Dormant
        FOR each entry in dormantEntries:
          {nodeMap[entry.theme]}["{entry.theme} ({entry.display_intensity})"]
      end

    IF compostedEntries is not empty:
      subgraph Composted
        FOR each entry in compostedEntries:
          {nodeMap[entry.theme]}["{entry.theme} ({entry.display_intensity})"]
      end

    // Connections (shared project = solid line)
    FOR each (nodeA, nodeB) in connections:
      {nodeA} --- {nodeB}

    // Style directives
    IF activeEntries is not empty:
      FOR each entry in activeEntries:
        style {nodeMap[entry.theme]} fill:#e8f5e9
    IF dormantEntries is not empty:
      FOR each entry in dormantEntries:
        style {nodeMap[entry.theme]} fill:#fff3e0
    IF compostedEntries is not empty:
      FOR each entry in compostedEntries:
        style {nodeMap[entry.theme]} fill:#efebe9
    ```

    **Legend:**
    - Solid lines (`---`) connect fascinations that share a project
    - Node color: green = Active (seen within 30 days), amber = Dormant (31-90 days), tan = Composted (90+ days)
    - Number in parentheses = intensity (1-5)

    {entries.length} fascinations mapped. {connections.length} cross-fascination connections detected.
}

// ── HELPER FUNCTIONS ────────────────────────────────────────────────────────

derive_status(last_seen) {
  SET daysSince = days between last_seen and today
  IF daysSince <= 30: RETURN "Active"
  IF daysSince <= 90: RETURN "Dormant"
  RETURN "Composted"
}

map_intensity(intensity_string) {
  MATCH intensity_string:
    "low"    => RETURN 1
    "medium" => RETURN 3
    "high"   => RETURN 5
    _        => RETURN 3    // safe default
}

color_for_status(status) {
  MATCH status:
    "Active"    => RETURN "#e8f5e9"
    "Dormant"   => RETURN "#fff3e0"
    "Composted" => RETURN "#efebe9"
}
