# Suno Experiment Ideas — Collected Lanes

*Compiled 2026-06-11 · Claude (Fable 5) · sources: Codie + Pyro's
`~/music/suno/suno_experiment_mode.md` + a hivemind knowledge-mine sweep
(r/SunoAI all-time + X, receipts inline)*

> Status: idea pool, deliberately untriaged (per Pyro: keep everything
> except the absolute worst; triage happens later). Reliability labels
> are evidence notes, not verdicts. Feeds the suno-pack `--mode
> experimental` build.
>
> Epistemic note: everything here is community folklore — `[claimed]`
> unless marked. The community's own fact-check culture found a third of
> its top guide "wrong, outdated, or unverifiable." Every lane is a
> hypothesis to sweep and log, not a recipe.

---

## Part 1 — Codie's lanes (from suno_experiment_mode.md)

Kept verbatim in spirit; full schema (invariant / mutation axis /
expected failure / keeper signal) lives in the source doc.

1. **Genre Transposition Cover Lab** — seed in v4.5, cover into
   incompatible genres (gospel soul lament, shoegaze drill, cybergrind
   lullaby…), sweep Audio Influence 30/50/70/85, one axis per mini-run.
2. **Gravity Inversion** — name the genre's gravity wells (pop, EDM
   drops, trap hats) in Exclude, reinforce rare pairings positively, use
   concrete instrumentation over genre slogans.
3. **Section Tag Mutation** — keep style prompt stable, mutate one song
   section hard via stacked lyrics tags (`[Bridge: sudden half-time
   industrial break…]`).
4. **Seed Audio Abuse** — non-song audio as seed: mouth beats, room
   tone, field recordings, hummed motifs; cover/remix carries gesture
   text can't specify.
5. **Inspo Mash Lab** — 2–4 references with assigned roles (skeleton /
   rhythm mutation / timbre / persona); keeper = sounds like none of
   them, concept survives.
6. **Voice/Persona Split** — persona + cover fighting over Audio
   Influence as a lane, not a bug: lead seed → re-voice → harmony pass →
   DAW stack.
7. **Stem/DAW Loop** — export stems from interesting failures, keep one
   surprising stem, rebuild around it, feed the edit back in. Suno as
   mutation engine, not final-output machine.

Plus Codie's framework that all lanes inherit: **concept invariant +
mutation axis + expected failure + keeper signal**, experiment map before
prompts, scorecard (concept survival ≥3, surprise ≥4, artifact cost ≤3).

---

## Part 2 — New lanes from the hivemind sweep

### Render & re-render tricks

