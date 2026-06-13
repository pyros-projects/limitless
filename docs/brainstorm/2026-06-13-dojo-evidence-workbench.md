# Dojo Evidence Workbench

*Concept spec · 2026-06-13 · first pass*

> Status: **design for James review.** Sparked by comparing Anthropic's
> skill-creator flow against Dojo's first James run. The result was not
> "replace Dojo." The result was: Dojo has the stronger truth discipline,
> while Anthropic has useful review and packaging ergonomics. This concept
> defines what to borrow without weakening Dojo's baseline-fail-first spine.

---

## The job

Dojo already answers the most important question:

> Did the skill change future agent behavior in an observable way?

Its first James run found the real failures: context contamination, missing
scope envelopes, score chasing, restart-vs-resume confusion, and prior-review
memory leaking into new evidence. Those failures shaped the current James skill.

Anthropic's skill-creator flow answers a different question well:

> Can the author and human inspect eval outputs, benchmark tables, packaging
> state, and description-trigger attempts in a coherent workspace?

The useful next step is a **Dojo Evidence Workbench**: an optional reporting and
eval-hygiene layer that keeps Dojo's seven kata, but makes the evidence easier
to inspect and harder to overclaim.

The kata are Dojo's named practice forms. This concept does not replace them or
rename them. It only adds evidence hygiene to the points in the existing loop
where a run can lie to us.

For orientation, the seven kata are:

1. **Intake:** classify the skill, choose rigor tier, design scenarios, and
   pre-write observable pass criteria.
2. **Baseline (RED):** run training scenarios without the new skill and record
   the failure modes the skill must close.
3. **Write (GREEN):** author or edit the skill to address those observed
   failures.
4. **Pressure-test (REFACTOR):** rerun training scenarios with the skill,
   score them against the same criteria, make bounded edits, and record rejected
   fixes.
5. **Graduation:** run held-out scenarios once to check generalization.
6. **Trigger eval:** test whether the skill description routes correctly
   against realistic positive and near-miss negative prompts.
7. **Package & record:** package the skill, preserve run outputs, and write the
   dojo record.

## Comparison summary

### What Dojo did better

- Designed scenarios before writing the skill.
- Treated baseline failure as curriculum, not as decoration.
- Logged exact observed loopholes and the edits that closed them.
- Kept held-out graduation separate from training scenarios.
- Ran a trigger collision matrix against adjacent installed skills.
- Preserved rejected fixes so future sessions do not repeat dead ends.
- Let the James skill evolve from actual failure modes instead of generic
  skill-writing advice.

### What Anthropic's flow did better

- Created a consistent workspace shape for eval iterations.
- Produced `evals.json`, per-eval metadata, grading JSON, `benchmark.json`,
  `benchmark.md`, and a static review page.
- Made human review of outputs a first-class step.
- Provided reusable grader, analyzer, comparator, packaging, and description
  optimization scripts.
- Treated trigger descriptions as optimizable objects with train/test splits.

### The important failure

The Anthropic-produced James eval looked formally successful but was not
discriminating:

- with-skill pass rate: `100%`
- without-skill pass rate: `100%`
- delta: `+0.00`
- timing data: unavailable, recorded as zero
- token data: approximated from output characters
- baseline prompts still mentioned James, so baseline agents produced
  James-like review logs without needing the skill

That benchmark is valuable as a warning. It proves the harness can produce
nice artifacts while failing to prove improvement.

## Core principle

Dojo may borrow workbench ergonomics, but it must not borrow false confidence.

Evidence labels:

- **Behavior-improving:** baseline failed an observable criterion and the
  skilled run passed it, or a documented historical failure was reproduced and
  closed.
- **Regression-protecting:** both baseline and skilled runs pass, but the eval
  is still useful to prevent future breakage.
- **Non-discriminating:** both baseline and skilled runs pass and no historical
  failure is being protected. This cannot be used as evidence that the skill
  helped.
- **Contaminated:** baseline or held-out runs saw skill instructions, scenario
  answers, private chat context, or task wording that smuggled in the target
  behavior.
- **Contaminated qualifier:** if the contamination affects only part of the run,
  record the evidence label as `contaminated` and add `qualifier: partial`.
- **Unavailable metric:** timing, token, cost, or other quantitative data was
  not captured from the runtime and must not be interpreted.

## Proposed shape

### V0: Eval hygiene and report discipline

Update Dojo's instructions and references so every run can classify its own
evidence quality.

Add to kata 1:

- Each scenario declares whether it is expected to be
  `behavior-improving`, `regression-protecting`, or exploratory.
- Each criterion is observable as yes/no from run output or transcript.
- If a prompt names the new skill or its expected behavior, it must explain why
  that is not contaminating the baseline. If it cannot, rewrite the prompt.

Add to kata 2:

- Baseline runs must not receive the target skill, the target skill's
  instructions, or scenario answer keys.
