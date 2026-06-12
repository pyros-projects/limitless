# Pins on Mars — Experiments

*2026-06-12 — suno-pack · derived from concept.md · menu + field journal for all experiment rolls · journal synced from library 2026-06-12 (saga sync)*

How to use: pick a lane (or roll a d5), follow its recipe in the Suno
web UI — or tell the agent "give me experiment N" (one roll, ~10
credits, it asks before spending). One roll per lane, verdict in the
journal, go deeper only on keepers.
**Keep = like or better. ♥ a track in Suno and "sync the journal" does
the bookkeeping.**

## Menu

| # | Lane | Mutation axis | This pack's pre-roll | Cost | Requires |
|---|---|---|---|---|---|
| 1 | Genre Transposition | genre, wholesale | gospel soul lament | ~10 cr | seed take |
| 2 | Controlled Friction | emotional architecture | real-tears warmth vs friendship-computing grid | ~10 cr | — |
| 3 | Alternate-Reality Renders | performance reality | rehearsal room demo | ~10 cr | seed keeper |
| 4 | Red-Letter Mining | weirdness ceiling | drum machine, felt piano, pads, bass, lead synth | ~10 cr | — |
| 5 | Emotion Lexicon | style vocabulary | hiraeth | ~10 cr | — |

## Lane 1 — Genre Transposition
- Seed: best take from `runs/` (none yet — render the faithful pack first)
- Pre-rolled: **gospel soul lament** anchored by hammond organ, full
  choir, handclaps — thematically perfect (a song about faith without
  proof) and sonically maximally incompatible with deadpan minimalism
- Re-roll menu: baroque boom bap, shoegaze drill, big-band swing noir,
  cybergrind lullaby
- Web UI: open seed → Cover → v5.5 · style: `gospel soul lament, hammond
  organ, full choir, handclaps, raw congregation warmth` · weirdness 30 ·
  style influence 50 · audio influence 50 (sweep 30/50/70/85 if it hugs
  or drifts)
- Expected failure: genre gravity drags it back to the whisper. Keeper:
  you can hum the deadpan original over a congregation.

## Lane 2 — Controlled Friction
- Pair (derived — the dream literally contains it: a machine computing
  friendship vs real tears): **"real-tears vocal warmth, trembling
  sustain, hand-played felt piano + friendship-computing machine
  percussion, expressionless quantized grid, calculator-cold sub bass"**
  · swapped-poles re-roll: warm humanized drums under a flat,
  affectless, metronomic vocal
- Fresh generate, lyrics from `lyrics_v4.5.md` UNCHANGED · style: the
  pair above, genre-first: `minimal slowcore indietronica, real-tears
  vocal warmth, trembling sustain, hand-played felt piano,
  friendship-computing machine percussion, expressionless quantized
  grid, calculator-cold sub bass, 84 BPM` · weirdness 45–60 · style
  influence 75
- Expected failure: mush, or one pole wins. Keeper: the melody more
  alive than the faithful takes — friction audible as depth.

## Lane 3 — Alternate-Reality Renders
- Pre-rolled reality: **"rehearsal room demo"** — a song about an
  unfinished, roofless house belongs in an unfinished room. Alternatives:
  "Live Performance, Concert" / "MTV Unplugged, crowd sings along to the
  chorus" / "bootleg tape recording".
- Web UI: cover the keeper → style append `rehearsal room demo` ·
  weirdness 0 · style influence 50 · audio influence 100
- Expected failure: canned room cheese, vocal identity drift. Keeper: a
  convincing other room — the demo you'd put on the B-side.

## Lane 4 — Red-Letter Mining
- Palette (from concept): dusty drum machine, felt piano, warm analog
  pads, round muted bass, expressive muted lead synth
- Step 1: instrumental create · style: `dusty drum machine, felt piano,
  warm analog pads, round muted bass, expressive muted lead synth` ·
  weirdness 100 · style influence 80. Expect wreckage — you're
  prospecting.
- Step 2 ("tame it", separate roll): rebuild around the survivor at
  weirdness 25 / style 80.
- Keeper: a structure you would never have prompted directly.

## Lane 5 — Emotion Lexicon
- Concept mood (longing across an unreachable distance — Mars as the
  home you can't check on) → pre-rolled word: **hiraeth** (observed:
  reverb, slow attack — fits the fog and the lanes) · backup: saudade
  (minor 7ths)
- Fresh generate, faithful settings, weirdness +10 (55) · style:
  `hiraeth, minimal slowcore indietronica, 3AM bowling alley after
  close, lanes in fog, tape hiss, vocals from the next room, 84 BPM`
- Expected failure: the word routes to generic "melancholic". Keeper: a
  texture neither "sad" nor "wistful" produces — the word earns a
  permanent place in the pack's vocabulary.

## Field Journal

Verdicts use the honest scale: **love / like / nope / hate** — keep =
like or better. Art stays unmeasured; decisions and findings get
recorded. The note is the knowledge.

**Like-sync:** pressing ♥ in the Suno UI is the verdict pipeline — after
`sync --latest-only`, `is_liked` in the local store fills journal rows
as "like" (never downgrades, absence is never "nope"); upgrade your
loves by hand or by telling the agent.

