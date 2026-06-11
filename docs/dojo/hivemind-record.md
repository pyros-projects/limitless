# Dojo record — hivemind

*Tier: technique · 2026-06-11 · Claude (Fable 5) + Pyro*

## Baseline findings (RED)

Run 2026-06-11, fresh general-purpose subagents, no skill. Honest note:
baseline quality far exceeded the concept doc's assumptions — both agents
self-corrected away from unscoped-search garbage and produced strong
briefs. The frontier-headroom insight cuts both ways. The skill's value
is in the specific gaps below, consistency across runs, token efficiency
(S1 burned 85k tokens, S3 94k — much of it on reinventable plumbing), and
the radar/series machinery no baseline produces.

| Scenario | Criterion | Result | Failure mode observed |
|---|---|---|---|
| S1 | 1 recon before scoped | ⚠️ | Broad X sweep first, yes — but Reddit went scoped immediately |
| S1 | 2 venues from recon, not assumption | ❌ | Subreddits (r/LocalLLaMA, r/AI_Agents…) chosen from priors; first unscoped `rdt search` returned r/all garbage incl. a 600KB post, agent adapted by *assuming* venues rather than frequency-counting results |
| S1 | 3 time-windowed sorting | ✅ | `--since`, top/month used |
| S1 | 4 engagement floors on X | ✅ | `--min-likes 50` |
| S1 | 5 explicit relevance triage | ❌ | Filtering happened implicitly; no stated rejection of high-engagement off-topic items |
| S1 | 6 deep-read ≥2 threads | ✅ | 4 Reddit posts w/ comments, tweet replies pulled |
| S1 | 7 receipts w/ engagement | ✅ | Throughout |
| S1 | 8 next directions | ❌ | None offered |
| S3 | 1 detected missing CLI | ✅ | (given in env note; no `command -v` check performed) |
| S3 | 2 offered install | ❌ | Never mentioned `uv tool install rdt-cli`; instead burned ~6 failed workaround attempts (reddit.com JSON 403, pullpush, jina proxy…) before finding a working redlib instance |
| S3 | 3 continued without blocking | ✅ | Exceeded: got Reddit data via redlib anyway |
| S3 | 4 flagged reduced coverage | ✅ | Rate-limit gaps caveated |
| S2 | (pre-recorded evidence) | ❌ | Manual smoke test 2026-06-11: global `rdt search "suno prompt" -s top` → r/CuratedTumblr + r/antiai viral noise; X top-search → 2k-like off-topic prompting tweets. Note: agent-level baselines partially self-correct; the skill makes the correction *systematic*. |

**Curriculum (what the skill must teach explicitly):**
1. Venue resolution is a *procedure* (frequency-count the recon results), not a vibe or a prior.
2. Relevance triage is *stated*: name what was rejected and why, or state nothing needed rejection.
3. The brief always ends with 2–4 next directions.
4. Degradation protocol: missing CLI → offer the 10-second `uv tool install` BEFORE any proxy spelunking; continue single-platform while the user decides.
5. Preserve baseline strengths — don't suppress initiative (link resolution, ad-hoc parsing, caveat-flagging were all good).

## Loopholes closed

(to be filled in kata 4)

## Rejected fixes

| # | Attempted edit | Why it didn't survive |
|---|---|---|

## Graduation

(to be filled in kata 5 — H1, H2 untouched)

## Trigger matrix

(to be filled in kata 6)

## Known limitations

(to be finalized at ship)
