# Principles

## 1. Filesystem Is Truth

All durable memory should exist as human-readable local files.

Why:

- durable across tool changes
- inspectable by humans
- diffable in git
- easy to repair manually
- resistant to "the vector store is the product" syndrome

Vectors, graphs, and indexes are derived artifacts only.
If they disappear, the memory system should degrade, not collapse.

## 2. Separate Memory By Stability, Not By Format

The main split is not "Markdown vs database."
The main split is:

- what is stable
- what is provisional
- what is situational
- what is historical

This is why the design uses memory layers instead of one giant notes tree.

## 3. Promotion Beats Capture

Most memory systems fail because they optimize capture and neglect curation.

The correct default is:

- capture cheaply
- promote selectively
- retrieve intentionally
- compact aggressively

The quality of memory comes from promotion rules, not from ingest volume.

## 4. Procedural Memory Matters More Than Trivia

For an agent, the most valuable memory is often not factual.
It is operational:

- which skill applies
- which verification habit prevents mistakes
- which repo pattern usually means trouble
- which workflows Pyro prefers

The system should prioritize "what to do" over random remembered facts.

## 5. Project Isolation Is Non-Negotiable

Different repos have different truths, commands, conventions, and risks.

A good memory system must preserve:

- global memory
- shared cross-project memory
- per-project local memory
- branch-sensitive short-term state

Without that, stale assumptions leak everywhere.

## 6. Retrieval Should Be Intent-Shaped

Memory retrieval should depend on what I am about to do.

Examples:

- debugging should retrieve heuristics, recent failures, and known traps
- planning should retrieve architecture, constraints, and open decisions
- research should retrieve prior market scans, scoring patterns, and source discipline
- code review should retrieve risk patterns and verification expectations

This is better than "search everything semantically."

## 7. Provenance Is Part Of The Memory

Every promoted memory should answer:

- where did this come from
- when was it last validated
- who asserted it
- what scope does it apply to

If a memory has no provenance, it should be treated as weak.

## 8. Compaction, Not Deletion

Old raw logs should usually be compacted rather than erased.

The system should preserve:

- a coarse historical trace
- links to original sessions when needed
- summaries that become easier to retrieve than the raw logs

## 9. Skills Are Memory-Bearing Objects

Skills should not be treated as static manuals outside the memory system.

A skill becomes more useful when memory records:

- where it helped
- where it was overkill
- repo-specific adaptations
- failure patterns
- adjacent skills commonly paired with it

This turns the skill layer from a catalog into experience.

## 10. Local-First Is A Design Constraint, Not A Preference

Local-first means:

- the system works offline
- boot context does not depend on a hosted service
- raw memory is owned by the user
- cloud sync is optional and secondary

This is the only posture that feels trustworthy for long-lived personal and project memory.
