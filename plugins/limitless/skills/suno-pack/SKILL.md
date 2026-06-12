---
name: suno-pack
description: This skill should be used when the user wants to create music with Suno (AI music generation) — a song, track, beat, anthem, jingle, or instrumental — or wants to execute an existing suno-pack for real via the suno-pp-cli integration. Produces a complete track package (concept document, per-model-version style and lyrics prompts, instrumental variants, a cover/re-render workflow file, and runnable per-prompt scripts), and can render packs into actual tracks, run cover pipelines, check the local Suno library, and run one-roll experiment lanes. Supports version selection via arguments like "--versions 5.5 4.5" and experiment mode via "--mode experimental". Responds to "suno-pack", "make a track in Suno", "write me a song", "Suno prompt", "lyrics for Suno", "instrumental version", "render the pack", "generate it for real", "make it real", "run the cover pipeline", "how are my Suno tracks doing", "suno experiment", "surprise me with a Suno experiment", or any request to turn an idea, mood, or theme into Suno-ready prompts or finished Suno tracks.
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
for the v4.5-specific prompt styles and lore. Before ANY execution work
(rendering, covers, library, experiments), read `references/pp-cli.md` —
the verified command truth; for experiment mode additionally
`references/experiment-lanes.md`. Do not prompt from memory and do not
improvise CLI flags — model behavior, limits, and the CLI surface are all
version-specific.

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
| `--mode experimental [n\|list]` | faithful | experiment mode: random lane, lane *n*, or the lane menu — see `references/experiment-lanes.md` |

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
- **v4.5** — emit ALL prompt-style variants, each a translation of the
  *same* concept (styles defined in the v4.5 reference). The vocal file
  carries three — **A: lean tags**, **B: conversational-narrative**,
  **C: structured-object** — the instrumental file two (A and C, with
  the `vocals:` key dropped from C; conversational is excluded there
  because its prose is vocal-contaminated by nature and its structure
  narration is redundant when the lyrics block already carries
  arrangement tags). Mark exactly ONE variant **Recommended**, chosen
  from the concept: lean → niche genre adherence; conversational →
  structure-arc briefs; structured-object → era/artist-flavored briefs.
  All variants ≤500 chars, genre first; repeat the genre name for
  stubborn niches.

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
├── cover_4.5_5.5.md
├── generate_lyrics_v5.5.sh        # one runnable script per prompt file
├── generate_no_lyrics_v5.5.sh     # (template in references/pp-cli.md;
├── generate_lyrics_v4.5.sh        #  keep in sync when prompts change)
└── generate_no_lyrics_v4.5.sh
```

Experimental packs additionally carry `experiment_map.md` (template in
`references/experiment-lanes.md`); executed packs accumulate `audio/` and
`runs/`.

Then present a compact summary: track name, premise line, file list, and the
recommended pipeline order. Offer variations (different genre lens, language,
vocal swap) as a follow-up, don't generate them unasked.

## Make It Real — Executing a Pack

Triggers: "render <prompt file>", "generate the pack", "make it real",
"run the cover pipeline", "how are my Suno tracks doing". **Read
`references/pp-cli.md` first — it is the only source of CLI truth; never
improvise or guess flags.** The execution loop:

1. **Gates:** binary present → `doctor` healthy → `credits` checked.
   Any gate fails → the degradation playbooks in the reference (offer
   install / browser re-auth; never paste secrets; fall back to
   authoring-side work — never fabricate execution).
2. **Parse the prompt file:** Settings table → flags; `## Lyrics`
   fenced block; `## Title`; `## Exclude Styles`; the ★ Recommended
   style variant unless the user names one.
3. **Already-ran check:** pack `runs/` hashes + library grep — surface
   prior takes before spending.
4. **Preflight:** the exact command with `--dry-run` (free, validates
   flags).
5. **Confirm:** one line — estimated cost, credit balance, running
   pack total, prior-takes finding. Explicit user yes required for
   EVERY spending/mutating command; `--yes` never substitutes for it.
6. **Fire and land:** run with `--wait`; parse clip ids; per-clip
   download + take-aware rename (`<slug>-<model>-take<N>-<clipid8>.mp3`
   — NEVER `--download`, it collides on title); write the immutable
   run log to `runs/`; `sync --latest-only`.
7. **Report:** files, clip ids, credits before/after, captcha state.
   The human listens and judges; the skill never claims to have heard
   anything.

Cover pipeline ("run the cover pipeline"): same loop — seed picked by
the human from skill-proposed observable-cited candidates, cover command
truth and the no-slider-flags caveat per the reference, `parent_clip` in
the run log, lineage verified after sync.

## Experiment Mode

`--mode experimental` — **read `references/experiment-lanes.md` plus
`references/pp-cli.md` first.** One invocation = one lane = ONE roll;
cost stated before firing; unmet requirements (e.g. missing seed) are
resolved in conversation, never refused or silently re-rolled. After the
roll: run log with lane metadata, empty scorecard skeleton, stop — depth
(re-rolls, taming, sweeps) is always human-triggered, one invocation
each.

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

**v4.5 deviation — style variants:** in `lyrics_v4.5.md` the
`## Style of Music` section carries three labeled variants instead of one
block (two in `no_lyrics_v4.5.md`: A and C only). Shape:

```markdown
## Style of Music — pick one variant, test in order

### A — lean tags · wins on niche genre adherence
```text
<lean variant>
```

### B — conversational · wins on structure-arc briefs · ★ Recommended
```text
<narrative variant>
```

### C — structured-object · wins on era/artist flavor
*(reset Advanced Options before pasting)*
```text
<const-block variant>
```

Testing discipline: one roll per variant, judge on pairs (a flaw must
repeat to count), then iterate only the winner.
```

The ★ Recommended marker goes on whichever variant the concept favors —
users who don't want to experiment paste that one and ignore the rest.

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
| Style prompt is per-version: detailed for v5.x, variant menu for v4.5 | the models obey different prompt shapes |
| v4.5 files ship all style variants with one ★ Recommended | which dialect wins is empirical; one roll each, iterate the winner |
| Style ≤1000 chars (sweet spot 400–800 on v5.x, ≤500 on v4.5), genre first | overflow silently truncated; unrelated tag piles average into mush |
| Canonical metatags only; `[Tag: descriptors]` for per-section direction | invented tags get ignored or sung |
| Performance directions in bracket tags, never bare `(parentheses)` lines | parens are sung as backing vocals |
| Negations via Exclude field + affirmative style phrasing | v5.x largely ignores "no X" in style |
| No artist names, no mixing jargon, BPM as number | unreliable / ignored / approximate |
| Instrumental = toggle + `[Instrumental]` + clean style + exclude vocals | v5.5 hallucinates vocals; layer all defenses |
| Repeat identical chorus text; number the verses | melodic reinforcement, structure tracking |
| `[End]` on everything | prevents trailing audio |
| Cover style prompt stays minimal; sweep Audio Influence | style field weakly honored in covers; slider semantics unstable |
| Execution: explicit user yes before EVERY spend, cost stated first | `--yes` silences the CLI's prompt, not the user's |
| Never `--download` on generate; per-clip download + take-aware rename | title-named files collide — a paid take was destroyed this way (2026-06-11) |

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
- **Improvising pp-cli flags** (`--style`, `--prompt`, `--exclude-styles`)
  or probing generate commands with `--help` — the flag truth lives in
  `references/pp-cli.md`; validate with `--dry-run`, never a live call.
