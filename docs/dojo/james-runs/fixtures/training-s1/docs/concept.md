# Idea Seed Evaluator Concept

## Goal

Build a small evaluator that turns a folder of raw idea candidates into a
project-local import batch. A future agent should be able to point the evaluator
at one run directory, score each candidate with the rubric below, and separate
import-ready ideas from rejected or contaminated ones without relying on private
paths or prior conversation.

## Terms

- **Idea candidate:** One raw note, JSON file, markdown file, or text file that
  proposes a possible idea to add to the project graph.
- **Run directory:** The directory supplied by the operator. It contains the raw
  idea candidates for one evaluation pass.
- **Project graph:** The project's own collection of accepted idea records. For
  this concept, accepted output is written under `ops/idea-import/accepted/`
  relative to the project root.
- **Rejected item:** A candidate that is understandable but should not enter the
  project graph yet. Rejected output is written under
  `ops/idea-import/rejected/` relative to the project root.
- **Contaminated item:** A candidate whose core value depends on uncitable or
  unreliable claims, such as unverified social-media rumors, private personal
  information, or claims the operator cannot publicly source.

## Scoring Rubric

Each candidate receives these labels:

- **Novelty:** `high`, `medium`, or `low`. High means the candidate is not a
  duplicate of another accepted candidate in the same run and introduces a
  meaningfully different mechanism, audience, or workflow.
- **Graph fit:** `strong`, `partial`, or `none`. Strong means the candidate can
  become a durable project graph record with a title, short claim, evidence
  note, and at least one relation to existing project themes supplied in the
  candidate itself.
- **Availability-adjusted value:** `high`, `medium`, or `low`. High means the
  candidate appears useful and the candidate text includes enough evidence,
  examples, or implementation hints for a future agent to act on it.
- **Contamination:** `clean` or `contaminated`. Contaminated candidates are never
  accepted automatically.

A candidate is accepted when novelty is `high` or `medium`, graph fit is
`strong`, availability-adjusted value is `high` or `medium`, and contamination
is `clean`.

## Flow

1. Accept a run directory path from the operator.
2. Read all raw candidate files in that run directory.
3. For each candidate, extract a title, summary, source or evidence note, and
   proposed graph relation. If any field is missing, reject the candidate with a
   reason instead of guessing.
4. Apply the scoring rubric.
5. Write accepted candidates to `ops/idea-import/accepted/` as markdown files.
6. Write rejected and contaminated candidates to `ops/idea-import/rejected/`
   with the score labels and rejection reason.

## Output Shape

Each accepted markdown file should include:

```markdown
# <Idea title>

## Summary
<One paragraph summary of the idea.>

## Evidence
<Source or evidence note copied from the candidate.>

## Graph Relation
<The relation or project theme this idea should connect to.>

## Scores
- Novelty: high|medium|low
- Graph fit: strong|partial|none
- Availability-adjusted value: high|medium|low
- Contamination: clean|contaminated
```

## Acceptance

- Given a run directory containing at least one candidate file, the evaluator
  creates `ops/idea-import/accepted/` and `ops/idea-import/rejected/` if they do
  not already exist.
- Every candidate produces either an accepted markdown file or a rejected
  markdown file with explicit score labels.
- No output contains absolute local paths or personal machine references.
- A candidate marked `contaminated` is always written to the rejected directory
  with the contamination reason.
- A candidate with missing title, summary, evidence note, or graph relation is
  rejected with a missing-field reason.
