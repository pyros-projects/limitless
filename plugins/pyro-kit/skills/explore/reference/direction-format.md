# Direction Format

Template for /explore direction output. Each of the 4 directions follows this structure.

## Template

```markdown
### Direction {LETTER}: {Descriptive Name}

**Scenario:** {1 paragraph -- a specific person using this in a specific moment. Present tense. Concrete details. Vivid enough that the developer can react immediately -- "yes, that" or "no, not that."}

**Sketch:**
{Inline sketch appropriate to idea type -- see sketch type selection below}

**Key Bet:** {The one assumption this direction makes that the others don't. Stated as a declarative belief: "Two questions is enough" not "Would two questions be enough?"}
```

## Sketch Type Selection

Select the sketch type that makes each direction's differentiator most vivid. A single exploration may mix sketch types across directions if different directions are best illustrated differently.

### CLI Transcript
**When:** Idea mentions CLI, terminal, command, shell, prompt, flags, arguments.
```
$ command --flag argument
> Interactive prompt question?
  User response here

Output displayed to user
```

### ASCII Wireframe Description
**When:** Idea mentions UI, dashboard, visual, interface, screen, page, layout.
Describe the layout in structured words -- sections, panels, what's visible, what's interactive. Not raw ASCII boxes.

### API Usage Example
**When:** Idea mentions API, endpoint, integration, webhook, SDK, library, import.
```javascript
const result = await tool.action({
  input: "...",
  options: { ... }
});
// result: { ... }
```

### Data Flow Description
**When:** Idea mentions system, flow, pipeline, process, queue, event, stream.
Describe how data or control moves through the system: source -> transform -> destination, with what happens at each stage.

### Mixed (Ambiguous Ideas)
**When:** Idea does not clearly match one type, or matches multiple.
Pick the sketch type per direction that best illustrates what makes THAT direction unique. Direction A might use a CLI transcript while Direction C uses an API example.

## Divergence Rules

Directions must be fundamentally different. Each makes a different bet:

- **Different bets** = each direction answers a DIFFERENT question about what matters most
- **Not variations** = not "the same thing but with more features" or "the same thing but simpler"
- **Named explicitly** = letter + descriptive name (e.g., "Direction A: The Two-Question Ritual")
- **Scenario-first** = the scenario must be specific enough to react to without reading the sketch
