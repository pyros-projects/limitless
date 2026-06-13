# Packaging — Limitless Conventions, Ship Checklist, Dojo Record

## Limitless Layout

```
plugins/limitless/skills/<name>/
  SKILL.md          # required: frontmatter (name, description) + body
  references/       # optional: docs loaded on demand, pointed to from SKILL.md
  assets/           # optional: files used in output (templates, images)
  scripts/          # optional: executable helpers (rare — prefer judgment over plumbing)
```

Skills are auto-discovered from `plugins/<plugin>/skills/` — no
registration entry for the skill itself.

House style:

- Description: pushy, third person, "This skill should be used when…"
  plus a "Responds to 'X', 'Y', 'Z'…" trigger-phrase list. Frontmatter
  name+description under 1024 characters AND strictly parseable YAML —
  VALIDATE at kata 7, don't eyeball it. Codex's loader hard-rejects both
  over-limit descriptions (suno-pack at 1139, 2026-06-12) and unquoted
  `: ` colon+space inside the description value (suno-pack again, same
  day, two hours later — "mapping values are not allowed"). Claude Code
  tolerates both silently. The gate:
  `uv run --with pyyaml python -c "import re,yaml;s=open('SKILL.md').read();d=yaml.safe_load(re.match(r'^---\n(.*?)\n---',s,16)[1]);assert isinstance(d['description'],str);n=len(d['name'])+len(d['description']);assert n<1024,n;print('frontmatter OK',n)"`
- SKILL.md body under ~350 lines; heavy detail goes to `references/`
  with explicit "read this when…" pointers (index-document pattern).
- No scripts unless the host genuinely can't do the job with judgment.

## Ship Checklist

1. `plugins/limitless/.claude-plugin/plugin.json` — bump `version`, add
   the skill to the `description` sentence.
2. `.claude-plugin/marketplace.json` (repo root) — update the limitless
   entry's `description` the same way.
3. Root `README.md` — limitless plugin table row: skill count and
   what-it-does cell.
4. Per-plugin `README.md` (`plugins/<plugin>/README.md`) — add the skill
   to its table (What It Does / When to Reach For It). Missed on
   hivemind's first ship — caught by Pyro 2026-06-11.
5. `/reload-plugins` — confirm the skill appears in the listing.
6. Smoke-invoke once with a tiny real input.
7. Persist the full evidence set under
   `~/.limitless/dojo/<repo-slug>/<skill>/`:
   `<skill>-scenarios.md` (battery + verbatim prompts as sent),
   `<skill>-runs/` (every test workspace's output files + README table).
8. Write/finalize the dojo record (below) linking both, commit, push.

## Dojo Record Template

One record per skill at
`~/.limitless/dojo/<repo-slug>/<skill>/<skill>-record.md`. The record is
the skill's belt rank: proof of what was tested, what broke, what was
fixed, and what is known not to hold. Copy only curated summaries or
examples into a target repo, and only when the user explicitly wants
checked-in documentation.

```markdown
# Dojo record — <skill>

*Tier: <discipline|technique|reference> · <date> · <author>*

## Baseline findings (RED)

| Scenario | Failure mode observed |
|---|---|
| S1 … | … |

## Loopholes closed

| # | Loophole | Edit that closed it |
|---|---|---|

## Rejected fixes

| # | Attempted edit | Why it didn't survive |
|---|---|---|

## Graduation

| Holdout | Result | Notes |
|---|---|---|

## Trigger matrix

| # | Prompt | Expected | Got (run 1 / run 2) | Pass |
|---|---|---|---|---|

Score: X/N · Collisions: <none | list>

## Known limitations

- …
```

Sections that don't apply to the tier are kept with an explicit
"n/a — <reason>" rather than deleted; an absent section reads as
forgotten, a marked one reads as decided.
