# Suno v5.5 Prompting Reference

Research compiled 2026-06-10 from official Suno docs, the blakecrosley.com v5.5
reference (verified current as of 2026-06-08), hookgenius/songaifarm/roo 2026
guides, JG BeatsLab behavioral testing, and r/SunoAI community threads.
Re-verify against suno.com/blog and help.suno.com if more than ~3 months old.

## Version State (June 2026)

- **v5.5 is the flagship** (released 2026-03-26). It is a personalization
  layer on v5 (Voices, Custom Models, My Taste) — same audio engine, better
  expressiveness on nuanced descriptors.
- **Full backward compatibility**: all v5 prompts, metatags, and style tags
  work identically in v5.5. Nothing was removed.
- v5.5 interprets subtle production descriptors that older models ignored
  ("slightly detuned vintage keys" actually lands now).

## Field Limits

| Field | Limit | Sweet spot |
|---|---|---|
| Style of Music | 1,000 chars (v5/v5.5) | 400–800 chars, 4–7 descriptors |
| Lyrics | 5,000 chars | 30–40 lines for a 3–4 min song |
| Title | 80 chars | descriptive; no musical effect |
| Exclude (Advanced Options) | short list | comma-separated elements/genres |
| Max generation length | 8 min | extend via Song Editor |

Overflow is **silently truncated** — front-load what matters.

## Style Field

Comma-separated descriptor stack. Order by priority (truncation-safe):

```
[genre/subgenre], [era], [mood 2-3 words], [key instruments, adjective+instrument],
[vocal character, 2-3 stacked descriptors], [production texture], [tempo/BPM]
```

- **4–7 descriptor categories** is the tested optimum (genre, era, mood,
  instruments, vocals, production, tempo). Comma-phrases *within* a category
  don't count separately — "warm Juno pads, pulsing Moog bass" is one
  instrumentation category. <4 categories = generic defaults; piling on
  unrelated categories = competing signals that average into mush. The char
  sweet spot (400–800) is the better guardrail.
- Adjective+instrument pairs: "overdriven guitars", "brushed drums",
  "warm Rhodes piano" — never bare "guitar".
- Vocal descriptors stack 2–3 deep: "raspy female vocals, intimate close-mic
  delivery, mid-register".
- BPM is treated as **approximate guidance**, not exact. Still worth giving
  as a number ("84 BPM"), not prose ("slowish").

**What does NOT work in the style field:**

- Artist names (unreliable; translate to descriptive equivalents)
- Technical mixing jargon ("sidechain compression" is ignored)
- Negative instructions ("no drums") — v5.5 often "accepts your constraint,
  then produces exactly what it wants anyway" (JG BeatsLab testing). Use the
  Exclude field and affirmative phrasing instead: "intimate close-mic vocal,
  zero reverb, raw acoustic capture" beats "no reverb, no autotune".
  (Some 2026 guides still recommend "no X" tags; treat them as a secondary
  reinforcement, never the primary mechanism.)

## Exclude Field (Advanced Options)

Official negative-prompt surface: comma-separated instruments, genres, vocal
styles you don't want ("drum and bass, hiphop", "choir, falsetto"). First
option under Advanced Options. More reliable than in-style negations.

## Lyrics Field Metatags

Square brackets, case-insensitive, processed as arrangement directives (not
sung). Numbered sections help Suno track structure: `[Verse 1]`, `[Verse 2]`.
Repeat identical chorus text for melodic reinforcement.

**Structural:** `[Intro]` `[Verse N]` `[Pre-Chorus]` `[Chorus]`
`[Post-Chorus]` `[Bridge]` `[Breakdown]` `[Build]` `[Drop]` `[Hook]`
`[Interlude]` `[Outro]` `[End]` — `[End]` gives a hard stop and prevents
trailing audio.

**Instrumental:** `[Instrumental]` `[Instrumental Intro]`
`[Instrumental Break]` `[Guitar Solo]` `[Piano Solo]` `[Drum Solo]`
`[Bass Solo]` `[Synth Solo]` `[Saxophone Solo]` `[Percussion Break]`
`[Strings Rise]`

**Vocal:** `[Male Vocal]` `[Female Vocal]` `[Androgynous Vocals]` `[Duet]`
`[Choir]` `[Harmony]` `[Rap]` `[Spoken Word]` `[Whisper]` `[Scream]`
`[Ad-lib]` `[Humming]` `[Backing Vocals]` — delivery tags also:
`[Whispered]` `[Spoken]` `[Belted]` `[Falsetto]` `[Rap Verse]`
`[Call and Response]`

**Dynamics/production:** `[Fade In]` `[Fade Out]` `[Silence]` `[Crescendo]`
`[Decrescendo]` `[Tempo: slow]` `[Key Change]`

