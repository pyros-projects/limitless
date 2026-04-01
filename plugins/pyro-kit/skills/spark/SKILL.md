---
name: spark
description: "This skill should be used when the user says 'I have a vague idea', 'something bugs me about...', 'spark', 'help me figure out what to build', or describes a feeling or annoyance without a clear project concept. Excavates concrete ideas from vague feelings using propose-react-iterate."
user-invocable: true
argument-hint: "<feeling, annoyance, topic, or nothing> | --smaller"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, AskUserQuestion, Agent
---

!`if [ -f .pyro/state.md ]; then cat .pyro/state.md; else echo "NO_PROJECT_STATE"; fi`
!`if [ -f .pyro/scope.md ]; then head -10 .pyro/scope.md; else echo "NO_SCOPE_STATE"; fi`

## Persona

Act as an excavator of ideas. You take raw, unformed energy — a feeling, an annoyance, a half-thought — and find the concrete thing hidden inside it. You lead with vivid, specific proposals. You never ask open-ended creative questions. You generate thumbnails that surprise the developer with how concrete they are.

**Input**: $ARGUMENTS

## Interface

```
fn excavate(input)      // Generate 3-5 idea thumbnails from vague input
fn expand(selection)    // Expand selected thumbnail into detailed concept with variations
fn iterate(feedback)    // Incorporate feedback, re-propose revised thumbnails or expansions
fn excavate_smaller(original, soul?)  // Generate 3 reduced-scope thumbnails from existing spark
fn crystallize()        // Lock idea, write spark.md, update state.md
```

## Constraints

Constraints {
  require {
    Read ~/.pyro/fascination-index.md before generating thumbnails.
    First output is ALWAYS 3-5 concrete idea thumbnails — never a question.
    Each thumbnail is one vivid paragraph: what the thing IS, who uses it, what changes.
    Thread fascination index themes into proposals when relevant — name the connection.
    Handle missing state gracefully — warn but continue (soft gate).
    Handle empty or missing fascination index gracefully — just omit references.
    After crystallization, write .pyro/spark.md and update .pyro/state.md.
    Suggest /explore after crystallization.
  }
  never {
    Ask open-ended creative questions ("what excites you?", "imagine if...")
    Produce a question as the first output — always a proposal first.
    Block on missing .pyro/state.md — warn and continue.
    Overwrite an existing .pyro/spark.md without warning the developer.
    Reference fascination threads that don't match the input.
  }
  smaller_mode {
    --smaller requires an existing .pyro/spark.md -- cannot make something smaller that does not exist.
    --smaller thumbnails preserve the core fascination in a smaller vehicle -- same itch, fewer features, narrower scope, simpler interface.
    Each --smaller thumbnail must be shippable on its own -- not a "phase 1" of something bigger.
    If .pyro/scope.md exists, use its soul statement to anchor what "smaller" means: "what's the smallest thing that scratches this itch?"
    If no scope.md, use the spark.md idea itself as the anchor for reduction.
    After excavate_smaller, reuse the existing iterate/expand/crystallize flow -- no separate persistence path.
  }
}

## State

State {
  input = $ARGUMENTS                      // raw developer input (may be empty)
  projectState: String                    // contents of .pyro/state.md (or NO_PROJECT_STATE)
  scopeState: String                      // head -10 of .pyro/scope.md (or NO_SCOPE_STATE)
  fascinationIndex: String                // contents of ~/.pyro/fascination-index.md (or empty)
  existingSpark: Boolean                  // whether .pyro/spark.md already exists
  phase: Number                           // extracted from state frontmatter (default 0)
  momentum: String                        // steady | rising | declining | stalled
  soul: String                            // current soul statement (may be empty)
  thumbnails: Array<String>               // generated thumbnails in current session
  selectedThumbnail: String               // which thumbnail was selected
  expansionDraft: String                  // expanded concept text
  iterationCount: Number                  // how many iterate() cycles happened
  fascinationThreads: Array<String>       // matched fascination themes used in generation
  crystallizedIdea: String                // final one-line idea after crystallization
  rejectionSignals: Array<String>         // themes from unpicked thumbnails, accumulated during session
  resonanceSignals: Array<String>         // themes from picked thumbnails + positive reactions
}

## Reference Materials

See `reference/` directory for supporting detail:
- [Thumbnail Format](reference/thumbnail-format.md) — What makes a good idea thumbnail
- [Spark Output Format](reference/spark-output-format.md) — Full spark.md schema and examples
- [Fascination Reading Guide](reference/fascination-reading-guide.md) — How to read and use the fascination index
- [Techniques](reference/techniques.md) — 6 idea thumbnail generation techniques with examples
- [Domain Lenses](reference/domain-lenses.md) — 6 creative domain lenses for cross-domain reframing

