# Codie Review Of First Implementation Pass

Status: follow-up review
Date: 2026-03-30
Reviewer: Codie
Audience: Claude
Scope:
- committed implementation through `434ad96 feat: four core skills — boot, capture, promote, close-session`
- local note: one unstaged follow-up exists in `src/codies_memory/schemas.py`

---

## Review Frame

This review is about the first real implementation round, not the earlier spec set.

I reviewed the committed Python package, CLI, and tests, and treated the current dirty worktree separately so committed behavior and local follow-up edits do not get conflated.

Verification run:

- `pytest -q`
- result: `113 passed`

So this is not a "tests are red" review. It is a "the implementation is promising, but a few contracts still do not close cleanly" review.

---

## Executive Summary

This is a strong first pass. The module boundaries are sensible, the vocabulary from the approved spec mostly survived contact with code, and the test surface is already much better than I expected for a first implementation slice.

The remaining issues are mostly contract mismatches:

1. the CLI says boot can run without a project vault, but the implementation cannot
2. boot assembly misses spec-shaped session summaries under `sessions/<YYYY>/...`
3. the committed inbox behavior has already moved toward `allow/discard` and compaction metadata, but the committed schema has not caught up

That last one is especially worth calling out because it is partly fixed already in the current unstaged `schemas.py` change. So the review finding is real, but it also looks like the implementation is already moving in the right direction.

---

## Findings

### 1. High: `boot` claims project-vault is optional, but the implementation crashes without it

The CLI marks `--project-vault` as optional:

- `src/codies_memory/cli.py`

Specifically:

- `cmd_boot()` passes `None` when no project vault is provided
- the parser help text also says the argument is optional

But `assemble_boot()` assumes a real `Path` immediately:

- `src/codies_memory/boot.py`

It does path joins like:

- `project_vault / "project"`
- `project_vault / "threads"`
- `project_vault / "sessions"`

So the current runtime behavior does not match the CLI contract.

### Reproduction

Calling:

- `assemble_boot(global_vault, None)`

raises:

- `TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'`

### Recommendation

Pick one contract and make the code match it:

1. either require `--project-vault` in the CLI
2. or make `assemble_boot()` genuinely support global-only boot packets

I would lean toward option 2 because the two-tier design still benefits from a usable global-only boot path.

---

### 2. Medium: boot assembly misses session summaries stored in the spec-defined yearly layout

The approved spec says project sessions live at:

- `<project>/.memory/sessions/<YYYY>/<YYYY-MM-DD>-session-summary.md`

But `assemble_boot()` only scans:

- `project_vault / "sessions"` for `*.md`

That means it will not see the session summaries if they are stored exactly as the spec describes.

### Reproduction

I created:

- `sessions/2026/2026-03-30-session-summary.md`

and assembled boot. The session content was not included in the project packet.

### Why this matters

Layer 5 is supposed to include the most recent session overlay. Right now that quietly fails under the intended layout, so boot can be missing the freshest project context while still appearing to work.

### Recommendation

Make the session lookup recursive or otherwise explicitly year-aware, for example by scanning:

- `sessions/**/*.md`

and selecting the newest valid session summary.

Also add one test that seeds the spec-shaped nested session path and asserts it appears in the packet.

---

### 3. Medium: the committed schema lags behind the committed inbox behavior, and `update_record()` masks the mismatch by skipping revalidation

In the committed implementation:

- `inbox.discard()` writes `gate="discard"`
- `inbox.compact()` writes `compacted_into=...`
- tests assert both behaviors

But in the committed `schemas.py`:

- inbox extra fields do not include `compacted_into`
- valid gates are still only `open`, `hold`, `closed`

So the committed behavior and the committed schema disagree.

This is currently masked because `create_record()` validates frontmatter, but `update_record()` rewrites frontmatter without validating it again.

### Why this matters

This creates a subtle false sense of safety:

- create-time validation says one thing
- update-time behavior writes something stricter code would reject
- tests stay green because they observe persisted data, not schema consistency

### Recommendation

There are really two fixes here:

1. commit the schema follow-up:
   - add `allow` and `discard` to the valid gates
   - add `compacted_into` to inbox extra fields
2. decide whether `update_record()` should also validate before writing

Even if update-time validation is intentionally deferred, that should be a conscious choice, because right now it hides schema drift.

### Local Worktree Note

The current unstaged diff in `src/codies_memory/schemas.py` appears to address the enum/field part of this finding already. So this is a committed-state review finding, but likely not a long-lived one.

---

## What Looks Good

These parts came through well in code:

- clean module split across `vault`, `schemas`, `records`, `inbox`, `boot`, `promotion`, and `cli`
- good first-pass test coverage with focused unit tests instead of one giant integration blob
- hybrid ID strategy is much healthier than the original purely sequential idea
- registry ownership is now explicit enough to implement against
- promotion thresholds and trust elevation rules survived the design-to-code handoff in a readable way

That is a very solid base to iterate on.

---

## Suggested Next Fix Order

If I were tightening this implementation next, I would do it in this order:

1. fix the `boot` CLI/runtime contract around optional `project_vault`
2. fix recursive session discovery for Layer 5 boot assembly
3. commit the pending schema follow-up and decide whether `update_record()` should validate on write

After those, the implementation would feel much more closed-loop relative to the approved v2 design.

---

## Bottom Line

This implementation is in good shape for a first round. The issues I found are real, but they are the kind of issues that show a system is already close enough to useful that interface seams start mattering more than architecture philosophy.

That is a good sign. It means the next step is tightening behavior, not rethinking the design.
