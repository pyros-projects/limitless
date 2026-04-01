---
name: memory-promote
description: "This skill should be used when the agent needs to evaluate or promote memory records through the trust pipeline. Responds to 'promote', 'evaluate inbox', 'elevate trust', 'promote to global', or when inbox items have accumulated and need triage. Converts inbox items to threads/lessons, elevates trust levels, promotes project knowledge to global."
---

# Memory Promote

## When To Use

- At session close (automatic evaluation)
- When an operator explicitly requests promotion
- When promotion thresholds are met during work

## Promotion Paths

### Within Project

```
inbox -> thread (recurring topic)
inbox -> lesson (actionable pattern)
thread -> decision (confirmed across 2+ sessions)
thread -> lesson (reusable pattern)
decision -> lesson (reusable pattern)
```

### Project to Global

```
project lesson -> global lesson (proven across 2+ projects)
```

## How To Run

```bash
# List active inbox items for promotion review
codies-memory list inbox --status active

# Evaluate all inbox items for promotion (no CLI equivalent yet)
uv run python -c "
from pathlib import Path
from codies_memory.records import list_records
from codies_memory.promotion import evaluate_for_promotion

vault = Path('.memory')
inbox_items = list_records(vault, 'inbox', scope='project')
for item in inbox_items:
    result = evaluate_for_promotion(item, context={'session_count': 3})
    if result['eligible']:
        print(f'  Promote: {item[\"frontmatter\"][\"title\"][:60]}')
        print(f'  Suggested: {result[\"suggested_types\"]}')
"

# Promote an inbox item to a thread
codies-memory promote /path/to/record.md --to thread

# Promote a project lesson to global
codies-memory promote /path/to/lesson.md --to-global
```

## Probation

All promoted records enter a 7-day probation window. During probation:
- Contradictory evidence can demote the record back
- Stronger newer records can supersede it
- The record participates in boot and retrieval normally
