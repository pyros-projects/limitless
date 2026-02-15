---
name: article-pack
description: Research topics and generate complete content packages. Creates articles for multiple platforms (Substack, LinkedIn) in multiple languages, slide decks, and social media kits with copy buttons. Can start from just a topic idea—will research via web search until enough material exists. Trigger with "article-pack" or when user wants to create publishable content.
---

# Article Pack Generator

Generate complete, publish-ready content packages from research, notes, or draft material.

## When to Use This Skill

Activate when the user:
- Says "article-pack" or "content pack"
- Wants to turn research/notes into publishable articles
- Asks for "Substack article", "LinkedIn post", or similar
- Requests multi-platform content creation
- Needs social media promotion materials
- Wants to research a topic and create content from findings
- Has a topic idea but needs help gathering material first

## Wizard Flow

This skill runs as an interactive wizard. Guide the user through each step using `AskUserQuestion`.

---

### Step 0: Content Sufficiency Check

**Before starting the wizard**, analyze whether sufficient source material exists for a meaningful article pack.

**Evaluate the available content for:**
- **Depth**: Is there enough substance for a full article (not just surface-level points)?
- **Examples/Evidence**: Are there concrete examples, data, or case studies?
- **Perspectives**: Are there multiple angles or viewpoints to explore?
- **Novelty**: Is there something genuinely interesting or new to say?

**If content is SUFFICIENT:**
- Briefly confirm what you're working with
- Proceed to Step 1

**If content is INSUFFICIENT:**
- Explain specifically what's missing (be concrete, not vague)
- Recommend web research to fill the gaps
- Offer to help research specific angles using web search
- Ask if the user wants you to research now or provide more material themselves

```
Question: "Your topic is interesting, but I need more material to create a strong pack. Want me to research first?"
Options:
- Yes, research this topic for me (I'll search the web)
- Let me add more context/notes first
- Proceed anyway with what we have (lighter output)
- Let me specify what to research
```

**Research loop:**
When researching, use web search to gather:
- Recent news and developments
- Key statistics and data points
- Expert opinions and quotes
- Counter-arguments and different perspectives
- Real-world examples and case studies

After each research round, summarize findings and ask:
```
Question: "I found [summary]. Is this enough, or should I dig deeper?"
Options:
- That's enough, let's proceed to article pack
- Research more on [specific angle]
- Add this to my notes, I'll provide more context
- Start over with a different focus
```

---

### Step 1: Identify Source & Voice

First, summarize what we're working with:
- What's the core topic/argument? (2-3 sentences)
- Where does the source material live?

Then check for author voice context (memory, previous work, instructions).
If no voice context available, ask:

First ask whether the user has existing content to match:

```
Question: "Do you have existing content (articles, tweets, style guides) I should match the voice to?"
Header: "Voice source"
Options:
- Yes, I have a reference folder (I'll analyze your existing content and extract a voice profile)
- No, let me pick a preset voice
```

**If "Yes, reference folder"** → proceed to **Voice from Reference Folder** below.

**If "No, pick a preset"** → ask:

```
Question: "Which writing style fits best?"
Header: "Voice"
Options:
- Opinionated & direct (hot takes, strong positions)
- Professional & measured (thought leadership)
- Academic & thorough (detailed, referenced)
- Casual & conversational (friendly, accessible)
```

#### Voice from Reference Folder

If user selects "Reference folder", ask them to provide a path:

> "Give me a folder path containing your existing content. I'll analyze everything in it to extract your voice, tone, and style patterns.
>
> This can include any mix of: articles, blog posts, tweets/threads, LinkedIn posts, style guides, brand docs, newsletter archives, social media exports, or even just notes you've written."

**After receiving the path:**

1. **Scan the folder** recursively for readable content:
   ```
   - .md, .txt, .html files (articles, posts, guides)
   - .json, .csv files (social media exports, tweet archives)
   - .pdf files (style guides, brand books)
   - Subdirectories (scan everything)
   ```

