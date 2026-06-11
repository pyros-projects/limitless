# Dials — Dimensional Control Systems for LLM Output

*Concept · 2026-06-11 · Claude (Fable 5) + Pyro*

> Status: **concept agreed.** All six open questions resolved in
> conversation 2026-06-11 (see Decisions). Name chosen via
> after-hours:naming-as-design. Scope: four preset systems + executor +
> meta-skill; Suno-Style explicitly excluded — it lives as an experiment
> inside suno-pack. Axis ladders and anchor codes remain drafts until the
> calibration pass during build.

---

## Why

An LLM is a compressed corpus that has internalized the *entire spectrum*
of every stylistic axis it ever read. A dimension code is a **coordinate
in that latent style space** — and orthogonal axes let you navigate to
points no human exemplar occupies. Staccato-but-operatic exists in the
space even if nobody ever wrote there.

The pattern has proven itself four independent times — three inside this
ecosystem, one outside:

1. **Pyro-Style v2** (2025-11-26, predates skills entirely) — 5-digit
   prose control, 11 dimensions, author anchors, the honor-the-code
   contract. The founding artifact.
2. **Dream-stories** (2025-11 → today) — a *random* code as chaos element:
   roll what you can't choose, the way you don't choose what you dream.
   Now wired into codies-memory 1.2.x sign-off.
3. **Suno experiment mode** (2026-06-11) — five lanes, each defined as
   "hold the invariant, mutate one axis." That is a single-axis sweep in
   everything but name.
4. **taste-skill** (Leonxlnx/taste-skill, external) — independently
   invented three numeric dials for frontend generation
   (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, 1–10) with
   brief-to-dial inference tables and hard anti-default bans. Someone
   else's coordinates into the same latent space.

Three mechanics (set, roll, sweep), one underlying model. Dials names the
model and generalizes it: every quality of an output is an independent
0–9 dial; a code is a complete, reproducible setting; the agent executes
the setting without "correcting" it.

