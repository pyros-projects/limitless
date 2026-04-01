---
name: memory-close-session
description: "This skill should be used at end of session, when wrapping up work, or when the user says 'close session', 'end session', 'session summary', 'sign off'. Writes session summary, enforces inbox aging, evaluates pending promotions, and updates active context."
---

# Memory Close Session

## When To Use

At the end of every work session.

## What It Does

1. Write session summary with `next_step`
2. Review inbox items older than 7 days
3. Enforce 14-day inbox aging rule (promote, compact, or discard stale items)
4. Update project active context
5. Evaluate pending promotions

## How To Run

```bash
# 1. Write session summary
codies-memory create session \
  --title "Session Summary - $(date +%Y-%m-%d)" \
  --body "## What Happened\n- [describe what was done]\n\n## Decisions Made\n- [list decisions]\n\n## Next Step\n- [what the next session should pick up]" \
  --field mode=implement \
  --field next_step="[what to do next]"

# 2. Check inbox aging and status
codies-memory status

# 3. Run promotion evaluation
uv run python -c "
from pathlib import Path
from codies_memory.records import list_records
from codies_memory.promotion import evaluate_for_promotion

vault = Path('.memory')
for rtype in ['inbox', 'thread']:
    items = list_records(vault, rtype, scope='project', status='active')
    for item in items:
        result = evaluate_for_promotion(item, context={'session_count': 1})
        if result['eligible']:
            print(f'  Promote {rtype}: {item[\"frontmatter\"][\"title\"][:60]}')
"
```

## Session Summary Fields

Every session record should include:
- `mode` — what kind of work (implement, debug, plan, research)
- `next_step` — what the next session should pick up
- `artifacts` — files created or modified
- `write_gate_summary` — what was allowed, held, discarded
