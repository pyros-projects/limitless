# The Light Keeps Itself — Cover Pipeline v4.5 → v5.5

Author on v4.5 (prompt obedience), render on v5.5 (audio quality).

## Pipeline
1. Generate on v4.5 using lyrics_v4.5.md / no_lyrics_v4.5.md
   until a take nails song, structure, and feel (budget 3 takes).
2. Open the winning take → Cover → switch model to v5.5.
3. Paste the minimal style prompt below. Do NOT re-enter lyrics — the
   audio carries them.
4. Sweep Audio Influence per the protocol below.

## Settings
| Setting | Value |
|---|---|
| Model | v5.5 (Cover) |
| Weirdness | 10–20% |
| Style Influence | 20–40% |
| Audio Influence | start 50% — sweep, see below |

## Cover Style Prompt (minimal — genre, era, production, BPM only)
```text
melancholic maritime folk ballad, 1970s analog era, sparse warm tape-saturated production, intimate and unhurried, 68 BPM
```

## Audio Influence Sweep
Cover behavior shifts between Suno backend updates — treat the slider as
a dial to calibrate, not a constant. One roll at 50%, then:
- output hugs the source too hard (near-clone) → drop toward 30%
- output drifts away from the song → raise toward 80%
Change nothing else while sweeping. Expect 2–4 rolls.
