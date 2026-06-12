# hivemind — Blocks, Wildcards, Drift: the briefing-engine back-port

*Brainstorm · 2026-06-12 · Claude (Fable 5) + Pyro · first pass*

> Status: **idea backlog for the next hivemind iteration** (current:
> 0.11.0, dojo-verified — see `docs/dojo/hivemind-record.md`). Source:
> design review of a sibling recurring-briefing engine on the work
> side, built the same day from the same "config = contract" insight.
> The two tools sit at opposite ends of a tool spectrum — hivemind
> assumes abundance (five venues, fix-offer-first, every tool wanted),
> the sibling assumes scarcity (web+gh floor, never ask to install) —
> so only philosophy-compatible mechanics are imported. Six items,
> ranked.

---

## 1. The block verb + scoped exclusions

**"block X"** — anytime, including after delivery: re-render derived
outputs minus the blocked item, add the config exclusion + changelog
line, bump the edition. Frames stay immutable; the suppressed item
moves to an audit location inside its frame, excluded from rendering.

The insight that earns it: **the cost of correction determines how
much config-truth the user ever voices.** If fixing "I never want
billing noise" looks like a full re-sweep, the correction gets
swallowed and the config silently rots. A correction must be a casting
operation, not a re-run.

Scoped exclusions fall out naturally: `- <topic> [brief]` suppresses
in the brief but allows a one-line mention elsewhere (e.g. a delivery
target's agenda); unscoped = excluded everywhere.

## 2. Wildcard slots in config topic lists

A `*` line in a config's topic list (optionally `* — <steer hint>`) is
**reserved discovery budget**: resolved ad-hoc each `repeat` to
something currently loud in the domain that no named topic covers.
Multiple `*` lines = that many slots. Exclusions bind wildcards like
named topics.

Why: a `repeat` only sees what the topics name plus whatever the
venue-top recipes happen to surface. Today the discourse floor is an
informal property of well-written configs (ai-dev-weekly's "major
dev-related AI news" catch-all); wildcards make the engine guarantee
it. Config-template line: every repeat carries at least one venue-top
or wildcard pass.

## 3. Topics, not products — fresh resolution at run time

Config topic lists hold **topic areas, never products**: "spec-driven
development", not "OpenSpec specifically". The sweep resolves each
topic to its *current* products/repos/sources fresh each run; product
preferences live in the intent/steering prose instead.

Why: prevents the staleness class instead of detecting it. The
staleness rule (thin 2 consecutive → propose replacement) then only
fires for genuinely dead topic *areas*, not for products that renamed,
pivoted, or got superseded. ai-dev-weekly e2 should migrate its
product-named entries when it next changes anyway.

## 4. Drift candidates in the manifest

New manifest field: `drift_candidates` — recurring findings that fit
no config topic, recorded per run. A wildcard resolution that keeps
earning its slot, or a drift candidate that recurs across frames,
becomes a **proposed** topic add at the next crystallize pass.

Why: crystallize today captures *user-steered* deltas only. Drift
candidates add the *data-driven* evolution channel — the sweep itself
proposing what the config is missing. (The H4 graduation subagent
improvised exactly this when it proposed re-homing a dead topic to the
papers venue; it should be designed machinery, not subagent
initiative.) Propose-confirm and degradation-is-not-intent apply
unchanged — drift proposals cite the evidence frames like staleness
proposals do.

## 5. Selection-time vs discovery-time constraint binding

Split config constraints into two kinds with different binding points:

- **Budget exclusions** ("mute async-std") — bind *discovery*: no
  search budget spent, suppressions logged.
- **Steering constraints** (audience, ecosystem priority, "Copilot+
  OpenSpec are priority signal") — bind *selection and writing only*,
  never discovery. Sweep wide, select narrow.

Why: steering constraints encode what the audience *uses*; a sweep's
job includes what the audience *doesn't know yet*. A tool dying that
nobody on the team uses is relevant precisely because they don't use
it. Evidence from the sibling engine's first production run: ecosystem
steering applied at discovery time pulled 5 of 8 articles into the
home ecosystem and missed the window's two biggest stories. One
sentence in the config template fixes the class.

## 6. The growing per-slug viewer

`~/.hivemind/<slug>/view.html` — regenerated from ALL frames after
every `repeat`, newest run first, per-run footer (venues, chain,
edition). Radar's HTML machinery is the base; this is the cumulative
variant.

Why: frames are an archive nobody reads. A `repeat` series is a
publication — the brief-of-briefs view makes the series legible over
time and gives the diff step a human-checkable surface. Lowest
priority of the six; the only one that's a feature rather than a
contract fix.

## What does NOT come over

- **Silent-probe / never-offer-installs** — wrong for hivemind; the
  fix-offer-first + named-venue honesty contract stays.
- **No-opinions article contract** — hivemind briefs want best takes
  and stance mining; that rule belongs to team briefings.
- **Wizard-style config creation** — hivemind stays
  demonstration-only (crystallize); a wizard is the right second door
  for team-facing tools, not for a single-operator skill.

## Testing sketch (dojo, when implemented)

Block verb (re-render minus item, frames untouched, edition bumped);
wildcard resolution (slot filled by in-window discourse story, steer
hint honored, exclusions bind); drift candidate → proposed topic add
with frame evidence; steering-vs-budget binding (steered run still
surfaces an out-of-ecosystem story); viewer regeneration (prior runs
preserved). Trigger eval: "block <topic>" positives; existing matrix
holds.
