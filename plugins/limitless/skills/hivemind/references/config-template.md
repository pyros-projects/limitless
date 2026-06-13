# Config Template — living recipes for recurring sweeps

Distilled from the first real config
(`~/.limitless/hivemind/ai-dev-weekly/config.md`, hand-crystallized
2026-06-12 from a live session) — read that file as the worked example
if it exists; every section below is present there with real values.

A config is a **contract**: prose is binding, the skill executes what
it says in the order it says. Propose-confirm only — every accepted
change bumps the edition and adds a dated changelog line. Never
silently rewrite user intent.

## Structure

```markdown
# Config — <topic-slug>

> Living recipe. Update via propose-confirm only — never silently
> rewrite user intent. Frames under ./<date>/ are immutable episodes;
> this file is the contract for the next run. "repeat <slug>"
> executes this file.

- edition: N
- derived_from: ./<date>/ (the frame this was crystallized from)
- cadence: <weekly|monthly|ad-hoc> (<anchoring event, if any>)
- window: <e.g. last 14 days>
- chain: <e.g. gh → x,reddit → verify(web)>   # optional, free-form

## Intent

Who the output is for and what it must accomplish. Audience framing
matters — it drives tone, depth, what counts as "prominent".

## Topics (staleness rule: thin results in N consecutive sweeps → propose replacement)

Numbered list. Each topic concrete enough to search.

## Exclusions

Muted subjects, with the reason — bound by lookup on ad-hoc asks too.

## Pipeline

Numbered prose steps — venues with exact recipes (incl. CLI traps and
keyword traps discovered in past runs), diff-vs-previous-frame step,
delivery step if any. Non-venue stages (e.g. "write into issue X")
are legitimate pipeline steps.

## Output format

Language, structure, sections, per-item shape, length rules — the
format the user actually accepted, not the default.

## Persistence

Frame contract per the skill; anything extra (e.g. side files).

## Changelog

- eN (<date>): <what changed and why — one line per accepted change>
```

## Crystallize mapping (session → config)

| Observed in session | Becomes |
|---|---|
| Mid-sweep correction ("make it 30 days") | scalar/recipe line |
| Muted topic ("skip async-std stuff") | Exclusions entry |
| The output the user finally accepted | Output format spec |
| Recurrence smell ("let's do this monthly") | cadence + the offer itself |
| CLI/keyword trap discovered | Pipeline trap note |
| Venue adaptations that held | Pipeline venue list |

The proposal shown to the user must contain every observed correction
mapped to its config line. Nothing is written before confirmation.

## Rules carried by every config

- Live ask > config > recon classification (per-run deviations are
  proposed deltas, not edits).
- Tool failures never become deltas; persistent breakage (2+ runs) may
  become a proposed *repair*, labeled as such.
- Staleness proposals cite the evidence from each thin frame.
- The config must stay self-contained enough for a cold session to
  execute `repeat <slug>` with no other context.
