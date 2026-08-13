---
name: learn-anything
description: "This skill should be used when the user wants a beginner-to-expert learning path, curriculum, study plan, or training progression for any topic — academic, physical, creative, linguistic, or professional — built by researching how that domain is optimally taught, then emitting only the first progression tier through a failable capstone. Also for mid-path progress reports, capability diagnosis, and authoring the next tier on demand after a gate. Responds to 'learn anything', 'build me a curriculum', 'beginner to expert in', 'learning path for', 'teach me X from scratch', 'study plan for', 'training plan to', 'progress report on my learning', 'what should I study next', 'I passed the capstone — next tier', or any ask whose job is sequenced mastery with gated progression rather than a one-shot explainer. NOT for one-off explanations, homework answers, or generic 'summarize this topic' without a progression path."
---

# Learn Anything — Curricula That Earn The Next Tier

## Overview

A learn-anything curriculum is a **moving target**. This skill never dumps a
full beginner→expert opus. It web-researches how *this* domain is taught,
locks a domain-shaped structure, and **fully formulates only Tier 1** —
lessons through the first **failable capstone**. Later tiers stay as
titles/exit-goals until the learner clears the gate; then the next block is
authored fresh (new search + learner feedback).

Lesson checks are **formative and non-failable** (they persist capability
notes; they never block within-tier progress). Capstones **fail or pass**.

Persist learner state under `~/.limitless/learn-anything/<slug>/` by default
(see `references/persistence.md`). Do not fill the user's project with
training debris unless they ask.

## Modes (classify first)

| Mode | Signals | What you do |
|---|---|---|
| **Genesis** | New topic / "build me a curriculum" | Recon → structure → emit Tier 1 only |
| **Continue** | "next tier", "I passed the capstone" | Load state → fresh recon → emit **one** next tier only |
| **Report** | "progress report", "how am I doing", "what would help me move faster" | Load state → structured report (see `references/reporting.md`) |
| **Lesson/assess** | "I'm done with L2", "grade this", "run the formative" | Update capability map; never invent a fail gate on formatives |

If ambiguous, ask one clarifying question, then proceed.

## Phase 0 — Preflight

1. Derive a stable `slug` from the topic (e.g. `number-theory`, `deadlift-2x-bw`).
2. Check for existing state: `ls ~/.limitless/learn-anything/<slug>/`.
   - Exists + continue/report → load it; do not reinvent.
   - Genesis with existing state → confirm overwrite vs resume.
3. Probe web search (SearXNG / available web search tools). Record live or dead.

## Phase 1 — Pedagogy recon (mandatory before structure)

**Before** writing any lesson list, search how this domain is *taught and
sequenced* — not only what the topic is.

Run ≥2 targeted queries shaped like:
- `"<topic> curriculum OR syllabus OR learning path OR progression"`
- `"how to learn <topic>" OR "<topic> beginner program OR course sequence"`
- Domain-specific: `"<topic> pedagogy"`, coaching manuals, first-course midterm
  scope, belt/grade systems, method books — whatever experts in *that* field use.

Synthesize into a short recon note (persist as `recon.md`):
- Canonical early sequence / milestones experts use
- What a **first real gate** looks like in this domain
- How structure should differ from other domains

**Anti-pattern:** inventing "Module 1 / Week 1" from generic templates before
any domain recon.

### Search down → degrade, do not block

If search is unavailable:
1. **Say so explicitly** before the curriculum body.
2. Still emit Tier 1 from best prior knowledge.
3. Label structure **provisional / lower-confidence**.
4. **Still obey the Tier-1-only gate** — degradation is not a license to dump
   the full expert path. (Baseline failure mode this rule closes.)

## Phase 2 — Lock domain shape

The skeleton must look like the domain, not like a blog outline.

| Domain family | Structure cues (examples, not checklists) |
|---|---|
| Academic / theoretical | Proof/problem ladders, definition→theorem→exercise, course-midterm gates |
| Physical / performance | Form → load → programming blocks, recovery, measurable PRs; safety before intensity |
| Creative / performance art | Ear/repertoire/etudes, constraints, jam/recital readiness — not textbook chapters |
| Linguistic / communicative | Comprehensible input, production drills, CEFR-like can-do gates |
| Professional / craft | Tooling → supervised reps → supervised solo → portfolio gate |

**Contrast test:** a number-theory Tier 1 and a deadlift Tier 1 must not share
the same section template. If they could swap titles and still read fine, the
shape is wrong — redo Phase 1–2.

Physical domains: **technique/safety diagnostics before heavy loading**.

## Phase 3 — Emit Tier 1 only (hard gate)

Allowed in the deliverable:
- Brief progression map: later tiers as **titles + exit goals only**
- **Fully written** Tier 1: ordered lessons, resources, practice, assessments
- Exactly **one failable capstone** ending Tier 1

Forbidden until Continue mode after a pass:
- Fully written Tier 2+ lessons
- Multi-phase "complete expert" manuals (even when search is down)

Each Tier-1 lesson includes:
- Objectives
- Study focus / practice
- **Formative assessment** (non-failable) — see `references/assessment.md`

Capstone must be **domain-sensical** (proof set, filmed lift standard, jam
etude, conversation can-do — not a generic multiple-choice quiz bolted on).

State the emission rule in the artifact so future agents do not "helpfully"
expand later tiers.

## Phase 4 — Persist

Write/update under `~/.limitless/learn-anything/<slug>/` (or user-named path):

- `learner.md` — topic, tier, assessments, strengths, issues, feedback
- `tier-N.md` — active tier body
- `recon.md` — pedagogy search log for this emission
- `progression-map.md` — titles/goals for unauthored tiers
- `reports/` — dated progress reports when in Report mode

Schemas: `references/persistence.md`.

## Phase 5 — Report mode

When asked how they are doing / how to go faster, read `references/reporting.md`
and produce that structure. Always:
- Load persisted state (do not invent a blank history if files exist)
- Name concrete strengths **and** issues from assessment notes
- Give actionable next steps tied to named lessons/weaknesses
- **Do not** emit a full next tier as the report — near-term guidance only
- Persist the report under `reports/` and update capability fields on `learner.md`

## Phase 6 — Continue mode (next tier)

Only after capstone **pass** (or user explicitly overrides with eyes open):

1. Load weaknesses, strengths, user feedback from `learner.md`
2. **Fresh** pedagogy recon for the *next* block (do not only copy the old map)
3. Emit **one** new fully written tier through its capstone
4. Explicitly design ≥1 lesson addressing named weak spots
5. Keep formative + failable dual assessment contract

## Quality bar (self-check before delivery)

- [ ] Recon happened before structure (or degradation labeled)
- [ ] Domain shape fails the swap-title contrast test vs a different family
- [ ] Only one tier fully written; later = titles/goals
- [ ] Every lesson has non-failable formative; tier ends in failable capstone
- [ ] Capstone matches the domain's real competence signal
- [ ] State persisted under learn-anything home
- [ ] Report/continue paths load state and respect gates

## References

- `references/assessment.md` — read when writing formatives or capstones
- `references/reporting.md` — read in Report mode
- `references/persistence.md` — read when creating/updating learner homes
