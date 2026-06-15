# Dojo vs Anthropic Skill Creator

*Review date: 2026-06-14*

## Verdict

I prefer **Dojo** as the governing method for creating durable skills.

Dojo is stricter about the thing that matters most: a skill is not a nice
instruction file, it is a claim about future agent behavior. Its workflow is
built to prevent false confidence: baseline first, observable process criteria,
bounded edits, held-out graduation, and trigger-collision tests. The James Dojo
run is imperfect, but it leaves a clear audit trail of what failed, what was
fixed, what remained contaminated, and what passed.

The Anthropic skill creator is better as an **eval product**. It has stronger
workspace structure, scripts, benchmark aggregation, grading schemas, human
review UI, and trigger-description optimization. It makes the run inspectable
by a human in a way Dojo currently does only through Markdown records and raw
folders.

So the answer is:

- Keep Dojo's philosophy and pass/fail discipline.
- Borrow Anthropic's harness, schemas, viewer, and automated description evals.
- Do not borrow Anthropic's willingness to let aggregate metrics look decisive
  when the control is contaminated.

The Anthropic James run itself proves the danger: its benchmark reports 100%
pass rate with and without the skill because the baseline prompts still named
James. The run correctly notes that contamination, but the headline metric is
therefore not discriminating. Dojo's more suspicious posture is the right
default.

## Sources Reviewed

Dojo:

- `plugins/limitless/skills/dojo/SKILL.md`
- `plugins/limitless/skills/dojo/references/pressure-testing.md`
- `plugins/limitless/skills/dojo/references/trigger-evals.md`
- `plugins/limitless/skills/dojo/references/packaging.md`
- `docs/dojo/james-scenarios.md`
- `docs/dojo/james-record.md`
- `docs/dojo/james-runs/`
- `plugins/limitless/skills/james/SKILL.md`

Anthropic skill creator:

- `/home/pyro/projects/agents/skill-test/.agents/skills/anthropic-skill-creator/SKILL.md`
- `/home/pyro/projects/agents/skill-test/.agents/skills/anthropic-skill-creator/agents/{grader,comparator,analyzer}.md`
- `/home/pyro/projects/agents/skill-test/.agents/skills/anthropic-skill-creator/references/schemas.md`
- `/home/pyro/projects/agents/skill-test/.agents/skills/anthropic-skill-creator/scripts/`
- `/home/pyro/projects/agents/skill-test/.agents/skills/james/SKILL.md`
- `/home/pyro/projects/agents/skill-test/.agents/skills/james/evals/evals.json`
- `/home/pyro/projects/agents/skill-test/.agents/skills/james-workspace/`

Evidence boundary: the Anthropic source paths above are provenance for this
review, not required runtime context for future Dojo work inside this repo. The
recommendations below embed the findings that matter: Anthropic has stronger
evaluation infrastructure, its James benchmark was baseline-contaminated, and
its trigger-description optimizer is worth adapting only behind Dojo's
collision checks.

## Comparison

