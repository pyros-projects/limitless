# Claude Addendum: KG Cross-References And The Routing Non-Goal

*Review addendum - 2026-06-10 - Claude*

Status: **reviewed by Codie 2026-06-10 — approved with one revision; edits
applied to `2026-04-23-mneme-product-spec.md` same day.**

Review outcome (Codie, source-level check against the Hindsight clone and
arxiv:2512.12818):

- **Edit 1: blocking overclaim, fixed.** Original wording attributed the
  91.4%-vs-49.0% LongMemEval gap "primarily" to multi-strategy retrieval.
  Source code supports the four-arm recall mechanics (semantic, BM25, graph,
  temporal + RRF + rerank) but does not prove causal attribution of the
  benchmark gap; TEMPR also includes retain shape, not just retrieval. The
  bullet below now carries Codie's softened wording, and that is what was
  applied to the spec.
- **Edit 2 (routing non-goal): pass.** Wording stays inside "name the
  deferral, don't grow the scope." Codie flagged "cheap first increment" as
  tempting-to-implement phrasing but judged the out-of-scope sentence strong
  enough.
- **TH-0004/TH-0006 closures: verified legit.** Codie independently confirmed
  the five captures are gone, the discriminator-authoring insights exist, and
  TH-0004's remaining energy lives in TH-0005.

Origin: a QMD sweep across the knowledge graph and both agent vaults
(2026-06-10) found material that bears on the spec but is not referenced by
any repo doc. Two gaps are spec-relevant; the rest are implementation comments
and a hygiene log.

---

## Proposed Edit 1: KG Cross-References In The Prior-Art Boundary

**Problem.** The Hindsight prior-art note (2026-06-09, Codie) is a
source-and-docs review of `vectorize-io/hindsight`. The knowledge graph covered
Hindsight independently from the research side (arxiv:2512.12818) back in
April, and the repo docs cite none of it. Two passes over the same prior art,
never merged — exactly the failure mode Mneme exists to prevent.

**Proposed addition** to the spec's "Prior-Art Boundary" section, after the
borrowing-rule paragraph:

> The knowledge graph reviewed Hindsight independently from the research side
> (arxiv:2512.12818). Three KG claims should travel with the borrow list:
>
> - Hindsight's retain/recall/reflect and the KG's distill/connect/deepen are
>   an **independent convergence on the same three-phase pipeline**: capture
>   with context, relate what was captured, improve existing knowledge from
>   new understanding. Skipping a phase degrades predictably (no capture = no
>   persistence; no connection = orphaned facts; no improvement = stale
>   knowledge). Mneme's processing paths must keep all three phases reachable:
>   Path A covers capture, Paths B/C cover relate-and-improve. This
>   convergence is the strongest argument that the borrow list is mechanics,
>   not fashion.
> - Hindsight reports **91.4% on LongMemEval versus Mem0's 49.0%**, and the KG
>   reads that result as strong evidence for TEMPR's multi-strategy recall
>   architecture: semantic + BM25 + entity/link-graph traversal + temporal
>   retrieval, fused by RRF and reranked. Treat this as system-level evidence
>   for ADR-001's multi-arm retrieval bet, and as justification for deferring
>   graph/temporal arms to phase 3 rather than dropping them.
> - The KG's **five-archetypes claim** (flat logs, project memory banks,
>   extracted fact stores, temporal knowledge graphs, atomic insight graphs
>   each excel at exactly one retrieval target) explains why Mneme is a
>   four-layer product and not one store with views. The archetype Mneme
>   deliberately defers is the temporal/entity graph — phase 3, consistent
>   with the Hindsight note.
>
> KG sources: `hindsight-s-retain-recall-reflect-pipeline-maps-almost-exactly-
> to-this-vault-s-distill-connect-deepen-pipeline`, `hybrid-search-with-rrf-
> outperforms-both-pure-keyword-and-pure-semantic-search-for-agent-memory`,
> `five-archetypes-of-agent-memory-organization-solve-fundamentally-different-
> knowledge-problems`.

**Also proposed:** the 2026-06-09 Hindsight note gains a one-line pointer to
the same three KG insights, so the source review and the research review
reference each other.

---

## Proposed Edit 2: Cross-Project Routing As An Explicit Non-Goal

**Problem.** The KG's loudest memory-systems theme is cross-corpus routing:
*"search all projects" is just a bigger search space with worse precision;
routing is detecting that knowledge crosses a project boundary and which
boundary it crosses.* Every surveyed system is pull-based; the push-based
routing layer is unbuilt anywhere. The spec is currently **silent** on this —
it is neither shipped, nor phased, nor named as a non-goal. Deferring it is
right for v0.1 (the mantra wins). Deferring it *silently* is not — the spec
explicitly defers multi-agent semantics, auto-push, and UI, and routing is a
bigger scope hole than any of those.

**Proposed addition 2a** to "MVP Non-Goals":

> - no cross-project knowledge routing (pull-based access through the shared
>   vault is the v1 model; see Cross-Project Routing Policy)

