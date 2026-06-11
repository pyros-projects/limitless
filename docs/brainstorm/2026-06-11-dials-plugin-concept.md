# Dials — Dimensional Control Systems for LLM Output

*Concept · 2026-06-11 · Claude (Fable 5) + Pyro*

> Status: **concept agreed.** All open questions resolved in conversation
> 2026-06-11 (see Decisions). Name chosen via
> after-hours:naming-as-design. Architecture simplified on Pyro's review:
> **two skills, systems are all reference files** — presets are just
> bundled ones. Suno-Style explicitly excluded — it lives as an
> experiment inside suno-pack. Axis ladders and anchor codes remain
> drafts until the calibration pass during build.

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
- **Two skills:**
  - `dials:use` — the executor: runs any system (bundled or forged) with
    the full mechanics grammar; lists and manages the registry.
  - `dials:forge` — derives a new dimensional system for any domain.
- **Four bundled systems** (reference files shipped with the plugin,
  identical in format to forged ones — just pre-calibrated):
  - **Pyro-Style** (prose) — v2 ported verbatim, the founding system
  - **Explain-Style** — teaching, docs, answers
  - **Critique-Style** — reviews of anything
  - **Visual-Style** — build UI/design/art artifacts
- **Out of scope v1:** Suno-Style (suno-pack experiment), Code-Style,
  Image-Style, Research-Style (backlog; forge makes them cheap later).
  Per-system trigger-wrapper skills: only if dojo trigger evidence
  demands them (see Decisions #7).

## Vocabulary

One mental model, one set of nouns (per naming-as-design):

| Term | Meaning |
|---|---|
| **system** | One domain's dimension set, as a standard-format reference file |
| **bundled system** | A system shipped with the plugin (pre-calibrated preset) |
| **forged system** | A system derived by forge, living in the registry |
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
reference file states its domain-specific floor (Visual's includes
taste-skill-style anti-default bans — the templated AI aesthetic is
regression to the mean in pixel form).

## Architecture: One Executor, Systems All the Way Down

The simplification that fell out of Pyro's review: **there is no
difference between a preset and a forged system.** Both are reference
files in the standard format. Presets are merely bundled with the
plugin, pre-calibrated, and maintained under dojo discipline.

- A **system** is pure data: ladders, anchors, floor notes. No behavior.
- **`dials:use`** is the only executor. It owns `mechanics.md` (the verb
  grammar) and binds it to whichever system the request names.
- **Name resolution:** bundled systems first by name (`explain`,
  `critique`, `prose`/`pyro-style`, `visual`), then `~/.dials/*.md`.
  A registry file with the same name as a bundled system shadows it;
  `use` announces the shadowing so it never happens silently.
- **Triggering:** `dials:use` triggers on dials vocabulary — 5-digit
  codes ("at 28401"), the verbs (roll/sweep/crossfade), system names,
  anchor references. Requests without dials markers ("explain RAFT
  simply") correctly do *not* trigger dials. This single-description
  trigger surface is a dojo test target; if evidence shows a domain
  routes poorly, a thin per-system wrapper skill can be added later as a
  pure triggering optimization — without changing this architecture.

Invocation, all equivalent in form:

```
/dials:use explain — explain RAFT at 28401
"critique this diff at 96176"
"use my research dials on this question"
"roll me a visual for the landing page"
```

## Anatomy of a System (standard reference format)

Every system — bundled or forged — is one reference file with the same
shape, so systems are portable, versionable, and forge-emittable:

1. Title + provenance
2. The contract (honor the code + floor, with domain-specific floor notes)
3. Announcement formats (standard 5-digit / modular)
4. No-code-given flow (propose three options: one sensible, two wild)
5. Dimensions: core A–E ladders, optional extended F+
6. Anchor table with reasoning per code
7. System properties (orthogonality, generativity, content interaction)

Pyro-Style v2 is the founding instance — it already has exactly this
shape, because this shape is reverse-engineered from it.

## The Bundled Systems (draft ladders — calibrate during build)

Ladders below are sketched by endpoints and midpoint; full 0–9 ladders
get authored at build time under forge discipline. Anchor codes are
eyeballed drafts pending the calibration pass.

### Explain-Style

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

### Critique-Style

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

### Visual-Style

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

### Pyro-Style (prose)

v2 ported as-is: 5 core + 6 extended dimensions, 14-author anchor table,
three-option proposal flow. No redesign — it is the calibration
reference for everything else. (The copy bundled into codies-memory
1.2.1 for dreams stays where it is; codies-memory must remain
self-contained. Accepted duplication.)

## The Executor (`dials:use`)

Runs any system and manages the registry:

- **Execute:** "explain RAFT at 28401" / `/dials:use explain` /
  "use my research dials on this" — resolve the system name, load its
  reference file + `mechanics.md`, apply the requested verb.
- **List:** "list my dials systems" — bundled + `~/.dials/*.md` with
  their one-line descriptions, shadowing flagged.
- **Delete/manage:** natural language ("delete the research one"),
  with confirmation before removal. Bundled systems can't be deleted —
  only shadowed.

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

Because presets and forged systems are the same kind of object,
**promotion is a file copy**: a forged system that proves out moves from
`~/.dials/` into the plugin's bundled systems (plus a dojo calibration
record). No wrappers, no scaffolding — forge output is already in final
form.

Forge's own acceptance test: derive Explain-Style from scratch and
produce ladders and anchors at least as good as this document's
hand-drafted sketch (the sketch is the hand-built comparator — the
shipped bundled system can't be, since forge is what builds it). The
cold-read pass is the objective gate on top.

## Mechanics & Invocation Grammar

The five verbs, defined once in `mechanics.md` (owned by `dials:use`):

| Verb | Invocation example | Behavior |
|---|---|---|
| set | "explain RAFT at 28401" | execute that code |
| propose | "explain RAFT with dials" (no code) | 3 options: sensible + 2 wild, then ask |
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

- **codies-memory dreams** — a Pyro-Style roll *is* the dream mechanic;
  already shipped independently. No dependency either direction.
- **suno-pack experiment mode** — lanes are single-axis sweeps in spirit;
  stays in suno-pack per Pyro's call. Dials is the theory, suno keeps the
  practice.
- **frontend-design / canvas-design / taste-skill** — craft sources for
  Visual-Style's ladders and floor; dials adds the coordinate system.
- **after-hours** — critique kinship; after-hours keeps its calm fixed
  voice (that *is* its identity), Critique-Style is the adjustable desk.
- **dojo** — both skills go through dojo verification before shipping;
  each bundled system gets a calibration record.

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

1. **Two skills, not six** (Pyro's simplification): `dials:use` +
   `dials:forge`. The four presets are bundled reference files, not
   skills — same format as forged systems, just pre-calibrated. Promotion
   of a forged system = file copy + dojo calibration record.
2. **Mechanics:** defined once in `mechanics.md`, owned by `dials:use`,
   the single executor. Systems are data, mechanics are behavior; custom
   systems never carry mechanics.
3. **Forged-system home:** `~/.dials/` registry (hivemind pattern), run
   via `dials:use`, managed via list/delete in natural language.
   Registry files shadow same-named bundled systems, announced, never
   silent. A reference-file → standalone-skill converter only if a real
   need appears.
4. **Visual scope:** framed as "build UI/design/art artifacts" —
   general-audience wording, because nobody outside this repo knows what
   SFD is. No SFD coupling at v1; kinship noted, integration left to
   future evidence. taste-skill + frontend-design + canvas-design are
   the craft sources.
5. **Calibration:** yes, scoped — full cold-read for the three new
   systems (as dojo records), spot-check the 3–4 most load-bearing
   anchors per system. Pyro-Style: field-calibrated by months of use, no
   pass needed.
6. **Extended dimensions:** core-only at v1, except Visual's F
   (convention), which already pulls real weight. Add the rest the way
   prose did: when usage demands them. Modular format makes this
   non-breaking forever.
7. **Trigger architecture:** single-description triggering on dials
   vocabulary (codes, verbs, system names) via `dials:use`, verified by
   dojo trigger tests. Thin per-system wrapper skills are the documented
   fallback if a domain demonstrably routes poorly — an additive
   optimization, not an architecture change.
8. **Marketplace row:** v0.1.0. Description: "Dimensional control for LLM
   output — 5-digit style codes over orthogonal 0–9 dials. Pyro-Style
   prose, Explain, Critique, and Visual systems, plus forge: a meta-skill
   that derives new dimensional systems for any domain." Bump to 1.0
   after dojo passes + a few weeks of real use.

## Build Order

1. **`mechanics.md` + `dials:use`** with **Pyro-Style** as the first
   bundled system — the executor, the grammar, and the founding system
   land together; validates the standard format against the one
   field-calibrated instance.
2. **`dials:forge`** — validates the format generatively and the
   discriminator/cold-read discipline.
3. **Explain-Style** — the first system to walk the full pipeline
   end-to-end: forge derives it into `~/.dials/` (judged against this
   doc's hand-drafted sketch) → cold-read calibration → promotion by
   file copy into the bundled systems. Dogfoods forge *and* promotion
   at once.
4. **Critique-Style**, then **Visual-Style** — same pipeline, now cheap.
   Visual additionally mines taste-skill/frontend-design/canvas-design
   for ladder and floor material.
5. **Dojo:** trigger tests on `dials:use` (the critical surface: organic
   code phrases routing correctly), process checks on forge, calibration
   records per bundled system — all before the marketplace row updates.