| Roll | Date | Lane / move | Clip | Verdict | Note |
|---|---|---|---|---|---|
| 1 | 2026-06-12 09:43Z | faithful instrumental create ("Felt Piano Single", auto-titled) | 6c2baa58 / 1674786f | like | — |
| 2 | 2026-06-12 09:43Z | faithful create, incl. one 8-min take | 00c19600 (479s!) / bfe351e5 | like | the long take became cover fodder |
| 3 | 2026-06-12 09:55Z | Lane 1? Genre Transposition: "gospel soul lament" cover — tags match the pack's pre-roll; rolled by hand in the web UI | f8dfa59f / 875f2cf7 | like | seed bfe351e5; verdict inherited from the prior catch-all row, no per-take call recorded |
| 4 | 2026-06-12 09:57Z | Lane 3? "MTV Unplugged, crowd sings along" — first batch, both takes 478s | fa8fe562 / 20dc9742 | like | seed bfe351e5 per metadata; verdict inherited from the prior catch-all row |
| 5 | 2026-06-12 09:58Z | Lane 3: "MTV Unplugged, crowd sings along" | 3057481a (♥ synced from Suno like) / f5b60f75 | **love** | ARTIST-PRIOR CAPTURE: tag summons Clapton '92 — output reads as Tears in Heaven. Brand-name realities carry persona priors |
| 6 | 2026-06-12 10:01Z | Lane 3: "bootleg tape recording" | d15b2b49 / c215cfac | like | TEXTURE TRANSFORM: composes with source palette → Ulrich Schnauss / Boards of Canada territory. Medium realities carry texture priors |
| 7 | 2026-06-12 10:07Z | chained cover: bootleg take → BoC descriptor genome — first batch | 7b83613b / bf01191e | like | seed d15b2b49; verdict inherited from the prior catch-all row |
| 8 | 2026-06-12 10:07Z | chained cover: bootleg take → BoC descriptor genome | c6399d22 / ac61d7fa (♥ synced from Suno like) | **love** | persona-laddering by hand, 3 rungs deep; artist translated to descriptors since names don't transmit |

*Saga sync 2026-06-12: the former catch-all row ("everything else rolled
tonight — see library 09:43–10:07Z — like — all chirp-fenix (v5.5); no
wrecks, no dead air reported") was expanded into rows 3, 4, and 7, one
row per generation; its human verdict and note carry over as marked.
Lane attributions inferred from tags are marked with "?". All 16 clips
are chirp-fenix (v5.5).*

### Lineage tree (rebuilt from `metadata.cover_clip_id`, saga sync 2026-06-12)

```
6c2baa58  "Felt Piano Single"  194s  faithful instr take   (roll 1)
1674786f  "Felt Piano Single"  154s  faithful instr take   (roll 1)
00c19600  "Pins on Mars"       479s  faithful 8-min take   (roll 2)
bfe351e5  "Pins on Mars"       159s  faithful take         (roll 2)
├── f8dfa59f   gospel soul lament cover        159s  (roll 3)
├── 875f2cf7   gospel soul lament cover        160s  (roll 3)
├── fa8fe562   MTV Unplugged cover             478s  (roll 4)
├── 20dc9742   MTV Unplugged cover             478s  (roll 4)
├── 3057481a ♥ MTV Unplugged cover             158s  (roll 5, love)
├── f5b60f75   MTV Unplugged cover             161s  (roll 5)
├── d15b2b49   bootleg tape recording cover    153s  (roll 6)
│   ├── 7b83613b   BoC-descriptor cover        133s  (roll 7)
│   ├── bf01191e   BoC-descriptor cover        150s  (roll 7)
│   ├── c6399d22   BoC-descriptor cover        175s  (roll 8)
│   └── ac61d7fa ♥ BoC-descriptor cover        175s  (roll 8, love)
└── c215cfac   bootleg tape recording cover    135s  (roll 6)
```

Persona ladder (3 rungs): bfe351e5 → d15b2b49 (bootleg) → ac61d7fa ♥
(BoC descriptors).

### Open questions (saga sync 2026-06-12 — answer and re-sync)

1. **Stray candidates:** "I Found My Name in the Files" — 2 takes
   (ad002a2c, 16f20ccf), 2026-06-12 08:50Z, ~53 min before this pack's
   session. Tags share "indietronica" with this pack, but 98 BPM vs 84,
   different theme, and lineage ties to "Terminal Chime Memory"
   (2026-06-11) — looks like a separate project. Include in this pack's
   journal, or confirm they belong elsewhere?
2. **Credit total:** library shows 8 generations for this pack (80 cr);
   the prior journal estimated ~90 ("1 agent cover + 8 manual"). One
   generation is unaccounted for in the library — trashed roll, or
   miscount?
3. **Roll 4 parentage:** both takes are 478s (≈ the 479s long take) and
   the roll-2 note says "the long take became cover fodder", but
   `metadata.cover_clip_id` on every first-level cover says the seed was
   bfe351e5 (the 159s take). Metadata is recorded as truth above; flag
   if you remember covering 00c19600.

Running credit total: 80 confirmed in library (8 generations × 10 cr,
all 2026-06-12); prior journal estimate was ~90 — see open question 2.
