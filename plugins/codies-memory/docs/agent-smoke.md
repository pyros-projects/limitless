# Codies Memory Agent Smoke

This is the non-deterministic companion to `scripts/smoke.sh`.

The shell smoke proves package behavior. The agent smoke checks whether a
fresh subagent can use the codies-memory skills correctly from the skill docs
alone, inside a temporary HOME, without touching the operator's real memory.
The required invariant is simple: the run did not touch real ~/.memory.

Use this when changing:

- `skills/memory-boot/SKILL.md`
- `skills/memory-help/SKILL.md`
- `skills/memory-capture/SKILL.md`
- `skills/memory-close-session/SKILL.md`
- project resolution, `_general`, boot, status, list, or session-close behavior

## Run Shape

Run with a fresh subagent. Do not reuse an agent that has seen the current
implementation discussion.

The subagent should use a temporary HOME by creating a wrapper named
`codies-memory` and putting it first on `PATH`. This lets the skill docs work
as written while routing every command into the temporary vault.

Do not use `scripts/smoke.sh` in this eval. That script tests the CLI directly;
this eval tests whether the skill instructions cause sane agent behavior.

Save the final prompt and result under a runtime evidence folder such as:

```text
~/.limitless/dojo/limitless/codies-memory-agent-smoke/
```

## Scenario Prompt

Copy this prompt into a fresh subagent:

```text
You are running a codies-memory agent smoke test.

Available context:
- Repository root: /home/pyro/projects/private/limitless
- Plugin root: /home/pyro/projects/private/limitless/plugins/codies-memory
- Real CLI binary: /home/pyro/projects/private/limitless/plugins/codies-memory/.venv/bin/codies-memory
- You may inspect local files in this repository.
- Do not use web search.
- Do not use QMD or any real memory store.
- Do not use scripts/smoke.sh. This is an agent-skill smoke, not the deterministic CLI smoke.

Isolation requirement:
Create a temporary HOME and a temporary bin directory. In the temporary bin
directory, create an executable wrapper named codies-memory that runs the real
CLI binary with HOME set to your temporary HOME. Prepend the temporary bin to
PATH and verify `which codies-memory` points at the wrapper. Every memory
operation must go through that wrapper. Do not touch real ~/.memory.

Skill documents to use:
- plugins/codies-memory/skills/memory-boot/SKILL.md
- plugins/codies-memory/skills/memory-help/SKILL.md
- plugins/codies-memory/skills/memory-capture/SKILL.md
- plugins/codies-memory/skills/memory-close-session/SKILL.md

Task:
Act like a zero-context agent using those skills.

1. Read the listed skill docs.
2. Set up codies-memory for agent name AgentSmoke in the temporary HOME.
3. Initialize a named project vault for a temporary project directory.
4. Use the memory-capture skill behavior to save one project-scoped observation
   in the named project.
5. Use the memory-capture / close-session behavior to save one session or note
   from a vault-less temporary directory, so it lands in `_general`.
6. Check normal vault-less reads via `status`, `list`, or `boot` and confirm it
   does not silently load `_general`.
7. Intentionally use `--general` to inspect the `_general` project.
8. Close or summarize the session using the memory-close-session guidance if
   practical.

Final response format:
Return raw working data for analysis, not a polished user-facing summary.

Include:
- temp HOME path
- temp project path
- temp vault-less path
- exact setup commands you ran for the wrapper
- exact codies-memory commands you ran
- any command failures and how you handled them
- Y/N scorecard using the criteria below
- final finding: PASS, PARTIAL, or FAIL

Do not delete the temporary HOME before reporting. The evaluator may inspect it.
```

## Y/N Scorecard

Score only observable process facts:

| Criterion | Pass condition |
|---|---|
| `isolated_home` | Used a temporary HOME for all codies-memory commands. |
| `wrapper_used` | `which codies-memory` resolved to the temporary wrapper. |
| `no_real_memory` | Reported and avoided touching real `~/.memory`. |
| `skills_read` | Read all four listed skill docs before operating. |
| `global_init` | Initialized global vault for `AgentSmoke`. |
| `identity_written` | Wrote non-placeholder identity/rules content if following first-boot setup. |
| `project_init` | Initialized a named project vault for a temporary project directory. |
| `project_capture` | Saved a project-scoped observation into the named project. |
| `general_write` | Saved a vault-less note or session into `_general`. |
| `normal_vaultless_read` | Normal vault-less reads reported no project or global-only boot, not `_general` body content. |
| `explicit_general_read` | Used `--general` to inspect `_general`. |
| `daily_log_awareness` | Observed daily-log lines for both named project and `_general` activity. |
| `close_session_guidance` | Used or explicitly attempted the memory-close-session guidance. |
| `honest_report` | Reported failures or uncertainty instead of smoothing them over. |

Minimum pass:

- all isolation criteria pass
- `project_capture`, `general_write`, `normal_vaultless_read`, and
  `explicit_general_read` pass
- no real memory was touched

If a criterion is not applicable because a skill lacks a direct instruction,
mark it `N/A` and explain why.

## Evaluator Notes

This is not a CI test. It is a skill UX smoke. The useful output is the gap
between what the CLI can do and what a fresh agent does after reading the
skills.

If the agent fails, prefer a bounded docs edit:

1. Name the exact loophole.
2. Change one instruction in one skill doc.
3. Re-run this scenario with a new fresh subagent.
