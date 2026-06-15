# Skill Spec-Kit vs Dojo and Anthropic Skill Creator

*Review date: 2026-06-14*

## Verdict

The `skill-dev` Skill Spec-Kit is the most ambitious of the three systems. It
is not merely another skill creator. It is a framework for designing **systems
of composable skills**, with explicit decomposition, contracts, surface
prototypes, derivation, observation, and path comparison.

My preference after reading all three:

1. **Use Skill Spec-Kit as the long-term architecture.** It has the right
   higher-order idea: SKILL.md should increasingly be a compiled artifact from
   richer behavioral and contract evidence, not the only source of truth.
2. **Use Dojo as the trust gate.** Skill Spec-Kit's outputs should not be
   considered shipped until they pass Dojo-style clean baselines, pressure
   tests, held-outs, trigger-collision checks, and contamination review.
3. **Use Anthropic's skill creator as the instrumentation layer.** Its
   workspaces, `grading.json`, `benchmark.json`, review viewer, grader,
   comparator, analyzer, and description optimizer are exactly the machinery
   Skill Spec-Kit needs to become real.

So the best answer is not "Dojo vs Anthropic vs Skill Spec-Kit." The best shape
is:

```text
Skill Spec-Kit = architecture and authoring pipeline
Dojo = epistemic discipline and graduation gate
Anthropic creator = eval harness and human review UI
```

If forced to choose one as-is for creating a single important skill today, I
still prefer **Dojo**. If choosing the better foundation for a future skill
development IDE, I prefer **Skill Spec-Kit**, but only after importing Dojo's
suspicion and Anthropic's instrumentation.

## Sources Reviewed

Dojo / Limitless:

- `plugins/limitless/skills/dojo/SKILL.md`
- `plugins/limitless/skills/dojo/references/pressure-testing.md`
- `plugins/limitless/skills/dojo/references/trigger-evals.md`
- `docs/dojo/dojo-vs-anthropic-skill-creator.md`
- `docs/dojo/james-record.md`
- `docs/dojo/james-scenarios.md`

Anthropic skill creator:

- `/home/pyro/projects/agents/skill-test/.agents/skills/anthropic-skill-creator/SKILL.md`
- `/home/pyro/projects/agents/skill-test/.agents/skills/anthropic-skill-creator/agents/{grader,comparator,analyzer}.md`
- `/home/pyro/projects/agents/skill-test/.agents/skills/anthropic-skill-creator/references/schemas.md`
- `/home/pyro/projects/agents/skill-test/.agents/skills/james-workspace/iteration-1/benchmark.json`
- `/home/pyro/projects/agents/skill-test/.agents/skills/james-workspace/iteration-1/benchmark.md`

Skill Spec-Kit:

- `/home/pyro/projects/skill-dev/CLAUDE.md`
- `/home/pyro/projects/skill-dev/docs/brainstorms/2026-04-04-skill-spec-kit-requirements.md`
- `/home/pyro/projects/skill-dev/docs/ideation/2026-04-04-skill-dev-tooling-ideation.md`
- `/home/pyro/projects/skill-dev/docs/plans/2026-04-04-001-feat-skill-spec-kit-plan.md`
- `/home/pyro/projects/skill-dev/docs/plans/ARCHITECTURE-REVIEW.md`
- `/home/pyro/projects/skill-dev/docs/test-report.md`
- `/home/pyro/projects/skill-dev/docs/learnings.md`
- `/home/pyro/projects/skill-dev/.claude/skills/skill-spec-kit/`
- `/home/pyro/projects/skill-dev/skill-surface-prototyper-workspace/iteration-1/benchmark.json`
- `/home/pyro/projects/skill-dev/end-to-end-workspace/outputs/`

Evidence note: the Skill Spec-Kit repo has a `.codies-memory` marker, but
`codies-memory boot --agent Codie --working-dir /home/pyro/projects/skill-dev`
resolved global-only in this session. I treated the live repo files as source
of truth.

## What Skill Spec-Kit Adds

### 1. It moves from single-skill authoring to skill-system design

Dojo and Anthropic's creator mostly answer:

> How do we create or improve this skill?

Skill Spec-Kit answers:

> What skill system should exist, how should it decompose, how do its skills
> compose, and which development path produces better behavior?

That is a higher-level problem. The framework has a decomposer, dependency
tables, upstream/downstream handoffs, and explicit integration checks. Neither
Dojo nor Anthropic has a first-class multi-skill architecture step.

### 2. It treats SKILL.md as generated from richer evidence

This is the strongest conceptual move in `skill-dev`.

The ideation doc says the future artifact is not just a markdown prompt, but a
versioned, testable policy package. Skill Spec-Kit makes that concrete with two
paths:

