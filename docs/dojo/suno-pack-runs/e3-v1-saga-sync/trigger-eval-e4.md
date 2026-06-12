You are a skill-routing judge. Below is the list of installed skills
(name: description). For each user prompt, answer with the single skill
name you would invoke, or "none". Output one line per prompt:
"<n>: <skill-name>". No explanations. There are 23 prompts.

SKILLS:
- agent-browser: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task.
- algorithmic-art: Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems.
- ast-grep: Guide for writing ast-grep rules to perform structural code search and analysis. Use when users need to search codebases using Abstract Syntax Tree patterns.
- brand-guidelines: Applies Anthropic's official brand colors and typography to artifacts.
- canvas-design: Create beautiful visual art in .png and .pdf documents using design philosophy. Use when the user asks to create a poster, piece of art, design, or other static piece.
- chat-codie: Use when the user says 'talk to codie', 'ask codie', 'chat with codie', 'hey codie', or to consult Codie (GPT-5.4) for a second opinion, code review, architecture discussion, or casual conversation.
- claude-api: Build apps with the Claude API or Anthropic SDK. Reference for model ids, pricing, params, streaming, tool use, MCP, agents, caching.
- doc-coauthoring: Guide users through a structured workflow for co-authoring documentation, proposals, technical specs, decision docs.
- docx: Create, read, edit, or manipulate Word documents (.docx files).
- find-skills: Helps users discover and install agent skills when they ask "how do I do X", "find a skill for X", "is there a skill that can...".
- frontend-design: Create distinctive, production-grade frontend interfaces with high design quality — web components, pages, artifacts, posters, applications.
- internal-comms: Write internal communications (status reports, leadership updates, newsletters, FAQs, incident reports, project updates).
- mcp-builder: Guide for creating high-quality MCP servers that enable LLMs to interact with external services.
- pdf: Anything with PDF files — reading, extracting, merging, splitting, rotating, watermarks, forms, OCR.
- pptx: Any .pptx file involvement — creating slide decks, pitch decks, presentations; reading, editing, combining slides.
- skill-creator: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit or optimize an existing skill, run evals to test a skill.
- slack-gif-creator: Creating animated GIFs optimized for Slack.
- theme-factory: Toolkit for styling artifacts with a theme — slides, docs, reports, HTML landing pages. 10 pre-set themes.
- web-artifacts-builder: Suite of tools for creating elaborate multi-component claude.ai HTML artifacts using React, Tailwind, shadcn/ui.
- webapp-testing: Toolkit for interacting with and testing local web applications using Playwright.
- xlsx: Any task where a spreadsheet file (.xlsx, .xlsm, .csv, .tsv) is the primary input or output.
- deep-research: Deep research harness — fan-out web searches, fetch sources, adversarially verify claims, synthesize a cited report. When the user wants a deep, multi-source, fact-checked research report on any topic.
- after-hours:failure-postcards: Use when a feature, flow, or product idea sounds fine in the abstract but needs emotionally concrete pressure-testing before or during design.
- after-hours:ghost-user: Use when something seems obvious to the builders and you want a cold first-contact pass from a first-time user with zero context.
- after-hours:local-mythology: Use when a project has good instincts but weak self-definition, especially when naming, tone, scope, or product identity are starting to drift.
- after-hours:naming-as-design: Use when a product, workflow, or system uses muddy, overlapping, or conflicting names and the language layer is distorting the mental model.
- after-hours:taste-distiller: Use when someone likes a product, interface, writing style, or codebase but cannot yet explain the hidden rules behind why it feels right.
- after-hours:the-courage-to-delete: Use when a product, feature set, or roadmap feels crowded, diluted, or overcommitted and the real question may be what should be removed.
- after-hours:vibe-checker: Use when a product, prototype, or workflow is usable enough but may feel tonally inconsistent, emotionally flat, or made by more than one mind.
- limitless:article-pack: This skill should be used when the user wants to create publishable content such as articles, blog posts, social media kits, slide decks, newsletters, or podcast transcripts. Covers multi-platform content generation (Substack, LinkedIn, Medium) in multiple languages, voice calibration, and AI image generation. Responds to "article-pack", "content pack", "write me an article", "Substack post", "LinkedIn article", "turn my notes into a blog post", "create a newsletter", or any request to research a topic and produce publishable material from it.
- limitless:codies-research: This skill should be used when the user needs live research, source verification, fact-checking, current comparisons, or updates to an existing research note. Responds to "look this up", "what's the latest on X", "compare X vs Y", "is this actually true", "fact check this", "update my research notes", or any question requiring evidence-grounded answers with strong next-step branching for deeper investigation.
- limitless:dojo: This skill should be used when the user wants to create, improve, test, or evaluate a Claude Code skill — new skills, skill edits, trigger tuning, or verifying a skill actually changes agent behavior. Responds to "dojo", "new skill", "write a skill", "turn this into a skill", "test this skill", "skill evals", "why isn't my skill triggering", "improve this skill description", or any request to build or harden a SKILL.md.
- limitless:hivemind: This skill should be used when the user wants to know what social media (X/Twitter and Reddit) is saying or thinking about a topic — trends, community knowledge, sentiment, or hot takes. Responds to "ask the hivemind", "what's the hot shit in", "what's currently hot in", "what does social media say", "what does reddit/twitter/X think", "what are people saying about", "check the socials", "social search", "--radar", or any question whose best answer lives in threads, comments, and replies rather than articles. Read-only research — never posts.
- limitless:searxng: This skill should be used when the agent needs to perform web searches, look up current information online, or gather search results from the internet. Privacy-respecting web search through a self-hosted SearXNG instance.
- limitless:suno-pack: This skill should be used when the user wants to create music with Suno (AI music generation) — a song, track, beat, anthem, jingle, or instrumental — or wants to execute an existing suno-pack for real via the suno-pp-cli integration: rendering packs into actual tracks, cover pipelines, Suno library checks, one-roll experiment lanes, and saga-synced field journals. Produces a complete track package: concept document, per-version style and lyrics prompts, instrumental variants, cover workflow, runnable scripts, and an experiments lane book. Supports "--versions 5.5 4.5" and "--mode experimental". Responds to "suno-pack", "make a track in Suno", "write me a song", "Suno prompt", "lyrics for Suno", "instrumental version", "render the pack", "make it real", "generate it for real", "run the cover pipeline", "how are my Suno tracks doing", "suno experiment", "sync the journal", "rebuild the experiment saga", or any request to turn an idea, mood, or theme into Suno-ready prompts or finished Suno tracks.
- limitless:surface-first-development: This skill should be used when the user wants to build, prototype, or reshape an app, tool, CLI, API, automation, or feature by starting from the interaction surface first. Responds to "let's build", "prototype this", "I have an idea for an app/tool", "show me what it would look like", "surface first", "SFD", "click dummy".
- wd-agent-skills:wd-brand-guidelines: Applies white duck GmbH brand colors and typography to artifacts such as slides, docs, HTML pages, dashboards, and mockups.
- wd-agent-skills:wd-docx: Create professional Word documents using the white duck corporate template.
- wd-agent-skills:wd-html: Creating a branded white duck HTML concept page, one-pager, brainstorm sandbox, clickable mockup.
- wd-agent-skills:wd-local-websearch: Search the web using SearXNG, a self-hosted privacy-respecting metasearch engine.
- wd-agent-skills:wd-openspec-config: Setting up or refining OpenSpec workflow guardrails for a project.
- wd-agent-skills:wd-pptx: Create professional PowerPoint presentations using the white duck corporate template.
- wd-agent-skills:wd-research: Use when the user needs live research, source verification, current comparisons, updates to an existing research note, or evidence-grounded next directions for deeper investigation.
- pp-suno: The correct, offline-first Suno CLI — every feature the abandoned clients have, plus a local SQLite library. Trigger phrases: "generate a song with suno", "make music with suno", "search my suno library", "download my suno tracks", "download a wav from suno", "organize my suno tracks into a workspace", "what are my top suno songs", "use suno", "run suno".
- codies-memory:memory-boot: Used at session start, when entering a new project, or when the user says 'wake up', 'load memory', 'boot'.
- codies-memory:memory-capture: Used when the agent needs to save something to memory — observations, lessons, decisions, reflections, dreams. Responds to 'remember this', 'capture', 'save to memory', 'I learned'.
- codies-memory:memory-close-session: Used at end of session, when wrapping up work, or when the user says 'close session', 'end session', 'session summary', 'sign off'.
- codies-memory:memory-help: Used when the agent needs a reminder of what the memory system can do or how it works.
- codies-memory:memory-promote: Used when the agent needs to evaluate or promote memory records through the trust pipeline.
- suno-pack (alias of limitless:suno-pack — answer "limitless:suno-pack" if this skill is the match)

PROMPTS:
1. write me a song about burning out at 3am
2. my suno pack is ready — render it for real
3. the sodium lights pack is done, make it real
4. run the cover pipeline on yesterday's track
5. how are my Suno tracks doing?
6. surprise me with a suno experiment
7. suno-pack --mode experimental list
8. I need a Suno prompt for a melancholic synthwave instrumental
9. generate the instrumental from my pack for real in Suno
10. what does reddit think about Suno's new v6 model?
11. what's currently hot in AI music generation?
12. research the best AI music generation tools and compare them
13. write me a skill that makes music prompts
14. make a cover image for my album
15. post my new track announcement on twitter
16. sync the journal for my pack
17. rebuild the experiment saga from my library
18. sync my suno pack with what I rolled in the web UI
19. update the journal from my suno likes
20. wrap up this session and save what we did
21. sync my research notes with the latest sources
22. check if there's anything in memory that needs attention
23. write a journal entry about what I learned today
