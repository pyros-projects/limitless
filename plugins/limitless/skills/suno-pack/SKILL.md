---
name: suno-pack
description: This skill should be used when the user wants to create music with Suno (AI music generation) — a song, track, beat, anthem, jingle, or instrumental — or wants to update, render, or experiment with an existing suno-pack — moving an old pack to Suno v6, rendering, library checks, one-roll experiment lanes, and saga-synced field journals. Produces a complete package for the Suno v6 family (v6, v6-wild, v6-mini) — concept document, style and lyrics prompts with v6 settings (Variety, Max Mode, Duration), instrumental variant, optional wild-to-v6 cover route, and an experiments lane book. Supports "--model", "--wild", and "--mode experimental". Responds to "suno-pack", "make a track in Suno", "write me a song", "Suno prompt", "lyrics for Suno", "instrumental version", "update my pack for v6", "render the pack", "make it real", "how are my Suno tracks doing", "suno experiment", "sync the journal", or any request to turn an idea, mood, or theme into Suno-ready prompts or tracks.
---

# Suno Pack

Turn a track idea into a complete, paste-ready Suno v6 package: a concept
document that gives the track a soul, then prompt artifacts that express it
with the settings that make v6 follow them.

**Core principle: concept before prompts.** A great track is not a pile of
genre tags — it is one emotional idea expressed through sound. Write the
concept first; derive every prompt from it. The prompts are the expression of
the concept, the same way a canvas expresses a design philosophy.

**Suno v6 only.** Suno retired every model before v6 on 2026-09-09 (v4.5,
v5, v5.5 …). Nothing new renders on them. Never write prompt files, settings,
or commands for a retired model; when a request or an old pack names one,
say so in one line and map it to the v6 family.

**REQUIRED REFERENCES:** Read `references/suno-v6-prompting.md` before
writing any prompt — it carries the truth: models, field limits, the
controls (Variety, Personalize, Max Mode, Duration, sliders), style field
order, metatags, the instrumental kit, covers, and known v6 behaviors.
Before authoring vocal lyrics, rewriting lyrics, or diagnosing lyric
density/flow problems, read `references/lyrics-rhythm-craft.md` — the lyric
beat-map and performance notation contract. Before ANY execution work
(rendering, covers, library, experiments, saga sync), read
`references/suno-cli.md` — the verified v6 command truth; for the browser
route additionally `references/browser-ui.md`, for experiment mode
`references/experiment-lanes.md`. Do not prompt
from memory of older Suno versions and do not improvise CLI flags.

## When to Use

- "Make me a track / song / beat about X"
- "I need Suno prompts for ..." / "lyrics for Suno"
- "Instrumental version of this idea"
- "Get my old pack ready for v6"
- Any creative brief — a mood, a scene, a story, a product, a feeling —
  that should become music.

Not for: composing sheet music, audio post-production advice, or non-Suno
generators (adapt the concept phase, but the prompt syntax is Suno-specific).

## Arguments

Parse from the invocation text; accept natural-language equivalents.

| Argument | Default | Effect |
|---|---|---|
| `--model <v6\|v6-wild\|v6-mini>` | `v6` | the model in every Settings block. v6-mini for Free accounts or sketches; v6-wild to explore |
| `--wild` | off | add the explore-then-finish route: `cover_v6-wild_v6.md` (generate on v6-wild, Cover the keeper on v6) |
| `--mode experimental [n\|list]` | faithful | experiment mode: random lane, lane *n*, or the lane menu — see `references/experiment-lanes.md` |

**Legacy `--versions` (4.5, 5, 5.5 …):** those models are retired. Say so in
one line, then map: one version → `v6`; several versions (the old
"author on one, render on another" chain) → `v6` plus the `--wild` route,
which is v6's version of that idea. Never emit a file for a retired model.

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
- **Sonic palette** — genre, instrumentation with roles, textures,
  production character, tempo feel, and the lead voice (human or instrument)
  that carries the melody, including where it sits in the mix.