2. **Read a representative sample** — prioritize:
   - Files with "style" or "guide" or "brand" in the name (read fully)
   - The 3-5 most recent articles/posts (read fully)
   - A sampling of shorter content like tweets/social posts (batch-read)
   - Skip binary files, images, and anything over 50KB without "guide" in the name

3. **Extract a voice profile** — analyze the content for:
   - **Tone:** formal vs. casual, serious vs. playful, measured vs. provocative
   - **Sentence patterns:** short punchy vs. flowing, fragment usage, rhetorical questions
   - **Vocabulary:** technical depth, jargon comfort level, favorite phrases/idioms
   - **Structure habits:** how they open articles, use of headers, paragraph length
   - **Signature moves:** recurring phrases, sign-offs, how they handle transitions
   - **Platform adaptation:** how the voice shifts between long-form and social

4. **Present the voice profile to the user for confirmation:**

   ```
   ## Voice Profile (extracted from {N} files)

   **Tone:** [e.g., "Confident and opinionated with technical depth. Uses humor
   sparingly but effectively. Not afraid of hot takes."]

   **Signature patterns:**
   - [e.g., "Opens with a bold claim or counter-intuitive observation"]
   - [e.g., "Uses one-sentence paragraphs for emphasis"]
   - [e.g., "Ends sections with a forward-looking hook"]

   **Vocabulary:** [e.g., "High technical fluency, avoids corporate jargon,
   prefers concrete over abstract"]

   **Social voice:** [e.g., "Punchier, more provocative, uses emoji sparingly,
   thread-style with cliffhangers between tweets"]

   **Sample phrases I'll echo:**
   - "[actual phrase from their content]"
   - "[actual phrase from their content]"
   - "[actual phrase from their content]"
   ```

5. **Ask for confirmation:**

   ```
   Question: "Does this voice profile capture your style? I'll use it across all articles and extras."
   Header: "Voice OK?"
   Options:
   - Yes, that's me — proceed
   - Close but needs tweaks (let me adjust)
   - Rescan with different/additional files
   - Scrap this, let me pick a preset instead
   ```

   If "Close but needs tweaks" — ask what to adjust (more formal? less humor? different opener style?) and update the profile.

6. **Use the voice profile throughout generation** — apply it to:
   - All article variants (as the baseline voice, adapted per platform/style)
   - Social media kit (match their social voice specifically)
   - Twitter threads (match their thread cadence)
   - Newsletter (match their direct-to-reader tone)
   - Podcast transcript (one host can mirror their voice)

**Store the extracted profile in memory** for future article-pack runs if the user's persistent memory is available. This way, subsequent packs can offer: "Use your saved voice profile from last time?"

---

### Step 2: Number of Articles

```
Question: "How many article versions do you need?"
Options:
- 1 article
- 2 articles
- 3 articles
- 4+ articles
```

---

### Step 3: Define Each Article

For each article (repeat N times), ask a single multi-part question:

```
Question: "Article {N}: What language, style, and platform?"
Header: "Article {N}"
Options:
- English / Full voice / Substack or Blog
- English / Professional / LinkedIn
- German / Full voice / Substack or Blog
- German / Professional / LinkedIn
- Other (let me specify)
```

If user selects "Other", follow up for custom combination.

**Available dimensions:**

| Dimension | Options |
|-----------|---------|
| Language | English, German, French, Spanish, Other |
| Style | Full voice (opinionated), Professional (toned down), Academic, Casual |
| Platform | Substack, LinkedIn, Medium, Company blog, Newsletter, Other |

---

### Step 4: Additional Content

**IMPORTANT**: Present ALL options to the user. Do not truncate this list.

**Note:** Images are NOT listed here — they are handled proactively in a separate step after the user confirms the pack (see "Image Generation" in the Generation Process). This keeps the image decision focused and allows skill assessment.