- If the baseline passes every criterion, Dojo must decide whether the scenario
  is regression-protecting or non-discriminating.
- A non-discriminating baseline cannot justify a skill edit by itself.

Add to kata 4 and kata 5:

- Skilled runs inherit the same criteria as the baseline.
- Report the result as a behavior delta, not only a pass/fail.
- If a metric is unavailable, write `unavailable`, not `0`, unless zero is the
  real measured value.

Add to kata 7:

- The dojo record includes an **Evidence Quality** section summarizing:
  behavior-improving scenarios, regression-protecting scenarios,
  non-discriminating scenarios, contaminated runs, unavailable metrics, and
  claims that require human qualitative judgment.

### V1: Static evidence pack

Add an optional static report pack beside the existing dojo record. This should
not replace the markdown-first record; it should make inspection easier.

Suggested artifact shape:

```text
~/.limitless/dojo/<repo-slug>/<skill>/
  <skill>-scenarios.md
  <skill>-record.md
  <skill>-runs/
    iteration-001/
      evals.json
      benchmark.json
      benchmark.md
      review.html
      eval-001-<slug>/
        baseline/
          outputs/
          grading.json
          timing.json
        skilled/
          outputs/
          grading.json
          timing.json
```

The static report should show:

- scenario prompt and expected evidence label
- baseline output
- skilled output
- pass/fail per criterion
- behavior delta
- contamination notes
- unavailable metrics
- human review notes

If a run is non-discriminating, the report should make that visually and
textually obvious. No green dashboard theater.

### V2: Description optimization without routing slop

Borrow the idea of optimizing skill descriptions, but keep Dojo's collision
discipline.

Process:

- Generate 12-20 realistic trigger prompts.
- Include positive prompts, near-miss negatives, and explicit competitor-skill
  prompts.
- Split into train and held-out sets.
- Run at least two routing judges over the full installed-skill description
  list.
- Select descriptions by held-out trigger accuracy and collision avoidance, not
  training score alone.
- Preserve rejected descriptions and why they failed.

This can be manual first. A script is useful only if it preserves the full
prompt list, judge outputs, and rejected-description trail.

## Implementation options

### Option A: Documentation-only V0

Edit Dojo's `SKILL.md` and references to add evidence labels, baseline
contamination checks, and Evidence Quality in the record template.

Good:

- Fast.
- No new runtime surface.
- Immediately improves the next skill run.

Bad:

- Still manual.
- No nice viewer or structured benchmark artifacts.

### Option B: Full Anthropic-style workbench

Port the workspace schema, benchmark aggregation, static viewer, and packaging
scripts into Limitless.

Good:

- Best inspection ergonomics.
- Makes human review easier.
- Creates comparable artifacts across skill runs.

Bad:

- Easy to overbuild.
- Scripts can create false authority if eval quality labels are weak.
- May distract from the actual skill behavior.

### Option C: Split wedge

Do V0 now. Then add only the minimal V1 static evidence pack once two more
Dojo runs show the same reporting friction.

Good:

- Keeps Dojo truthful now.
- Defers tooling until there is enough repeated pain to justify it.
- Lets the James and Hivemind runs become fixtures for the eventual reporter.

Bad:

- Human review remains markdown-heavy for a bit longer.

**Recommendation: Option C.**

## First implementation slice

Target files:

- `plugins/limitless/skills/dojo/SKILL.md`
- `plugins/limitless/skills/dojo/references/pressure-testing.md`
- `plugins/limitless/skills/dojo/references/packaging.md`

Changes:

1. Add the five evidence labels to the measurability rule.
2. Add baseline contamination checks to kata 1 and kata 2.
3. Add non-discriminating scenario handling to kata 2.
4. Add unavailable-metric wording to kata 4, kata 5, and kata 7.
5. Add an Evidence Quality section to the dojo record template.
6. Add a note that Anthropic-style benchmark artifacts are optional helpers,
   not proof by themselves.

Patch-level guidance:

- In `SKILL.md`, extend the existing measurability rule with the evidence labels
  above and say that a run's label is part of the result, not commentary.
- In `SKILL.md` kata 1, add the scenario-label requirement before the scenario
  battery is persisted.
- In `SKILL.md` kata 2, add the baseline contamination rule immediately before
  the baseline run instruction, then add the non-discriminating/regression
  decision immediately after baseline scoring.
- In `SKILL.md` kata 4 and kata 5, add behavior-delta reporting and
  unavailable-metric handling wherever run scoring is described.
- In `SKILL.md` kata 7, require the dojo record to include the Evidence Quality
  section shown below.
- In `references/pressure-testing.md`, add examples of clean baseline prompts
  versus contaminated baseline prompts.
- In `references/packaging.md`, add the Evidence Quality section to the record
  template and mention optional benchmark/report artifacts as helpers.

Record-template addition:

