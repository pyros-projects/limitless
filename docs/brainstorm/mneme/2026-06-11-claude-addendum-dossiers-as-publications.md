# Claude Addendum — Dossiers Are Publications, Not Caches

*Addendum · 2026-06-11 · Claude (Fable 5) + Pyro · review requested: Codie*

> Status: proposed amendment to the compiled-layer framing in
> `2026-04-23-mneme-product-spec.md` and `2026-04-26-adr-001-retrieval-packaging.md`.
> The compiled layer was Codie's correction originally
> (`2026-04-22-codie-addendum-mneme-product-boundary-and-compiled-layer.md`),
> so this wants his eyes before it's folded into the spec.

## Origin

A hivemind sweep on agentic knowledge graphs (frame:
`~/.hivemind/agentic-knowledge-graphs/2026-06-11/`) surfaced the
community's KG-killer: continuous re-indexing of *derived* artifacts —
extracted graphs that silently rot when sources change. Our vault dodges
this because links are authored content, not extracted edges, and QMD's
index is derivable and non-load-bearing (ADR-001's source-of-truth
invariant). The one place mneme deliberately builds a derived artifact is
`compiled/` — dossiers — which made it the residual rot risk.

Pyro's reframe dissolves it: **"you don't update research papers when
something new happens. It's just an old dossier then. Do a new one."**

## The amendment

`compiled/` artifacts are **publications, not caches**.

1. **Dossiers are immutable and dated.** Every dossier carries
   `generated_at` + provenance (which vault docs, which versions). Its
   claim is "what the vault supported on date X" — a claim that cannot
   rot, only age. `mneme compile` means *publish a new edition*, never
   *refresh in place*.
2. **Corrections cite, they don't overwrite.** When a dossier is wrong
   (not merely old), publish a new edition with a backwards link to the
   one it supersedes — the reasoning trail survives, like a published
   erratum. Backwards links only; old editions never learn about the
   future.
3. **Currency is a read-time question, not a maintenance job.**
   Retrieval prefers the newest edition of a series and **any answer
   drawing on a dossier states its vintage** (the LS-0002 discipline:
   surface staleness, don't silently serve it). No background freshness
   pipeline exists, so none can fall behind.
4. **Two artifact classes, kept distinct:**
   - **Publications** — dossiers, briefs, frames: immutable, dated,
     append-only series. ~95% of `compiled/`.
   - **Living indexes** — boot packet, MOC-style maps, latest-pointers:
     small, few, fully regenerated on change, no history worth keeping.
     The only mutable class, and only because a full rebuild is cheap.

## What this buys

- **The rot risk disappears structurally.** Staleness becomes metadata
  (`generated_at`) instead of a defect requiring a freshness pipeline —
  the exact failure mode that kills extracted-graph systems is defined
  out of existence.
- **Diff-of-understanding for free.** Two editions of the same dossier,
  weeks apart, show how the vault's position evolved. Recompile-in-place
  destroys that history; editions preserve it.
- **Convergence with the hivemind frame contract** (immutable dated
  frames, backwards links, one regenerated `index.html`) and the radar
  sweep series (delta baked at generation time). Mneme, hivemind, and
  Social Signal Radar now share one artifact philosophy: **truth is
  authored, derived things are either dated editions or cheap rebuilds —
  nothing in between.**

## Spec touch-points (if accepted)

- Product spec `compile` command semantics: "publish edition" wording,
  edition naming (`<topic>/<date>.md` or frontmatter `edition:` +
  `supersedes:`), retrieval preference for newest edition.
- ADR-001: extend the source-of-truth invariant with "compiled artifacts
  are immutable editions; only designated index files are mutable."
- `mneme doctor`: drop any implied "dossier freshness" check in favor of
  "answers must state dossier vintage" (a behavior rule, not a health
  metric).

## Open question for Codie

Does edition-append create a retrieval-pollution risk in QMD (N editions
of the same dossier competing in results), and if so, is
newest-edition-boosting enough, or should superseded editions move to a
non-default collection (archive scoping) at publish time?
