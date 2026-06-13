---
name: james
description: "This skill should be used after the agent writes or materially edits a concept, PRD, plan, spec, design document, strategy document, or similar planning artifact, and whenever the user says invoke James, run James, James this, or James-review. It reviews whether the document is self-contained inside project-owned scope, persists recipes and review chains under ~/.limitless/james, fixes what can be fixed, then resumes James for re-review until pass. Not for code review, article editing, or writing the initial document."
---

# James — Fresh Eyes For Documents

## What James Does

James is the persistent constrained reviewer for planning documents. James
checks whether a future agent, seeing only the document and the allowed
project-owned context, can understand and act on it without hidden
conversation, private memory, external files, or "you know what I mean"
residue.

James is not a prose polish pass. James protects restartability.

## Mandatory Triggers

Use this skill immediately after you write or materially edit:

- a concept document
- a PRD
- a plan
- a specification
- a design document
- a strategy document
- an architecture or implementation proposal

Also use it whenever the user says "invoke James", "run James", "James this",
"James-review", "ask James", or equivalent.

Do not use James for code review, article voice editing, ordinary research
summaries, or the first drafting pass itself. Write the document first, then
James reviews it.

## Scope Envelope

Before spawning James, decide and state the allowed context envelope.

Rules:

1. **Project-owned only.** James may see files inside the current project root.
   James may not use web search, QMD, global memories, private cross-project
   knowledge, this conversation, or files outside the project.
2. **Standalone docs default narrow.** Concepts, PRDs, plans, specs, design
   docs, and strategy docs are reviewed as primary standalone artifacts:
   target document only, plus file path and project name. Add same-project
   context only when the document explicitly declares a dependency or the user
   explicitly names the context.
3. **Chronological notes may use older project context.** Post-release ideas,
   retrospectives, release notes, migration notes, and follow-up notes may use
   same-project files older than the target. Prefer git history for age; if
   unavailable, use filesystem mtime and state the fallback.
4. **Narrower beats broader.** If the user names a narrower scope, obey it.
   If the user asks for broader context, broader still means project-owned
   only.
5. **Missing context is a finding.** If a claim can only be understood from
   chat history, memory, private paths, or external systems, James flags it.
   Do not broaden the scope to rescue the document.

If the target document is ambiguous, select the only plausible recently changed
planning document. If multiple plausible targets exist, ask the user.

## Output Root, Recipes, And Review Chain

James-owned output lives outside the project by default:

```text
~/.limitless/james/<repo-slug>/<target-slug>/
  recipe.md
  chain.md
  reviews/
    001-initial.md
    002-after-fixes.md
```

- `repo-slug` is the project root basename, slugged to lowercase ASCII.
- `target-slug` is the target document path relative to the project root,
  slugged by replacing path separators with `--` and dropping a common
  markdown/text extension. If two targets collide, append a short hash.
- Use a custom output path only when the user explicitly provides one.
- Never write James review logs into the target project's docs folder by
  implication. The reviewed document stays in the project; James's operational
  output stays in `~/.limitless/james/...`.

Before the first review, create `recipe.md`. Before later reviews, load it.
The recipe is process memory, not evidence. It may store:

- project root
- target document
- document intent
- allowed context envelope
- James output root
- current James subagent/thread id, if available
- next review number
- changelog entries for scope/process changes

Update the recipe when scope, target, intent, or reviewer thread changes. Do
not use the recipe to supply missing product facts to James.

Save every raw James review as an immutable file under `reviews/`. Also update
`chain.md` as an index with review number, review file, score, pass/fail,
fixes recorded, and next action. Do not overwrite older reviews.

## Review Loop

1. **Load or create the recipe.** Derive the default output root, create the
   folder if needed, load any existing `recipe.md`, and determine the next
   review number. State the output root in your working notes or final report.
2. **Resume James, or spawn him once.** If a James subagent/thread already
   exists for the current session, project, or document, resume it. Spawn a new
   James only when no resumable James exists. Subsequent James calls should keep
   using that James thread.
3. **Reset the evidence boundary every call.** Resumed James may remember his
   prior issue list and review calibration, but previous document facts are not
   admissible evidence unless they are inside the current allowed scope. Send the
   target document, allowed scope, and the prompt template in
   `references/review-prompt.md` every time. For review 2+, also send the
   previous saved review and a concise list of fixes the main agent attempted,
   so James can verify what actually changed.
4. **James returns a simple review.** Required format:
   - `Score: X/10`
   - `Passed: yes/no`
   - for review 2+: `Fixed since previous review:` with numbered fixes James
     can verify from the current document and previous review
   - numbered issue list only, with no high/medium/low buckets
   - each issue says whether it is fixable now or needs the human
5. **Persist the review before editing.** Save James's raw review to
   `reviews/001-initial.md` for the first pass, then
   `reviews/<NNN>-after-fixes.md` for later passes. Update `chain.md` after
   every saved review.
6. **Fix what can be fixed.** Safe fixes include adding definitions, replacing
   private names with public/project-local terms, removing local absolute
   paths, declaring dependencies, adding examples, and making acceptance checks
   testable. Do not invent missing product decisions, facts, pricing, launch
   policy, target users, or commitments.
7. **Resume James for the re-review.** Send the updated document, allowed
   scope, previous saved review, and attempted fix summary back to the same
   James thread. Do not spawn a different reviewer just because this is the next
   pass. James's next review must include the fixed section.
8. **Stop only when passed.** Done means James says `Passed: yes` or scores
   9/10 to 10/10.
9. **Respect the hard loop cap.** After the first review, you get at most three
   fix passes. Count every edit pass after a James review. If the third
   re-review still scores below 9/10, do not make a fourth edit to chase the
   score. Escalate the remaining issues.
10. **Escalate when needed.** If the remaining issues cannot be improved without
   human information, stop and show the unresolved questions.

If subagents are unavailable, run the same loop yourself as a degraded James
pass and say that the independent-review guarantee was unavailable.

## What James Looks For

James should especially catch:

- private project names, local paths, or personal shorthand in public docs
- references to "as discussed", "our KG", "the usual flow", "the previous
  thing", or similar hidden context
- acceptance criteria that are vibes instead of observable checks
- terms that are used before being defined
- dependencies on files outside the allowed scope
- plans that cannot be implemented because the document omits authority,
  input/output shape, target user, or success criteria
- docs that assume the author will be present to explain them later

James should not demand every document become huge. A short doc can pass if its
scope is explicit and future action can proceed from the allowed context.

## Final Report

After the loop, tell the user:

- target document
- James output root
- final score
- number of review passes
- changes made
- unresolved human questions, if any

Keep it brief. The document and the James reviews carry the detail.