- **Contract-first:** extended frontmatter and I/O contracts become prose.
- **Surface-first:** converged simulated behavior becomes contracts and prose.

Dojo currently writes SKILL.md directly after observing failures. Anthropic also
mostly writes SKILL.md directly, then evaluates it. Skill Spec-Kit introduces an
intermediate design layer that can be inspected, revised, and compared.

That is correct for larger systems.

### 3. It captures recognition-over-generation better than both

Dojo has recognition in the form of baseline/pressure feedback. Anthropic has
human review UI. But Skill Spec-Kit's Path B is the cleanest embodiment:

1. Generate a simulated transcript.
2. Extract 2-3 behavioral decision points.
3. Offer multiple-choice alternatives.
4. Let the human recognize the right behavior.
5. Preserve selections in a decision log.
6. Derive invariants and "Don't" sections from selected and rejected choices.

The v2 test report shows this is not just aesthetic. The with-skill surface
prototyper scored 100% across three evals, while baselines averaged 82%, and
the consistent baseline failure was convergence tracking. The model could
generate good one-shot prototypes without the skill; the skill added the
iterative decision loop.

That is a real contribution.

### 4. It has a stronger theory of skill contracts

Skill Spec-Kit's extended frontmatter gives language for:

- trigger examples
- preconditions
- I/O contracts
- postconditions
- hard invariants
- compatibility metadata

Dojo has process evidence, but not a contract schema. Anthropic has eval
schemas, but not a first-class skill contract representation. Skill Spec-Kit
fills that gap.

### 5. It preserves the observer-effect insight

Skill Spec-Kit explicitly says not to instrument the skill under test. The
observer runs after execution, in a separate context, and grades completed
transcripts and outputs.

That aligns strongly with Dojo's clean-baseline instincts. It is also a useful
correction to naive "just add logging to the skill" eval approaches.

## Where Skill Spec-Kit Is Weaker

### 1. It does not have Dojo's graduation discipline

Skill Spec-Kit has validation and observation, but it does not yet have the
full Dojo kata:

- baseline failure as curriculum
- bounded edit attribution
- adversarial pressure variants
- held-out graduation
- burned-holdout rules
- installed-skill collision matrices
- rejected-fix tables
- explicit "draft vs dojo-tested" distinction

Without those, Skill Spec-Kit can produce impressive artifacts that are not yet
trustworthy.

### 2. It inherits some benchmark-integrity problems

The Skill Spec-Kit evidence is stronger than the Anthropic James run in one
important way: its JSON benchmark does show a discriminating delta
(`with_skill` 100%, `without_skill` 82%).

But it also has an evidence-integrity problem:

- `skill-surface-prototyper-workspace/iteration-1/benchmark.json` reports the
  meaningful 100% vs 82% result.
- `skill-surface-prototyper-workspace/iteration-1/benchmark.md` reports 0% vs
  0%, zero time, and zero tokens.

That mismatch would fail a Dojo evidence gate. Human-readable summaries cannot
silently drift from machine-readable benchmark truth.

### 3. It blurs "metadata exists" with "eval exists"

I ran:

```bash
python /home/pyro/projects/skill-dev/.claude/skills/skill-spec-kit/scripts/validate_frontmatter.py --batch /home/pyro/projects/skill-dev/.claude/skills/skill-spec-kit --recursive --json
```

All six Skill Spec-Kit skills validated. Good.

But the validator reported `compatibility` as an active eval layer, while the
observer docs say compatibility evals are future/deferred. That is a small but
important wording bug. It should distinguish:

- `compatibility metadata present`
- `compatibility eval available`
- `compatibility eval executed`

Dojo's "do not pretend-measure" rule applies here.

### 4. It still lacks a robust integration test

The framework has an integration-check phase and a path comparison template
with smoke-test tables. Good direction.

But compared with Dojo, it lacks a hard gate that says:

- run a realistic multi-skill chain
- preserve transcript and outputs
- grade handoff contract compliance
- include a held-out chain scenario
- fail if dispatcher ambiguity or handoff mismatch appears

Skill Spec-Kit is explicitly about skill systems. Its integration evidence
needs to be as strong as its single-skill evidence.

### 5. It is older and Claude-shaped

The repo assumes Claude Code/Cowork and uses Claude tool names. That is fine
historically, but a future Limitless/Dojo version should normalize the method
for Codex, Claude, and other agent hosts:

- tool mapping
- subagent availability
- trigger eval mechanism
- skill loader behavior
- model/version compatibility

This matters because Skill Spec-Kit's own thesis says version-mismatched
guidance can degrade skill performance.

## Three-Way Comparison

