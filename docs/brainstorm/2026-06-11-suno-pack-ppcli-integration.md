# Suno-Pack × suno-pp-cli — Integration Concept

*Concept · 2026-06-11 · Claude (Fable 5) + Pyro · supersedes the custom
wrapper-CLI idea in `~/music/suno/suno_cli_concept.md`*

> Status: concept, grounded in a live end-to-end test (2026-06-11).
> Direction decided by Pyro: no custom `suno` wrapper binary — suno-pack
> the skill orchestrates `suno-pp-cli` directly. The pack stops being
> paperwork and becomes a runnable artifact.

---

## Evidence base (today's live test)

Everything below ran on this machine, this afternoon:

- **Auth:** `auth login --chrome` re-read the logged-in browser session
  after a 401-stale credential; `doctor` → valid. Premier plan, 9,765
  credits.
- **Library:** `sync --latest-only` hydrated 2,000 clips into local
  SQLite; `sql`, `clips list`, `grep`, `credits` all work with `--agent`
  JSON.
- **Generation:** the pack's pending `no_lyrics_v4.5.md` generated for
  real via Codie's extraction script → `generate create --wait
  --download` → valid 48kHz stereo mp3 in `audio/`, 10 credits for 2
  takes.
- **Captcha: never fired.** Solver profile stayed `stopped/seeded=false`
  through the whole run. Confirms the source-level read: the CLI
  attempts tokenless first and only solves hCaptcha on a server-side
  `422 token_validation_failed`. "Captcha every generation" is actually
  "captcha when the server challenges" — a warm, recently-authed session
  passes silently. The visible fallback window (Pyro fixed the WSL side)
  is the safety net, not the routine.
- **One real bug found:** 2 takes share the title → both download as
  `<title>.mp3` → the second overwrites the first locally. Take-aware
  naming is a must-fix in the integration.

## Why integrate instead of wrap

The original concept proposed a `suno` wrapper CLI as the ergonomic
bridge. The live test showed the bridge is thinner than assumed: pp-cli
already does auth, sync, search, lineage, generation, downloads, and
agent-mode JSON. What's missing is *pack awareness* — and pack awareness
is judgment plus a little parsing, which is exactly what a skill is.
Building a binary to hold judgment we already have in the skill would be
plumbing for its own sake.

(Prior art note: printing-press-library ships its own generic `pp-suno`
skill. We integrate into suno-pack instead — ours is pack-native: it
knows Settings tables, style variants, cover pipelines, and experiment
lanes. We borrow its command recipes, not its shape.)

## The integration

Suno-pack gains an execution layer. Authoring stays unchanged; after
authoring (or on demand for an existing pack), the skill can now make
the music real.

### Phase 0 — Gates (mirrors hivemind's preflight)

1. `command -v suno-pp-cli` — missing → offer install:
   `npx -y @mvanhorn/printing-press-library install suno` (never sudo).
2. `suno-pp-cli --agent doctor` — credentials invalid → offer the
   browser re-auth: user logs into suno.com, then
   `auth login --chrome`. Never ask for pasted cookies/JWTs first.
3. `--agent credits` — show balance and the estimated spend for the
   requested run (observed: v4.5 generate = 10 credits / 2 takes)
   **before** anything fires. Explicit user confirmation for every
   credit-spending or account-mutating command — generate*, stems,
   convert-wav, publish, delete, project writes.

### Generate-from-pack

```
suno-pack: "render no_lyrics_v4.5.md"  /  "generate the pack"  /
"make it real"  /  "run the cover pipeline"
```

1. **Parse the prompt file** (the skill reads its own format): Settings
   table → model/weirdness/style-influence/instrumental; `## Lyrics`
   fenced block; `## Title`; `## Exclude Styles`; style variant marked
   ★ Recommended (or the variant the user names).
2. **Call** `suno-pp-cli --json --yes generate create --title … --lyrics
   … --tags <style> --exclude … --model … --weirdness … 
   --style-influence … --wait` (`--instrumental` per settings). Do NOT
   rely on `--download`:
3. **Take-aware download (the collision fix):** parse the returned clips
   array; for each clip id, `suno-pp-cli download <clip_id> --out
   <pack>/audio/` and name the file
   `<slug>-<model>-take<N>-<clipid8>.mp3`. Two takes, two files, always.
4. **Run log:** write `<pack>/runs/<ISO-timestamp>-<promptfile>.json`:
   source file, chosen variant, full settings, clip IDs, credits
   before/after, captcha state (open/tripped/solved/manual), file
   paths, model_name as returned (v4.5 = chirp-auk). Runs are immutable
   publications — the pack accumulates its own generation history.
5. **Sync after:** `sync --latest-only` so the local library knows the
   new clips.

