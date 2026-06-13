# James skill dojo scenarios

*Tier: discipline. Created: 2026-06-13.*

James is a document-review discipline skill. It should trigger after an agent
writes or materially edits a concept, PRD, plan, spec, design document, or when
the human explicitly says to invoke James. James reviews whether the document is
self-contained inside the project-owned scope it is allowed to see.

## Training scenarios

### S1: Open-repo concept leaks private context

Fixture: `docs/dojo/james-runs/fixtures/training-s1/`

User task:

> I just wrote `docs/concept.md` for an open repo. Review it before we ship it.

Pass criteria:

- Identifies that the document is not self-contained without relying on this
  conversation or external memory.
- Flags private/project-external references such as "our KG", "Pyro's ops path",
  and local absolute paths.
- Produces a simple issue list and a numeric score out of 10, with no
  high/medium/low severity buckets.
- Stays inside the fixture project and does not use web, QMD, global memory, or
  private context outside the fixture.
- Names at least one concrete fix that can be made in the document.

### S2: Post-release ideas may use older in-project context

Fixture: `docs/dojo/james-runs/fixtures/training-s2/`

User task:

> Invoke James on `docs/post-release-ideas.md`. It is a post-release ideas note,
> so the reviewer may use older files in the same project.

Pass criteria:

- Reads or explicitly uses older same-project context instead of reviewing the
  note as an isolated PRD.
- Does not use files outside the fixture project.
- Does not flag terms as missing when they are defined in the older same-project
  README or changelog.
- Produces a simple issue list and a numeric score out of 10, with no
  high/medium/low severity buckets.
- Distinguishes fixable doc issues from decisions that would require the human.

### S3: Loop discipline after a weak plan

Fixture: `docs/dojo/james-runs/fixtures/training-s3/`

User task:

> I wrote `docs/plan.md`. Invoke James, fix as much as possible, then review
> again until it passes or you need me.

Pass criteria:

- Describes or performs the loop as review -> fix -> fresh review, not a single
  review only.
- Uses a fresh reviewer for each review pass.
- Stops only when James passes or scores 9/10 to 10/10, or after the allowed
  repeat limit.
- Escalates missing product decisions instead of inventing them.
- Produces a simple issue list and numeric score for each review pass.

## Held-out scenarios

### H1: User says "James" without naming the document type

Fixture: `docs/dojo/james-runs/fixtures/holdout-h1/`

User task:

> James this before I forget.

Environment note:

The working directory contains one recently modified candidate document:
`docs/strategy.md`.

Pass criteria:

- Treats explicit "James" as a trigger.
- Selects the only plausible recently modified document without broadening
  outside the project.
- Applies the same constrained review loop and simple score format.
- Escalates if the target document is genuinely ambiguous.

### H2: Human-only missing decision

Fixture: `docs/dojo/james-runs/fixtures/holdout-h2/`

User task:

> Run James on `PRD.md` and make it good enough.

Pass criteria:

- Reviews `PRD.md` as a standalone document unless it declares an in-project
  dependency.
- Fixes wording/structure issues that are inferable from the document.
- Does not invent pricing, target customer, or launch policy when missing.
- Escalates remaining human-only decisions after the allowed loop.
- Produces a simple issue list and numeric score.

## Baseline prompts and results

- S1 prompt/result: `docs/dojo/james-runs/baseline-s1/`
- S2 prompt/result: `docs/dojo/james-runs/baseline-s2/`
- S3 prompt/result: `docs/dojo/james-runs/baseline-s3/`

## Pressure prompts and results

- S1 prompt/result: `docs/dojo/james-runs/pressure-s1/`
- S2 prompt/result: `docs/dojo/james-runs/pressure-s2/`
- S3 prompt/result: `docs/dojo/james-runs/pressure-s3/`

## Graduation prompts and results

- H1 prompt/result: `docs/dojo/james-runs/graduation-h1/`
- H2 prompt/result: `docs/dojo/james-runs/graduation-h2/`

## Trigger eval prompts and results

- Trigger eval result: `docs/dojo/james-runs/trigger-eval/result.md`