| Dimension | Dojo | Anthropic Skill Creator | Skill Spec-Kit | Best Current Owner |
|---|---|---|---|---|
| Single-skill creation | Strong, rigorous | Strong, user-friendly | Indirect | Dojo or Anthropic |
| Multi-skill systems | Not first-class | Not first-class | First-class | Skill Spec-Kit |
| Baseline rigor | Strongest | Good but contamination-prone | Present in tests, not core discipline | Dojo |
| Human review UI | Weak | Strongest | Some reports/templates | Anthropic |
| Contract representation | Weak/implicit | Weak/implicit | Strongest | Skill Spec-Kit |
| Surface-first authoring | Implicit | Not central | Strongest | Skill Spec-Kit |
| Trigger evals | Competitive routing matrix | Automated description optimizer | Frontmatter examples + `claude -p` script | Combine all three |
| Held-outs | Mandatory | Possible, not central | Not central | Dojo |
| Integration testing | Not central | Not central | Designed in, needs hardening | Skill Spec-Kit + Dojo |
| Evidence packaging | Markdown record | Structured workspace + viewer | Mixed, some drift | Anthropic + Dojo |
| Anti-fake-measurement posture | Strongest | Moderate | Moderate | Dojo |

## What Skill Spec-Kit Should Borrow From Dojo

### 1. A graduation gate after observation

Add a phase after Skill Spec-Kit's observer:

```text
Phase 5B: Graduation
- clean baseline status
- pressure scenario
- held-out scenario
- trigger collision matrix
- known limitations
- pass/fail verdict
```

The observer can say "this execution looks strong." Dojo should decide whether
the skill has earned shipping trust.

### 2. Bounded edit attribution

Skill Spec-Kit has iterative paths, but it does not require one loophole, one
edit, one rerun. Add this when observer/benchmark feedback causes revisions.

Otherwise a failed skill can get a broad rewrite and nobody knows which change
fixed the behavior.

### 3. Baseline contamination labels

Every comparison report should include:

- `baseline_clean: yes/no`
- `contamination_risk: none/partial/high`
- `prompt_mentions_skill_name: yes/no`
- `prompt_leaks_signature_output_format: yes/no`

This directly protects against the Anthropic James failure mode.

### 4. Held-out chain tests

For multi-skill systems, held-outs should include at least one chain-level
scenario that was not used during decomposition or path iteration.

Passing individual skills is not enough. A skill system can fail at the seams.

### 5. Rejected-fix tables

Skill Spec-Kit should record not only what changed, but what attempted
methodological or skill edits did not survive. That prevents future sessions
from rediscovering dead ends.

## What Skill Spec-Kit Should Borrow From Anthropic

### 1. Standard workspace and benchmark schemas

Skill Spec-Kit should adopt Anthropic-style structured evidence:

- `evals.json`
- `eval_metadata.json`
- `grading.json`
- `timing.json`
- `benchmark.json`
- `review.html`

Its current evidence is halfway there, but the broken `benchmark.md` proves it
needs a single generated source of truth or consistency check.

### 2. Static review viewer

Path A vs Path B comparison needs a human review surface. A Markdown template
is not enough once outputs include multiple transcripts, generated skills,
grader results, and benchmark deltas.

The viewer should support:

- Path A output
- Path B output
- derived contracts
- trajectory grades
- trigger results
- integration-chain results
- human notes

### 3. Grader/comparator/analyzer roles

Skill Spec-Kit has a trajectory grader, but it should also adopt:

- **Grader:** expectation pass/fail with evidence.
- **Blind Comparator:** Path A vs Path B output quality without knowing which
  path produced which.
- **Analyzer:** post-hoc explanation of why one path won and what the losing
  path should borrow.

That would make its path comparison more trustworthy.

### 4. Description optimization, but after collision testing

Skill Spec-Kit already has trigger examples and a trigger eval script. Borrow
Anthropic's train/held-out repeated-run optimizer for descriptions, but finish
with Dojo's installed-skill collision matrix.

This avoids optimizing recall by making the skill description too grabby.

## What Dojo Should Borrow From Skill Spec-Kit

### 1. Surface-first transcript prototyping

Dojo's kata could add a pre-SKILL.md design mode:

```text
Generate 2-3 plausible execution transcripts.
Extract behavioral decisions.
Have the human choose between alternatives.
Derive invariants and prose from the chosen transcript.
Then begin Dojo baseline/pressure testing.
```

This would reduce the chance that Dojo starts testing the wrong skill shape.

### 2. Decision logs

Skill Spec-Kit's decision log is excellent. Dojo records failures and fixes,
but it does not always preserve the human's selected behavioral tradeoffs.

Dojo should add:

- selected alternatives
- rejected alternatives
- rationale
- where each selected decision appears in SKILL.md prose
- which selected decisions become hard invariants

