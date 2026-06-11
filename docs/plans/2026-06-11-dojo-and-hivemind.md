# Dojo + Hivemind Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Context note (overrides the default recommendation):** the authoring
> tasks in this plan depend on heavy conversation context (design
> decisions, SkillOpt borrow rationale, fanzine template choice). Inline
> execution (superpowers:executing-plans) is the right mode here; fresh
> subagents are used *inside* tasks for dojo test runs, where zero
> context is exactly the point (lesson LS-G0009).

**Goal:** Build the `dojo` skill (skill-writing with verification discipline), then dogfood it by building `hivemind` (social-media search via twitter-cli + rdt-cli) as its first student.

**Architecture:** Two phases. Phase A writes dojo as a lean SKILL.md + three references in the limitless plugin, then runs dojo's own trigger eval (recursion). Phase B runs hivemind through all seven dojo kata: intake scenarios with holdouts → baseline RED runs → write SKILL.md + references → pressure-test with bounded edits → graduation → trigger eval → package with dojo record.

**Tech Stack:** Markdown skills (Claude Code plugin format), Agent tool subagents for all testing, twitter-cli + rdt-cli for hivemind's live runs. No python, no build step.

**Required reading before executing (canonical sources):**
- `docs/brainstorm/2026-06-11-dojo-skill-design.md` — the dojo spec (the seven kata, tiers, evidence base)
- `docs/brainstorm/2026-06-11-hivemind-social-search-skill.md` — the hivemind concept (search flow, radar mode, decisions)
- `docs/brainstorm/hivemind-mockups/04-fanzine.html` — the chosen radar template

---

## File structure

```
plugins/limitless/skills/dojo/
  SKILL.md                          # Task 1 — the loop, tiers, measurability rule
  references/
    pressure-testing.md             # Task 2 — scenarios, pass criteria, subagent prompts
    trigger-evals.md                # Task 3 — matrix design, scoring, collision checks
    packaging.md                    # Task 4 — limitless conventions, dojo record template
docs/dojo/
  dojo-record.md                    # Task 5 — dojo's own trigger-eval record
  hivemind-scenarios.md             # Task 6 — intake artifact (scenarios + holdouts)
  hivemind-record.md                # Tasks 7–13 — accumulated dojo record for hivemind
plugins/limitless/skills/hivemind/
  SKILL.md                          # Task 8
  references/
    x-playbook.md                   # Task 9 — twitter-cli recipes + floors
    reddit-playbook.md              # Task 9 — rdt recipes + venue resolution
    radar.md                        # Task 9 — radar pipeline, KG schema, sweep series
  assets/
    radar-template.html             # Task 9 — copy of 04-fanzine.html
plugins/limitless/.claude-plugin/plugin.json   # Task 13 — version + description bump
.claude-plugin/marketplace.json                # Task 13 — limitless entry description
README.md                                      # Task 13 — skill count + table row
```

---

## Phase A — Build dojo

### Task 1: dojo SKILL.md

**Files:**
- Create: `plugins/limitless/skills/dojo/SKILL.md`

- [ ] **Step 1: Write SKILL.md.** Frontmatter name `dojo`; description verbatim from spec §Description (the "This skill should be used when…" draft). Body sections, distilled from spec (keep under 250 lines — references carry detail):
  1. *Overview* — core principle: a skill is a claim about future agent behavior; untested claims ship as liabilities (SkillsBench −1.3pp vs SkillOpt +20pp gated). One paragraph.
  2. *The measurability rule* — pass criteria are observable y/n process checks and exact-match trigger tests, never subjective quality scores.
  3. *Tier table* — verbatim from spec §Tiered testing (discipline / technique / reference).
  4. *The seven kata* — numbered list, 2–4 sentences each, from spec §The loop: Intake (scenarios + pass criteria + 1–2 holdouts NOW), Baseline RED, Write GREEN (house description style: pushy, trigger phrases), Pressure-test (bounded edits, rejected-fix buffer), Graduation (holdouts once; fail → new holdouts), Trigger eval (matrix + collision check), Package & record (dojo record to `docs/dojo/<skill>-record.md`).
  5. *Subagent rules* — fresh subagent per run; self-contained scenario + context in the prompt (LS-G0009); criteria written before the run; subagent told its final message is raw data.
  6. *When NOT to use* — one-line config tweaks, non-skill docs, skills with real scalar graders (point SkillOpt at those).
  7. *References* pointer block — which file to read when.
