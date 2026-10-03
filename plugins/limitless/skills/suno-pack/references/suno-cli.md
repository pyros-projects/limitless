# suno-cli Execution Reference — Making Packs Real on v6

`suno` (paperfoot/suno-cli, crate `suno`) is the v6 execution CLI: a Rust
binary that talks to Suno's web API with the user's own browser session.
Verified 2026-10-03 against 0.10.1 (help text, offline dry-runs, and live
v6 / v6-wild generations on the user's account). **Do not improvise flags —
the tables below are the truth; when unsure, run the `--dry-run` preview,
never a live call.**

Execution routes, decided per request in SKILL.md:
- **CLI route** (this file) — default for every render, cover, extend,
  remaster, download.
- **Browser route** (`references/browser-ui.md`) — Claude with the Claude in
  Chrome tools only, for captcha-gated sessions and controls the CLI cannot
  set.
- **Paste route** — the human renders in their own browser from the prompt
  file. The fallback for every agent without Claude in Chrome.

## Phase 0 — Gates (before ANY execution work)

1. **Binary:** `command -v suno` and `suno --version` (expect ≥ 0.10.1).
   Missing → OFFER the install and wait for a yes — a render request
   authorizes rendering, NOT installing software:
   `cargo install --locked suno` (or `brew install paperfoot/tap/suno`).
   Never sudo. **Never run `suno skill install`** — it writes a competing
   `suno` skill into the agent's skill folders.
2. **Health:** `suno doctor --json`. Check `jwt`, `studio_api`, `credits`,
   and `captcha_preflight`.
   - `auth_expired` / stale JWT → `suno auth --refresh`; if that fails, ask
     the user to be logged into suno.com in their normal Chrome, then
     `suno auth --login` (reads the browser session). NEVER ask the user to
     paste cookies or JWTs into the chat.
   - `captcha_preflight: required: true` → the CLI route is closed for
     generation right now; see Captcha posture.
3. **Credits:** `suno credits --json` → `total_credits_left`. State the
   balance AND the estimated spend before anything fires.

**The confirmation rule (hard):** every credit-spending or account-mutating
command needs the user's explicit yes in conversation first, with the cost
stated — `generate`, `describe`, `cover`, `extend`, `remaster`, `concat`,
`stems`, `delete`, `publish`, `set`. A yes the user already gave for this
exact action in the request counts; a vague "make it real" for a whole pack
covers one generation per prompt file, not re-rolls.

## Captcha posture (hard)

- **Always pass `--no-captcha`** on generate, describe, cover, extend,
  remaster. Never run the CLI's built-in solver: it drives a headless Chrome
  and then a headed Chrome parked offscreen to get past the captcha's bot
  detection — that is evasion, not use. Never set `SUNO_CAPTCHA_HEADED` /
  `SUNO_CAPTCHA_HEADLESS`, never `--headless` for generation, never hand
  out or request solved tokens from third-party solving services.
- `captcha_required` (or doctor says `required: true`) → the human solves
  it, in their own browser:
  - Claude with Claude in Chrome tools: the browser route
    (`browser-ui.md`) on the user's real Chrome — if Turnstile shows a
    checkbox there, the USER clicks it; the agent never clicks a captcha.
  - Any other agent: the paste route.
  - After one human-solved generation the session usually reads
    `required: false` again (observed 2026-10-03), so the CLI route reopens.
- Record the captcha state in every run log (`open` / `required` /
  `solved-by-user` / `paste-route`).

## Command truth tables

### `suno generate` (Advanced/custom mode)

```
suno generate --no-captcha \
  --model v6 \
  --title "<Title block>" \
  --tags "<Style of Music block>" \
  --exclude "<Exclude Styles block>" \
  --lyrics-file <file holding the Lyrics block verbatim> \
  --weirdness 35 --style-influence 75 \
  --vocal female \                          # only when Settings name a Vocal Gender
  --instrumental \                          # only for Lyrics Mode Instrumental
  --max-mode \                              # only when Settings say Max Mode on (2× credits)
  --request-id <fresh uuid4> \
  --wait --json
```

| Real flag | Maps from prompt file |
|---|---|
| `--model` | Settings Model: `v6`, `v6-wild`, `v6-mini` (older names are rejected against the live catalogue) |
| `--title` | `## Title` (≤100) |
| `--tags` | `## Style of Music` (≤1,000) |
| `--exclude` | `## Exclude Styles` (≤1,000) — sent as `negative_tags`, works |
| `--lyrics-file` / `--lyrics` | `## Lyrics`, verbatim incl. all `[tags]` (≤5,000) |
| `--weirdness` / `--style-influence` | Settings, 0–100 integers |
| `--audio-influence` | only with source audio |
| `--vocal male\|female` | Settings Vocal Gender |
| `--instrumental` | Lyrics Mode Instrumental (still pass the tags-only Lyrics block) |
| `--persona <uuid>` | a Voice id, only when the user names one |
| `--max-mode` | Settings Max Mode on |
| `--request-id` | always — a fresh UUID per intended generation |
| `--wait` | always |

**The CLI cannot set:** Variety, Personalize/My Taste, Duration, Lyrics
Mode Mumble, image/video/MIDI/playlist inputs. Flags that DO NOT exist:
`--variety`, `--personalize`, `--my-taste`, `--duration`, `--style`,
`--prompt` (on generate), `--audio`. Never pass them. When these are only
the pack's defaults (Variety Off, a fixed Duration), render with server
defaults (Duration Auto), name what was not applied in the confirmation
line and the report, and check the stored tags afterwards. When the
request is about one of them (a Variety or My Taste experiment, Mumble, a
Duration the user asked for), the CLI is the wrong route: browser route
(Claude with Claude in Chrome) or paste route.

Do not use `--download` on generate; download per clip (below).

### `--dry-run` preview (free, offline)

`suno generate ... --dry-run --json` validates limits and prints the full
request (`mv`, `tags`, `negative_tags`, `prompt`, `make_instrumental`,
`metadata.control_sliders`, `is_max_mode`) without authentication or
credits. Run it before every live generate, then repeat the identical
command without `--dry-run` after the yes. Only `generate` and `describe`
have it — cover, extend, remaster do not.

### Other spending commands

```
suno cover <clip_id> --no-captcha --model v6 --tags "<minimal cover style>" --audio-influence <0-100> --wait --json
suno remaster <clip_id> --no-captcha --model v6 --wait --json
suno extend <clip_id> --at <seconds> --no-captcha --model v6 --tags "<style>" --lyrics "<continuation>" --wait --json
```

- `cover` takes only `--tags --model --audio-influence` (no title, lyrics,
  exclude, weirdness, style influence). Keep its style prompt minimal; the
  source audio carries song and structure. Variety and Max Mode for covers
  are browser-route only.
- `remaster` on v6 sends Suno's v6 remaster model; strength
  (Subtle/Normal/High) is browser-route only. **Check availability first:**
  `suno credits --json` → `remaster_model_types[]` → the v6 entry's
  `can_use`. On 2026-10-03 the user's Premier account reported
  `can_use: false` for v6 (`chirp-halibut`). Then do not fire: say the
  account cannot remaster on v6 right now, offer Cover on v6 (a
  reinterpretation, ~10 credits) or checking Remaster in the web UI, and
  ask before spending on the alternative — the approval was for a
  remaster.
- `stems` (Auto Split 50 credits) and `delete`/`publish`/`set` mutate the
  account: confirmation rule.

### Recovery, status, library reads (no confirmation needed)

```
suno jobs --json                       # durable receipts: request id, state, clip ids
suno status <id> [<id>] --wait --json  # resume or check; never submits
suno info <clip_id> --json             # metadata: tags, prompt, duration, make_instrumental, type
suno list --json [--cursor <c>]        # newest first, paginated
suno search "<title or tags>" --json
suno credits --json ; suno models --json
```

A timeout or crash after submission: `suno jobs`, then `suno status <ids>
--wait`. Reusing the same `--request-id` with the same payload returns the
saved clips instead of paying again; never resubmit with a new id before
checking.

## The already-ran check (before every spend)

1. Read the pack's `runs/` — a prior log with the same `lyrics_sha256` +
   `style_sha256` means takes already exist; surface them, re-spending
   needs the user's reason.
2. Library: `suno search "<title>"` (or pp-cli library reads below).
3. Report the finding (or "no prior takes") in the confirmation line.

## Downloads — staging, then take-aware names

1. Parse clip ids from the generate/cover/remaster response (`data` is a
   list of clips).
2. `mkdir -p <pack>/_tmp/downloads` →
   `suno download <id1> <id2> --format mp3 --output <pack>/_tmp/downloads/ --json`
   (files arrive as `<title-slug>-<clipid8>.mp3`).
3. `mv` each into `<pack>/audio/<slug>-<model>-take<N>-<clipid8>.mp3`
   (model = the Settings model, e.g. `v6-wild`; N continues the pack's
   numbering). Never write into `audio/` directly, never overwrite.
   Verify every file exists before reporting.
4. Download caps apply (Pro 20/month, Premier 60/month): mention them when
   a pack plans many downloads.

## After the roll: verify what Suno actually did

- **Stored tags:** `suno info <id> --json` → `metadata.tags`. Equal to the
  sent style → the prompt ran as written. Different → Variety rewrote it;
  report the stored text (it is useful vocabulary) and note it in the run
  log. Observed 2026-10-03 (live, v6 and v6-wild): CLI renders send no
  Variety field, and both takes stored the style byte-identical — the API
  does not apply the UI's Normal default, so a faithful pack needs no
  browser route for Variety Off. Keep the check: testers report that a
  Variety rewrite shows up in the clip's style text.
- **Model:** `model_name` is not proof (v6-wild clips report
  `chirp-hawk`). The truth is the UI label, stored as
  `metadata.model_badges.songrow.display_name` (e.g. `V6-WILD`) — readable
  through the pp-cli library below.
- **Duration:** `metadata.duration` in seconds.

## Run logs — immutable publications

Every execution writes `<pack>/runs/<ISO-timestamp>-<promptfile>.json`.
Never edit an existing run log.

```json
{
  "request": {
    "pack": "<slug>",
    "prompt_file": "lyrics_v6.md",
    "route": "cli | browser | paste",
    "settings": {"model": "v6", "variety": "off", "personalize": "off", "weirdness": 35,
                 "style_influence": 75, "duration_s": 180, "max_mode": false, "vocal_gender": "female"},
    "cli_args": ["generate", "--no-captcha", "--model", "v6", "…"],
    "request_id": "<uuid>",
    "lyrics_sha256": "<first 10 hex>", "style_sha256": "<first 10 hex>",
    "not_applied": ["variety", "duration"]
  },
  "result": {
    "clips": [{"clip_id": "<uuid>", "model_label": "V6", "duration": 179.6,
               "file": "audio/<take-aware name>.mp3", "stored_tags_equal_sent": true}],
    "credits_before": 0, "credits_after": 0,
    "captcha": "open | required | solved-by-user | paste-route"
  },
  "lane": {"name": "…", "invariant": "…", "mutation_axis": "…", "expected_failure": "…"},
  "verdicts": {}
}
```

`lane` only for experiment rolls; `verdicts` fills via saga sync or the
human. Covers and remasters add `"parent_clip": "<seed id>"` per result
clip — the reliable parentage record. Never self-score listening
judgments; the skill has no ears.

## Library & saga sync — suno-pp-cli, read-only

suno-cli's `list`/`search`/`info` omit likes and cover lineage. The older
`suno-pp-cli` cannot generate on v6, but its **read-only library commands
still work on v6 clips** (verified 2026-10-03: `sync` pulled 860 clips incl.
v6 and v6-wild, with `is_liked`, `metadata.cover_clip_id`,
`major_model_version`, `metadata.model_badges`). Use it only for reads:

```
suno-pp-cli --agent sync --latest-only
suno-pp-cli --agent sql "select id, title, model_name, created_at,
  json_extract(data,'$.is_liked') liked,
  json_extract(data,'$.metadata.cover_clip_id') parent,
  json_extract(data,'$.metadata.model_badges.songrow.display_name') model_label,
  json_extract(data,'$.metadata.tags') tags,
  json_extract(data,'$.play_count') plays,
  json_extract(data,'$.metadata.duration') duration
  from clips where title in (…)"
```

Never run pp-cli `generate`, `cover`, `extend`, `remaster`, `project`, or
any other mutating command. If pp-cli is missing or its reads fail, saga
sync falls back to `suno search`/`suno info` (no likes, no lineage — say so)
or to the browser route for reading likes.

Saga sync loop: sync → clips by the pack's title(s) → lineage closure via
`cover_clip_id` both ways → strays (same time window, matching style
vocabulary, other titles) listed as QUESTIONS, never silently included or
dropped → journal merge under the sacred rules: one row per generation,
`is_liked` → at least "like" (mark which clip carries the ♥), never
downgrade, never overwrite a human verdict or note, absence of a like is
never "nope" → render the lineage tree as text, update the running credit
total.

## Verdicts and cover seeds

Verdicts are love / like / nope / hate (keep = like or better); no numeric
scores on art. Objective facts (glitches, dead air, wrong duration) go in
notes. Cover/remaster seeds: the human picks; the skill proposes citing
observables only — journal verdicts (outrank plays), `is_liked`,
play counts, lineage. Fresh takes with zero signal → ask.

## Credit table

| Action | Credits | Source |
|---|---|---|
| generate v6 / v6-wild / v6-mini (2 songs) | 10 | observed 2026-10-03 (2,707 → 2,697 → 2,687) |
| same with Max Mode | 20 | Suno app tooltip |
| cover, remaster, extend | ~10 (assumed; confirm via credits before/after) | not yet observed on v6 |
| stems: Auto Split / Split from Mix | 50 / 10 per stem | Suno help 13925185 |
| dry-run, downloads, library reads, doctor | 0 | observed |

Track a running per-pack total across run logs; state it in every
confirmation line.
