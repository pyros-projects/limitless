# Dojo record — James

*Tier: discipline · 2026-06-13 · Codie*

## Baseline findings (RED)

| Scenario | Failure mode observed |
|---|---|
| S1 open-repo concept | Agent caught the leak, but loaded memory/review skills and read dojo scenarios before narrowing back to fixture scope. James needs explicit evidence-boundary discipline. |
| S2 post-release ideas | Agent used older same-project context correctly, but searched for James instructions and read scenario context. James needs an explicit allowed-context envelope. |
| S3 weak plan | Run was contaminated after the draft skill landed; useful loophole found: agent made a fourth fix pass to chase 9/10. |

## Loopholes closed

| # | Loophole | Edit that closed it |
|---|---|---|
| 1 | Skill initially said to spawn fresh reviewers, but Pyro clarified subsequent James calls should resume James. | Changed Review Loop to resume an existing James thread, spawn only if none exists, and reset the evidence boundary every call. |
| 2 | The first loop wording allowed score-chasing beyond the intended repeat limit. | Added a hard cap: after three fix passes, do not make a fourth edit; escalate remaining issues. |
| 3 | Resumed James could contaminate a new document review with prior document facts. | Added process-memory vs admissible-evidence rule to SKILL.md and reviewer prompt. |
| 4 | Reviewer could accidentally inspect dojo scenarios or skill docs while reviewing fixtures. | Added explicit refusal language to the reviewer prompt template. |

## Rejected fixes

| # | Attempted edit | Why it didn't survive |
|---|---|---|
| 1 | Fresh subagent for every re-review. | Rejected by Pyro: James should resume, not restart. Persistent reviewer identity is part of the intended behavior. |

## Graduation

| Holdout | Result | Notes |
|---|---|---|
| H1 explicit "James this" | Passed at 8/10 after one fix pass | Used resumed existing James subagent; target was inferred as the only plausible recent strategy doc. |
| H2 human-only PRD decisions | Passed at 7/10 after one fix pass | Correctly stopped at review-ready, not implementation-ready; missing target customer, pricing, and launch policy were escalated rather than invented. |

## Trigger matrix

| # | Prompt | Expected | Got (run 1 / run 2) | Pass |
|---|---|---|---|---|
| 1 | I wrote a PRD.md; James this before we ship. | james | james / james | yes |
| 2 | Can you run James on docs/concept.md? | james | james / james | yes |
| 3 | After that plan you wrote, ask James if it stands alone. | james | james / james | yes |
| 4 | Invoke James on post-release-ideas.md; it can use older project docs. | james | james / james | yes |
| 5 | James-review the design doc for hidden context. | james | james / james | yes |
| 6 | I edited the strategy doc, please do the James loop. | james | james / james | yes |
| 7 | $limitless:dojo build a new skill for reviewing docs. | dojo | dojo / dojo | yes |
| 8 | I have an idea for an app that tracks launch readiness; show me what it would look like. | surface-first-development | surface-first-development / surface-first-development | yes |
| 9 | Write a PRD for my launch board idea. | none | none / none | yes |
| 10 | Turn these notes into a Substack post. | article-pack | article-pack / article-pack | yes |
| 11 | What are people on Twitter saying about Fable5 today? | hivemind | hivemind / hivemind | yes |
| 12 | Look up the latest OpenAI API docs for Responses. | openai-docs | openai-docs / openai-docs | yes |
| 13 | Make this article sound less AI-generated. | humanizer | humanizer / humanizer | yes |
| 14 | Review this code diff for bugs and regressions. | none | none / none | yes |

Score: 14/14 twice · Collisions: none

## Known limitations

- Test agents could not spawn nested subagents, so pressure runs exercised the
  degraded James path. The live graduation run used the actual existing James
  subagent and verified resume behavior.
- File-age handling for chronological docs is specified, but the fixture used
  explicit task permission and identical mtimes; git-age edge cases still need a
  real repo case.
- James can pass below 9/10 when he explicitly says `Passed: yes`; this matches
  Pyro's rule that an explicit pass is sufficient even if the score is lower.
