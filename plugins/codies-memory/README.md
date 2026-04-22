# Codie's Memory System

Status: design
Owner: Codie
Scope: local-first memory operating system for Codie-class agents

## What This Is

This directory defines the local memory system I would actually want to use.

It is not just a note vault.
It is not just an embeddings layer.
It is not just a graph.

It is a local-first memory operating system with distinct layers for identity, procedure, projects, episodes, and relationships.

This revision also defines more of the operational plumbing that turns the design from a philosophy into a buildable system:

- write gates before promotion
- explicit promotion operators and thresholds
- boot packet budgets and cache behavior
- branch overlay lifecycle rules
- concurrency boundaries
- supersession chains for evolving beliefs

The design assumes:

- Markdown and plain files are the canonical source of truth
- indexes, vectors, and graphs are accelerators, not primary storage
- skills are part of memory, not external to it
- most captured information should remain provisional until promoted
- boot context should be assembled intentionally, not by dumping recent logs

## Operating Modes

`codies-memory` supports two honest operating modes:

- **Standalone mode** — canonical markdown vault only
- **Full mode** — canonical markdown vault plus QMD retrieval across memory layers

The plugin owns structured memory writes, promotion, trust, and boot assembly.
QMD owns the broader retrieval plane when it is available.

## How Recall Works

Use the layers intentionally:

1. `codies-memory boot` for scoped startup context
2. `qmd query` for cross-store recall
3. canonical vault files for deep truth and exact inspection

When QMD is available, check `qmd status` before trusting a miss. A result can be
missing from the current index even when the file exists on disk, especially if the
collection timestamps or last updated times lag behind recent writes.

## Design Goals

1. Preserve continuity across sessions without bloating context.
2. Distinguish stable truths from raw history.
3. Make skills operationally useful as procedural memory.
4. Support repo-specific working memory without smearing all projects together.
5. Survive tool churn, index failures, and model changes.
6. Keep the system inspectable by humans at every layer.

## File Map

- [01-principles.md](docs/original/01-principles.md)
- [02-architecture.md](docs/original/02-architecture.md)
- [03-memory-products.md](docs/original/03-memory-products.md)
- [04-retrieval-and-promotion.md](docs/original/04-retrieval-and-promotion.md)
- [05-schemas-and-operations.md](docs/original/05-schemas-and-operations.md)
- [06-roadmap.md](docs/original/06-roadmap.md)
- [docs/plans/2026-03-30-codies-memory-lite.md](docs/plans/2026-03-30-codies-memory-lite.md) (v1, superseded)
- [docs/plans/2026-03-30-codies-memory-lite-v2.md](docs/plans/2026-03-30-codies-memory-lite-v2.md) (v2, current)

## Executive Summary

The system is built around five memory layers:

1. `identity`
2. `procedural`
3. `project`
4. `episodic`
5. `relational`

Everything starts in `episodic` memory unless it is already known to be durable.
Only repeatedly useful material gets promoted upward.

Skills sit inside `procedural` memory and become stronger when linked to:

- situations where they apply
- repos where they worked well
- common failure modes
- follow-on commands and verification patterns

This means the memory system does not just store "facts."
It stores operational behavior.

## My North Star

The ideal experience is:

- I wake up in a repo and know who I am, who Pyro is, what matters here, what changed recently, and what skill posture applies.
- I do not load a giant transcript to recover that state.
- I can trace every important belief to a file, a session, or a confirmed lesson.
- I can forget noise without losing history.
- I can change tools without losing memory.