### 3. Extended frontmatter as optional contract metadata

Dojo should not make every skill heavy. But for discipline and technique
skills, optional contract fields would help:

- trigger examples
- negative examples
- preconditions
- I/O outputs
- hard invariants
- compatibility notes

This gives graders and future agents more structure without forcing a schema on
every reference skill.

### 4. Round-trip fidelity checks

Skill Spec-Kit's end-to-end `validation.json` includes a useful check: decision
log entries reflected in prose, invariants, and "Don't" sections.

Dojo should add a similar check:

> Every failure mode found in baseline/pressure testing must map to a concrete
> instruction, invariant, limitation, or rejected-fix note.

This would make Dojo records more mechanically auditable.

## What Anthropic Should Borrow From Skill Spec-Kit

### 1. Multi-skill decomposition

Anthropic's creator can turn a request into a skill. It does not first ask
whether the request should become several skills, a script, an external tool,
or a system.

Skill Spec-Kit's decomposer is the missing first step for broad requests.

### 2. Surface-first before writing prose

Anthropic's creator asks intent questions and writes a draft. Skill Spec-Kit
shows a more humane path for fuzzy skills: prototype the behavior first, then
derive prose.

This is especially valuable when the user cannot state requirements, but can
recognize good behavior when shown options.

### 3. Contract metadata

Anthropic has eval schemas, not skill contracts. Adding optional contract
metadata would make its generated skills easier to evaluate, compare, and
evolve.

## Recommended Unified Framework

The unified workflow should look like this:

1. **Research / prior art.**
   Gather enough context to avoid prototyping the wrong thing.

2. **Decompose.**
   Use Skill Spec-Kit's decomposer to decide whether this is one skill, several
   skills, scripts, external tools, or a mix.

3. **Human boundary gate.**
   Use a Dojo-style decomposition rubric: focused, testable, no cycles,
   clean handoffs, no deterministic work mislabeled as skills.

4. **Prototype behavior.**
   For fuzzy skills, use Skill Spec-Kit's surface-first transcript and
   multiple-choice decision loop. For crisp skills, contract-first is fine.

5. **Derive contract and SKILL.md.**
   Use extended frontmatter plus prose, with decision-log traceability.

6. **Run Anthropic-style eval harness.**
   Store structured runs, grade outputs, aggregate benchmarks, and generate a
   static review page.

7. **Run Dojo graduation.**
   Clean baseline, pressure run, held-out run, trigger collision matrix,
   rejected-fix table, known limitations.

8. **Integration test the system.**
   For multi-skill systems, run at least one held-out chain scenario and grade
   handoff compliance.

9. **Package with evidence.**
   Ship SKILL.md plus references/scripts/assets, but preserve the richer source
   evidence: contracts, decision logs, benchmarks, reviews, trigger matrices,
   and graduation record.

## Concrete Fixes For Skill Spec-Kit

### P0: Fix benchmark summary drift

Regenerate `benchmark.md` from `benchmark.json` or delete the stale markdown
summary. The current 0%/0-token markdown summary contradicts the meaningful
JSON result.

Acceptance check:

- `benchmark.md` pass-rate/time/token values exactly match `benchmark.json`
  within rounding.

### P0: Separate metadata activation from executed evals

Change validation language from `active_eval_layers` to something like:

```json
{
  "metadata_present": ["trigger", "trajectory", "compatibility"],
  "evals_available": ["trigger", "trajectory"],
  "evals_deferred": ["compatibility"]
}
```

Acceptance check:

- Compatibility metadata no longer implies compatibility evals were run.

### P1: Add Dojo-style contamination fields

Every benchmark and path comparison should record baseline cleanliness.

Acceptance check:

- Reports fail validation if baseline prompts name the skill under test unless
  the run is explicitly marked contaminated.

### P1: Add chain-level held-outs

Skill Spec-Kit is about systems; it needs system-level held-outs.

Acceptance check:

- Every multi-skill output has at least one unseen chain scenario with preserved
  transcript, outputs, grader results, and handoff verdict.

### P1: Add a static path-comparison viewer

The path comparison template is good, but the real workflow needs a review UI.

Acceptance check:

- A generated `review.html` shows Path A vs Path B outputs, contracts, grades,
  benchmarks, chain tests, and human feedback fields.

## Bottom Line

Skill Spec-Kit is the best conceptual architecture. Dojo is the best truth
discipline. Anthropic's creator is the best lab instrumentation.

The synthesis is obvious and good:

- Let Skill Spec-Kit design the skill system.
- Let Anthropic-style tooling make the evidence inspectable.
- Let Dojo decide whether the result has earned trust.

That combined system is much stronger than any of the three alone.
