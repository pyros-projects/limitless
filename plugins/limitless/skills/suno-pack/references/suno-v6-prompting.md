# Suno v6 Prompting Reference

Research compiled 2026-10-03 from Suno's v6 blog and FAQ, the app's own label
files (`suno.com/locales/en/create.json`, `voices.json`, `lyrics.json`), the
help center, launch-week testers (HookGenius, AI Musicpreneur, JG BeatsLab, a
measured X article by @tshikimi), the bitwize-music-studio v6 reference, and
r/SunoAI and X practitioner threads. Hivemind frame:
`~/.limitless/hivemind/suno-v6/2026-10-03/brief.md`. Re-verify against
suno.com/blog and help.suno.com when this is more than ~2 months old — several
help articles (sliders, Exclude, Covers) had not been updated for v6 yet.

## Model State (October 2026)

Suno retired **every model before v6 on 2026-09-09** (v4.5, v4.5+, v5,
v5.5, v4.5-all). Nothing new renders on them. Old songs stay playable, and
Extend, Cover, and Remaster of them run on v6. Prompts written for older
models do not transfer: re-prompt, don't rerun.

| Model | Internal key | Plans | Variety default | Use it for |
|---|---|---|---|---|
| **v6** | `chirp-hawk` | Pro, Premier | Normal → set **Off** | every finished track; follows the brief closely |
| **v6-wild** | `chirp-hawk-wild` (unconfirmed) | Pro, Premier | **Off** | exploring a sound, genres where v6 plays it safe (rock, metal, soul); finish the keeper on v6 via Cover |
| **v6-mini** | `chirp-goose` | all, incl. Free | Normal | sketches, high-volume ideas; the only Free-tier model (Free downloads are non-commercial) |
| Custom Model | — | Pro, Premier | Normal → set Off | catalog-wide voice/aesthetic consistency; auto-upgraded to v6 |

Internal keys are for reading API payloads and run logs only; never write
`V6`/`V6_WILD` identifiers into prompts.

## Field Limits

| Field | Limit | Notes |
|---|---|---|
| Style of Music | 1,000 chars | sweet spot ~400–800; truncates from the END — front-load |
| Lyrics | 5,000 chars | 30–40 lines for a 3–4 min song |
| Exclude Styles | 1,000 chars | shown back as `-term` |
| Title | ~80–100 chars | no musical effect |
| Simple-mode description | 3,000 chars | prose brief; up to 5 images + 1 video as inputs |
| Duration | 10 s – 6 min (slider) | max generation 8 min via Extend |

The Create tabs are now **Simple / Advanced / Sounds** — "Custom" mode is
called **Advanced**. Everything below is Advanced mode.

## Controls (More Options)

| Control | What it does | Skill default |
|---|---|---|
| **Variety** (Off / Normal / High / Extra / Max) | Rewrites your style prompt server-side before generating, differently per take. Off = "Exact style". Suno: "reduce the Variety slider to 0" to keep control of your tags | **Off** — the skill writes deliberate style prompts. Raise only in experiments or for vibe-only prompts |
| **Personalize** | "Make Variety match your taste" — only acts when Variety is above Off | **Off** |
| **Weirdness** (0–100) | How experimental the choices are | 30 (20–40 for songs that must land; 50+ only to explore; >60 breaks easily on wild) |
| **Style Influence** (0–100) | How hard Suno commits to the prompt it has | 70–85. Measured: 50 and 100 sounded alike and 90 came out darker — the effect is not monotonic, so change it last |
| **Audio Influence** (0–100) | Only with source audio (Cover, upload, Voice, Inspiration) | see Covers |
| **Max Mode** | More compute for consistency through the song; **2× credits** | Off for drafts; **On for the final take** of anything over ~2:00, faithful covers, Voices |
| **Duration** | Auto or a fixed length | **Fixed**, matched to the structure (typically 2:45–3:45). Auto runs longer, slower, and sparser than the prompt implies |
| **Vocal Gender** | male / female | set only when the concept needs it; leave unset with a Voice |
| **Lyrics Mode** | Write / Prompt / **Instrumental** / Mumble | Write for vocal songs; Instrumental for instrumentals (see kit) |

Set Variety first: Style Influence governs commitment to the prompt; Variety
changes which prompt there is. Typing slider values into the style field does
nothing.

## Style Field

v6 "understands the language musicians actually use" (Suno). Comma list and
short sentences perform about the same (measured: 17/19 metrics within
noise); what matters is **content and order**. Truncation hits the end, so
order by priority:

```
[genre/subgenre], [mood + scene, 2–3 words], [lead voice: character + placement],
[players: adjective+instrument with a role verb], [arrangement arc: one sentence],
[production clause], [BPM number, optional key/meter], [ending]
```

- **Genre names carry context** — removing them broke the track in testing.
  Name the genre first; repeat it once for a stubborn niche.
- **Era words pull production defaults** ("80s glam metal" brings a gated
  snare). Use an era only when you want its whole sound.
