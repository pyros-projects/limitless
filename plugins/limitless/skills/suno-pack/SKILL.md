---
name: suno-pack
description: This skill should be used when the user wants to create music with Suno (AI music generation) — a song, track, beat, anthem, jingle, or instrumental. Produces a complete track package (concept document, per-model-version style and lyrics prompts, instrumental variants, and a cover/re-render workflow file) ready to paste into Suno. Supports version selection via arguments like "--versions 5.5 4.5". Responds to "suno-pack", "make a track in Suno", "write me a song", "Suno prompt", "lyrics for Suno", "instrumental version", or any request to turn an idea, mood, or theme into Suno-ready prompts.
---

# Suno Pack

Turn a track idea into a complete, paste-ready Suno package: a concept
document that gives the track a soul, then per-version prompt artifacts that
express it — plus the cover pipeline that combines v4.5's prompt obedience
with v5.5's audio quality.

**Core principle: concept before prompts.** A great track is not a pile of
genre tags — it is one emotional idea expressed through sound. Write the
concept first; derive every prompt from it. The prompts are the expression of
the concept, the same way a canvas expresses a design philosophy.

**REQUIRED REFERENCES:** Read `references/suno-v5-5-prompting.md` before
writing any prompt — it carries the shared truth: field limits, the canonical
metatag taxonomy, per-version behavior and slider settings, the cover
workflow, and the instrumental anti-vocal-hallucination kit. When v4.5 is
among the requested versions, ALSO read `references/suno-v4-5-prompting.md`
for the v4.5-specific prompt styles and lore. Do not prompt from memory —
model behavior and limits changed across versions.

## When to Use

- "Make me a track / song / beat about X"
- "I need Suno prompts for ..." / "lyrics for Suno"
- "Instrumental version of this idea"
- Any creative brief — a mood, a scene, a story, a product, a feeling —
  that should become music.

Not for: composing sheet music, audio post-production advice, or non-Suno
generators (adapt the concept phase, but the prompt syntax is Suno-specific).

## Arguments

Parse from the invocation text; accept natural-language equivalents.

| Argument | Default | Effect |
|---|---|---|
| `--versions <v...>` | `5.5 4.5` | which model versions get prompt files (accepts `5.5 5.0 4.5`, comma-separated, or "only v5.5", "all versions") |
| `--no-cover` | cover on | skip the cover/re-render file |
| `--cover <from> <to>` | oldest→newest requested | override the cover chain endpoints |

Cover file rules: generated whenever ≥2 versions are requested — from the
**oldest** requested version (the authoring model, best prompt adherence) to
the **newest** (the rendering model, best audio). One version requested →
no cover file unless `--cover` says otherwise.

## Workflow

### 1. Absorb the brief

Take whatever the user gives — a phrase, a mood, a story, a genre. Parse
arguments. Infer boldly; ask only when a choice genuinely forks the work
(e.g. vocal language, explicit genre preference). If the user gave a track
name, keep it; otherwise name the track yourself — evocative, short, no
genre words.

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
- **Generation notes** — which versions are being targeted and why, the
  recommended pipeline (e.g. author on v4.5 → cover on v5.5), how many takes
  to budget per version, post-production flags (de-esser, mastering), and
  any niche-genre workaround that applies.

### 3. Derive the prompts (one vocal + one instrumental file per version)

Every line of every prompt must trace back to the concept. Follow the
reference for syntax, limits, and per-version prompt shape — **the style
prompt is version-specific, never copy-pasted across versions:**

- **v5.5 / v5.0** — detailed descriptor stack (4–7 categories, 400–800
  chars): genre, era, mood, adjective+instrument pairs, stacked vocal
  descriptors, production texture, BPM.
- **v4.5** — lean variant (≤500 chars) by default: genre first, core
  instruments, mood, BPM. Short and clear beats detailed. For stubborn
  niche genres, repeating the genre name measurably improves adherence.
  The v4.5 reference offers two more styles when the concept calls for
  them: conversational-narrative (structure direction in the style field —
  works on v4.5, fails on v5.5) and the structured-object technique for
  era/artist-flavored briefs.

The lyrics field ports across versions unchanged (same metatag system).
Write it as a lyricist, not a rhyme machine: concrete images from the
concept's motif list, singable line lengths, a chorus that earns repetition,
and one turn — a line or image that recontextualizes the song near the end.