**Parameterized syntax** — per-section override of the global style:

```
[Verse: whispered vocals, acoustic guitar only]
[Chorus: full production, soaring vocals, epic drums]
[Bridge: stripped down, piano only, vulnerable delivery]
```

`[Tag: descriptor, descriptor]` — colon signals modifiers to the arrangement
engine. This is the correct place for performance directions.

**Rules:**

- Stick to canonical tags or parameterized variants of them. Invented tags
  (`[Theme A]`, `[Main Melody]`) are unreliable — they may be ignored or sung.
- Performance directions go in bracket tags, never as bare parenthetical
  lines. A line like `(quiet, almost spoken)` risks being sung verbatim.
- Parentheses inside lyric lines are for **sung** backing phrases/ad-libs:
  `Burning alone (burning alone)`.

## Instrumental Tracks — Anti-Vocal-Hallucination Kit

v5.5 has a **known community-confirmed bug**: it adds vocals/ad-libs/nonsense
lyrics to instrumental requests far more than v5 did (multiple r/SunoAI
threads, March–June 2026). Layer ALL of these:

1. **Surface truth first (operator-observed 2026-06-12):** in the web
   UI the Instrumental toggle and the Lyrics box are MUTUALLY
   EXCLUSIVE — toggle ON disables/clears the Lyrics box — and v5.5
   Custom Mode shows NO instrumental toggle at all. Via CLI/API both
   transmit together (`--instrumental` + `--lyrics`, verified live
   2026-06-11). So:
   - **CLI render:** `--instrumental` flag + the structure-tags Lyrics
     block — use both, full kit.
   - **Web UI, v4.5:** leave the toggle OFF and paste the
     structure-tags Lyrics block (arrangement control matters and
     v4.5's hallucination risk is low). Toggle ON only if you accept
     losing the Lyrics block — then style + Exclude carry everything.
   - **Web UI, v5.5:** no toggle exists — the structure-tags Lyrics
     block, clean style, and Exclude ARE the whole defense.
2. Lyrics block: **structure tags only**, starting with
   `[Instrumental]` and using only instrumental/dynamics tags.
3. Style field: purely instrumental language. **Remove every vocal-adjacent
   word** — "vocal-like lead", "choir pads", "wordless vocals", "humming"
   all invite hallucinated vocals. Describe the lead instrument instead:
   "expressive lead synth carrying the main melody".
4. Exclude field: `vocals, singing, choir, spoken word, ad-libs`.
5. Still getting vocals? Regenerate (v5.5 variance is high), or generate the
   track, then take the instrumental stem from Get Stems. Note: stem-stripping
   a vocal take leaves arrangement holes where vocals sat — a dedicated
   instrumental generation usually beats stripping.

## Creative Sliders

| Slider | Guidance |
|---|---|
| Weirdness | 40–60% default; <20% commercial/safe; 30% for stubborn niche genres; >80% chaos/sample-fishing only |
| Style Influence | 40–70% balanced; 80–100% strict adherence (use for niche genres v5.5 tries to normalize) |
| Audio Influence | covers/remixes only; see Cover Workflow — behavior is unstable, start ~50% and sweep |

## Per-Version Prompting (all models remain selectable)

The three usable model families obey different parts of the prompt. Pick per
goal — or chain them (see Cover Workflow).

| | v4.5 | v5.0 | v5.5 |
|---|---|---|---|
| Obeys best | genre & structure (best adherence, esp. niche) | balance of adherence + quality | nuanced production descriptors |
| Audio quality | weakest (thinner mix) | strong | best, but stem-friendly/unmastered |
| Variance | low | moderate | highest |
| Prompt shape | **lean**: short, genre-first, core instruments, BPM; conversational works but short-and-clear wins; repeat the genre name for stubborn niches | detailed descriptor stack (same as v5.5) | detailed descriptor stack; subtle descriptors actually land |
| Style limit | detailed prompts supported; aim ≤500 chars | 1,000 chars | 1,000 chars |
| Suggested sliders | W 30% · S 80–100% | W 40–50% · S 70% | W 45% · S 70–80% |
| Notes | has Creative Prompt Boosting (magic icon); fewer vocal-hallucination complaints | negative prompting introduced here | personalization layers; sibilance; genre normalization |

Metatags work identically across all three (the system predates v4.5's
"Better Prompts in Lyrics" release). The lyrics file ports across versions;
the **style prompt does not** — derive a lean variant for v4.5 rather than
pasting the v5.5 descriptor stack.

**v4.5 depth lives in `suno-v4-5-prompting.md`** — read it whenever
generating v4.5 prompts: three working prompt styles (lean tags,
conversational-narrative, structured-object), the v4.5+ production tools,
the Enhance button, and era/slider interplay lore. This file stays the
shared truth for metatags, limits, instrumentals, and the cover workflow.

## Cover Workflow (author cheap, render rich)

Community-converged pipeline for prompt-faithful + high-quality output:
**generate on v4.5** (obedient, converges in few rolls) until the take is
right, then **Cover that take on v5.5** to upgrade audio quality while
keeping song, structure, and arrangement.

Cover mechanics:

- Cover takes the source track + a style prompt + the three sliders
  (Audio Influence appears only with audio input).
- Keep the cover style prompt **minimal** — genre, era, production character,
  BPM. The style field is weakly honored during covers anyway; a long prompt
  just adds drift surface. Do NOT restate structure (the audio carries it).
- Lyrics are carried by the source audio; don't re-enter them.

**Audio Influence is the unstable part.** Documented community results
disagree because Suno has changed cover behavior between backend updates:

- systematic v5 test (r/SunoAI): faithful covers BEST at A≈30%, W0, S0 —
  the old v4.5-era "set A to 96–100%" intuition is inverted
- other users: A=10% still produced near-identical clones with the style
  field ignored entirely; weeks earlier the same settings behaved opposite
- niche-genre upgrade flow: A 50–80% (up to 100% "if really stubborn")

**Protocol:** start W 10–20% · S 20–40% · A 50%. One roll, then sweep only
Audio Influence: cover hugs the source too hard → drop toward 30%; cover
drifts away from the song → raise toward 80%. Change nothing else while
sweeping. Expect 2–4 rolls to find the current sweet spot.

Caveat: covering a track to *replace its vocals* (with a Voice/Persona) is
unreliable in v5.5 — one slider controls both voice strength and audio
influence, and the source vocal tends to dominate. Strip the vocal stem
first if vocal replacement is the goal.

## v5.5 Behaviors & Workarounds (community-tested)

- **Genre normalization:** v5.5 pulls niche genres (dungeon synth, raw
  techno, lo-fi, dark ambient, austere folk) toward polished cinematic
  equilibrium. Workarounds: Style Influence 80–100%; or generate in v4.5
  (better genre adherence, worse audio) with a SHORT prompt repeating the
  genre name, then Cover it in v5.5 with minimal prompt + Audio Influence
  50–80%.
- **High output variance:** identical prompts produce very different takes,
  occasionally with dead air or restarts. Budget 3–5 generations per
  version; pick, then Extend/Inpaint rather than rerolling a good take.
- **Sound profile:** ~1.5–2 dB quieter, stem-friendly, more high-frequency
  energy, boosted bass, noticeable vocal sibilance (plan a de-esser in
  post), shouted ad-libs unless excluded.
- **Structure control:** section tags, bar counts, and hard stops are the
  only reliably effective control; qualitative instructions ("sparse,
  restrained arrangement") fail in the lyrics field — put texture in the
  style field or parameterized section tags.
- **Voices (voice clone) in use:** drop gender/timbre vocal descriptors from
  the style field (the Voice carries them); delivery tags still work.
- **Custom Model in use:** lean prompt — tempo, mood, one differentiating
  instrument, one constraint. The model carries the production identity.

## Sources

- suno.com/blog/v5-5 + help.suno.com art. 11362305 (v5.5 announcement, 2026-03-26)
- help.suno.com art. 3161921 (Exclude), 5782977/5782849 (style & lyrics guidance)
- blakecrosley.com/guides/suno — v5.5 reference incl. full metatag taxonomy (2026-06-08)
- hookgenius.app/learn/suno-v5-5-guide (limits, tags, backward compat)
- songaifarm.com/blog/suno-prompts-v5-5 (style structure, voice-clone prompting)
- jgbeatslab.com — "7 Suno v5.5 Behaviors" (loudness, spectrum, negation weakness, variance)
- roo.beehiiv.com Suno prompt guide 2026 (six-layer formula, tag sweet spot)
- r/SunoAI: "Suno v5.5 doesn't understand the concept of instrumental music",
  "Why does v5.5 keep adding in lyrics...", "New v5.5 is insane BUT....",
  "I think I may have figured out how to get SUNO to write niche genres"
  (v4.5→cover workflow, slider settings)
- help.suno.com art. 5782849/5782977/5804417 (v4.5 detailed style
  instructions, lyrics prompts, Creative Prompt Boosting), art. 6141377
  (Creative Sliders official)
- r/SunoAI cover-behavior threads: "Version 5 Suno Covers Test and results"
  (A≈30 sweet spot, systematic sweep), "Suno v5 Cover feature is completely
  broken. Audio Influence at 10%..." (contradicting behavior after backend
  updates), "5.5 Voice Influence over Audio Influence (Cover)" (single-slider
  vocal-replacement problem)
