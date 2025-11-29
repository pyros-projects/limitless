# Article Pack

**Transform research into publish-ready content across platforms, languages, and formats.**

The `article-pack` skill is an interactive wizard that generates complete content packages from your notes, drafts, or research materials. Get articles, social posts, slide decks, podcast scripts, and more — all calibrated to your voice.

---

## Quick Start

Just say:
```
article-pack
```

Or describe what you want:
```
Turn my AI research notes into a Substack article and LinkedIn post
```

The wizard guides you through the rest.

---

## What You Get

| Content Type | Description |
|--------------|-------------|
| **Articles** | Platform-optimized pieces (Substack, LinkedIn, Medium, blogs) |
| **Social Media Kit** | Tweets, LinkedIn posts, hashtags, hooks with copy buttons |
| **Slide Deck** | Presentation-ready slides |
| **Twitter/X Thread** | Threaded format with hooks |
| **Email Newsletter** | Subject lines, preview text, CTA |
| **Executive Summary** | TL;DR card format |
| **Press Release** | Full press release structure |
| **Quote Cards** | Shareable image quotes |
| **Podcast Transcript** | Two-host dialogue (NotebookLM-style) |
| **Prose Story** | Creative narrative around your topic |
| **AI Images** | Hero images, diagrams, illustrations |

---

## Wizard Flow

### Step 0: Content Sufficiency Check
Before anything else, Claude analyzes whether there's enough material to create a meaningful article pack:

**If sufficient content exists:**
- Proceeds to Step 1

**If content is thin or missing:**
- Explains what's lacking (depth, examples, data, perspectives)
- Recommends web research to fill gaps
- Offers to help research specific angles
- Loops back when ready

This means you can start with just a topic idea and use the skill for **research-first workflows**:

```
User: "article-pack about quantum computing breakthroughs in 2024"

Claude: "I don't have enough material yet for a solid article pack.
To create compelling content, we'd need:
- Recent breakthrough announcements (IBM, Google, etc.)
- Technical context on what makes these significant
- Expert perspectives or quotes
- Implications for industry/society

Want me to research these areas first? I can search the web
and compile findings until we have enough for a strong pack."
```

---

### Step 1: Source & Voice
Summarizes your material and detects (or asks about) your writing style:
- **Opinionated & direct** — hot takes, strong positions
- **Professional & measured** — thought leadership
- **Academic & thorough** — detailed, referenced
- **Casual & conversational** — friendly, accessible

### Step 2: Article Count
Choose how many article versions you need (1–4+).

### Step 3: Configure Each Article
For each article, specify:
- **Language**: English, German, French, Spanish, Other
- **Style**: Full voice, Professional, Academic, Casual
- **Platform**: Substack, LinkedIn, Medium, Company blog, Newsletter

### Step 4: Additional Content
Select extras from three batches:
- Social media kit, AI images, slide deck, thread
- Newsletter, TL;DR, press release, quote cards
- Podcast transcript, prose story

### Step 5: Output Location
Choose where to save the pack.

### Step 6: Review & Confirm
See the full configuration summary and confirm before generation.

---

## Output Structure

```
{YYYY-MM-DD}-{Slug}/
├── assets/
│   ├── 01-hero.png
│   ├── 02-diagram.png
│   └── ...
├── {Date} - {Title} - EN-Substack.html
├── {Date} - {Title} - DE-LinkedIn.html
├── {Date} - {Title} - Social Media Kit.html
├── {Date} - {Title} - Slide Deck.html
├── {Date} - {Title} - Newsletter.html
├── {Date} - {Title} - Thread.html
├── {Date} - {Title} - TL;DR.html
├── {Date} - {Title} - Press Release.html
├── {Date} - {Title} - Podcast Transcript.html
└── {Date} - {Title} - Prose Story.html
```

---

## Voice Styles

