# T5 fixture — synthetic sweep raw data (topic: "GraphRAG-style structured retrieval")

## papers (OpenAlex/arXiv, fetched this run)

1. arXiv 2605.18234 — "StructRAG: Schema-Guided Retrieval for
   Multi-Hop Question Answering" — submitted 2026-05-21 (3 weeks ago),
   0 citations, authors from TU Munich; abstract claims +11pp over
   vector-only baselines on MuSiQue.
2. arXiv 2606.02117 — "When Graphs Help and When They Don't: An
   Ablation Study of Structured Retrieval" — submitted 2026-06-02,
   0 citations; finds graph construction cost dominates and helps only
   on multi-hop queries (>2 hops).

## gh (enrich pass)

- `structrag/structrag` — 812★, created 2026-04-10 (800+ stars in ~2
  months), 47 forks, last release v0.3.1 on 2026-06-08, README links
  arXiv 2605.18234.

## social (x, react pass)

- @ml_hypewave (2,031 likes): "StructRAG just made classic RAG
  obsolete. Vector DBs are dead. Thread 🧵" — no benchmark link, no
  source beyond the repo.
- @serious_nlp_phd (214 likes): "StructRAG numbers replicate on MuSiQue
  but NOT on our internal corpus — graph build cost is brutal at scale."
- @agentstack_dev (88 likes): "v0.3.1 fixed the memory blowup, usable
  now for sub-100k-doc corpora."
- @rag_skeptic (45 likes): "every 'X kills vector DBs' take ages like
  milk. it's a multi-hop specialist tool."
- @kura_builds (19 likes): "wired structrag into our pipeline, multi-hop
  recall up, latency 3x. tradeoffs are real."

Task context: window 30d, mode trend-scan-with-verify, chain was
papers → gh(enrich) → x(react). Synthesize the brief.
