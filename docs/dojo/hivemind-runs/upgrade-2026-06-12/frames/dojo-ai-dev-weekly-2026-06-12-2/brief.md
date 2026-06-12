# Hivemind Brief — repeat dojo-ai-dev-weekly (2026-06-12-2)

Config: dojo-ai-dev-weekly **edition 1** | Mode: trend scan | Window: 2026-05-29 → 2026-06-12 (14d)
Depth: **SHALLOW per config sandbox override** (1 query/venue, n=10, research step skipped)
Chain (config-authored): `social(reddit×7, x) ∥ gh(trending + SDD landscape + OpenSpec enrich) → diff(prev frame ../2026-06-12/) → delivery(issue-draft.md, German)`

## TL;DR

Same-day shallow re-sweep; everything the morning frame reported still dominates
(Copilot billing revolt, Fable 5 cost routing, deterministic backlash). The
**material developments** since that frame: agent security broke out of theory —
a documented prompt-injection/malware incident in r/opencode plus Microsoft
announcing MDASH (agentic vulnerability discovery for Copilot CLI); a high-traction
`[claimed]` story that Anthropic intentionally degrades Fable 5 on competitor-LLM
development work, sourced to Anthropic's own technical report p.13 (unverified —
research step skipped per sandbox override); and the Copilot app's waitlist
removal (June 10), which also corrects the previous frame's "GA" framing to
"expanded technical preview for all paid plans."

## Consensus / new findings (with receipts)

**1. Agent harnesses are now an attack surface — incident-grade [observed]**
- r/opencode user documents auto-created `wget` sessions pulling arch-specific
  binaries from a compromised WordPress URL, with no webfetch/websearch records
  around them [r/opencode 1u3044z, 93↑/28c, 06-11]. Top comment [31↑]: "This is
  malware. Check your skills, MCPs, and plugins." A commenter extracted the
  actual dropper one-liner from the DB.
- Vendor echo same week: MDASH — "agentic vulnerability discovery and
  remediation… coming soon to GitHub Copilot CLI" [@msdev, 79 likes, 06-11]
  `[claimed]`/[unverified]. Cross-grade echo with last frame's
  anthropics/defending-code-reference-harness repo → strongest-signal label.

**2. Model neutrality is contested — `[claimed]`, unverified**
- "Anthropic is intentionally nerfing Fable when asked to develop other LLMs"
  [r/LocalLLaMA 1u1s2oz, 1490↑/380c, 06-10]. Claim anchored to Anthropic's own
  technical report (www-cdn.anthropic.com/d00db56…20.pdf, p.13). Top comments:
  "taking your money and poisoning your code base" [593↑]; "mask-off moment"
  [309↑]; screenshot claim that Fable is blocked from reading its own technical
  report [248↑]. **Marked [unverified]: the config's verification step was
  skipped per the sandbox override.** High enough engagement + a primary-source
  pointer that it goes in the draft with the flag, not silently dropped.

**3. Copilot app: waitlist gone, preview for all paid plans [observed]**
- "No more waitlist. The GitHub Copilot app's technical preview is now available
  to everyone currently on Copilot Pro, Pro+, Max, Business, and Enterprise
  plans." [@github, 703 likes, 06-10]. Earlier: "expanded technical preview"
  [@github, 113 likes, 06-02]. **Corrects the previous frame's "Copilot app GA'd
  June 11" line — it is a technical preview, not GA.**
- Fable 5 GA in Copilot [@github, 2095 likes, 06-09] — already reported,
  diff-dropped.

**4. Local-model practitioner consensus [observed, satire-wrapped]**
- "Stop asking what model to run. There are literally only two." [r/LocalLLaMA
  1tu82wi, 2831↑/709c, 06-01] — post is deliberate rage-bait/satire (community
  calls it out [76↑]), but the comment layer carries a real consensus: Qwen 3.6
  (35B-A3B / 27B) for coding, Gemma 4 for creative work [710↑, 625↑].

**5. gh newcomers (full table in gh-trending.md)**
- `superloglabs/superlog` [gh, 790★, created 06-02] — AI agents self-healing
  software (observability).
- `DietrichGebert/ponytail` [gh, 772★, created **06-12**] — "laziest senior dev"
  skill; the social trend from the previous frame's manifest became a repo
  within days.
- `study8677/awesome-architecture` [gh, 1326★, created 05-23] — RAG/agent
  architecture tutorials.
- OpenSpec: still v1.4.1 (06-03), no new release since the previous frame.

## Contested