- **Give players roles, verbs beat adjectives:** "slide guitar answering the
  vocal", "upright bass walking under the verses", not a bare instrument list.
- **Lead vocal character AND placement:** "warm, slightly husky female lead,
  close-mic, upfront in the mix". "Lead vocal in front of the instrumental
  mix" fixes buried vocals.
- **One arrangement arc:** "restrained verses build into full choruses; the
  bridge strips to voice and guitar". v6 follows one arrangement instruction
  more reliably than v5.5 did; more than one competes.
- **Production clause:** "close-mic, crisp transients, warm tape saturation,
  stable loudness". This is the main lever against the muddy/over-loud v6
  mix.
- **BPM as a number** ("84 BPM") — usually close (96 requested, 96.8
  measured), sometimes far off; verify in the audio.
- **The style field controls WHAT sounds, not WHEN.** Timbre, texture,
  stereo placement, and tempo land; timestamps ("silence at 0:45"),
  per-section tempo, `[half-time]`, and `[double time]` are ignored. Put
  timing and section changes in the lyrics' section order and tags.
- **Negations go to Exclude, never the style field** — the model keeps the
  noun and drops the "no". Describe what you want instead ("solo acoustic
  guitar and upright bass only").
- **Artist names are blocked** by the app ("enter genres or vibes instead").
  Translate references into traits.
- **Don't** use pipe-`|` templates in the style field (read as song structure)
  or stack contradictory genre lists (they average into mush).

Examples that tested well:

```
indie folk, acoustic singer-songwriter, chamber folk, fingerpicked steel-string guitar,
upright bass, brushed snare, close-mic intimate male vocal, room tone, sparse arrangement,
78 BPM, instrumental break before final chorus
```

```
Dark post-punk synth-pop, 118 BPM, minor key, nocturnal and sophisticated, steady
four-on-the-floor groove, crisp drum-machine percussion, prominent melodic octave bass
forward in the mix, chorus-soaked guitar, icy analog synths, deep dry theatrical male
baritone, detached verses, controlled melodic choruses, bridge strips to bass and
atmosphere before a powerful final chorus, analog warmth, tape saturation, restrained reverb
```

## Exclude Styles

The official negative surface; comma-separated; up to 1,000 chars. Use it
for every "no". Known limit: **Exclude fails when the genre itself wants the
element** ("-pedal steel" on modern country failed 2/2; "no guitar" on
synthwave held 4/4). Then change the genre word or describe the wanted
instrumentation positively, and put structural instructions in section tags.

Useful defaults by concern:
- muddy mix: `muffled vocals, reverb wash, muddy, boomy, harsh highs`
- instrumentals: `vocals, singing, choir, spoken word, ad-libs, humming, wordless vocals, oh oh oh`

## Lyrics Field Metatags

v6 follows **tagged instructions inside the lyrics far more reliably** than
older models — section tags are the strongest arrangement control.

- Structure tags as before: `[Intro]` `[Verse 1]` `[Pre-Chorus]` `[Chorus]`
  `[Post-Chorus]` `[Bridge]` `[Breakdown]` `[Build]` `[Drop]` `[Hook]`
  `[Interlude]` `[Outro]` `[End]`. Number verses; repeat identical chorus
  text.
- **Per-section direction inside the bracket:**
  `[Verse 1: soft, breathy, low dynamic, intimate]`,
  `[Chorus | full band, stacked harmonies]`,
  `[Bridge | female, whispered, pitch drifting on the hold]`.
- **Give gaps a length and a job:** `[Instrumental Interlude: 8 bars, soaring
  violin solo]`; `[Pause: 3 seconds of absolute silence]` (a bare `[Pause]`
  is ~1 s). An unassigned gap invites "oh-oh" fills.
- Invented tags (`[2 Bar Rest]`, `[Theme A]`) are dropped or sung. Bare text
  outside brackets is sung ("piano stabs in" gets sung).
- `( )` = sung backing vocals and call-and-response, still. CAPS gives a
  harder delivery.
- **Ending:** `[Final Chorus]` → `[Outro: …]` → `[End]`, and keep "extended",
  "jam", "long outro" out of the style field — v6 likes to run 6–7 minutes
  and loop.
- Reported fix for rushed vocals: an inline `[Silence]` at the end of lines
  (single source; try it on the second take, not by default). A trailing
  comma at line end can cause stutter.

## Instrumental Kit

The dedicated toggle became **Lyrics Mode → Instrumental** ("no vocals or
lyrics"). Vocals still leak on some genres (EDM, D&B reported). Layer:

1. **Surface:**
   - Web UI, simplest: Lyrics Mode **Instrumental** — style + Exclude carry
     everything.
   - Web UI, arrangement control: Lyrics Mode **Write** with the
     structure-tags-only Lyrics block (each gap with a job). Higher leak risk;
     re-roll on leaks.
   - CLI (when the execution layer supports v6): the instrumental flag plus
     the structure-tags Lyrics block.
   - A song with a **Voice cannot be instrumental** — remove the Voice.
2. Lyrics block: structure tags only, starting with `[Instrumental]`, every
   section naming the instrument that carries it, ending with `[End]`.
3. Style field: zero vocal-adjacent words (vocal, voice, choir, humming,
   singing, "vocal-like"). The melody carrier is an instrument: "expressive
   lead synth carrying the main melody".
4. Exclude: `vocals, singing, choir, spoken word, ad-libs, humming, wordless vocals, oh oh oh`.
5. Still leaking: re-roll (two takes per generation differ a lot), or
   Replace Section on the leaking part.

## Known v6 Behaviors & Workarounds

- **Long-song decay** (top complaint): loudness creeps up and the mix
  muddies after ~2–3 min (measured RMS −20 → −9 dB on one track). Defenses:
  fixed Duration ≤ ~3:45, production clause in style, Max Mode on the final
  take. Repair: Extend from just before the decay point, or Replace Section.
- **Take variance:** the two takes of one generation can differ more than a
  deliberate prompt edit. Judge pairs; A/B prompt edits only with Variety Off.
- **Genre normalization:** rock, metal, grunge, alt-country, and some
  synth-pop drift to a generic voice/mix. Workarounds: "raw, unpolished,
  live studio performance" in style; start on **v6-wild**, then Cover the
  keeper on v6; or a Custom Model.
- **Muddy/buried vocals:** production clause + "lead vocal in front of the
  mix" + Exclude `muffled vocals, reverb wash, muddy`.
- **Sibilance and harsh highs** after Max Mode/Remaster: plan a de-esser.
- **Melody hooks:** describe the melodic shape ("wide interval jumps, a
  distinct rising phrase into the chorus").

## Covers, Remaster, Voices

- **Remaster** (Subtle / Normal / High): small changes, same song — e.g. an
  old v4.5/v5.5 take re-rendered on v6. Can come out more compressed.
- **Cover:** v6 reinterpretation that follows the source melody and
  structure ("cover accuracy is hyper"). Keep **Variety Off** (Variety makes
  cover melodies drift) and the cover style prompt **minimal** (genre, era,
  production, BPM — the audio carries lyrics and structure). Max Mode for
  faithful covers. Audio Influence: high (70–85) stays close, ~25 via
  **Inspiration** gives real variation; Suno has published no v6-specific
  Audio Influence guidance — calibrate with one roll, then sweep only Audio
  Influence.
- **Wild → v6 finish:** generate on v6-wild, pick the take with the
  character, Cover it on v6 (reported starting point: Weirdness 10–28, Style
  Influence 45–50, Audio Influence 70–80, Variety Off, Personalize Off).
  Experimental — no published settings reliably preserve wild's character.
- **Covering a cover degrades** the sound; download, re-upload, then cover.
- **Voices** (formerly Personas): legacy "Style Voices" still work; "Upgrade
  Voice to v6" improves consistency. With a Voice, drop gender/timbre words
  from the style field, keep Audio Influence fairly high, use Max Mode.
  v6-wild reportedly ignores Voices.
- **Custom Models:** auto-upgraded to v6; prompt lean (tempo, mood, one
  differentiating instrument, one constraint) and keep section direction.

## Costs

| Action | Credits |
|---|---|
| Generation (2 songs), v6 / v6-wild / v6-mini | 10 |
| same with Max Mode | 20 |
| Stems: Auto Split / Split from Mix | 50 / 10 per stem |
| Custom Model | 100 |

Download caps since 2026-09-03: Free 7 lifetime, Pro 20/month, Premier
60/month (Studio downloads on Premier uncapped). Mention the cap when a pack
plans many downloads.

## Sources

- suno.com/blog/introducing-v6 (2026-09-09); help.suno.com 13924481 (v6 FAQ:
  retirement, Variety, Max Mode, costs), 13924801, 13924737, 13924993,
  8105281 (Remaster), 13925185 (stems), 10625537 (Simple/Advanced/Sounds)
- suno.com/locales/en/create.json, voices.json, lyrics.json (app labels:
  Variety stops, Personalize, Duration 10 s–6 min, Lyrics Mode, Max Mode 2×,
  artist-name block, Voices cannot be instrumental) — fetched 2026-10-03
- hookgenius.app/learn/suno-v6-guide (2026-09-09); aimusicpreneur.com v6 vs
  v5.5 (27 generations); jgbeatslab.com edit ladder (09-15) and genre prior
  (09-17); @tshikimi measured X article (09-17)
- github.com/bitwize-music-studio/claude-ai-music-skills reference/suno
  (models.md, creative-sliders.md — Variety defaults per model)
- r/SunoAI threads 1wdysw9, 1wjmlpj, 1wjkilz, 1wknz4l, 1wcyryw, 1wv7eqv,
  1wo8fwt, 1wcuj5m, 1wm80fd, 1wwipa5; X @suno launch thread, @alexutopia,
  @KazeKasukana, @AIs_of_Dragoon
