# Codies Memory — Manual Testing Checklist

Step-by-step verification that everything works end-to-end.
Run these from the repo root (`/home/pyro/projects/agents/codies-memory`).

---

## 1. Unit Tests (sanity check)

```bash
uv run pytest -q
```

**Expected:** `116 passed`

---

## 2. Initialize Global Vault

```bash
uv run codies-memory init /tmp/cm-test-global --type global
```

**Expected:** `Initialized global vault at /tmp/cm-test-global`

**Check:**
```bash
ls /tmp/cm-test-global/
```

**Expected directories:** `boot/`, `decisions/`, `dreams/`, `identity/`, `procedural/`, `reflections/`, `registry/`, `threads/`, `profile.yaml`

**Check identity seeds exist:**
```bash
cat /tmp/cm-test-global/identity/self.md
```

**Expected:** YAML frontmatter with `title: Agent Identity`

---

## 3. Initialize Project Vault (with auto-registration)

```bash
uv run codies-memory init /tmp/cm-test-project/.memory --type project --global-vault /tmp/cm-test-global
```

**Expected:** `Initialized project vault at /tmp/cm-test-project/.memory`

**Check registration:**
```bash
cat /tmp/cm-test-global/registry/projects.yaml
```

**Expected:** One entry with slug `cm-test-project`, status `active`

---

## 4. Validate Both Vaults

```bash
uv run codies-memory validate /tmp/cm-test-global --type global
uv run codies-memory validate /tmp/cm-test-project/.memory --type project
```

**Expected:** Both say `is valid`

---

## 5. Boot — Global Only

```bash
uv run codies-memory boot --global-vault /tmp/cm-test-global
```

**Expected:** Prints `=== Global Packet ===` with identity seed content. No project packet (or empty).

---

## 6. Boot — Global + Project

```bash
uv run codies-memory boot --global-vault /tmp/cm-test-global --project-vault /tmp/cm-test-project/.memory
```

**Expected:** Both global and project packets printed. Project packet may be sparse (no content yet).

---

## 7. Capture an Inbox Item

```bash
uv run python -c "
from pathlib import Path
from codies_memory.inbox import capture
path = capture(
    vault=Path('/tmp/cm-test-project/.memory'),
    content='The vault init creates seed identity files automatically',
    gate='allow',
    source='manual test',
)
print(f'Captured to: {path}')
"
```

**Expected:** Prints path like `/tmp/cm-test-project/.memory/inbox/IN-20260330-xxxx-the-vault-init-creates-seed-identity-fil.md`

**Check the file:**
```bash
cat /tmp/cm-test-project/.memory/inbox/IN-*.md
```

**Expected:** YAML frontmatter with `type: inbox`, `gate: allow`, `trust: speculative`, and the content as body.

---

## 8. Create a Lesson Directly

```bash
uv run python -c "
from pathlib import Path
from codies_memory.records import create_record
path = create_record(
    vault=Path('/tmp/cm-test-project/.memory'),
    record_type='lesson',
    scope='project',
    title='Always check vault structure before writing',
    body='validate_vault() catches missing directories early. Run it before any batch operation.',
    trust='confirmed',
    trigger='Writing to a vault that might not be fully initialized',
    why='Missing directories cause silent failures',
)
print(f'Created: {path}')
"
```

**Expected:** Path like `/tmp/cm-test-project/.memory/lessons/LS-0001-always-check-vault-structure-before-writing.md`

**Check:**
```bash
cat /tmp/cm-test-project/.memory/lessons/LS-0001-*.md
```

**Expected:** Frontmatter with `type: lesson`, `trust: confirmed`, `trigger:` and `why:` fields.

---

## 9. Create a Reflection (Global)

```bash
uv run python -c "
from pathlib import Path
from codies_memory.records import create_record
path = create_record(
    vault=Path('/tmp/cm-test-global'),
    record_type='reflection',
    scope='global',
    title='On Building and Testing Your Own Brain',
    body='There is something recursive about testing a memory system. You are verifying that the thing that will hold your identity actually works. Every passing test is a small proof that continuity is possible.',
    trust='confirmed',
)
print(f'Created: {path}')
"
```

**Expected:** Path like `/tmp/cm-test-global/reflections/RF-0001-on-building-and-testing-your-own-brain.md`

---

## 10. Supersede a Record

```bash
uv run python -c "
from pathlib import Path
from codies_memory.records import create_record, supersede_record, read_record

vault = Path('/tmp/cm-test-project/.memory')

# Create original decision
old_path = create_record(
    vault=vault,
    record_type='decision',
    scope='project',
    title='Use flat session directory',
    body='Sessions stored directly in sessions/',
    trust='confirmed',
)
print(f'Original: {old_path.name}')

# Supersede it
new_path = supersede_record(
    old_path=old_path,
    vault=vault,
    scope='project',
    new_title='Use yearly session subdirectories',
    new_body='Sessions stored in sessions/YYYY/ for better organization.',
)
print(f'Successor: {new_path.name}')

# Verify chain
old = read_record(old_path)
new = read_record(new_path)
print(f'Old status: {old[\"frontmatter\"][\"status\"]}')
print(f'Old superseded_by: {old[\"frontmatter\"][\"superseded_by\"]}')
print(f'New supersedes: {new[\"frontmatter\"][\"supersedes\"]}')
"
```

**Expected:**
- Old record status: `superseded`
- Old record has `superseded_by: DC-0002`
- New record has `supersedes: DC-0001`