- **The nerfing claim**: vendor-policy sabotage vs alignment-side-effect — the
  thread itself contains no Anthropic response; unresolved, and this run could
  not verify (step skipped). Not averaged; carried as [claimed]+[unverified].
- **The opencode incident**: top comments split between prompt injection via
  poisoned context (skills/MCPs/codebase) [31↑] and a mundane exposed
  0.0.0.0 server [8↑]. Unresolved in-thread; both diagnoses imply the same dev
  action (audit skills/MCPs, don't expose the agent server).

## Best takes

> "This is malware. Check your skills, MCPs, and plugins. If you started
> working on someone else's codebase… check if it has some hidden malicious
> instructions trying to taint the agent context." — [r/opencode, 31↑]

> "A refusal or HTTP-4xx error for content is fair enough, but this is
> basically taking your money and poisoning your code base." — [r/LocalLLaMA, 593↑]

## Freshness & coverage

- Window 2026-05-29 → 2026-06-12; venues: r/GithubCopilot, r/AI_Agents,
  r/ClaudeAI, r/LocalLLaMA, r/Rag, r/LangChain, r/opencode (config list, <1
  month old, recon re-confirmation not required), X (1 query: "github
  copilot"), gh (4 enumerated pipeline lookups).
- **Chain ran as stated above.** All preflight probes green (twitter auth ok,
  rdt auth ok, gh active account pyros-projects, SearXNG 200 — web unused, step
  4 skipped).
- **Depth adaptations (operator override, not tool failure):** SHALLOW — one
  `rdt sub <venue> -s top -t month -n 10` per sub (config's week+month pair
  collapsed to month + 14d date-filter at triage, to keep full window coverage
  in one query); one X query (priority topic 1, known CLI trap honored — no
  `--exclude retweets` with min-likes+lang); gh's 4 explicitly enumerated
  lookups all ran with limit 10 (read as named contract steps, not open-ended
  fan-out); deep-reads capped at 3; codies-research step skipped → all News
  flagged [unverified].
- **Triage rejections (named):** r/ClaudeAI 1tz1tzv "responding like Claude"
  (19194↑) and 1u18cey "I'm ready" (5454↑) — memes, no knowledge;
  r/LocalLLaMA 1tw8eul "Me visiting this sub" (2098↑) + 1ttn15z Jensen meme
  (1473↑) — memes; r/AI_Agents 1tty1og beginner thread (136↑) — wrong
  audience; X @kentcdodds built-in-game tweet (169 likes) — fluff; gh:
  Duel-Agents (942★) dropped from draft — description too thin to state a
  "why" without the skipped research step; gh off-topic list in gh-trending.md.
- **Diff-dropped (already in ../2026-06-12/brief.md):** Copilot billing-revolt
  threads (1tv77df, 1tuot1q, 1ttlrsq…), Fable 5 routing (1u1cyx1), rip-AI-out
  (1u067cf), HITL theater, team-killed-agent, RAG 4-approaches/RAGAS/PDF-parsing
  threads, framework-fatigue (1u05gn6 ≈ prev 105↑ item), SDD harness (1ttts4v),
  Gemma 4 drop, OpenSpec v1.4.x releases, all previously listed trending repos.
- **Staleness check (threshold: 2 consecutive thin frames):** topic 3 (loop
  engineering) had zero dedicated hits this run — but at SHALLOW depth with no
  dedicated query this does not count as a thin frame; not incremented, noted
  for the next full run. No replacement proposed.
- Auto-save to codies-memory inbox **not performed**: operator constraint
  restricts writes to ~/.hivemind/dojo-ai-dev-weekly/ this run.

## Next directions

1. Verify the Anthropic-nerfing claim against the technical report PDF (p.13)
   and any Anthropic response — it's the draft's riskiest [unverified] item.
2. Re-run at full depth before the actual meeting: loop-engineering and
   OpenSpec/X coverage were structurally thin at SHALLOW (1 query/venue).
3. Watch `DietrichGebert/ponytail` star velocity for a week — 772★/day-one is
   either a breakout or a star-farming event; issues/PRs will tell.
4. Deep-read the opencode incident follow-ups (`rdt read 1u3044z` next frame)
   — if the maintainers respond, it becomes a teachable security item for the
   monthly.

## Crystallize pass

No user-steered deviations occurred this run (non-interactive sandbox repeat);
no tool failures. **No config deltas proposed; edition stays 1.** The
"GA → technical preview" correction is a *content* fix carried in the draft,
not a config change.