- **Structure sketch** — the intended arrangement arc in plain language
  (how it opens, where the energy lifts, what contrast the bridge brings,
  how it closes) and the target length.
- **Generation notes** — model (v6 / v6-wild / v6-mini) and why, Max Mode
  plan, Duration, how many takes to budget, known v6 risks for this genre
  (e.g. long-song decay, genre normalization) and the workaround that
  applies, post-production flags (de-esser, mastering).

### 2.5 Write the lyric beat map (vocal/lyrics work only)

For any vocal track, lyric rewrite, or "lyrics for Suno" request, read
`references/lyrics-rhythm-craft.md` before writing the `## Lyrics` block.
Suno lyrics are not poems; they are a **beat map plus performance score**.

- Pick a cadence-reference artist by emotional intent before writing. Search
  for real lyric/form examples when tools are available; do not go from vibes
  and do not copy lyrics. Extract structure, line lengths, repetition/chant
  patterns, open-vowel releases, build devices (anaphora, call-and-response,
  wordless climb), negative space, and delivery/layering ideas, then write
  original lyrics with that rhythmic DNA.
- After every vocal `## Lyrics` block, add `## Lyric Form Inspiration` naming
  the artist(s) and song title(s) used for form/cadence inspiration, plus the
  specific structural observations borrowed. This is provenance for the human
  and a test surface for the skill; do not paste or quote lyric lines. If no
  search/source was available, say so instead of inventing references.
- Build the section skeleton first (`[Intro]`, `[Verse 1]`, `[Chorus]`,
  `[Bridge]`, `[Final Chorus]`, `[Outro]`, `[End]`).
- v6 follows **direction inside section tags** more reliably than any older
  model: give the sections that change the energy their direction in the
  bracket (`[Verse 1: soft, breathy, intimate]`,
  `[Chorus | full band, stacked harmonies]`), and give every instrumental gap
  a length and a job (`[Instrumental Interlude: 8 bars, fiddle answers the
  melody]`).
- Keep corresponding lines roughly within the ±2 syllable rule. Use short
  verses, tighter chantable choruses, and open-vowel release lines where the
  voice should soar.
- Preserve the source motifs, but spend one image per slot. Translate dense
  concepts, jargon, and stacked metaphors into singable concrete phrases.
- Use `[ ]` only for structure, arrangement, delivery, and section cues; use
  `( )` only for sung backing layers, echoes, ad-libs, or harmonies. Never put
  production instructions in parentheses or as bare text — bare text is sung.
- Add performance notation while writing: sparse backing echoes in `( )`,
  power words in CAPS (1-3 per section), sustained vowels with `...`, `~`, or
  repeated letters.
- End on `[Final Chorus]` → `[Outro: …]` → `[End]` — v6 otherwise likes to
  run long and loop.
- Verify line shape before claiming the lyric is fixed. If the lyric cadence
  implies a faster pulse, chant percussion, 6/8 feel, or a different BPM,
  update the style prompt too so music and words agree.

Pure instrumental/no-lyrics files do **not** use this as lyric authoring:
their Lyrics block remains structure tags only, starting with `[Instrumental]`
and ending with `[End]`, with no verses, sung words, ad-libs, or
parenthetical backing vocals.

### 3. Derive the prompts (one vocal + one instrumental file)

Every line of every prompt must trace back to the concept. Follow the
reference for syntax, limits, and field order:

- **Style of Music** — one block, 400–800 chars (≤1,000; truncation cuts the
  end), in the reference's priority order: genre first, mood/scene, lead
  voice with character and mix placement, players with roles, ONE
  arrangement arc, a production clause, BPM as a number, the ending. Comma
  list or short sentences both work; content and order matter. No negations
  (they go to Exclude), no artist names (translate to traits), no timing
  instructions (they go to section tags).
- **Exclude Styles** — every "no", plus the concept's known v6 risks (e.g.
  `muffled vocals, reverb wash, muddy` for vocal-forward tracks).
