# Suno Experiment Mode — The Five Default Lanes

*Concept · 2026-06-11 · Claude (Fable 5) + Pyro · lane set chosen by Pyro
from the 27-lane pool (`2026-06-11-suno-experiment-ideas.md`, which
remains the backlog)*

> Status: decided. Defines the default `--mode experimental` lane set for
> suno-pack, in the experiment-map schema from Codie's
> `~/music/suno/suno_experiment_mode.md`. Execution model per
> `2026-06-11-suno-pack-ppcli-integration.md`: one automated roll per
> lane per round, depth always human-triggered, per-pack hard ceiling.

---

## Invocation API — one lane at a time (decided by Pyro)

Experimental mode never batches lanes. One invocation = one lane = one
roll. The invocation is the consent; cost (~10 credits) is stated in the
confirmation line before firing.

| Invocation | Behavior |
|---|---|
| `--mode experimental` / "surprise me" | One **random** lane, picked among currently *eligible* lanes (no seed yet → random over 2/4/5; seed exists → over all five) |
| `--mode experimental 3` / "give me experiment 3" | That specific lane |
| `--mode experimental list` / "list all experiments" | The menu: number, name, mutation axis, one-liner, cost, seed requirement, current eligibility |
| "tame it" (after a Lane 4 keeper) | Lane 4 step 2 on the chosen survivor |
| "lane 1 again, baroque boom bap" / "re-roll friction, poles swapped" | Repeat invocations — depth is just asking again |

Mechanics per invocation:

1. If the lane needs a seed (1, 3) and none is chosen: the skill says
   so and proposes candidates from observables (library keepers, prior
   takes, run-log scorecards) — human picks, or orders a faithful seed
   roll first.
2. Roll once. Run log written (request + result blocks, lane metadata:
   invariant, axis, expected failure). Take-aware download to `audio/`.
3. Report take + scorecard row skeleton (concept survival ≥3, surprise
   ≥4, artifact cost ≤3 → keep). The scorecard accumulates across
   invocations.
4. Lane 1's audio-influence sweep (4 rolls) remains the declared
   exception — only on explicit request, never via "surprise me".

Pack authoring is unchanged and free: `experiment_map.md` (all five
lanes on paper) ships with every experimental pack and doubles as the
`list` menu source. Per-pack credit ceiling is tracked as a running
total across run logs.

**Optional Pass 0 — Producer's Ear (diagnostic, not a lane):** cover the
seed at weirdness 0 / style 0 / audio influence 100, matched lyrics,
empty style → Suno's reconstruction shows what it considers load-bearing
in the seed. The delta informs every lane's prompt. 10 credits, opt-in.

---

## Lane 1 — Genre Transposition Cover Lab

**Invariant:** lyrics + core hook remain recognizable.
**Mutation axis:** genre, wholesale.
**Prompt strategy:** `generate cover <seed_clip_id>` with tags carrying
one incompatible target genre from the pack's menu (gospel soul lament,
baroque boom bap, shoegaze drill, ambient drone hymn, chamber trip-hop…)
plus 2–3 concrete instruments to anchor it. One genre per roll; the next
genre is a new round.
**Settings:** v5.5 cover · audio influence 50 (first roll) · weirdness
30. The 30/50/70/85 audio-influence sweep is the opt-in exception.
**Expected failure:** genre gravity drags the cover back toward the
seed, or melody drift destroys the hook.
**Keeper signal:** the concept is audible in an alien body — you can hum
the original over it.
**Next move:** keeper → remaster or stems; near-miss → adjust audio
influence one step, re-roll on human order.

## Lane 2 — Controlled Friction

