# Suno v4.5 / v4.5+ Prompting Reference

Research compiled 2026-06-10 from official Suno help docs (model timeline,
v4.5 feature articles), music-industry press coverage of the v4.5+ launch,
and r/SunoAI community technique guides. Companion to
`suno-v5-5-prompting.md`, which owns the shared truth (metatag taxonomy,
field limits, instrumental kit, cover workflow) — this file is the
v4.5-specific delta and lore.

## Identity & Timeline

- **v4.5** — released 2025-05-01: 8-minute first generations, improved
  prompt adherence, "smarter style mashups", stronger vocals, reduced
  shimmer vs v4.
- **v4.5+** — released 2025-07: same core model plus production tools —
  **Add Vocals** (turn an instrumental into a full song, swap words or whole
  lyric sets), **Add Instrumentals** (build music under recorded vocals),
  **Inspire** (generate from playlist vibes). A v4.5-class model also serves
  the free tier ("v4.5-all").
- Both remain selectable in 2026. When this document says "v4.5", v4.5+ is
  included unless noted.

## Why v4.5 in 2026

The community keeps choosing v4.5 deliberately, not nostalgically:

| Strength | Detail |
|---|---|
| Genre adherence | best in the lineup, especially niche genres v5+ normalizes (raw techno stays raw techno) |
| Genre fusion | the v4.5 superpower — "midwest emo + neosoul", "EDM + folk" blend seamlessly (official claim, community-confirmed) |
| Structure-in-style obedience | narrative structure direction in the STYLE field actually works ("Begin with… build gradually…") — this fails on v5.5 |
| Low variance | fewer rolls to converge; the prompt laboratory |
| Vocal character | 3.5–4.5-era vocals are still rated "startlingly human" by parts of the community; v5 remix vocals get called lifeless by comparison |
| Instrumentals | far fewer vocal-hallucination complaints than v5.5 |

Weaknesses: thinner, less polished mix; weaker low end; production quality a
clear tier below v5+. That's what the cover pipeline is for (author here,
render on v5.5 — see the cover workflow in the main reference).

**Portability warning (both directions):** v4.5 prompts pasted into v5+
produce degraded or weird results, and v5-style detailed descriptor stacks
degrade adherence on v4.5. Every version gets its own style prompt.

## Three Working Prompt Styles

### 1. Lean tags (default)

Genre-first, short and clear, ≤500 chars:

```
raw techno, hypnotic raw techno, dusty analog kick, rolling modular
bassline, dark warehouse mood, 132 BPM
```

- 2–4 signature instruments; Suno fills in the rest.
- **Repeat the genre name** for stubborn niches — measurably improves
  adherence (community-tested; one producer reports listing the genre many
  times beats listing it once).
- Specific subgenre labels beat broad ones: "acoustic reggae-folk with
  gospel choir", not "pop".

### 2. Conversational / narrative (official v4.5 feature)

v4.5 was the release that made prose prompts work. Structural direction
inside the style field is honored:

```
Create a melodic, emotional deep house song with organic textures and
hypnotic rhythms. Begin with soft ambient layers, natural sounds, and a
deep, steady groove. Build gradually with flowing melodic synths, warm
basslines, and intricate, subtle percussion.
```

Use when the concept's structure sketch matters more than its tag list.
Template: `Create a [genre+subgenre] track with [core instruments]. The
mood should be [emotion]. Start with [intro idea], build to [chorus idea].
Vocal style should feel [tone]. Keep the structure [dynamic/minimal].`

### 3. Structured-object style (community: "Disckordia" technique, v4.5+)

Pseudo-code key-value blocks pasted straight into the style field:

```
const nightdriveSound analogProducer = {
era: "1980s",
genre: "synthwave, retrowave, dreamwave",
style: "melodic nightdrive grooves, hypnotic arpeggios, cinematic restraint",
vocals: "male, breathy low tenor, intimate close-mic delivery",
mood: "melancholic, nocturnal, nostalgic, spacious",
instrumentation: "warm analog pads, pulsing Moog bass, gated reverb drums, glassy guitar accents",
mastering: "masterpiece, warm analog depth, wide stereo panorama, 24 bit resolution, 192 khz sample rate"
};
```

