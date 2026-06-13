# GitHub Playbook — gh as a hivemind venue

Evidence grade: **medium** — repo metadata is factual (stars, dates,
releases are `[observed]`), but stars measure popularity, not quality,
and README claims are `[claimed]` like any other self-description.

## Preflight

```bash
gh auth status   # SAY which account is active in your reply
```

Account identity matters: recipes that touch specific orgs (issue
delivery steps in configs, private repos) silently fail or — worse —
act as the wrong identity. If the active account isn't the one the
recipe needs, stop and say so; never `gh auth switch` without telling
the user.

## Recipes

**Discover — trending by creation window (primary):**

```bash
gh search repos --created=">2026-05-29" --sort=stars --limit 10 --json fullName,stargazersCount,createdAt,description -- "<topic terms>"
gh search repos --topic=<topic-slug> --created=">-3 weeks" --sort=stars --limit 10
```

This finds *new* breakouts. For "trending" in the velocity sense
(established repos gaining now), the API has no endpoint; the public
trending page works without auth and may be fetched + parsed with a
throwaway parser (record it in raw/ like any other source):

```bash
curl -s "https://github.com/trending?since=weekly" -o "$FRAME/raw/gh-trending.html"
```

Parse the `<h2>` anchors, not sponsor links (observed trap 2026-06-12:
naive regex grabs sponsor URLs for some entries).

**Enrich — per-entity factual lookup:**

```bash
gh repo view <owner>/<repo> --json stargazerCount,createdAt,pushedAt,latestRelease,description,forkCount
gh api repos/<owner>/<repo>/releases --jq '.[0:3] | .[] | {tag_name, published_at}'
```

An entity ask ("most mentioned repos") is incomplete without this
stage — mention counts without stars/recency/what-it-is is half an
answer.

**Landscape check** (who else is in this space):

```bash
gh search repos --sort=stars --limit 15 --json fullName,stargazersCount,pushedAt -- "<concept>"
```

## Engagement proxies & triage

- **Stars-per-day** since creation, not raw stars — 800★ in 2 months
  beats 3k★ in 4 years for trend signal.
- **Release recency + cadence** — a starred-but-dormant repo is
  archaeology, not a trend.
- **Fork ratio** — high forks/stars suggests use, not just bookmarking.
- **Star-farming caveat**: README-driven star spikes (launch-day HN/X
  pushes) are popularity events; check whether issues/PRs show actual
  use before reading stars as adoption. Label the distinction.

## Collision traps

Repo names collide with everything — generic words ("memory",
"agent"), older same-name projects, research-paper names. Before using
an entity name as a search term in another venue:

- Qualify with org (`"acme-ai/memory"`), URL
  (`github.com/acme-ai/memory`), or context terms.
- Keep a collision register in the manifest: which names are
  ambiguous, what qualifier was chosen, what got rejected because it
  matched the wrong thing.
- A hit counts as reaction to THIS repo only if it names org/repo,
  links the URL, or unambiguously describes it.

## Quirks

- `gh search repos` `--created` accepts both `">2026-05-29"` and
  relative `">-3 weeks"` forms.
- `--json` field names differ between `gh search repos`
  (`stargazersCount`) and `gh repo view` (`stargazerCount`). Check with
  `--json` and no fields to list what's available.
- Search rate limits are generous but real on bursts; batch per-entity
  enrichment with `--jq` instead of one call per field.
