# Contract Emission Reference — schema, the Accord, round-trip

This file supersedes the whitepaper's v0.6 contract-derivation wording for
this variant. Canonical upstream of the schema and door policy:
`docs/concepts/01-contract-schema-and-door-policy.md` in the docket repo.
If this file and that doc disagree, that doc wins — fix the drift here.

## The contract file — schema by example

`.contracts/<project>.contract.yaml`. Four clause archetypes cover the space:

```yaml
contract: tipsy                  # project slug
rev: 1
source: .sfd/clause-log.md (SFD Gate 2, 2026-06-12)   # which horse, when
signed: []                       # user signs at Gate 2: {rev, by, date}

clauses:
  # Archetype 1: test-checked
  - id: C-007                    # FROM THE CLAUSE LOG, unchanged
    obligation: >
      Tips MUST be rounded to the nearest $0.10, ties rounding up.
    acceptance:
      test: tests/test_rounding.py::test_nearest_dime_ties_up
    anchors:
      - surface: "calculate × happy-path"     # inventory cell
      - decision: D-003                       # decision-log entry

  # Archetype 2: metric-checked (this is what "feels fast" must become)
  - id: C-011
    obligation: >
      Invocation-to-output MUST complete in under 50ms at p95 on the
      reference machine.
    acceptance:
      metric: scripts/bench_startup.sh
      threshold: "p95 < 50ms"
    anchors:
      - surface: "calculate × happy-path"

  # Archetype 3: negative clause (mined from a rejected alternative)
  - id: C-014
    obligation: >
      The tool MUST NOT read stdin under any invocation — no interactive
      mode exists.
    acceptance:
      command: "echo '' | tipsy 2>&1; test $? -eq 2"
      expect: "exit 2, stdin never consumed"
    anchors:
      - decision: D-009          # "kill interactive mode, flags only"

  # Archetype 4: human-verdict (legal, but explicit — never silent vibes)
  - id: C-016
    obligation: >
      Error messages MUST NOT use jargon or stack traces.
    acceptance:
      verdict: human
    anchors:
      - surface: "calculate × validation-failure"
```

Field rules: every clause needs `id` (C-NNN, per-project monotonic, from the
clause log), `obligation` (exactly one MUST or MUST NOT — SHOULD is banned:
decide or defer), `acceptance` (exactly one of `test:` / `metric:` +
`threshold:` / `command:` + `expect:` / `verdict: human`), `anchors` (≥1
typed: `surface:` inventory cell, `decision:`, `incident:`, `regulation:`,
`sla:`, `compat:`). Optional: `risk: low|medium|high`, `evidence_required:`
(list of evidence kinds), `scope: {applies_to, excludes}`, `status:
active|deferred`, `notes:` (residuals).

## Self-admission — the Accord checklist (A1–A9)

Walk every clause through these checks as if you were the ledger refusing
your own work. **Refuse** = fix at the source before Gate 2. **Flag** =
record honestly in the contract file (`notes:`) and the round-trip report.

| # | Check | Outcome on failure |
|---|---|---|
| A1 | `acceptance` present and one of the four types; `verdict: human` is legal but must be explicit | REFUSE — "how would the ledger check this? a test, a number, a command, or declared human judgment" |
| A2 | ≥1 typed anchor | REFUSE — "where did this come from?" |
| A3 | acceptance target (test file, script) exists | FLAG `PENDING-HARNESS` — clause is law; cannot go green until the harness exists. Normal in pre-implementation handoffs |
| A4 | obligation contains exactly one MUST or MUST NOT; no SHOULD | REFUSE — "a hope, not an obligation" |
| A5 | no two clauses claim the same acceptance target with different expectations | FLAG `OVERLAP` — resolve or scope before signing |
| A6 | qualitative performance words (fast, reliable, scalable, snappy, robust) appear only with numbers | REFUSE — "give me a number, a test, or demote to open questions" |
| A7 | schema validity: required fields present, unique ids, valid YAML | REFUSE — plain validation error |
| A8 | atomicity: exactly one obligation per clause | REFUSE — "two laws in one clause — split them" |
| A9 | `risk: high` clauses carry `evidence_required` with ≥2 kinds | FLAG `THIN-EVIDENCE` |

Record the walk: one line per clause in the round-trip report ("C-007:
admitted · C-011: admitted · C-013: REFUSED A6 → numbered → admitted").
A handoff bundle whose contract file would bounce off a docket door is not
done — fixing refusals here is 10x cheaper than after import.

## Round-trip test protocol

Purpose: contracts are sufficient iff a blind agent can rebuild the surface
from them. Procedure:

1. Collect ONLY `.contracts/<project>.contract.yaml` +
   `.sfd/surface-state-inventory.md`. Not the prototype. Not the decision
   log. Not the conversation.
2. Fresh-context subagent: "Reconstruct this product's surface at
   wireframe / session-transcript fidelity from these two files alone."
3. Diff the reconstruction against the converged prototype. Classify each
   divergence: **leak** (behavior the contracts failed to pin — tighten or
   add a clause, via the clause log) or **cosmetic** (layout/wording the
   contracts legitimately don't govern).
4. Max 2 rounds. Write `.sfd/round-trip-report.md`: mode
   (subagent | self-blind), per-round leak list, fixes applied, accepted
   cosmetic diffs, the A1–A9 walk results.

Fallback without subagent tooling: self-blind — write the reconstruction
from the two files before re-opening the prototype, then diff honestly.
Weaker (you have memory); mark `mode: self-blind`.

## Handoff Bundle manifest (Gate 2 deliverable)

| # | Artifact | Path |
|---|---|---|
| 1 | Intent document | `.sfd/intent.md` |
| 2 | Converged surface prototype | `prototype/` |
| 3 | Decision log | `.sfd/decision-log.md` |
| 4 | Clause log | `.sfd/clause-log.md` |
| 5 | Surface state inventory | `.sfd/surface-state-inventory.md` |
| 6 | **Contract file (the product)** | `.contracts/<project>.contract.yaml` |
| 7 | Round-trip report | `.sfd/round-trip-report.md` |

The bundle is consumer-agnostic: a docket ledger imports #6 directly; #1–#5
and #7 are the provenance that lets any future reader audit why each clause
exists. Open questions live in the decision log's open-questions section —
they are NOT clauses and never ride along in the contract file.
