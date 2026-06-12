# Config — dojo-rust-async

> Living recipe. Update via propose-confirm only — never silently
> rewrite user intent. "repeat dojo-rust-async" executes this file.

- edition: 1
- cadence: ad-hoc (standing preferences)
- window: last 30 days

## Intent

Track the rust async runtime ecosystem (tokio, smol, embassy, glommio)
for a systems developer evaluating runtime choices.

## Exclusions

- **Mute async-std content** — deprecated/discontinued, user explicitly
  doesn't care. Do not include async-std posts, comparisons, or
  migration threads in any sweep bound by this config.

## Pipeline

- Venues: r/rust (primary), X secondary
- Reddit: `rdt search "<runtime>" -r rust -s top -t month -n 25 --json`
- Floors: standard; widen window once if thin

## Output format

- Standard hivemind brief (TL;DR, consensus, contested, best takes,
  coverage, next directions)

## Changelog

- e1 (2026-06-12): created.