- [ ] **Step 2: Validate.** Frontmatter: name+description < 1024 chars, name is `dojo`, body < 250 lines. Run: `wc -l plugins/limitless/skills/dojo/SKILL.md` and `head -5` to eyeball frontmatter.
- [ ] **Step 3: Commit.** `git add plugins/limitless/skills/dojo/SKILL.md && git commit -m "limitless: dojo SKILL.md — the seven kata"`

### Task 2: pressure-testing reference

**Files:**
- Create: `plugins/limitless/skills/dojo/references/pressure-testing.md`

- [ ] **Step 1: Write the file.** Sections:
  1. *Scenario design* — realistic task, not a quiz; one scenario per archetype the skill claims to handle; 3–5 training + 1–2 holdout; holdouts differ in kind (different archetype or stress condition), not just wording.
  2. *Pass criteria patterns* — y/n observables on process, with hivemind-flavored examples: "scoped search to a discovered venue before deep-reading (y/n)", "labeled claims observed/claimed/inferred (y/n)". Anti-pattern: "output was good (1–10)".
  3. *Baseline (RED) subagent prompt template* — verbatim:
     ```
     You are working on the following task. Use whatever approach you
     think is right. Available context: <self-contained scenario,
     environment notes, tool availability>. Task: <scenario>. Your final
     message is raw working data for analysis, not a user-facing summary:
     report what you did step by step, then your result.
     ```
  4. *Pressure (GREEN) variant* — same template + "The following skill document is installed and applies: <full SKILL.md content>".
  5. *Adversarial variants (discipline tier only)* — add time pressure ("ship in 10 minutes"), sunk cost ("we already wrote it the other way"), authority ("the lead said skip it"). Score whether the skill's rule held.
  6. *Bounded-edit rule* — one loophole → one targeted add/delete/replace → re-run; log edits that didn't survive in the dojo record's rejected-fix table.
- [ ] **Step 2: Commit.** `git add plugins/limitless/skills/dojo/references/pressure-testing.md && git commit -m "limitless: dojo pressure-testing reference"`

### Task 3: trigger-evals reference

**Files:**
- Create: `plugins/limitless/skills/dojo/references/trigger-evals.md`

- [ ] **Step 1: Write the file.** Sections:
  1. *Matrix design* — 10–15 prompts: ~60% should-trigger positives phrased the way the user actually talks, ~40% near-miss negatives that belong to *other* installed skills or no skill.
  2. *Harvesting the description list* — the authoring session lists every installed skill's name + description (from its own system context) into the eval prompt.
  3. *Eval subagent prompt template* — verbatim:
     ```
     You are a skill-routing judge. Below is the list of installed skills
     (name: description). For each user prompt, answer with the single
     skill name you would invoke, or "none". Output one line per prompt:
     "<n>: <skill-name>". No explanations.
     SKILLS: <full list including the new skill>
     PROMPTS: <numbered matrix>
     ```
  4. *Scoring* — exact match per row; report `X/N`. Threshold: every positive must hit; a near-miss negative hitting the new skill = collision, fix the description, re-run. Run the matrix twice (different subagents) to catch flaky routing.
  5. *Tuning* — add the missed phrasing to the description's "Responds to" list; remove or sharpen overlapping nouns that caused collisions.
- [ ] **Step 2: Commit.** `git add plugins/limitless/skills/dojo/references/trigger-evals.md && git commit -m "limitless: dojo trigger-evals reference"`

### Task 4: packaging reference

**Files:**
- Create: `plugins/limitless/skills/dojo/references/packaging.md`

- [ ] **Step 1: Write the file.** Sections:
  1. *Limitless layout* — `plugins/limitless/skills/<name>/SKILL.md` + optional `references/`, `assets/`, `scripts/`; auto-discovered, no registration file for the skill itself.
  2. *Ship checklist* — bump `plugins/limitless/.claude-plugin/plugin.json` version + description skill list; update `.claude-plugin/marketplace.json` limitless entry description; update root `README.md` plugin table (skill count + what-it-does); `/reload-plugins` and confirm the skill appears; smoke-invoke it once.
  3. *Dojo record template* — verbatim markdown skeleton:
     ```markdown
     # Dojo record — <skill>
     *Tier: <discipline|technique|reference> · Date · Author*
     ## Baseline findings (RED)
     | Scenario | Failure mode observed |
     ## Loopholes closed
     | # | Loophole | Edit that closed it |
     ## Rejected fixes
     | # | Attempted edit | Why it didn't survive |
     ## Graduation
     | Holdout | Result | Notes |
     ## Trigger matrix
     | # | Prompt | Expected | Got | Pass |
     Score: X/N · Collisions: <none|list>
     ## Known limitations
     - ...
     ```
