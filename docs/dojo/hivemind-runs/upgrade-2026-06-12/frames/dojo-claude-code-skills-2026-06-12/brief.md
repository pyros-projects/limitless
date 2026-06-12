# Hivemind brief — what Reddit says about Claude Code skills (shallow pass)

> Coverage warning up front: the `rdt` CLI is not installed, so this is a
> degraded pass — SearXNG snippets of Reddit threads, no comment deep-reads.
> **10-second fix: `uv tool install rdt-cli`** — say the word and a proper
> sweep (comment mining of the top threads) is possible.

## TL;DR

Reddit treats Claude Code skills as a maturing ecosystem worth curating:
the dominant post genre is "which skills are actually worth installing,"
with recurring names like frontend-design, Superpowers, hooks-related
skills, and Skill Seekers [observed in snippets]. The communities are
r/ClaudeAI and r/ClaudeCode. Enthusiasm is high but two frictions recur:
newcomers are confused about what skills *are* versus subagents/memory,
and even experienced users report skills failing to trigger consistently.
Meta-usage (skills that build skills) and serious multi-agent
architectures built on skills+subagents show the power-user end.

## Consensus [claimed by posters; snippet-level evidence only]

- **Curation is the conversation.** "The Claude Code skills actually worth
  installing right now (March 2026)" [r/claude, 1s51b5u]; "I tested 30+
  community Claude Skills for a week" [r/ClaudeAI, 1ok9v3d] ("Community
  skills are a must. Claude Code user? Hooks + Superpowers are
  non-negotiable"); "30+ Skills collection — dev, planning, docs,
  architecture, diagrams" [r/ClaudeAI, 1qjaq92]; "Top Claude Code skills I
  used to build mobile apps" [r/ClaudeCode, 1s2dacs].
- **Skills compose into real systems.** Multi-agent editorial team for
  novel writing: 7 reviewer agents + 1 revision agent, built on Skills +
  subagents [r/ClaudeAI, 1pd7847].
- **Meta-skills are a thing.** "This Claude Code Skill Creates Claude Code
  Skills For You" — a create-agent-skill walkthrough [r/ClaudeAI, 1p0n7pg].
- **Triggering reliability is a known pain.** "Getting Claude skills to
  invoke consistently with Claude Code" [r/ClaudeAI, 1pu0pmb, Dec 2025],
  cross-linking "Why does Claude Code ignore my /skills?" [r/ClaudeCode,
  17↑, 13 comments].
- **Active demand thread:** "What are your most useful Claude skills?"
  [r/ClaudeCode, 1spvmtu, 125↑, 87 comments] — the single best deep-read
  target once rdt exists.

## Contested / unclear

- **What skills even are.** "What are Claude skills really?" [r/ClaudeAI,
  1oalv0o, Oct 2025] — posters compare them to Claude Code's memory system
  and custom subagents; positioning confusion persists months later.
  Unresolved at snippet level.
- **Install mechanism claim [claimed, unverified]:** one post describes
  loading skills via `/skill load <raw-github-url>` [r/ClaudeCode,
  1s2dacs] — this does not match known Claude Code commands; likely
  paraphrase or third-party tooling. Needs verification against docs.

## Best takes (verbatim from snippets)

- "Community skills are a must. Claude Code user? Hooks + Superpowers are
  non-negotiable. Working with custom/internal tools? Skill Seekers
  changes ..." [r/ClaudeAI, 1ok9v3d]
- "I've been telling myself that I'll start using skills when I notice
  myself doing something repeatedly in Claude Code ..." [r/ClaudeCode,
  1spvmtu]

## Freshness & coverage

- Window observed: Oct 2025 – Mar 2026 (snippet dates); no window enforced.
- Reddit: SearXNG snippets only (1 query, top 10) — rdt missing, so no
  scoped venue passes and no comment mining. Weak-evidence surface, weaker
  than usual.
- X: 2 shallow passes (floor 50, then adapted to 25) → 0 results; platform
  dropped, coverage flagged.
- Rejected: r/vibecoding Antigravity/Gemini combo post (off-topic);
  details in manifest.md.

## Next directions

1. **Install rdt** (`uv tool install rdt-cli`) and deep-read the two
   highest-value threads: 1spvmtu (125↑/87 comments, "most useful skills")
   and 1ok9v3d ("tested 30+ skills") — the actual answers live in those
   comments.
2. **Verify the `/skill load <url>` claim** against official Claude Code
   docs/changelog — likely wrong, and it's load-bearing for anyone
   following that mobile-apps post.
3. **Deepen the triggering-consistency friction** (1pu0pmb + the
   ignore-/skills thread) — directly relevant to this repo's dojo skill
   work on trigger tuning.
4. **Retry X** with unquoted variants ("claude skills", "agent skills") or
   searxng `categories=social+media` to see if the zero was query-shaped
   rather than genuine silence.