```
Question: "What additional content do you want?"
Header: "Extras"
multiSelect: true
Options (present all 9):
1. Social media kit (tweets, LinkedIn posts, hashtags, hooks)
2. Slide deck (presentation version)
3. Twitter/X thread (standalone thread format)
4. Email newsletter version
5. Executive summary (TL;DR card)
6. Press release
7. Quote cards (shareable image quotes)
8. Podcast transcript (NotebookLM-style two-host dialogue)
9. Prose story (creative narrative woven around the topic)
```

Note: AskUserQuestion only supports 4 options max, so present in batches:

**Batch 1 (Core):**
- Social media kit
- Slide deck
- Twitter/X thread
- Email newsletter

**Batch 2 (Distribution):**
- Executive summary (TL;DR)
- Press release
- Quote cards
- Podcast transcript (with dice-rolled hosts!)

**Batch 3 (Creative):**
- Prose story
- None from this batch
- Back to add more from previous

---

### Step 5: Output Location

```
Question: "Where should I save the article pack?"
Header: "Location"
Options:
- [Suggest sensible default based on context]
- Let me specify a path
- Current directory
```

---

### Step 6: Review & Confirm

**CRITICAL**: Always get explicit confirmation before generating.

First, display the full configuration summary:

```
## 📋 Article Pack Configuration

**Source:** [topic summary - 2-3 sentences]
**Voice:** [detected or selected style]

**Articles:**
1. English / Full voice / Substack
2. German / Professional / LinkedIn

**Extras:**
- Social media kit
- Podcast transcript (hosts will be dice-rolled!)
- Prose story

**Images:** Will be decided after confirmation (OpenRouter detected / skill assessment)

**Output:** /path/to/output/{YYYY-MM-DD}-{Slug}/
```

Then use `AskUserQuestion` for explicit confirmation:

```
Question: "Ready to generate? You can also request changes first."
Header: "Confirm"
multiSelect: false
Options:
- Yes, let's go! Generate everything
- Wait, I want to change something (tell me what)
- Add more detail/context first (let me explain)
- Cancel, start over
```

**If user selects "Wait, I want to change something":**
- Ask what they'd like to modify
- Allow changes to: voice/style, articles, extras, specific instructions
- Re-display updated summary
- Ask for confirmation again

**Only after explicit "Yes" confirmation:** Use `TodoWrite` to track all deliverables and begin generation.

---

## Folder Structure

`index.html` is always a **container shell** (app shell with nav bar + iframe) — not the article itself. The primary article lives in its own file. Just open `index.html` in any browser to navigate the entire pack.

```
{output-directory}/{YYYY-MM-DD}-{Slug}/
├── assets/                                    # Generated images
│   ├── 01-{description}.png
│   ├── 02-{description}.png
│   └── ...
├── index.html                                 # Container shell (nav + iframe)
├── {YYYY-MM-DD} - {Title} - {ContentType}.html # All content pages (articles + extras)
├── {YYYY-MM-DD} - {Title} - Social Media Kit.html
├── {YYYY-MM-DD} - {Title} - Slide Deck.html
├── {YYYY-MM-DD} - {Title} - Newsletter.html
├── {YYYY-MM-DD} - {Title} - Thread.html
├── {YYYY-MM-DD} - {Title} - TL;DR.html
├── {YYYY-MM-DD} - {Title} - Press Release.html
├── {YYYY-MM-DD} - {Title} - Podcast Transcript.html
└── {YYYY-MM-DD} - {Title} - Prose Story.html
```

**Naming rules:**
- `index.html` is **always** the container shell — never an article
- The primary article uses a dated filename with its content type suffix (e.g., `2024-11-29 - Title - EN-Substack.html` or `2024-11-29 - Title - Release-Blog.html`)
- All deliverables (articles + extras) follow the same `{YYYY-MM-DD} - {Title} - {Suffix}.html` pattern
- The container shell's iframe defaults to loading the primary article

---

## Generation Process

### Articles