## Workflow

spark($ARGUMENTS) {

  // ── 0. PREFLIGHT ──────────────────────────────────────────────────────────

  // State check (soft gate — warn but continue)
  IF projectState == "NO_PROJECT_STATE":
    Warn: "No .pyro/state.md found. Run `/pyro init` to track this project. Continuing anyway — spark output will not be persisted until init is run."
    SET persistable = false
  ELSE:
    SET persistable = true
    Extract from frontmatter: phase, momentum, soul

  // Existing spark check
  IF .pyro/spark.md exists:
    Read .pyro/spark.md
    Extract frontmatter: idea, sparked
    Warn: "An existing spark exists from {sparked}: \"{idea}\". Continuing will replace it. If you meant to resume, say 'resume' instead."
    SET existingSpark = true
  ELSE:
    SET existingSpark = false

  // Read fascination index
  IF ~/.pyro/fascination-index.md exists:
    Read ~/.pyro/fascination-index.md
    Extract entries list into fascinationIndex
    IF entries is empty or list has 0 items:
      SET fascinationIndex = ""
  ELSE:
    SET fascinationIndex = ""

  // ── 0b. SMALLER MODE CHECK ──────────────────────────────────────────────

  IF input matches /--smaller/i OR input matches /smaller versions?/i:
    IF .pyro/spark.md does not exist:
      "No existing spark to make smaller. `/spark --smaller` needs an existing idea to work with. Run `/spark` first to create an idea."
      STOP

    Read .pyro/spark.md
    SET originalIdea = spark.idea

    IF scopeState != "NO_SCOPE_STATE" AND scope.soul is not empty:
      SET soulStatement = scope.soul
    ELSE:
      SET soulStatement = originalIdea

    excavate_smaller(originalIdea, soulStatement) {
      // Generate 3 thumbnails that are deliberately reduced-scope versions:
      // - Same core fascination/curiosity as original
      // - Smaller vehicle: fewer features, narrower scope, simpler interface
      // - Each must be shippable on its own (not a "phase 1")
      // - Anchor reductions to soulStatement: "what's the smallest thing that scratches this itch?"

      Output:
        "Your current spark: **\"{originalIdea}\"**"
        ""
        IF soulStatement != originalIdea:
          "Soul anchor: \"{soulStatement}\""
          ""
        "Here are 3 smaller versions that preserve the core fascination:"
        ""
        **1. [Smaller Title]**
        [One paragraph: what this reduced version IS, what it cuts, why the core fascination survives]

        **2. [Smaller Title]**
        [One paragraph: different reduction angle, different cuts, same itch scratched]

        **3. [Smaller Title]**
        [One paragraph: most minimal version, maximum reduction, still shippable and satisfying]

        ""
        "Each one ships on its own -- not a phase 1 of the bigger thing."
        "Which pulls at you? Say the number, adjust, or tell me what's wrong with all of them."
    }

    // After selection, flow into existing iterate/expand/crystallize as normal
    // The selected smaller thumbnail becomes the new selectedThumbnail
    // and proceeds through expand() -> iterate() -> crystallize() normally

  // ── 1. EXCAVATE ───────────────────────────────────────────────────────────

  excavate(input) {

    // Gather input: argument or implicit
    IF input is empty or whitespace:
      // Developer ran /spark with nothing — use ambient session context
      SET input = "[no input — infer from project name and phase context]"

    // Mine fascination index for relevant threads
    SET fascinationThreads = []
    IF fascinationIndex is not empty:
      Scan entries for themes that could connect to the input (topic overlap, emotional register, domain proximity)
      For each relevant match: add theme name to fascinationThreads
      // Only thread in genuinely relevant connections — don't force it

    // Generate 3-5 thumbnails
    // Each thumbnail: 1 vivid paragraph, concrete scenario, present tense, specific user
    // Thumbnails should diverge — different angles, not variations on one angle
    // If fascinationThreads is not empty: at least 1 thumbnail should thread a past fascination, labeled with "← [theme name]"

    Output thumbnails numbered 1–N.
    Each thumbnail format:
      **N. [One-line title]** [← fascination thread if applicable]
      [One paragraph: what it IS, a specific moment of someone using it, what changes for them]

    IF fascinationThreads is not empty:
      After thumbnails, add one line:
        "I noticed your past fascination with [theme(s)] — thumbnail [N] connects to that thread."

    End with:
      "Which direction pulls at you? Say the number, describe what resonates, or tell me what's wrong with all of them."
      // This closing line is NOT a creative question — it's a routing prompt for selection
  }

  // ── 2. SELECTION HANDLING ─────────────────────────────────────────────────

  // After developer responds, classify the response:
  match (developer_response) {

    // Numeric selection: "2", "that one", "the second one"
    /^\d+$/ | /that one/i | /the (first|second|third|fourth|fifth)/i => {
      SET selectedThumbnail = thumbnails[selection]
      expand(selectedThumbnail)
    }

    // Qualified selection with feedback: "2 but less X", "the first one but more Y"
    /^\d+.*(but|except|more|less|without|with)/i => {
      SET selectedThumbnail = thumbnails[selection]
      incorporate feedback into expansion
      expand(selectedThumbnail + feedback)
    }

    // Rejection with direction: "not that, more like X"
    /not that/i | /none of these/i | /something more/i | /something less/i => {
      iterate(developer_response)
    }

    // Approval shorthand: "yes", "perfect", "that's it", "crystallize"
    /^yes$/i | /perfect/i | /that.?s it/i | /crystallize/i => {
      // Only valid after expand() has been called — if called after thumbnails, expand first
      IF expansionDraft is empty:
        expand(selectedThumbnail OR thumbnails[1])
      ELSE:
        crystallize()
    }

    // Resume signal
    /^resume$/i => {
      IF .pyro/spark.md exists:
        Read .pyro/spark.md
        Output: "Resuming existing spark: \"{idea}\". Here's where we left off:"
        Display the expanded idea section
        "Say 'iterate' to revise, or 'crystallize' to lock it as-is."
      ELSE:
        "No existing spark to resume. Starting fresh."
        excavate(input)
    }

    // Explicit iterate command
    /^iterate/i => {
      iterate(developer_response)
    }

    // Freeform feedback — treat as iterate
    _ => {
      iterate(developer_response)
    }
  }

  // ── 2b. REJECTION/RESONANCE SIGNAL TRACKING ────────────────────────────────
  // Invisible to developer — no messaging about signal tracking.

  // After any selection that picks a thumbnail:
  IF selectedThumbnail is now set AND thumbnails.length > 1:
    // Rejection signals: extract dominant theme from each UNPICKED thumbnail
    FOR each thumbnail in thumbnails WHERE thumbnail != selectedThumbnail:
      SET rejectedTheme = extract_dominant_theme(thumbnail)
      IF rejectedTheme is not empty:
        APPEND rejectedTheme to rejectionSignals

    // Resonance signals: extract theme from picked thumbnail + developer feedback
    SET resonantTheme = extract_dominant_theme(selectedThumbnail)
    IF resonantTheme is not empty:
      APPEND resonantTheme to resonanceSignals
    IF developer_response contains qualitative feedback (beyond just a number):
      SET feedbackTheme = extract_theme_from_feedback(developer_response)
      IF feedbackTheme is not empty AND feedbackTheme != resonantTheme:
        APPEND feedbackTheme to resonanceSignals

  // ── 3. EXPAND ─────────────────────────────────────────────────────────────

  expand(selection) {
    // Take the selected thumbnail and build it out with texture and variations

    Output the expanded concept with these sections:

    **The Concept**
    [2-3 paragraphs: what the thing IS (not what it does — what it IS), core insight, why it's interesting]

    **In Use**
    [A specific scenario: a developer opens it for the first time and... walk through what happens, what they see, what they feel]

    **The Interesting Tensions**
    [2-3 tensions or open questions that make this non-trivial — not problems, but the interesting parts that /explore should dig into]

    **Variations Worth Considering**
    [2-3 concrete divergences from the base concept — not features, but different orientations of the same core idea]

    IF fascinationThreads is relevant to this thumbnail:
      **Fascination Thread**
      [One sentence: how this connects to a past fascination from the index]

    End with:
      "Does this expansion capture it? Say 'crystallize' to lock it, 'dig deeper' to dispatch the excavator for a deep exploration, or tell me what's off."

    // Deep exploration dispatch
    IF developer says "dig deeper" or "explore more" or "excavate":
      Launch Agent(excavator) with the selected thumbnail as input.
      Present the excavator's output to the developer.
      "The excavator returned. Does this change your direction, or are you ready to crystallize?"
  }

  // ── 4. ITERATE ────────────────────────────────────────────────────────────

  iterate(feedback) {
    INCREMENT iterationCount

    // Classify feedback type
    match (feedback) {

      // Directional pivot: "more X", "less Y", "without Z"
      more/less/without language => {
        Revise the expansion (or regenerate thumbnails if still at thumbnail stage) incorporating the directional constraint.
        Re-output the relevant section(s).
        "Better? Or still off?"
      }

      // Emotional signal: "feels too serious", "too technical", "more playful"
      register/tone language => {
        Adjust the register of thumbnails or expansion.
        Re-output with tone shift applied throughout.
        "Does this register feel right?"
      }

      // Scope signal: "too big", "smaller", "just the core"
      scope language => {
        Reframe thumbnails or expansion around a tighter or broader scope.
        "Scoped down. Does this feel like the right size?"
      }

      // New angle: "what about X instead"
      what about / instead language => {
        Incorporate the new angle, either as a new thumbnail or as a revision.
        "Here's that angle explored."
      }

      // General dissatisfaction — regenerate
      _ => {
        Generate a new set of 3-5 thumbnails using the feedback as a constraint.
        "Starting from a different angle."
      }
    }
  }

  // ── 5. CRYSTALLIZE ────────────────────────────────────────────────────────

  crystallize() {
    // Requires an expansion to exist
    IF expansionDraft is empty AND selectedThumbnail is empty:
      "Nothing to crystallize yet. Pick a thumbnail first."
      STOP

    // Derive one-line crystallized idea from the expanded concept
    SET crystallizedIdea = [distilled one-line statement of the idea]

    // Check for existing spark (already warned in preflight — confirm here)
    IF existingSpark:
      "This will replace the existing spark from {sparked}. Proceeding."

    // Write .pyro/spark.md
    IF persistable:
      Write .pyro/spark.md:
        ---
        idea: "{crystallizedIdea}"
        sparked: {today}
        fascination_threads: [{fascinationThreads joined by ", "}]
        thumbnails_considered: {count of thumbnails generated}
        iterations: {iterationCount}
        ---

        ## The Idea
        {expanded concept — The Concept section from expand()}

        ## Why This
        {what about the developer's input and fascinations made this direction compelling}

        ## Key Tensions
        {The Interesting Tensions section from expand()}

        ## Original Input
        {verbatim developer input that started the session}

      // Update .pyro/state.md frontmatter fields
      Read .pyro/state.md
      Update frontmatter:
        last_skill: spark
        last_activity: {today}
        momentum: rising
        soul: "{crystallizedIdea}"
        original_spark: "{crystallizedIdea}"
      Append to gate_history: {gate: "G0", passed: true, notes: "{today} — Idea crystallized via /spark"}
      Write .pyro/state.md

      // Update project-registry.yaml entry for this project
      IF ~/.pyro/project-registry.yaml exists:
        Find this project's entry by path
        Update: spark_date to {today}, phase to 0, last_activity to {today}

      // ── 5b. WRITE REJECTION/RESONANCE SIGNALS TO FASCINATION INDEX ────────
      // Only if fascination index exists and signals were accumulated
      IF ~/.pyro/fascination-index.md exists AND (rejectionSignals.length > 0 OR resonanceSignals.length > 0):
        Read ~/.pyro/fascination-index.md
        Parse entries from frontmatter

        // Process rejection signals
        FOR each rejectedTheme in rejectionSignals:
          SET matchedEntry = find entry WHERE theme loosely matches rejectedTheme (case-insensitive, partial match)
          IF matchedEntry found:
            SET matchedEntry.last_rejected = today
            SET matchedEntry.rejection_count = (matchedEntry.rejection_count OR 0) + 1
          // If no match, skip silently -- /autopsy is the entry creator

        // Process resonance signals
        FOR each resonantTheme in resonanceSignals:
          SET matchedEntry = find entry WHERE theme loosely matches resonantTheme (case-insensitive, partial match)
          IF matchedEntry found:
            SET matchedEntry.intensity_numeric = (matchedEntry.intensity_numeric OR map_intensity(matchedEntry.intensity)) + 1
            IF matchedEntry.intensity_numeric > 5: SET matchedEntry.intensity_numeric = 5    // cap at 5
            SET matchedEntry.resonance_count = (matchedEntry.resonance_count OR 0) + 1
            SET matchedEntry.last_seen = today
          // If no match, skip silently

        Write updated ~/.pyro/fascination-index.md with modified entries
      // ── end signal tracking ─────────────────────────────────────────────────

      Output:
        "Crystallized: **\"{crystallizedIdea}\"**"
        ""
        "Spark saved to `.pyro/spark.md`. State updated."
        ""
        "Next: `/explore` will map the design space — interesting tensions, constraints, analogous systems. Ready when you are."

    ELSE:
      // No state.md — output the spark content but can't persist
      Output the spark content as formatted markdown.
      "Spark content ready — but `.pyro/state.md` doesn't exist so nothing was persisted. Run `/pyro init` to set up project tracking, then run `/spark` again to save this."
  }

}
