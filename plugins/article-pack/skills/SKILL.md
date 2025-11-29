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

```
Question: "How would you describe your writing style?"
Options:
- Opinionated & direct (hot takes, strong positions)
- Professional & measured (thought leadership)
- Academic & thorough (detailed, referenced)
- Casual & conversational (friendly, accessible)
```

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

```
Question: "What additional content do you want?"
Header: "Extras"
multiSelect: true
Options (present all 10):
1. Social media kit (tweets, LinkedIn posts, hashtags, hooks)
2. AI-generated images (hero + section images)
3. Slide deck (presentation version)
4. Twitter/X thread (standalone thread format)
5. Email newsletter version
6. Executive summary (TL;DR card)
7. Press release
8. Quote cards (shareable image quotes)
9. Podcast transcript (NotebookLM-style two-host dialogue)
10. Prose story (creative narrative woven around the topic)
```

Note: AskUserQuestion only supports 4 options max, so present in batches:

**Batch 1 (Core):**
- Social media kit
- AI-generated images
- Slide deck
- Twitter/X thread

**Batch 2 (Distribution):**
- Email newsletter
- Executive summary (TL;DR)
- Press release
- Quote cards

**Batch 3 (Creative):**
- Podcast transcript (with dice-rolled hosts!)
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
- AI-generated images
- Podcast transcript (hosts will be dice-rolled!)
- Prose story

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

```
{output-directory}/{YYYY-MM-DD}-{Slug}/
├── assets/                                    # Generated images
│   ├── 01-{description}.png
│   ├── 02-{description}.png
│   └── ...
├── {YYYY-MM-DD} - {Title} - EN-Substack.html # Article 1
├── {YYYY-MM-DD} - {Title} - DE-LinkedIn.html # Article 2
├── {YYYY-MM-DD} - {Title} - Social Media Kit.html
├── {YYYY-MM-DD} - {Title} - Slide Deck.html
├── {YYYY-MM-DD} - {Title} - Newsletter.html
├── {YYYY-MM-DD} - {Title} - Thread.html
├── {YYYY-MM-DD} - {Title} - TL;DR.html
├── {YYYY-MM-DD} - {Title} - Press Release.html
├── {YYYY-MM-DD} - {Title} - Podcast Transcript.html
└── {YYYY-MM-DD} - {Title} - Prose Story.html
```

---

## Generation Process

### Articles

1. Generate primary article first (usually the full-voice version)
2. Include image placeholders with prompts
3. Generate subsequent articles by adapting voice/language
4. All articles reference same `assets/` folder

### Image Generation

#### Pre-flight: API Key Check

**BEFORE attempting any image generation**, verify the OpenRouter API key exists. Run ALL of these checks to be certain:

```bash
# Check 1: Environment variable
echo "ENV_CHECK: ${OPENROUTER_API_KEY:+SET}"

# Check 2: Try to read from Claude settings (may have key but not loaded yet)
cat ~/.claude/settings.json 2>/dev/null | grep -o '"OPENROUTER_API_KEY"' || echo "NOT_IN_SETTINGS"

# Check 3: Verify it's not empty/whitespace
[ -n "${OPENROUTER_API_KEY// }" ] && echo "KEY_VALID" || echo "KEY_EMPTY_OR_MISSING"
```

**Interpret results:**
- If `ENV_CHECK: SET` AND `KEY_VALID` → Key is ready, proceed to image generation
- If key is in settings but `KEY_EMPTY_OR_MISSING` → User needs to restart Claude Code
- If all checks fail → Key is missing, run setup flow

#### API Key Setup Flow

**Only run this if the key is confirmed missing.** Tell the user:

> "🔑 Image generation requires an OpenRouter API key.
> 
> OpenRouter gives you access to multiple image models (Gemini, FLUX) through one API.
> 
> **Get your free key:** https://openrouter.ai/keys
> 
> Paste your key below (starts with `sk-or-`):"

After receiving the key, validate format:
```bash
# Key should start with sk-or- and be reasonably long
[[ "$USER_KEY" =~ ^sk-or-.{20,}$ ]] && echo "FORMAT_OK" || echo "FORMAT_BAD"
```

If format looks wrong, ask user to double-check they copied the full key.

**Then ask where to save:**

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
# Read existing settings or create empty object
SETTINGS_FILE="$HOME/.claude/settings.json"
mkdir -p ~/.claude

if [ -f "$SETTINGS_FILE" ]; then
    # File exists - check if it has env section
    cat "$SETTINGS_FILE"
else
    # Create new settings file
    echo '{}' > "$SETTINGS_FILE"
fi
```

Then update the JSON to add/merge the env key. The resulting file should look like:
```json
{
  "env": {
    "OPENROUTER_API_KEY": "sk-or-v1-xxxxx"
  }
}
```

**Important:** After saving to Claude settings, tell the user:

> "✅ API key saved to Claude Code settings.
> 
> **You need to restart Claude Code** for the key to load.
> 
> After restart, run `article-pack` again and image generation will work!"

Then **stop the wizard** - don't continue without the key active.

**For shell profile:**

```bash
# Detect shell
SHELL_RC="$HOME/.bashrc"
[ -n "$ZSH_VERSION" ] || [ "$SHELL" = "/bin/zsh" ] && SHELL_RC="$HOME/.zshrc"

# Append export (avoid duplicates)
grep -q "OPENROUTER_API_KEY" "$SHELL_RC" 2>/dev/null || \
  echo 'export OPENROUTER_API_KEY="sk-or-v1-xxxxx"' >> "$SHELL_RC"

# Source it for current session
source "$SHELL_RC"

# Verify
echo $OPENROUTER_API_KEY
```

**For session only:**

```bash
export OPENROUTER_API_KEY="sk-or-v1-xxxxx"
```

Warn the user: "This key will be lost when you close Claude Code."

#### Image Generation (after key verified)

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

#### Fallback if No Key

If user chooses "Cancel - skip image generation":
- Continue with article pack generation
- Use placeholder comments instead of images: `<!-- IMAGE: [prompt description] -->`
- Note in completion summary: "Images skipped (no API key)"

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

### Full Voice
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

### Articles Generated
1. EN-Substack.html (2,400 words, full voice)
2. DE-LinkedIn.html (1,800 words, professional)

### Additional Content
- Social Media Kit.html (12 posts, 3 languages)
- Slide Deck.html (12 slides)
- Podcast Transcript.html (15 min read, 2 hosts)
- Prose Story.html (short story, ~1500 words)
- assets/01-hero.png
- assets/02-diagram.png
- assets/03-quote.png

### Output Location
/path/to/2024-11-29-Article-Title/

### Next Steps
- [ ] Review and edit articles
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

User: Selects "Social media kit" + "AI-generated images"

Claude: "Perfect! Here's your configuration:
[Shows summary]
Ready to generate?"

User: "Yes"

Claude: [Creates TodoWrite, generates everything, reports completion]
```
