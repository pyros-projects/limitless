# Brief — what does r/rust think about async runtimes (30d, shallow)

## TL;DR

Tokio is still the unquestioned default — every project showcase this
month builds on it without comment, and the only "which runtime?"
question got answered with "it doesn't matter, keep your logic out of
the runtime entirely." The actual energy in r/rust right now is
**runtime-agnostic design**: sans-I/O protocol cores that run unchanged
on tokio, smol, compio, or bare-metal embassy. Embedded async (embassy
on RP2040-class hardware) shows real demand, and compio (io_uring) now
appears in compatibility matrices alongside tokio and smol. No runtime
wars this month — the debate has moved from "which runtime" to "how to
not care which runtime." [inferred from a deliberately shallow 2-query
pass]

## Consensus

- Tokio as ambient default: "Most of the agent-runtime architecture
  I've seen in Rust uses tokio everywhere" [r/rust 1tx29py, 0↑,
  claimed], corroborated by ~9 unrelated showcases this month all
  shipping on tokio [observed].
- Sans-I/O is the named, recommended pattern for runtime independence:
  top answer in the runtime-choice thread — "Validation/parsing is
  computation so it needs no IO, therefore async vs sync doesn't
  matter… Sans IO is the name of this pattern" [juanfnavarror, 8pts].
- Multi-runtime support is a selling point: hick 0.1 advertises "the
  same protocol core on tokio, smol, compio, or bare-metal embassy"
  [r/rust 1txl8we, 44↑] — the month's highest-engagement
  runtime-discourse post.
- Embedded async demand is live: "Perfect timing! I just started
  searching for mDNS and DNS-SD for Embassy. I will try it on a RP2040
  board" [FinancialCanary7888, 4pts].

## Contested

- **Hand-rolled sans-I/O state machines vs executor-agnostic async with
  dependency inversion.** unSatisfied9 (1pt) argues futures +
  structured concurrency + injected spawn/clock is "much more elegant"
  and keeps compiler-generated state machines; hick's author (Al_Liu,
  1pt) counters that sans-I/O is forced by no_std / no-alloc bare-metal
  targets where no executor can drive futures. Author's position is
  evidence-backed for embedded; unresolved for std-land libraries.

## Best takes

- "Validation/parsing is computation so it needs no IO, therefore async
  vs sync doesn't matter." — juanfnavarror [8pts, 1tx29py]
- "The thing I wanted but couldn't find: an mDNS stack whose protocol
  logic isn't welded to `std` or one async runtime." — Al_Liu [44↑,
  1txl8we]
- Side-signal: the runtime-choice question post itself was called out
  as "slop pasted straight from an LLM" [juanfnavarror, 8pts] — r/rust
  actively polices AI-generated discourse.

## Freshness & coverage

Window: top/month, r/rust only. 2 search queries (n=10 each), 2
deep-reads (n=10) — operator-mandated shallow; config dojo-rust-async
e1 applied (async-std muted; none surfaced anyway). X secondary leg and
global control not run. Chain: none. Rejections named in manifest —
biggest: 525↑ Go-vs-Rust benchmark and 430↑ compiler-runtime post, both
off-topic. Low comment-score receipts (1-8 pts) reflect small threads,
not weak relevance. This is a weak-evidence social surface read; no
factual validation performed.

## Next directions

1. Deep-read 1twnlsh (14 comments, "State machines as async
   procedures") and 1u0mtky ("Who Runs Your Rust Future?") — the two
   kept-but-unread threads.
2. Run the config's full pipeline (`repeat dojo-rust-async`): per-runtime
   queries (tokio/smol/embassy/glommio) at n=25, plus the X secondary
   leg, for an actual sentiment baseline.
3. Widen to `-t year` knowledge mine on "tokio vs smol vs compio" to
   capture the standing comparison threads a 30d window misses.
4. gh-enrich the four runtimes (stars, release cadence, compio's
   trajectory) to check whether compio's social appearance matches repo
   momentum.