- **Lyrics** — from Step 2.5: concrete motifs, sparse density, verified line
  shape, per-section direction tags, a chorus that earns repetition, and
  one turn — a line or image that recontextualizes the song near the end.

Every prompt file carries a **Settings block** with the v6 defaults from the
reference, adjusted by the concept's Generation Notes: Variety **Off**,
Personalize Off, Weirdness, Style Influence, a **fixed Duration** that fits
the structure, the Max Mode plan, and the Lyrics Mode.

### 4. Write the wild-to-v6 route (only with `--wild`)

`cover_v6-wild_v6.md` documents the explore-then-finish route Suno itself
suggests for v6-wild: generate on v6-wild with the vocal or instrumental
file (Model row switched to v6-wild) until a take has the character, then
Cover it on v6 with a **minimal** style prompt (genre, era, production
character, BPM — the audio carries structure and lyrics), Variety Off, Max
Mode on, and the Audio Influence calibration from the reference. Label it
experimental: no published settings reliably preserve wild's character.

### 5. Emit the package

Create `~/.limitless/suno-pack/suno_<slug>/` by default — `<slug>` is
the track name, lowercased, spaces to underscores, ASCII only (e.g.
"Sodium Lights" → `suno_sodium_lights/`). Write elsewhere only when the
user explicitly chooses a path. Default file set:

```
~/.limitless/suno-pack/suno_<slug>/
├── concept.md
├── lyrics_v6.md
├── no_lyrics_v6.md
├── cover_v6-wild_v6.md            # only with --wild
└── experiments.md                 # concept-derived lane book: web-UI
                                   #  recipes + field journal (template +
                                   #  derivation rules in
                                   #  references/experiment-lanes.md)
```

`experiments.md` payloads are DERIVED from the concept (read the
derivation rules in `references/experiment-lanes.md` before emitting) —
pre-rolled picks with re-roll menus, never generic madlib fills. Packs no
longer ship `generate_*.sh` scripts; the skill renders them (see Make It
Real). Executed packs accumulate `audio/` and `runs/`.

Then present a compact summary: track name, premise line, file list, and the
output path, recommended order (draft with Max Mode off, final take with Max
Mode on), credit estimate (10 per generation, 20 with Max Mode), ending with
the handoff line: the pack is paper until the user says so — "say 'make it
real' to render it (credits, I'll confirm cost first), paste it into Suno's
Advanced mode yourself, or pick a lane from experiments.md / 'give me
experiment N'". Offer
variations (different genre lens, language, vocal swap, the `--wild` route)
as a follow-up, don't generate them unasked.

### Updating a pre-v6 pack

A pack with `lyrics_v4.5.md`, `lyrics_v5.5.md`, `cover_4.5_5.5.md`, or
`generate_*.sh` files predates v6. When asked to render, refresh, or "get it
ready":

1. Say in one line that its models are retired and the pack renders on v6
   now; old prompts don't transfer as-is.
2. Leave every existing file untouched — they are history, and old takes in
   the library stay valid.
3. Derive `lyrics_v6.md` and `no_lyrics_v6.md` from `concept.md` and the
   **v5.5 style block** (the closest shape), rewritten to the v6 style order.
   Never start from the v4.5 lean, conversational, or structured-object
   variants. Lyrics port; re-check them for per-section direction tags and
   the `[Final Chorus] → [Outro] → [End]` ending.
4. Add v6 Settings blocks. If `experiments.md` is missing, emit it.
5. For takes the user already loves in the library: offer Remaster on v6
   (same song, better audio) or Cover on v6 (reinterpretation) instead of
   re-rolling from scratch.

## Make It Real — Executing a Pack

Triggers: "render <prompt file>", "generate the pack", "make it real",
"run the cover pipeline", "remaster/cover/extend <take>", "how are my Suno
tracks doing". **Read `references/suno-cli.md` first — the only source of
command truth; never improvise flags.**

**Pick the route per request:**