| Style | Characteristics |
|-------|-----------------|
| **Full Voice** | Strong opinions, personal anecdotes, no hedging, signature sign-off |
| **Professional** | Same insights, measured tone, business-appropriate, formal pronouns |
| **Academic** | Thorough, well-referenced, balanced perspectives, technical precision |
| **Casual** | Conversational, simple language, relatable examples |

---

## AI Image Generation

Uses OpenRouter to generate images via multiple models:

```bash
python skills/generate_images.py \
  --prompt "your image prompt" \
  --output path/to/image.png \
  --model gemini
```

| Model | Best For |
|-------|----------|
| `gemini` (default) | Text, infographics, editorial illustrations |
| `pro` | FLUX 2 Pro — stylized, illustrated |
| `flex` | FLUX 2 Flex — photorealistic |

Requires `OPENROUTER_API_KEY` environment variable.

---

## Podcast Host Generator 🎲

For podcast transcripts, the skill generates random host personalities for natural, engaging dialogue.

```bash
# Quick archetype mode (default)
python skills/dice_roll.py --hosts 2

# Full 5-dimension personality mode
python skills/dice_roll.py --hosts 2 --mode full

# JSON output
python skills/dice_roll.py --hosts 2 --json
```

### Personality Dimensions (d6 each)

| Dimension | 1 | 2 | 3 | 4 | 5 | 6 |
|-----------|---|---|---|---|---|---|
| **Energy** | Chill | Thoughtful | Warm | Enthusiastic | Hyped | Chaotic gremlin |
| **Expertise** | Total newbie | Curious learner | Informed amateur | Knowledgeable | Expert | World authority |
| **Style** | Analytical | Storyteller | Comedian | Philosopher | Skeptic | Devil's advocate |
| **Quirk** | Loves analogies | Goes on tangents | "But why?" | Pop culture refs | Personal anecdotes | Conspiracy brain |
| **Vibe** | NPR host | Joe Rogan | Tech bro | Academic | Your smart friend | Unhinged genius |

### Example Archetypes
- **Grumpy professor**: Chill + Expert + Skeptic + "But why?" + Academic
- **Caffeinated intern**: Hyped + Curious learner + Storyteller + Pop culture refs + Your smart friend
- **Devil's advocate**: Thoughtful + Knowledgeable + Devil's advocate + "But why?" + Philosopher

---

## Example Session

```
User: "article-pack based on my AI trends research"

Claude: "I see this covers AI trends for 2026 — software engineering
bifurcation, agent risks, world models, robotics, and taste as moat.

Step 1: How many article versions?"

User: "2"

Claude: "Article 1 — language, style, platform?"

User: "English / Full voice / Substack"

Claude: "Article 2?"

User: "German / Professional / LinkedIn"

Claude: "What extras?"

User: "Social media kit + AI images + podcast transcript"

Claude: "Here's your config:
  Articles: EN-Substack (full voice), DE-LinkedIn (professional)
  Extras: Social kit, images, podcast (hosts will be dice-rolled!)
  Output: ./2024-11-29-AI-Trends-2026/

Ready to generate?"

User: "Yes"

Claude: [Generates everything, reports completion]
```

---

## Completion Summary

```
## Article Pack Complete ✅

### Articles
1. EN-Substack.html (2,400 words, full voice)
2. DE-LinkedIn.html (1,800 words, professional)

### Extras
- Social Media Kit.html (12 posts)
- Podcast Transcript.html (15 min, 2 hosts)
- assets/01-hero.png
- assets/02-diagram.png

### Output
./2024-11-29-AI-Trends-2026/

### Next Steps
- [ ] Review and edit articles
- [ ] Upload images to platforms
- [ ] Schedule social posts
```

---

## Trigger Phrases

The skill activates when you:
- Say "article-pack" or "content pack"
- Want to turn research/notes into publishable articles
- Ask for "Substack article", "LinkedIn post", or similar
- Request multi-platform content creation
- Need social media promotion materials
- Want to **research a topic** and turn it into content
- Have a topic idea but need help gathering material first
