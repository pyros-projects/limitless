# hivemind — Crystallize & Repeat: Configs by Demonstration

*Brainstorm · 2026-06-12 · Claude (Fable 5) + Pyro · first pass*

> Status: **design for review.** Crystallized from the 2026-06-12
> `ai-dev-weekly` session: a multi-topic trend sweep (social + gh +
> verification) whose recipe was shaped live by mid-session corrections
> (window 7d→14d, topics extended, output format rewritten twice). The
> first config produced this way already exists:
> `~/.hivemind/ai-dev-weekly/config.md` (edition 1, hand-crystallized).
> This design makes the mechanic part of the skill. Related KG capture:
> `captures/2026-06-12-canon-evidence-from-the-skill-layer.md`
> (engine + definitions; "config = contract"; self-managed config
> lifecycle as unclaimed territory).

---

## The job

Hivemind sweeps are currently one-shot: frames persist *what happened*
(manifest.md, immutable), but recurring intents have no *living recipe*.
Repeating last week's sweep requires the conversation that produced it.
User preferences revealed mid-session (windows, topics, output formats,
muted subjects) evaporate unless someone hand-writes them down.

The inversion this design adds: **the session is the requirements
interview.** Instead of configuring upfront (wizard-style, predicting
what you'll want), the user just runs a sweep and steers; the skill
records what the steering revealed and crystallizes it into a config.
Next time: "repeat ai-dev-weekly".

Mid-session corrections are exactly the data a wizard can't elicit —
nobody knows they want "one flowing paragraph, no What/Why labels"
until they've seen the labeled version.

## Design

### The config file

`~/.hivemind/<topic-slug>/config.md` — topic level, *beside* the dated
frame dirs, never inside them.

| | manifest.md (existing) | config.md (new) |
|---|---|---|
| Scope | one sweep (dated frame) | the recurring intent |
| Mutability | immutable once written | living, edition-bumped |
| Tense | past — what happened | future — what to do next time |

Sections (template in `references/`): intent + audience, topic list
(with a staleness rule), pipeline recipe (venues, windows, floors,
known CLI quirks and keyword traps discovered in past runs), output
format + delivery target, persistence rules, dated changelog with
edition numbers.

**The canonical worked example already exists:**
`~/.hivemind/ai-dev-weekly/config.md` (edition 1, hand-crystallized
2026-06-12 from a real session). The `references/` template is
*distilled from that file*, not invented — an implementer should read
it first; every section named above is present there with real values,
including the recorded CLI trap (`--exclude retweets` + min-likes
combination returns empty) and the keyword traps (unscoped "RAG"/
"agentic" collide with non-tech usage).

Hard rule: **propose-confirm only.** The skill never silently rewrites
user intent. Every accepted change = edition bump + dated changelog
line naming what changed and why.

### Verbs

1. **Crystallize.** After any sweep that smells recurring (user says
   "weekly", "again next time", names a cadence, or asks to freeze the
   process) — or on explicit request — offer to write/update
   `config.md`. Source material: the frame's manifest (queries,
   adaptations, named rejections) plus every user correction observed
   in the session. Corrections map to config lines; muted topics map
   to an exclusions list; the output the user finally accepted maps to
   the format spec.

2. **Repeat.** `repeat <slug>` (or "wiederhole <slug>"):
   - Load `config.md`; say which edition is running.
   - Execute the recipe as a normal hivemind sweep (full frame
     contract: raw/, manifest.md, brief.md — unchanged).
   - **Diff against the previous frame's brief**: stories already
     reported are dropped unless there's a material development
     (a weekly that re-reports last week is worthless).
   - **Staleness check**: a topic returning thin results for 2
     consecutive frames triggers a replacement proposal (the config's
     staleness rule names the threshold).
   - Deliver per the config's output spec.
   - Close with a crystallize pass: any deviation the user steered
     this run becomes a proposed config delta.

3. **Lookup.** At the start of any *ad-hoc* sweep request: if the ask
   plausibly matches an existing config slug, say so and apply that
   config's constraints (especially exclusions) before sweeping. The
   counterpart of crystallize — demonstration captures what the user
   *says*; lookup replays what they *already said*. Without it,
   standing preferences silently fail to reach ad-hoc sessions (the
   2026-06-12 silent-drift lesson, captured as IN-20260612-1f82).

### What does NOT change

- The frame contract (immutability, manifest discipline, named triage
  rejections, `--no-keep`) stays exactly as is.
- Radar mode untouched; a radar series can carry a config like any
  other topic dir.
- Sweep methodology (recon → fan-out → triage → deep-read → synthesis)
  unchanged — the config parameterizes it, never replaces phases.

## Approaches considered

- **Separate "research-loops" skill** owning configs and calling
  hivemind — rejected: second engine over the same frames; the config
  is meaningless without the sweep mechanics it parameterizes.
- **Config as YAML frontmatter on the topic dir** — rejected: the
  recipe is prose-shaped (steer hints, traps, audience framing);
  markdown with a changelog reads and anneals better. Frontmatter for
  the scalar fields only (cadence, window, edition).
- **Auto-crystallize without confirm** — rejected: configs are
  contracts; silent rewrites destroy trust in them.

## Error handling

- `repeat <slug>` with no config → say so, offer a normal sweep +
  crystallize at the end.
- Config conflicts with the live ask ("repeat ai-dev-weekly but only
  Reddit") → the ask wins for this run; the deviation becomes a
  proposed delta, not an auto-edit.
- Stale recipe details (dead venue, renamed CLI flag) → adapt per the
  existing adaptive-floor rules, record in manifest, propose the
  config fix in the crystallize pass.
- Previous frame missing/corrupt → run without the dedup diff, say so.

## Testing (dojo)

Tier: technique. Scenarios:

1. **Cold replay**: fresh subagent, no conversation context, only
   `repeat ai-dev-weekly` + the config file — must execute the recipe
   (correct venues, window, output shape) without asking the user
   anything the config already answers.
2. **Crystallize-on-deviation**: scripted session with two mid-sweep
   corrections — the proposal must contain both; nothing written
   before confirm.
3. **Staleness**: synthetic frames where one topic is thin twice —
   replacement proposal must fire, naming the evidence.
4. **Lookup**: ad-hoc ask overlapping an existing config with an
   exclusion — output must honor the exclusion and say which config
   bound it.

Trigger eval: positives ("repeat ai-dev-weekly", "wiederhole den
Sweep von letzter Woche", "frier den Prozess ein") must route to
hivemind; near-miss negatives (one-off "what's hot in X" without
recurrence smell) must not trigger crystallize offers.

First real test object: `~/.hivemind/ai-dev-weekly/config.md` (edition
1) — the cold-replay scenario can run against it as-is.

## Non-goals

- No scheduling/cron (user-triggered; `/loop` exists for cadence).
- No cross-config inheritance or global defaults file.
- No sync with any other engine's config stores — one config per
  intent, owned here.
