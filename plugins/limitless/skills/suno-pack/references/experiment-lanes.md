# Experiment Mode — Lanes, API, Mechanics

Experimental mode turns a pack into a small, trackable music experiment.
Five default lanes (chosen 2026-06-11 from a 27-lane community-evidence
pool). All execution mechanics from `pp-cli.md` apply — gates,
confirmation rule, run logs, take-aware downloads.

## Invocation API — one lane at a time

Experimental mode never batches lanes. **One invocation = one lane = one
roll.** The invocation is the consent to discuss; cost (~10 credits) is
stated in the confirmation line before anything fires.

| Invocation | Behavior |
|---|---|
| `--mode experimental` / "surprise me with an experiment" | one RANDOM lane — dice roll over all five, always |
| `--mode experimental 3` / "give me experiment 3" | that specific lane |
| `--mode experimental list` / "list all experiments" | the menu: number, name, mutation axis, one-liner, cost, requirements |
| "tame it" (after a Lane 4 keeper) | Lane 4 step 2 on the chosen survivor |
| "lane 1 again, baroque boom bap" / "re-roll friction, poles swapped" | repeat invocations — depth is just asking again |

**No fail state — it's experimentation.** A lane with an unmet
requirement is never excluded, errored, swapped silently, or silently
re-rolled. The requirement gets resolved in conversation and the
experiment proceeds.

### Per-invocation mechanics

1. **Requirement resolution.** Lanes 1 and 3 need a seed clip. None
   chosen → ask, offering ALL of: (a) generate the faithful pack now
   (state cost, ~10 credits / 2 takes), (b) pick an existing track —
   propose candidates from observables per the seed-selection rules in
   `pp-cli.md` (scorecard ratings outrank play counts; never claim to
   have listened), (c) the user provides a clip id directly, (d) swap to
   another lane. Same resolve-never-refuse pattern for any future
   requirement.
2. **Confirm, then roll ONCE.** One generate/cover call. Where the lane
   specifies slider values the CLI cannot set (covers have no slider
   flags), say so in the confirmation line, roll on server defaults,
   record the target values in the run log for web-UI re-rolls.
3. **Run log** with `lane` metadata (name, invariant, mutation_axis,
   expected_failure). Take-aware downloads to `audio/`.
4. **Report**: takes + an EMPTY scorecard row skeleton (concept survival
   ≥3, surprise ≥4, artifact cost ≤3 → keep). The human listens and
   scores; the skill never self-scores audio.
5. **Stop.** Re-rolls, taming, sweeps — all human-triggered, each its
   own invocation. Exception: Lane 1's audio-influence sweep (4 rolls)
   runs only when explicitly ticked in the budget confirmation, never
   via "surprise me".

Pack authoring stays free: `experiments.md` (the concept-instantiated
lane book, spec below) ships with EVERY pack and doubles as the `list`
menu source and the scorecard ledger. Track the per-pack running credit
total across run logs and mirror it in the scorecard.

**Optional Pass 0 — Producer's Ear (diagnostic, not a lane):** cover the
seed with matched lyrics and an empty style at the web UI's weirdness 0
/ style 0 / audio influence 100 → Suno's reconstruction shows what it
considers load-bearing in the seed. ~10 credits, opt-in, log it like any
roll.

## Lane 1 — Genre Transposition Cover Lab

- **Invariant:** lyrics + core hook remain recognizable.
- **Mutation axis:** genre, wholesale.
- **Prompt strategy:** `generate cover <seed_clip_id>` with `--tags`
  carrying ONE incompatible target genre from the pack's menu (gospel
  soul lament, baroque boom bap, shoegaze drill, ambient drone hymn,
  chamber trip-hop…) plus 2–3 concrete instruments to anchor it. One
  genre per roll; the next genre is a new invocation.
- **Settings:** `--model v5.5`. Target sliders (web-UI only): audio
  influence 50 first roll, weirdness 30. The 30/50/70/85 audio-influence
  sweep is the opt-in exception.
- **Expected failure:** genre gravity drags the cover back toward the
  seed, or melody drift destroys the hook.
- **Keeper signal:** the concept is audible in an alien body — you can
  hum the original over it.
- **Next move:** keeper → remaster or stems; near-miss → adjust audio
  influence one step (web UI), re-roll on human order.

## Lane 2 — Controlled Friction