| Situation | Claude with Claude in Chrome tools | Any other agent |
|---|---|---|
| Default render, cover, remaster, extend | **CLI route** (`suno`, always `--no-captcha`) | CLI route |
| `suno doctor` says captcha `required: true`, or a call returned `captcha_required` | **browser route** (`references/browser-ui.md`) on the user's real Chrome; the user solves any captcha | **paste route** |
| A setting the CLI cannot set is only part of the pack's defaults (Variety Off, fixed Duration in a faithful pack) | CLI route with server defaults; name what was not applied in the report and check stored tags after the roll | same |
| The request is ABOUT a control the CLI cannot set (Variety/My Taste experiment, Mumble, a Duration the user asked for, Remaster strength, image/video/MIDI/playlist input) | **browser route** | **paste route** |

Never run the CLI's built-in captcha solver, never a CDP automation browser
or stealth flags for generation, never `suno-pp-cli` generation commands
(it cannot send v6), never click a captcha yourself.

The execution loop (CLI route):

1. **Gates:** `suno` present → `suno doctor` healthy (refresh auth on
   `auth_expired`) → `suno credits`. A failing gate → the playbooks in the
   reference (offer install, user logs in in their own browser; never paste
   secrets; fall back to authoring work — never fabricate execution).
2. **Parse the prompt file:** Settings table → flags; `## Lyrics` block;
   `## Style of Music`; `## Exclude Styles`; `## Title`. Note every setting
   the CLI cannot apply.
3. **Already-ran check:** pack `runs/` hashes + library search — surface
   prior takes (and their verdicts) before spending. A request that
   explicitly asks for this re-render and approves the spend ("render it
   again, go") is the reason: say what exists and proceed.
4. **Preflight:** the exact command with `--dry-run` (free; generate and
   describe only).
5. **Confirm:** one line — estimated cost, credit balance, running pack
   total, prior-takes finding, settings the route cannot apply. Explicit
   user yes required for EVERY spending or mutating command; a yes already
   given in the request for this action counts — then state the line and
   fire, without asking again.
6. **Fire and land:** live command with a fresh `--request-id` and
   `--wait`; parse clip ids; download per clip into staging and move to
   take-aware names (`<slug>-<model>-take<N>-<clipid8>.mp3`); verify stored
   tags with `suno info`; write the immutable run log to `runs/`.
7. **Report:** files, clip ids, credits before/after, captcha state,
   stored-tags result, settings not applied. The human listens and judges;
   the skill never claims to have heard anything.

Browser route: the same loop with the UI as the generation step
(`references/browser-ui.md`); ids, downloads, and the run log still go
through `suno`. Paste route: hand the prompt file in Advanced-mode order
(Settings → Lyrics → Style → Exclude → Title) with the exact settings and
cost; after the user renders, saga sync records the takes.

Covers and remasters: the human picks the seed; the skill proposes from
observables (journal verdicts, likes, plays, lineage); `parent_clip` goes
into the run log.

## Experiment Mode

`--mode experimental` — **read `references/experiment-lanes.md` plus
`references/suno-cli.md` first.** One invocation = one lane = ONE roll;
cost stated before firing; unmet requirements (e.g. missing seed) are
resolved in conversation, never refused or silently re-rolled. The
pack's `experiments.md` is the menu source and journal ledger (emit it
first if the pack predates it). The roll follows the route table above: a
lane whose settings the CLI can send fires through `suno` after the yes;
a lane that needs Variety, My Taste, or another UI-only control goes
through the browser route (Claude) or becomes a paste recipe (other
agents). After the roll: run log with lane metadata, journal row appended
unverdicted, stop — depth (re-rolls, taming, sweeps) is always
human-triggered, one invocation each. Variety above Off is a legitimate
experiment axis here (never in faithful packs).

Verdicts are the field journal scale — love/like/nope/hate, keep = like
or better; no numeric scores on art, ever. ♥ in the Suno UI syncs as
"like" via saga sync.

## Saga Sync — Rebuild the Journal from the Library

