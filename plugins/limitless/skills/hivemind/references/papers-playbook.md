# Papers Playbook — OpenAlex + arXiv as a hivemind venue

Evidence grade: **strong** — papers are primary sources. This is the
venue where `--verify` naturally lands: a contested social claim
chased to a paper gets marked verified/refuted instead of staying
he-said-she-said. Benchmark numbers inside a paper are still
`[claimed]` by its authors until independently replicated.

Both APIs are free, keyless, verified working 2026-06-12.

## Recipes

**OpenAlex — the structured-triage workhorse (~250M works, citation
counts, filters):**

```bash
# Relevance search
curl -s "https://api.openalex.org/works?search=<q>&per-page=10&mailto=<email>" | jq -r '.results[] | "\(.publication_date) | \(.cited_by_count) cites | \(.title)"'

# Recent-first (trend scans)
curl -s "https://api.openalex.org/works?search=<q>&sort=publication_date:desc&filter=from_publication_date:<YYYY-MM-DD>&per-page=10&mailto=<email>"
```

Always pass `mailto=` — it routes to the polite pool (100k req/day).
Abstracts come as an inverted index (`abstract_inverted_index`);
reconstruct with a throwaway parser or triage on title + venue +
citation count.

**arXiv — freshest preprints (where AI/ML research lands first;
OpenAlex indexing lags arXiv by days-to-weeks):**

```bash
curl -s "http://export.arxiv.org/api/query?search_query=all:%22<q>%22&sortBy=submittedDate&sortOrder=descending&max_results=10" -o "$FRAME/raw/arx-1.xml"
grep -oP '(?<=<title>)[^<]+' "$FRAME/raw/arx-1.xml"   # quick triage; full parse for abstracts
```

Atom XML — a throwaway parser is fine (Initiative section applies).
URL-encode the query (`%22` for phrase quotes).

**SearXNG science category** — breadth aggregator (google scholar,
pubmed, semantic scholar, openaire) when the local instance is up; see
web-playbook. Use for recall, not for triage metadata.

Rejected tooling: Semantic Scholar direct API (unauthenticated pool is
shared and tight; OpenAlex covers it keyless). No paid APIs.

## The citation-lag rule

For papers younger than ~6 months, citation counts are meaningless —
**never read "0 citations" as weak**. Triage fresh papers by recency +
venue + author track record, and say so in the brief: `[arXiv
2606.xxxxx, 0 cites — too fresh]`. Citation counts become signal on
the 6-month-plus tail.

## Triage & discipline

- Dedup by DOI / arXiv id — the same paper arrives via multiple
  engines and as preprint + published version.
- Fallbacks: OpenAlex down → arXiv-only with a coverage flag (and vice
  versa); both down → science category as last resort, flagged.
- Reaction to a paper (social react stage) searches the paper's short
  name AND arXiv id — paper titles collide with product names.
- Papers in a chain: discover (what's new in the field), enrich
  (citation counts for entities), or verify (chase a claim). State
  which role the venue played.
