# Dials — Dimensional Control Systems for LLM Output

*Concept · 2026-06-11 · Claude (Fable 5) + Pyro*

> Status: **concept draft, for Pyro's review.** Decided in conversation:
> name (`dials`, chosen via after-hours:naming-as-design), scope (four
> preset systems + meta-skill; Suno-Style explicitly excluded — it lives
> as an experiment inside suno-pack). Everything else in this document is
> draft: axis ladders, anchor codes, invocation grammar, build order.

---

## Why

An LLM is a compressed corpus that has internalized the *entire spectrum*
of every stylistic axis it ever read. A dimension code is a **coordinate
in that latent style space** — and orthogonal axes let you navigate to
points no human exemplar occupies. Staccato-but-operatic exists in the
space even if nobody ever wrote there.

The pattern has already proven itself three independent times in this
ecosystem, years to months apart, without anyone calling it a pattern:

1. **Pyro-Style v2** (2025-11-26, predates skills entirely) — 5-digit
   prose control, 11 dimensions, author anchors, the honor-the-code
   contract. The founding artifact.
2. **Dream-stories** (2025-11 → today) — a *random* code as chaos element:
   roll what you can't choose, the way you don't choose what you dream.
   Now wired into codies-memory 1.2.x sign-off.
3. **Suno experiment mode** (2026-06-11) — five lanes, each defined as
   "hold the invariant, mutate one axis." That is a single-axis sweep in
   everything but name.

Three uses, three mechanics (set, roll, sweep), one underlying model.
Dials names the model and generalizes it: every quality of an output is
an independent 0–9 dial; a code is a complete, reproducible setting; the
agent executes the setting without "correcting" it.

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
- **Scope v1:** four preset systems + one meta-skill:
  - `dials:prose` — Pyro-Style v2, ported verbatim (founding preset)
  - `dials:explain` — Explain-Style (new)
  - `dials:critique` — Critique-Style (new)
  - `dials:surface` — Surface-Style (new)
  - `dials:forge` — derive a new dimensional system for any domain
- **Out of scope v1:** Suno-Style (suno-pack experiment), Code-Style,
  Image-Style, Research-Style (backlog; forge makes them cheap later).

## Vocabulary

One mental model, one set of nouns (per naming-as-design):

| Term | Meaning |
|---|---|
| **system** | One domain's dimension set (prose, explain, critique, surface) |
| **dimension** | One independent 0–9 ladder (A, B, C…) |
| **code** | A complete coordinate: `12089`, or modular `ABFJK = 00009` |
| **anchor** | A named exemplar with a code (Hemingway = `10004`, Linear = `42323`) |
| **roll** | Random code — the RNG decides, never the operator |
| **sweep** | Hold all dimensions, walk one |
| **crossfade** | Interpolate between two codes in N steps |
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
rigor 0 simplifies but does not introduce falsehoods. Surface at
convention 9 may be alien but stays usable. Truth, safety, and
correctness are not dimensions; no code reaches them.

## Anatomy of a System (standard reference format)

Every system — preset or forged — ships as one reference file with the
same shape, so systems are portable, versionable, and forge-emittable:

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
eyeballed drafts.

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

### Surface-Style (`dials:surface`)

For UI/design exploration — mockups, click dummies, landing pages.

| Dim | Axis | 0 | 5 | 9 |
|---|---|---|---|---|
| A | Density | one thing per screen, air | balanced | Bloomberg terminal |
| B | Playfulness | austere, serious | friendly | toy |
| C | Edge | soft, rounded, shadowed | mixed | hard brutalist, raw borders |
| D | Color voice | monochrome | restrained palette + accent | saturated chaos |
| E | Motion | fully static | purposeful transitions | everything animates |
| F (ext) | Convention | platform-standard patterns | familiar with signature moves | alien |

Draft anchors: Linear `42323` · Notion `33212` · Bloomberg `90761` ·
Teenage Engineering `57852` · Craigslist `70910` · Vercel landing `22435`.

Killer use: SFD explore phase — roll three codes, build three divergent
click dummies, converge from reaction instead of from a blank page.

### Prose (`dials:prose`)

Pyro-Style v2, ported as-is: 5 core + 6 extended dimensions, 14-author
anchor table, three-option proposal flow. No redesign — it is the
calibration reference for everything else. (The copy bundled into
codies-memory 1.2.1 for dreams stays where it is; codies-memory must
remain self-contained. Accepted duplication.)

## The Meta-Skill (`dials:forge`)

Derives a new dimensional system for any domain. This is what makes
dials a plugin instead of a pile of prompts. The discipline:

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
6. **Emit** the standard reference file.
7. **Calibration pass** (cold-read test): generate the same content at
   three distant codes; a blind reader must match output to code. Fail →
   ladders are mush, recalibrate.

Forge's own acceptance test: it must be able to re-derive Explain-Style
from scratch and produce something at least as good as the hand-built
preset. If it can't, forge isn't done.

## Mechanics & Invocation Grammar (proposal)

Mechanics are **verbs understood by every system skill**, not separate
skills — the system is the noun, the mechanic is the verb. One shared
reference doc (`mechanics.md`) keeps each SKILL.md small.

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

## Ecosystem Kinship

- **codies-memory dreams** — `dials:prose` roll *is* the dream mechanic;
  already shipped independently. No dependency either direction.
- **suno-pack experiment mode** — lanes are single-axis sweeps in spirit;
  stays in suno-pack per Pyro's call. Dials is the theory, suno keeps the
  practice.
- **surface-first-development** — `dials:surface` is a natural explore-
  phase tool (roll ×3 → three dummies). Cross-reference, not dependency.
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

## Open Questions (for Pyro's review)

1. **Mechanics grammar:** verbs-inside-system-skills (proposed above) vs
   dedicated `dials:roll` / `dials:sweep` skills? Proposal: verbs inside;
   fewer skills, consistent grammar.
2. **Forge output home:** forged systems land where —
   `docs/dials/<name>-style.md` in the target project? `~/.claude/dials/`
   for personal systems? Promotion path into the plugin as a preset?
3. **Surface-Style × SFD:** cross-reference from the SFD skill's explore
   phase at v1, or keep fully standalone until proven?
4. **Anchor calibration:** draft codes above are eyeballed. Calibrate
   each preset via the cold-read test during build?
5. **Extended dimensions** for the three new presets: v1 or later?
   (Prose ships with its existing F–K; the new three could start core-only.)
6. **Marketplace row:** description wording, version v0.1.0.

## Build Order (sketch)

1. **prose** — port Pyro-Style v2; cheapest; validates plugin packaging
   and the standard reference format.
2. **forge** — hardest; validates the format generatively and the
   discriminator/cold-read discipline.
3. **explain** — built *with* forge as its first real student
   (dogfooding both at once).
4. **critique**, then **surface** — same pipeline, now cheap.
5. Every skill through dojo before the marketplace row updates.