Mechanics worth knowing:

- The **identifier names carry signal** — the original guide smuggles artist
  and producer flavor through them (`const beatlesSound georgemartinProducer`).
  Useful for era/scene flavor without naming artists in descriptor text.
- The `mastering:` line ("masterpiece, … 24 bit resolution, 192 khz sample
  rate, <era> production style") is the technique's signature quality nudge.
- Designed for plug-and-play: **reset Advanced Options before pasting**
  (the guide's author warns expanded advanced settings interfere).
- Field order: era / genre / style / vocals / mood / instrumentation /
  mastering — a ready-made mapping from the concept document's sections.

ALL-CAPS field lines are a related community dialect that also shows up in
v4.x prompting (`VOCAL: CLEAN, MASTERED`, `PRODUCTION: Studio, Radio Ready`).

## Enhance Button (Creative Prompt Boosting)

v4.5's magic icon (top right of the style box): drop in rough tags, get a
fully-formed style prompt back. Two uses: a quick baseline, and a
**vocabulary mine** — generate the enhanced prompt, harvest its descriptor
phrasing into your own prompt, discard the rest. (v5.5's equivalent is the
My Taste wand; different feature, same harvesting trick.)

## Lyrics Field

Identical metatag system to v5.x (see main reference for the full taxonomy —
it predates v4.5's "Better Prompts in Lyrics" release). v4.5-specific craft
notes:

- 6–12 syllables per line paces naturally at most tempos.
- Context lines in the lyrics box ("add more context for your songs directly
  in the Lyrics box") are officially sanctioned in v4.5.
- Covers + Personas can be combined in one operation (remix voice,
  structure, and style at once) since v4.5.

## Settings

| Slider | v4.5 guidance |
|---|---|
| Weirdness | 30% baseline; some niches want 18–39%, a few need 60%+ for variety |
| Style Influence | 80–100% (80% typical) |
| Audio Influence | n/a unless covering — see main reference cover workflow |

Community data point on slider interplay: with artist-style prompts, slider
position shifts *which era* of the style you get (one Portishead-style test:
S100/W50 lands the polished early era; S≤80/W65+ lands the rawer one).
Treat sliders as an era/fidelity dial, not just adherence.

## Instrumentals on v4.5

Same layered kit as the main reference (toggle + `[Instrumental]` +
vocal-free style + Exclude), but expect far fewer violations — the
vocal-hallucination epidemic is a v5.5 behavior. v4.5 is the safer model
for wordless choir/vocal-drone textures that v5.5 turns into lyrics.

## Limits

Same fields as v5.x: style 1,000 chars (lean prompts ≤500 recommended
regardless), lyrics ~5,000, 8-minute generations, title 80.

## Sources

- help.suno.com art. 5782721 (model timeline), 5782593 (What's new in V4.5),
  5782849 (Detailed Style Instructions), 5782977 (Better Prompts in Lyrics),
  5804417 (Creative Prompt Boosting)
- digitalmusicnews.com / musicbusinessworldwide.com / techradar.com v4.5+
  launch coverage (2025-07; Add Vocals, Add Instrumentals, Inspire, v4.5-all)
- jackrighteous.com "Plan & Prompt Your First Theme Song with Suno V4.5 Plus"
  (planning framework, conversational template, 6–12 syllable pacing)
- r/SunoAI: "Disckordia's Artist Prompt Guide for v4.5+" (structured-object
  technique + era/slider interplay in comments), "I think I may have figured
  out how to get SUNO to write niche genres" (genre repetition, v4.5→v5
  cover flow), "[V5] Suno V5 is better, but it's hit or miss" (prompt
  portability, vocal-character sentiment)