**Invariant:** song structure and lyrical concept of the faithful pack.
**Mutation axis:** emotional architecture of the style prompt.
**Prompt strategy:** fresh `generate create`; the style prompt carries a
deliberate contradiction pair built from the concept's primary emotion —
one side emotional, one side mechanical/textural ("tender vocal warmth +
rigid machine percussion", "nostalgic glow + unresolved harmonic
undertow"). Lyrics unchanged from faithful.
**Settings:** same model as faithful pack · weirdness 45–60 · style
influence 75.
**Expected failure:** the contradiction resolves to mush, or one pole
simply wins and you get a faithful take with extra words.
**Keeper signal:** the melody is more alive than the faithful takes —
friction audible as depth, not noise.
**Next move:** keeper → this friction pair graduates into the pack's
main style prompt; miss → swap which pole is emotional vs mechanical
before any re-roll.

## Lane 3 — Alternate-Reality Renders

**Invariant:** the song itself — melody, lyrics, arrangement bones.
**Mutation axis:** performance reality (the room it happens in).
**Prompt strategy:** `generate cover <keeper_clip_id>`, style appended
with one reality per roll: "Live Performance, Concert" / "MTV Unplugged,
crowd sings along to the chorus" / "rehearsal room demo" / "bootleg tape
recording". Works on any keeper — including the existing library
(thousands of candidates).
**Settings:** cover · weirdness 0 · audio influence 100 · style
influence 50.
**Expected failure:** canned-crowd cheese, vocal identity drift.
**Keeper signal:** a convincing other room — the unplugged version you'd
put on the B-side.
**Next move:** keeper → ship as companion version; this lane rarely
needs a second roll (highest-reliability trick in the pool, 308↑
multiply confirmed).

## Lane 4 — Red-Letter Mining (two-step by design)

**Invariant:** the concept's instrumental palette (named instruments
from the pack).
**Mutation axis:** controlled chaos — the weirdness ceiling.
**Prompt strategy (step 1, this round):** instrumental `generate create`
with the pack's palette in the style prompt · **weirdness 100** · style
influence 80. Expect wreckage; you're prospecting.
**Step 2 (next round, human-ordered):** cover the surviving crazy-good
instrumental with the pack's lyrics at sane settings (weirdness 25 /
style 80) — tame it without flattening it.
**Expected failure:** 15-second glitch tracks, AM-radio noise, mush.
That's the mine, not a bug; budget says one roll, so one core sample.
**Keeper signal:** a structure or sound you would never have prompted
directly — the scorecard's surprise criterion ≥4 is this lane's reason
to exist.
**Next move:** survivor → step 2 taming; total wreckage → re-roll only
on explicit order, or drop the lane for this pack.

## Lane 5 — Untranslatable-Emotion Lexicon

**Invariant:** structure, lyrics, instrumentation of the faithful pack.
**Mutation axis:** the emotional vocabulary of the style prompt.
**Prompt strategy:** fresh `generate create`; replace the faithful
pack's generic mood words with ONE tier-1 rare word + scene descriptors
that set its stage ("hiraeth, 3AM, bedroom production, tape hiss,
vocals from another room"). Word chosen to match the concept's mood:

| Concept mood | Candidate words (observed effects) |
|---|---|
| longing / homesick | saudade (minor 7ths), hiraeth (reverb, slow attack) |
| bittersweet / transient | mono no aware (trad. scales + synths), natsukashii |
| grief / weeping | lacrimoso (affects vocal vibrato rate) |
| crowd-feeling / outward | sonder (uptempo, busy instrumentation) |

**Settings:** same as faithful pack, weirdness +10 over faithful.
**Expected failure:** tier-3 behavior — the word routes to its nearest
generic synonym and you get a faithful take.
**Keeper signal:** a texture neither "sad" nor "melancholic" produces;
the word demonstrably did the heavy lifting.
**Next move:** keeper → the word enters the pack's permanent style
vocabulary (this lane is also R&D for faithful mode); miss → try the
second candidate word, human-ordered.

---

## Benched (one line each, backlog in the ideas doc)

- **Gravity inversion** — friction's mechanical twin; joins as a Lane 2
  variant if friction underdelivers.
- **Persona laddering** — inherently multi-roll chains; fights the
  one-roll rule. Revisit when rounds feel too slow.
- **Seed audio abuse** — pp-cli upload support unverified; verify first.
- **Section-tag mutation** — low surprise; partially covered by Lane 2.
- **Haunted tails** — speculative keeper rate; someday-lane.

## Execution notes

- Every lane maps to commands proven live on 2026-06-11 (`generate
  create`, `generate cover`, per-clip-id downloads, run logs).
- Lanes 1 and 3 need a seed clip → decision #2 applies (human picks,
  skill proposes from observables).
- Lane 4 step 2 and all re-rolls are separate invocations — the
  automated surface is always exactly one roll.
- Scorecard, experiment_map.md, and runs/ ledger ship with the pack as
  immutable publications.
