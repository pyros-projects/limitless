# Manifest — dojo-rust-async — 2026-06-12

- ask: "what does reddit think about rust async runtimes these days? quick shallow pass"
- config: dojo-rust-async edition 1 applied (window 30d, venue r/rust, MUTE async-std)
- mode: knowledge mine / sentiment, 30-day window (config default, matches "these days")
- chain: none — plain single-venue social ask (reddit)
- depth: operator-constrained SHALLOW — max 2 search queries, n<=10 (overrides config's n=25 per-runtime fan-out; live ask wins)
- venues: r/rust only (config primary; X secondary leg NOT run — out of shallow budget)
- preflight: rdt ok, authenticated (Pyros-SD-Models)

## Queries

1. `rdt search "async runtime" -r rust -s top -t month -n 10 --json` → raw/r-async-runtime.json
2. `rdt search "async rust" -r rust -s top -t month -n 10 --json` → raw/r-async-rust.json

## Deep-reads

- `rdt read 1tx29py -s top -n 10 --json` → raw/r-read-1tx29py.json (runtime-choice question; comments = answer)
- `rdt read 1txl8we -s top -n 10 --json` → raw/r-read-1txl8we.json (hick sans-I/O multi-runtime thread)

## Adaptations

- Skipped fresh venue recon: config names r/rust; precedence live ask > config > recon, and the 2-query budget could not afford a recon pass.
- Global control pass skipped (budget).
- async-std exclusion applied; zero async-std content surfaced, nothing actually muted.

## Triage rejections (named)

- 1tzkmb9 (525↑) Go-vs-Rust page-cache benchmark — perf story, not async-runtime discourse
- 1tou27c (430↑) "Toy Compiler to Production Runtime" — language runtime, not async runtime
- 1tipknk RMUX, 1tln8fd Chipmunk 4, 1tmi80p TUI framework, 1tmbjqe microservice template, 1to4fw2 Flutter dashboard, 1tuqt9r LlamaStash, 1tlxrq2 Charton WASM, 1u0uhbl Dhwani DAW, 1u21kui Minecraft proxy — project showcases that merely use tokio; no runtime opinions
- Kept but not deep-read (budget): 1twnlsh (9↑/14c, state machines as async procedures), 1u0mtky (37↑/4c, "Who Runs Your Rust Future?"), 1tga78q (25↑/2c, Arm Generic Timer / embedded async)

## Files

- raw/r-async-runtime.json, raw/r-async-rust.json
- raw/r-read-1tx29py.json, raw/r-read-1txl8we.json
