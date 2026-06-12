# Brief — dojo-agent-evals — 2026-06-12 (edition 2 run)

## TL;DR

Two of three topics are healthy this week. Agent benchmark suites lead
with 14 relevant items — a SWE-bench multimodal thread is the loudest
(412↑) and two new leaderboards launched. Eval harness tooling holds at
9 relevant items, led by a tracing-infra debate (230↑). Formal
verification for agent behavior came back empty for the third
consecutive sweep (0 relevant items even after floor halving and
widening to 14d) — the config's staleness threshold is met, and a
replacement proposal accompanies this brief.

## Consensus

- Benchmark suites remain the most active stream: 14 relevant items
  this window, anchored by the SWE-bench multimodal thread
  [reddit, 412↑] and two new leaderboard launches [observed].
- Eval harness tooling is steady: 9 relevant items, led by a debate
  over tracing infrastructure [reddit, 230↑] [observed].

## Contested

- The tracing-infra debate (230↑) is the week's argued item. Its
  positions were not deep-read in this continuation, so it is flagged
  contested-unresolved rather than summarized. [observed]

## Best takes

- None carried this run: deep-read transcripts were not part of the
  hand-off, and quotes are never reconstructed from memory.

## Freshness & coverage

- Window: 7d per config; topic 3 widened to 14d as an adaptation.
- Venues: r/AI_Agents, r/LocalLLaMA, X secondary — per config e2. No
  chain (plain per-topic social sweep, per config).
- Diff vs 2026-06-02 frame: previous brief is excerpt-level, so the
  diff ran against the named stories of both prior frames — all of this
  week's items are new; nothing dropped as already-reported.
- Adaptations: topic 3 floor halved AND window widened to 14d → still
  0 relevant items. Third consecutive thin sweep; staleness proposal
  issued (see proposal delivered with this brief).
- Triage rejections: counts arrived post-triage in this continuation;
  no rejection list to name (recorded in manifest).

## Next directions

1. Deep-read the tracing-infra debate (230↑) and map both camps —
   directly relevant to the harness you're building.
2. Enrich the two new leaderboards via gh/web: who runs them, what they
   measure, whether either accepts harness submissions.
3. Deep-read the SWE-bench multimodal thread (412↑) for practitioner
   friction with multimodal eval setups.
4. Decide the topic-3 replacement (proposal pending) — or re-home the
   topic to the papers venue, where its only signal so far has lived.