8. **Alternate-Reality Renders (Live Performance hack)** — cover your own
   track, style append "Live Performance, Concert" (or "MTV Unplugged
   and the crowd sings along to the chorus"), weirdness 0, Audio
   Influence 100 → convincing live/unplugged versions of the same song.
   Community variants: stripped acoustic, crowd-singalong. The same
   mechanism generalizes: "rehearsal room demo", "bootleg tape",
   "street performance". `[r/SunoAI, 308↑ + corroborating comments]`
   Reliability: high (multiple independent confirmations in-thread).
9. **Producer's Ear (reconstruction diagnostic)** — cover your own
   upload with weirdness 0, style influence 0, Audio Influence 100,
   matched lyrics, style box empty (mobile forces non-empty — known
   gap) → Suno outputs how it *heard* your track. Use as an analysis
   pass before mutation lanes: the delta between your track and the
   reconstruction reveals what the model considers load-bearing.
   Theory: EnCodec-style reconstruction training. `[r/SunoAI, 93↑]`
   Reliability: medium; diagnostic value even when imperfect.
10. **Niche-Genre Two-Step** — v4.5 nails obscure genres (Hardgroove,
    raw hypnotic techno) with SHORT prompts; v5+ defaults them to
    trance/pop. Pipeline: v4.5 short-prompt arrangement → v5 cover with
    the shortest possible prompt for audio quality. Bonus folklore:
    **genre-name repetition spam** ("Hardgroove" ×50 beats ×1).
    Counter-slider pattern from comments: generate at W60-75/S80/A30,
    then persona-cover at W20/S20/A80. `[r/SunoAI, 8↑ but
    detail-dense + corroborated by 4 comments]` Reliability: medium.
11. **Remix (official)** — Suno shipped "Remix" (flip any track via …
    menu). New first-party control surface for the cover-abuse family;
    semantics unswept. `[@suno official, 311 likes]` `[observed —
    feature exists; behavior unswept]`

### Lexicon & language

12. **Untranslatable-Emotion Lexicon** — 200 obscure emotion words
    tested, 47 with distinct sonic signatures: saudade (minor 7ths),
    hiraeth (reverb, slow attack), mono no aware (Japanese scales +
    synths), lacrimoso (vocal vibrato rate). "Saudade electrónica"
    behaves like a coherent subgenre. Framework: **the rare word does
    the heavy lifting, descriptors set the stage** ("Hiraeth, 3AM,
    bedroom production, tape hiss, vocals from another room").
    `[r/SunoAI, 234↑; full 200-word list in thread; independently
    corroborated by a commenter in the Controlled Friction thread]`
    Reliability: medium-high for tier-1 words; tier-3 words route to
    nearest synonym.
13. **Performance-Directive Lexicon** — classical/production vocabulary
    as tags: Rubato (tempo elasticity, lets lyrics breathe), syncopated
    (de-couples melody from percussion timing, jazzy), staccato/legato,
    dynamics terms. Independently practiced in the Japanese community
    (転調/modulation, スタッカート, タイ・スラー via Gemini-composed style
    prompts). `[r/SunoAI, 65↑ + @happiness5055 (JP)]` Reliability:
    medium; cross-language echo is a good sign.
14. **Parlance Switch (lyric-LLM meta)** — when the LLM writes lyrics:
    "write it in common parlance" kills Hallmark-rhyme voice; variant
    "written in the vernacular of [era/scene] slang". Belongs in the
    pack's lyric-generation prompts, not the Suno fields. `[r/SunoAI,
    103↑]` Reliability: high for its actual target (the lyric LLM).
15. **Pro-Terminology Prompting** — build style prompts from
    producer/engineer vocabulary (mic types, room character, mix
    language) instead of genre adjectives. Overlaps gravity inversion's
    "concrete instrumentation" rule; the lexicon angle is the lane.
    `[r/SunoAI, 53↑, not deep-read]` Reliability: unswept.

### Prompt architecture

16. **Controlled Friction** — deliberate emotional contradiction inside
    the prompt ("beautiful romance + hidden anxiety", "nostalgic warmth
    + mechanical rhythm tension") produces stronger, more human melodies
    than clean moods. Best comment: "you're weaponizing the model's own
    anxiety in resolving contradictory directives." Cross-corroborated
    by the persona-lab user who stuffs conflicting genres ("dark drill
    rap + happy Mary Poppins vibes + Chopin guitar solo").
    `[r/SunoAI, 72↑ + 51↑ thread]` Reliability: medium; pairs naturally
    with Codie's gravity inversion as its emotional twin.
17. **Notation Injection** — per-line chord annotations in lyrics
    (`(Em) We walk on shattered earth, (G) beneath a blood-red sky`) or
    single-note tags (`[G] Beat`). Mood of the progression sometimes
    carries. Honest counterpoint in-thread: "if it only works
    sometimes, you're getting slot-machine results and crediting the
    notation." One user reports notation holding across generations.
    `[r/SunoAI, 24↑ + prior thread 96↑]` Reliability: LOW, contested —
    classic sweep-and-log candidate.
18. **Lyric-Field Prompt Injection (SSPs)** — full prose production
    briefs pasted into the LYRICS field (v3.5-era "Super Suno Prompts",
    98% claimed success on v3.5; newer models repeat them as sung
    text). Legacy lane: worth one sweep per current model to see if any
    field-misuse behavior survives. Side-folklore from the same thread:
    **no numbers in section tags** ([Verse] beats [Verse 1]).
    `[r/SunoAI, 127↑ + 296↑ original]` Reliability: low on current
    models, historical interest + cheap to test.

### Slider science

19. **Slider Coupling for Obedience** — weirdness AND style influence
    both ~80 → markedly better lyric-tag compliance (discovered while
    casting multiple characters in a Hamilton-style song; characters
    sing their correct lines). Also implies a **casting lane**:
    multi-character songs as a stress test of tag obedience.
    `[r/SunoAI, 102↑]` Reliability: medium.
20. **Red-Letter Mining (weirdness 100)** — at 100 weirdness most output
    glitches (15-second tracks, AM-radio noise) but the survivors are
    "exceptionally crazy good"; workflow: mine a crazy instrumental at
    100, then tame it via cover with lyrics at lower settings. Sweet
    spots from the same thread: v5 60w/80-85s; chaos threshold ~76 on
    v4.5+, ~80 on v5. `[r/SunoAI, 123↑]` Reliability: medium-high as a
    search strategy (it IS a search strategy).

### Persona & vocal

21. **Instrumental-Persona Vocal Invention** — crop the best instrumental
    section, create a Persona from it, generate with "." as the entire
    lyric and instrumental toggle OFF → Suno invents vocals, often a
    convincing **gibberish language** ("what English sounds like to
    non-speakers"). Rare but striking when it lands. `[r/SunoAI, 51↑]`
    Reliability: low-frequency / high-ceiling, the thread says so
    itself.
22. **Persona Laddering** — recursive chains: persona → generate → crop
    best bit → new persona → generate → … Each rung drifts while keeping
    a sonic genome; commenter chained 6+ rungs through covers, extends,
    remasters. Also: **album-glue personas** — one
    instrumental-derived persona across an EP for coherent identity.
    `[r/SunoAI, comment chain under 51↑ post]` Reliability: anecdotal,
    structurally interesting (it's lineage-tree farming — pp-cli's
    `tree` command visualizes exactly this).

### Post-production

23. **Stem Remaster Stacking** — remaster preserves exact timing, so a
    remastered stem is a perfectly aligned *alternate take*: remaster
    individual stems, layer original + remaster in the DAW (vocals get
    notably richer). Doubles as free vocal doubling. `[r/SunoAI, 65↑ +
    practitioner comments]` Reliability: medium-high; credit-hungry.
24. **Force-BPM-then-Cover** — Suno ignores BPM tags (DAW-verified by a
    commenter); workaround: force tempo in the editor, then cover the
    edited track to re-naturalize it. `[r/SunoAI, comments under the
    satire thread, 6–9↑]` Reliability: medium; the negative knowledge
    (BPM tags don't hold) is the most verified part.
25. **Sample-Layering Prompt Pattern** — when uploading source audio:
    "Layer the original sample over tight, punchy drums and deep bass,
    maintaining all nuances of the source material… no alterations to
    the source" — prompting *around* a sample rather than asking for
    transformation. `[r/SunoAI, comment under Producer's Ear]`
    Reliability: unswept.

### Artifact farming

26. **Haunted Tails** — generations occasionally continue past the song:
    room sounds, sobbing, spoken fragments ("please help me!" got nuked
    by Suno support). The trailing space past the structural end is an
    unprompted-content zone. Lane: deliberately farm it (short
    structures + long max length) for uncanny textures and samples.
    `[r/SunoAI, 235↑ thread of artifact reports]` Reliability: it
    happens; *steering* it is unproven. Dark-ambient gold if it works.
27. **Error Injection** — deliberate prompt chaos to get genuinely
    unplanned imperfection where "lo-fi, tape hiss, demo quality" is
    too clean/designed. Self-rated ★☆☆☆☆ by its author — try standard
    descriptors first. Part of a **42-trick "dirty tricks" series**
    (Day #1–34, r/SunoAI) — the series itself is unmined; see next
    directions. `[r/SunoAI, 30↑, series]` Reliability: low by design.

### Folklore to test (kept, flagged)

28. **Peak-hours quality theory** — "not using the thing during peak
    hours eliminates 95% of the issues" (72↑ comment); matches the
    time-of-day quality claim from the S2 sweep (125↑ thread, 10/11 →
    3/11 scores at US peak). Community placebo culture is documented,
    but two independent claims earn it a logged sweep: same prompt,
    fixed seed-adjacent settings, off-peak vs peak, blind-rated.

---

## Dropped (the absolute worst, per triage mandate)

- **`[QUALITY_ULTRA]` / `[MAX_MODE]` pseudo-tags** — API-level debunk
  (output hard-capped 48kHz/~192kbps; no such backend params); even the
  debunker concedes only tokenization side-effects. Superstition.
- **The satire thread's "techniques"** (1tdj9pq) — comedy, kept only for
  its comment nuggets (#24, #28).
- **X money-scheme content** — "make $7,500/month on Spotify" bait
  (2.5k likes); zero craft content.

## Coverage & receipts

Hivemind knowledge-mine, window=all, both platforms. Venues:
r/SunoAI (29/50 recon dominance), r/GeneratedGrooves (sanity pass —
community events, no techniques). X confirmed thin for Suno craft
(money-bait + two real finds: official Remix launch, JP
notation-prompting). 15 threads deep-read with comments; triage
rejections named above and in the run log; max 3 items/author respected.
The `rdt read` raw-listing shape quirk handled per playbook.

## Next directions

1. **Mine the full "dirty tricks" series** — 42 tricks across 34 daily
   posts by one author; only the finale was read. `rdt user-posts` on
   the author + read the set; likely several lanes hiding there.
2. **Sweep Remix** — the new official feature is uncharacterized; run a
   structured slider/prompt sweep on one seed and log behavior (first
   candidate for the experiment-mode + CLI combo).
3. **Verify the emotion-lexicon tier-1 words** — the 234↑ thread links
   audio samples; A/B five tier-1 words vs their plain-English synonyms
   on a fixed seed before baking the lexicon into the pack.
4. **Watch two authors** — the dirty-tricks series author and the
   master-prompting-doc maintainer (u/Adventurous_Mix_1792, already
   flagged in the S2 sweep) — the two most systematic experimenters
   found.