Every prompt file carries a **Settings block** with the per-version slider
defaults from the reference (adjusted by the concept's Generation Notes).

### 4. Write the cover file (default on)

`cover_<from>_<to>.md` documents the re-render pipeline: pick the best
take from the authoring version, Cover it on the rendering version with a
**minimal** style prompt (genre, era, production character, BPM — the audio
carries structure and lyrics) and the Audio Influence sweep protocol from
the reference. This is the quality path for prompt-obedience maximalists.

### 5. Emit the package

Create `suno_<slug>/` in the current working directory — `<slug>` is the
track name, lowercased, spaces to underscores, ASCII only (e.g. "Sodium
Lights" → `suno_sodium_lights/`). Default file set:

```
suno_<slug>/
├── concept.md
├── lyrics_v5.5.md
├── no_lyrics_v5.5.md
├── lyrics_v4.5.md
├── no_lyrics_v4.5.md
└── cover_4.5_5.5.md
```

Then present a compact summary: track name, premise line, file list, and the
recommended pipeline order. Offer variations (different genre lens, language,
vocal swap) as a follow-up, don't generate them unasked.

## Artifact Specs

Field order in every prompt file mirrors Suno's Custom Mode UI top-to-bottom,
so the user can paste while scrolling: **Settings → Lyrics → Style →
Exclude → Title.**

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

### `lyrics_v<version>.md` — vocal version

```markdown
# <Track Name> — Vocal — v<version>

## Settings
| Setting | Value |
|---|---|
| Model | v<version> |
| Mode | Custom |
| Instrumental toggle | OFF |
| Weirdness | <n>% |
| Style Influence | <n>% |
| Takes to budget | <n> |

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

## Style of Music
```text
<version-appropriate style prompt — detailed stack for v5.x,
lean genre-first variant for v4.5>
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

### `no_lyrics_v<version>.md` — instrumental version

Same layout and field order, with the full anti-vocal-hallucination kit from
the reference:

- Settings block states: **Instrumental toggle ON**.
- Lyrics block contains structure tags only — canonical instrumental and
  dynamics tags, opening with `[Instrumental]`, closing with `[End]`.
- Style block rewritten with zero vocal-adjacent words; the concept's melody
  carrier becomes an instrument description (version-appropriate shape).
- Exclude block includes `vocals, singing, choir, spoken word, ad-libs`.

### `cover_<from>_<to>.md` — re-render pipeline

```markdown
# <Track Name> — Cover Pipeline v<from> → v<to>

Author on v<from> (prompt obedience), render on v<to> (audio quality).

## Pipeline
1. Generate on v<from> using lyrics_v<from>.md / no_lyrics_v<from>.md
   until a take nails song, structure, and feel (budget <n> takes).
2. Open the winning take → Cover → switch model to v<to>.
3. Paste the minimal style prompt below. Do NOT re-enter lyrics — the
   audio carries them.
4. Sweep Audio Influence per the protocol below.

## Settings
| Setting | Value |
|---|---|
| Model | v<to> (Cover) |
| Weirdness | 10–20% |
| Style Influence | 20–40% |
| Audio Influence | start 50% — sweep, see below |

## Cover Style Prompt (minimal — genre, era, production, BPM only)
```text
<minimal re-render prompt>
```

## Audio Influence Sweep
Cover behavior shifts between Suno backend updates — treat the slider as
a dial to calibrate, not a constant. One roll at 50%, then:
- output hugs the source too hard (near-clone) → drop toward 30%
- output drifts away from the song → raise toward 80%
Change nothing else while sweeping. Expect 2–4 rolls.
```

## Quick Rules

| Rule | Why |
|---|---|
| Style prompt is per-version: detailed for v5.x, lean for v4.5 | the models obey different prompt shapes |
| Style ≤1000 chars (sweet spot 400–800 on v5.x, ≤500 on v4.5), genre first | overflow silently truncated; unrelated tag piles average into mush |
| Canonical metatags only; `[Tag: descriptors]` for per-section direction | invented tags get ignored or sung |
| Performance directions in bracket tags, never bare `(parentheses)` lines | parens are sung as backing vocals |
| Negations via Exclude field + affirmative style phrasing | v5.x largely ignores "no X" in style |
| No artist names, no mixing jargon, BPM as number | unreliable / ignored / approximate |
| Instrumental = toggle + `[Instrumental]` + clean style + exclude vocals | v5.5 hallucinates vocals; layer all defenses |
| Repeat identical chorus text; number the verses | melodic reinforcement, structure tracking |
| `[End]` on everything | prevents trailing audio |
| Cover style prompt stays minimal; sweep Audio Influence | style field weakly honored in covers; slider semantics unstable |

## Common Mistakes

- **Prompting from memory of older Suno versions** — limits and behavior
  changed; the reference is the truth.
- **Skipping the concept** and stacking genre tags — produces competent,
  soulless output. The concept is where "amazing" comes from.
- **Copy-pasting the v5.5 style prompt into the v4.5 file** — v4.5 wants
  lean and genre-first; the detailed stack degrades adherence there.
- **Reusing the vocal style prompt for the instrumental** with "no vocals"
  appended — v5.5 will sing anyway. Rewrite it clean.
- **Stage directions as parentheticals** (`(whispered)` on its own line) —
  use `[Bridge: whispered, stripped down]`.
- **Restating lyrics or structure in the cover prompt** — the source audio
  carries both; a long cover prompt only adds drift.
