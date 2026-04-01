# Pyro Kit — Backlog

Future ideas and enhancements beyond the v0.1.0 MVP scope. These are seeds — some may become full skills, others may fold into existing ones.

---

## 1. Explorative Web Excavation

**Status:** Idea
**Relates to:** Excavator agent, /spark

The excavator agent currently operates without web access (using only existing knowledge). It should gain the ability to use the web — but **exploratively**, not analytically.

The goal is **not** serious business case analysis or market research. It's weird, divergent, novelty-maximizing exploration: finding strange repos, obscure papers, unexpected connections, and ideas from non-obvious communities.

**Inspiration:** The `researchfun` command (see `docs/reference/researchfun.md`) embodies this energy — it optimizes for novelty, delight, hackability, and "mind-melting" ideas. The excavator should channel this same spirit when it goes online.

**Key principles:**
- Optimize for novelty and surprise, not comprehensiveness
- Explore global/non-English communities (Qiita, Zenn, Chinese dev forums)
- Favor "toy-but-touchable" projects over polished enterprise tools
- Cross-pollinate ideas from unrelated domains
- The web is for serendipity, not validation

---

## 2. Persisted Discarded Thumbnails

**Status:** Idea
**Relates to:** /spark

When /spark presents thumbnails (idea sketches) and the user picks one, the unchosen thumbnails are currently lost. They should be persisted.

**Why:** What the user doesn't choose *today* might spark something tomorrow. Discarded thumbnails represent explored-but-not-pursued directions — they're raw material for future excavation, not waste.

**Possible implementation:**
- Save all generated thumbnails to `.pyro/discarded-thumbnails.md` (or per-spark session files)
- Include the context they were generated in (what the user was exploring, what they chose instead)
- Let the excavator and /spark reference discarded thumbnails when generating new ideas
- Consider a `/spark revisit` subcommand that resurfaces old thumbnails

---

## 3. Web Scout Skill (/scout)

**Status:** Idea
**Relates to:** researchfun command, excavator agent, /spark

Generalize the `researchfun` command (see `docs/reference/researchfun.md`) into a first-class Pyro Kit skill. This would be **unguided, curiosity-driven web scouting** of a topic — finding the wildest ideas, weirdest repos, most surprising connections — and proposing thumbnails based on them.

**How it differs from /spark and /explore:**
- /spark starts from the user's existing fascinations and excavates depth (Phase 0)
- /explore maps the design space of a crystallized idea (Phase 1)
- /scout goes **out into the web** to find things you'd never think to look for — serendipity as a service

**How it differs from the excavator:**
- The excavator works from internal knowledge to dig up pre-idea raw material
- /scout goes online with the same weird, divergent energy but taps into live sources

**Key features from researchfun to preserve:**
- FUN scoring rubric (novelty, wow/delight, hackability, cultural resonance, remixability)
- Falsification protocol (prior-art sweep + weekend feasibility)
- Query logging and research log for reproducibility
- The "10/10 mind-melter" standard — don't stop until you find something genuinely surprising
- PoC generation for the winner

**Key adaptations for Pyro Kit:**
- Output thumbnails in /spark format so they feed into the lifecycle naturally
- Store exploration results in `.pyro/` state (not standalone date folders)
- Integrate with fascination index — exploration findings can seed new fascination entries
- Respect the anti-abandonment philosophy: scouting is Phase 0 fuel, not procrastination

---

## Reference Documents

- `docs/reference/researchfun.md` — The original Weird Research Scout (FUN mode) command that inspired /scout
- `docs/reference/sfd/SKILL.md` — Surface-First Development agent skill (Pyro Kit's underlying methodology)
- `docs/reference/sfd/whitepaper-v0.6.md` — SFD whitepaper (academic framing of the methodology)