1. Generate primary article first (usually the full-voice version)
2. Save the primary article with a **dated filename** (e.g., `{YYYY-MM-DD} - {Title} - EN-Substack.html`) — NOT as `index.html`
3. Include image placeholders with prompts
4. Generate subsequent article variants by adapting voice/language
5. All articles reference same `assets/` folder

### Container Shell (index.html)

**REQUIRED:** After generating all deliverables, create `index.html` as an **app shell** — a lightweight page with a nav bar and an iframe that loads content pages. This eliminates nav duplication and gives the pack a polished, single-window experience.

**Architecture:**
- `index.html` is a dark-themed shell with a top nav bar + full-height iframe
- Nav links switch the iframe `src` — users never leave `index.html`
- The iframe defaults to loading the primary article
- Sub-pages stay clean (no nav code in them), but still work if opened directly
- Includes a loading spinner between page transitions
- Supports left/right arrow keyboard navigation

**Required HTML structure for `index.html`:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Pack Title} — Content Pack</title>
<style>
  :root {
    --shell-bg: #0f1117;
    --nav-bg: #161b22;
    --nav-border: #30363d;
    --text: #e6edf3;
    --text-muted: #8b949e;
    --accent: #0969da;
    --pill-bg: #21262d;
    --pill-hover: #30363d;
    --pill-active-bg: #0969da;
    --pill-active-text: #ffffff;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { height: 100%; overflow: hidden; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--shell-bg);
    color: var(--text);
    display: flex;
    flex-direction: column;
  }
  .shell-nav {
    background: var(--nav-bg);
    border-bottom: 1px solid var(--nav-border);
    padding: 0.65rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    flex-shrink: 0;
    z-index: 10;
  }
  .shell-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .shell-brand-icon { font-size: 1.1rem; }
  .shell-brand-text {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .shell-divider {
    width: 1px;
    height: 1.4rem;
    background: var(--nav-border);
    flex-shrink: 0;
  }
  .shell-links {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    align-items: center;
  }
  .shell-links a {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-muted);
    text-decoration: none;
    background: var(--pill-bg);
    border: 1px solid transparent;
    transition: all 0.15s ease;
    white-space: nowrap;
    cursor: pointer;
  }
  .shell-links a:hover {
    color: var(--text);
    background: var(--pill-hover);
    border-color: var(--nav-border);
  }
  .shell-links a.active {
    color: var(--pill-active-text);
    background: var(--pill-active-bg);
    border-color: var(--pill-active-bg);
    font-weight: 600;
  }
  .shell-links a .icon { font-size: 0.95rem; line-height: 1; }
  .shell-content {
    flex: 1;
    position: relative;
    overflow: hidden;
  }
  .shell-content iframe {
    width: 100%;
    height: 100%;
    border: none;
    background: #ffffff;
  }
  .shell-loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--shell-bg);
    z-index: 5;
    transition: opacity 0.3s ease;
  }
  .shell-loading.hidden { opacity: 0; pointer-events: none; }
  .shell-loading-spinner {
    width: 28px;
    height: 28px;
    border: 3px solid var(--nav-border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  @media (max-width: 640px) {
    .shell-nav { flex-wrap: wrap; gap: 0.5rem; padding: 0.5rem 0.75rem; }
    .shell-divider { display: none; }
    .shell-links { gap: 0.3rem; }
    .shell-links a { padding: 0.3rem 0.55rem; font-size: 0.75rem; }
  }
</style>
</head>
<body>

<nav class="shell-nav">
  <div class="shell-brand">
    <span class="shell-brand-icon">{emoji}</span>
    <span class="shell-brand-text">{Pack Title}</span>
  </div>
  <div class="shell-divider"></div>
  <div class="shell-links">
    <!-- Add one link per generated deliverable. First link gets class="active" -->
    <a href="#" data-page="{primary-article-filename}.html" class="active">
      <span class="icon">📰</span> Article
    </a>
    <a href="#" data-page="{dated-filename}-TLDR.html">
      <span class="icon">⚡</span> TL;DR
    </a>
    <!-- Include only links for deliverables that were actually generated -->
  </div>
</nav>

<div class="shell-content">
  <div class="shell-loading" id="loader">
    <div class="shell-loading-spinner"></div>
  </div>
  <iframe id="content-frame" src="{primary-article-filename}.html"></iframe>
</div>

<script>
(function() {
  const links = document.querySelectorAll('.shell-links a');
  const frame = document.getElementById('content-frame');
  const loader = document.getElementById('loader');
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const page = link.dataset.page;
      if (frame.src.endsWith(page)) return;
      links.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
      loader.classList.remove('hidden');
      frame.src = page;
    });
  });
  frame.addEventListener('load', () => { loader.classList.add('hidden'); });
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    const active = document.querySelector('.shell-links a.active');
    const all = Array.from(links);
    const idx = all.indexOf(active);
    if (e.key === 'ArrowRight' && idx < all.length - 1) all[idx + 1].click();
    else if (e.key === 'ArrowLeft' && idx > 0) all[idx - 1].click();
  });
})();
</script>

