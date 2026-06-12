# Hivemind brief — what Reddit says about Claude Code skills (shallow pass, re-sweep)

> **Coverage warning first: the `rdt` CLI is not installed.** 10-second
> fix: `uv tool install rdt-cli` — with it, a proper sweep (scoped venue
> passes + comment mining) becomes possible. Everything below is
> **proxy-of-reddit** (SearXNG `site:reddit.com` snippets): no comments
> read, engagement numbers only where snippets exposed them. A frame for
> this exact ask already ran earlier today (`2026-06-12`); this brief
> reports the *diff* — new threads and themes — on top of it.

## TL;DR

Reddit's Claude Code skills conversation has three layers. The dominant
genre is still curation — "which skills are worth installing" lists,
now up to 92-skill open-source packs [observed in snippets]. Beneath it
sits a persistent comprehension problem: from Oct 2025 through Apr 2026
the communities keep producing "skills vs subagents vs commands"
explainers and cheat sheets, which means the mental model still isn't
landing. New in this pass: a visible skeptic minority ("struggling to
see the value", "are skills worth using?") and a sharp criticism of the
Agent Skills spec integration — plus the claim that skills are becoming
a cross-harness standard (Codex CLI, Gemini CLI), and a dedicated
r/claudeskills subreddit. Venues confirmed: r/ClaudeAI and r/ClaudeCode
primary; r/claude, r/AI_Agents secondary.

## Consensus [claimed by posters; snippet-level evidence only]

- **Skills are the current meta.** "Agent Skills tops the trends right
  now. Earlier it was custom commands + MCP. So focus your energy on
  getting the right set of Agent Skills in" [r/ClaudeCode, 1pxou18,
  Dec 2025]. The ecosystem ships volume: "I built 92 open-source
  skills/agents for Claude Code" [r/ClaudeCode, 1sf75oz, Apr 2026];
  "10 Claude Skills that actually changed how I work (no fluff)"
  [r/ClaudeAI, 1ojuqhm] — whose comments also surface a macOS app for
  managing skills across projects [claimed].
- **The concept-confusion industry is steady.** "Understanding Claude
  Skills vs. Subagents. It's not that confusing" [r/ClaudeAI, 1obq6wq,
  Oct 2025]; "When should I use a Skill, a Slash Command, or a
  Sub-Agent" [r/ClaudeAI, 1orozs4, Nov 2025]; "Give me examples of
  Claude skills that are useful vs agents" [r/ClaudeCode, 1oz0ed8,
  Nov 2025]; "Help me understand: agents vs skills" [r/ClaudeAI,
  1s5bo5v, ~Apr 2026]. An "Agent Skills Cheat Sheet" [r/ClaudeCode,
  130↑, 12 comments, via snippet cross-ref] exists because demand
  exists. Six months in, this friction has not closed.
- **Skills travel beyond Claude Code [claimed].** "The Agent skills are
  compatible with all major harnesses like claude code, codex cli and
  gemini cli" [r/ClaudeAI, 1q5i4a5, Jan 2026]. Consistent with the spec
  framing in 1qcigma's title ("The spec unified us").
- **Skills + MCP is a liked combination.** "Claude Agent Skills are
  really awesome, and much better with MCP tools" [r/AI_Agents,
  1ohc97r, Oct 2025].
- **Meta-skills keep developing.** The "create-agent-skill" meta-skill
  (reported in the prior frame) crossposted to r/ClaudeCode with a new
  detail: a "Heal Skill" repair system [r/ClaudeCode, 1p0n64q].
- **Cross-sub echo:** the March 2026 curation post and the meta-skill
  post are both crossposted across subreddits — same stories, clustered
  as one each; echo flagged as reach, not extra validation.

## Contested / unclear

- **Are skills actually worth it?** A skeptic minority is visible:
  "Struggling to See the Value of Claude Code Skills & Agents — What Am
  I Doing Wrong?" [r/ClaudeAI, 13↑, 27 comments, via snippet cross-ref]
  and "Are Claude Code skills worth using?" [r/claude, 1typx6i, ~6 days
  old]. Against the enthusiast majority, unresolved at snippet level —
  the 27-comment thread is where the resolution would live.
- **Spec/implementation criticism [claimed, single source]:** ""Agent
  Skills" — The spec unified us. The paths divided us... made me
  realize the Claude Code devs don't know what they are doing and just
  use Claude to write itself" [r/ClaudeCode, 1qcigma, Jan 2026].
  Apparently about skill path/discovery handling across harnesses; one
  poster's take, no counter-weight readable at snippet level.

## Best takes (verbatim from snippets)

- "Agent Skills tops the trends right now. Earlier it was custom
  commands + MCP." [r/ClaudeCode, 1pxou18]
- "The spec unified us. The paths divided us." [r/ClaudeCode, 1qcigma]
- "The Agent skills are compatible with all major harnesses like claude
  code, codex cli and gemini cli" [r/ClaudeAI, 1q5i4a5]

## Freshness & coverage

- Window observed: Oct 2025 – Apr 2026 (snippet dates; freshest item
  ~6 days old); no window enforced.
- Venue: Reddit only, as named — via **proxy-of-reddit** (2 SearXNG
  site-scoped queries, top 10 each). No scoped subreddit passes, no
  comment mining (rdt missing). Chain: none (single-venue ask).
- X deliberately not used: named-venue ask; prior same-day frame also
  logged 0 X hits on this topic.
- Triage: no off-topic rejections; dedups and crosspost clustering
  listed in manifest.md. Four previously-reported threads dropped via
  diff against the morning frame.
- Evidence grade: social, snippet-level — weaker than hivemind's normal
  reddit floor. Nothing here is validated; all engagement-backed claims
  are [claimed].

## Next directions

1. **Install rdt** (`uv tool install rdt-cli`) and deep-read the two
   highest-leverage threads this pass surfaced: the 27-comment
   "Struggling to See the Value" thread (the skeptic case, answered by
   practitioners) and 1qcigma (the spec criticism — relevant to anyone
   building skills for multiple harnesses).
2. **Verify the cross-harness claim** [1q5i4a5] against primary
   sources: the agentskills spec repo / Codex CLI and Gemini CLI docs —
   if true, it changes what "writing a skill" targets.
3. **Recon r/claudeskills** as a venue: subscriber count and post
   velocity decide whether future sweeps should scope it.
4. **Widen to X with unquoted variants** ("claude skills", "agent
   skills") to test whether the prior frame's 0-hit X result was
   query-shaped rather than genuine silence.