- **Invariant:** song structure and lyrical concept of the faithful pack.
- **Mutation axis:** emotional architecture of the style prompt.
- **Prompt strategy:** fresh `generate create`; the style prompt carries
  a deliberate contradiction pair built from the concept's primary
  emotion — one side emotional, one side mechanical/textural ("tender
  vocal warmth + rigid machine percussion", "nostalgic glow + unresolved
  harmonic undertow"). Lyrics unchanged from the faithful pack.
- **Settings:** same model as the faithful pack ·
  `--weirdness 45`–`60` · `--style-influence 75` (CLI-settable here).
- **Expected failure:** the contradiction resolves to mush, or one pole
  wins and you get a faithful take with extra words.
- **Keeper signal:** the melody is more alive than the faithful takes —
  friction audible as depth, not noise.
- **Next move:** keeper → the friction pair graduates into the pack's
  main style prompt; miss → swap which pole is emotional vs mechanical
  before any re-roll.

## Lane 3 — Alternate-Reality Renders

- **Invariant:** the song itself — melody, lyrics, arrangement bones.
- **Mutation axis:** performance reality (the room it happens in).
- **Prompt strategy:** `generate cover <keeper_clip_id>`, `--tags`
  appended with ONE reality per roll: "Live Performance, Concert" /
  "MTV Unplugged, crowd sings along to the chorus" / "rehearsal room
  demo" / "bootleg tape recording". Works on any keeper — including the
  existing library (thousands of candidates).
- **Settings:** cover. Target sliders (web-UI only): weirdness 0 ·
  audio influence 100 · style influence 50.
- **Expected failure:** canned-crowd cheese, vocal identity drift.
- **Keeper signal:** a convincing other room — the unplugged version
  you'd put on the B-side.
- **Next move:** keeper → ship as companion version; this lane rarely
  needs a second roll (highest-reliability trick in the pool, 308↑
  multiply confirmed).

## Lane 4 — Red-Letter Mining (two-step by design)

- **Invariant:** the concept's instrumental palette (named instruments
  from the pack).
- **Mutation axis:** controlled chaos — the weirdness ceiling.
- **Prompt strategy (step 1, this invocation):** instrumental
  `generate create` with the pack's palette in `--tags` ·
  `--weirdness 100` · `--style-influence 80`. Expect wreckage; you're
  prospecting.
- **Step 2 ("tame it", next invocation, human-ordered):** cover the
  surviving crazy-good instrumental with the pack's lyrics at sane
  settings — `generate cover` carrying lyrics is not possible, so step 2
  is a fresh `generate create` seeded by the survivor's style learnings,
  OR a web-UI cover with lyrics; state which and why in the
  confirmation.
- **Expected failure:** 15-second glitch tracks, AM-radio noise, mush.
  That's the mine, not a bug; budget says one roll, one core sample.
- **Keeper signal:** a structure or sound you would never have prompted
  directly — the surprise ≥4 criterion is this lane's reason to exist.
- **Next move:** survivor → step 2 taming; total wreckage → re-roll only
  on explicit order, or drop the lane for this pack.

## Lane 5 — Untranslatable-Emotion Lexicon