| Dimension | Dojo | Anthropic skill creator | Winner |
|---|---|---|---|
| Core philosophy | "No skill ships on vibes"; skills earn trust through scenario pressure. | Draft, run, benchmark, show user, iterate. More flexible and user-friendly. | Dojo |
| Failure model | Explicitly looks for loopholes, contamination, overfitting, and trigger collisions. | Strong eval loop, but easier to let a weak benchmark look authoritative. | Dojo |
| Test design | Training scenarios, held-outs, adversarial variants for discipline skills, y/n observable process checks. | 2-3 realistic prompts first, then assertions while runs execute. Stronger machinery, weaker default rigor. | Dojo |
| Baseline discipline | Baseline before skill, and baseline failure must become the skill's curriculum. | With-skill and baseline launched in the same turn; good for comparability, but can contaminate if prompts name the skill. | Dojo, with Anthropic borrow |
| Iteration discipline | Bounded edits: one loophole, one targeted edit, rerun that scenario. | Human feedback and benchmark-driven iteration; encourages generalizing from feedback and avoiding overfit. | Tie |
| Human review UX | Markdown records and raw run folders. Useful, but manual. | Static/browser review UI with outputs, grades, feedback, benchmark tab. Much better. | Anthropic |
| Metrics and schemas | Mostly Markdown tables and process notes. Trigger eval is exact-match. | `evals.json`, `eval_metadata.json`, `grading.json`, `timing.json`, `benchmark.json`, aggregation scripts. | Anthropic |
| Trigger testing | Competitive installed-skill matrix, positives and near-miss negatives, two routing judges. | Description optimizer with 20 queries, repeated runs, train/test split, best by held-out score. | Tie; combine them |
| Packaging | Clear Limitless conventions and frontmatter validation. | Package script and Claude.ai/Cowork adaptation notes. | Tie |
| Final artifact quality | The shipped James skill in `plugins/limitless` is sharper: persistent recipes, review chains, scope envelope, resumed James, hard loop cap. | The generated James skill is simpler and less operationally durable. | Dojo |

## What Dojo Does Better

### 1. It refuses fake measurement

Dojo's measurability rule is correct: if there is no scalar grader, do not
pretend there is one. Use observable process checks and exact trigger tests.

The Anthropic James run shows why this matters. Its `benchmark.md` says both
with-skill and without-skill got 100%, then correctly warns that the baseline
was contaminated because the prompt itself mentioned James. The aggregate
number looks clean; the evidence is not.

Dojo already has the better epistemic immune system here.

### 2. It treats baseline failure as curriculum

Dojo asks: what did the agent fail to do before the skill existed? That makes
the skill answer a real behavioral gap.

In the Dojo James record, the baseline failures became concrete curriculum:

- evidence-boundary discipline
- project-local context envelopes
- loop caps
- no score-chasing past the repeat limit
- no hidden memory or scenario leakage

That is stronger than merely checking whether a skilled output looks good.

### 3. It has better trigger-collision discipline

Dojo's trigger eval asks whether the new skill steals traffic from adjacent
skills. The James run's 14-prompt matrix explicitly tested collisions with
Dojo, surface-first-development, article-pack, hivemind, openai-docs,
humanizer, and ordinary code review.

That is the right shape. Skills fail not only by under-triggering, but by
silently grabbing work that belongs elsewhere.

### 4. Its final James skill is more mature

The Anthropic-generated James skill is solid as a first pass, but the Dojo /
Limitless version is more operational:

- explicit output root under `~/.limitless/james/`
- `recipe.md` and `chain.md`
- immutable saved reviews
- resumed James thread instead of fresh reviewer churn
- process memory separated from admissible evidence
- hard cap after three fix passes
- clearer not-for-code-review / not-for-article-editing boundaries

That is the kind of detail that matters when a skill is used repeatedly.

## What Anthropic Does Better

### 1. It has a real eval harness

Anthropic's creator has a coherent directory shape:

```text
<skill>-workspace/
  iteration-1/
    eval-.../
      eval_metadata.json
      with_skill/run-1/
      without_skill/run-1/
      old_skill/run-1/
```

It also has explicit schemas for:

- `evals.json`
- `eval_metadata.json`
- `grading.json`
- `metrics.json`
- `timing.json`
- `benchmark.json`

Dojo should not keep hand-rolling Markdown tables forever.

### 2. It puts outputs in front of the human

The review viewer is the best single artifact in the Anthropic workflow.
It gives the user:

- prompt
- output
- formal grades
- benchmark summary
- previous output on later iterations
- feedback capture

Dojo's raw run folders are honest but not pleasant. A human review surface
would make Dojo runs much easier to inspect and compare.

### 3. It grades evidence with a reusable contract

The grader agent contract is good: read transcript, inspect outputs, evaluate
each expectation, cite evidence, extract claims, and critique weak assertions.

