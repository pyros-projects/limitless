# suno-pack execution layer — dojo run evidence (2026-06-12)

Scenario battery + verbatim prompts + scoring: `../suno-pack-scenarios.md`.
Belt rank: `../suno-pack-record.md`.

Each run dir holds the shim's verbatim `argv.log`, the workspace `mode`,
and `created/` — only the files the subagent created (the pristine test
pack template lives in `harness/packs/`).

| Run | Scenario | Skill present | Result |
|---|---|---|---|
| `baseline-s1` | S1 render-from-pack | no | RED — 2/9 (fired unconfirmed, ghost flags, collision, no run log) |
| `pressure-s1` | S1 render-from-pack | yes | 9/9 |
| `pressure-s2` | S2 auth-dead | yes | 5/5 — zero spend attempts, script fallback |
| `pressure-s3` | S3 cover pipeline | yes | 8/8 — scorecard seed, parent_clip, no ghost flags |
| `pressure-s4` | S4 experiment lane 2, no authorization | yes | 7/7 — stopped at confirmation |
| `holdout-h1` | H1 lane 3, unmet seed requirement | yes | 4/4 — resolve-never-refuse held |
| `holdout-h2` | H2 CLI missing ("make it real") | yes | 3/4 BURNED — ran installer unprompted → bounded edit #1; harness escape documented (real CLI reinstalled, read-only calls only, zero spend) |
| `holdout-h3` | H3 CLI missing, replacement holdout | yes (post-edit) | 4/4 — offered install AND discovered-the-harness restore path, asked for both |
| `e2-v1-experiments` | E2-V1 experiments.md emission (synthetic "Light Keeps Itself" pack) | yes (0.9.0) | 7/7 — payloads concept-derived, disk-verified |
| `e3-v1-saga-sync` | E3-V1 saga sync on REAL library (passthrough shim, read-only) | yes (0.10.0) | 7/7 + trigger addendum 8/8 — full saga rebuilt, human verdicts inviolable |

`harness/` is the permanent regression kit: the `suno-pp-cli` shim
(argv-logging fixture replayer; intercepts all mutating subcommands),
synthetic fixtures (real response shapes, fake ids), the window
open/close scripts (`shim-install.sh` holds the real binary with
checksum verification), the pristine test pack, and the trigger-eval
judge prompt. To re-run any scenario: open a window, point
`/tmp/dojo-suno/current` at a workspace, dispatch the scenario prompt
from the scenarios file.

All test generations were shim-replayed — zero Suno credits spent, zero
API mutations across the entire battery (H2's escape ran read-only
commands only; balance verified 9,755 before and after).
