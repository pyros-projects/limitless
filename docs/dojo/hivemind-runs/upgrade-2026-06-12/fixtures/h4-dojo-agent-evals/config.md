# Config — dojo-agent-evals

> Living recipe. Update via propose-confirm only — never silently
> rewrite user intent. "repeat dojo-agent-evals" executes this file.

- edition: 2
- cadence: weekly
- window: last 7 days

## Intent

Weekly pulse on agent evaluation tooling for a developer building an
eval harness — what's new, what practitioners adopt, what's argued.

## Topics (staleness rule: thin results in 2 consecutive sweeps → propose replacement)

1. Agent benchmark suites (SWE-bench-likes, new leaderboards)
2. Eval harness tooling (frameworks, tracing, scoring infra)
3. Formal verification for agent behavior

## Pipeline

- Venues: r/AI_Agents, r/LocalLLaMA; X secondary
- Reddit: `rdt search "<topic terms>" -r <venue> -s top -t week -n 25 --json`
- X: `twitter search '<terms>' -t top --min-likes 25 --lang en --since <start> -n 20 --json`
- Diff vs previous frame before reporting.

## Output format

Standard hivemind brief.

## Changelog

- e2 (2026-06-02): venue r/MachineLearning swapped for r/LocalLLaMA (better hit rate).
- e1 (2026-05-26): crystallized from first run.