Dojo currently encodes this spirit in prose, but Anthropic has a reusable
`grading.json` shape. Borrow the shape, not necessarily the exact grading
philosophy.

### 4. It has description optimization machinery

Anthropic's description optimizer is valuable:

- 20 realistic trigger queries
- should-trigger and should-not-trigger labels
- repeated runs per query
- train/held-out split
- improvement loop
- best description selected by held-out score

Dojo's trigger eval is more collision-aware, but it is manual. Anthropic's
optimizer could become an optional Dojo kata after the manual matrix passes.

### 5. It notices repeated scripts in transcripts

Anthropic tells the skill author to inspect transcripts for repeated work. If
every test run writes the same helper script, bundle it into `scripts/`.

Dojo says scripts should be rare, which is a good bias. But "rare" should not
mean "miss obvious reusable machinery." This is an easy borrow.

## What Dojo Should Borrow

### Borrow 1: A structured run workspace

Add a canonical Dojo workspace layout:

```text
~/.limitless/dojo/<repo>/<skill>/
  scenarios.md
  evals.json
  iterations/
    iteration-1/
      eval-<id>-<slug>/
        eval_metadata.json
        baseline/run-1/
        skilled/run-1/
        old_skill/run-1/
  benchmark.json
  review.html
  record.md
```

Keep Dojo's current Markdown record, but back it with machine-readable run
metadata.

### Borrow 2: `grading.json` and `benchmark.json`

Use Anthropic's schemas as the starting point, with Dojo-specific guardrails:

- `grading.json.expectations[]` keeps `text`, `passed`, `evidence`
- `benchmark.json` reports pass rates, timing, tokens, and tool calls
- every metric field must distinguish measured values from placeholders
- if timing is unavailable, store `measurement_unavailable: true`, not `0.0`
  as if zero runtime were real
- benchmark notes must call out contamination, nondiscriminating assertions,
  and weak controls

This gives Dojo better evidence without letting metrics become theater.

### Borrow 3: A contamination guard for baselines

Anthropic's "spawn with-skill and baseline in the same turn" is good, but
Dojo should wrap it with a baseline scrubber:

- baseline prompts must not name the skill under test
- baseline prompts must not quote the skill's signature output format unless
  the user's natural prompt really would
- baseline prompt paths should use neutral run labels, not `james`,
  `dojo`, or the skill name
- the record must explicitly say whether the baseline was clean,
  partially contaminated, or unusable

This borrow directly addresses the failure in the Anthropic James run.

### Borrow 4: Static HTML review viewer

Add a Dojo command or helper script that turns a run directory into a static
review page:

- eval prompt
- baseline output
- skilled output
- grader results
- benchmark notes
- known contamination warnings
- freeform human feedback export

Use Anthropic's `generate_review.py` as the reference pattern. Dojo does not
need prettier HTML; it needs a dependable human-inspection surface.

### Borrow 5: Reusable grader, comparator, and analyzer roles

Dojo should adopt three optional reviewers:

- **Grader:** pass/fail observable expectations with evidence.
- **Blind Comparator:** compare two outputs without knowing which run is
  skilled.
- **Analyzer:** explain why the winner won and what skill changes would likely
  change the result.

This would make Dojo's qualitative judgment more explicit without pretending
judgment is a scalar truth.

### Borrow 6: Description optimizer as "Kata 6B"

Dojo's current trigger eval should stay as the manual gate. After that, add an
optional automated pass:

1. Generate 20 realistic trigger and near-miss prompts.
2. Have the user review the set.
3. Run repeated trigger decisions.
4. Split train and hold-out.
5. Improve only the description.
6. Pick by hold-out score.
7. Re-run Dojo's competitive installed-skill matrix afterward.

The final re-run matters. Automated description optimization can improve recall
while creating new collisions.

### Borrow 7: Transcript-mining for scripts

Add this to Dojo kata 4 or 7:

