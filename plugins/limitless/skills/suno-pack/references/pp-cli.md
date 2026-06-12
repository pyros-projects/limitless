# pp-cli Execution Reference — Making Packs Real

`suno-pp-cli` is the unofficial, agent-friendly Suno CLI (local control
plane + synced SQLite library). This reference carries the verified
command truth for executing suno-packs. **Do not improvise flags — the
baseline failure mode is inventing plausible-sounding flags (`--style`,
`--prompt`, `--exclude-styles`) that do not exist. The real flags are in
the tables below; when unsure, run the `--dry-run` preflight, never a
live call.**

## Phase 0 — Gates (run before ANY execution work)

1. **Binary:** `command -v suno-pp-cli`. Missing → OFFER the install,
   never run it unprompted:
   `npx -y @mvanhorn/printing-press-library install suno` (NEVER sudo —
   sudo installs into root's home and breaks PATH). Installing modifies
   the user's machine: present the command and wait for their yes — a
   render request ("make it real") authorizes rendering, NOT installing
   software. Run it yourself only after the user agrees (or had already
   told you to install). If the user declines, continue with
   authoring-side value (pack review, prompt edits, per-pack scripts);
   do not fabricate execution.
2. **Health:** `suno-pp-cli --agent doctor`. Credentials invalid/stale →
   degradation playbook below. Never proceed to spending commands on a
   failing doctor.
3. **Credits:** `suno-pp-cli --agent credits` — state the balance AND
   the estimated spend for the requested run (credit table below)
   BEFORE anything fires.

**The confirmation rule (hard):** every credit-spending or
account-mutating command requires explicit user confirmation in
conversation first — `generate create/describe/cover/extend/remaster`,
`clips stems`, `clips convert-wav`, `clips publish`, `clips delete`,
`project create/add/remove/rename/trash`. `--yes` only silences the
CLI's own prompt; it is never a substitute for asking the user. State
the cost, get the yes, then fire.

## Degradation playbooks

**Auth dead (doctor reports invalid/401-stale):**
1. Ask the user to log into suno.com in their normal browser
   (offer `xdg-open https://suno.com`).
2. Run `suno-pp-cli auth login --chrome` (reads the browser session).
3. Re-run `suno-pp-cli --agent doctor` to confirm.
4. NEVER ask the user to paste cookies, JWTs, or tokens. Manual
   `auth login --cookie/--jwt` exists only as a last resort the user
   chooses explicitly after the Chrome flow fails.
5. While auth is down: no spending attempts; offer authoring work.

**CLI missing:** gate 1 above. No substitute packages, no sudo.

## Command truth tables

### `generate create` (custom-mode generation)

```
suno-pp-cli --json --yes generate create \
  --title "<title>" \
  --lyrics "<lyrics block verbatim>" \      # or --lyrics-file <path>
  --tags "<style prompt>" \
  --exclude "<exclude line>" \
  --model v4.5 \
  --weirdness 25 --style-influence 90 \
  --instrumental \                          # only when Settings say ON
  --wait
```

| Real flag | Maps from prompt file |
|---|---|
| `--title` | `## Title` fenced block |
| `--lyrics` / `--lyrics-file` | `## Lyrics` fenced block, verbatim incl. all `[tags]` |
| `--tags` | the ★ Recommended style variant (or the variant the user names); v5.x files have a single style block |
| `--exclude` | `## Exclude Styles` fenced block — pass it, but see caveat below |
| `--model` | Settings table Model (`v5.5 v5 v4.5+ v4.5 v4 v3.5 v3 v2`) |
| `--weirdness` / `--style-influence` | Settings table, 0–100 integers |
| `--instrumental` | Settings "Instrumental toggle ON" |
| `--wait` | always — without it the response returns before clips complete |

Flags that DO NOT exist here: `--style`, `--prompt`, `--exclude-styles`,
`--audio-influence`. Never probe a generate command with `--help`
appended "to see what happens" — read this table instead.

**Exclude caveat (verified from CLI help):** `--exclude` is "accepted
for compatibility; negative_tags is sent empty" — the CLI currently does
NOT transmit excludes. Pass it anyway (forward-compat), but tell the
user: exclude enforcement needs the web UI. The instrumental
anti-vocal defense therefore rests on the toggle + clean style + bracket
structure tags, which all transmit.

### `generate cover` (re-render pipeline)

```
suno-pp-cli --json --yes generate cover <seed_clip_id> \
  --title "<title>" \        # REQUIRED by the upstream endpoint
  --tags "<minimal cover style>" \
  --model v5.5 \
  --wait
```

Cover takes ONLY `--title --tags --model --workspace --wait --download`
(+captcha flags). **No slider flags exist on cover** — weirdness, style
influence, and audio influence are not CLI-settable. When a workflow
calls for cover slider values (the cover file's Audio Influence sweep,
experiment lanes): say so honestly, run the CLI roll on server defaults
and record that in the run log, and hand the user exact slider values as
web-UI instructions for manual re-rolls. Never pass ghost flags. Do not
restate lyrics anywhere — the seed audio carries them.

### Downloads — the collision rule

The CLI names downloaded files by clip TITLE. Two takes of one
generation share the title → the second overwrites the first (this
destroyed a paid take on 2026-06-11). Therefore:

1. NEVER use `--download` on generate commands.
2. Parse the clip ids from the generate response — the real envelope is
   top-level `.clips` (verified live 2026-06-12); keep `.data.clips` as
   the defensive fallback.
3. Per clip: download into a TEMP dir, then move to the take-aware name:
   `suno-pp-cli download <clip_id> --out <tmpdir>/` →
   `mv <tmpdir>/<title>.mp3 <pack>/audio/<slug>-<model>-take<N>-<clipid8>.mp3`
   (slug = pack slug, N = batch order, clipid8 = first 8 hex of the id).
   Never download straight into `audio/` — the title-named file will
   CLOBBER any pre-existing take of the same title already sitting there
   (this destroyed a local v4.5 file on 2026-06-12 before recovery from
   the cloud). Two takes, two files, always — verify both exist before
   reporting.

### Library & read-only commands (no confirmation needed)

```
suno-pp-cli --agent sync --latest-only        # after every generation
suno-pp-cli --agent grep "<query>"            # lyrics/prompt fragment search
suno-pp-cli --agent search "<query>"          # style tag / title search
suno-pp-cli --agent sql '<select …>'          # local SQLite (clips table)
suno-pp-cli --agent clips list --limit 20
suno-pp-cli --agent clips get <clip_id>
suno-pp-cli --agent lineage <clip_id>         # parent chain
suno-pp-cli --agent tree <clip_id>            # full descent tree
suno-pp-cli --agent top --by play_count
suno-pp-cli --agent analytics
suno-pp-cli --agent credits
```

Never `sync --full` by default (libraries run to thousands of clips);
`--latest-only` unless the user asks for a full sync.

### The `--dry-run` preflight (verified 2026-06-12)

`--dry-run` is a global flag: the command parses, sends nothing, exit 0.
`generate create` prints `{"action":"generate","dry_run":true}`;
`generate cover` succeeds SILENTLY in `--json` mode (exit 0, no output —
observed 2026-06-12; verify no-spend via `credits` if in doubt). Use it
as the free preflight for every generate invocation — it catches flag
errors and arg mistakes at zero cost. It does NOT echo the payload;
it validates, nothing more. Run the dry-run, then repeat the identical
command without `--dry-run` after user confirmation.

## The already-ran check (before every spend)

Before generating from a prompt file:
1. Read the pack's `runs/` directory — if a prior run log carries the
   same `lyrics_sha256` + `style_sha256`, surface it: takes already
   exist, re-spending needs an explicit reason.
2. `suno-pp-cli --agent grep "<distinctive lyric line>"` against the
   local library for prior takes outside this pack's history.
3. Report findings (or "no prior takes") as part of the confirmation
   line.

## Run logs — immutable publications

Every execution writes `<pack>/runs/<ISO-timestamp>-<promptfile>.json`.
Never edit an existing run log. Schema (two vocabularies, namespaced;
join key is `clip_id`):

```json
{
  "request": {
    "pack": "<slug>",
    "prompt_file": "no_lyrics_v4.5.md",
    "variant": "A",
    "settings": {"model": "v4.5", "weirdness": 25, "style_influence": 90, "instrumental": true},
    "cli_args": ["generate", "create", "--title", "…", "…"],
    "lyrics_sha256": "<first 10 hex>", "style_sha256": "<first 10 hex>",
    "sliders_not_cli_settable": null
  },
  "result": {
    "clips": [
      {"clip_id": "<uuid>", "model_name": "<as returned>", "created_at": "<as returned>", "file": "audio/<take-aware name>.mp3"}
    ],
    "credits_before": 0, "credits_after": 0,
    "captcha": "open | tripped | solved | manual"
  },
  "lane": {"name": "…", "invariant": "…", "mutation_axis": "…", "expected_failure": "…"},
  "verdicts": {}
}
```

`lane` only for experiment rolls; `verdicts` starts empty and fills via
saga sync (`{"<clip_id>": {"verdict": "like", "note": "…"}}`) or the
human. Never self-score listening judgments; the skill has no ears and
never claims otherwise. For covers, each
result clip carries `"parent_clip": "<seed id>"` — this is the RELIABLE
parentage record: local `lineage` on a freshly synced cover may show a
single node with no ancestry (observed 2026-06-12); treat lineage as
best-effort verification, the run log as truth.

## Saga sync — rebuild the journal from the library (read-only, free)

Trigger: "sync the journal" / "sync the pack" / "rebuild the saga".
Reconstructs a pack's whole experiment history — including rolls the
user made by hand in the web UI — and updates `experiments.md`'s field
journal. No confirmation needed: library reads only.

1. `sync --latest-only`, then collect clips by the pack's title(s)
   (every `## Title` block in the pack):
   ```
   suno-pp-cli --agent sql "select id, title, model_name, created_at,
     json_extract(data,'$.is_liked') liked,
     json_extract(data,'$.metadata.cover_clip_id') parent,
     json_extract(data,'$.metadata.tags') tags,
     json_extract(data,'$.reaction.play_count') my_plays,
     json_extract(data,'$.reaction.skip_count') my_skips,
     duration from clips where title in (…)"
   ```
2. **Lineage closure:** `metadata.cover_clip_id` is the parent edge —
   walk it both ways until the set is closed (covers of covers, renamed
   children). The tree rebuilds fully offline; `lineage`/`tree` API
   calls are optional verification, not the source.
3. **Stray detection:** clips in the same time window whose tags match
   the pack's style vocabulary but whose titles don't (Suno auto-titles
   non-custom rolls from the style prompt, e.g. "Felt Piano Single") are
   CANDIDATES — list them and ask the user; never silently include or
   drop.
4. **Journal merge (sacred rules):** one row per generation
   (`created_at` groups the takes). `is_liked = 1` → verdict at least
   "like" (mark which clip carries the ♥). Never downgrade, never
   overwrite a human verdict or note; absence of a like is NOT "nope".
   Lane attribution from tags is best-effort — mark inferred lanes
   with "?". Render the lineage tree as text in the journal. Update the
   running credit total from generation counts.

## Verdicts — the field journal scale

No numeric scores on art, ever (operator rule + dojo's Measurability
Rule): verdicts are **love / like / nope / hate**, keep = like or
better. The note column is the knowledge — findings, not numbers.
Objective facts (glitches, dead air, wrong duration) are facts, not
verdicts; record them in notes or leave them to tooling. Run logs carry
`"verdict"` and `"note"` per clip (filled by sync or the human),
replacing the former numeric `human_scorecard`.

## Cover seed selection (decision 2026-06-11)

The human picks the seed; the skill proposes. Proposals cite observables
only: journal verdicts from prior run logs (love > like — these OUTRANK
play counts), is_liked, play_count, upvote_count, prior lineage, ship
history. Fresh
takes with zero signal → ask, no default. Never claim to have heard
anything.

## Captcha posture

1. Fire plain generate commands first — the tokenless attempt usually
   passes on a warm session (verified live 2026-06-11: zero challenges).
2. On `422 token_validation_failed`: tell the user, then (with their ok)
   `suno-pp-cli auth captcha login` once — a visible browser window;
   the profile stays warm for the session. `--wait-for-gate
   --gate-timeout 30m` only with explicit user ok.
3. Record captcha state in every run log (`open/tripped/solved/manual`)
   — over time this measures the real challenge rate.
4. Never bypass, never run the solver silently in `--agent` contexts
   (the CLI refuses: ErrInteractiveRequired).

## Credit table (observed costs)

| Action | Cost | Status |
|---|---|---|
| `generate create`, v4.5, 2 takes | 10 credits | observed 2026-06-11 |
| `generate cover`, v5.5, 2 takes | 10 credits | observed 2026-06-12 (9,755 → 9,745) |
| downloads, sync, library reads | 0 | observed |
| pack authoring | 0 | by construction |

Track a running per-pack total across run logs; state it in every
confirmation line.

## model_name mapping (as returned by the API)

| CLI `--model` | `model_name` in responses | Status |
|---|---|---|
| v4.5 | `chirp-auk` | observed 2026-06-11 |
| v5.5 | `chirp-fenix` (response also carries `major_model_version: "v5.5"`) | observed 2026-06-12 |
| others | `chirp-crow`, `chirp-bluejay`, … | present in libraries; mapping unverified — record what returns, don't guess |

## Per-pack runnable scripts

Pack emission includes one `generate_<promptfile>.sh` per prompt file:
banner (settings + credit warning), explicit confirm prompt (`--yes` to
skip), awk extraction of Title/Lyrics/Exclude/★-variant from the
canonical markdown, then the exact `generate create` invocation from the
truth table — but WITHOUT `--download`; the script downloads per clip id
and applies the take-aware rename. Keep scripts in sync when prompts
change. Scripts make packs runnable without the skill; the skill remains
the orchestrator with judgment.

## Experiment workspaces

One Suno project per experiment pack:
`suno-pp-cli --json --yes project create --name "exp: <slug>"` (this IS
account-mutating — confirmation rule applies), then add branch clips via
`project add <project_id> --clip <clip_id>`. `lineage`/`tree`
reconstructs the mutation map.