- **Invariant:** structure, lyrics, instrumentation of the faithful pack.
- **Mutation axis:** the emotional vocabulary of the style prompt.
- **Prompt strategy:** fresh `generate create`; replace the faithful
  pack's generic mood words with ONE tier-1 rare word + scene
  descriptors that set its stage ("hiraeth, 3AM, bedroom production,
  tape hiss, vocals from another room"). Word chosen to match the
  concept's mood:

| Concept mood | Candidate words (observed effects) |
|---|---|
| longing / homesick | saudade (minor 7ths), hiraeth (reverb, slow attack) |
| bittersweet / transient | mono no aware (trad. scales + synths), natsukashii |
| grief / weeping | lacrimoso (affects vocal vibrato rate) |
| crowd-feeling / outward | sonder (uptempo, busy instrumentation) |

- **Settings:** same as the faithful pack, weirdness +10 over faithful.
- **Expected failure:** tier-3 behavior — the word routes to its nearest
  generic synonym and you get a faithful take.
- **Keeper signal:** a texture neither "sad" nor "melancholic" produces;
  the word demonstrably did the heavy lifting.
- **Next move:** keeper → the word enters the pack's permanent style
  vocabulary (this lane is also R&D for faithful mode); miss → try the
  second candidate word, human-ordered.

## Benched lanes (backlog: docs/brainstorm/2026-06-11-suno-experiment-ideas.md)

- **Gravity inversion** — friction's mechanical twin; joins as a Lane 2
  variant if friction underdelivers.
- **Persona laddering** — inherently multi-roll chains; fights the
  one-roll rule.
- **Seed audio abuse** — pp-cli upload support unverified; verify first.
- **Section-tag mutation** — low surprise; partially covered by Lane 2.
- **Haunted tails** — speculative keeper rate; someday-lane.

## experiments.md — the per-pack lane book (emitted with EVERY pack)

The cover file's sibling: a self-serve experiment tutorial the user can
run in the Suno web UI without the skill present, AND the agent's `list`
menu + scorecard ledger when lanes run via CLI. Emit it at pack
authoring time (step 5), derived from `concept.md` while the concept is
fresh in context.

**Derivation rules — the payloads are concept work, not madlibs:**

- **Lane 1:** pre-roll ONE genre maximally incompatible with the
  concept's palette (judged against ITS genre, not a stock list) + 2–3
  concrete anchor instruments; list 3–4 alternative incompatible genres
  as the re-roll menu.
- **Lane 2:** derive the contradiction pair from the concept's PRIMARY
  emotion — one pole emotional, one mechanical/textural, both phrased
  with the concept's own imagery; include the swapped-poles variant as
  the documented re-roll.
- **Lane 3:** pre-roll the reality that most productively collides with
  the concept's premise (say why in one clause); list the other three.
- **Lane 4:** the palette IS the concept's named instruments — copy
  them, never improvise new ones.
- **Lane 5:** match the concept's mood to the lexicon table, pre-roll
  the tier-1 word, name the backup word; scene descriptors come from the
  concept's imagery/motifs section.

Pre-rolled picks are suggestions with alternatives — the human can
re-roll any of them by hand. Web-UI recipes carry the FULL slider values
(the UI can set what the CLI cannot — this file is where slider-true
experimentation lives).

Template:

```markdown
# <Track Name> — Experiments

*<date> — suno-pack · derived from concept.md · menu + scorecard for all experiment rolls*

How to use: pick a lane (or roll a d5), follow its recipe in the Suno
web UI — or tell the agent "give me experiment N" (one roll, ~10
credits, it asks before spending). One roll per lane, judge on the
scorecard, go deeper only on keepers.
**Keep = concept survival ≥3 AND surprise ≥4 AND artifact cost ≤3.**

## Menu

| # | Lane | Mutation axis | This pack's pre-roll | Cost | Requires |
|---|---|---|---|---|---|
| 1 | Genre Transposition | genre, wholesale | <pre-rolled genre> | ~10 cr | seed take |
| 2 | Controlled Friction | emotional architecture | <pair, compressed> | ~10 cr | — |
| 3 | Alternate-Reality Renders | performance reality | <pre-rolled reality> | ~10 cr | seed keeper |
| 4 | Red-Letter Mining | weirdness ceiling | <palette, compressed> | ~10 cr | — |
| 5 | Emotion Lexicon | style vocabulary | <pre-rolled word> | ~10 cr | — |

## Lane 1 — Genre Transposition
- Seed: <runs/ keeper, or "generate the faithful pack first">
- Pre-rolled: **<genre>** anchored by <2–3 instruments>
- Re-roll menu: <3–4 alternative incompatible genres>
- Web UI: open seed → Cover → v5.5 · style: `<genre + anchors>` ·
  weirdness 30 · style influence 50 · audio influence 50
  (sweep 30/50/70/85 if the first roll hugs or drifts)
- Expected failure: genre gravity pulls back to the seed. Keeper: you
  can hum the original over the alien body.

## Lane 2 — Controlled Friction
- Pair (derived): **"<emotional pole> + <mechanical pole>"** ·
  swapped-poles re-roll: "<inverse>"
- Fresh generate, lyrics from `lyrics_v<X>.md` UNCHANGED · style:
  `<friction style prompt>` · weirdness 45–60 · style influence 75
- Expected failure: mush, or one pole wins. Keeper: friction audible as
  depth — melody more alive than the faithful takes.

## Lane 3 — Alternate-Reality Renders
- Pre-rolled reality: **"<reality>"** — <why it collides with the
  premise>. Alternatives: <other three>.
- Web UI: cover the keeper → style append `<reality>` · weirdness 0 ·
  style influence 50 · audio influence 100
- Expected failure: canned-crowd cheese. Keeper: a convincing other
  room — the B-side version.

## Lane 4 — Red-Letter Mining
- Palette (from concept): <named instruments>
- Step 1: instrumental create · style: `<palette tags>` · weirdness
  100 · style influence 80. Expect wreckage — you're prospecting.
- Step 2 ("tame it", separate roll): rebuild around the survivor at
  weirdness 25 / style 80.
- Keeper: a structure you would never have prompted directly.

## Lane 5 — Emotion Lexicon
- Concept mood <mood> → pre-rolled word: **<word>** (<observed
  effect>) · backup: <second word>
- Fresh generate, faithful settings, weirdness +10 · style: `<word>,
  <scene descriptors from the concept's imagery>`
- Expected failure: the word routes to its generic synonym. Keeper: a
  texture neither "sad" nor "melancholic" produces — the word earns a
  permanent place in the pack's vocabulary.

## Scorecard

| Roll | Date | Lane | Clip | Concept | Surprise | Cost | Keep? | Note |
|---|---|---|---|---|---|---|---|---|

Running credit total: 0
```