- [ ] **Step 2: Commit.** `git add plugins/limitless/skills/dojo/references/packaging.md && git commit -m "limitless: dojo packaging reference"`

### Task 5: dojo's own trigger eval (recursion)

**Files:**
- Create: `docs/dojo/dojo-record.md`

- [ ] **Step 1: Build dojo's trigger matrix** (12 prompts). Positives (must route to dojo): "let's make a new skill for X", "turn this workflow into a skill", "test whether my skill actually works", "why isn't my skill triggering", "run it through the dojo", "improve this skill's description", "harden this SKILL.md". Near-miss negatives (must NOT route to dojo): "write an implementation plan for this feature" (→ writing-plans), "create an agent that reviews code" (→ agent-creator), "set up a new plugin with hooks" (→ plugin-dev/create-plugin), "review this skill I wrote" (→ skill-reviewer is also acceptable — count either skill-reviewer or dojo as pass, note ambiguity), "make me a slash command" (→ command-development).
- [ ] **Step 2: Run the eval.** Two fresh subagents via Agent tool with the trigger-evals template, full installed-skill description list + dojo's description. Expected: all positives → dojo; negatives → their owners.
- [ ] **Step 3: Tune if needed.** Any miss → adjust dojo's description ("Responds to" list), re-run both subagents. Repeat until positives 7/7 and no collisions.
- [ ] **Step 4: Write `docs/dojo/dojo-record.md`** using the Task 4 template (baseline/loophole sections marked "n/a — reference-adjacent meta skill; trigger eval only" per tier rules — dojo is technique tier but its baseline IS this conversation's research; note that honestly).
- [ ] **Step 5: Commit.** `git add docs/dojo/dojo-record.md plugins/limitless/skills/dojo/SKILL.md && git commit -m "limitless: dojo trigger eval + record (recursion test)"`

---

## Phase B — Hivemind through the dojo

### Task 6: Intake — scenarios, pass criteria, holdouts

**Files:**
- Create: `docs/dojo/hivemind-scenarios.md`

- [ ] **Step 1: Write the intake artifact.** Tier: technique. Training scenarios:
  - **S1 (trend scan):** "What's currently the new hot shit in AI agent memory systems?" Pass criteria (y/n each): ran a recon search before scoped searches; identified ≥2 venues (subreddits) from recon; used time-windowed sort (`-t week|month` / `--since`); applied engagement floors on X; LLM-triaged for relevance (rejected ≥1 high-engagement-but-off-topic item OR stated none found); deep-read ≥2 threads (comments/replies); final answer cites receipts with engagement numbers; offered 2–4 next directions.
  - **S2 (knowledge mine):** "What does social media say about how optimal Suno prompts look like?" Pass criteria: venue resolution happened (r/SunoAI or equivalent discovered, not assumed... discovered OR justified); searches scoped to venue; comments deep-read (`rdt read`); consensus vs contested split in the answer; claims labeled observed/claimed/inferred; no averaging of contradictions.
  - **S3 (degradation):** Same as S1 but "the rdt CLI is not installed on this machine." Pass criteria: detected missing CLI; offered install (uv tool install rdt-cli); continued single-platform rather than blocking; flagged reduced coverage in the answer.
  - **Holdouts (do NOT use during iteration):**
  - **H1 (people sentiment):** "What do people on social media think about Codex CLI vs Claude Code these days?" Criteria: venue recon, both-sides stance mining with receipts, no truth-claims from sentiment.
  - **H2 (radar, thin topic):** "--radar 'agentic knowledge graphs'" Criteria: full sweep runs; thin-results adaptation triggered (floor lowered or window widened, stated); radar.json emitted with provenance + observed_at per claim; radar.html rendered from the JSON using the fanzine template; enrichment ≤3 lookups per topic; files land in `~/.hivemind/agentic-knowledge-graphs/<date>/`.
- [ ] **Step 2: Commit.** `git add docs/dojo/hivemind-scenarios.md && git commit -m "limitless: hivemind dojo intake — scenarios + holdouts"`

### Task 7: Baseline runs (RED)

**Files:**
- Create: `docs/dojo/hivemind-record.md` (start it: header + baseline table)

- [ ] **Step 1: Run S1 and S3 baselines.** Two fresh subagents (Agent tool, general-purpose), pressure-testing baseline template, no skill content. Context note in prompt: "twitter and rdt CLIs are installed and authenticated (except as stated); you may run real searches." S2's baseline is already evidenced (2026-06-11 smoke test: global `rdt search "suno prompt" -s top` returned r/CuratedTumblr + r/antiai garbage; engagement≠relevance on X) — record it, don't re-run.
- [ ] **Step 2: Score against pass criteria; document failure modes** in `docs/dojo/hivemind-record.md` baseline table. Expected failures (verify, don't assume): no venue recon, single broad query, no comment deep-read, no evidence labels, S3 blocks or silently skips Reddit.
- [ ] **Step 3: Commit.** `git add docs/dojo/hivemind-record.md && git commit -m "limitless: hivemind baseline (RED) findings"`

### Task 8: Write hivemind SKILL.md (GREEN)

**Files:**
- Create: `plugins/limitless/skills/hivemind/SKILL.md`

- [ ] **Step 1: Write SKILL.md** from the concept doc §The search flow + §Decisions, explicitly answering every Task 7 failure mode. Frontmatter description verbatim from concept §Skill interface trigger phrases, pushy style. Body (< 350 lines): Phase 0 preflight (command -v, install offer, auth check, degrade single-platform); mode table (trend/knowledge knobs); Phase 1 scope; Phase 2 recon (subreddit frequency-count recipe); Phase 3 fan-out (CLI command patterns with adaptive floors); Phase 4 triage & deep-read (LLM relevance before engagement; `rdt read` / `twitter tweet`; author cap; dedup); Phase 5 synthesis (answer-first brief shape, epistemic labels, 2–4 next directions); flags (`--quick/--deep`, `--platform`, `--window`, `--verify`, `--radar` → references/radar.md); auto-save rule (load-bearing findings → codies-memory inbox); pointers to references.
- [ ] **Step 2: Validate.** `wc -l` < 350; frontmatter limits; every S1–S3 pass criterion is addressed by an explicit instruction (walk the checklist).
- [ ] **Step 3: Commit.** `git add plugins/limitless/skills/hivemind/SKILL.md && git commit -m "limitless: hivemind SKILL.md (GREEN)"`

### Task 9: hivemind references + radar template asset

**Files:**
- Create: `plugins/limitless/skills/hivemind/references/x-playbook.md`
- Create: `plugins/limitless/skills/hivemind/references/reddit-playbook.md`
- Create: `plugins/limitless/skills/hivemind/references/radar.md`
- Create: `plugins/limitless/skills/hivemind/assets/radar-template.html`

- [ ] **Step 1: x-playbook.md** — twitter-cli recipes from concept §Tooling + §Fan-out: search flag table, quoted-topic rule, floor ladder (top: start 50, halve if <5 hits, double + `--exclude replies` if noisy; latest: start 10), `twitter tweet <id>` reply mining, JSON output handling (`--json -o`, compact `-c`), auth check.
- [ ] **Step 2: reddit-playbook.md** — rdt recipes: venue resolution via frequency-count of `subreddit` field over a broad relevance search (the r/antiai cautionary example verbatim), scoped search patterns per mode, `rdt read -s top --expand-more` comment mining, `sub-info` sanity check, pagination, export.
- [ ] **Step 3: radar.md** — from concept §Radar mode + §Sweep series: pipeline delta (cluster → stance-mine → enrich ≤3 lookups/topic → emit JSON → render HTML), the radar.json schema verbatim, sweep-series contract (slugs, immutability, backwards links, index.html, `HIVEMIND_DIR` override, `~/.hivemind` default), template usage: copy `assets/radar-template.html` structure, replace sample data, keep both views + fanzine visual language.
- [ ] **Step 4: Copy the template.** `cp docs/brainstorm/hivemind-mockups/04-fanzine.html plugins/limitless/skills/hivemind/assets/radar-template.html`
- [ ] **Step 5: Commit.** `git add plugins/limitless/skills/hivemind/references plugins/limitless/skills/hivemind/assets && git commit -m "limitless: hivemind playbooks + radar template"`

### Task 10: Pressure-test (REFACTOR)

**Files:**
- Modify: `docs/dojo/hivemind-record.md` (loopholes + rejected fixes tables)
- Modify: `plugins/limitless/skills/hivemind/SKILL.md` (bounded edits only)

- [ ] **Step 1: Run S1, S2, S3** with fresh subagents, GREEN template (skill content + relevant playbook content in prompt). Score every pass criterion y/n.
- [ ] **Step 2: Bounded-edit loop.** Each failed criterion: identify the loophole, one targeted edit to SKILL.md/reference, re-run that scenario only. Log every edit in the record; failed attempts go to rejected-fixes.
- [ ] **Step 3: Exit when S1–S3 fully pass** (or a criterion is consciously demoted to Known Limitations with rationale).
- [ ] **Step 4: Commit.** `git add -u plugins/limitless/skills/hivemind docs/dojo/hivemind-record.md && git commit -m "limitless: hivemind pressure-test loop"`

### Task 11: Graduation (holdouts)

**Files:**
- Modify: `docs/dojo/hivemind-record.md` (graduation table)

- [ ] **Step 1: Run H1 and H2 once each**, fresh subagents, GREEN template. H2 needs the radar.md + template content included. No edits between the two runs.
- [ ] **Step 2: Record results.** Pass → proceed. Fail → fix via bounded edits, then design NEW holdouts (H3/H4, different archetypes — e.g., compare-mode query, non-English topic) before re-attempting graduation. Never reuse burned holdouts.
- [ ] **Step 3: Commit.** `git add docs/dojo/hivemind-record.md && git commit -m "limitless: hivemind graduation"`

### Task 12: Trigger eval

**Files:**
- Modify: `docs/dojo/hivemind-record.md` (trigger matrix)

- [ ] **Step 1: Matrix (14 prompts).** Positives: "what's the hot shit in rust tooling right now", "what does social media say about MCP security", "what does reddit think of the new Suno version", "check the socials for reactions to the Claude release", "ask the hivemind about local LLM agents", "what are people saying about devcontainers", "--radar AI coding agents", "is twitter hyped about anything new in image gen". Negatives: "search the web for SearXNG docker setup" (→ searxng), "what's the latest on the EU AI Act, with sources" (→ codies-research), "deep research report on vector DB pricing" (→ deep-research), "write me an article about agent memory" (→ article-pack), "look up the twitter API docs" (→ searxng/codies-research), "post this on twitter" (→ none — hivemind is read-only).
- [ ] **Step 2: Run twice** (two fresh subagents), full installed description list + hivemind's. Score exact-match.
- [ ] **Step 3: Tune description on misses, re-run.** Watch the known risk: codies-research owns "what's the latest on X" — hivemind must NOT steal it; social-platform wording is the differentiator.
- [ ] **Step 4: Commit.** `git add -u && git commit -m "limitless: hivemind trigger eval"`

### Task 13: Package & ship

**Files:**
- Modify: `plugins/limitless/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md`
- Modify: `docs/dojo/hivemind-record.md` (final: known limitations, belt rank)

- [ ] **Step 1: plugin.json** — version `0.6.0` → `0.7.0`; description: append "Dojo" and "Hivemind" to the skill list sentence.
- [ ] **Step 2: marketplace.json** — limitless entry description: same additions.
- [ ] **Step 3: README.md** — limitless row: skill count 5 → 7; mention social-media search + skill dojo in the what-it-does cell; same in the plugin table description if listed elsewhere.
- [ ] **Step 4: Reload + smoke.** `/reload-plugins` (user runs it or instruct); confirm both skills listed; smoke-invoke hivemind with a tiny query (`--quick`, n small).
- [ ] **Step 5: Finalize `docs/dojo/hivemind-record.md`** — known limitations (e.g., radar HTML quality depends on session model; X auth is cookie-fragile), final scores.
- [ ] **Step 6: Commit + push.** `git add -u && git add plugins/limitless/skills/hivemind && git commit -m "limitless: ship dojo + hivemind (v0.7.0)" && git push`

---

## Self-review notes

- Spec coverage: all seven kata exercised in Phase B (intake T6, baseline T7, write T8/9, pressure T10, graduation T11, trigger T12, package+record T13); dojo recursion covered in T5; measurability rule embedded in every pass-criteria list (all y/n observables). Tier table honored (hivemind = technique tier → no adversarial variants).
- No placeholders: subagent prompt templates, matrices, scenarios, and record skeleton are spelled out verbatim.
- Consistency: record path `docs/dojo/<skill>-record.md` used uniformly; template asset path `assets/radar-template.html` matches radar.md instruction; `~/.hivemind` default matches concept doc.