</body>
</html>
```

**Rules:**
- Only include nav links for deliverables that were actually generated
- The first nav link (primary article) gets `class="active"` by default
- The iframe's `src` defaults to the primary article filename
- Use relative paths — the folder must work via `file://` without a web server
- If there are multiple article variants, add separate nav links for each (e.g., "EN Article", "DE Article")
- The brand text should be a short, descriptive title for the content pack
- Sub-pages must NOT contain any nav elements — the shell handles all navigation

### Image Generation

#### Proactive Pre-flight Check

**BEFORE writing any articles** (i.e., right after the user confirms the pack configuration in Step 6), proactively check whether the OpenRouter API key is available:

```bash
# Check 1: Environment variable
echo "ENV_CHECK: ${OPENROUTER_API_KEY:+SET}"

# Check 2: Try to read from Claude settings (may have key but not loaded yet)
cat ~/.claude/settings.json 2>/dev/null | grep -o '"OPENROUTER_API_KEY"' || echo "NOT_IN_SETTINGS"

# Check 3: Verify it's not empty/whitespace
[ -n "${OPENROUTER_API_KEY// }" ] && echo "KEY_VALID" || echo "KEY_EMPTY_OR_MISSING"
```

**Interpret results:**
- If `ENV_CHECK: SET` AND `KEY_VALID` → Key is available
- If key is in settings but `KEY_EMPTY_OR_MISSING` → Key exists but needs restart
- If all checks fail → No key available

#### Image Strategy Decision

**Regardless of whether the user selected "AI-generated images" as an extra**, if the OpenRouter key IS available, proactively ask:

```
Question: "I detected an OpenRouter API key. Want me to generate images for the pack?"
Header: "Images"
Options:
- AI-generated images (OpenRouter — Gemini, FLUX models)
- Hand-crafted visuals (I'll use design skills to create SVG/HTML/CSS graphics natively)
- Skip images (text-only pack)
```

**If the key is NOT available**, still offer the native option:

```
Question: "No OpenRouter API key detected. How should I handle images?"
Header: "Images"
Options:
- Set up OpenRouter key now (I'll walk you through it)
- Hand-crafted visuals (I'll use design skills to create SVG/HTML/CSS graphics natively)
- Skip images (text-only pack)
```

#### Option A: AI-Generated Images (OpenRouter)

If user selects AI-generated images and the key is ready:

```bash
python ~/.claude/skills/article-pack/generate_images.py \
  --prompt "prompt from placeholder" \
  --output "{folder}/assets/01-name.png"
```

**Models** (`--model`):
| Model | Best For |
|-------|----------|
| `gemini` (default) | Text, infographics, editorial |
| `pro` | FLUX 2 Pro - stylized |
| `flex` | FLUX 2 Flex - photorealistic |

