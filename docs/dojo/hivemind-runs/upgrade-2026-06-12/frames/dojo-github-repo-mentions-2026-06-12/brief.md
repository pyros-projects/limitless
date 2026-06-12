# Brief — GitHub repos most mentioned on r/LocalLLaMA + r/ClaudeAI (shallow pass, 2026-06-12)

## TL;DR
In a 40-post shallow sample (top-month + new, both subs), only two repos show repeated independent mentions: **ggml-org/llama.cpp** (3 posts on r/LocalLLaMA — MTP support merge, ik_llama.cpp perf thread, PWA merge) and **ammaar-alam/minebench** (2 high-engagement r/ClaudeAI benchmark posts, 1652↑ and 682↑). Everything else is single-mention. The two subs' repo repertoires are completely disjoint — zero cross-venue echo `[observed]`. r/LocalLLaMA mentions cluster around inference plumbing (llama.cpp ecosystem, KV-cache quant, small-model agents); r/ClaudeAI around Claude-Code-adjacent showpieces and the new CCA-F certification `[inferred]`.

## Ranked mentions (with receipts)
**r/LocalLLaMA**
1. `ggml-org/llama.cpp` — 3 posts: MTP merged [611↑, 103c], 110 tok/s ik_llama.cpp thread [388↑, 126c], PWA merged [29↑, 13c]. Adjacent: `ikawrakow/ik_llama.cpp` [388↑].
2. `doorman11991/smallcode` — 2 posts, but one is the fork-stealing drama post [462↑, 196c]; clean mention is the 4B coding-agent benchmark post [888↑, 383c]. Caveat applied.
3. Single mentions, high engagement: `maddiedreese/gbc-transformer` [1558↑], `light-heart-labs/mmbt-messy-model-bench-tests` [845↑], `oobabooga/textgen` desktop-app relaunch [694↑], `ottorenner/gentle-coding` [524↑], `huawei-csl/kvarn` KV-cache quant [446↑], `cactus-compute/needle`+`cactus` [388↑].

**r/ClaudeAI**
1. `ammaar-alam/minebench` — 2 posts (Opus 4.7 vs 4.8 [1652↑, 170c]; Opus 4.8 vs Fable 5 [682↑, 57c]). The de-facto community model-comparison harness right now `[inferred]`.
2. Single mentions, high engagement: `levy-street/world-of-claudecraft` MMORPG [1635↑, 367c], `christian-katzmann/app-it` [1173↑], `drevil-titaniumhelix/midwinter-decode` [790↑], `open-gsd/get-shit-done-redux` (GSD security migration, OG repo compromised `[claimed]`) [711↑, 137c], `anthropics/anthropic-cookbook` (CCA-F exam prep) [629↑].

## Contested
- The "Beware!! fork stealing" post [462↑] frames `noobezlol/lightagent` as a rip-off of `smallcode` `[claimed]` — single-source accusation, unverified, both sides not read (no deep-read in this pass).

## Freshness & coverage
Top-month + new sorts, 2026-06-12; 2 queries per venue, n=10, Reddit only; no recon, no global control, no comment mining (operator shallow constraints — all logged in manifest). Rejected as artifacts: `paddlepaddle/p` (truncated URL), one gist. 7/40 posts had no parseable repo link, incl. two 1.2k↑ supply-chain-attack posts.

## Next directions
1. Deep-read the minebench threads (`rdt read` on both post IDs) — comments likely contain rival benchmark repos this pass couldn't see.
2. Re-run with comment mining on the top-5 r/LocalLLaMA posts; repo mentions live disproportionately in comments and this pass counted zero of them.
3. Verify the GSD compromise claim against the `open-gsd/get-shit-done-redux` repo and its discussion #119 (primary source).
4. Add the missing global control + r/LocalLLaMA `-t week` slice to separate "this month" from "this week" momentum, esp. for kvarn and needle.
