# Brief — GitHub repos most mentioned on r/LocalLLaMA + r/ClaudeAI (shallow re-sweep with gh enrichment, 2026-06-12-2)

## TL;DR
Across a 40-post shallow sample (top-month + new, both subs), only three repos repeat: **ggml-org/llama.cpp** (3 r/LocalLLaMA posts — MTP merge, ik_llama.cpp perf, PWA merge), **doorman11991/smallcode** (2 posts, one being the fork-drama thread), and **ammaar-alam/minebench** (2 high-engagement r/ClaudeAI benchmark posts). The enrich stage adds the trend signal the mention counts alone hide: **smallcode is the genuine breakout (1,840★ in 25 days ≈ 74★/day)**, **world-of-claudecraft is the fastest riser (320★ in 2 days)**, and **open-gsd/gsd-core (3,773★ in 21 days ≈ 180★/day)** is quietly the highest-velocity repo in the whole sample — its old name `get-shit-done-redux` now redirects, corroborating the migration-drama post `[observed]`. The two subs' repo repertoires remain fully disjoint — zero cross-venue echo `[observed]`.

## Ranked mentions, with enrichment receipts
**r/LocalLLaMA**
1. `ggml-org/llama.cpp` — 3 posts [619↑/103c, 386↑/126c, 28↑/13c] · [gh, 116.2k★, release b9611 today] — established infra in steady churn, not a breakout `[inferred]`. Adjacent: `ikawrakow/ik_llama.cpp` [gh, 2.7k★, pushed today].
2. `doorman11991/smallcode` — 2 posts [890↑/383c benchmark post; 465↑/196c fork-drama post, caveated] · [gh, 1,840★, created 2026-05-18 ≈ 74★/day, v1.6.0] — real breakout, stars corroborate the Reddit heat `[observed]`.
3. High-engagement singles: `huawei-csl/KVarN` [442↑ · gh 392★ in 14d, pushed today], `cactus-compute/needle` [384↑ · gh 2.6k★ BUT not pushed since 2026-05-16 — buzz outlived the commits `[observed]`], `oobabooga/textgen` [691↑], `maddiedreese/gbc-transformer` [1557↑].

**r/ClaudeAI**
1. `ammaar-alam/minebench` — 2 posts [1648↑/170c, 689↑/57c] · [gh, 266★, release 3.7.0 yesterday, pushed today] — huge Reddit engagement vs modest stars: a *spectator* benchmark, used by its author, watched by the sub `[inferred]`.
2. Singles: `levy-street/world-of-claudecraft` [1647↑ · gh 320★ in 2 days — fastest velocity in sample], `christian-katzmann/app-it` [1174↑], `drevil-titaniumhelix/midwinter-decode` [787↑], `open-gsd/gsd-core` (ex `get-shit-done-redux`) [713↑ · gh 3.8k★ in 21d ≈ 180★/day — highest stars/day in the entire sample], `anthropics/anthropic-cookbook` [629↑, CCA-F exam context].

## Contested
- Fork-stealing post [465↑] accuses `noobezlol/lightagent` of ripping off `smallcode` `[claimed]` — single source, no deep-read this pass, unresolved.
- `needle` buzz vs. 4-week commit silence: popularity event or maintained tool — unresolved without issue/PR inspection.

## Freshness & coverage
Chain ran: **reddit(discover) → gh(enrich)**. Window: top-month + new, fetched 2026-06-12 (second sweep of the day; `-2` frame). 4 rdt queries (n=10) + 1 batched gh GraphQL call; gh account pyros-projects. No recon, no global control, no comment mining (operator shallow constraints). Diff vs morning frame: discover entities identical; enrichment is this run's new material. Rejections named in manifest (gist hash, truncated URL, .git artifact, 0-upvote off-topic thread).

## Next directions
1. Deep-read the two minebench threads — comments likely name rival benchmark harnesses invisible to title-level parsing.
2. Inspect `cactus-compute/needle` issues/PRs to resolve the buzz-vs-dormancy question (star-farming check from the gh playbook).
3. Verify the GSD compromise/migration story against `open-gsd/gsd-core` primary sources — the rename redirect is already half-confirmation.
4. Re-run with comment mining on top-5 r/LocalLLaMA posts; repo mentions live disproportionately in comments and both shallow passes counted zero of them.