After generation, replace placeholders with `<figure><img>` tags.

#### Option A (setup needed): OpenRouter Key Setup

**Only if user chose "Set up OpenRouter key now".** Tell the user:

> "OpenRouter gives you access to multiple image models (Gemini, FLUX) through one API.
>
> **Get your free key:** https://openrouter.ai/keys
>
> Paste your key below (starts with `sk-or-`):"

After receiving the key, validate format:
```bash
[[ "$USER_KEY" =~ ^sk-or-.{20,}$ ]] && echo "FORMAT_OK" || echo "FORMAT_BAD"
```

Then ask where to save:

```
Question: "Where should I save this API key?"
Options:
- Claude Code settings (recommended - auto-loads every session)
- Shell profile (~/.bashrc or ~/.zshrc)
- This session only (won't persist)
- Cancel - skip image generation
```

**For Claude Code settings (recommended):**

```bash
SETTINGS_FILE="$HOME/.claude/settings.json"
mkdir -p ~/.claude
if [ -f "$SETTINGS_FILE" ]; then
    cat "$SETTINGS_FILE"
else
    echo '{}' > "$SETTINGS_FILE"
fi
```

Update the JSON to add the env key:
```json
{
  "env": {
    "OPENROUTER_API_KEY": "sk-or-v1-xxxxx"
  }
}
```

After saving to Claude settings, tell the user they need to restart Claude Code, then **stop the wizard** — don't continue without the key active.

**For shell profile:**

```bash
SHELL_RC="$HOME/.bashrc"
[ -n "$ZSH_VERSION" ] || [ "$SHELL" = "/bin/zsh" ] && SHELL_RC="$HOME/.zshrc"
grep -q "OPENROUTER_API_KEY" "$SHELL_RC" 2>/dev/null || \
  echo 'export OPENROUTER_API_KEY="sk-or-v1-xxxxx"' >> "$SHELL_RC"
source "$SHELL_RC"
```

**For session only:** `export OPENROUTER_API_KEY="sk-or-v1-xxxxx"` (warn: lost on close).

#### Option B: Hand-Crafted Visuals (Native Design Skills)

If user selects hand-crafted visuals, **before creating anything**, perform a skill assessment:

**Step 1: Scan for available design-related skills.**

Check which design-capable skills are currently available in the environment. Look for skills like `frontend-design`, `design-foundation`, or any skill with design/visual/UI capabilities.

**Step 2: Report the assessment to the user.**

Present a brief report of what you found:

```
## Design Skills Assessment

**Available:**
- `frontend-design` — Can create production-grade HTML/CSS/SVG graphics,
  diagrams, and visual components. Good for: hero banners, architecture
  diagrams, comparison charts, data visualizations.

**Not available:**
- No dedicated illustration or icon-design skills detected.

**My native capabilities:**
- HTML/CSS graphics (gradients, shapes, layouts)
- SVG diagrams and charts (flowcharts, architecture diagrams, data viz)
- CSS art and decorative elements
- Mermaid-style diagrams rendered as SVG

**Recommendation:** Between `frontend-design` and my native SVG/CSS capabilities,
I can create [hero banners, architecture diagrams, comparison charts] for this pack.
The output will be crisp vector graphics (SVG) or styled HTML — no raster artifacts.
```

Adapt the assessment honestly based on what's actually available. Be specific about what each skill can and can't do for image creation.

**Step 3: Ask user to confirm.**

```
Question: "Here's what I can do for visuals. Want me to proceed with these capabilities?"
Header: "Confirm"
Options:
- Yes, create visuals with these skills
- Actually, let me set up OpenRouter instead (switch to AI-generated)
- Skip images entirely
```

**Step 4: If confirmed, create the visuals.**

- Use available design skills (via Task tool) for complex graphics
- Fall back to native HTML/CSS/SVG generation for simpler graphics
- Save output as `.svg` or `.png` (screenshot SVG if PNG needed) in the `assets/` folder
- Replace image placeholders with `<figure><img>` tags pointing to the created assets
- Prefer SVG for diagrams/charts (crisp at any size) and raster only when photorealism is needed