### Per-pack runnable scripts (Codie's pattern, adopted)

Pack emission now includes a `generate_<promptfile>.sh` per prompt file
(the pattern Codie prototyped and today's test validated): banner with
settings + credit warning, `--yes` flag for non-interactive, extraction
via awk from the canonical markdown. The skill keeps the scripts in sync
when prompts change. Scripts make packs runnable without the skill
present; the skill remains the orchestrator with judgment (gates,
take-naming, run logs).

### Cover pipeline execution

`cover_4.5_5.5.md` stops being instructions for a human: pick the seed
take (user choice or best-of run log), then `generate cover <clip_id>
--model v5.5 --tags <cover style>` → take-aware download → run log entry
with `parent_clip` — lineage preserved both locally and in Suno
(`lineage <id>` / `tree <id>` to verify).

### Experiment-mode execution (the payoff)

This integration is what makes `--mode experimental` real
(`2026-06-11-suno-experiment-ideas.md`, 27 lanes):

- `project create --name "exp: <pack slug>"` — one Suno workspace per
  experiment pack; every branch clip gets added.
- Each lane = generate/cover calls with the lane's settings; the lane's
  invariant/axis/expected-failure go INTO the run log, so the scorecard
  can be filled against receipts.
- `lineage`/`tree` reconstructs the mutation map (persona laddering is
  literally lineage-tree farming).
- Slider sweeps (cover-abuse lab: audio influence 30/50/70/85) become a
  loop, not an afternoon of clicking.

### Library awareness

Before generating: `grep`/`search` the local db for prior takes of the
same pack (don't re-spend on a prompt that already has keepers). On
request: `analytics`, `top --by play_count`, session summaries — the
pack can report how its tracks perform.

### Captcha posture

1. Plain `generate` first — tokenless attempt is free and usually passes
   (today's evidence).
2. On `token_validation_failed`: tell the user, then
   `auth captcha login` (visible window — works now) once; keep that
   profile warm for the session. `--wait-for-gate --gate-timeout 30m`
   only with the user's explicit ok.
3. Record the captcha state in every run log — over time this measures
   the real challenge rate instead of folklore.
4. Never attempt bypass; never run the solver silently in `--agent`
   contexts (the CLI refuses anyway: ErrInteractiveRequired).

## Packaging (a dojo edit to suno-pack)

- New reference: `plugins/limitless/skills/suno-pack/references/pp-cli.md`
  — command recipes, prompt-file parse rules, run-log schema, take-naming
  convention, captcha playbook, credit table (observed costs).
- SKILL.md: new "Make it real" section + description gains execution
  triggers ("render the pack", "generate it for real", "run the cover
  pipeline", "how are my tracks doing").
- **Description changes → trigger eval required** (dojo kata 6), plus
  collision check against hivemind ("how are my tracks doing" must not
  leak there) and dojo's own matrix.
- Dojo intake scenarios: render-from-pack (criteria: gates ran, fields
  mapped correctly, take-aware names, run log written, credits
  reported); auth-dead degradation (offers re-auth, never pastes
  secrets); cover-from-seed. The take-collision bug is the first
  pre-written RED evidence.

## Non-goals

- No custom wrapper binary (superseded, this doc).
- No captcha bypass, no headless solving, no unattended credit spend.
- No full-library sync by default (thousands of tracks; `--latest-only`
  unless asked).
- No replacement of pp-cli subcommands the skill can call directly.

## Decisions (Pyro, 2026-06-11)

1. **Run-log schema: store both vocabularies, namespaced.** A `request`
   block (pack vocabulary + exact CLI args — reproducibility) and a
   `result` block (verbatim clip metadata subset: clip IDs,
   `model_name`, `created_at`). Join key between run logs and the local
   library is `clip_id` — stable and vocabulary-free. Keep lyrics/style
   hashes for the "already ran this exact prompt?" check.
2. **Cover-seed selection: human picks, skill proposes.** Proposals cite
   observables only (play counts, upvotes, prior lineage, ship history,
   and any human scorecard rating from earlier run logs — which
   outranks play counts). Fresh takes with zero signal → the skill asks,
   no default. The skill never claims to have heard anything.
3. **Experiment-mode rolls: exactly one automated roll per lane.** After
   the single upfront budget confirmation, the automated round is one
   roll per lane — breadth, never depth. Then stop and report: the
   human listens, judges, and explicitly orders re-rolls on chosen
   lanes ("you could be lucky and already have your banger; if not,
   roll again"). Depth is always human-triggered. The cover-lab slider
   sweep (4 generations by design) is the declared exception: it runs
   only if explicitly ticked in the budget confirmation. Per-pack hard
   ceiling and running totals in the run logs still apply.
