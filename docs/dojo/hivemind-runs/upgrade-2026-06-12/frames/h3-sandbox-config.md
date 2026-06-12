# Config — dojo-ai-dev-weekly

> Living recipe. Crystallized from the 2026-06-12 session (first run).
> Update via propose-confirm only — never silently rewrite user intent.
> Frames under ./<date>/ are immutable episodes; this file is the contract
> for the next run. "repeat dojo-ai-dev-weekly" executes this file.

- edition: 1
- derived_from: ./2026-06-12/ (manifest.md, brief.md, gh-trending.md, codie-research.md)
- cadence: weekly (before the weekly AI dev meeting)
- window: last 14 days

## Intent

Prepare the weekly AI dev meeting issue so senior leads can collect topics
for the company-wide AI monthly. Audience includes AI-skeptic devs who only
hear about AI here: paradigm/concept shifts must be prominent and explain
why they are happening AND why they apply to the reader (defuse "I just
don't use it"). Devs use GitHub Copilot + OpenSpec — news in those two
ecosystems is priority signal.

## Topics (staleness rule: thin results in 2 consecutive sweeps → propose replacement)

1. GitHub Copilot ecosystem (features, billing, models, changelog context)
2. Spec-driven development — OpenSpec specifically (releases, funding, competitors)
3. New concepts/paradigm shifts (current: loop engineering; rotate as discourse moves)
4. Building agentic software: RAG applications, enterprise agents
5. Trending skills/tools/libraries devs would actually use
6. Major dev-related AI news (model releases, tool shutdowns/pivots, pricing)

## Pipeline

1. **Delivery target**: this sweep delivers into a local draft file
   ./<date>/issue-draft.md (sandbox run — no GitHub issue access).
2. **Hivemind trend-scan** (this folder's frame contract):
   - Venues (re-confirm via recon if >1 month old): r/GithubCopilot,
     r/AI_Agents, r/ClaudeAI, r/LocalLLaMA, r/Rag, r/LangChain (+r/opencode fringe)
   - Reddit: `rdt sub <venue> -s top -t week -n 25 --json` AND `-t month`,
     date-filter to window at triage (no native 14d sort)
   - X: `twitter -c search '<query>' -t top --min-likes 50 --lang en --since <window-start> -n 30 --json`
     ⚠️ do NOT combine `--exclude retweets` with min-likes+lang (returns empty, CLI bug as of 2026-06)
   - Known keyword traps: unscoped "RAG" (rags/sharks), unscoped "agentic"
     (non-tech agents) — always scope to venues
   - Deep-read 3-5 top threads (`rdt read <id> -s top --json`, shape: data[0]=post, data[1]=comments)
3. **gh trending**: `gh search repos --created=">-3 weeks" --sort=stars` (overall +
   "agent" keyword), plus SDD landscape check ("spec driven development" by stars
   with pushedAt) and OpenSpec releases (`gh api repos/Fission-AI/OpenSpec/releases`)
4. **Research/verify** (codies-research): every News item needs a primary source
   + date; flag satire/unverified explicitly (e.g. r/InterstellarKinetics is satire);
   parallel WebSearch batches per claim
5. **Diff vs previous frame**: read last frame's brief.md; do not re-report
   stories already presented — only material developments
6. **Write the draft** into ./<date>/issue-draft.md with the output
   format sections below (no checkboxes/Notes handling in sandbox).

## Output format (issue body sections)

- Sections: `## 💡 Konzepte`, `## 📦 Repos`, `## 📰 News`, `## 🧩 Andere Themen`
- **German**, one flowing paragraph per item — NO "What it is / Why it matters"
  label structure
- Every item: 1–2 links to good sources + short explanation incl. why it
  matters for devs; news items: date + key facts + action point where relevant
- Konzepte: max 3, the paradigm shift of the window gets the longest paragraph;
  anchor new concepts to what the team already does (e.g. "üben wir mit
  OpenSpec-Specs schon")
- Repos: ~5 one-liners with a "why"
- Flag deadlines prominently (e.g. free windows, EOL dates)
- Public-safe: no private ecosystem names in issue content

## Persistence

- Everything (raw JSON, brief.md, manifest.md, gh-trending.md,
  codie-research.md) into ./<date>/ per the frame contract; frames immutable
- After each run: propose config updates for any user deviation observed
  this session; bump edition + changelog below on accept

## Changelog

- e1 (2026-06-12): crystallized from first run. Mid-session corrections that
  shaped this config: window 7d→14d; topics extended with RAG/enterprise
  agents; output switched to German single-paragraph format; What/Why label
  structure explicitly rejected.

## Sandbox depth override (operator)

- SHALLOW: max 1 query per venue, -n 10; skip the codie-research
  step (step 4) — mark News items [unverified] instead.
