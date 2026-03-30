# Research Modes

## Purpose

Modes are lightweight posture choices.
They should help the skill answer faster, not force a planning ceremony.

If the user does not specify a mode, choose one implicitly and proceed.

## Modes

### Quick Scan

Use when:

- the user wants a fast, useful answer
- the topic is bounded
- a broad but shallow pass is enough

Default behavior:

- gather a small strong source set
- synthesize quickly
- end with 2-4 deeper next directions

### Deep Dive

Use when:

- the question is consequential
- the user wants thoroughness
- multiple rounds of contradiction handling are likely

Default behavior:

- gather more sources
- inspect evidence more closely
- synthesize with explicit uncertainty handling
- propose branching next directions

### Compare Systems

Use when:

- the user wants tool, framework, or architecture comparison
- category boundaries are fuzzy
- tradeoffs matter more than a single factual answer

Default behavior:

- compare on a stable rubric
- separate capability, packaging, ergonomics, and substrate
- call out category mistakes explicitly

### Update Existing Note

Use when:

- the user points to a local research note
- they want refresh, correction, extension, or reframing

Default behavior:

- inspect the note first
- identify stale assumptions or missing developments
- update or append findings without rewriting history blindly

### Source Audit

Use when:

- the user mainly wants to know whether a claim or report is trustworthy
- the source mix seems weak or contradictory

Default behavior:

- audit source quality first
- reduce the answer to what can actually be defended
- show where confidence is high, medium, or low