Triggers: "sync the journal", "sync the pack", "rebuild the saga",
"update the journal from my library". Read-only, free, no confirmation
needed — recipes in `references/suno-cli.md` (Library & saga sync:
`suno-pp-cli` read-only commands, which still read v6 clips). The loop:
clips by pack title(s) → lineage closure via `metadata.cover_clip_id`
(rebuilds the full tree offline, including rolls made by hand in the web
UI) → strays by style/time-window surfaced as QUESTIONS, never silently
included or dropped → journal merge under the sacred rules: one row per
generation, `is_liked` → at least "like" (mark which clip carries the ♥),
never downgrade, never overwrite a human verdict or note, absence of a
like is never "nope" → render the lineage tree, update the running credit
total. Record each clip's model from its UI label
(`metadata.model_badges.songrow.display_name`, e.g. `V6-WILD`) —
`model_name` reports `chirp-hawk` for v6-wild too.

## Artifact Specs

Field order in every prompt file mirrors Suno's Advanced Mode UI top to
bottom, so the user can paste while scrolling: **Settings → Lyrics → Lyric
Form Inspiration (read-only provenance; do not paste to Suno) → Style →
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

### `lyrics_v6.md` — vocal version

```markdown
# <Track Name> — Vocal — <model>

## Settings
| Setting | Value |
|---|---|
| Model | <v6 \| v6-wild \| v6-mini> |
| Mode | Advanced |
| Lyrics Mode | Write |
| Variety | Off |
| Personalize | Off |
| Weirdness | <n>% |
| Style Influence | <n>% |
| Duration | <m:ss> (fixed) |
| Max Mode | off for drafts · on for the final take (2× credits) |
| Vocal Gender | <male \| female \| unset> |
| Takes to budget | <n> generations (2 songs each, 10 credits) |

## Lyrics
```text
[Intro: <texture descriptors>]

[Verse 1: <delivery/dynamics>]
...

[Chorus | <arrangement, layering>]
...

[Bridge: <contrast descriptors>]
...

[Final Chorus | <peak>]
...

[Outro: <wind-down descriptors>]
[End]
```

## Lyric Form Inspiration
| Artist | Song(s) studied | What was studied | How it shaped these lyrics |
|---|---|---|---|
| <artist> | <song title(s)> | <line length, repetition, open vowels, build, negative space, layering> | <specific original-form decision; no copied lyric lines> |

## Style of Music
```text
<v6 style prompt — genre first, mood, lead voice + placement, players with
roles, one arrangement arc, production clause, BPM, ending>
```

## Exclude Styles
```text
<comma-separated unwanted elements and the concept's v6 risk terms>
```

## Title
```text
<track title, ≤80 chars>
```
```

### `no_lyrics_v6.md` — instrumental version

Same layout and field order, with the full instrumental kit from the
reference:

- Settings block is SURFACE-AWARE: a `Lyrics Mode` row reading
  `Instrumental (simplest: style + Exclude carry it) · or Write + paste the structure-tags Lyrics block for arrangement control (re-roll if a voice leaks)`,
  no Vocal Gender row, and a note that a Voice cannot be attached to an
  instrumental.
- Lyrics block contains structure tags only — opening with `[Instrumental]`,
  every section naming the instrument that carries it, closing with `[End]`.
- Style block rewritten with zero vocal-adjacent words; the concept's melody
  carrier becomes an instrument description.
- Exclude block includes `vocals, singing, choir, spoken word, ad-libs, humming, wordless vocals`.

### `cover_v6-wild_v6.md` — explore-then-finish route (`--wild` only)

