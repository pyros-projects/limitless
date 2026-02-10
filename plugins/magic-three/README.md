# Magic Three

**Pyro's essential agent skill trio for structured AI-assisted development.**

Three skills that turn your AI coding agent into a disciplined engineering partner: plan what to build, track what to do next, and research anything — all without leaving your terminal.

---

## Skills

| Skill | What It Does | When to Use |
|-------|-------------|-------------|
| [**OpenSpec**](skills/openspec/) | Spec-driven development — plan before you code | Starting features, brownfield changes, structured planning |
| [**Beads**](skills/beads/) | Git-backed task graph with dependencies | Long-horizon projects, multi-session work, complex task ordering |
| [**SearXNG**](skills/searxng/) | Self-hosted privacy-respecting web search | When your agent needs to search the web without API keys |

## How These Work Together

**OpenSpec** defines *what* to build (specs, proposals, design, tasks).
**Beads** tracks *what to do next* (dependency graph, execution state, session memory).
**SearXNG** provides *research capability* (web search for investigation and planning).

The recommended combo for feature development:

```
OpenSpec (plan) -> Beads (execute) -> OpenSpec (verify + archive)
```

1. Use OpenSpec to create structured planning artifacts
2. Import tasks into Beads with dependencies
3. Use `bd ready` to work through tasks in correct order
4. Verify and archive when done

For small features (<5 tasks), OpenSpec alone is sufficient. Add Beads when work gets complex or spans multiple sessions.

---

## Installation

### Via Limitless Marketplace

```
/plugin marketplace add pyros-projects/limitless
/plugin install magic-three@limitless
```

### Manual (As Agent Skills)

Each skill is a standalone `SKILL.md` that can be loaded by your AI coding tool:

- **Claude Code:** Copy to `.claude/skills/`
- **Cursor:** Reference in `.cursor/rules/`
- **Other tools:** Point your agent at the relevant `SKILL.md` file

### The Tools Themselves

Each skill documents how to install the underlying tool:

- **OpenSpec:** `npm install -g @fission-ai/openspec@latest`
- **Beads:** `brew install beads` (macOS) or `npm install -g @beads/bd`
- **SearXNG:** `docker run -d --name searxng --restart always -p 8888:8080 searxng/searxng:latest`

---

## Structure

```
magic-three/
├── .claude-plugin/
│   └── plugin.json         # Plugin metadata
├── README.md               # This file
└── skills/
    ├── openspec/
    │   ├── README.md       # Detailed guide for humans
    │   └── SKILL.md        # Agent-readable skill file
    ├── beads/
    │   ├── README.md       # Detailed guide for humans
    │   └── SKILL.md        # Agent-readable skill file
    └── searxng/
        ├── README.md       # Detailed guide for humans
        └── SKILL.md        # Agent-readable skill file
```

---

## License

MIT