**What to create (adapt to the article content):**
- Hero/banner image — visual identity for the article
- Architecture/flow diagrams — if the article discusses technical concepts
- Comparison charts — if the article compares features or options
- Data visualizations — if the article references metrics or statistics
- Quote cards — stylized pull-quotes as images

#### Skip Images

If user chooses to skip images:
- Continue with article pack generation
- Use placeholder comments instead of images: `<!-- IMAGE: [prompt description] -->`
- Note in completion summary: "Images skipped (user choice)"

### Social Media Kit

Dark-themed HTML with copy-to-clipboard buttons:
- Hashtags (per platform/language)
- Twitter/X posts (multiple variants)
- LinkedIn posts (per language)
- Threads posts (casual style)
- Opening hooks (labeled)
- Quotable lines

### Slide Deck

- Title slide
- Problem statement (1-2)
- Key insights (2-3)
- Evidence/examples (2-4)
- Predictions/implications (1-2)
- Discussion / CTA

### Email Newsletter

- Subject line options
- Preview text
- Body (adapted from article, more personal)
- CTA button text
- P.S. line

### Executive Summary (TL;DR)

- One-page card format
- Key takeaways (3-5 bullets)
- One quotable line
- "Read more" link placeholder

### Twitter/X Thread

- Hook tweet
- Numbered thread tweets (1/N format)
- Call to action tweet
- Self-reply with link

### Press Release

- Headline
- Dateline
- Lead paragraph (who, what, when, where, why)
- Body paragraphs
- Quote from author
- Boilerplate / About
- Contact info placeholder

### Quote Cards

- Generate 3-5 best quotes from article
- Create image prompts for each
- Simple, shareable format

### Podcast Transcript

NotebookLM-style two-host conversational dialogue.

**Host Personality Generator** 🎲

**IMPORTANT**: Use the dice roll script for true randomness:

```bash
# Quick archetype mode (default)
python3 ~/.claude/skills/article-pack/dice_roll.py --hosts 2

# Full 5-dimension personality mode
python3 ~/.claude/skills/article-pack/dice_roll.py --hosts 2 --mode full

# JSON output for programmatic use
python3 ~/.claude/skills/article-pack/dice_roll.py --hosts 2 --json
```

Alternatively, roll manually on each dimension for each host (or let user pick):

| Dimension | 1 | 2 | 3 | 4 | 5 | 6 |
|-----------|---|---|---|---|---|---|
| **Energy** | Chill & laid-back | Thoughtful | Warm | Enthusiastic | Hyped | Chaotic gremlin |
| **Expertise** | Total newbie | Curious learner | Informed amateur | Knowledgeable | Expert | World authority |
| **Style** | Analytical | Storyteller | Comedian | Philosopher | Skeptic | Devil's advocate |
| **Quirk** | Loves analogies | Goes on tangents | "But why though?" | Pop culture refs | Personal anecdotes | Conspiracy brain |
| **Vibe** | NPR host | Joe Rogan | Tech bro | Academic | Your smart friend | Unhinged genius |

**Example rolls:**
- Host A: Enthusiastic + Curious learner + Storyteller + Pop culture refs + Your smart friend
- Host B: Chill + Expert + Devil's advocate + "But why though?" + Academic

**Generation rules:**
- Natural conversation flow with interruptions, "mm-hmm", reactions
- Hosts stay in character based on their rolled traits
- Break down complex topics into digestible back-and-forth
- Include moments of humor, surprise, tangents that circle back
- End with key takeaways summarized conversationally
- Ready to feed into text-to-speech or NotebookLM

