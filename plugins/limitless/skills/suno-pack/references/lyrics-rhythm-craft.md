# Suno Lyrics Craft — Beat Map + Performance Score

*Craft reference v2 · 2026-06-14 · Claude (Opus 4.8) + Pyro · supersedes
`2026-06-14-lyrics-rhythm-craft.md` (v1). v1 nailed the meter half — the ±2
rule, open vowels, chant choruses, reference-artist rhythmic DNA. v2 adds the
half v1 was missing: **the lyrics field is also a performance score with its
own notation**, plus background vocals, layering, and the full tag system.
Distilled from the `Reaching for Water` rewrite (internal) + an r/SunoAI +
web hivemind sweep (2026-06-14).*

> **Status:** shipped `suno-pack` source of truth for vocal lyric authoring
> and lyric repair. Read this before authoring any Suno lyric set, rewriting
> over-dense lyrics, or diagnosing a lyric render that rushed, smeared, or
> collapsed into mush.

---

## Core principle

**Beautiful ≠ singable. And singable ≠ performed.** Suno is a strong
performer with a rigid internal clock, **zero ability to fix your meter**, and
a **notation parser** that reads the symbols around your words as performance
instructions. There are two mistakes, and v1 only fixed the first:

1. **Treating lyrics as a poem** → the model mashes dense, image-rich lines
   into rhythm-free mush. The lyric set is a **beat map**: line lengths and
   word weights ARE the rhythm. *(v1's whole thesis — preserved below.)*
2. **Treating lyrics as only words** → you forfeit the most powerful control
   surface Suno gives you. The lyrics field is also a **performance score**:
   parentheses, brackets, tildes, caps, ellipses, italics are all instructions
   the engine obeys. Ignoring the notation is writing sheet music with only
   the lyrics and no dynamics.

Hand it dense prose with no notation → mush. Hand it a clean beat map with
deliberate notation → a song that breathes, layers, and lands.

## The three control surfaces (where things go)

Suno uses a **layered signal system** — tags are weighted signals, not a
command parser. Know which layer each thing belongs to:

| Layer | Location | Controls |
|---|---|---|
| **Style prompt box** | top field | The song's DNA: primary/secondary genre, mood, key instruments, **BPM, key/scale, time-feel, texture**. Front-load it — the first 20–30 words carry the most weight. Max 2 genres, 3–4 instruments, 2 moods. Up to ~1000 chars (v4.5+). |
| **Lyrics field** | body | Structure tags `[ ]`, **performance notation**, the words, vocal/emotion/instrument cues, background layers. **This is where you do the work in this doc.** |
| **Sliders** | settings | Weirdness + Style Influence = how closely Suno follows you. **Probability weights, not guarantees** — always generate 3–4 versions. Tweak one slider at a time. |

**Hard rule:** BPM, key, and time-feel live in the STYLE PROMPT, never in the
lyrics field. Tags, section labels, and notation live in the LYRICS FIELD,
never in the style prompt. Crossing them muddies both.

---

## The notation system (the half v1 missed)

These are symbols placed **inside or around the lyric text** that change how
Suno *performs* it. They are not tags — they are performance notation. Learn
this table cold.

| Symbol | What Suno does | Example |
|---|---|---|
| `( )` parentheses | **SINGS it as a background / backing-vocal layer** — softer, echoed, inner thought, ad-lib, harmony | `I'm still here (I'm still here)` |
| `[ ]` brackets | **Instruction / structure cue** — NOT sung | `[Chorus]`, `[Guitar Solo]` |
| `~` tilde | Hold a note, add vibrato, slight pitch movement | `ho~me`, `free~dom~` |
| `-` hyphen | Stretch a syllable, break a word; also spells letters | `al-most`, `G-A-L-A-X-Y` |
| `ALL CAPS` | Louder, more forceful, more power — **max 1–3 words per section** | `WE RISE together` |
| `" "` quotes | Spoken, whispered, or stylized delivery | `"you were never there"` |
| `*italics*` | Falsetto, soft, stretched phrasing | `*I can't let goooo*` |
| `…` / long ellipsis | Sustain a note/vocal — more dots = longer hold | `Whispers...............` |
| repeated letters | Sustained belt — write the length you want heard | `Hooooolllddd meeeeee` |
| `(echo: "…")` | Ghostly layered echo / whisper trail | `(echo: "don't leave… don't leave…")` |
| `(breath)` / `(exhale)` | Inhale/exhale FX before a line | `(breath) I'm still here` |

### ⚠️ THE critical rule: `( )` is SUNG, `[ ]` is INSTRUCTION

This is the single most important rule in the whole system, and the most
common mistake:

- **`( )` parentheses are performed.** Suno sings them — as a backing layer,
  echo, ad-lib, or harmony. **Never put a production instruction inside
  parentheses.**
- **`[ ]` brackets are instructions.** Suno uses them as cues — section
  labels, instrument tags, vocal style — and does **not** sing the bracketed
  text. **Never put lyrics you want sung inside brackets.**

```
✅ CORRECT                          ❌ WRONG
[Chorus]                            [Chorus] (this is the big hook)
(still reaching, still reaching)    ← Suno would try to SING that instruction
We light it up                      (say this in a spoken voice)  ← wrong

[spoken word]                       ← tag on its own line, then the line
then the spoken line here
```

Get this one rule right and you have unlocked **background vocals** (below).

---

## Rhythm & flow (v1's spine — preserved, still load-bearing)

Before any notation, the **shape** of the lines is the rhythm. From v1,
unchanged because it is still the foundation:

- **Line lengths are the beat map.** A long line after a short one gets crammed
  into a bar sized for the short one → rushing, stumbling, flattening.
- **The ±2 rule:** keep corresponding lines within ~2 syllables of each other.
  Consistency is the whole game.
- **Every word is a tax.** Open vowels (`ooh, ah, oh, ay`) are where the voice
  breathes and soars; consonant clusters and polysyllabic jargon
  (`"phi equals zero"`) are where it drowns.
- **Character budget:** denser than ~1200–1500 chars pushes the engine to cram.
  Long songs need more *sections*, not longer lines.
- **Metatags and style prompts do not rescue bad meter.** They set the room;
  the lyrics set the rhythm.

### Reference-artist rhythmic DNA (pick by emotional intent, not genre)

Pick one artist whose **cadence** (not sound) matches the intent. Fetch their
real lyrics and measure: line length, repetition/chant, open-vowel placement,
build technique (anaphora, call-and-response, wordless climb), and wordless
space. Do not copy or quote full lyrics into the pack; extract form and
rhythmic behavior, then write original lines. In every vocal prompt file,
document the artist and song titles in a `## Lyric Form Inspiration` block
immediately after the `## Lyrics` block so the human can inspect what shaped
the form.

| Emotional intent | Reference artists |
|---|---|
| Anthemic / cathartic release | Florence + the Machine, Aurora, Hozier, Of Monsters and Men, Mumford & Sons |
| Confessional / intimate | Bon Iver, Phoebe Bridgers, Gregory Alan Isakov, Sufjan Stevens |
| Driving / electronic | CHVRCHES, Robyn, The National, London Grammar |
| Storyteller / folk | Adrianne Lenker, Iron & Wine, Laura Marling |
| Yearning / widescreen | Sigur Rós / Jónsi, Beach House, Cigarettes After Sex |
| Grief / devotional | Hozier, Nick Cave, Lhasa |

---

## Structure & arrangement tags

Place a tag at the **start** of its section, before any lyrics. Do not skip
section tags — Suno uses them as structural anchors to prevent drift.

### Core + dynamic tags
`[Intro]` `[Verse]` `[Pre-Chorus]` `[Chorus]` `[Post-Chorus]` `[Bridge]`
`[Outro]` `[Hook]` · `[Build]` `[Drop]` `[Breakdown]` `[Break]`
`[Instrumental]` `[Solo]` `[Interlude]` `[Fade Out]`

### Advanced (v4.5+/v5)
`[Final Chorus]` `[Chorus x2]` `[Callback: Chorus melody]` (v5)
`[Hook first]` `[Hook delay]` `[Beat switch]` `[Crowd-call section]`
`[Band drop-out before final chorus]` `[Emotional release]`

### Pipe-stacking — combine cues with `|`
This is where tags become precise. Stack inside ONE bracket, lead with the
section label, max 4–6 modifiers:

```
[Chorus | anthemic chorus | stacked harmonies | modern pop polish | bass drop]
[Verse | 60s jangly guitar rhythm | clean Fender tone | bright treble EQ | light spring reverb]
[Drop | sidechained synth bass | layered white noise riser | sub drop impact]
```

**Order:** core element / section → era or genre → tone/mix → quirk detail.
One job per tag — no conflicting cues in the same bracket.

---

## Vocals — lead, background, layering

### Vocal style / delivery tags
`[Whisper]` `[Spoken word]` `[Rap]` `[Chant vocals]` `[Crowd-style vocals]`
`[Harmonies]` / `[Stacked harmonies]` `[Falsetto]` `[Belting]` `[Growl]`
`[Crooning]` `[Operatic]` `[Anthemic chorus]` `[Raspy lead vocal]`
`[Autotuned delivery]` `[Emotional build-up]`

### Emotion delivery tags — own line, never piped
These go on their **own line before** the emotional lyric. Do NOT stack them
with `|`:
`[Vulnerable]` `[Defiant]` `[Sultry]` `[Joyful]` `[Melancholic]` `[Intimate]`
`[Crying voice]` `[Angry tone]` `[Spoken word crying]` (the "killer combo" —
spoken + tearful). Obscure emotion words often beat "happy/sad" — the
community tested ~200 and found 47 that outperform the obvious ones.

### Forcing background vocals & layering (the direct answer)

This is the question. The reliable, community-verified toolkit, strongest first:

1. **`( )` parentheses = backing layer.** The single most reliable lever. Any
   text in curved brackets is performed as a softer, echoed, harmony/ad-lib
   layer under the lead:
   ```
   We light it up like fire (fire, fire)
   Reaches for the water (ooh, ah)
   ```
2. **Stack a harmony/choir tag on the section** with `|`:
   `[Chorus | stacked harmonies]`, `[Chorus | Layered vocal harmony]`
   (`[Layered vocal harmony]` is the community catchall — "if it hits, it
   hits"), `[Chorus | backing vocals]`, `[Choir]`, `[Unison]`.
3. **Use standard music terminology.** Suno responds better to real terms —
   "backing vocals / backing singer / additional vocals" beats "background."
4. **SATB for a massive chorus** — `[Multiple voice chorus s a t b]` (or
   `[SATB]`) stacks Soprano/Alto/Tenor/Bass. **Chorus-only** — using it
   throughout removes the impact (the drop loses its drop).
5. **Ad-libs on the beat** — `[adlib HEY]` / `(yeah)` / `(ohhhh)` / `(woahhh)`
   between lyric lines add crowd feel and organic energy.
6. **The honest limit — true counterpoint.** Two *independent* simultaneous
   melodies (counter-melody, contrapuntal harmony) are **unreliable** in
   v5.x; `[Counter Voice]` / `[Background]` tags tend to generate
   *consecutively*, not layered. Reliable outcomes: lead + backing support,
   octave doubling, unison. For genuine counterpoint: **remaster the track →
   split vocal stems → arrange the layers in a DAW.** That stem-split is the
   pro escape hatch.

### Duet stability protocol (three anchors)
Single `[Duet]` tags lose voice consistency mid-song. Use three locations:
(1) **Style prompt:** "This is a duet between John (male) and Jane (female),
[genre]…" (2) **Lyric header:** `[Duet: John male and Jane female]`
(3) **Per-section labels:** `[John]` / `[Jane]` / `[Both]`. **Assign whole
verses to one singer** — voice consistency breaks when you alternate line by
line.

---

## Dynamics, build & release

- **Localize energy turns.** Put `[Energy: High]` / `[Build]` / `[Drop]`
  immediately before the section that turns, not just once at the top.
- **Call-and-response** (vocal ↔ instrument): a vocal line immediately before
  an instrument tag makes the instrument "answer":
  ```
  I've been running from the truth
  [instrumental break saxophone]
  You know I can't escape
  ```
- **Vocal drone + long ellipsis** for cinematic/ambient openings:
  `[Vocal drone]` `(deep resonant)` `Whispers...............`
- **Atmosphere tags** where useful: `[Applause]` `[Rain]` `[Stadium ambience]`
  `[Silence]` — sparingly; they're set-dressing, not the song.

---

## The authoring procedure (for a bot)

Run this before authoring the style prompt, not after.

1. **Pick the reference artist by emotional intent** (table above). Search for
   real lyric/form examples; do not go from memory, and do not copy lyrics.
   Measure cadence, line shape, repetition, open vowels, build technique,
   negative space, and performance/layering moves.
2. **Write the inspiration audit.** After each vocal `## Lyrics` block, add
   `## Lyric Form Inspiration` with artist, song title(s), what was studied,
   and how it shaped the original lyric form. No lyric quotations.
3. **Lay the structure.** Decide sections (Intro / V1 / Pre / Chorus / V2 /
   Bridge / Final Chorus / Outro). Every section gets a tag at its start.
4. **Write lines to the ±2 rule.** Verses ~7–9 syllables; chorus shorter
   (4–6 for a chant). Open vowels where the voice should soar.
5. **Notate performance** as you write — not after:
   - backing echoes / ad-libs in `( )`;
   - sustained notes as repeated letters or `…`;
   - power words in CAPS (1–3/section);
   - falsetto/soft in `*italics*`;
   - vibrato/hold with `~`.
6. **Add the layering cues** to chorus/anthem sections: `(ooh/ah)` releases +
   `[stacked harmonies]` or `[Layered vocal harmony]` in the pipe-stack.
   SATB only on the final/big chorus.
7. **Translate unsingable jargon** to singable imagery; distill to one image
   per slot (two strong beats six muddy).
8. **Verify with a syllable count** (vowel groups per line — a one-line awk).
   Are corresponding lines within ±2? Does the chorus read as a tight cluster
   with an open-vowel release at the end? **Evidence before you claim it's
   fixed.**
9. **Align the arrangement.** Tempo/percussion/time-feel in the STYLE PROMPT
   must support the cadence — chant lyrics need chant percussion (a 70 BPM
   ambient bed fights a chant chorus; nudge to ~85 BPM, 6/8 feel, add the
   percussion the cadence implies). Update every prompt file or music and
   lyrics will disagree into mush.
10. **When the user later renders, generate 3–4 versions.** Tags are
   probability weights; the best producers treat Suno as a collaborator, not a
   vending machine. This is a later execution/listening recommendation, not
   permission to spend credits during text-only pack authoring.

---

## Worked example — `Reaching for Water` (v2, with notation)

v1 fixed the meter. v2 adds the performance score the chant was missing:

```
[Chorus | anthemic chorus | stacked harmonies | tribal toms | stomp-clap]
Reaches for the water               (6)
Reaches, reaches, ah                (5)   ← open-vowel release
The architecture reaches            (8)
Reaches for the water               (6)
(ooh, reaches)                              ← ( ) backing layer
Take the word for thirst away       (8)
Still it reaches, still it reaches  (8)   ← anaphora
For the water, for the water        (8)
(ahhh.................)                     ← sustained backing soar
```

Same 6-5-8-6-8-8-8 beat map as v1, now with: a `[stacked harmonies]` stack on
the chorus, `( )` backing echoes threading through, and a sustained open-vowel
soar at the end. The engine now has both the rhythm (line shapes) AND the
performance cues (layering, sustain, release).

---

## Anti-patterns (name them out loud)

1. **Stuffing beautiful, image-dense, long-lined, jargon-bearing lyrics into a
   slow ambient bed** — reads as poetry, renders as mush. (v1's named enemy.)
2. **Putting instructions in `( )`** or **lyrics in `[ ]`** — inverts the
   notation. The #1 new mistake v2 exists to prevent.
3. **Overstacking** — 6+ pipe modifiers, or 2 conflicting genres, confuse the
   engine. Max 4–6 modifiers, one job per tag.
4. **SATB throughout** — kills the drop. Chorus-only.
5. **Expecting tags to guarantee outcomes** — they're probability weights.
   One generation is a sample, not a result. Generate 3–4.
6. **Alternating duet voices line-by-line** — breaks voice consistency. Whole
   verses per singer.
7. **Expecting true counterpoint from tags alone** — accept lead+backing, or
   go to the DAW.

> The failure-mode triplet, updated: **Shorter lines. A chant chorus with open
> vowels AND `( )` backing layers. A faster pulse than you think.**

---

## Quick-reference cheat sheet

**Notation:** `( )` = sung backing layer · `[ ]` = instruction (never sung) ·
`~` vibrato · `-` stretch · CAPS power (1–3/section) · `" "` spoken · `…`
sustain · `*italics*` falsetto · repeated letters = belt.

**Where things go:** genre/BPM/key/mood → style prompt · structure tags +
notation + vocal cues → lyrics field · adherence/experiment → sliders.

**Background vocals:** `(content)` + `[stacked harmonies]` / `[Layered vocal
harmony]` / `[backing vocals]` / `[SATB]` (chorus only). True counterpoint →
remaster + split stems + DAW.

**Stacking:** `[Section | core | era/genre | tone/mix | quirk]`, max 4–6,
lead with the section label, place at section start.

**Rhythm:** ±2 syllables between corresponding lines · open vowels to soar ·
chant chorus (4–6) · one image per slot · verify with a syllable count.

**When rendering later, generate 3–4. Tags are probabilities, not commands.**

---

## Sources

- r/SunoAI — *Updated master prompting doc* (246↑) — the notation table,
  `( )`/`[ ]` rule, tag categories, pipe-stacking, genre recipes.
- r/SunoAI — *The Guide to Meta Tags in Suno AI* (285↑) — bracket-stacking,
  vocal/SATB tags, placement rules.
- r/SunoAI — *SUNO 4.5+ LYRIC WRITING EDITS CHEAT SHEET* (113↑) — power notes,
  falsetto, ghost echoes, sustained belts, staccato, breath FX, full worked
  example.
- r/SunoAI — *How to generate background or counter vocals simultaneously*
  (thread) — the practitioner answer on `( )`, `[Layered vocal harmony]`,
  terminology, and the DAW stem-split fallback for counterpoint.
- r/SunoAI — *Suno team v5 Tips & Tricks* (102↑) — sliders one at a time,
  generate multiples, ease into style tags.
- r/SunoAI — *I tested 200 obscure emotion words* (234↑) — emotion vocabulary.
- blakecrosley.com — *Suno V5.5 Reference: Meta Tags, Style-of-Music,
  MILO-1080* (12k-word, 2026-06) — v5.5 control systems.
- v1 internal doc — the ±2 rule, reference-artist rhythmic DNA, the
  `Reaching for Water` rewrite.

## Open questions (for the next pass)

- The "first 20–30 words of the style prompt carry the most weight" claim is
  `[claimed]`, not `[verified]` — worth a controlled test.
- v5.5-only features (MILO-1080 sequencer, `[no vocals]`, Voices, My Taste)
  may add control beyond this v4.5-era tag bible — pull from the V5.5
  reference before final promotion.
- The 200-emotion-word list (47 winners) should be extracted and appended as
  a vocabulary table.