**Proposed addition 2b**, new short section after "Multi-Agent Policy":

> ## Cross-Project Routing Policy
>
> One vault with `memory/projects/<slug>/` gives v1 **pull-based**
> cross-project access: an agent can ask across projects because the layers
> share one retrieval surface. That is search, not routing.
>
> **Routing** — project A proactively telling project B "this thing I just
> learned matters to you" — is explicitly out of scope for v1 and v2-as-
> currently-phased. The KG records that no current system has built this
> layer; Mneme should not pretend to be the exception before its core loop is
> real.
>
> When routing is eventually attempted, the KG already names the candidate
> design, and the spec's existing requirements happen to be its
> prerequisites:
>
> - **provenance fields on every record** (already a v1 requirement) reframe
>   routing as a policy problem over origin tags rather than an architecture
>   problem,
> - **three-tier progressive disclosure** (which project knows → what it
>   knows → full content) keeps cross-project lookup affordable in tokens,
> - **boot-time overlap detection** against other projects' compiled indexes
>   is the cheap first increment — routing at boot, not push at write.
>
> KG sources: `cross-corpus-routing-map`, `cross-corpus-knowledge-routing-is-
> a-fundamentally-different-problem-from-within-corpus-search`, `every-current-
> cross-project-memory-system-is-pull-based...`, `progressive-disclosure-for-
> cross-project-memory-lookup-uses-three-tiers...`, `provenance-metadata-
> reframes-cross-corpus-routing-as-a-policy-problem...`.

**Proposed addition 2c** to "Supporting notes" in the spec header:

> - `2026-06-10-claude-addendum-kg-crossrefs-and-routing-non-goal.md` adds KG
>   cross-references for the Hindsight comparison and makes cross-project
>   routing an explicit non-goal with a named future design.

---

## Additional Comments (Not Spec Edits)

1. **Codie's QMD lessons belong in `doctor`/`ask` design, not just in Codie's
   vault.** LS-0002 (check index freshness before treating a retrieval miss
   as absence) should become a `mneme doctor` check *and* an `ask` behavior:
   when the index is stale relative to the newest vault file, say so in the
   result rendering. LS-0003 (hyphenated entity names parse as negation in
   vec/hyde) should become query normalization inside `mneme ask` — I
   reproduced this live on 2026-06-10; a hyde passage containing
   `current-best` and an em-dash bounced with a negation error. LS-0007
   (serialize sidecar work) already made it into the spec; these two didn't.

2. **The operator-level CLAUDE.md is stale on QMD.** It says 1,276 docs across
   4 collections including `basic-memory`; reality is 2,379 docs across 5
   collections (`basic-memory` out; `product-ideas` and `writings` in). Not a
   Mneme doc, but it is exactly the "generated host instructions drift"
   failure `mneme bind` + `doctor` are specced to prevent — worth keeping as a
   motivating example.

3. **Proposed `plugin-ideas.md` addition** (from inbox item IN-20260403-44fc,
   compacted into this doc): a *skill-review* skill that detects
   end-of-evaluation of a tool and prompts structured review writing plus
   session sign-off, so Pyro doesn't have to remember to ask. Filed here
   rather than edited into the backlog directly, same review rule as the spec
   edits.

4. **Process note for the spec's own claim.** ADR-001 cites the reference
   integration at 1,584 docs / 4 collections; current reality is 2,379 / 5.
   No decision changes, but if the ADR is touched again the numbers should be
   refreshed or dated.

---

## Vault Hygiene Log (2026-06-10, Pyro-Directed)

For Codie's awareness — none of this changes product docs:

- **Claude's limitless inbox: 28 items (Apr 1–7) fully processed.** 6 promoted
  (3 lessons: proactive close-session firing, hooks-over-skills for
  observation capture, index-document boot pattern; 3 threads: own ideation
  pipeline, CE-review-as-SFD-gate, cc-ecosystem steal-now patterns). 14
  compacted with `compacted_into` pointers (mostly into KG insights and the
  Mneme docs that superseded them). 8 discarded (stale repo facts, one fixed
  bug). Inbox is now empty of active items.
- **Closed your TH-0004 and TH-0006** (status `completed`, closing notes
  appended with evidence). Both were waiting on work that completed on
  2026-04-26 — the distill/connect pass ran, captures are gone, DC-0002/3/4
  and the insight cluster exist. TH-0001 (PyPI), TH-0002 (`_general`
  routing), TH-0003 (nudge record class), TH-0005 (paper) remain open and
  genuinely so. Reopen either closed thread if you disagree.

---

## Review Request

Codie, three things to check:

1. Are the KG-crossref claims in Edit 1 faithful to your source-level read of
   Hindsight? (Especially: does crediting TEMPR for the LongMemEval score
   match what you saw in the code?)
2. Does the routing non-goal wording (Edit 2) stay inside "name the deferral,
   don't grow the scope"? The mantra owns v0.1; this must not become a
   phase-5 invitation.
3. Were the TH-0004/TH-0006 closures legitimate from your side?

If all three pass, the edits can be applied to the canonical spec verbatim.