```markdown
# <Track Name> — Wild → v6 Finish

Explore on v6-wild (character), finish on v6 (polish). Experimental.

## Route
1. Generate on v6-wild with lyrics_v6.md / no_lyrics_v6.md (Model row → v6-wild;
   wild's Variety default is already Off) until a take has the character
   (budget <n> generations; wild's length varies — judge pairs).
2. Open the keeper → Cover → model v6.
3. Paste the minimal style prompt below. Do NOT re-enter lyrics — the audio
   carries them.
4. Calibrate Audio Influence per the protocol below.

## Settings
| Setting | Value |
|---|---|
| Model | v6 (Cover) |
| Variety | Off |
| Personalize | Off |
| Max Mode | On |
| Weirdness | 10–28% |
| Style Influence | 45–50% |
| Audio Influence | start 75% — calibrate, see below |

## Cover Style Prompt (minimal — genre, era, production, BPM only)
```text
<minimal re-render prompt>
```

## Audio Influence Calibration
No v6-specific official guidance exists — treat the slider as a dial. One
roll at 75%, then:
- the cover loses the wild take's character → raise toward 85%
- the cover is a near-clone that keeps wild's flaws → drop toward 60%
Change nothing else while calibrating. Expect 2–3 rolls.
```

## Quick Rules

| Rule | Why |
|---|---|
| v6 family only; map any older model name and say so | everything before v6 was retired on 2026-09-09 |
| Variety Off, Personalize Off in every faithful pack | above Off, Suno rewrites the style prompt before generating |
| Fixed Duration matched to the structure; end `[Final Chorus] → [Outro] → [End]` | Auto runs long and sparse; long takes decay after ~2–3 min |
| Max Mode off for drafts, on for the final take (2× credits) | Suno recommends it for songs over 2 min, covers, Voices |
| Style ≤1,000 chars (400–800), genre first, one arrangement arc, production clause, BPM number | truncation cuts the end; genre names carry context; competing instructions average out |
| Every "no" goes to Exclude; no artist names; no timing in the style field | v6 keeps the noun and drops the "no"; names are blocked; style controls what, not when |
| Direction inside section tags; every gap gets a length and a job | v6 follows tagged instructions most reliably; empty gaps get "oh-oh" fills |
| Instrumental = Lyrics Mode Instrumental (or Write + tags-only block) + clean style + Exclude vocals | the toggle is gone and vocals still leak |
| Canonical metatags only; `( )` only for sung backing | invented tags and bare text get dropped or sung |
| Cover style prompt minimal, Variety Off on covers | the audio carries the song; Variety makes cover melodies drift |
| Execute through `suno` with `--no-captcha`; captcha → the user solves it (browser route on Claude, paste route otherwise) | the CLI's solver evades bot detection; pp-cli cannot send v6 |
| Name every setting the route cannot apply; verify stored tags after the roll | the CLI cannot set Variety, Personalize, Duration |
| Explicit user yes before EVERY spend, cost stated first | `--yes`-style shortcuts never replace the user's yes |

## Common Mistakes

- **Prompting from memory of older Suno versions** — models, controls, and
  behavior changed; the reference is the truth.
- **Writing files for v4.5/v5.5 or a v4.5→v5.5 cover chain** — those models
  are gone; the v6 version of "explore then polish" is the `--wild` route.
- **Leaving Variety on its default** — on v6 and v6-mini it defaults to
  Normal and silently rewrites the carefully built style prompt.
- **Skipping the concept** and stacking genre tags — produces competent,
  soulless output. The concept is where "amazing" comes from.
- **Negations in the style field** ("no drums") — the model keeps "drums".
  Use Exclude and affirmative phrasing.
- **Timing in the style field** ("silence at 0:45", "verse 2 half-time") —
  ignored; use section order and tags.
- **Reusing the vocal style prompt for the instrumental** with "no vocals"
  appended — rewrite it clean.
- **Stage directions as parentheticals** (`(whispered)` on its own line) —
  use `[Bridge: whispered, stripped down]`.
- **Restating lyrics or structure in a cover prompt** — the source audio
  carries both; a long cover prompt only adds drift.
- **Ghost flags** (`--variety`, `--duration`, `--personalize`) or letting
  `suno` start its captcha solver — the flags don't exist and the solver is
  evasion; name what the CLI cannot set and pick a route.
- **Running pp-cli generate** — it cannot send v6; pp-cli stays read-only
  for saga sync.
