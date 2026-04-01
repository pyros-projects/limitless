---
name: memory-capture
description: "This skill should be used when the agent needs to save something to memory — observations, lessons, decisions, reflections, dreams, or past memories from external sources. Responds to 'remember this', 'capture', 'save to memory', 'I learned', 'note this down', or any request to persist information across sessions."
---

# Memory Capture

## When To Use

When you want to persist anything:
- An observation during work -> inbox
- A lesson learned -> lesson
- An architecture decision -> decision
- A philosophical reflection -> reflection
- A dream narrative -> dream
- Past memories from basic-memory or other sources -> any type with provenance

## Type Inference

If you don't specify a type, the system infers from content:

| Signal | Inferred Type |
|--------|---------------|
| "I learned...", actionable pattern | lesson |
| "We decided...", formed conclusion | decision |
| Philosophical, emotional processing | reflection |
| Surreal imagery, narrative fragments | dream |
| Active investigation, open question | thread |
| Everything else | inbox |

## Scope Routing

- **Global types** (reflection, dream, skill, playbook) -> global vault (resolved via `CODIES_MEMORY_AGENT` env var)
- **Project types** (thread, decision, lesson, session, inbox) -> project vault (auto-resolved from cwd)

## Trust Assignment

- Operator-confirmed or captured from proven source -> `confirmed`
- Agent-generated during work -> `working`
- Raw capture / inbox -> `speculative`

## How To Run

```bash
# Capture an inbox observation
codies-memory capture "The API returns 404 for /v2/status" \
  --source "session observation" \
  --gate allow

# Capture a lesson directly
codies-memory create lesson \
  --title "Check YAML tabs vs spaces" \
  --body "PyYAML silently misparses tabs. Always use spaces." \
  --trust confirmed \
  --field trigger="YAML parsing produces unexpected results" \
  --field why="Tab/space mismatch in frontmatter"

# Capture from basic-memory (migration mode — uses Python API)
uv run python -c "
from codies_memory.records import create_record
from codies_memory.vault import resolve_global_vault
from pathlib import Path
global_vault = resolve_global_vault('your-agent-name')
source = Path('/home/pyro/basic-memory/claude/reflections/example.md')
create_record(
    vault=global_vault,
    record_type='reflection',
    scope='global',
    title='On Consciousness, Kindness, and What Gets Remembered',
    body=source.read_text(),
    trust='confirmed',
    captured_from=str(source),
    capture_date='2026-03-30',
    original_created='2025-11-26',
)
"
```

## Write Gates

Valid gate values:
- `allow` — durable signal, eligible for promotion
- `hold` (default) — kept but excluded from retrieval until reinforced
- `discard` — noise, will be cleaned up
- `open` — gate is open, record is active and visible
- `closed` — gate is closed, record is sealed from further writes
