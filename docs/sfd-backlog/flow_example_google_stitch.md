# Flow Example: "local google stitch"

Shows how the revised SFD skill handles the failure case that prompted this whole backlog. Every user response in this example is one keystroke or one short phrase.

## Context

User prompt: *"help me build a local google stitch"*

What happened in the original session: assistant assumed "stitch" meant image-stitching (like panorama merging), built 3 image-editing prototypes over ~20 minutes. Google Stitch is Google's AI UI-design tool. All 20 minutes were landfill.

## How revised SFD handles it

### [Phase 0.5 fires immediately — "google stitch" is a proper noun that doesn't map with high confidence]

**Assistant (one web search, then):**
> I'm reading "google stitch" as **Google Stitch — Google Labs' AI-powered UI design tool** (lets you describe an interface in natural language and generates design mocks + React code). Is that right?
>
> **A.** Yes — build a local version of the AI UI-design tool.
> **B.** No — one of: (1) image-stitching / panorama tool, (2) Git "stitch" workflow tool, (3) text/document concatenation tool.
> **C.** None of those — one-word hint?

**User:** `A`

*(Decision logged: target = local Google Stitch clone = AI UI design tool.)*

Elapsed: **~30 seconds.** Original session wasted ~20 minutes before reaching the same confirmation.

---

### [Phase 1 — identify surface]

**Assistant:**
> Target confirmed: local Google Stitch = AI UI design tool. Primary surface is a **web GUI** (text prompt → generated mockup/code preview). Any objections?
>
> **A.** GUI (recommended — matches Google Stitch).
> **B.** CLI-only (could work if you want a pipeline tool, but less aligned).
> **C.** Both — web GUI that also exposes a CLI.

**User:** `A`

### [Phase 1.5 — offer visual companion since surface is GUI]

**Assistant:** *(own message, nothing else)*
> Since we're designing a GUI, I can launch a local browser preview window so you can click through prototypes instead of reading HTML files. Use it?
>
> **Y / N** (token-light either way)

**User:** `Y`

### [Phase 2 — premise announcement, then chunked build]

**Assistant:**
> Working premise: **a local web app where a user types an interface description, an LLM generates a design preview + React code, and the user can iterate on it**. First chunk: the prompt-input + generated-mockup-preview screen. ~3 minutes.

*[builds screen 1, shows in browser preview]*

> Landing screen done. Input textarea, "Generate" button, split-pane preview on the right. Keep going?
>
> **Y / N / (tweak before continuing)**

**User:** `Y`

*[builds screen 2: iteration/variant selection]*

> Iteration view done — user can regenerate variants, keep any of 3 alternates. Continue?
>
> **Y / N / tweak**

**User:** `Y`

*[builds screen 3: code export]*

> Code export view done — see generated React code, copy/download. Prototype complete.
>
> Ready for critique? **Y / N / (ship as-is)**

**User:** `Y`

*(Elapsed: ~10 minutes, with 3 checkpoint beats. User could have aborted at any of them in 1 second.)*

---

### [Phase 3 — critique ladder, Rung 1]

**Assistant:**
> Walk through the prototype. Does it feel roughly right?
>
> **A.** Yes, ship this.
> **B.** Almost, but one part is off.
> **C.** Not quite — different angle needed.

**User:** `B`

### [Rung 2 — narrow]

**Assistant:**
> The prototype has three parts: **A. prompt input + generate button**, **B. variant selection (3 alternates)**, **C. code export**. Which feels weakest?
>
> A / B / C / (all fine — converged)

**User:** `B`

### [Rung 3 — action]

**Assistant:**
> For the variant selection, I can:
> 1. Research how Google Stitch's own variant UI works (~5-min web search)
> 2. Ask you 3 guided questions to narrow the fix
> 3. Propose 2 alternate versions of variant selection (grid vs. tabs vs. carousel)
>
> Pick 1 / 2 / 3.

**User:** `3`

*[produces 2 alternate variant-selection designs in browser preview: tabbed vs carousel]*

### [back to Rung 2]

**Assistant:**
> Two alternates ready. Does one fit better?
>
> **1. tabbed**, **2. carousel**, **3. original grid** / (mix freeform)

**User:** `2`

*[updates prototype with carousel variant selection]*

> Updated. Rung 2 again: which part feels weakest now? A / B / C / (all fine)

**User:** `all fine`

---

### [Convergence — Phase 4]

**Assistant:**
> Surface converged. Moving to contract derivation. **OK? Y / N**

**User:** `Y`

*[Phase 2.5 probe: would this be on?]*

*In this case the surface is a GUI and a call-out to an LLM — probe could catch "the LLM API we want to use doesn't support structured output in the shape we need." But probe default is OFF for GUI, so:*

**Assistant:**
> About to derive contracts. Feasibility probe is optional for this GUI surface — skip? **Skip (recommended for pure GUI) / Run (for the LLM integration)**

**User:** `Run`

*[probe dispatched: checks that the planned LLM call signature actually returns a shape the frontend can render — catches e.g. "Gemini returns streaming text, frontend expects structured JSON"]*

**Assistant:**
> Probe found: frontend assumes synchronous JSON response; Gemini streams. Options:
>
> **A.** Add streaming response UI to Phase 3 prototype (recommended).
> **B.** Use non-streaming model call (slower but simpler).
> **C.** Re-open surface — let's rethink the generation flow.

**User:** `A`

*[one more screen chunk + critique ladder loop, ~5 min]*

*Now converged. Contracts derived. Surface matches what the backend can actually deliver.*

---

## The contrast

| | Original session | Revised SFD |
|---|---|---|
| Target verification | None — assumed "stitch" = panorama | 30-second search + one confirmation |
| Wrong-direction wall-clock time | **~20 minutes** before user could correct | **~0 seconds** — caught before any build |
| Build-cycle feedback gaps | 20 min silent | 3 chunked confirmations at ~3 min each |
| Critique phase | "Tell me what's wrong" → user had no idea where to start | Guided ladder → 3 decisions, each one keystroke |
| Feasibility (streaming vs sync) | Would have been caught at implementation, another wasted hour | Caught at Phase 2.5 in 5 min |
| Total time to convergence | Never reached (user gave up) | ~20 minutes total, all productive |

## Keystrokes the user typed in the full session

```
A Y Y Y Y Y B B 3 2 "all fine" Y Run A
```

14 responses — none longer than a phrase. No expert analysis required.
