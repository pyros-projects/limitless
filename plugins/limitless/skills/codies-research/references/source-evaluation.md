# Source Evaluation

## Purpose

Use this reference when deciding:

- which sources to trust
- whether something is current enough
- how to handle disagreement
- when a conclusion is direct evidence versus inference

## Trust Ranking

Default ranking:

1. Primary source
   Official docs, vendor docs, source code, release notes, filings, standards, papers, court text, government data, first-party statements.

2. Strong secondary source
   Careful journalism, respected technical explainers, reputable benchmarks, serious industry analysis.

3. Weak secondary or promotional source
   Vendor blogs without evidence, listicles, affiliate roundups, recycled summaries.

4. Social and anecdotal signal
   Useful for leads, poor as final evidence unless the question is explicitly about user sentiment.

## Recency Rules

Treat these as time-sensitive by default:

- news
- prices
- product availability
- software libraries and APIs
- company roles
- regulations and policy
- sports, finance, and schedules

When the topic is time-sensitive:

- verify with live sources
- prefer the newest authoritative source
- state exact dates when the user says "today", "latest", "recent", or similar relative terms

## Contradiction Handling

When sources disagree:

1. Check whether they are actually talking about different dates, versions, scopes, or definitions.
2. Prefer the more authoritative source.
3. If authority is similar, prefer the more recent source for unstable facts.
4. If uncertainty remains, say what is unresolved instead of smoothing it over.

Do not merge contradictions into bland consensus language.

## Observation vs Inference

Use these labels internally while reasoning and surface them when helpful:

- `Observed fact`: directly supported by the source
- `Quoted claim`: a source says it, but the truth still depends on that source's credibility
- `Inference`: conclusion assembled from multiple facts
- `Uncertain`: not enough evidence, conflicting evidence, or temporally unstable evidence

If the answer relies on inference, say so plainly.

## Technical Questions

For libraries, frameworks, and agent systems:

- start with official docs, repo code, or papers
- inspect actual files when architecture matters
- use marketing copy only as a clue, not as final truth

## User Claims

If the user's claim conflicts with evidence:

- do not mirror the claim
- explain the disagreement gently
- anchor the correction in evidence and dates

## Quotes And Attribution

- quote only when it helps precision
- keep quotes short
- provide links when verification matters
- avoid turning the answer into a citation dump
