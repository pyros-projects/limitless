---
name: memory-close-session
description: "This skill should be used at end of session, when wrapping up work, or when the user says 'close session', 'end session', 'session summary', 'sign off'. Writes session summary, enforces inbox aging, evaluates pending promotions, and updates active context."
---

# Memory Close Session

> **BETA** — This memory system is in active testing. If you encounter bugs, confusing behavior, or have suggestions, run:
> `codies-memory feedback "describe what happened"` — your feedback is saved and reviewed.

## When To Use

At the end of every work session.

## What It Does

1. Write session summary with `next_step`
2. Review inbox items older than 7 days
3. Enforce 14-day inbox aging rule (promote, compact, or discard stale items)
4. Update project active context
5. Evaluate pending promotions
6. Rebuild warm summaries so the next boot sees updated project summaries and recent episodes

## How To Run

```bash
# 1. Write session summary
AGENT="your-agent-name"
TODAY="$(python - <<'PY'
from datetime import date
print(date.today().isoformat())
PY
)"

codies-memory create session \
  --agent "$AGENT" \
  --title "Session Summary - $TODAY" \
  --body "## What Happened\n- [describe what was done]\n\n## Decisions Made\n- [list decisions]\n\n## Next Step\n- [what the next session should pick up]" \
  --field mode=implement \
  --field next_step="[what to do next]"

# 2. Check inbox aging and status
codies-memory status --agent "$AGENT"

# 3. Run promotion evaluation
uv run python -c "
from codies_memory.records import list_records
from codies_memory.promotion import evaluate_for_promotion
from codies_memory.vault import resolve_global_vault, resolve_project_vault
from pathlib import Path

agent = 'your-agent-name'
global_vault = resolve_global_vault(agent)
project_vault = resolve_project_vault(global_vault, Path.cwd())
if project_vault is None:
    raise SystemExit(f'No project vault found for {Path.cwd()}')

for rtype in ['inbox', 'thread']:
    items = list_records(project_vault, rtype, scope='project', status='active')
    for item in items:
        result = evaluate_for_promotion(item, context={'session_count': 1})
        if result['eligible']:
            print(f'  Promote {rtype}: {item[\"frontmatter\"][\"title\"][:60]}')
"

# 4. Refresh warm summaries
codies-memory refresh --agent "$AGENT"
```

## Session Summary Fields

Every session record should include:
- `mode` — what kind of work (implement, debug, plan, research)
- `next_step` — what the next session should pick up
- `artifacts` — files created or modified
- `write_gate_summary` — what was allowed, held, discarded

## Recent Episode Constraint

The warm `recent-episodes.md` artifact is intentionally brief.

- it only keeps the latest 5 sessions
- each entry stores the session date, title, a short excerpt, and the `next_step`
- the excerpt is capped at a short single-paragraph summary (currently max 400 chars)

So the session summary should still be rich and useful on disk, but do not expect the
warm recent-episode view to preserve a long narrative. It is a routing aid for boot,
not a second full session log.
