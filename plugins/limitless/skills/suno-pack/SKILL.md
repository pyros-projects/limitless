---
name: suno-pack
description: This skill should be used when the user wants to create music with Suno (AI music generation) — a song, track, beat, anthem, jingle, or instrumental. Produces a complete track package (concept document, style prompt, lyrics prompt, instrumental variant) ready to paste into Suno. Responds to "suno-pack", "make a track in Suno", "write me a song", "Suno prompt", "lyrics for Suno", "instrumental version", or any request to turn an idea, mood, or theme into Suno-ready prompts.
---

# Suno Pack

Turn a track idea into a complete, paste-ready Suno package: a concept
document that gives the track a soul, then prompt artifacts that express it.

**Core principle: concept before prompts.** A great track is not a pile of
genre tags — it is one emotional idea expressed through sound. Write the
concept first; derive every prompt from it. The prompts are the expression of
the concept, the same way a canvas expresses a design philosophy.

**REQUIRED REFERENCE:** Read `references/suno-v5-5-prompting.md` before
writing any prompt. It carries the current field limits, the canonical metatag
taxonomy, v5.5 behaviors, and the instrumental anti-vocal-hallucination kit.
Do not prompt from memory — model behavior and limits changed across versions.

## When to Use

- "Make me a track / song / beat about X"
- "I need Suno prompts for ..." / "lyrics for Suno"
- "Instrumental version of this idea"
- Any creative brief — a mood, a scene, a story, a product, a feeling —
  that should become music.

Not for: composing sheet music, audio post-production advice, or non-Suno
generators (adapt the concept phase, but the prompt syntax is Suno-specific).

## Workflow

### 1. Absorb the brief

Take whatever the user gives — a phrase, a mood, a story, a genre. Infer
boldly; ask only when a choice genuinely forks the work (e.g. vocal language,
explicit genre preference). If the user gave a track name, keep it; otherwise
name the track yourself — evocative, short, no genre words.

### 2. Write the concept (`concept.md`)

This is the design-document phase — the track's manifesto. 4–6 short
sections, written with conviction, generic enough to survive regeneration but
specific enough that two readers would imagine the same track:

- **Premise** — the one-sentence soul of the track. What it is *about*,
  emotionally, not musically.
- **Mood & emotional arc** — where it starts, where it peaks, how it ends.
  An arc, not a static adjective list.
- **Imagery & motifs** — the pictures the track should put in the listener's
  head. Concrete images (sodium streetlights, a coffee going cold), recurring
  motifs, the one detail that makes it specific.
- **Sonic palette** — era, instrumentation, textures, production character,
  tempo feel, and the lead voice (human or instrument) that carries the
  melody. Adjective+instrument pairs.
- **Structure sketch** — the intended arrangement arc in plain language
  (how it opens, where the energy lifts, what contrast the bridge brings,
  how it closes).
- **Generation notes** — model (v5.5 unless reason not to), slider settings,
  how many takes to budget, post-production flags (de-esser, mastering),
  and any niche-genre workaround that applies.

### 3. Derive the prompts (`lyrics.md`, `no_lyrics.md`)

Every line of every prompt must trace back to the concept. Follow the
reference for syntax and limits. Both files are copy-paste ready: each Suno
field is a fenced code block under a heading naming the field.

Write the lyrics as a lyricist, not a rhyme machine: concrete images from the
concept's motif list, singable line lengths, a chorus that earns repetition,
and one turn — a line or image that recontextualizes the song near the end.

### 4. Emit the package

Create `suno_<slug>/` in the current working directory — `<slug>` is the
track name, lowercased, spaces to underscores, ASCII only (e.g. "Sodium
Lights" → `suno_sodium_lights/`). Write the three files. Then present the
user a compact summary: track name, premise line, and where the files are.
Offer variations (different genre lens, language, female/male vocal swap) as
a follow-up, don't generate them unasked.

## Artifact Specs

### `concept.md`

```markdown
# <Track Name>

*Track concept — <date> — suno-pack*

## Premise
## Mood & Emotional Arc
## Imagery & Motifs
## Sonic Palette
## Structure Sketch
## Generation Notes
```

### `lyrics.md` — vocal version

Field order mirrors Suno's Custom Mode UI top-to-bottom, so the user can
paste while scrolling: Lyrics → Style → Exclude → Title.

```markdown
# <Track Name> — Vocal Version

Model: v5.5 · Custom Mode · Instrumental toggle OFF
Weirdness: <n>% · Style Influence: <n>%

## Lyrics
```text
[Intro: <texture descriptors>]

[Verse 1]
...

[Chorus]
...

[Bridge: <contrast descriptors>]
...

[Outro: <wind-down descriptors>]
[End]
```

## Style of Music (≤1000 chars, 4–7 descriptor categories, front-loaded)
```text
<genre/subgenre>, <era>, <mood>, <adjective+instrument ×2-3>,
<stacked vocal descriptors>, <production texture>, <BPM> BPM
```

## Exclude Styles (Advanced Options)
```text
<comma-separated unwanted genres/elements>
```

## Title
```text
<track title, ≤80 chars>
```
```

### `no_lyrics.md` — instrumental version

Same layout and field order (Lyrics → Style → Exclude → Title), with the
full anti-vocal-hallucination kit from the reference:

- Header states: **Instrumental toggle ON**.
- Lyrics block contains structure tags only — canonical instrumental and
  dynamics tags, opening with `[Instrumental]`, closing with `[End]`.
- Style block rewritten with zero vocal-adjacent words; the concept's melody
  carrier becomes an instrument description.
- Exclude block includes `vocals, singing, choir, spoken word, ad-libs`.

## Quick Rules (v5.5)

| Rule | Why |
|---|---|
| Style ≤1000 chars (sweet spot 400–800), 4–7 descriptor categories, genre first | overflow silently truncated; unrelated tag piles average into mush |
| Canonical metatags only; `[Tag: descriptors]` for per-section direction | invented tags get ignored or sung |
| Performance directions in bracket tags, never bare `(parentheses)` lines | parens are sung as backing vocals |
| Negations via Exclude field + affirmative style phrasing | v5.5 largely ignores "no X" in style |
| No artist names, no mixing jargon, BPM as number | unreliable / ignored / approximate |
| Instrumental = toggle + `[Instrumental]` + clean style + exclude vocals | v5.5 hallucinates vocals; layer all defenses |
| Repeat identical chorus text; number the verses | melodic reinforcement, structure tracking |
| `[End]` on everything | prevents trailing audio |
| Budget 3–5 generations | v5.5 variance is high |

## Common Mistakes

- **Prompting from memory of older Suno versions** — limits and behavior
  changed; the reference is the truth.
- **Skipping the concept** and stacking genre tags — produces competent,
  soulless output. The concept is where "amazing" comes from.
- **Reusing the vocal style prompt for the instrumental** with "no vocals"
  appended — v5.5 will sing anyway. Rewrite it clean.
- **Stage directions as parentheticals** (`(whispered)` on its own line) —
  use `[Bridge: whispered, stripped down]`.
- **Maxing out the style field** — 400–800 chars of intentional descriptors
  beats 1000 chars of noise.