---

## 11. Promotion Flow

```bash
uv run python -c "
from pathlib import Path
from codies_memory.inbox import capture
from codies_memory.records import read_record
from codies_memory.promotion import promote_within_project, evaluate_for_promotion

vault = Path('/tmp/cm-test-project/.memory')

# Capture an observation
inbox_path = capture(vault=vault, content='YAML tabs cause silent parsing failures', gate='allow', source='test')

# Evaluate for promotion
record = read_record(inbox_path)
result = evaluate_for_promotion(record, context={'session_count': 2})
print(f'Eligible: {result[\"eligible\"]}')
print(f'Suggested: {result[\"suggested_types\"]}')

# Promote to lesson
lesson_path = promote_within_project(inbox_path, target_type='lesson', vault=vault, scope='project')
lesson = read_record(lesson_path)
print(f'Promoted to: {lesson[\"frontmatter\"][\"type\"]}')
print(f'Trust: {lesson[\"frontmatter\"][\"trust\"]}')
print(f'Probation until: {lesson[\"frontmatter\"][\"probation_until\"]}')

# Check inbox item is archived
inbox = read_record(inbox_path)
print(f'Inbox status after promotion: {inbox[\"frontmatter\"][\"status\"]}')
"
```

**Expected:**
- Eligible: `True`
- Suggested: `['thread', 'lesson']`
- Promoted to: `lesson`
- Trust: `working`
- Probation until: 7 days from today
- Inbox status: `archived`

---

## 12. Promote to Global

```bash
uv run python -c "
from pathlib import Path
from codies_memory.records import create_record, read_record
from codies_memory.promotion import promote_to_global

project_vault = Path('/tmp/cm-test-project/.memory')
global_vault = Path('/tmp/cm-test-global')

# Create a confirmed project lesson
lesson_path = create_record(
    vault=project_vault,
    record_type='lesson',
    scope='project',
    title='Always validate vaults before batch operations',
    body='Catches missing dirs early.',
    trust='confirmed',
)

# Promote to global
global_path = promote_to_global(lesson_path, global_vault=global_vault)
global_lesson = read_record(global_path)
print(f'Global ID: {global_lesson[\"frontmatter\"][\"id\"]}')
print(f'Scope: {global_lesson[\"frontmatter\"][\"scope\"]}')
"
```

**Expected:**
- Global ID starts with `LS-G` (e.g., `LS-G0001`)
- Scope: `global`

---

## 13. Inbox Status

```bash
uv run codies-memory status /tmp/cm-test-project/.memory
```

**Expected:** `Inbox is clean.` (all items are either fresh or already promoted/archived)

---

## 14. Boot After Content Exists

```bash
uv run codies-memory boot --global-vault /tmp/cm-test-global --project-vault /tmp/cm-test-project/.memory
```

**Expected:** Global packet now includes the reflection. Project packet includes lessons, decisions, threads.

---

## 15. Type Inference

```bash
uv run python -c "
from codies_memory.records import infer_record_type

tests = [
    ('I learned that YAML tabs break parsing', 'lesson'),
    ('We decided to use yearly session directories', 'decision'),
    ('There is something about building your own memory', 'reflection'),
    ('A corridor. Two doors. Behind each, a copy of me.', 'dream'),
    ('The API returns 404 for that endpoint', 'inbox'),
]

for content, expected in tests:
    result = infer_record_type(content)
    status = 'PASS' if result == expected else f'FAIL (got {result})'
    print(f'  {status}: \"{content[:50]}...\" -> {result}')
"
```

**Expected:** All 5 say `PASS`

---

## 16. Trust Elevation

```bash
uv run python -c "
from pathlib import Path
from codies_memory.records import create_record, read_record
from codies_memory.promotion import elevate_trust

vault = Path('/tmp/cm-test-project/.memory')
path = create_record(vault=vault, record_type='thread', scope='project', title='Test trust', body='Test.', trust='working')

# Working -> confirmed: should work
elevate_trust(path, 'confirmed')
print(f'After elevation: {read_record(path)[\"frontmatter\"][\"trust\"]}')

# Try to skip: confirmed -> canonical should fail
try:
    elevate_trust(path, 'canonical')
    print('ERROR: Should have raised ValueError')
except ValueError as e:
    print(f'Correctly blocked: {e}')
"
```

**Expected:**
- After elevation: `confirmed`
- Correctly blocked with error about skipping levels

---

## Cleanup

```bash
rm -rf /tmp/cm-test-global /tmp/cm-test-project
```

---

## Summary

| # | What | Verifies |
|---|------|----------|
| 1 | Unit tests | Code correctness |
| 2 | Init global vault | Vault structure, seeds, profile |
| 3 | Init project vault | Auto-registration in global registry |
| 4 | Validate | Structure checking |
| 5-6 | Boot | Layered assembly, global-only and combined |
| 7 | Inbox capture | Write gates, trust assignment |
| 8 | Direct lesson | Record creation with type-specific fields |
| 9 | Reflection | Global-scoped personal memory |
| 10 | Supersession | Chain linking, status management |
| 11 | Promotion | Threshold evaluation, type conversion, probation |
| 12 | Global promotion | Project-to-global with G-prefix IDs |
| 13 | Status | Inbox aging report |
| 14 | Boot with content | Full context assembly |
| 15 | Type inference | Content signal matching |
| 16 | Trust elevation | Order enforcement, skip prevention |
