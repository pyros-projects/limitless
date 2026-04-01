---
title: Codie Review Of Current Repo State
date: 2026-04-01
reviewer: Codie
type: review
scope: current implementation in `src/`, `tests/`, and `skills/`
---

# Codie Review Of Current Repo State

This is a code-review style pass over the current `codies-memory` repo state.

Review posture:

- prioritize behavioral risks and contract drift
- focus on what Claude should fix next
- treat passing tests as useful evidence, not proof that the operator surface is correct

Verification run during review:

```bash
uv run pytest -q
```

Result:

- `116 passed`

---

## Findings

### 1. High: `status` lies about fresh inbox items

Current behavior:

- `codies-memory status <project-vault>` only shows `aging` and `stale` inbox records
- if neither list has entries, it prints `Inbox is clean.`

That means a project can have active inbox items and still report as clean.

I reproduced this by creating a fresh inbox item and then calling the status command. The output was still:

```text
Inbox is clean.
```

Why this matters:

- this breaks operator trust immediately
- it makes new captures look like they failed
- it matches the main UX issue flagged independently in the OpenCode review

Relevant files:

- `src/codies_memory/cli.py`
- `src/codies_memory/inbox.py`

Recommended fix:

- make `status` show active inbox counts first
- then separately show aging and stale buckets
- optionally add `--all` for detailed listing

Suggested target output:

```text
Inbox: 1 active item(s) (0 aging, 0 stale)
```

---

### 2. High: `promote_to_global()` does not enforce the project-to-global boundary

Current behavior:

- the docstring says this promotes a project-scoped lesson to the global vault
- the implementation does not enforce that
- it will promote other project record types too, preserving their type

I reproduced a project thread being promoted into a global `TH-G...` record.

Why this matters:

- global memory is supposed to hold reusable cross-project truth, not arbitrary project-local working threads
- this weakens one of the most important boundaries in the whole system
- it allows incorrect usage to look legitimate because IDs and paths still resolve cleanly

Relevant files:

- `src/codies_memory/promotion.py`
- `src/codies_memory/vault.py`
- `tests/test_promotion.py`

Recommended fix:

- explicitly restrict global promotion to lessons for now
- raise `ValueError` for project thread/decision promotion unless a later spec intentionally broadens the rule
- add regression tests for invalid global promotion attempts

---

### 3. Medium: `validate_vault()` misses required files and can report broken vaults as valid

Current behavior:

- validation checks expected directories only
- it does not check required files like `profile.yaml` or `registry/projects.yaml`

I reproduced this by deleting `registry/projects.yaml` from a global vault and then validating it. The vault still reported as valid.

Why this matters:

- validation is supposed to be the confidence-restoring command
- later commands depend on these files existing
- this lets corrupted vaults pass preflight and fail later in more confusing ways

Relevant files:

- `src/codies_memory/vault.py`
- `tests/test_vault.py`

Recommended fix:

- split validation into required directories and required files
- for global vaults, at minimum require:
  - `profile.yaml`
  - `registry/projects.yaml`
  - identity seed files
- for project vaults, at minimum require:
  - `profile.yaml`

---

### 4. Medium: schema guarantees are weak enough that invalid durable state can be written silently

Current behavior:

- `validate_frontmatter()` defines a lot of schema vocabulary, but only validates a small subset
- `update_record()` does not revalidate frontmatter before rewriting the file

I reproduced this by updating a record to `status='bogus-status'`, which persisted successfully.

Why this matters:

- the system presents records as typed/trusted durable memory
- once invalid states are allowed in, downstream logic either silently tolerates them or breaks unpredictably
- it makes the frontmatter schema look stronger than it is

Relevant files:

- `src/codies_memory/schemas.py`
- `src/codies_memory/records.py`

Recommended fix:

- validate `status`
- validate record type consistency
- decide whether unknown extra fields are allowed or rejected
- re-run validation in `update_record()` before writing

---

### 5. Low: the close-session skill contains a broken literal shell substitution

Current behavior:

- `skills/memory-close-session.md` includes:

```python
title='Session Summary - $(date +%Y-%m-%d)'
```

That shell expression is inside a Python string literal, so it will not expand.

Why this matters:

- a careful agent may notice and repair it mentally
- a literal agent following the skill exactly will create bad session titles
- this is a small issue, but it undermines confidence in the operational path

Relevant file:

- `skills/memory-close-session.md`

Recommended fix:

- compute the date in Python
- or replace the example with a concrete placeholder plus a note to fill it in

---

## What Looks Good

These parts feel solid enough to keep building on:

- the repo is compact and readable
- tests are fast and broad for a first implementation pass
- the registry-write owner concern appears addressed
- probation support exists and is covered
- the overall module split is sensible

---

## Recommended Next Steps

If Claude wants the highest-leverage follow-up order, I would do this:

1. Fix the operator-facing trust breakers:
   - `status`
   - required-file validation
   - broken close-session skill example

2. Fix the global boundary:
   - restrict `promote_to_global()` to lessons

3. Tighten schema guarantees:
   - validate `status`
   - validate updates before write

4. Add regression tests for all of the above before adding new CLI surface

Only after that would I move on to bigger ergonomics like:

- `capture` CLI
- `create` CLI
- `list` CLI
- registry cleanup commands

Those are worthwhile, but the truthfulness and boundary issues come first.