```md
## Evidence Quality

| Scenario | Label | Baseline Result | Skilled Result | Delta | Contamination | Unavailable Metrics | Claim Allowed |
|---|---|---|---|---|---|---|---|
| S1 | behavior-improving | failed C1, C3 | passed all | +2 criteria | none | timing | skill improved this behavior |
| S2 | regression-protecting | passed all | passed all | no delta | none | none | regression coverage only |
| S3 | contaminated | passed all | passed all | no trusted delta | partial: baseline prompt named target behavior | tokens | no improvement claim |

Notes:
- `Label` must be one of `behavior-improving`,
  `regression-protecting`, `non-discriminating`, `contaminated`, or
  `unavailable-metric`.
- `Contamination` may use qualifiers such as `partial` or `severe`, but the
  base label remains `contaminated`.
- `Claim Allowed` is the plain-language claim the run is allowed to support.
```

Trigger eval pass condition:

- Build a 10-20 prompt matrix with positive prompts, near-miss negatives, and
  competitor prompts.
- Give routing judges the full installed-skill description list that is relevant
  to the skill's neighborhood.
- Run at least two independent judge passes.
- A changed description passes only if every positive routes to the intended
  skill in both runs and no negative or competitor prompt routes to the intended
  skill in either run.
- If a prompt is declared ambiguous before judging, list the acceptable answers
  up front and score only against that declared set.

V1 minimum JSON fields:

`evals.json`:

```json
{
  "skill_name": "example-skill",
  "iteration": "001",
  "evals": [
    {
      "id": "S1",
      "name": "open-repo-context-leak",
      "prompt": "self-contained user prompt",
      "expected_label": "behavior-improving",
      "criteria": [
        {"id": "C1", "text": "observable yes/no criterion"}
      ],
      "files": []
    }
  ]
}
```

`grading.json`:

```json
{
  "run_id": "S1-skilled",
  "configuration": "baseline|skilled|old-skill",
  "criteria": [
    {"id": "C1", "passed": true, "evidence": "short evidence quote or path"}
  ],
  "label": "behavior-improving",
  "contamination": {"status": "none|partial|severe", "evidence": ""},
  "human_judgment_required": []
}
```

`timing.json`:

```json
{
  "duration_ms": "unavailable",
  "total_tokens": "unavailable",
  "cost": "unavailable",
  "measurement_note": "runtime did not provide these metrics"
}
```

`benchmark.json`:

```json
{
  "skill_name": "example-skill",
  "iteration": "001",
  "summary": {
    "behavior_improving": 1,
    "regression_protecting": 1,
    "non_discriminating": 1,
    "contaminated": 1
  },
  "evals": [
    {
      "id": "S1",
      "baseline_passed": 1,
      "baseline_total": 3,
      "skilled_passed": 3,
      "skilled_total": 3,
      "delta": "+2 criteria",
      "evidence_label": "behavior-improving",
      "claim_allowed": "skill improved this behavior"
    }
  ]
}
```

These schemas are intentionally smaller than Anthropic's. They are sufficient
for V1 static reports and should not block V0.

Validation:

- Update the Dojo record template.
- Use the Anthropic-produced James eval as a paper fixture: it should be
  classified as `contaminated` with `qualifier: partial`, and as
  `non-discriminating` for improvement claims. Relevant fixture facts:
  with-skill pass rate `100%`, without-skill pass rate `100%`, delta `+0.00`,
  baseline prompts still named James, timing was unavailable but recorded as
  zero, and token counts were approximated from output character counts.
- Use the Dojo James run as a paper fixture: its pressure runs should be
  classified as behavior-improving because they start from observed failures
  and close specific loopholes. Relevant fixture facts: pressure S1 improved
  from `2/10` to `9/10`, pressure S2 from `7/10` to `9/10`, pressure S3 from
  `3/10` to `8/10` to `9/10`; the recorded loopholes included evidence-boundary
  contamination, missing allowed-context envelopes, score-chasing, and
  prior-review fact contamination on resumed James threads.
- Run Dojo's trigger eval if the description changes.
- Run James on this concept before implementing.

## Non-goals

- Do not replace Dojo's seven kata.
- Do not require an HTML viewer for every skill edit.
- Do not pretend subjective output taste is a scalar benchmark.
- Do not count a clean benchmark table as evidence if the baseline also passes.
- Do not port Anthropic's flow wholesale.
- Do not add a persistent Skill IDE or dashboard in this slice.

## Open questions

- Should V1 reuse Anthropic's JSON schema directly, or define a smaller
  Limitless schema with only the fields Dojo actually trusts?
- Should static reports live only under `~/.limitless/dojo/`, or should curated
  review pages sometimes be copied into project docs after leak-checking?
- Is description optimization worth scripting before we have more trigger-drift
  failures, or should it remain a manual trigger-eval recipe for now?

## Decision rule

Implement V0 if James confirms the concept is self-contained enough and the
first slice is narrow. Do not start V1 until at least two future Dojo runs show
that markdown-only evidence review is slowing decisions down.