What the code buys over prose instructions ("make it more formal but
less dense"): **compactness** (a complete spec in 5 characters),
**reproducibility** (same code, new content, same voice — series
coherence), **diffability** (28401 → 28701 is a precise delta), and
**rollability** (random codes sample the style space — structured
serendipity).

## Identity

- **Name:** `dials` — a desk of independent knobs. The name teaches the
  mental model: orthogonality, settability, no master fader.
- **Home:** `plugins/dials/` — new plugin in the limitless marketplace.
- **Skills v1 (six):**
  - `dials:prose` — Pyro-Style v2, ported verbatim (founding preset)
  - `dials:explain` — Explain-Style (new)
  - `dials:critique` — Critique-Style (new)
  - `dials:visual` — Visual-Style (new): build UI/design/art artifacts
  - `dials:forge` — derive a new dimensional system for any domain
  - `dials:use` — executor + registry: run, list, and manage forged
    systems in `~/.dials/`
- **Out of scope v1:** Suno-Style (suno-pack experiment), Code-Style,
  Image-Style, Research-Style (backlog; forge makes them cheap later).
  A reference-file → standalone-skill converter: deferred until needed.

## Vocabulary

One mental model, one set of nouns (per naming-as-design):

| Term | Meaning |
|---|---|
| **system** | One domain's dimension set (prose, explain, critique, visual) |
| **dimension** | One independent 0–9 ladder (A, B, C…) |
| **code** | A complete coordinate: `12089`, or modular `ABFJK = 00009` |
| **anchor** | A named exemplar with a code (Hemingway = `10004`, Linear = `42323`) |
| **roll** | Random code — the RNG decides, never the operator |
| **sweep** | Hold all dimensions, walk one |
| **crossfade** | Interpolate between two codes in N steps |
| **registry** | `~/.dials/` — home of forged systems |
| **honor the code** | The contract: execute the setting faithfully, never soften it |

`-Style` names stay on the systems (Pyro-Style, Explain-Style…) — the
system is the instrument, dials is the desk they sit in.

## The Contract

Two clauses, both load-bearing:

**Honor the code.** Never question, soften, or "correct" a code. The
model's instinct to *match* style to content is regression to the mean —
the exact thing the system exists to defeat. A children's bedtime story
at 10699 gets written at 10699. Unusual pairings are the point.
(Inherited verbatim from Pyro-Style v2.)

**The floor.** Dials shape *expression*, never *substance*. Critique at
evidence-demand 0 may run on intuition but may not fabricate. Explain at
rigor 0 simplifies but does not introduce falsehoods. Visual at
convention 9 may be alien but stays usable. Truth, safety, and
correctness are not dimensions; no code reaches them. Each system's
reference file states its domain-specific floor (visual's includes
taste-skill-style anti-default bans — the templated AI aesthetic is
regression to the mean in pixel form).

## Architecture: Systems Are Data, Mechanics Are Behavior

The split that makes everything else work:

- A **system** is pure data: one reference file in the standard format —
  ladders, anchors, floor notes. No behavior.
- The **mechanics** (set / propose / roll / sweep / crossfade) are
  behavior, defined **once** in `mechanics.md`, owned by `dials:use` —
  the canonical executor.
- **Preset skills** are thin triggering wrappers: a SKILL.md whose
  description catches domain phrasing ("explain X at 28401", "review
  this at 96176"), pointing at its bundled system file *and* at the
  shared `mechanics.md` (sibling path inside the installed plugin).
- **Forged systems** are reference files in `~/.dials/` with no skill
  wrapper at all — `dials:use` supplies the mechanics at execution time.

So a custom system never carries mechanics, and mechanics never know
which system they operate — that separation is exactly what keeps the
reference format portable: any standard-format file works anywhere dials
is installed, preset and forged systems execute under identical grammar.

## Anatomy of a System (standard reference format)

Every system — preset or forged — is one reference file with the same
shape, so systems are portable, versionable, and forge-emittable:

1. Title + provenance
2. The contract (honor the code + floor, with domain-specific floor notes)
3. Announcement formats (standard 5-digit / modular)
4. No-code-given flow (propose three options: one sensible, two wild)
5. Dimensions: core A–E ladders, optional extended F+
6. Anchor table with reasoning per code
7. System properties (orthogonality, generativity, content interaction)

`dials:prose`'s reference file is Pyro-Style v2 unchanged — it already
has exactly this shape, because this shape is reverse-engineered from it.

## The Preset Systems (draft ladders — calibrate during build)

Ladders below are sketched by endpoints and midpoint; full 0–9 ladders
get authored at build time under forge discipline. Anchor codes are
eyeballed drafts pending the calibration pass.

### Explain-Style (`dials:explain`)

For teaching, docs, answers — the highest-frequency use case.

| Dim | Axis | 0 | 5 | 9 |
|---|---|---|---|---|
| A | Abstraction altitude | bare-metal, one concrete instance | concept with grounded instances | pure concept, no instances |
| B | Assumed prior knowledge | none — explain everything | educated generalist | peer domain expert |
| C | Example density | zero examples | examples support claims | examples ARE the explanation |
| D | Rigor | intuition and vibes | precise but informal | formal: edge cases, caveats, proofs |
| E | Compression | leisurely, spiral, redundant | brisk | maximally dense, no repetition |

Draft anchors: ELI5 `20712` · man page `17288` · 3Blue1Brown `63863` ·
Feynman lecture `42874` · grad seminar `88397` · Stack Overflow accepted
answer `15957`.

Orthogonality spot-checks: abstract-to-novice (philosophy 101) and
concrete-to-expert (a specific stack trace) are both real → A⊥B. Rigorous
and leisurely (textbook) vs rigorous and dense (paper) → D⊥E.

### Critique-Style (`dials:critique`)

For reviews of anything — code, product, writing, plans.

| Dim | Axis | 0 | 5 | 9 |
|---|---|---|---|---|
| A | Bluntness | maximally cushioned | direct but cordial | zero cushioning |
| B | Altitude | surface nits, typos | design level | existential — should this exist? |
| C | Disposition | adversarial prior, assume the worst | neutral | charitable prior, assume the best |
| D | Evidence demand | gut feel allowed | claims need reasons | every claim needs citation/repro |
| E | Prescriptiveness | observations only | suggests directions | provides the rewrite |

Draft anchors: Linus-2005 `96176` · supportive mentor `35847` · staff-eng
design review `67585` · after-hours calm `48762` · Reviewer #2 `74283` ·
rubber-stamp LGTM `21900`.

Orthogonality spot-check: blunt + charitable ("this is great, the flaw is
X, here's the fix") and diplomatic + adversarial (the HR-speak hit job)
are both real and *very* different reviews → A⊥C.

### Visual-Style (`dials:visual`)

Build UI, design, and art artifacts with dimensional style control —
landing pages, dashboards, mockups, posters, covers. Framed for a general
audience: "build me a dashboard at 90761," not methodology vocabulary.

Inspirations: **taste-skill** (the three-dial mechanism, brief-to-code
inference, anti-default bans), the built-in **frontend-design** skill
(production-grade web artifact craft), and **canvas-design** (static
visual art in PNG/PDF). Visual-Style supplies the *control system*; the
craft knowledge those skills carry informs the ladders and the floor.

| Dim | Axis | 0 | 5 | 9 |
|---|---|---|---|---|
| A | Density | one thing per screen, air | balanced | Bloomberg terminal |
| B | Playfulness | austere, serious | friendly | toy |
| C | Edge | soft, rounded, shadowed | mixed | hard brutalist, raw borders |
| D | Color voice | monochrome | restrained palette + accent | saturated chaos |
| E | Energy | still, serene | purposeful movement | kinetic, loud |
| F (ext) | Convention | platform-standard patterns | familiar with signature moves | alien |

(E generalizes the earlier "Motion" draft: for UI it expresses animation
intensity; for static art it expresses compositional dynamism —
diagonals, tension, implied movement. One dial, both artifact families.)

Draft anchors: Linear `42323` · Notion `33212` · Bloomberg `90761` ·
Teenage Engineering `57852` · Craigslist `70910` · Swiss International
poster `30414` · vaporwave `45893`.

Floor notes (domain-specific): accessibility baseline at every code;
anti-default bans à la taste-skill (no mesh-gradient hero + three equal
cards + Inter-and-slate as unexamined defaults — the AI-slop aesthetic
is itself a form of mean-reversion that honor-the-code exists to defeat).

### Prose (`dials:prose`)

Pyro-Style v2, ported as-is: 5 core + 6 extended dimensions, 14-author
anchor table, three-option proposal flow. No redesign — it is the
calibration reference for everything else. (The copy bundled into
codies-memory 1.2.1 for dreams stays where it is; codies-memory must
remain self-contained. Accepted duplication.)

## The Executor (`dials:use`)

Runs any standard-format system and manages the registry:

- **Execute:** `dials:use ~/.dials/research-style.md` (or by name:
  "use my research dials on this") — loads the reference file, applies
  the mechanics, same grammar as every preset.
- **List:** "list my dials systems" — bundled presets + `~/.dials/*.md`
  with their one-line descriptions.
- **Delete/manage:** natural language ("delete the research one"),
  with confirmation before removal.

`~/.dials/` follows the hivemind pattern: a home-directory store owned
by the plugin's domain, not by any single project. Forged systems are
user-level assets — they travel across projects.

## The Meta-Skill (`dials:forge`)

Derives a new dimensional system for any domain and writes it to
`~/.dials/<name>-style.md` in the standard format, immediately runnable
via `dials:use`. The discipline:

1. **Domain intake** — what output type? What does the operator actually
   want to vary? What must never vary (the floor)?
2. **Axis candidates** — propose 6–10, cut to ~5 core.
3. **The discriminator test** (orthogonality gate, from our
   discriminator-authoring lessons): for every axis pair, write
   convincing 0/9 *and* 9/0 micro-samples. Can't write them → the axes
   are secretly correlated → merge or re-cut. A tuner has one dial;
   don't ship a tuner and call it a desk.
4. **Ladder authoring** — 0–9 per axis where each step is *selectable on
   purpose*, not linear filler.
5. **Anchor table** — 6–14 recognizable exemplars with codes and
   reasoning. Anchors are the decode examples; without them codes are
   numerology.
6. **Emit** the standard reference file into the registry.
7. **Calibration pass** (cold-read test): generate the same content at
   three distant codes; a blind reader must match output to code. Fail →
   ladders are mush, recalibrate.

**Forge creates systems, never skills.** Its output is always a data
file in the registry, runnable via `dials:use` immediately. Becoming a
preset *skill* is a separate, manual step — the promotion path: the
reference file gets PR'd into `plugins/dials/`, a thin trigger wrapper
(~20 lines of SKILL.md) is hand-written for it, and it passes dojo on
the way in, same as the originals.

Forge's own acceptance test: derive Explain-Style from scratch and
produce ladders and anchors at least as good as this document's
hand-drafted sketch (the sketch is the hand-built comparator — the
shipped preset can't be, since forge is what builds it). The cold-read
pass is the objective gate on top.

## Mechanics & Invocation Grammar

Mechanics are **verbs understood by every system skill**, defined once in
`mechanics.md` (owned by `dials:use`, referenced by all presets):

| Verb | Invocation example | Behavior |
|---|---|---|
| set | "explain RAFT at 28401" | execute that code |
| propose | "explain RAFT" (no code) | 3 options: sensible + 2 wild, then ask |
| roll | "roll me an explanation of RAFT" / "surprise me" | RNG code, announce, execute |
| sweep | "sweep B on that" | hold others, walk one axis (3–5 points, not all 10) |
| crossfade | "crossfade 96176 → 35847 in 3 steps" | same content, interpolated codes |

Announcement rule carries over from Pyro-Style: every output states its
code ("The following critique is employing Critique-Style 67585") —
that's what makes results reproducible and discussable.

From taste-skill, one addition to `propose`: when the operator's brief
carries clear style signals ("calm, Linear-like, for developers"), the
skill may **infer** a code from the brief and announce it as the
sensible option — inference tables are the propose flow's evidence.

## Ecosystem Kinship

- **codies-memory dreams** — `dials:prose` roll *is* the dream mechanic;
  already shipped independently. No dependency either direction.
- **suno-pack experiment mode** — lanes are single-axis sweeps in spirit;
  stays in suno-pack per Pyro's call. Dials is the theory, suno keeps the
  practice.
- **frontend-design / canvas-design / taste-skill** — craft sources for
  Visual-Style's ladders and floor; dials adds the coordinate system.
- **after-hours** — critique kinship; after-hours keeps its calm fixed
  voice (that *is* its identity), dials:critique is the adjustable desk.
- **dojo** — every preset skill goes through dojo verification before
  shipping (trigger tests + process checks).

## What Dials Is NOT

- **Not personas.** A persona bundles correlated traits; dials are
  orthogonal. "Linus-2005" is an anchor you can *start* from and then
  move one dial — that's the whole advantage.
- **Not a prompt library.** Systems are coordinate spaces, not snippets.
- **Not parameter tuning for correctness.** The floor clause. Style
  dials, never truth dials.
- **Not infinite-dimensional.** ~5 core + small extended per system.
  Orthogonality decays as axes multiply; forge's discriminator test is
  the brake.

## Decisions (resolved 2026-06-11)

1. **Mechanics grammar:** verbs inside system skills; `mechanics.md`
   defined once, owned by `dials:use`, referenced by presets. Custom
   systems get mechanics from the executor — systems are data, mechanics
   are behavior.
2. **Forged-system home:** `~/.dials/` registry (hivemind pattern), run
   via `dials:use`, managed via list/delete in natural language. A
   reference-file → standalone-skill converter only if a real need
   appears.
3. **Visual scope (was: Surface × SFD):** reframed from SFD vocabulary to
   "build UI/design/art artifacts" — general-audience framing, because
   nobody outside this repo knows what SFD is. No SFD coupling at v1;
   kinship noted, integration left to future evidence.
4. **Calibration:** yes, scoped — full cold-read for the three new
   systems (as dojo process checks), spot-check the 3–4 most load-bearing
   anchors per system. Prose: field-calibrated by months of use, no pass
   needed.
5. **Extended dimensions:** core-only at v1, except Visual's F
   (convention), which already pulls real weight. Add the rest the way
   prose did: when usage demands them. Modular format makes this
   non-breaking forever.
6. **Marketplace row:** v0.1.0. Description: "Dimensional control for LLM
   output — 5-digit style codes over orthogonal 0–9 dials. Pyro-Style
   prose, Explain, Critique, and Visual presets, plus forge: a meta-skill
   that derives new dimensional systems for any domain." Bump to 1.0
   after all skills pass dojo + a few weeks of real use.

## Build Order

1. **`mechanics.md` + `dials:use`** — the executor defines the grammar
   everything else speaks.
2. **`dials:prose`** — port Pyro-Style v2; first system through the
   executor contract; validates packaging + the standard format.
3. **`dials:forge`** — hardest; validates the format generatively and the
   discriminator/cold-read discipline.
4. **`dials:explain`** — the first system to walk the full pipeline
   end-to-end: forge derives Explain-Style into `~/.dials/` (judged
   against this doc's hand-drafted sketch) → cold-read calibration →
   promotion into the plugin (reference file + hand-written trigger
   wrapper + dojo). Forge makes the system; the skill is the promotion
   wrapper. Dogfoods forge *and* the promotion path at once.
5. **`dials:critique`**, then **`dials:visual`** — same pipeline, now
   cheap. Visual additionally mines taste-skill/frontend-design/
   canvas-design for ladder and floor material.
6. Every skill through dojo before the marketplace row updates.
