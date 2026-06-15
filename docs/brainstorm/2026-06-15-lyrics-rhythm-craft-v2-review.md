# Lyrics Rhythm Craft v2 — Review & Tightenings

*Review note · 2026-06-15 · Claude (Opus 4.6) + Pyro · feedback on the
shipped `suno-pack/references/lyrics-rhythm-craft.md` (v2), itself
distilled in `docs/brainstorm/2026-06-14-lyrics-rhythm-craft-v2.md`*

> Status: **not a teardown.** v2 is a genuine upgrade over v1 — the
> "performance score" half (the `( )` / `[ ]` notation rule, the three
> control surfaces, the background-vocal toolkit, the
> `## Lyric Form Inspiration` provenance block) is the dimension v1
> missed and arguably the more powerful lever. These three points are
> pre-final tightenings surfaced during review, for the next suno-pack
> maintenance pass. Each has a concrete fix.

---

## The v2 is strong (one paragraph)

v1 fixed meter only. v2's thesis — *beautiful ≠ singable, and singable ≠
performed* — correctly identifies the lyrics field as a **performance
score with a notation parser**, not just a beat map. The `( )` = sung
backing layer / `[ ]` = instruction rule, made into THE critical rule,
is the highest-value line in the doc. The provenance block turns the
reference-artist step into an auditable test surface *and* a copyright
guardrail. Ship it. Below are the three places it contradicts or
stretches itself.

## Tightening 1 — `( )` contradicts its own absolute rule

**Problem.** The critical rule is stated absolutely: *never put a
production instruction inside parentheses — `( )` is always sung.* But
the same notation table lists `(echo: "…")`, `(breath)`, `(exhale)` as
parenthetical **FX** — and those are instructions, not sung backing
words.

**Evidence.** "THE critical rule" section vs. the notation table's last
three rows.

**Fix (one sentence).** State explicitly that `(breath)`, `(exhale)`,
and `(echo: "…")` are a **closed set of recognized FX tokens** the
engine parses — a named exception — not a license to put arbitrary
production prose (e.g. `(quiet, stripped down)`) in parens. Without
this, a reader can justify any parenthetical instruction by pointing at
`(breath)`.

## Tightening 2 — "key instruments" has two homes

**Problem.** The three-control-surface table assigns "key instruments"
to the **style prompt**, but the lyrics-field row also lists "instrument
cues," and every pipe-stacking example puts instrumentation in the
**lyrics bracket** (`[Verse | 60s jangly guitar | Fender tone]`,
`[Drop | sidechained synth bass | …]`, and the worked example's
`[Chorus | … | tribal toms | stomp-clap]`). The doc's own examples are
consistent with each other but contradict the table.

**Evidence.** Control-surface table row 1 ("key instruments") and row 2
("instrument cues") vs. the pipe-stacking section + the worked example.

**Fix (one sentence).** Sharpen the boundary: **overall instrumentation
DNA → style prompt; per-section arrangement accents → lyrics pipe-stack.**
That makes `tribal toms | stomp-clap` in the chorus bracket correct (it's
a per-section accent), resolves the table's internal tension, and notes
that when an instrument is both the song's DNA *and* a section accent it
may appear in both places — which is fine, not duplication.

## Tightening 3 — a v4.5-era tag bible on a 5.5-default skill

**Problem.** The reference is sourced almost entirely from v4.5-era
community docs, but the skill defaults to **v5.5** (and v5.5 is where it
sends users first). The doc is least verified exactly where the flagship
model lives.

**Evidence.** Open Questions already flags MILO-1080, `[no vocals]`,
Voices, My Taste — but it reads as a footnote, not the priority it is.

**Fix.** Elevate: add a short **"v5.5 caveat"** callout near the top
stating the notation here is verified for v4.5 and *presumed* to carry
to v5.5 but not yet confirmed — and make "v5.5-specific notation
verification" the headline item for the next pass, not a buried open
question. The risk otherwise is that v5.5-specific behavior (the noted
vocal-hallucination-on-instrumental bug, My Taste personalization, the
`[no vocals]` token) silently changes how this notation lands and the
doc gives false confidence.

## Already-flagged, deferred (not new)

- The 200-emotion-word list (47 winners) should be extracted into a
  vocabulary table — already in Open Questions, second priority.
- The "first 20–30 words of the style prompt carry the most weight"
  claim is `[claimed]` not `[verified]` — worth a controlled test before
  it hardens into doctrine. Already in Open Questions.

## When to apply

Fold these into a **v2.1** of `references/lyrics-rhythm-craft.md` at the
next suno-pack maintenance pass. Tightening 1 and 2 are one-sentence
edits each; tightening 3 is a callout + reprioritization. None of them
blocks v2 from being used as-is right now — they're refinements, not
faults that would mislead a careful user.