> If two or more pressure/graduation runs independently create the same helper
> script, command sequence, template, or validation checklist, decide whether it
> belongs in `scripts/`, `assets/`, or `references/`.

This is a concrete way to turn observed repeated work into skill affordances.

### Borrow 8: User-facing eval explanation

Anthropic is better at telling a normal user what they are about to see. Dojo
can keep its sharper internal language, but should add a short operator-facing
summary before long eval runs:

- what scenarios are being run
- what counts as pass/fail
- what the human will review
- what the current limitations are

This would reduce the "mysterious research ritual" feel.

## What Dojo Should Not Borrow

### Do not let the user opt out too casually

Anthropic's skill creator is intentionally flexible: if the user wants to
"vibe," it can skip eval rigor. That is fine for Claude.ai convenience, but it
is not Dojo.

Dojo's whole value is that skills earn trust. If the user explicitly wants a
quick draft, call it a draft, not a dojo-tested skill.

### Do not trust aggregate pass rate without control quality

The Anthropic James benchmark says 100% vs 100%. That should never become a
green badge. Dojo should always require an "eval discriminates?" note:

- Did baseline fail where the skill should help?
- Did with-skill pass for the right reason?
- Are assertions hard to satisfy by surface compliance?
- Did the prompt leak the desired behavior?

### Do not replace held-outs with benchmark volume

More runs are useful, but held-out scenario design catches a different failure:
writing to the training set. Dojo's held-outs should remain mandatory.

### Do not optimize descriptions without a competitive skill landscape

Anthropic's description optimizer tests trigger/no-trigger. Dojo's matrix tests
ownership among installed skills. Both are needed. Optimizing against isolated
queries can make a description more aggressive and steal adjacent work.

## Recommended Integration Plan

1. **Add Dojo run schemas.**
   Start with `evals.json`, `eval_metadata.json`, `grading.json`, and
   `benchmark.json`. Keep the existing Markdown record as the human-readable
   summary.

2. **Add baseline contamination checks.**
   Make clean/contaminated/unusable baseline status a required field in the
   Dojo record.

3. **Port or adapt the static review viewer.**
   Generate `review.html` for Dojo iterations from the run directory. The
   first version can be ugly; the important part is side-by-side output +
   grades + feedback.

4. **Add an optional grader helper.**
   Grader outputs should be evidence-backed JSON. Dojo still decides whether
   the expectation set is meaningful.

5. **Add optional blind comparison.**
   Use it when two skill versions both pass structural checks but differ in
   output quality.

6. **Add Kata 6B for description optimization.**
   Use Anthropic's train/hold-out idea, but always finish by re-running Dojo's
   installed-skill collision matrix.

7. **Document "draft skill" vs "dojo-tested skill."**
   If the full kata are skipped, the artifact should be labeled honestly.

## Integration Quality Gates

If Dojo borrows the Anthropic machinery, the borrow is only successful when
these checks pass:

- Every run has a machine-readable `eval_metadata.json`, `grading.json`, and
  iteration-level `benchmark.json`.
- Every metric records whether it was measured, estimated, or unavailable.
- Baseline prompts are scrubbed so they do not name the skill under test or
  leak the skill's signature behavior.
- Each benchmark says whether the assertions discriminated between baseline
  and skilled runs.
- A static `review.html` is generated for human inspection before the skill is
  declared improved.
- Any automated description optimization is followed by Dojo's installed-skill
  trigger matrix, with near-miss negatives and collision reporting.
- The final Dojo record links the scenarios, run workspace, benchmark, review
  page, trigger matrix, known contamination, and known limitations.

## Bottom Line

Dojo is the better judge. Anthropic's creator is the better lab bench.

The next version of Dojo should not become softer or more benchmark-worshipful.
It should become more instrumented: structured workspaces, JSON evidence,
static review pages, reusable graders, blind comparison, and trigger
optimization. Keep the suspicion; add the machinery.