**Structure:**
```
[INTRO MUSIC]

HOST A (Enthusiastic Storyteller): Okay okay okay, so you know how everyone's
been losing their minds about AI lately?

HOST B (Chill Devil's Advocate): *sighs* Which part? The benchmarks discourse
or the actual interesting stuff nobody's talking about?

HOST A: SEE, that's exactly what we're getting into today...

[Continue natural dialogue covering all article points]

[OUTRO]
```

### Prose Story

Creative narrative that weaves the article's themes into fiction:
- Create characters and a scenario that embody the topic
- Show don't tell — demonstrate concepts through story
- Can be: short story, parable, day-in-the-life, future scenario, allegory
- Maintain the core insights while making them emotionally resonant
- Include a subtle "moral" or takeaway woven into the narrative
- Tone adapts to article topic (tech thriller, slice-of-life, speculative fiction, etc.)

Example approaches:
- AI trends article → Story of a developer navigating the 2026 landscape
- Productivity piece → Day in the life before/after adopting the method
- Business insight → Boardroom drama illustrating the concept
- Technical concept → Sci-fi scenario exploring implications

---

## Voice Calibration

### Reference Folder (custom voice)
- Extracted from user's existing content (articles, tweets, style guides)
- Voice profile with tone, sentence patterns, vocabulary, signature moves
- Applied as the baseline voice across all deliverables
- Platform-specific adaptations still apply (social is punchier than long-form)
- Stored in memory for reuse in future packs

### Opinionated & Direct
- Strong opinions, clear positions
- Personal anecdotes
- No hedging
- Signature sign-off

### Professional
- Same insights, measured tone
- Business-appropriate
- Thought-leadership framing
- Formal pronouns for German ("Sie")

### Academic
- Thorough, well-referenced
- Balanced perspectives
- Technical precision
- Formal structure

### Casual
- Conversational, friendly
- Simple language
- Relatable examples
- Approachable tone

---

## Completion Summary

```
## Article Pack Complete ✅

### Entry Point
→ Open index.html in any browser (container shell with nav — loads all content in-place)

### Articles Generated
1. {dated} - EN-Substack.html (2,400 words, full voice) ← default in shell
2. {dated} - DE-LinkedIn.html (1,800 words, professional)

### Additional Content
- Social Media Kit.html (12 posts, 3 languages)
- Slide Deck.html (12 slides)
- Podcast Transcript.html (15 min read, 2 hosts)
- Prose Story.html (short story, ~1500 words)
- assets/01-hero.png
- assets/02-diagram.png
- assets/03-quote.png

### Container Shell
- index.html (app shell with nav bar + iframe, keyboard nav, loading spinner)

### Output Location
/path/to/2024-11-29-Article-Title/

### Next Steps
- [ ] Open index.html to review the full pack
- [ ] Zip the folder and share with stakeholders
- [ ] Upload images to platforms
- [ ] Schedule social posts
- [ ] Send newsletter
```

---

## Example Wizard Session

```
User: "Generate an article-pack based on this draft about AI trends"

Claude: "Great! Let me walk you through the setup.

I see this is about AI trends for 2026 - covering software engineering
bifurcation, agent risks, world models, robotics, and taste as a moat.

[Checks memory for voice context - finds author style notes]

Step 1 of 4: How many article versions do you need?"

User: Selects "2 articles"

Claude: "Step 2 of 4: Article 1 - What language, style, and platform?"

User: Selects "English / Full voice / Substack"

Claude: "Step 3 of 4: Article 2 - What language, style, and platform?"

User: Selects "German / Professional / LinkedIn"

Claude: "Step 4 of 4: What additional content do you want?"

User: Selects "Social media kit" + "Slide deck"

Claude: "Perfect! Here's your configuration:
[Shows summary]
Ready to generate?"

User: "Yes"

Claude: [Checks OpenRouter key → found! Asks about image strategy]
Claude: "I detected an OpenRouter API key. Want me to generate images?"

User: Selects "AI-generated images (OpenRouter)"

Claude: [Creates TodoWrite, generates articles, then images, then extras, reports completion]
```
