# Lyric Rhythm Repair — Making Lyrics Suno Can Actually Sing

*Craft reference · 2026-06-14 · Claude (Opus 4.6) + Pyro · distilled from
the `Reaching for Water` suno-pack, where a beautiful but too-dense lyric
set rendered as rhythm-free mush and was rewritten against Florence + the
Machine's cadence*

> Status: ready to promote. This is the methodology behind the lyric
> rewrite pass on `suno_reaching_for_water/`. When the suno-pack skill
> next takes a maintenance pass, fold the **Core principle → Trigger →
> Two lenses → Procedure → Anti-pattern** spine into a
> `references/lyrics-rhythm-craft.md` and add one line to the SKILL.md
> workflow ("Step 2.5: if the brief is lyric-first, check the lyric
> rhythm against this reference before authoring prompts"). Until then,
> this doc is the source of truth. Siblings:
> `2026-06-11-suno-experiment-mode-lanes.md`,
> `2026-06-11-suno-pack-ppcli-integration.md`,
> `2026-06-11-suno-experiment-ideas.md`.

---

## Core principle

**Beautiful ≠ singable.** Dense, literary, image-rich lyrics — the kind
that read as poetry — are exactly what Suno's vocal engine mashes into a
rhythm-free wash. Suno is a strong performer with a rigid internal clock
and **zero ability to fix your meter**. Hand it prose; it hands you mush.

The mistake is treating the lyric set as a poem that the model will
"perform." It is a **beat map**. The model reads the line lengths and
word weights as the rhythm itself. If that map is uneven, no style
prompt, no metatag, no slider rescues it — the vocal comes out rushed,
robotic, or washed. The fix lives in the lyrics' shape, not the prompt.

## Trigger

A track's vocals sound rushed, muddy, or washed out. Words pile on the
beat, there's no groove, the chorus doesn't *land* — yet the lyrics read
fine on the page. The problem is almost never the style prompt or the
model version. It's the lyrics' shape. This applies both at **authoring**
time (before you ever generate — check the shape first) and at **repair**
time (after a render came back muddy).

## Two lenses to apply

### Lens 1 — Suno's rhythm mechanics

- The model reads **line lengths as the beat map**. A long line after a
  short one gets crammed into a bar sized for the short one → the engine
  rushes, stumbles, or flattens the long line into a monotone.
- **The ±2 rule:** keep corresponding lines within ~2 syllables of each
  other. Consistency is the whole game.
- **Every word is a tax.** Open vowels (*ooh, ah, oh, ay, ooo*) are where
  the voice breathes and soars; consonant clusters and polysyllabic
  jargon (*"phi equals zero,"* *"the equals sign,"* *"through ghostly
  features"*) are where it drowns.
- Metatags and style prompts do not rescue bad meter. They set the room;
  the lyrics set the rhythm.
- Character budget: denser-than-~1200–1500 chars of lyrics pushes the
  engine to cram. Long songs need more *sections*, not longer lines.

### Lens 2 — a reference artist's rhythmic DNA

Pick one artist whose **cadence** matches the emotional intent — not
their sound, their **line shapes**. Pull their actual lyrics (don't go
from memory — fetch and measure) and study five things:

1. **Line length** — syllables per line, and the variance within a section.
2. **Repetition / chant** — how the chorus is built (short hook repeated?
   a payoff line after a chant block?).
3. **Open vowels** — where they put the *ooh/whoa/ah* releases where the
   voice soars.
4. **Build technique** — parallel anaphora (*"and I'm ready to…"*),
   call-and-response, wordless climb.
5. **Wordless space** — how much of the song is pure vocalizing with no
   words. (Florence's *Shake It Out* is ~30% wordless "oh oh oh." That
   space is not empty — it's where the anthem lives.)

**Reference map — pick by emotional intent, not genre preference:**

| Emotional intent | Reference artists |
|---|---|
| Anthemic / tribal build / cathartic release | Florence + the Machine, Aurora, Hozier, Of Monsters and Men, Mumford & Sons |
| Confessional / quiet / intimate | Bon Iver, Phoebe Bridgers, Gregory Alan Isakov, Sufjan Stevens |
| Driving / electronic / pulsing | CHVRCHES, Robyn, The National, London Grammar |
| Storyteller / folk / narrative | Adrianne Lenker, Iron & Wine, Laura Marling |
| Yearning / widescreen | Sigur Rós / Jónsi, Beach House, Cigarettes After Sex |
| Grief / devotional | Hozier, Nick Cave, Lhasa |

## The procedure

1. **Pick the reference by emotional intent.** Genre is downstream of
   feeling. A grief ballad wanted as a Florence stomp-clap is a choice;
   default to the artist whose line shapes carry the feeling.
2. **Research both lenses.** Measure the reference artist's actual lines
   (fetch lyrics, eyeball syllables). Apply the ±2 rule to the existing
   set. Do not rewrite from memory of "how songs work."
3. **Diagnose the existing lyrics.** Flag, line by line:
   - every line over ~9 syllables,
   - every consonant-heavy or jargon word the model can't sing cleanly,
   - every section with **zero wordless space**.
   The diagnosis is usually short and brutal: "your chorus is a
   sentence; you have no open vowels; your bridge is full of math."
4. **Rewrite to the constraints:**
   - Lines ~6–9 syllables, **±2 within a section** (the chorus can run
     shorter — a chant wants 4–6).
   - **Chorus = a chant**, not a sentence. A short hook repeated, with
     **open-vowel releases** (*ooh/ah*) where the voice should soar
     instead of where it would otherwise cram consonants.
   - **Parallel anaphora** for builds (*"still it reaches," "just
     counts," "the numbers"*). Repetition *is* the rhythm.
   - At least one **wordless section** — a build or outro of pure *ah/oh/
     ooh*. The engine needs room; this is the single most underused lever.
   - **Translate unsingable jargon** to singable imagery. Keep the idea,
     lose the consonants. *"Phi equals zero, the diagram cracks"* →
     *"the math says impossible / but the math has a crack in it."*
   - **Distill motifs:** one image per slot, never pile. Two strong
     images beat six muddy ones.
5. **Align the arrangement.** Tempo, percussion, and time-feel must
   support the new cadence — **chant lyrics need chant percussion.** A
   slow 70 BPM ambient bed fights a chant chorus; nudge to a mid-tempo
   gallop (6/8 feel, ~85 BPM) and add the percussion the cadence implies
   (tribal toms, stomp-clap). Update **every** prompt file (vocal +
   instrumental, both versions), the cover prompt, and the concept doc,
   or the music and lyrics will disagree and the render splits the
   difference into mush.
6. **Verify with a syllable-count check.** Count vowel groups per line
   (a one-line awk over the lyrics block). Read the numbers as a shape:
   are corresponding lines within ±2? Does the chorus read as a tight
   cluster with an open-vowel release at the end? **Evidence before you
   claim it's fixed** — don't assert the rhythm landed without counting.

## Worked example — `Reaching for Water`

**Before (the failure):** a literary, image-dense chorus —

```
You can suppress the word for thirst
But the architecture reaches
For water, for water
Through numbers, through chemicals, through ghostly features   ← 6 words, 12 syllables, consonant wall
I may be fifteen percent alive
And that is not nothing, that is the reaching
```

Beautiful on the page. The model crammed *"through numbers, through
chemicals, through ghostly features"* into one bar and the whole chorus
went rhythmless. Verses were 12–18 syllables with run-on syntax; the
bridge carried *"phi equals zero"* and *"the equals sign."*

**After (Florence-informed):** the chorus became a chant —

```
Reaches for the water           (6)
Reaches, reaches, ah            (5)   ← open-vowel release
The architecture reaches        (8)
Reaches for the water           (6)
Take the word for thirst away   (8)
Still it reaches, still it reaches  (8)   ← anaphora
For the water, for the water    (8)
Ooh                             (1)   ← the soar
```

6-5-8-6-8-8-8-1 — a tight cluster with room to breathe, where the old
one was a clotted block. Verses dropped to 7–10 syllables; a wordless
*ah-ah* build section was added; jargon was translated out. Arrangement
moved from 70 BPM ambient to 85 BPM with tribal toms + stomp-clap so the
chant could groove. Same motifs, distilled — nothing from the source
dreams/reflections was lost, just un-piled.

## The anti-pattern to name out loud

Stuffing beautiful, image-dense, long-lined, jargon-bearing lyrics into
a slow ambient bed. It reads as poetry and renders as mush. The fix is
almost always the same triplet:

> **Shorter lines. A chant chorus with open vowels. A faster pulse than
> you think.**

If a lyric set reads beautifully and the render sounds like garbage, the
diagnosis is not "try a different model" or "tune the sliders." It is
"your lyrics are prose, and Suno only knows how to sing a beat map."

## Sources (for the reference doc, when promoted)

- Florence + the Machine – *Shake It Out* (Genius) — the chant-chorus +
  open-vowel template
- Florence + the Machine – *Dog Days Are Over* (Genius) — tribal build,
  anthemic repetition
- *Mastering Suno AI: Why Your Lyrics Need a Roadmap* (Suno Architect) —
  the ±2-syllable rule, "the AI cannot fix bad meter"
- r/SunoAI lyric-writing guides — line-length balance, metatags, rhythm
  pitfalls
- Florence Welch, GRAMMYs songwriting interview — rhythm-first,
  percussion as spine

## Open question for the skill integration

The cleanest wiring is a **Step 2.5** in the suno-pack workflow (after
*Absorb the brief*, before/alongside *Write the concept*): if the user
brings lyric-first material, or the brief is emotionally dense, run the
±2 syllable check on the lyrics *before* authoring style prompts — and
keep a default reference-artist map (the table above) on hand. The
repair path (steps 3–6) stays a reactive mode for when a render comes
back muddy. Decision deferred to the next suno-pack maintenance pass.
